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

# Uygulama dosyalarını kopyala
COPY app.py .
COPY ocr.py .

# Port (Render.com PORT environment variable'ını kullanacak)
EXPOSE 8000

# Uygulamayı çalıştır (PORT environment variable'ını kullan)
# Render.com her deploy'da PORT verir, app.py bunu okuyor
CMD python app.py
