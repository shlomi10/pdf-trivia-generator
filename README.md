# 🧠 AI-Powered PDF Trivia Generator

[![Build Status](https://img.shields.io/github/actions/workflow/status/shlomi10/pdf-trivia-generator/docker-hub-push.yml?branch=main&style=for-the-badge&logo=github&logoColor=white&label=BUILD)](https://github.com/shlomi10/pdf-trivia-generator/actions)
[![Docker Hub](https://img.shields.io/docker/pulls/shlomi10/pdf-trivia-app?style=for-the-badge&logo=docker&logoColor=white&label=DOCKER%20PULLS&color=2496ED)](https://hub.docker.com/repository/docker/shlomi10/pdf-trivia-app/general)
[![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-412991?style=for-the-badge&logo=openai&logoColor=white)](https://openai.com)
[![AWS S3](https://img.shields.io/badge/AWS-S3-FF9900?style=for-the-badge&logo=amazons3&logoColor=white)](https://aws.amazon.com/s3/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docs.docker.com/compose/)

Generate fun trivia quizzes from any uploaded PDF using AI!  
This project uses FastAPI, OpenAI, JWT authentication, AWS S3 storage, and a clean UI.  
Built with ❤️ by [Shlomi Gross](https://github.com/shlomi10).

---

## 🚀 Features

- 📄 Upload PDFs and generate AI-based trivia
- ☁️ **AWS S3 integration** for secure PDF storage
- ✅ JWT Authentication (Register, Login)
- 🎯 Multiple-choice questions with answers
- 🧑‍💻 User-based score saving and history
- 📊 Scoreboard per user
- 🎛️ Select number of questions to generate
- 💻 Modern frontend with HTML & CSS
- 🐳 Docker & Docker Compose support
- 🚀 GitHub Actions CI/CD pipeline
- 📦 Automated Docker Hub deployment

---

## 🗂️ Project Structure

```
├── main.py                     # FastAPI app entry point
├── db/                         # Database
│   ├── db.py                   # Database session and setup
│   └── models.py               # SQLAlchemy ORM models
├── games/                      # Games logic
│   └── games.py                # Game-related CRUD logic
├── services/                   # Services
│   ├── aws_file_utilities.py   # S3 upload/download logic
│   └── trivia_generator.py     # Extract PDF content & send to GPT
├── auth/                       # Authentication
│   └── auth.py                 # Auth routes & JWT handling
├── templates/                  # HTML templates (Jinja2)
│   ├── index.html              # Main page
│   ├── login.html              # User login
│   ├── register.html           # User registration
│   ├── scores.html             # Score history
│   ├── upload.html             # PDF upload interface
│   └── result.html             # Quiz results
├── static/                     # Static assets
│   ├── bg.jpg                  # Background wallpaper
│   ├── favicon.ico             # Site favicon
│   └── style.css               # Main stylesheet
├── .env                        # Environment variables (secrets)
├── Dockerfile                  # Docker container configuration
├── docker-compose.yml          # Docker Compose setup
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
└── .github/                    # GitHub Actions
    └── workflows/
        └── docker-hub-push.yml # CI/CD pipeline for Docker Hub
```

---

## ⚙️ Tech Stack

- 🐍 **Backend:** Python 3.13 + FastAPI + Jinja2
- 🤖 **AI:** OpenAI GPT-4o for trivia generation
- 🛢️ **Database:** SQLAlchemy + SQLite (PostgreSQL ready)
- ☁️ **Storage:** AWS S3 for PDF file storage
- 🔐 **Auth:** Python-Jose + Passlib (JWT Authentication)
- 📄 **PDF Processing:** PyMuPDF (PDF → text extraction)
- 🐳 **DevOps:** Docker + Docker Compose + GitHub Actions
- 📦 **Deployment:** Automated Docker Hub publishing

---

## ✅ Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/shlomi10/pdf-trivia-generator.git
cd pdf-trivia-generator
```

### 2. Create virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create `.env` file in the project root:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# AWS S3 Configuration
AWS_ACCESS_KEY_ID=your_aws_access_key_id
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
AWS_REGION=us-east-1
S3_BUCKET_NAME=your-pdf-storage-bucket

# JWT Configuration (optional - will use defaults)
SECRET_KEY=your_jwt_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database (optional - defaults to SQLite)
DATABASE_URL=sqlite:///./trivia_game.db
```

### 5. Run the application

```bash
uvicorn main:app --reload
```

Visit: [http://localhost:8000](http://localhost:8000)

---

## 🐳 Docker Usage

### Option 1: Docker Compose (Recommended)

```bash
# Start the application
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the application
docker-compose down
```

### Option 2: Docker Build & Run

```bash
# Build the image
docker build -t shlomi10/pdf-trivia-generator .

# Run with environment file
docker run --env-file .env -p 8000:8000 shlomi10/pdf-trivia-generator

# Or run with environment variables
docker run -e OPENAI_API_KEY=your_key \
           -e AWS_ACCESS_KEY_ID=your_key \
           -e AWS_SECRET_ACCESS_KEY=your_secret \
           -p 8000:8000 shlomi10/pdf-trivia-generator
```

### Option 3: Pull from Docker Hub

```bash
# Pull the latest image
docker pull shlomi10/pdf-trivia-generator:latest

# Run the container
docker run --env-file .env -p 8000:8000 shlomi10/pdf-trivia-generator:latest
```

---

## 🔐 Authentication Flow

| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| `/register` | POST | Create new user account | ❌ |
| `/login` | POST | Login and receive JWT token | ❌ |
| `/upload-pdf/` | POST | Upload PDF and generate trivia | ✅ |
| `/scores/` | GET | View user score history | ✅ |

**Authentication Header:**
```http
Authorization: Bearer <your_jwt_token>
```

---

## ☁️ AWS S3 Integration

The application now supports secure PDF storage on AWS S3:

- **Automatic Upload:** PDFs are automatically uploaded to your S3 bucket
- **Secure Access:** Uses IAM credentials for secure file operations
- **File Management:** Automatic cleanup and organization
- **Scalable Storage:** No local storage limitations

### S3 Bucket Setup

1. Create an S3 bucket in your AWS account
2. Configure IAM user with S3 permissions:
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Action": [
           "s3:GetObject",
           "s3:PutObject",
           "s3:DeleteObject"
         ],
         "Resource": "arn:aws:s3:::your-bucket-name/*"
       }
     ]
   }
   ```
3. Add credentials to your `.env` file

---

## 🚀 CI/CD Pipeline

This project includes automated GitHub Actions workflow:

- **Automatic Building:** Docker images built on every push
- **Docker Hub Publishing:** Images pushed to Docker Hub registry
- **Multi-platform Support:** Builds for AMD64 and ARM64
- **Tag Management:** Automatic versioning with Git tags

### Workflow Triggers
- Push to `main` branch
- Pull requests to `main`
- Git tag creation (for releases)

---

## 📦 Dependencies

```txt
fastapi>=0.104.1
uvicorn[standard]>=0.24.0
python-multipart>=0.0.6
python-dotenv>=1.0.0
openai>=1.3.0
pillow>=10.1.0
jinja2>=3.1.2
aiofiles>=23.2.1
pymupdf>=1.23.0
sqlalchemy>=2.0.23
passlib[bcrypt]>=1.7.4
python-jose>=3.3.0
boto3>=1.34.0
botocore>=1.34.0
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 API Documentation

Once running, visit:
- **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🐛 Troubleshooting

### Common Issues

**PDF Upload Fails:**
- Check AWS credentials in `.env`
- Verify S3 bucket permissions
- Ensure bucket exists and is accessible

**OpenAI API Errors:**
- Verify API key is correct
- Check OpenAI account has sufficient credits
- Ensure API key has proper permissions

**Docker Issues:**
- Ensure Docker is running
- Check port 8000 is not in use
- Verify environment variables are set

---

## 📝 License

MIT License © 2025 [Shlomi Gross](https://github.com/shlomi10)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

⭐ **If you found this project helpful, please give it a star!** ⭐