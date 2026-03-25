# 🔐 Dijital Ayak İzi Farkındalık Uygulaması (Digital Footprint Awareness)

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)
![React](https://img.shields.io/badge/react-18-61dafb.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100.0%2B-009688.svg)

Bu proje, kullanıcıların dijital ayak izlerini etik ve yasal sınırlar içinde analiz ederek kişisel gizlilik farkındalığını artırmayı amaçlayan profesyonel bir OSINT (Open-Source Intelligence) ve veri agregasyon platformudur.

---

## ✨ Özellikler

### 🔍 Analiz Motoru
- **Sosyal Medya Taraması**: Instagram, Twitter/X, LinkedIn, Facebook, GitHub, YouTube ve 50+ diğer platformda kapsamlı profil araması.
- **Ters Görsel Arama**: Profil fotoğraflarını kullanarak internet üzerindeki diğer izlerin takibi.
- **Veri İhlali Kontrolü**: `HaveIBeenPwned` API entegrasyonu ile e-posta sızıntısı kontrolü.
- **Kullanıcı Adı Keşfi**: Tek bir kullanıcı adı ile tüm popüler platformlarda hesap varlığı kontrolü.
- **İletişim Bilgisi Analizi**: Bio metinlerinden halka açık e-posta ve iletişim bilgilerinin otomatik tespiti.

### 🎨 Kullanıcı Deneyimi (UI/UX)
- **Modern Dashboard**: Analiz sonuçlarını görselleştiren, cam efekti (glassmorphism) tasarımlı panel.
- **Dinamik Temalar**: Göz yormayan Dark Mode ve standart Light Mode desteği.
- **Akıcı Animasyonlar**: Framer Motion ile profesyonel geçişler ve mikro-etkileşimler.
- **Responsive Tasarım**: Tüm mobil ve masaüstü cihazlarla tam uyumluluk.

### 🛡️ Güvenlik ve Gizlilik
- **Veri Şifreleme**: Hassas veriler AES-256 ve PBKDF2 ile yerel olarak korunur.
- **Otomatik Temizleme**: Kullanıcı verileri 30 gün sonra sistemden otomatik olarak silinir.
- **Etik Uyarılar**: KVKK, GDPR ve CCPA ile tam uyumlu, etik kullanım bildirimleri.

---

## 🛠️ Teknoloji Yığını

| Bileşen | Teknolojiler |
| :--- | :--- |
| **Backend** | Python, FastAPI, SQLAlchemy, BeautifulSoup, uvicorn |
| **Frontend** | React 18, Vite, Tailwind CSS, Framer Motion, Lucide React |
| **Veritabanı** | SQLite (Hızlı ve taşınabilir) |
| **API'ler** | Google Custom Search, SerpAPI, ScraperAPI, HaveIBeenPwned |
| **Güvenlik** | AES-256 Encryption, PBKDF2 Key Derivation |

---

## 🚀 Kurulum

### 1. Depoyu Klonlayın
```bash
git clone https://github.com/omercangumus/dijital-ayak-izi.git
cd dijital-ayak-izi
```

### 2. Backend Kurulumu
```bash
# Bağımlılıkları yükleyin
pip install -r requirements.txt

# Çevre değişkenlerini yapılandırın (Aşağıdaki API bölümüne bakın)
# backend/config.env dosyasını oluşturun

# Sunucuyu başlatın
cd backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

### 3. Frontend Kurulumu
```bash
cd frontend
npm install
npm run dev
```

---

## 🔑 API Anahtarları ve Güvenlik

Projenin tam kapasite çalışması için aşağıdaki anahtarlar gereklidir. Bu anahtarları **asla** GitHub'a push etmeyin!

`.env` veya `backend/config.env` dosya yapısı:
```env
GOOGLE_API_KEY="AIza..."
GOOGLE_SEARCH_ENGINE_ID="51f9..."
SCRAPER_API_KEY="your_key"
SERPAPI_KEY="your_key"
HIBP_API_KEY="your_key"
ENCRYPTION_PASSWORD="guclu-bir-sifre"
```

> [!IMPORTANT]
> API anahtarlarınızı `config.env` gibi dosyalarda saklayın. Bu dosyalar `.gitignore` içerisinde olduğu için güvenli kalacaktır.

---

## 📊 Kullanım

1. **Arama**: Ana sayfada ad-soyad ve hedef platformları seçerek analizi başlatın.
2. **Doğrulama**: Bulunan profiller arasından kendinize ait olanı seçerek detaya gidin.
3. **Rapor**: Dashboard üzerinden risk skorunuzu, sızdırılmış verilerinizi ve görsel ayak izinizi inceleyin.

---

## ⚖️ Etik ve Yasal Uyarılar

- **Yasal Uyarı**: Bu araç sadece yasal ve etik amaçlar (güvenlik araştırması, kişisel farkındalık) için kullanılmalıdır.
- **İzin**: Başkalarının verilerini izinsiz taramak KVKK ve ilgili yasalarca suç teşkil edebilir.
- **Doğruluk**: Sonuçlar halka açık verilere dayanır ve %100 doğruluk garantisi vermez.

---

## 🤝 Katkıda Bulunma

1. Projeyi Fork edin.
2. Feature branch oluşturun (`git checkout -b feature/yenilik`).
3. Değişikliklerinizi commit edin (`git commit -m 'Yeni özellik eklendi'`).
4. Branch'inizi push edin (`git push origin feature/yenilik`).
5. Pull Request açın.

---

**Geliştirici**: Siber Güvenlik Projesi & Ömer Can Gümüş
**Versiyon**: 1.0.0
**Lisans**: MIT
