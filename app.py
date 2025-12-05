#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OCR API - FastAPI ile PDF ve görüntü dosyalarından OCR
n8n ve diğer servislerden kullanım için REST API
"""

from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import tempfile
import os
from pathlib import Path
import pytesseract
from PIL import Image

try:
    from pdf2image import convert_from_path
    PDF_SUPPORT = True
except ImportError:
    PDF_SUPPORT = False

app = FastAPI(
    title="OCR API",
    description="PDF ve görüntü dosyalarından OCR ile metin çıkarma API'si",
    version="1.0.0"
)

# CORS ayarları - n8n ve diğer servislerden erişim için
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Production'da spesifik domain'ler belirtin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def ocr_image(image_path: str, lang: str = "tur+eng") -> str:
    """Görüntü dosyasından OCR yapar"""
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image, lang=lang)
        return text.strip()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR hatası: {str(e)}")


def ocr_pdf(pdf_path: str, lang: str = "tur+eng", dpi: int = 300) -> str:
    """PDF dosyasından OCR yapar"""
    if not PDF_SUPPORT:
        raise HTTPException(
            status_code=500, 
            detail="PDF desteği için pdf2image paketi gerekli"
        )
    
    try:
        pages = convert_from_path(pdf_path, dpi=dpi)
        all_text = ""
        total_pages = len(pages)
        
        for i, page in enumerate(pages, 1):
            text = pytesseract.image_to_string(page, lang=lang)
            all_text += f"\n\n{'='*50}\nSAYFA {i}/{total_pages}\n{'='*50}\n{text}"
        
        return all_text.strip()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF OCR hatası: {str(e)}")


@app.get("/")
async def root():
    """API ana sayfası"""
    return {
        "message": "OCR API",
        "version": "1.0.0",
        "endpoints": {
            "POST /ocr": "Dosya yükleyip OCR yap",
            "GET /health": "API sağlık kontrolü"
        }
    }


@app.get("/health")
async def health():
    """API sağlık kontrolü"""
    return {
        "status": "healthy",
        "pdf_support": PDF_SUPPORT,
        "tesseract_available": True
    }


@app.post("/ocr")
async def process_ocr(
    file: UploadFile = File(...),
    lang: Optional[str] = Form("tur+eng"),
    dpi: Optional[int] = Form(300)
):
    """
    PDF veya görüntü dosyası yükleyip OCR yapar
    
    Parameters:
    - file: Yüklenecek dosya (PDF, PNG, JPG, vb.)
    - lang: OCR dili (varsayılan: tur+eng)
    - dpi: PDF için DPI değeri (varsayılan: 300)
    
    Returns:
    - JSON response: text, character_count, page_count
    """
    # Geçici dosya oluştur
    temp_dir = tempfile.mkdtemp()
    filename = file.filename or "uploaded_file"
    temp_file_path = os.path.join(temp_dir, filename)
    
    try:
        # Dosyayı kaydet
        with open(temp_file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Dosya tipini belirle
        file_ext = Path(filename).suffix.lower()
        
        # OCR işlemi
        if file_ext == ".pdf":
            text = ocr_pdf(temp_file_path, lang=lang, dpi=dpi)
            # PDF sayfa sayısını tahmin et
            try:
                pages = convert_from_path(temp_file_path, dpi=dpi)
                page_count = len(pages)
            except:
                page_count = 1
        elif file_ext in [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff", ".tif"]:
            text = ocr_image(temp_file_path, lang=lang)
            page_count = 1
        else:
            # Bilinmeyen tip, görüntü olarak dene
            text = ocr_image(temp_file_path, lang=lang)
            page_count = 1
        
        # Sonucu döndür
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "filename": filename,
                "text": text,
                "character_count": len(text),
                "page_count": page_count,
                "language": lang
            }
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"İşlem hatası: {str(e)}"
        )
    finally:
        # Geçici dosyaları temizle
        try:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
            if os.path.exists(temp_dir):
                os.rmdir(temp_dir)
        except:
            pass


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

