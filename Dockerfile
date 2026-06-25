# 🔧 Base image with Python
FROM python:3.11-slim

# 📁 Set working directory
WORKDIR /app

# 📦 Copy requirements file
COPY requirements.txt .

# 🚀 Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 📂 Copy project files
COPY . .

# 🌐 Expose FastAPI default port
EXPOSE 8000

# ▶️ Run the FastAPI app with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]