# 🎥 VIDEO KURULUM REHBERİ - ADIM ADIM

Bu dosya, projeyi sıfırdan kurmak için izleyeceğiniz adımları içerir.

## 🖥️ SİSTEM GEREKSİNİMLERİ

- Ubuntu 20.04+ / Debian / macOS / Windows (WSL2)
- 2GB+ RAM
- 1GB+ Disk alanı
- İnternet bağlantısı

---

## 📹 KURULUM VİDEOSU - ADIMLAR

### 🎬 BÖLÜM 1: Python Kurulumu (5 dakika)

**Adım 1.1 - Python Versiyonunu Kontrol Et**
```bash
python3 --version
```
**Beklenen:** Python 3.9.0 veya üzeri

**Adım 1.2 - Eğer Python yoksa yükle**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3.9 python3-pip python3-venv

# macOS
brew install python@3.9

# Windows (WSL2'de Ubuntu kullan)
```

**Adım 1.3 - Pip'i güncelle**
```bash
python3 -m pip install --upgrade pip
```

---

### 🎬 BÖLÜM 2: Projeyi İndirme (2 dakika)

**Adım 2.1 - Klasör oluştur ve gir**
```bash
mkdir ~/projects
cd ~/projects
```

**Adım 2.2 - Projeyi kopyala (eğer GitHub'da ise)**
```bash
git clone https://github.com/yourusername/crypto-compatibility-engine.git
cd crypto-compatibility-engine
```

**Veya zip'ten çıkar:**
```bash
unzip crypto-compatibility-engine.zip
cd crypto-compatibility-engine
```

**Adım 2.3 - Dosyaları kontrol et**
```bash
ls -la
```
**Görecekleriniz:**
- app.py
- personality.py
- requirements.txt
- setup.sh
- vb.

---

### 🎬 BÖLÜM 3: Otomatik Kurulum (10 dakika)

**Adım 3.1 - Script'leri executable yap**
```bash
chmod +x setup.sh start.sh
```

**Adım 3.2 - Otomatik kurulumu başlat**
```bash
./setup.sh
```

**Kurulum sırasında görecekleriniz:**
```
╔══════════════════════════════════════════════╗
║  🚀 Crypto Compatibility Engine Setup       ║
╚══════════════════════════════════════════════╝

📝 Creating .env file from template...
✅ .env file created!

🐍 Creating Python virtual environment...
✅ Virtual environment created!

🔌 Activating virtual environment...
✅ Virtual environment activated!

📦 Installing dependencies...
[...pip install çıktısı...]
✅ Dependencies installed!

🔍 Checking PostgreSQL...
⚠️  PostgreSQL not found (optional, but recommended)

🔍 Checking Redis...
⚠️  Redis not found (optional, but recommended)

📁 Creating directories...
✅ Directories created!

╔══════════════════════════════════════════════╗
║  ✅ Setup Complete!                          ║
╚══════════════════════════════════════════════╝
```

---

### 🎬 BÖLÜM 4: Database Kurulumu - OPSİYONEL (15 dakika)

**DİKKAT:** Demo mode için bu adım gerekli değil!

**Adım 4.1 - PostgreSQL yükle**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

**Adım 4.2 - PostgreSQL'i başlat**
```bash
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

**Adım 4.3 - PostgreSQL'e gir**
```bash
sudo -u postgres psql
```

**Adım 4.4 - Database oluştur**
PostgreSQL shell'de:
```sql
CREATE DATABASE crypto_compatibility;
CREATE USER cryptouser WITH PASSWORD 'senin_sifren_123';
GRANT ALL PRIVILEGES ON DATABASE crypto_compatibility TO cryptouser;
\q
```

**Adım 4.5 - .env dosyasını düzenle**
```bash
nano .env
```

Şu satırı bul ve düzenle:
```env
DATABASE_URL=postgresql://cryptouser:senin_sifren_123@localhost:5432/crypto_compatibility
```

Kaydet: `Ctrl+O`, Enter, Çık: `Ctrl+X`

---

### 🎬 BÖLÜM 5: API Key'leri Ayarlama - OPSİYONEL (10 dakika)

**DİKKAT:** Demo mode için bu adım gerekli değil!

**Adım 5.1 - OpenAI API Key Al**

1. Tarayıcıda aç: https://platform.openai.com/
2. Sign up / Login yap
3. Sol menüden "API Keys" seç
4. "Create new secret key" butonuna tıkla
5. İsim ver (örn: "crypto-compatibility")
6. Key'i kopyala (sk-... ile başlar)

**Adım 5.2 - Neynar (Farcaster) API Key Al**

1. Tarayıcıda aç: https://neynar.com/
2. Sign up / Login yap
3. "Developer Console" git
4. "Create New App" tıkla
5. Uygulama adı ver
6. API Key'i kopyala

**Adım 5.3 - .env dosyasına ekle**
```bash
nano .env
```

Şu satırları düzenle:
```env
OPENAI_API_KEY=sk-your-actual-openai-key-here
FARCASTER_API_KEY=your-actual-neynar-key-here
```

**Adım 5.4 - app.py'yi düzenle (Production mode için)**
```bash
nano app.py
```

20-21. satırları bul:
```python
matchmaker = MatchmakerAI(use_mock_data=True)  # Demo mode
```

Şu şekilde değiştir:
```python
matchmaker = MatchmakerAI(use_mock_data=False)  # Production mode
```

---

### 🎬 BÖLÜM 6: Placeholder Görseller Oluşturma (2 dakika)

**Adım 6.1 - Görsel oluştur**
```bash
python3 create_images.py
```

**Çıktı:**
```
🎨 Creating placeholder images...
✅ Created: static/images/start.png
✅ Created: static/images/analyzing.png
✅ Created: static/images/no-matches.png
✅ Created: static/images/error.png
✅ Created: static/images/rate-limit.png
✅ Created: static/images/info.png
✅ Created: static/images/placeholder.png

✨ All placeholder images created!
```

---

### 🎬 BÖLÜM 7: Test Çalıştırma (3 dakika)

**Adım 7.1 - Virtual environment'ı aktif et**
```bash
source venv/bin/activate
```
Prompt'un başına `(venv)` eklenmeli.

**Adım 7.2 - Test çalıştır**
```bash
python3 test.py
```

**Beklenen çıktı:**
```
🧪 Testing Crypto Compatibility Engine...
==================================================

1️⃣  Testing imports...
✅ All modules imported successfully

2️⃣  Testing Personality Analyzer...
✅ Found 12 personality types
✅ Personality analysis working: Bitcoin Purist

3️⃣  Testing Comedy Generator...
✅ Comedy generation working
   Sample: You two are like ETH and gas fees - inseparable! 💕

4️⃣  Testing Farcaster Client...
✅ Farcaster client working
   Mock user: cryptoking_12345

5️⃣  Testing Matchmaker AI...
✅ User analysis working: DeFi Degenerate
✅ Match finding working: Found 3 matches
   Top match: 88% with shitcoin_surfer_67890

6️⃣  Testing Frame Generator...
✅ Frame generation working
   Frame has 2 buttons

7️⃣  Testing Database...
⚠️  Database test skipped (this is OK for demo mode)

==================================================
🎉 All tests passed!
==================================================
```

---

### 🎬 BÖLÜM 8: Uygulamayı Başlatma (1 dakika)

**Adım 8.1 - Start script ile başlat**
```bash
./start.sh
```

**Veya manuel:**
```bash
source venv/bin/activate
python app.py
```

**Çıktı:**
```
🚀 Starting Crypto Compatibility Engine...

✅ Virtual environment activated
🌐 Starting server on http://localhost:8000

INFO:     Started server process
INFO:     Waiting for application startup.
🚀 Starting Crypto Compatibility Engine...
✅ Database connected
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000

    ╔══════════════════════════════════════════════╗
    ║  🚀 Crypto Compatibility Engine Started!    ║
    ║                                              ║
    ║  🌐 Server: http://0.0.0.0:8000             ║
    ║  📚 Docs: http://0.0.0.0:8000/docs          ║
    ║  ❤️  Frames: http://0.0.0.0:8000/           ║
    ╚══════════════════════════════════════════════╝
```

---

### 🎬 BÖLÜM 9: Tarayıcıda Test (3 dakika)

**Adım 9.1 - Ana sayfa**
1. Tarayıcı aç
2. Git: http://localhost:8000
3. Frame preview görmelisin

**Adım 9.2 - API Documentation**
1. Git: http://localhost:8000/docs
2. Swagger UI göreceksin
3. Endpoint'leri test edebilirsin

**Adım 9.3 - API Test**

**Test 1: Health Check**
```bash
curl http://localhost:8000/api/health
```
Response:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "service": "Crypto Compatibility Engine"
}
```

**Test 2: Kişilikleri Listele**
```bash
curl http://localhost:8000/api/personalities
```

**Test 3: Kullanıcı Analizi**
```bash
curl http://localhost:8000/api/user/12345
```

**Test 4: Uyum Kontrolü**
```bash
curl http://localhost:8000/api/compatibility/12345/67890
```

---

### 🎬 BÖLÜM 10: Durdurma ve Yeniden Başlatma

**Durdurmak için:**
```bash
# Terminal'de Ctrl+C
```

**Yeniden başlatmak için:**
```bash
./start.sh
```

**Veya:**
```bash
source venv/bin/activate
python app.py
```

---

## 🔧 SORUN GİDERME VİDEOSU

### Problem 1: "Module not found" hatası

**Çözüm:**
```bash
# Virtual environment aktif mi kontrol et
which python
# /home/user/projects/crypto-compatibility-engine/venv/bin/python olmalı

# Değilse aktif et
source venv/bin/activate

# Kütüphaneleri tekrar yükle
pip install -r requirements.txt
```

### Problem 2: "Port already in use"

**Çözüm:**
```bash
# Portu kullanan process'i bul
lsof -i :8000

# Process'i kapat
kill -9 [PID]

# Veya farklı port kullan
APP_PORT=8001 python app.py
```

### Problem 3: Database bağlanamıyor

**Çözüm:**
```bash
# PostgreSQL çalışıyor mu?
sudo systemctl status postgresql

# Çalışmıyorsa başlat
sudo systemctl start postgresql

# Hala sorun varsa demo mode'da çalıştır
# (zaten default olarak çalışır)
```

### Problem 4: Permission denied

**Çözüm:**
```bash
# Script'lere çalıştırma izni ver
chmod +x setup.sh start.sh

# Tekrar dene
./setup.sh
```

---

## 📱 MOBİL CIHAZDAN ERIŞIM

### Adım 1: IP Adresini Bul
```bash
hostname -I
# Örnek çıktı: 192.168.1.100
```

### Adım 2: Firewall'u Aç (Gerekirse)
```bash
sudo ufw allow 8000
```

### Adım 3: Mobil Cihazdan Bağlan
- Mobil tarayıcıda: http://192.168.1.100:8000
- Aynı WiFi ağında olmalısınız!

---

## 🐳 DOCKER İLE KURULUM (ALTERNATİF)

### Adım 1: Docker Yükle
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

### Adım 2: Docker Compose ile Başlat
```bash
cd crypto-compatibility-engine
docker-compose up -d
```

### Adım 3: Logları İzle
```bash
docker-compose logs -f app
```

### Adım 4: Durdur
```bash
docker-compose down
```

---

## 🎓 İLERİ SEVİYE AYARLAR

### Production Deployment

**Vercel:**
```bash
npm install -g vercel
vercel login
vercel
```

**Railway:**
```bash
# railway.app'te proje oluştur
# GitHub'a push et
# Otomatik deploy olur
```

**Render:**
```bash
# render.com'da web service oluştur
# GitHub repo bağla
# Environment variables ekle
# Deploy!
```

---

## 📞 YARDIM

### Hata Aldıysanız:
1. Test scriptini çalıştırın: `python3 test.py`
2. Logları kontrol edin
3. README.md'deki troubleshooting bölümüne bakın
4. GitHub issues'a yazın

### Başarıyla Çalışıyorsa:
1. ⭐ GitHub'da yıldız verin
2. 🎉 Farcaster'da paylaşın
3. 💕 Matchmaking'in tadını çıkarın!

---

**Video bitişi:** "Tebrikler! Crypto Compatibility Engine'iniz hazır. Happy matching! 🚀💕"

**Total Video Süresi:** ~45 dakika
**Zorluk Seviyesi:** Başlangıç-Orta
**Gerekli Ön Bilgi:** Temel terminal kullanımı
