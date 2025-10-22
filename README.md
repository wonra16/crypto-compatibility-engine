# 🚀 Crypto Compatibility Engine

**AI-destekli Crypto Dating Frame for Farcaster**

Kullanıcıların crypto kişiliklerini analiz edip, uyumlu eşleşmeler bulan viral dating frame kütüphanesi.

---

## 📋 İçindekiler

1. [Özellikler](#özellikler)
2. [Kurulum](#kurulum)
3. [Konfigürasyon](#konfigürasyon)
4. [Kullanım](#kullanım)
5. [API Endpoints](#api-endpoints)
6. [Deployment](#deployment)
7. [Geliştirme](#geliştirme)

---

## ✨ Özellikler

- **12 Farklı Crypto Kişilik Tipi**: Bitcoin Purist'ten DeFi Degenerate'e
- **AI-Powered Comedy**: GPT-4 ile komik yorumlar
- **Akıllı Eşleştirme**: Kişilik ve trait bazlı uyum algoritması
- **Farcaster Frames v2**: İnteraktif kullanıcı deneyimi
- **Viral Paylaşım**: Optimize edilmiş share formatları
- **Rate Limiting**: Günlük 100 istek limiti
- **PostgreSQL + Redis**: Hızlı caching ve veri saklama

---

## 🔧 Kurulum

### Gereksinimler

- Python 3.9 veya üzeri
- PostgreSQL 12+ 
- Redis (opsiyonel ama önerilen)
- OpenAI API Key
- Farcaster API Key (Neynar)

### Adım 1: Repository'i İndirin

```bash
git clone https://github.com/yourusername/crypto-compatibility-engine.git
cd crypto-compatibility-engine
```

### Adım 2: Conda veya Python Virtual Environment Oluşturun

**Conda ile:**
```bash
conda create -n cryptomatch python=3.9
conda activate cryptomatch
```

**Venv ile:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# veya
venv\Scripts\activate  # Windows
```

### Adım 3: Bağımlılıkları Yükleyin

```bash
pip install -r requirements.txt
```

### Adım 4: Veritabanı Kurulumu

**PostgreSQL Kurulumu (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

**Database Oluşturma:**
```bash
sudo -u postgres psql
```

PostgreSQL shell'de:
```sql
CREATE DATABASE crypto_compatibility;
CREATE USER cryptouser WITH PASSWORD 'your_password_here';
GRANT ALL PRIVILEGES ON DATABASE crypto_compatibility TO cryptouser;
\q
```

**Redis Kurulumu (Opsiyonel):**
```bash
sudo apt install redis-server
sudo systemctl start redis
sudo systemctl enable redis
```

### Adım 5: Environment Variables

`.env.example` dosyasını `.env` olarak kopyalayın:

```bash
cp .env.example .env
```

`.env` dosyasını düzenleyin:

```bash
nano .env
```

**Gerekli Ayarlar:**
```env
# OpenAI API (ZORUNLU - comedy generation için)
OPENAI_API_KEY=sk-your-openai-api-key-here

# Farcaster API (ZORUNLU - kullanıcı verileri için)
FARCASTER_API_KEY=your-neynar-api-key-here
FARCASTER_APP_FID=your-app-fid

# PostgreSQL (ZORUNLU)
DATABASE_URL=postgresql://cryptouser:your_password_here@localhost:5432/crypto_compatibility

# Redis (Opsiyonel)
REDIS_HOST=localhost
REDIS_PORT=6379

# App Config
BASE_URL=http://localhost:8000
APP_ENV=development
APP_PORT=8000
SECRET_KEY=change-this-to-random-string-in-production
```

---

## 🎯 Konfigürasyon

### OpenAI API Key Alma

1. https://platform.openai.com/ adresine gidin
2. Sign up / Login
3. "API Keys" bölümüne gidin
4. "Create new secret key" tıklayın
5. Key'i kopyalayıp `.env` dosyasına yapıştırın

### Farcaster (Neynar) API Key Alma

1. https://neynar.com/ adresine gidin
2. Sign up / Login
3. Developer Console'a gidin
4. "Create New App" yapın
5. API Key'inizi kopyalayın
6. `.env` dosyasına yapıştırın

**NOT:** Demo mode'da çalıştırmak isterseniz API key'ler olmadan da çalışır (mock data ile).

---

## 🚀 Kullanım

### Development Mode'da Başlatma

```bash
python app.py
```

Veya uvicorn ile:

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

Başarılı başlatma sonrası göreceksiniz:

```
╔══════════════════════════════════════════════╗
║  🚀 Crypto Compatibility Engine Started!    ║
║  🌐 Server: http://0.0.0.0:8000             ║
║  📚 Docs: http://0.0.0.0:8000/docs          ║
║  ❤️  Frames: http://0.0.0.0:8000/           ║
╚══════════════════════════════════════════════╝
```

### Tarayıcıda Test Etme

1. Tarayıcınızda `http://localhost:8000` açın
2. Frame preview'ini göreceksiniz
3. API documentation: `http://localhost:8000/docs`

### Demo Mode (API Key'siz Test)

Eğer henüz API key'leriniz yoksa, `app.py` dosyasında:

```python
matchmaker = MatchmakerAI(use_mock_data=True)  # Mock data kullan
```

Bu şekilde sahte verilerle test edebilirsiniz.

---

## 📡 API Endpoints

### Frame Endpoints (Farcaster için)

- `GET /` - Ana frame (başlangıç)
- `POST /api/analyze` - Kişilik analizi
- `POST /api/find-matches` - Eşleşme bul
- `POST /api/match/{index}` - Belirli eşleşmeyi göster
- `POST /api/match-details/{index}` - Detaylı analiz
- `POST /api/share/{index}` - Paylaş

### Public API Endpoints

```bash
# Health check
GET /api/health

# Tüm kişilikleri listele
GET /api/personalities

# Kullanıcı analizi
GET /api/user/{fid}

# İki kullanıcı arası uyum
GET /api/compatibility/{fid1}/{fid2}

# Analytics
GET /api/analytics
```

### Örnek API Kullanımı

**Python:**
```python
import requests

# Kullanıcı analizi
response = requests.get('http://localhost:8000/api/user/12345')
data = response.json()
print(f"Personality: {data['personality_name']}")

# Uyum kontrolü
response = requests.get('http://localhost:8000/api/compatibility/12345/67890')
match_data = response.json()
print(f"Compatibility: {match_data['compatibility_score']}%")
```

**JavaScript:**
```javascript
// Kullanıcı analizi
fetch('http://localhost:8000/api/user/12345')
  .then(res => res.json())
  .then(data => console.log(data.personality_name));

// Uyum kontrolü
fetch('http://localhost:8000/api/compatibility/12345/67890')
  .then(res => res.json())
  .then(data => console.log(`${data.compatibility_score}% compatible!`));
```

**cURL:**
```bash
# Kullanıcı analizi
curl http://localhost:8000/api/user/12345

# Uyum kontrolü
curl http://localhost:8000/api/compatibility/12345/67890

# Kişilikleri listele
curl http://localhost:8000/api/personalities
```

---

## 🌐 Deployment

### Vercel ile Deploy

1. Vercel hesabı oluşturun: https://vercel.com
2. Repository'nizi GitHub'a push edin
3. Vercel'de "New Project" tıklayın
4. GitHub repo'nuzu seçin
5. Environment Variables ekleyin (`.env` içindekiler)
6. Deploy!

**vercel.json** örneği:
```json
{
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ]
}
```

### Render.com ile Deploy

1. Render hesabı oluşturun: https://render.com
2. "New Web Service" seçin
3. GitHub repo'nuzu bağlayın
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `uvicorn app:app --host 0.0.0.0 --port $PORT`
6. Environment Variables ekleyin
7. Deploy!

### Railway ile Deploy

1. Railway hesabı: https://railway.app
2. "New Project" > "Deploy from GitHub"
3. Repository seçin
4. PostgreSQL service ekleyin
5. Environment Variables ayarlayın
6. Auto-deploy!

### Docker ile Deploy

**Dockerfile:**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Build & Run:**
```bash
docker build -t crypto-compatibility .
docker run -p 8000:8000 --env-file .env crypto-compatibility
```

---

## 🔍 Troubleshooting

### Problem: Database bağlanamıyor

**Çözüm:**
```bash
# PostgreSQL çalışıyor mu kontrol et
sudo systemctl status postgresql

# PostgreSQL'i başlat
sudo systemctl start postgresql

# Connection string'i kontrol et
psql postgresql://cryptouser:password@localhost:5432/crypto_compatibility
```

### Problem: OpenAI API hatası

**Çözüm:**
- API key'inizin doğru olduğundan emin olun
- OpenAI hesabınızda kredi olup olmadığını kontrol edin
- Rate limit'e takılmış olabilirsiniz (biraz bekleyin)

### Problem: Farcaster API çalışmıyor

**Çözüm:**
- Demo mode'da test edin: `use_mock_data=True`
- Neynar API key'inizin aktif olduğunu kontrol edin
- Rate limit olabilir

### Problem: Port zaten kullanımda

**Çözüm:**
```bash
# Portu kullanan process'i bul
lsof -i :8000

# Process'i öldür
kill -9 <PID>

# Veya farklı port kullan
APP_PORT=8001 python app.py
```

---

## 🛠️ Geliştirme

### Yeni Kişilik Tipi Ekleme

`personality_profiles/personalities.json` dosyasını düzenleyin:

```json
{
  "id": "new_personality",
  "name": "New Personality",
  "emoji": "🎯",
  "description": "Description here",
  "traits": {
    "token_preference": "btc_only",
    "risk_tolerance": 50,
    "nft_interest": 50,
    "defi_engagement": 50,
    "meme_coin_tolerance": 50
  },
  "comedy_lines": [
    "Funny line 1",
    "Funny line 2"
  ]
}
```

### Yeni Komedi Şablonu Ekleme

`comedy_templates/comedy.json` dosyasını düzenleyin.

### Custom Image Generation

`app.py` içinde image generation endpoint'lerini düzenleyin:

```python
from PIL import Image, ImageDraw, ImageFont

@app.get("/api/generate-image/personality")
async def generate_personality_image(data: str):
    # PIL ile image oluştur
    img = Image.new('RGB', (600, 600), color='purple')
    # ... image processing
    return Response(content=img_bytes, media_type='image/png')
```

---

## 📊 Analytics

Analytics verileri otomatik olarak topla nır:

```python
# Analytics sorgulama
stats = await db.get_analytics_summary(days=7)

# Returns:
{
  "total_users": 1234,
  "total_matches": 5678,
  "popular_personalities": [
    {"personality_type": "defi_degenerate", "count": 234}
  ]
}
```

---

## 🤝 Katkıda Bulunma

1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit edin (`git commit -m 'Add amazing feature'`)
4. Push edin (`git push origin feature/amazing-feature`)
5. Pull Request açın

---

## 📝 License

MIT License - detaylar için LICENSE dosyasına bakın

---

## 🙏 Teşekkürler

- Farcaster ekibine
- OpenAI'ye
- Tüm crypto community'ye

---

## 📞 Destek

- GitHub Issues: [Create an issue](https://github.com/yourusername/crypto-compatibility-engine/issues)
- Discord: [Join our community](#)
- Twitter: [@yourhandle](#)

---

**⭐ Beğendiyseniz yıldız vermeyi unutmayın!**
