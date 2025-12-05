# OCR API - PDF ve Görüntü OCR Servisi

Bu proje PDF ve görüntü dosyalarından OCR (Optical Character Recognition) ile metin çıkaran bir REST API servisidir. Render.com'da deploy edilebilir ve n8n gibi otomasyon araçlarından kullanılabilir.

## Özellikler

- ✅ PDF ve görüntü dosyalarından OCR
- ✅ REST API (FastAPI)
- ✅ Docker desteği
- ✅ Render.com deployment hazır
- ✅ n8n entegrasyonu için uygun
- ✅ Türkçe ve İngilizce dil desteği

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

---

## 🌐 API Kullanımı (Render.com Deployment)

### Render.com'da Deploy Etme

1. **GitHub'a push edin:**
   ```bash
   git add .
   git commit -m "Add API and Docker support"
   git push origin main
   ```

2. **Render.com'da yeni servis oluşturun:**
   - Render.com dashboard'a gidin
   - "New +" → "Web Service" seçin
   - GitHub repo'nuzu bağlayın
   - **Environment:** Docker
   - **Dockerfile Path:** `./Dockerfile`
   - **Start Command:** (otomatik algılanır)
   - Deploy edin!

3. **API URL'inizi alın:**
   - Render.com size bir URL verecek: `https://your-app.onrender.com`

### API Endpoints

#### `GET /`
API bilgileri

#### `GET /health`
Sağlık kontrolü

#### `POST /ocr`
Dosya yükleyip OCR yap

**Request:**
- Method: `POST`
- Content-Type: `multipart/form-data`
- Body:
  - `file`: (file) Yüklenecek dosya
  - `lang`: (optional, default: "tur+eng") OCR dili
  - `dpi`: (optional, default: 300) PDF için DPI

**Response:**
```json
{
  "success": true,
  "filename": "document.pdf",
  "text": "OCR edilen metin...",
  "character_count": 1234,
  "page_count": 5,
  "language": "tur+eng"
}
```

### cURL Örneği

```bash
curl -X POST "https://your-app.onrender.com/ocr" \
  -F "file=@document.pdf" \
  -F "lang=tur+eng" \
  -F "dpi=300"
```

### Python Örneği

```python
import requests

url = "https://your-app.onrender.com/ocr"
files = {"file": open("document.pdf", "rb")}
data = {"lang": "tur+eng", "dpi": 300}

response = requests.post(url, files=files, data=data)
result = response.json()

print(result["text"])
print(f"Karakter sayısı: {result['character_count']}")
```

### n8n Kullanımı

n8n'de HTTP Request node'u kullanarak:

1. **HTTP Request Node ekleyin:**
   - Method: `POST`
   - URL: `https://your-app.onrender.com/ocr`
   - Authentication: None
   - Body Type: `Multipart-Form-Data`
   - Parameters:
     - `file`: (File) Dosya
     - `lang`: `tur+eng` (optional)
     - `dpi`: `300` (optional)

2. **Response'u kullanın:**
   - `{{ $json.text }}` - OCR edilen metin
   - `{{ $json.character_count }}` - Karakter sayısı
   - `{{ $json.page_count }}` - Sayfa sayısı

### JavaScript/Node.js Örneği

```javascript
const FormData = require('form-data');
const fs = require('fs');
const axios = require('axios');

const form = new FormData();
form.append('file', fs.createReadStream('document.pdf'));
form.append('lang', 'tur+eng');
form.append('dpi', '300');

axios.post('https://your-app.onrender.com/ocr', form, {
  headers: form.getHeaders()
})
.then(response => {
  console.log(response.data.text);
})
.catch(error => {
  console.error(error);
});
```

---

## 🐳 Docker ile Lokal Test

```bash
# Docker image oluştur
docker build -t ocr-api .

# Container çalıştır
docker run -p 8000:8000 ocr-api

# API'yi test et
curl -X POST "http://localhost:8000/ocr" \
  -F "file=@test.pdf"
```

---

## 📝 Notlar

- API timeout'ları için Render.com'da planınızı kontrol edin
- Büyük PDF'ler için işlem süresi uzayabilir
- n8n'de timeout ayarlarını artırmanız gerekebilir

