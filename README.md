# 🔐 Dijital Ayak İzi Farkındalık Uygulaması

## 📋 Proje Açıklaması

Bu uygulama, kullanıcıların dijital ayak izlerini analiz ederek gizlilik farkındalığını artırmayı amaçlayan bir web uygulamasıdır.

## ✨ Özellikler

- **Sosyal Medya Tarama**: Twitter, LinkedIn, Instagram, Facebook, YouTube, GitHub vb. platformlarda profil arama
- **Web Arama**: Google'da genel arama sonuçları
- **Görsel Analiz**: Profil fotoğrafları ve diğer görseller
- **Veri İhlali Kontrolü**: HaveIBeenPwned API ile e-posta kontrolü
- **WebArchive Entegrasyonu**: Geçmiş web sayfaları
- **Dark/Light Mode**: Kullanıcı dostu arayüz
- **Risk Skorlaması**: Dijital ayak izi risk seviyesi

## 🚀 Teknolojiler

- **Backend**: FastAPI, Python
- **Frontend**: HTML, CSS, JavaScript
- **Veritabanı**: SQLite
- **API'ler**: SerpAPI, HaveIBeenPwned, WebArchive
- **Görsel İşleme**: Pillow, ImageHash, ExifRead

## 📦 Kurulum

1. **Gereksinimler**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Çevre Değişkenleri**:
   `backend/config.env` dosyasını oluşturun:
   ```
   SERPAPI_KEY=your-serpapi-key
   HIBP_API_KEY=your-hibp-key
   SYNTHETIC_MODE=false
   OFFLINE_MODE=false
   ```

3. **Çalıştırma**:
   ```bash
   cd backend
   python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
   ```

4. **Tarayıcıda Aç**:
   http://127.0.0.1:8000

## 🔧 API Endpoints

- `GET /` - Ana sayfa
- `POST /api/self-scan/detailed-scan` - Detaylı tarama
- `GET /health` - Sistem durumu

## 📊 Kullanım

1. Ana sayfada "İz Tarama" sekmesini seçin
2. Adınızı ve e-posta adresinizi girin
3. "Tarama Başlat" butonuna tıklayın
4. Sonuçları inceleyin ve risk skorunuzu görün

## 🔒 Gizlilik

- Tüm veriler 30 gün sonra otomatik silinir
- API anahtarları güvenli şekilde saklanır
- Kullanıcı onayı olmadan üçüncü taraf tarama yapılmaz

## 👥 Katkıda Bulunma

Bu proje eğitim amaçlı geliştirilmiştir. Katkılarınızı bekliyoruz!

## 📝 Lisans

Bu proje eğitim amaçlıdır ve ticari kullanım için lisans gerektirir.

---

**Geliştirici**: Siber Güvenlik Projesi  
**Versiyon**: 1.0.0  
**Son Güncelleme**: 2024