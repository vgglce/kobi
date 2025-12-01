#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OCR Script - PDF ve görüntü dosyalarından metin çıkarma
"""

import pytesseract
import argparse
import sys
import os
from pathlib import Path
from PIL import Image

try:
    from pdf2image import convert_from_path
    PDF_SUPPORT = True
except ImportError:
    PDF_SUPPORT = False
    print("Uyarı: pdf2image yüklü değil. PDF desteği devre dışı.")


def ocr_image(image_path, lang="tur+eng"):
    """Görüntü dosyasından OCR yapar"""
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image, lang=lang)
        return text
    except Exception as e:
        print(f"Hata ({image_path}): {e}")
        return ""


def ocr_pdf(pdf_path, lang="tur+eng", dpi=300):
    """PDF dosyasından OCR yapar"""
    if not PDF_SUPPORT:
        print("Hata: PDF desteği için pdf2image paketini yükleyin: pip install pdf2image")
        return None
    
    try:
        print(f"PDF yükleniyor: {pdf_path}")
        pages = convert_from_path(pdf_path, dpi=dpi)
        
        all_text = ""
        total_pages = len(pages)
        
        for i, page in enumerate(pages, 1):
            print(f"[{i}/{total_pages}] Sayfa OCR ediliyor...")
            text = pytesseract.image_to_string(page, lang=lang)
            all_text += f"\n\n{'='*50}\nSAYFA {i}\n{'='*50}\n{text}"
        
        return all_text
    except Exception as e:
        print(f"Hata: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(
        description="PDF veya görüntü dosyalarından OCR ile metin çıkarır",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("input_file", help="Giriş dosyası (PDF, PNG, JPG, vb.)")
    parser.add_argument("-o", "--output", help="Çıktı dosyası (varsayılan: ocr_sonuc.txt)")
    parser.add_argument("-l", "--lang", default="tur+eng", 
                       help="OCR dili (varsayılan: tur+eng)")
    parser.add_argument("--dpi", type=int, default=300,
                       help="PDF için DPI değeri (varsayılan: 300)")
    
    args = parser.parse_args()
    
    input_path = Path(args.input_file)
    
    # Dosya kontrolü
    if not input_path.exists():
        print(f"Hata: Dosya bulunamadı: {input_path}")
        sys.exit(1)
    
    # Çıktı dosyası adı
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = Path("ocr_sonuc.txt")
    
    # Dosya tipine göre işle
    file_ext = input_path.suffix.lower()
    
    print(f"OCR başlatılıyor...")
    print(f"Dosya: {input_path}")
    print(f"Dil: {args.lang}")
    
    if file_ext == ".pdf":
        text = ocr_pdf(str(input_path), lang=args.lang, dpi=args.dpi)
    elif file_ext in [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff", ".tif"]:
        print("Görüntü OCR ediliyor...")
        text = ocr_image(str(input_path), lang=args.lang)
        if text:
            text = f"{'='*50}\n{input_path.name}\n{'='*50}\n{text}"
    else:
        print(f"Uyarı: Desteklenmeyen dosya tipi: {file_ext}")
        print("Görüntü olarak işlenmeye çalışılıyor...")
        text = ocr_image(str(input_path), lang=args.lang)
        if text:
            text = f"{'='*50}\n{input_path.name}\n{'='*50}\n{text}"
    
    # Sonucu kaydet
    if text:
        try:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(text)
            print(f"\n✓ OCR tamamlandı!")
            print(f"✓ Sonuç kaydedildi: {output_path}")
            print(f"✓ Toplam karakter: {len(text)}")
        except Exception as e:
            print(f"Hata: Dosya yazılamadı: {e}")
            sys.exit(1)
    else:
        print("Hata: OCR sonucu boş!")
        sys.exit(1)


if __name__ == "__main__":
    main()
