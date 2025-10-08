# 🔍 Sosyal Medya Profil Analiz Scripti

Bu Python scripti, sosyal medya profillerini analiz eder ve ters görsel arama yapar. Scraper API ve Google Custom Search API kullanarak güvenli bir şekilde veri toplar.

## ✨ Özellikler

- **Profil Scraping**: Scraper API ile sosyal medya profil verilerini çeker
- **Ters Görsel Arama**: Google Custom Search API ile profil resmi arama
- **Platform Desteği**: Instagram, Twitter, LinkedIn, Facebook ve diğerleri
- **Güvenli API Yönetimi**: Tüm API anahtarları .env dosyasından yüklenir
- **Detaylı Logging**: Tüm işlemler loglanır
- **JSON Çıktı**: Sonuçlar JSON formatında döndürülür

## 🚀 Kurulum

### 1. Gereksinimleri Yükle
```bash
pip install -r profile_analyzer_requirements.txt
```

### 2. API Anahtarlarını Yapılandır
```bash
# .env dosyası oluştur
cp env_example.txt .env

# .env dosyasını düzenle ve gerçek API anahtarlarınızı girin
```

### 3. Google Custom Search Engine Kurulumu
1. [Google Cloud Console](https://console.cloud.google.com/)'a gidin
2. Yeni proje oluşturun veya mevcut projeyi seçin
3. Custom Search API'yi etkinleştirin
4. API anahtarı oluşturun
5. [Custom Search Engine](https://cse.google.com/) oluşturun
6. Search Engine ID'yi alın

### 4. Scraper API Kurulumu
1. [ScraperAPI](https://www.scraperapi.com/) hesabı oluşturun
2. API anahtarınızı alın
3. .env dosyasına ekleyin

## 📝 .env Dosyası Yapısı

```env
GOOGLE_API_KEY="your_google_api_key_here"
GOOGLE_SEARCH_ENGINE_ID="your_search_engine_id_here"
SCRAPER_API_KEY="your_scraper_api_key_here"
```

## 🎯 Kullanım

### Komut Satırından
```bash
python profile_analyzer.py
```

### Python Kodundan
```python
from profile_analyzer import ProfileAnalyzer

# Analizörü başlat
analyzer = ProfileAnalyzer()

# Profil analizi yap
result = analyzer.analyze_profile("https://instagram.com/username")

# Sonuçları yazdır
print(result)
```

## 📊 Çıktı Formatı

```json
{
  "profile_analysis": {
    "url": "https://instagram.com/username",
    "platform": "instagram",
    "username": "username",
    "full_name": "Full Name",
    "bio": "Bio text here...",
    "profile_picture": "https://example.com/image.jpg",
    "verification_status": false,
    "followers_count": 1000,
    "following_count": 500,
    "posts_count": 100
  },
  "reverse_image_search": {
    "image_url": "https://example.com/image.jpg",
    "total_results": "50",
    "search_time": "0.123456",
    "results": [
      {
        "title": "Result Title",
        "link": "https://example.com/result",
        "snippet": "Result description...",
        "image_url": "https://example.com/result-image.jpg",
        "source": "example.com",
        "context_link": "https://example.com/context"
      }
    ]
  },
  "analysis_timestamp": 1703123456,
  "analysis_status": "completed"
}
```

## 🔧 Desteklenen Platformlar

### Tam Destek
- **Instagram**: Profil resmi, bio, takipçi sayısı
- **Twitter/X**: Profil resmi, bio, tweet sayısı
- **LinkedIn**: Profil resmi, bio, bağlantı sayısı
- **Facebook**: Profil resmi, bio, arkadaş sayısı

### Temel Destek
- **YouTube**: Kanal bilgileri
- **TikTok**: Profil bilgileri
- **Diğer Platformlar**: Genel meta tag'ler

## 🛡️ Güvenlik

### API Anahtarı Güvenliği
- ✅ API anahtarları .env dosyasında saklanır
- ✅ .env dosyası .gitignore'a eklenir
- ✅ Hardcoded anahtarlar yoktur
- ✅ Hata mesajlarında anahtarlar görünmez

### Veri Güvenliği
- ✅ Sadece halka açık veriler çekilir
- ✅ Kişisel veriler saklanmaz
- ✅ Rate limiting uygulanır
- ✅ Timeout koruması vardır

## 📝 Logging

Script detaylı logging yapar:
- INFO: Normal işlemler
- WARNING: Uyarılar
- ERROR: Hatalar

Log formatı:
```
2024-01-01 12:00:00 - INFO - ProfileAnalyzer başarıyla başlatıldı
2024-01-01 12:00:01 - INFO - Profil scraping başlatıldı: https://instagram.com/username
2024-01-01 12:00:02 - INFO - Profil scraping başarıyla tamamlandı
```

## 🐛 Hata Yönetimi

### Yaygın Hatalar

#### 1. API Anahtarı Hatası
```
ValueError: Eksik API anahtarları: GOOGLE_API_KEY
```
**Çözüm**: .env dosyasını kontrol edin

#### 2. Scraping Hatası
```
Exception: Profil scraping başarısız: 403 Forbidden
```
**Çözüm**: Scraper API anahtarını kontrol edin

#### 3. Google API Hatası
```
Exception: Ters görsel arama başarısız: 403 Forbidden
```
**Çözüm**: Google API anahtarını ve Search Engine ID'yi kontrol edin

## 🔄 Rate Limiting

- Scraper API: Dakikada 1000 istek
- Google Custom Search: Günde 100 istek (ücretsiz)
- Script otomatik olarak rate limit kontrolü yapar

## 📚 API Dokümantasyonu

### Scraper API
- [Dokümantasyon](https://www.scraperapi.com/documentation/)
- [Pricing](https://www.scraperapi.com/pricing/)

### Google Custom Search API
- [Dokümantasyon](https://developers.google.com/custom-search/v1/introduction)
- [Quota](https://developers.google.com/custom-search/v1/cse/list)

## 🤝 Katkıda Bulunma

1. Fork the repository
2. Feature branch oluştur
3. Değişiklikleri yap
4. Test et
5. Pull request gönder

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## ⚠️ Yasal Uyarı

Bu script sadece eğitim ve araştırma amaçlıdır. Kullanımından doğacak yasal sorumluluk kullanıcıya aittir. KVKK ve diğer gizlilik yasalarına uygun kullanın.

## 🆘 Destek

Sorunlar için:
1. Log dosyalarını kontrol edin
2. API anahtarlarını doğrulayın
3. Internet bağlantınızı kontrol edin
4. GitHub Issues'da sorun bildirin
