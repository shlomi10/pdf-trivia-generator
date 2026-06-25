# 🎯 PDF Trivia Generator

<p align="center">

[![GitHub CI](https://img.shields.io/github/actions/workflow/status/shlomi10/pdf-trivia-generator/dockerhub-push.yml?label=Build&style=for-the-badge&logo=github-actions&logoColor=white)](https://github.com/shlomi10/pdf-trivia-generator/actions)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Docker Pulls](https://img.shields.io/docker/pulls/shlomi10/pdf-trivia-app?style=for-the-badge&logo=docker&logoColor=white&color=orange)](https://hub.docker.com/r/shlomi10/pdf-trivia-app)
[![Docker Image Size](https://img.shields.io/docker/image-size/shlomi10/pdf-trivia-app/latest?style=for-the-badge&logo=docker&logoColor=white)](https://hub.docker.com/r/shlomi10/pdf-trivia-app)

</p>

<p align="center">

[![Python](https://img.shields.io/badge/Python-3.14+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![OpenAI](https://img.shields.io/badge/GPT--5-412991?style=for-the-badge&logo=openai&logoColor=white)](https://openai.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![AWS S3](https://img.shields.io/badge/AWS%20S3-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white)](https://aws.amazon.com/s3/)
[![Google OAuth](https://img.shields.io/badge/Google%20OAuth-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://developers.google.com/identity)

</p>

<p align="center">

[![Live App](https://img.shields.io/badge/🟢%20Live%20App-strivia.onrender.com-22c55e?style=for-the-badge&logo=render&logoColor=white)](https://strivia.onrender.com/)
[![Swagger](https://img.shields.io/badge/📘%20Swagger%20UI-/docs-85EA2D?style=for-the-badge&logo=swagger&logoColor=black)](https://strivia.onrender.com/docs)
[![Guest Play](https://img.shields.io/badge/🎮%20Guest%20Play-enabled-blueviolet?style=for-the-badge)](https://strivia.onrender.com/upload/guest)
[![Alice Story](https://img.shields.io/badge/📖%20Alice%20in%20Wonderland-default%20PDF-ff69b4?style=for-the-badge)](https://strivia.onrender.com/upload/guest)

</p>

<p align="center">
  <strong>🚀 Transform any PDF into an interactive trivia game powered by GPT-5!</strong><br/>
  Upload your own document, play as a guest, or try the built-in <em>Alice in Wonderland</em> story.
</p>

## ✨ Features

### Play modes

| Mode | Login required | Score saved | Upload own PDF | Default story |
|------|----------------|-------------|----------------|---------------|
| **Registered user** | Yes | Yes | Yes | Yes |
| **Guest** | No | No | Yes | Yes |

### Core capabilities

- **PDF upload** — Upload any PDF and generate 3, 5, or 10 trivia questions with GPT-5
- **Guest play** — Play without registering; scores are not saved to the score board
- **Default story** — Built-in *Alice in Wonderland* / *עליסה בארץ הפלאות* (no upload needed)
- **Live scoring** — Real-time feedback and score tracking during the game
- **Score history** — Logged-in users can view past games at `/scores`

### Authentication

- Username / password registration and login
- Google OAuth sign-in
- JWT session cookies for authenticated users

### Infrastructure

- AWS S3 for user-uploaded PDFs
- PostgreSQL for users, games, and scores
- Docker image published to Docker Hub
- GitHub Actions CI/CD pipeline

## 👤 User flows

### Guest

1. Open `/` and click **Start Now**
2. At `/upload` choose **Continue as Guest**
3. At `/upload/guest` either:
   - Upload your own PDF, or
   - Play **Alice in Wonderland**
4. Play trivia — score is **not** saved

### Registered user

1. Register or log in (or use Google OAuth)
2. Go to `/upload`
3. Upload a PDF **or** play the default Alice story
4. Play trivia — score is saved to `/scores`

## 📖 Default PDF (Alice in Wonderland)

The default story is configured in `services/default_pdfs.py` and stored in S3 only.

**On each play:**
1. Generate a presigned S3 URL (`eu-central-1`)
2. Download the PDF from that URL
3. Generate trivia from the file bytes

There is **no local copy** in the project — S3 must be available.

S3 key:
```
pdf/2a08f2f4-0967-45fc-b48d-d6cefd9b9a97_alice_in_wonderland.pdf
```

Bucket: `files.handson.academy` · Region: `eu-central-1`

The IAM user needs `s3:GetObject` and `s3:PutObject` on `arn:aws:s3:::files.handson.academy/pdf/*`.

## 🏗️ Tech stack

| Layer | Technology |
|-------|------------|
| Backend | FastAPI, Python 3.14+, SQLAlchemy |
| AI | OpenAI GPT-5 |
| PDF | PyMuPDF |
| Storage | AWS S3 (Boto3) |
| Database | PostgreSQL |
| Auth | Passlib, python-jose, Authlib (Google OAuth) |
| Frontend | Jinja2, HTML/CSS/JS |
| Deploy | Docker, Docker Compose, GitHub Actions |

## 🚀 Quick start

### Prerequisites

- Docker and Docker Compose
- OpenAI API key
- PostgreSQL database (`DATABASE_URL`)
- AWS credentials with S3 access (required for user uploads **and** default Alice PDF)
- Google OAuth credentials (optional, for Google login)
- `SESSION_SECRET` (required for OAuth sessions)

### 1. Clone

```bash
git clone https://github.com/shlomi10/pdf-trivia-generator.git
cd pdf-trivia-generator
```

### 2. Environment

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key

AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=eu-central-1

GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret

SECRET_KEY=your_jwt_secret
SESSION_SECRET=your_session_secret

DATABASE_URL=postgresql://user:password@host:5432/dbname
```

### 3. Run with Docker (recommended)

```bash
docker compose up --build -d
```

Open **http://localhost:8000**

```bash
docker compose logs -f web    # view logs
docker compose restart web    # restart after .env changes
docker compose down           # stop
```

### 4. Run locally (without Docker)

```bash
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## 🔐 Google OAuth setup

1. [Google Cloud Console](https://console.cloud.google.com/) → create or select a project
2. Create OAuth 2.0 credentials (Web application)
3. **Authorized redirect URI:** `http://localhost:8000/auth/google/callback` (and your production URL)
4. Set `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, and `SESSION_SECRET` in `.env`

## 🛠️ Architecture

```mermaid
flowchart TB
    User([Browser])
    API[FastAPI]
    PG[(PostgreSQL)]
    S3[AWS S3]
    GPT[OpenAI GPT-5]

    User -->|Guest or login| API
    User -->|Google OAuth| API
    API --> PG

    User -->|Upload PDF| API
    API -->|Store file| S3
    API -->|Presigned URL + download| S3
    API -->|Generate questions| GPT
    API -->|Save game and score| PG
    API -->|Trivia game| User
```

## 📘 Swagger / OpenAPI

FastAPI generates interactive API documentation automatically.

| Environment | Swagger UI | ReDoc | OpenAPI JSON |
|-------------|------------|-------|--------------|
| Local | [localhost:8000/docs](http://localhost:8000/docs) | [localhost:8000/redoc](http://localhost:8000/redoc) | [localhost:8000/openapi.json](http://localhost:8000/openapi.json) |
| Production | [strivia.onrender.com/docs](https://strivia.onrender.com/docs) | [strivia.onrender.com/redoc](https://strivia.onrender.com/redoc) | [strivia.onrender.com/openapi.json](https://strivia.onrender.com/openapi.json) |

**API title:** PDF Trivia Generator · **version:** 1.1.0

Endpoints are grouped by tags in Swagger:

| Tag | Description |
|-----|-------------|
| `pages` | HTML pages (home, login, upload, guest) |
| `auth` | Login, registration, Google OAuth, logout |
| `upload` | PDF upload and default story (logged in) |
| `guest` | Guest play without login or score saving |
| `scores` | Save and view game scores |

> Most `POST` endpoints return HTML (trivia game page), not JSON. Use **Try it out** in Swagger to test form uploads and see the response.

## 📋 API endpoints

### Pages

| Method | Path | Tag | Description |
|--------|------|-----|-------------|
| GET | `/` | pages | Home |
| GET | `/login` | pages | Login form |
| GET | `/register` | pages | Registration form |
| GET | `/upload` | pages | Upload page (logged in) or choose login/guest |
| GET | `/upload/guest` | pages | Guest upload + default story |
| GET | `/scores` | scores | Score board (logged in only) |

### Actions

| Method | Path | Tag | Auth | Description |
|--------|------|-----|------|-------------|
| POST | `/login` | auth | — | Username/password login |
| POST | `/register` | auth | — | Create account |
| GET | `/login/google` | auth | — | Start Google OAuth |
| GET | `/auth/google/callback` | auth | — | Google OAuth callback |
| GET | `/logout` | auth | — | Log out |
| POST | `/upload-pdf` | upload | Required | Upload PDF, save to S3 + DB |
| POST | `/upload-pdf-guest` | guest | — | Upload PDF, guest play |
| POST | `/play-default-pdf` | upload | Required | Play Alice, save to DB |
| POST | `/play-default-pdf-guest` | guest | — | Play Alice as guest |
| POST | `/save-score` | scores | Required | Save game score |

## 📁 Project structure

```
TriviaGame/
├── main.py                      # FastAPI routes
├── services/
│   ├── trivia_generator.py      # PDF text extraction + GPT questions
│   ├── aws_file_utils.py        # S3 upload/download
│   └── default_pdfs.py          # Default PDF S3 config + presigned URL fetch
├── templates/
│   ├── upload.html              # Logged-in upload page
│   ├── upload_choose.html       # Login vs guest choice
│   ├── upload_guest.html        # Guest upload page
│   └── result.html              # Trivia game UI
├── static/
│   ├── style.css                # Global styles
│   ├── bg.jpg
│   └── favicon.ico
├── docker-compose.yml
└── Dockerfile
```

## 🐳 Docker Hub

```bash
docker pull shlomi10/pdf-trivia-app:latest
```

Tags: `latest` and build numbers from CI.

## 🔧 Troubleshooting

**OpenAI errors**
- Check `OPENAI_API_KEY` in `.env`
- Question generation can take several seconds (GPT API call)

**Database errors**
- Verify `DATABASE_URL` is reachable from the container

**S3 upload or default PDF fails**
- Set `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, and `AWS_REGION=eu-central-1` in `.env` (and on Render)
- Ensure IAM policy includes `s3:GetObject` and `s3:PutObject` on `files.handson.academy/pdf/*`
- Default Alice has **no local fallback** — S3 must work
- Test: `venv\Scripts\python.exe -c "from services.default_pdfs import get_default_pdf_bytes; print(len(get_default_pdf_bytes('alice_in_wonderland')[0]))"`

**Google OAuth fails**
- Set `SESSION_SECRET` in `.env` (and on Render)
- Redirect URI must match exactly: `/auth/google/callback`
- Use a valid OAuth client (not deleted) in Google Console

**Static files / 500 on startup**
- Ensure `static/` exists (includes `style.css`, `bg.jpg`, `favicon.ico`)

## 📄 License

MIT License — see repository for full text.

## 📞 Contact

- **GitHub:** [@shlomi10](https://github.com/shlomi10)
- **Repo:** [pdf-trivia-generator](https://github.com/shlomi10/pdf-trivia-generator)
- **Docker Hub:** [shlomi10/pdf-trivia-app](https://hub.docker.com/r/shlomi10/pdf-trivia-app)
- **Live:** [strivia.onrender.com](https://strivia.onrender.com/)

---

<p align="center">
  <a href="https://github.com/shlomi10/pdf-trivia-generator">
    <img src="https://img.shields.io/badge/⭐%20Star%20this%20repo-if%20you%20like%20it-yellow?style=for-the-badge" alt="Star this repo"/>
  </a>
  <br/><br/>
  <img src="https://img.shields.io/badge/Made%20with-❤️%20by%20Shlomi-red?style=for-the-badge" alt="Made with love"/>
</p>
