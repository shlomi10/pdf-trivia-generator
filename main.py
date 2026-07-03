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
from sqlalchemy.orm import Session
from auth.auth import get_password_hash, verify_password, create_access_token
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
from auth.auth import get_current_user_optional

import os
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth
from dotenv import load_dotenv
# Removed jinja2 Environment imports and custom class

load_dotenv() # Load environment variables from .env file

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
async def register(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        return render_template(request, "register.html", {
            "error_key": "register.error_exists",
        })

    hashed_password = get_password_hash(password)
    new_user = User(username=username, email=email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    return RedirectResponse(url="/login", status_code=302)

@app.post("/upload-pdf", response_class=HTMLResponse, tags=["upload"], summary="Upload PDF and generate trivia (logged in)")
async def upload_pdf(
    request: Request,
    file: UploadFile = File(...),
    num_questions: int = Form(3),
    current_user: User = Depends(get_current_user)
):
    file_bytes = await file.read()
    key, _ = upload_and_get_presigned_url(file_bytes, file.filename, file.content_type)
    lang = get_lang(request)
    trivia = generate_trivia_from_pdf(file_bytes, num_questions=num_questions, lang=lang)
    game = create_game(user_id=current_user.id, file_key=key, trivia=trivia)
    return render_template(request, "result.html", {
        "trivia": trivia,
        "game_id": game.id,
        "username": current_user.username,
        "guest_mode": False
    })


@app.post("/upload-pdf-guest", response_class=HTMLResponse, tags=["guest"], summary="Upload PDF and play as guest")
async def upload_pdf_guest(
    request: Request,
    file: UploadFile = File(...),
    num_questions: int = Form(3),
):
    file_bytes = await file.read()
    lang = get_lang(request)
    trivia = generate_trivia_from_pdf(file_bytes, num_questions=num_questions, lang=lang)
    return render_template(request, "result.html", {
        "trivia": trivia,
        "game_id": None,
        "username": None,
        "guest_mode": True
    })



@app.post("/play-default-pdf", response_class=HTMLResponse, tags=["upload"], summary="Play default PDF trivia (logged in)")
async def play_default_pdf(
    request: Request,
    pdf_id: str = Form("alice_in_wonderland"),
    num_questions: int = Form(3),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    file_bytes, key = get_default_pdf_bytes(pdf_id)
    lang = get_lang(request)
    trivia = generate_trivia_from_pdf(file_bytes, num_questions=num_questions, lang=lang)
    game = create_game(user_id=current_user.id, file_key=key, trivia=trivia, db=db)
    return render_template(request, "result.html", {
        "trivia": trivia,
        "game_id": game.id,
        "username": current_user.username,
        "guest_mode": False
    })


@app.post("/play-default-pdf-guest", response_class=HTMLResponse, tags=["guest"], summary="Play default PDF trivia as guest")
async def play_default_pdf_guest(
    request: Request,
    pdf_id: str = Form("alice_in_wonderland"),
    num_questions: int = Form(3),
):
    file_bytes, _ = get_default_pdf_bytes(pdf_id)
    lang = get_lang(request)
    trivia = generate_trivia_from_pdf(file_bytes, num_questions=num_questions, lang=lang)
    return render_template(request, "result.html", {
        "trivia": trivia,
        "game_id": None,
        "username": None,
        "guest_mode": True
    })


@app.post("/save-score", tags=["scores"], summary="Save game score")
async def save_score(game_id: int = Form(...), score: int = Form(...), db: Session = Depends(get_db)):
    game = db.query(ImageTrivia).filter(ImageTrivia.id == game_id).first()
    if game:
        game.score = score
        db.commit()
        return {"message": "Score saved!"}
    raise HTTPException(status_code=404, detail="Game not found")

@app.get("/scores", response_class=HTMLResponse, tags=["scores"], summary="View score board")
def show_scores(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    scores = db.query(ImageTrivia).filter(ImageTrivia.user_id == current_user.id).order_by(ImageTrivia.uploaded_at.desc()).all()
    for s in scores:
        s.display_name = s.file_key.split("_", 1)[-1]
    return render_template(request, "scores.html", {
        "scores": scores,
        "username": current_user.username
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
    return render_template(request, "login.html", {
        "username": current_user.username if current_user else None,
        "error_key": error_key,
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