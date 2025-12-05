# Python base image
FROM python:3.11-slim

# Sistem bağımlılıklarını yükle
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-tur \
    poppler-utils \
    libpoppler-cpp-dev \
    && rm -rf /var/lib/apt/lists/*

# Çalışma dizini
WORKDIR /app

# Python bağımlılıklarını kopyala ve yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# pdf2image'ın poppler yolunu bulması için ENV ekliyoruz
ENV POPPLER_PATH=/usr/bin

# Tüm proje dosyalarını kopyala
COPY . .

# Railway’in verdiği PORT değerini kullan
ENV PORT=$PORT

# Railway için doğru startup komutu
CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port ${PORT}"]
