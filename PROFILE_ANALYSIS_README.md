# 🔬 Profil Analiz Motoru - Etik OSINT Araçları

## 📋 Proje Açıklaması

Bu proje, etik ve yasal sınırlar içinde profil analizi yapan bir "Profil Analiz Motoru" geliştirmektedir. Araç, dijital ayak izi farkındalığı, güvenlik araştırması ve gizlilik eğitimi amaçları için tasarlanmıştır.

## ✨ Özellikler

### 🔍 Ana Fonksiyonlar

1. **Sosyal Medya Profil Arama** (`search_social_media`)
   - Belirtilen isimle sosyal medya platformlarında arama
   - Platform-specific arama (Twitter, LinkedIn, Instagram, Facebook, GitHub, YouTube)
   - Profil detayları, fotoğraflar ve bio bilgileri

2. **Detaylı Profil Analizi** (`analyze_profile`)
   - Profil detaylarını çekme
   - Ters görsel arama
   - Diğer platformlardaki hesapları keşfetme
   - Halka açık e-posta tespiti
   - Halka açık fotoğrafları listeleme
   - Risk değerlendirmesi

3. **Alt Fonksiyonlar**
   - `fetch_profile_details`: Profil detaylarını çekme
   - `reverse_image_search`: Ters görsel arama (SerpAPI)
   - `discover_other_accounts`: 50+ platformda kullanıcı adı kontrolü
   - `find_public_email`: Bio'dan e-posta çıkarma
   - `list_public_photos`: Halka açık fotoğrafları listeleme

### 🔒 Güvenlik Özellikleri

1. **Veri Şifreleme**
   - AES şifreleme ile hassas verilerin korunması
   - PBKDF2 ile güçlü anahtar türetme
   - Güvenli salt kullanımı

2. **Veri Saklama Politikası**
   - 30 gün otomatik veri silme
   - KVKK uyumlu veri işleme
   - Onay yönetimi sistemi

3. **Audit Logging**
   - Tüm işlemlerin loglanması
   - Erişim kayıtları
   - Veri silme logları

4. **Rate Limiting**
   - API çağrı sınırlamaları
   - Platform dostu istek oranları
   - Robots.txt uyumu

## 🚀 Kurulum

### Gereksinimler

```bash
pip install -r backend/requirements.txt
```

### Çevre Değişkenleri

`backend/config.env` dosyasını oluşturun:

```env
SERPAPI_KEY=your-serpapi-key
HIBP_API_KEY=your-hibp-key
SYNTHETIC_MODE=false
OFFLINE_MODE=false
ENCRYPTION_PASSWORD=your-strong-encryption-password
```

### Çalıştırma

```bash
cd backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

## 📊 API Endpoints

### Profil Analiz Motoru

- `POST /api/profile-analysis/search-social-media` - Sosyal medya profil arama
- `POST /api/profile-analysis/analyze-profile` - Detaylı profil analizi
- `POST /api/profile-analysis/fetch-profile-details` - Profil detaylarını çekme
- `POST /api/profile-analysis/reverse-image-search` - Ters görsel arama
- `POST /api/profile-analysis/discover-other-accounts` - Kullanıcı adı kontrolü
- `POST /api/profile-analysis/find-public-email` - E-posta çıkarma
- `POST /api/profile-analysis/list-public-photos` - Fotoğraf listeleme
- `GET /api/profile-analysis/ethical-guidelines` - Etik kullanım kılavuzu
- `GET /api/profile-analysis/supported-platforms` - Desteklenen platformlar
- `GET /api/profile-analysis/health` - API sağlık kontrolü

## 🌐 Desteklenen Platformlar

### Sosyal Medya
- Twitter, LinkedIn, Instagram, Facebook, YouTube, GitHub
- Reddit, TikTok, Pinterest, Snapchat, Medium, Dev.to
- Behance, Dribbble, Steam, Discord, Telegram, Twitch

### Profesyonel Platformlar
- Vimeo, SoundCloud, Spotify, Last.fm, Flickr, 500px
- DeviantArt, ArtStation, CodePen, Stack Overflow, GitLab, Bitbucket
- Keybase, HackerNews, Product Hunt, AngelList, Crunchbase

### Akademik Platformlar
- SlideShare, Speaker Deck, Mixcloud, Goodreads, Letterboxd, IMDb
- ResearchGate, Academia, ORCID, Google Scholar, Mendeley, Kaggle

### Programlama Platformları
- HackerRank, LeetCode, Codeforces, AtCoder, TopCoder, CodeChef

## ⚠️ Etik Kullanım Kuralları

### ✅ İZİNLİ KULLANIM
- Kendi profillerinizi analiz etmek
- Açık onay verilen profilleri analiz etmek
- Güvenlik araştırması ve eğitim amaçlı kullanım
- Dijital ayak izi farkındalığı eğitimi

### ❌ YASAK KULLANIM
- Başkalarının profillerini izinsiz analiz etmek
- KVKK ihlali yapmak
- Stalking veya kötü niyetli amaçlarla kullanım
- Platform hizmet şartlarını ihlal etmek

### 🔒 Yasal Uyarı
Bu araç KVKK ve diğer gizlilik yasalarına uygun olarak kullanılmalıdır. Yasadışı kullanım yasaktır ve sorumluluk kullanıcıya aittir.

## 🛡️ Güvenlik Önlemleri

### Veri Koruma
- Tüm hassas veriler AES-256 ile şifrelenir
- 30 gün sonra otomatik veri silme
- Güvenli anahtar yönetimi
- Salt kullanımı

### Erişim Kontrolü
- Rate limiting ile API koruması
- Audit logging ile tüm işlemlerin kaydı
- Session token tabanlı kimlik doğrulama
- IP adresi takibi

### Veri Saklama
- Şifrelenmiş veri saklama
- Otomatik veri temizleme
- KVKK uyumlu veri işleme
- Onay yönetimi sistemi

## 🔧 Teknik Detaylar

### Backend Teknolojileri
- **FastAPI**: Modern Python web framework
- **BeautifulSoup**: Web scraping
- **SerpAPI**: Google arama API'si
- **Cryptography**: Veri şifreleme
- **SQLAlchemy**: Veritabanı ORM
- **APScheduler**: Zamanlanmış görevler

### Frontend Teknolojileri
- **HTML5/CSS3**: Modern web standartları
- **JavaScript (ES6+)**: Dinamik arayüz
- **Responsive Design**: Mobil uyumlu tasarım
- **Dark/Light Mode**: Tema desteği

### Veri Güvenliği
- **AES-256**: Simetrik şifreleme
- **PBKDF2**: Anahtar türetme
- **SHA-256**: Hash fonksiyonları
- **Fernet**: Güvenli token sistemi

## 📈 Performans Optimizasyonları

### Paralel İşleme
- ThreadPoolExecutor ile platform kontrolleri
- Asenkron API çağrıları
- Connection pooling
- Rate limiting

### Veri Yönetimi
- Otomatik veri temizleme
- Şifrelenmiş veri saklama
- Audit log rotasyonu
- Memory-efficient işleme

## 🧪 Test Senaryoları

### Sentetik Mod
```python
# config.env
SYNTHETIC_MODE=true
```

Sentetik mod ile gerçek API çağrıları yapmadan test edebilirsiniz.

### Offline Mod
```python
# config.env
OFFLINE_MODE=true
```

İnternet bağlantısı olmadan test edebilirsiniz.

## 📝 Geliştirici Notları

### Kod Yapısı
```
backend/app/
├── services/
│   ├── profile_analysis.py    # Ana profil analiz motoru
│   ├── encryption.py          # Veri şifreleme servisi
│   └── cleanup.py            # Veri temizleme servisi
├── routers/
│   └── profile_analysis.py   # API endpoint'leri
└── static/
    └── index.html           # Frontend arayüzü
```

### Hata Yönetimi
- Comprehensive exception handling
- User-friendly error messages
- Detailed logging
- Graceful degradation

### Genişletilebilirlik
- Plugin architecture
- Modular design
- Configuration-driven
- API-first approach

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit yapın (`git commit -m 'Add amazing feature'`)
4. Push yapın (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

## 📄 Lisans

Bu proje eğitim amaçlıdır ve ticari kullanım için lisans gerektirir.

## 📞 İletişim

Etik kullanım hakkında sorularınız için: info@example.com

---

**Geliştirici**: Siber Güvenlik Projesi  
**Versiyon**: 1.0.0  
**Son Güncelleme**: 2024  
**Etik Uyum**: KVKK, GDPR, CCPA
