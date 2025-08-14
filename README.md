# 🎯 PDF Trivia Generator

[![GitHub CI](https://img.shields.io/github/actions/workflow/status/shlomi10/pdf-trivia-generator/dockerhub-push.yml?label=Build&style=for-the-badge&logo=github-actions&logoColor=white)](https://github.com/shlomi10/pdf-trivia-generator/actions)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Docker Pulls](https://img.shields.io/docker/pulls/shlomi10/pdf-trivia-app?style=for-the-badge&logo=docker&logoColor=white&color=orange)](https://hub.docker.com/r/shlomi10/pdf-trivia-app)
[![Docker Image Size](https://img.shields.io/docker/image-size/shlomi10/pdf-trivia-app?style=for-the-badge&logo=docker&logoColor=white)](https://hub.docker.com/r/shlomi10/pdf-trivia-app)
[![Python](https://img.shields.io/badge/Python-3.13+-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-06b6d4?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-6f42c1?style=for-the-badge&logo=openai&logoColor=white)](https://openai.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![AWS S3](https://img.shields.io/badge/AWS%20S3-FF9900?style=for-the-badge&logo=amazon-s3&logoColor=white)](https://aws.amazon.com/s3/)

> 🚀 **Transform any PDF into an interactive trivia game powered by GPT-5!**

A modern web application that extracts content from PDF documents and automatically generates engaging trivia questions using OpenAI's GPT-5. Perfect for educators, students, and anyone looking to gamify their learning experience.

[![Live App](https://img.shields.io/badge/🟢%20Live%20App-strivia.onrender.com-brightgreen?style=for-the-badge&logo=fastapi)](https://strivia.onrender.com/)

## ✨ Features

### 🎮 **Interactive Gaming Experience**
- **Smart Question Generation**: AI-powered trivia creation from any PDF content
- **Multiple Difficulty Levels**: Choose between 3, 5, or 10 questions per game
- **Real-time Scoring**: Live score tracking with instant feedback
- **Cross-Platform Access**: Seamlessly works on desktop and tablet devices

### 🔐 **User Management**
- **Secure Authentication**: JWT-based login system with bcrypt password hashing
- **Personal Dashboard**: Track your trivia history and scores
- **Session Management**: Persistent login with secure cookie handling

### ☁️ **Cloud-Native Architecture**
- **AWS S3 Integration**: Secure file storage with pre-signed URLs
- **PostgreSQL Database**: Robust data persistence for users and games
- **Docker Containerization**: Easy deployment and scaling
- **GitHub Actions CI/CD**: Automated builds and deployments

## 🏗️ Tech Stack

### **Backend**
- **[FastAPI](https://fastapi.tiangolo.com/)** - Modern, fast web framework for building APIs
- **[Python 3.13+](https://www.python.org/)** - Latest Python features and performance
- **[SQLAlchemy](https://www.sqlalchemy.org/)** - Powerful SQL toolkit and ORM
- **[PostgreSQL](https://www.postgresql.org/)** - Advanced open source database

### **AI & Document Processing**
- **[OpenAI GPT-4](https://openai.com/)** - State-of-the-art language model for question generation
- **[PyMuPDF](https://pymupdf.readthedocs.io/)** - High-performance PDF text extraction

### **Cloud Services**
- **[AWS S3](https://aws.amazon.com/s3/)** - Scalable object storage for uploaded files
- **[Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)** - AWS SDK for Python

### **Security & Authentication**
- **[Passlib](https://passlib.readthedocs.io/)** - Password hashing with bcrypt
- **[Python-JOSE](https://python-jose.readthedocs.io/)** - JWT token handling
- **[FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)** - OAuth2 with JWT tokens

### **Frontend**
- **HTML5 & CSS3** - Modern web standards with responsive design
- **JavaScript ES6+** - Interactive UI components
- **CSS Grid & Flexbox** - Responsive layouts
- **Jinja2 Templates** - Server-side rendering

### **DevOps & Deployment**
- **[Docker](https://www.docker.com/)** - Containerization for consistent deployments
- **[Docker Compose](https://docs.docker.com/compose/)** - Multi-container orchestration
- **[GitHub Actions](https://github.com/features/actions)** - CI/CD pipeline automation

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- OpenAI API key
- AWS credentials for S3
- PostgreSQL database

### 1. Clone the Repository
```bash
git clone https://github.com/shlomi10/pdf-trivia-generator.git
cd pdf-trivia-generator
```

### 2. Environment Setup
Create a `.env` file with your credentials:
```env
OPENAI_API_KEY=your_openai_api_key_here
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
```

### 3. Docker Deployment (Recommended)
```bash
# Pull the latest image from Docker Hub
docker pull shlomi10/pdf-trivia-app:latest

# Run with Docker Compose
docker-compose up -d
```

### 4. Manual Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Initialize database
python db/db.py

# Run the application
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 5. Access the Application
- **Desktop**: Open your browser and navigate to `http://localhost:8000`
- **Public Access**: Deploy to a cloud service and access from any device

## 🎯 Usage Guide

### 📝 **Getting Started**
1. **Register/Login** - Create your account or sign in
2. **Upload PDF** - Choose any PDF document from your device
3. **Generate Trivia** - AI automatically creates questions from your content
4. **Play & Learn** - Answer questions with intuitive interface
5. **Review Scores** - Check your trivia history and performance

## 🏛️ Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Client    │    │   FastAPI       │    │   PostgreSQL    │
│   (Browser)     │◄──►│   Backend       │◄──►│   Database      │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
        │                       │                         │
        │                       ▼                         ▼
        │              ┌─────────────────┐    ┌─────────────────┐
        │              │   OpenAI API    │    │   AWS S3        │
        │              │   (GPT-5)       │    │   Storage       │
        │              └─────────────────┘    └─────────────────┘
```

### **Data Flow**
1. **Access**: User opens web app in browser
2. **Upload**: PDF files uploaded via web interface
3. **Processing**: Server-side text extraction and AI processing
4. **Gaming**: Interactive trivia interface
5. **Storage**: Progress and scores saved to database

## 🐳 Docker Hub

The application is available as a Docker image on Docker Hub:

**Pull the image:**
```bash
docker pull shlomi10/pdf-trivia-app:latest
```

**Available tags:**
- `latest` - Latest stable release
- Build numbers for CI/CD tracking

## 🔄 CI/CD Pipeline

Automated deployment pipeline using GitHub Actions:

- ✅ **Continuous Integration**: Automated testing on every commit
- 🏗️ **Docker Build**: Multi-stage builds for optimized images
- 📦 **Registry Push**: Automatic pushes to Docker Hub
- 🚀 **Deployment**: Ready for production deployment

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Setup
```bash
# Clone your fork
git clone https://github.com/your-username/pdf-trivia-generator.git

# Install development dependencies
pip install -r requirements.txt

# Run tests
pytest

# Start development server
uvicorn main:app --reload
```

## 📋 API Documentation

Once running, visit `/docs` for interactive API documentation powered by FastAPI's automatic OpenAPI generation.

### Key Endpoints:
- `POST /upload-pdf` - Upload PDF and generate trivia
- `POST /save-score` - Save game results
- `GET /scores` - Retrieve user's trivia history
- `POST /login` - User authentication
- `POST /register` - User registration

## 🧪 Testing

Run the test suite to ensure everything works correctly:

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run with coverage
pytest --cov=. tests/
```

## 🔧 Configuration

### Environment Variables:
```env
# Required
OPENAI_API_KEY=your_openai_api_key
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key

# Optional
SECRET_KEY=your_jwt_secret_key
ACCESS_TOKEN_EXPIRE_MINUTES=60
S3_BUCKET=your_s3_bucket_name
AWS_REGION=us-east-1
```

## 🔒 Security Features

- **JWT Authentication** with secure token management
- **Password Hashing** using bcrypt with salt
- **SQL Injection Protection** via SQLAlchemy ORM
- **File Upload Validation** with content type checking
- **Secure Cookie Handling** with HttpOnly flags
- **HTTPS Enforcement** for secure connections

## 📊 Performance

- **Fast Response Times** with FastAPI's async capabilities
- **Efficient PDF Processing** using PyMuPDF
- **Scalable Architecture** with Docker containerization
- **Optimized Database** queries with SQLAlchemy

## 🛠️ Troubleshooting

### Common Issues:

**OpenAI API Errors:**
```bash
# Check your API key
echo $OPENAI_API_KEY
```

**Database Connection:**
```bash
# Verify PostgreSQL is running
docker-compose logs db
```

**AWS S3 Upload:**
```bash
# Check AWS credentials and CORS settings
aws s3api get-bucket-cors --bucket your-bucket-name
```

## 📈 Roadmap

- [ ] **Multi-language Support** - Support for non-English PDFs
- [ ] **Team Competitions** - Multiplayer trivia battles
- [ ] **Question Categories** - Filter by topic or difficulty
- [ ] **Export Features** - Download trivia as Kahoot/Quizlet format
- [ ] **Analytics Dashboard** - Detailed performance insights

## 📄 License

This project is licensed under the MIT License.

```
MIT License

Copyright (c) 2024 Shlomi

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
```

## 🙏 Acknowledgments

- **OpenAI** for providing the GPT-5 API
- **FastAPI** team for the excellent web framework
- **AWS** for reliable cloud infrastructure
- **Docker** for containerization technology

## 📞 Contact

**Shlomi** - [@shlomi10](https://github.com/shlomi10)

**Project Link**: [https://github.com/shlomi10/pdf-trivia-generator](https://github.com/shlomi10/pdf-trivia-generator)

**Docker Hub**: [https://hub.docker.com/r/shlomi10/pdf-trivia-app](https://hub.docker.com/r/shlomi10/pdf-trivia-app)

---

⭐ **Star this repository if you found it helpful!**

![Footer](https://img.shields.io/badge/Made%20with-❤️-red?style=for-the-badge)
