from fastapi import UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi import Request
from fastapi.responses import HTMLResponse
from auth.auth import get_current_user
from db.models import User, ImageTrivia
from services.aws_file_utils import upload_and_get_presigned_url
from services.trivia_generator import generate_trivia_from_pdf
from games.games import create_game, get_db
from fastapi import FastAPI, Form, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from auth.auth import get_password_hash, verify_password, create_access_token
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
from auth.auth import get_current_user_optional

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.post("/login", response_class=HTMLResponse)
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        # Render login page again with error
        return templates.TemplateResponse("login.html", {
            "request": request,
            "username": "",
            "error": "❌ Invalid username or password. Please try again."
        }, status_code=401)

    token = create_access_token({"sub": user.username})
    response = RedirectResponse(url="/", status_code=302)
    response.set_cookie(key="token", value=token, httponly=True)
    return response



@app.post("/register")
async def register(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        return templates.TemplateResponse("register.html", {
            "request": request,
            "error": "Username already exists.<br>Please choose another."
        })

    hashed_password = get_password_hash(password)
    new_user = User(username=username, email=email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    return RedirectResponse(url="/login", status_code=302)

@app.post("/upload-pdf", response_class=HTMLResponse)
async def upload_pdf(request: Request, file: UploadFile = File(...), current_user: User = Depends(get_current_user)):
    file_bytes = await file.read()
    key, _ = upload_and_get_presigned_url(file_bytes, file.filename, file.content_type)
    trivia = generate_trivia_from_pdf(file_bytes)
    game = create_game(user_id=current_user.id, file_key=key, trivia=trivia)
    return templates.TemplateResponse("result.html", {
        "request": request,
        "trivia": trivia,
        "game_id": game.id,
        "username": current_user.username
    })


@app.post("/save-score")
async def save_score(game_id: int = Form(...), score: int = Form(...), db: Session = Depends(get_db)):
    game = db.query(ImageTrivia).filter(ImageTrivia.id == game_id).first()
    if game:
        game.score = score
        db.commit()
        return {"message": "Score saved!"}
    raise HTTPException(status_code=404, detail="Game not found")

@app.get("/scores", response_class=HTMLResponse)
def show_scores(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    scores = db.query(ImageTrivia).filter(ImageTrivia.user_id == current_user.id).order_by(ImageTrivia.uploaded_at.desc()).all()
    return templates.TemplateResponse("scores.html", {
        "request": request,
        "scores": scores,
        "username": current_user.username
    })


@app.get("/logout")
def logout():
    response = RedirectResponse(url="/?logout=1", status_code=302)
    response.delete_cookie("token")
    return response


@app.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user_optional)):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "username": current_user.username if current_user else None
    })


@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request, current_user=Depends(get_current_user_optional)):
    return templates.TemplateResponse("register.html", {
        "request": request,
        "username": current_user.username if current_user else None
    })


@app.get("/login", response_class=HTMLResponse)
async def login_form(request: Request, current_user=Depends(get_current_user_optional)):
    return templates.TemplateResponse("login.html", {
        "request": request,
        "username": current_user.username if current_user else None
    })


@app.get("/upload", response_class=HTMLResponse)
def upload_page(request: Request, current_user=Depends(get_current_user_optional)):
    return templates.TemplateResponse("upload.html", {
        "request": request,
        "username": current_user.username if current_user else None
    })


@app.get("/favicon.ico")
async def favicon():
    return FileResponse("static/favicon.ico")
