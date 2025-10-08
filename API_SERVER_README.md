# Sosyal Medya Profil Analiz API Server

Bu proje, sosyal medya profillerini analiz eden sürekli çalışan bir FastAPI web server'ıdır. Docker container olarak çalışır ve RESTful API endpoint'leri sunar.

## 🚀 Özellikler

- **FastAPI Web Server**: Modern, hızlı Python web framework
- **Docker Containerization**: Kolay deployment ve environment management
- **Sosyal Medya Analizi**: Instagram, Twitter, LinkedIn, Facebook desteği
- **Ters Görsel Arama**: Google Custom Search API entegrasyonu
- **Scraper API**: JavaScript render desteği ile profil verisi çekme
- **RESTful API**: JSON request/response formatı
- **Auto Documentation**: FastAPI'nin otomatik API dokümantasyonu
- **Health Check**: Server durumu kontrol endpoint'i

## 📋 Gereksinimler

### API Anahtarları
1. **Google Custom Search API Key**
   - [Google Cloud Console](https://console.cloud.google.com/) üzerinden alın
   - Custom Search Engine oluşturun
   - API Key ve Search Engine ID'yi not edin

2. **Scraper API Key**
   - [ScraperAPI](https://www.scraperapi.com/) üzerinden kayıt olun
   - API key'inizi alın

### Sistem Gereksinimleri
- Docker
- Docker Compose (opsiyonel)

## 🛠️ Kurulum

### 1. Proje Dosyalarını Hazırlayın
```bash
# Proje dizinine gidin
cd your-project-directory

# Gerekli dosyalar:
# - main.py
# - Dockerfile
# - requirements.txt
# - env.example
```

### 2. Environment Variables Ayarlayın
```bash
# env.example dosyasını .env olarak kopyalayın
cp env.example .env

# .env dosyasını düzenleyin ve API anahtarlarınızı girin
nano .env
```

`.env` dosyası içeriği:
```env
GOOGLE_API_KEY=your_actual_google_api_key
GOOGLE_SEARCH_ENGINE_ID=your_actual_search_engine_id
SCRAPER_API_KEY=your_actual_scraper_api_key
```

### 3. Docker Container'ı Build Edin
```bash
# Docker image'ı build edin
docker build -t analyzer-api .
```

### 4. Container'ı Çalıştırın
```bash
# Detached mode'da çalıştırın (arka planda)
docker run -d -p 5001:8000 --env-file .env analyzer-api
```

**Parametre Açıklamaları:**
- `-d`: Detached mode (arka planda çalışır)
- `-p 5001:8000`: Port mapping (localhost:5001 → container:8000)
- `--env-file .env`: Environment variables dosyası

## 🧪 API'yi Test Etme

### Yöntem 1: cURL ile Test
```bash
# Temel test
curl -X POST "http://localhost:5001/analyze" \
  -H "Content-Type: application/json" \
  -d '{"profile_url": "https://www.instagram.com/nasa/"}'
```

**Beklenen Yanıt:**
```json
{
  "success": true,
  "data": {
    "profile_analysis": {
      "url": "https://www.instagram.com/nasa/",
      "platform": "instagram",
      "full_name": "NASA",
      "bio": "Explore the universe and discover our home planet...",
      "profile_picture": "https://...",
      "verification_status": true
    },
    "reverse_image_search": {
      "total_results": "10",
      "results": [...]
    },
    "analysis_timestamp": 1699123456,
    "analysis_status": "completed"
  },
  "error": null,
  "timestamp": 1699123456,
  "processing_time": 3.45
}
```

### Yöntem 2: FastAPI Auto Documentation
1. Web tarayıcınızı açın
2. `http://localhost:5001/docs` adresine gidin
3. Swagger UI'da `/analyze` endpoint'ini bulun
4. "Try it out" butonuna tıklayın
5. Request body'ye profil URL'i girin:
   ```json
   {
     "profile_url": "https://www.instagram.com/nasa/"
   }
   ```
6. "Execute" butonuna tıklayın

### Yöntem 3: Health Check
```bash
# Server durumunu kontrol edin
curl http://localhost:5001/health
```

## 📚 API Endpoints

### `GET /`
Ana sayfa bilgileri
```json
{
  "message": "Sosyal Medya Profil Analiz API",
  "version": "1.0.0",
  "docs": "/docs",
  "endpoint": "/analyze"
}
```

### `GET /health`
Sağlık kontrolü
```json
{
  "status": "healthy",
  "timestamp": 1699123456,
  "analyzer_ready": true
}
```

### `POST /analyze`
Profil analizi (ana endpoint)

**Request Body:**
```json
{
  "profile_url": "https://www.instagram.com/nasa/"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "profile_analysis": {
      "url": "string",
      "platform": "instagram|twitter|linkedin|facebook|unknown",
      "username": "string",
      "full_name": "string",
      "bio": "string",
      "profile_picture": "string",
      "verification_status": boolean,
      "followers_count": "string",
      "following_count": "string",
      "posts_count": "string"
    },
    "reverse_image_search": {
      "image_url": "string",
      "total_results": "string",
      "search_time": "string",
      "results": [
        {
          "title": "string",
          "link": "string",
          "snippet": "string",
          "image_url": "string",
          "source": "string",
          "context_link": "string"
        }
      ]
    },
    "analysis_timestamp": 1699123456,
    "analysis_status": "completed|failed"
  },
  "error": null,
  "timestamp": 1699123456,
  "processing_time": 3.45
}
```

## 🔧 Geliştirme

### Local Development
```bash
# Python virtual environment oluşturun
python -m venv venv
source venv/bin/activate  # Linux/Mac
# veya
venv\Scripts\activate     # Windows

# Bağımlılıkları yükleyin
pip install -r requirements.txt

# Development server'ı başlatın
python main.py
```

### Docker Compose (Opsiyonel)
```yaml
# docker-compose.yml
version: '3.8'
services:
  analyzer-api:
    build: .
    ports:
      - "5001:8000"
    env_file:
      - .env
    restart: unless-stopped
```

```bash
# Docker Compose ile çalıştırın
docker-compose up -d
```

## 🐛 Troubleshooting

### Container Başlamıyor
```bash
# Container loglarını kontrol edin
docker logs <container_id>

# Çalışan container'ları listeleyin
docker ps -a
```

### API Anahtarı Hataları
- `.env` dosyasının doğru konumda olduğundan emin olun
- API anahtarlarının doğru olduğunu kontrol edin
- Google Custom Search Engine'in aktif olduğundan emin olun

### Port Çakışması
```bash
# Farklı port kullanın
docker run -d -p 8080:8000 --env-file .env analyzer-api
```

### Memory/CPU Sorunları
```bash
# Resource limitleri belirleyin
docker run -d -p 5001:8000 --env-file .env \
  --memory="1g" --cpus="1.0" analyzer-api
```

## 📊 Monitoring

### Container Durumu
```bash
# Container stats
docker stats <container_id>

# Container logs
docker logs -f <container_id>
```

### API Metrics
- Processing time: Her request'in işlem süresi
- Success rate: Başarılı/başarısız request oranı
- Error logs: Detaylı hata mesajları

## 🔒 Güvenlik

- API anahtarlarını `.env` dosyasında saklayın
- `.env` dosyasını git'e commit etmeyin
- Production'da CORS ayarlarını sınırlayın
- Rate limiting ekleyin (opsiyonel)

## 📝 Notlar

- İlk request biraz yavaş olabilir (cold start)
- Scraper API'nin rate limit'leri vardır
- Google Custom Search API'nin günlük limit'i vardır
- Profil verileri sadece halka açık bilgilerden çekilir

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun
3. Değişikliklerinizi commit edin
4. Pull request gönderin

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.
