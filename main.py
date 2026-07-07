from fastapi import UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi import Request
from fastapi.responses import HTMLResponse
from auth.auth import get_current_user
from db.models import User, ImageTrivia
from services.aws_file_utils import upload_and_get_presigned_url
from services.default_pdfs import get_default_pdf_bytes
from services.trivia_generator import generate_trivia_from_pdf
from services.i18n import get_lang, translate, js_strings
from games.games import create_game, get_db
from fastapi import FastAPI, Form, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session, load_only
from auth.auth import get_password_hash, verify_password, create_access_token
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
from auth.auth import get_current_user_optional

import os
import uuid
import threading
from db.db import SessionLocal
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth
from dotenv import load_dotenv
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
# Removed jinja2 Environment imports and custom class

load_dotenv() # Load environment variables from .env file

MAX_NUM_QUESTIONS = 50
MAX_PDF_BYTES = 10 * 1024 * 1024
ALLOWED_DIFFICULTIES = {"easy", "medium", "hard", "progressive"}
SCORES_PAGE_SIZE = 25
USERNAME_MIN = 3
USERNAME_MAX = 30
EMAIL_MAX = 254
PASSWORD_MIN = 6
PASSWORD_MAX = 72


def clamp_num_questions(value: int) -> int:
    return max(1, min(value, MAX_NUM_QUESTIONS))


def clean_difficulty(value: str) -> str:
    return value if value in ALLOWED_DIFFICULTIES else "medium"


def public_trivia(trivia):
    return [
        {"question": q.get("question"), "options": q.get("options", [])}
        for q in (trivia or [])
    ]


TRIVIA_JOBS = {}
JOBS_LOCK = threading.Lock()
FIRST_BATCH = 3


def _bg_generate(job_id, file_bytes, remaining, lang, difficulty, exclude, game_id):
    try:
        more = generate_trivia_from_pdf(
            file_bytes, num_questions=remaining, lang=lang,
            difficulty=difficulty, exclude_questions=exclude,
        )
    except Exception:
        more = []
    with JOBS_LOCK:
        job = TRIVIA_JOBS.get(job_id)
        existing = list(job["questions"]) if job else []
    full = existing + more
    if game_id is not None and more:
        db = SessionLocal()
        try:
            game = db.query(ImageTrivia).filter(ImageTrivia.id == game_id).first()
            if game:
                game.trivia = full
                db.commit()
        finally:
            db.close()
    with JOBS_LOCK:
        job = TRIVIA_JOBS.get(job_id)
        if job:
            job["questions"] = full
            job["done"] = True


def _run_generation(file_bytes, key, num_questions, lang, difficulty, user_id, db):
    stream = difficulty != "progressive" and num_questions > FIRST_BATCH
    first_n = FIRST_BATCH if stream else num_questions
    first_trivia = generate_trivia_from_pdf(file_bytes, num_questions=first_n, lang=lang, difficulty=difficulty)
    if not first_trivia:
        return [], None, None, 0
    game_id = None
    if user_id is not None:
        game = create_game(user_id=user_id, file_key=key, trivia=first_trivia, db=db)
        game_id = game.id
    if not stream:
        return first_trivia, game_id, None, len(first_trivia)
    job_id = str(uuid.uuid4())
    with JOBS_LOCK:
        TRIVIA_JOBS[job_id] = {
            "questions": list(first_trivia),
            "total": num_questions,
            "done": False,
            "game_id": game_id,
        }
    threading.Thread(
        target=_bg_generate,
        args=(job_id, file_bytes, num_questions - len(first_trivia), lang, difficulty,
              [q["question"] for q in first_trivia], game_id),
        daemon=True,
    ).start()
    return first_trivia, game_id, job_id, num_questions


async def read_pdf_within_limit(request: Request, file: UploadFile) -> bytes:
    if file.size is not None and file.size > MAX_PDF_BYTES:
        raise HTTPException(status_code=413, detail=translate("error.file_too_large", get_lang(request)))
    file_bytes = await file.read()
    if len(file_bytes) > MAX_PDF_BYTES:
        raise HTTPException(status_code=413, detail=translate("error.file_too_large", get_lang(request)))
    return file_bytes


limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="PDF Trivia Generator",
    description="Upload a PDF or play the default Alice in Wonderland story to generate GPT-powered trivia. Supports guest play and registered users with score tracking.",
    version="1.1.0",
    openapi_tags=[
        {"name": "pages", "description": "HTML pages"},
        {"name": "auth", "description": "Login, registration, and Google OAuth"},
        {"name": "upload", "description": "PDF upload and trivia generation (logged in)"},
        {"name": "guest", "description": "Guest play without login or score saving"},
        {"name": "scores", "description": "Game scores"},
    ],
)
app.state.limiter = limiter


@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    from fastapi.responses import JSONResponse
    return JSONResponse(
        status_code=429,
        content={"detail": translate("error.rate_limited", get_lang(request))},
    )


app.mount("/static", StaticFiles(directory="static"), name="static")

# Revert to the simplest Jinja2Templates initialization
templates = Jinja2Templates(directory="templates")


def render_template(request: Request, name: str, context: dict = None, status_code: int = 200):
    lang = get_lang(request)
    ctx = {
        "lang": lang,
        "dir": "rtl" if lang == "he" else "ltr",
        "t": lambda key, **kw: translate(key, lang, **kw),
        "i18n_js": js_strings(lang),
    }
    if context:
        ctx.update(context)
    return templates.TemplateResponse(request, name, ctx, status_code=status_code)

# Explicitly disable Jinja2's cache to work around the TypeError
# This line is now removed as it didn't prevent the error and the issue is earlier in the call stack.
# templates.env.cache = None

CONTENT_SECURITY_POLICY = (
    "default-src 'self'; "
    "script-src 'self' 'unsafe-inline'; "
    "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
    "font-src 'self' https://fonts.gstatic.com; "
    "img-src 'self' data: https://www.gstatic.com https://static.rolex.com; "
    "frame-src https://static.rolex.com; "
    "connect-src 'self'; "
    "frame-ancestors 'self'; "
    "base-uri 'self'; "
    "form-action 'self'"
)


@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["Content-Security-Policy"] = CONTENT_SECURITY_POLICY
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response


app.add_middleware(SessionMiddleware, secret_key=os.getenv("SESSION_SECRET"))

oauth = OAuth()
oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"}
)

@app.get("/login/google", tags=["auth"], summary="Start Google OAuth")
async def login_google(request: Request):
    if not os.getenv("GOOGLE_CLIENT_ID") or not os.getenv("GOOGLE_CLIENT_SECRET"):
        return RedirectResponse(url="/login?error=google_not_configured", status_code=302)
    redirect_uri = request.url_for("auth_google_callback")
    return await oauth.google.authorize_redirect(request, redirect_uri)

@app.get("/auth/google/callback", name="auth_google_callback", tags=["auth"], summary="Google OAuth callback")
async def auth_google_callback(request: Request, db: Session = Depends(get_db)):
    token = await oauth.google.authorize_access_token(request)
    userinfo = await oauth.google.userinfo(token=token)
    email = userinfo.get("email")
    name = userinfo.get("name") or (email.split("@")[0] if email else None)
    if not email:
        return RedirectResponse(url="/login", status_code=302)
    user = db.query(User).filter(User.email == email).first()
    if not user:
        username_base = (name or email.split("@")[0]).replace(" ", "").lower()
        username = username_base
        i = 1
        while db.query(User).filter(User.username == username).first():
            i += 1
            username = f"{username_base}{i}"
        user = User(username=username, email=email, hashed_password="oauth-google")
        db.add(user)
        db.commit()
        db.refresh(user)
    jwt_token = create_access_token({"sub": user.username})
    resp = RedirectResponse(url="/", status_code=302)
    resp.set_cookie(key="token", value=jwt_token, httponly=True)
    return resp


@app.post("/login", response_class=HTMLResponse, tags=["auth"], summary="Login with username and password")
@limiter.limit("10/minute")
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        # Render login page again with error
        return render_template(request, "login.html", {
            "username": "",
            "error_key": "login.error_invalid",
        }, status_code=401)

    token = create_access_token({"sub": user.username})
    response = RedirectResponse(url="/", status_code=302)
    response.set_cookie(key="token", value=token, httponly=True)
    return response



@app.post("/register", tags=["auth"], summary="Register a new user")
@limiter.limit("5/minute")
async def register(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    username = username.strip()
    email = email.strip()

    if not (USERNAME_MIN <= len(username) <= USERNAME_MAX):
        return render_template(request, "register.html", {
            "error_key": "register.error_username_length",
            "username": username,
            "email": email,
        })
    if len(email) > EMAIL_MAX:
        return render_template(request, "register.html", {
            "error_key": "register.error_email_length",
            "username": username,
            "email": email,
        })
    if not (PASSWORD_MIN <= len(password) <= PASSWORD_MAX):
        return render_template(request, "register.html", {
            "error_key": "register.error_password_length",
            "username": username,
            "email": email,
        })

    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        return render_template(request, "register.html", {
            "error_key": "register.error_exists",
            "username": username,
            "email": email,
        })

    hashed_password = get_password_hash(password)
    new_user = User(username=username, email=email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    return RedirectResponse(url="/login?registered=1", status_code=302)

@app.post("/upload-pdf", response_class=HTMLResponse, tags=["upload"], summary="Upload PDF and generate trivia (logged in)")
@limiter.limit("10/minute;60/hour")
async def upload_pdf(
    request: Request,
    file: UploadFile = File(...),
    num_questions: int = Form(3),
    difficulty: str = Form("medium"),
    current_user: User = Depends(get_current_user)
):
    file_bytes = await read_pdf_within_limit(request, file)
    key, _ = upload_and_get_presigned_url(file_bytes, file.filename, file.content_type)
    lang = get_lang(request)
    first_trivia, game_id, job_id, total = _run_generation(
        file_bytes, key, clamp_num_questions(num_questions), lang,
        clean_difficulty(difficulty), user_id=current_user.id, db=None,
    )
    return render_template(request, "result.html", {
        "trivia": public_trivia(first_trivia),
        "game_id": game_id,
        "job_id": job_id,
        "total": total,
        "username": current_user.username,
        "guest_mode": False
    })


@app.post("/upload-pdf-guest", response_class=HTMLResponse, tags=["guest"], summary="Upload PDF and play as guest")
@limiter.limit("10/minute;60/hour")
async def upload_pdf_guest(
    request: Request,
    file: UploadFile = File(...),
    num_questions: int = Form(3),
    difficulty: str = Form("medium"),
):
    file_bytes = await read_pdf_within_limit(request, file)
    lang = get_lang(request)
    first_trivia, game_id, job_id, total = _run_generation(
        file_bytes, None, clamp_num_questions(num_questions), lang,
        clean_difficulty(difficulty), user_id=None, db=None,
    )
    return render_template(request, "result.html", {
        "trivia": first_trivia,
        "game_id": None,
        "job_id": job_id,
        "total": total,
        "username": None,
        "guest_mode": True
    })



@app.post("/play-default-pdf", response_class=HTMLResponse, tags=["upload"], summary="Play default PDF trivia (logged in)")
@limiter.limit("10/minute;60/hour")
async def play_default_pdf(
    request: Request,
    pdf_id: str = Form("alice_in_wonderland"),
    num_questions: int = Form(3),
    difficulty: str = Form("medium"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    file_bytes, key = get_default_pdf_bytes(pdf_id)
    lang = get_lang(request)
    first_trivia, game_id, job_id, total = _run_generation(
        file_bytes, key, clamp_num_questions(num_questions), lang,
        clean_difficulty(difficulty), user_id=current_user.id, db=db,
    )
    return render_template(request, "result.html", {
        "trivia": public_trivia(first_trivia),
        "game_id": game_id,
        "job_id": job_id,
        "total": total,
        "username": current_user.username,
        "guest_mode": False
    })


@app.post("/play-default-pdf-guest", response_class=HTMLResponse, tags=["guest"], summary="Play default PDF trivia as guest")
@limiter.limit("10/minute;60/hour")
async def play_default_pdf_guest(
    request: Request,
    pdf_id: str = Form("alice_in_wonderland"),
    num_questions: int = Form(3),
    difficulty: str = Form("medium"),
):
    file_bytes, _ = get_default_pdf_bytes(pdf_id)
    lang = get_lang(request)
    first_trivia, game_id, job_id, total = _run_generation(
        file_bytes, None, clamp_num_questions(num_questions), lang,
        clean_difficulty(difficulty), user_id=None, db=None,
    )
    return render_template(request, "result.html", {
        "trivia": first_trivia,
        "game_id": None,
        "job_id": job_id,
        "total": total,
        "username": None,
        "guest_mode": True
    })


@app.post("/answer-question", tags=["scores"], summary="Submit a single answer; score is computed server-side")
@limiter.limit("120/minute")
async def answer_question(
    request: Request,
    game_id: int = Form(...),
    question_index: int = Form(...),
    choice: str = Form(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    game = db.query(ImageTrivia).filter(ImageTrivia.id == game_id).first()
    if not game or game.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Game not found")

    trivia = game.trivia or []
    if question_index < 0 or question_index >= len(trivia):
        raise HTTPException(status_code=400, detail="Invalid question index")

    progress = request.session.get("game_progress", {})
    key = str(game_id)
    state = progress.get(key, {"answered": [], "score": 0})

    correct_answer = trivia[question_index].get("answer")
    is_correct = choice == correct_answer

    if question_index not in state["answered"]:
        state["answered"].append(question_index)
        if is_correct:
            state["score"] += 1
        progress[key] = state
        request.session["game_progress"] = progress

    finished = len(state["answered"]) >= len(trivia)
    if finished:
        game.score = state["score"]
        db.commit()

    return {
        "correct": is_correct,
        "answer": correct_answer,
        "explanation": trivia[question_index].get("explanation", ""),
        "score": state["score"],
        "total": len(trivia),
        "finished": finished,
    }


@app.get("/trivia-status/{job_id}", tags=["scores"], summary="Poll for background-generated trivia questions")
async def trivia_status(job_id: str):
    with JOBS_LOCK:
        job = TRIVIA_JOBS.get(job_id)
        if not job:
            return {"questions": [], "total": 0, "done": True}
        include_answers = job["game_id"] is None
        questions = job["questions"] if include_answers else public_trivia(job["questions"])
        result = {"questions": questions, "total": job["total"], "done": job["done"]}
        if job["done"]:
            TRIVIA_JOBS.pop(job_id, None)
        return result

@app.get("/scores", response_class=HTMLResponse, tags=["scores"], summary="View score board")
def show_scores(request: Request, page: int = 1, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if page < 1:
        page = 1
    base = db.query(ImageTrivia).filter(ImageTrivia.user_id == current_user.id)
    total = base.count()
    total_pages = max(1, (total + SCORES_PAGE_SIZE - 1) // SCORES_PAGE_SIZE)
    if page > total_pages:
        page = total_pages
    scores = (
        base.options(
            load_only(
                ImageTrivia.id,
                ImageTrivia.file_key,
                ImageTrivia.score,
                ImageTrivia.uploaded_at,
            )
        )
        .order_by(ImageTrivia.uploaded_at.desc())
        .offset((page - 1) * SCORES_PAGE_SIZE)
        .limit(SCORES_PAGE_SIZE)
        .all()
    )
    for s in scores:
        s.display_name = s.file_key.split("_", 1)[-1]
    return render_template(request, "scores.html", {
        "scores": scores,
        "username": current_user.username,
        "page": page,
        "total_pages": total_pages,
        "total": total,
        "start_index": (page - 1) * SCORES_PAGE_SIZE,
    })


@app.get("/set-language/{lang_code}", tags=["pages"], summary="Switch UI language")
async def set_language(request: Request, lang_code: str):
    if lang_code in ("en", "he"):
        request.session["lang"] = lang_code
    referer = request.headers.get("referer") or "/"
    return RedirectResponse(url=referer, status_code=302)


@app.get("/logout", tags=["auth"], summary="Log out")
def logout():
    response = RedirectResponse(url="/?logout=1", status_code=302)
    response.delete_cookie("token")
    return response


@app.get("/about", response_class=HTMLResponse, tags=["pages"], summary="About page")
def about_page(request: Request, current_user=Depends(get_current_user_optional)):
    return render_template(request, "about.html", {
        "username": current_user.username if current_user else None
    })


@app.get("/", response_class=HTMLResponse, tags=["pages"], summary="Home page")
def home(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user_optional)):
    return render_template(request, "index.html", {
        "username": current_user.username if current_user else None
    })


@app.get("/register", response_class=HTMLResponse, tags=["pages"], summary="Registration page")
def register_page(request: Request, current_user=Depends(get_current_user_optional)):
    return render_template(request, "register.html", {
        "username": current_user.username if current_user else None
    })


@app.get("/login", response_class=HTMLResponse, tags=["pages"], summary="Login page")
async def login_form(request: Request, current_user=Depends(get_current_user_optional)):
    error_param = request.query_params.get("error")
    error_key = None
    if error_param == "google_not_configured":
        error_key = "error.google_not_configured"
    success_key = None
    if request.query_params.get("registered") == "1":
        success_key = "login.registered"
    return render_template(request, "login.html", {
        "username": current_user.username if current_user else None,
        "error_key": error_key,
        "success_key": success_key,
    })


@app.get("/upload", response_class=HTMLResponse, tags=["pages"], summary="Upload page or login/guest choice")
def upload_page(request: Request, current_user=Depends(get_current_user_optional)):
    if current_user:
        return render_template(request, "upload.html", {
            "username": current_user.username
        })
    return render_template(request, "upload_choose.html", {
        "username": None
    })


@app.get("/upload/guest", response_class=HTMLResponse, tags=["pages"], summary="Guest upload and default story page")
def upload_guest_page(request: Request, current_user=Depends(get_current_user_optional)):
    if current_user:
        return RedirectResponse(url="/upload", status_code=302)
    return render_template(request, "upload_guest.html", {
        "username": None
    })


@app.get("/favicon.ico", tags=["pages"], include_in_schema=False)
async def favicon():
    return FileResponse("static/favicon.ico")