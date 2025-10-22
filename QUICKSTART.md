# ⚡ 5 Dakikada Başlangıç Rehberi

Crypto Compatibility Engine'i hızlıca çalıştırmak için bu adımları takip edin.

## 🎯 Hızlı Kurulum (API Key'siz Demo)

### 1. Gerekli Yazılımları Yükleyin

```bash
# Python 3.9+ yüklü mü kontrol edin
python3 --version

# Eğer yoksa:
sudo apt update
sudo apt install python3.9 python3-pip python3-venv
```

### 2. Projeyi İndirin

```bash
cd ~/
git clone https://github.com/yourusername/crypto-compatibility-engine.git
cd crypto-compatibility-engine
```

### 3. Otomatik Kurulum Çalıştırın

```bash
# Executable yapın
chmod +x setup.sh start.sh

# Kurulumu başlatın
./setup.sh
```

### 4. Placeholder Görselleri Oluşturun

```bash
python3 create_images.py
```

### 5. Başlatın!

```bash
./start.sh
```

Tarayıcınızda açın: **http://localhost:8000**

## 🎨 Demo Mode Özellikleri

API key'ler olmadan çalışır:
- ✅ Sahte kullanıcı verileri
- ✅ Kişilik analizi
- ✅ Eşleştirme algoritması  
- ✅ Komedi şablonları
- ✅ Frame'ler
- ❌ Gerçek Farcaster verileri (mock data kullanır)
- ❌ AI-generated comedy (template comedy kullanır)

## 🔑 Production Mode (Gerçek API'ler ile)

### 1. API Key'leri Alın

**OpenAI API:**
1. https://platform.openai.com/ → Sign up
2. API Keys → Create new
3. Kopyalayın

**Neynar (Farcaster) API:**
1. https://neynar.com/ → Sign up
2. Developer Console → Create App
3. API Key'i kopyalayın

### 2. .env Dosyasını Düzenleyin

```bash
nano .env
```

Şunları ekleyin:
```env
OPENAI_API_KEY=sk-your-key-here
FARCASTER_API_KEY=your-neynar-key-here
```

### 3. PostgreSQL Kurulumu

```bash
# Yükleyin
sudo apt install postgresql postgresql-contrib

# Başlatın
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Database oluşturun
sudo -u postgres psql
```

PostgreSQL içinde:
```sql
CREATE DATABASE crypto_compatibility;
CREATE USER cryptouser WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE crypto_compatibility TO cryptouser;
\q
```

.env'de güncelleyin:
```env
DATABASE_URL=postgresql://cryptouser:your_password@localhost:5432/crypto_compatibility
```

### 4. app.py'de Mock Data'yı Kapatın

```python
# Satır 20-21 civarı
matchmaker = MatchmakerAI(use_mock_data=False)  # False yapın
```

### 5. Yeniden Başlatın

```bash
./start.sh
```

## 🐳 Docker ile Çalıştırma (En Kolay)

```bash
# Docker yüklü mü?
docker --version

# Yoksa:
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Çalıştırın
docker-compose up -d

# Loglara bakın
docker-compose logs -f app
```

Tarayıcıda: **http://localhost:8000**

## 📱 Test Etme

### API Test

```bash
# Health check
curl http://localhost:8000/api/health

# Kullanıcı analizi
curl http://localhost:8000/api/user/12345

# Kişilikleri listele
curl http://localhost:8000/api/personalities
```

### Python Test

```bash
python3 test.py
```

### Tarayıcı Test

1. http://localhost:8000 → Ana frame
2. http://localhost:8000/docs → API documentation
3. http://localhost:8000/api/personalities → JSON response

## 🚨 Sorun Giderme

### Port zaten kullanımda

```bash
# Farklı port kullan
APP_PORT=8001 python app.py
```

### Module not found hatası

```bash
# Virtual environment aktif mi?
source venv/bin/activate

# Tekrar yükle
pip install -r requirements.txt
```

### Database bağlanamıyor

Demo mode'da çalıştırın (database olmadan):
```python
# app.py'de database bağlantısı hata verirse otomatik devam eder
```

## 📚 Sonraki Adımlar

1. ✅ Demo'yu test edin
2. 🔑 API key'leri alın ve production mode'a geçin
3. 🎨 Görselleri özelleştirin (create_images.py)
4. 🎭 Komedi şablonlarını düzenleyin (comedy_templates/)
5. 👤 Yeni kişilik tipleri ekleyin (personality_profiles/)
6. 🌐 Deploy edin (Vercel, Railway, etc.)

## 🎉 Başarılı!

Artık kendi crypto dating frame'iniz çalışıyor!

- 💕 Matchmaking algoritması aktif
- 😂 Komedi motoru çalışıyor
- 🎨 Frame'ler hazır
- 📊 Analytics takip ediliyor

**Viral olma zamanı! 🚀**
