# Python base image
FROM python:3.11-slim

# Sistem bağımlılıklarını yükle
COPY apt.txt /tmp/apt.txt
RUN apt-get update && \
    xargs -a /tmp/apt.txt apt-get install -y && \
    rm -rf /var/lib/apt/lists/* && \
    rm /tmp/apt.txt

# Çalışma dizini
WORKDIR /app

# Python bağımlılıklarını kopyala ve yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama dosyalarını kopyala
COPY app.py .
COPY ocr.py .

# Port
EXPOSE 8000

# Uygulamayı çalıştır
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

