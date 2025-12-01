# OCR Script - Kullanım Kılavuzu

Bu script PDF ve görüntü dosyalarından OCR (Optical Character Recognition) ile metin çıkarır.

## Kurulum

### 1. Virtual Environment Oluştur ve Aktif Et

```bash
# Virtual environment oluştur (sadece ilk seferde)
python3 -m venv venv

# Virtual environment'ı aktif et
source venv/bin/activate
```

### 2. Python Paketlerini Yükle

```bash
# Virtual environment aktifken
pip install -r requirements.txt
```

**Not:** Her kullanımda önce `source venv/bin/activate` komutunu çalıştırmanız gerekir.

### 2. Tesseract OCR Kurulumu

**macOS:**
```bash
brew install tesseract tesseract-lang
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install tesseract-ocr tesseract-ocr-tur
```

**Windows:**
[Tesseract installer](https://github.com/UB-Mannheim/tesseract/wiki) indirip kurun.

## PDF Dosyasını Nereye Koymalıyım?

PDF dosyanızı **herhangi bir yere** koyabilirsiniz! Script, dosyanın tam yolunu kabul eder.

### Seçenek 1: Proje Klasörüne Koy (En Kolay)

PDF dosyanızı `/Users/ovgulec/ocr/` klasörüne kopyalayın, sonra:

```bash
./run.sh dosya.pdf
```

### Seçenek 2: Tam Yol Kullan

PDF dosyanız başka bir yerdeyse, tam yolunu belirtin:

```bash
./run.sh /Users/ovgulec/Downloads/belge.pdf
```

veya

```bash
./run.sh ~/Desktop/belge.pdf
```

## Kullanım

**ÖNEMLİ:** Her kullanımda önce virtual environment'ı aktif edin (veya `run.sh` kullanın):

```bash
source venv/bin/activate
```

### Temel Kullanım

```bash
# PDF dosyası için (aynı klasördeyse)
./run.sh dosya.pdf

# veya tam yol ile
./run.sh /path/to/dosya.pdf

# Görüntü dosyası için (PNG, JPG, vb.)
./run.sh resim.png
```

### Seçenekler

```bash
# Özel çıktı dosyası belirtme
python3 ocr.py dosya.pdf -o sonuc.txt

# Dil seçimi (varsayılan: tur+eng)
python3 ocr.py dosya.pdf -l tur        # Sadece Türkçe
python3 ocr.py dosya.pdf -l eng        # Sadece İngilizce
python3 ocr.py dosya.pdf -l tur+eng    # Türkçe + İngilizce

# PDF için DPI ayarı (varsayılan: 300)
python3 ocr.py dosya.pdf --dpi 400

# Yardım
python3 ocr.py --help
```

## Örnekler

```bash
# Basit kullanım
python3 ocr.py belge.pdf

# Sonucu farklı dosyaya kaydet
python3 ocr.py belge.pdf -o cikti.txt

# Yüksek kalite için DPI artır
python3 ocr.py belge.pdf --dpi 400 -o yuksek_kalite.txt
```

## Çıktı

Script, OCR sonuçlarını `ocr_sonuc.txt` dosyasına (veya belirttiğiniz dosyaya) kaydeder.

Her sayfa için:
- Sayfa numarası
- OCR edilen metin

içerir.

