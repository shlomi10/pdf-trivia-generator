# 🎯 PDF Trivia Generator

[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/shlomi10/pdf-trivia-generator/dockerhub-push.yml?style=for-the-badge&logo=github-actions&logoColor=white)](https://github.com/shlomi10/pdf-trivia-generator/actions)
[![Docker Pulls](https://img.shields.io/docker/pulls/shlomi10/pdf-trivia-app?style=for-the-badge&logo=docker&logoColor=white)](https://hub.docker.com/r/shlomi10/pdf-trivia-app)
[![Docker Image Size](https://img.shields.io/docker/image-size/shlomi10/pdf-trivia-app/latest?style=for-the-badge&logo=docker&logoColor=white)](https://hub.docker.com/r/shlomi10/pdf-trivia-app)
[![Python](https://img.shields.io/badge/python-3.13+-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)](https://openai.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![AWS S3](https://img.shields.io/badge/AWS%20S3-FF9900?style=for-the-badge&logo=amazon-s3&logoColor=white)](https://aws.amazon.com/s3/)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)

> 🚀 **Transform any PDF into an interactive trivia game powered by GPT-4!**

A modern web application that extracts content from PDF documents and automatically generates engaging trivia questions using OpenAI's GPT-4. Perfect for educators, students, and anyone looking to gamify their learning experience.

![PDF Trivia Demo](https://img.shields.io/badge/Live%20Demo-Coming%20Soon-green?style=for-the-badge)

## ✨ Features

### 🎮 **Interactive Gaming Experience**
- **Smart Question Generation**: AI-powered trivia creation from any PDF content
- **Multiple Difficulty Levels**: Choose between 3, 5, or 10 questions per game
- **Real-time Scoring**: Live score tracking with instant feedback
- **Cross-Platform Access**: Seamlessly works on desktop, tablet, and mobile devices

### 📱 **Mobile-Optimized Experience**
- **Responsive Web Design**: Adaptive layout that works perfectly on any screen size
- **Touch-Friendly Interface**: Optimized buttons and interactions for mobile devices
- **Progressive Web App (PWA) Ready**: Add to home screen for app-like experience
- **Offline Capability**: Play generated trivia even when internet connection is limited
- **Mobile-First Approach**: Designed primarily for mobile users, enhanced for desktop

### 🔐 **User Management**
- **Secure Authentication**: JWT-based login system with bcrypt password hashing
- **Personal Dashboard**: Track your trivia history and scores across all devices
- **Session Management**: Persistent login with secure cookie handling
- **Sync Across Devices**: Access your progress from any device

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

### **Frontend & Mobile Support**
- **HTML5 & CSS3** - Modern web standards with mobile-first design
- **JavaScript ES6+** - Interactive UI components optimized for touch devices
- **CSS Grid & Flexbox** - Responsive layouts that adapt to any screen size
- **Media Queries** - Device-specific styling for optimal mobile experience
- **Viewport Meta Tags** - Proper mobile viewport configuration
- **Touch Events** - Enhanced mobile interaction support
- **Jinja2 Templates** - Server-side rendering with mobile optimization
- **Progressive Web App** - Service worker and manifest for app-like experience

### **DevOps & Deployment**
- **[Docker](https://www.docker.com/)** - Containerization for consistent deployments
- **[Docker Compose](https://docs.docker.com/compose/)** - Multi-container orchestration
- **[GitHub Actions](https://github.com/features/actions)** - CI/CD pipeline automation

## 📱 Mobile Support

### **Responsive Design Features**
- **Adaptive Layout**: Automatically adjusts to screen sizes from 320px to 4K displays
- **Touch Optimization**: Large, easy-to-tap buttons and form elements
- **Swipe Gestures**: Navigate through questions with intuitive swipe motions
- **Mobile Navigation**: Collapsible menu system for small screens
- **Readable Typography**: Optimized font sizes and line spacing for mobile reading

### **Mobile Performance**
- **Fast Loading**: Optimized assets and lazy loading for quick mobile access
- **Minimal Data Usage**: Compressed images and efficient API calls
- **Battery Friendly**: Optimized JavaScript to preserve mobile battery life
- **Smooth Animations**: Hardware-accelerated CSS transitions for fluid experience

### **Cross-Device Compatibility**
- **iOS Safari**: Full compatibility with iPhone and iPad devices
- **Android Chrome**: Optimized for Android smartphones and tablets
- **Mobile Firefox**: Support for Firefox mobile browser
- **Edge Mobile**: Compatible with Microsoft Edge mobile
- **WebView**: Works within mobile app WebView components

### **Progressive Web App (PWA) Features**
```json
{
  "name": "PDF Trivia Generator",
  "short_name": "PDFTrivia",
  "description": "Transform PDFs into interactive trivia games",
  "display": "standalone",
  "orientation": "portrait-primary",
  "theme_color": "#005571",
  "background_color": "#ffffff",
  "start_url": "/",
  "icons": [
    {
      "src": "/static/icons/icon-192x192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "/static/icons/icon-512x512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ]
}
```

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
- **Mobile**: Access the same URL from your mobile device on the same network
- **Public Access**: Deploy to a cloud service and access from any mobile device

## 🎯 Usage Guide

### 📝 **Getting Started**
1. **Register/Login** - Create your account or sign in (works seamlessly on mobile)
2. **Upload PDF** - Choose any PDF document from your device (mobile file picker supported)
3. **Generate Trivia** - AI automatically creates questions from your content
4. **Play & Learn** - Answer questions with touch-friendly interface
5. **Review Scores** - Check your trivia history and performance across devices

### 🎮 **Mobile Game Features**
- **Touch Controls**: Tap to select answers, swipe for navigation
- **Vibration Feedback**: Haptic feedback for correct/incorrect answers (on supported devices)
- **Landscape Mode**: Optimized layout for both portrait and landscape orientations
- **Keyboard Support**: External keyboard support for tablets
- **Voice Input**: Speech-to-text for accessibility (browser dependent)

### 📱 **Mobile-Specific Features**
- **File Upload**: Camera integration for PDF scanning and upload
- **Offline Play**: Continue playing generated trivia without internet
- **Push Notifications**: Get notified about new features and updates
- **Share Functionality**: Native mobile sharing of trivia results
- **Home Screen Installation**: Add as PWA for quick access

## 🏛️ Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Mobile Web    │    │   FastAPI       │    │   PostgreSQL    │
│   (Responsive)  │◄──►│   Backend       │◄──►│   Database      │
│                 │    │   + PWA         │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
        │                       │                         │
        │                       ▼                         ▼
        │              ┌─────────────────┐    ┌─────────────────┐
        │              │   OpenAI API    │    │   AWS S3        │
        │              │   (GPT-4)       │    │   Storage       │
        │              └─────────────────┘    └─────────────────┘
        ▼
┌─────────────────┐
│   Service       │
│   Worker        │
│   (Offline)     │
└─────────────────┘
```

### **Mobile Data Flow**
1. **Access**: User opens web app in mobile browser
2. **PWA Install**: Optional installation as home screen app
3. **Upload**: PDF files uploaded via mobile file picker or camera
4. **Processing**: Server-side text extraction and AI processing
5. **Caching**: Trivia questions cached for offline play
6. **Gaming**: Touch-optimized interface for mobile gaming
7. **Sync**: Progress synchronized across all user devices

## 🐳 Docker Hub

The application is available as a Docker image on Docker Hub:

**Pull the image:**
```bash
docker pull shlomi10/pdf-trivia-app:latest
```

**Available tags:**
- `latest` - Latest stable release with mobile optimizations
- Build numbers for CI/CD tracking

## 🔄 CI/CD Pipeline

Automated deployment pipeline using GitHub Actions:

- ✅ **Continuous Integration**: Automated testing on every commit
- 📱 **Mobile Testing**: Cross-browser mobile compatibility tests
- 🏗️ **Docker Build**: Multi-stage builds for optimized images
- 📦 **Registry Push**: Automatic pushes to Docker Hub
- 🚀 **Deployment**: Ready for production deployment with mobile support

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

# Run tests (including mobile compatibility tests)
pytest

# Start development server
uvicorn main:app --reload

# Test mobile responsiveness
# Use browser dev tools or access from mobile device
```

### Mobile Development Guidelines
- Test on multiple screen sizes (320px, 768px, 1024px+)
- Ensure touch targets are at least 44px for accessibility
- Test with slow 3G connections for performance
- Validate PWA functionality with Lighthouse
- Check compatibility across iOS Safari, Android Chrome, and mobile Firefox

## 📋 API Documentation

Once running, visit `/docs` for interactive API documentation powered by FastAPI's automatic OpenAPI generation.

### Key Endpoints:
- `POST /upload-pdf` - Upload PDF and generate trivia (mobile file upload supported)
- `POST /save-score` - Save game results with device information
- `GET /scores` - Retrieve user's trivia history across devices
- `POST /login` - User authentication with mobile-friendly responses
- `POST /register` - User registration optimized for mobile forms
- `GET /manifest.json` - PWA manifest for mobile installation
- `GET /sw.js` - Service worker for offline functionality

## 🧪 Testing

Run the test suite to ensure everything works correctly:

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run all tests including mobile
pytest tests/ -v

# Run mobile-specific tests
pytest tests/test_mobile.py -v

# Test responsive design
pytest tests/test_responsive.py -v

# Run with coverage
pytest --cov=. tests/

# Test PWA functionality
pytest tests/test_pwa.py -v
```

### Mobile Testing Checklist
- [ ] Responsive layout on all screen sizes
- [ ] Touch-friendly interface elements
- [ ] File upload works on mobile browsers
- [ ] PWA installation and offline functionality
- [ ] Performance on slow networks
- [ ] Cross-browser mobile compatibility

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

# Mobile-specific
ENABLE_PWA=true
OFFLINE_MODE=true
MOBILE_OPTIMIZATION=true
```

### Mobile Configuration
```css
/* Viewport Configuration */
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">

/* PWA Configuration */
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="theme-color" content="#005571">

/* Mobile Icons */
<link rel="apple-touch-icon" href="/static/icons/apple-touch-icon.png">
<link rel="manifest" href="/manifest.json">
```

## 🔒 Security Features

- **JWT Authentication** with secure token management on mobile
- **Password Hashing** using bcrypt with salt
- **SQL Injection Protection** via SQLAlchemy ORM
- **File Upload Validation** with content type checking for mobile uploads
- **Secure Cookie Handling** with HttpOnly flags and mobile compatibility
- **HTTPS Enforcement** for secure mobile connections
- **CSP Headers** for mobile security protection

## 📊 Performance

- **Fast Response Times** with FastAPI's async capabilities
- **Mobile-Optimized Loading** with compressed assets and lazy loading
- **Efficient PDF Processing** using PyMuPDF with mobile upload optimization
- **Scalable Architecture** with Docker containerization
- **Optimized Database** queries with SQLAlchemy
- **Mobile Caching** strategies for better performance on mobile networks

## 🛠️ Troubleshooting

### Common Issues:

**Mobile Display Issues:**
```css
/* Check viewport meta tag */
<meta name="viewport" content="width=device-width, initial-scale=1.0">

/* Ensure responsive CSS */
@media (max-width: 768px) {
  /* Mobile styles */
}
```

**File Upload on Mobile:**
```html
<!-- Ensure mobile file input works -->
<input type="file" accept=".pdf" capture="environment">
```

**PWA Installation Issues:**
```bash
# Check manifest.json is accessible
curl http://localhost:8000/manifest.json

# Verify service worker registration
# Check browser console for SW errors
```

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

**AWS S3 Mobile Upload:**
```bash
# Check AWS credentials and CORS settings
aws s3api get-bucket-cors --bucket your-bucket-name
```

## 📈 Roadmap

- [ ] **Native Mobile Apps** - iOS and Android applications
- [ ] **Multi-language Support** - Support for non-English PDFs
- [ ] **Team Competitions** - Multiplayer trivia battles with mobile support
- [ ] **Question Categories** - Filter by topic or difficulty on mobile
- [ ] **Export Features** - Download trivia as Kahoot/Quizlet format from mobile
- [ ] **Enhanced Mobile Features** - Camera PDF scanning, voice commands
- [ ] **Analytics Dashboard** - Detailed performance insights with mobile analytics

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

- **OpenAI** for providing the GPT-4 API
- **FastAPI** team for the excellent web framework
- **AWS** for reliable cloud infrastructure
- **Docker** for containerization technology
- **Web Community** for responsive design best practices and PWA standards

## 📞 Contact

**Shlomi** - [@shlomi10](https://github.com/shlomi10)

**Project Link**: [https://github.com/shlomi10/pdf-trivia-generator](https://github.com/shlomi10/pdf-trivia-generator)

**Docker Hub**: [https://hub.docker.com/r/shlomi10/pdf-trivia-app](https://hub.docker.com/r/shlomi10/pdf-trivia-app)

---

⭐ **Star this repository if you found it helpful!**

📱 **Perfect for mobile learning on the go!**

![Footer](https://img.shields.io/badge/Made%20with-❤️-red?style=for-the-badge)
![Mobile](https://img.shields.io/badge/Mobile-Optimized-green?style=for-the-badge)