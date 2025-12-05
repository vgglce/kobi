#!/bin/bash
# OCR script çalıştırma yardımcısı

# Virtual environment'ı aktif et
source venv/bin/activate

# OCR script'ini çalıştır
python3 ocr.py "$@"

