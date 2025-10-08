# 🚀 Dijital Ayak İzi Analiz Paneli - React Frontend

Modern, kullanıcı dostu React + Tailwind CSS frontend uygulaması.

## ✨ Özellikler

### 🎨 Modern UI/UX
- **Dark Theme**: Göz yormayan koyu tema
- **Responsive Design**: Mobil ve masaüstü uyumlu
- **Smooth Animations**: Framer Motion ile akıcı animasyonlar
- **Beautiful Typography**: Inter font ailesi
- **Glassmorphism**: Modern cam efekti tasarım

### 🔧 Teknik Özellikler
- **React 18**: En son React sürümü
- **Vite**: Hızlı geliştirme ortamı
- **Tailwind CSS**: Utility-first CSS framework
- **Framer Motion**: Profesyonel animasyonlar
- **Lucide React**: Modern ikonlar
- **Axios**: HTTP istekleri
- **React Router**: Sayfa yönlendirme

### 📱 Bileşenler

#### Ana Sayfalar
- **HomePage**: Arama formu ve etik uyarılar
- **ReportPage**: Analiz sonuçları dashboard'u

#### Form Bileşenleri
- **SearchForm**: Gelişmiş arama formu
- **ProfileSelectionModal**: Profil seçim modal'ı
- **WarningBox**: Etik kullanım uyarıları

#### Dashboard Widget'ları
- **SummaryCard**: Profil özeti ve gizlilik skoru
- **RiskAssessment**: Risk değerlendirmesi
- **VisualFootprint**: Görsel ayak izi galerisi
- **AccountDiscovery**: Platform keşfi
- **ContactInfo**: İletişim bilgileri analizi
- **PublicMedia**: Halka açık fotoğraf galerisi

## 🚀 Kurulum ve Çalıştırma

### Ön Gereksinimler
- Node.js (v16 veya üzeri)
- npm veya yarn
- Python backend çalışıyor olmalı

### 1. Bağımlılıkları Yükle
```bash
cd frontend
npm install
```

### 2. Development Server
```bash
# PowerShell
.\dev.ps1

# veya manuel
npm run dev
```

Frontend: http://localhost:3000
Backend API: http://localhost:8000

### 3. Production Build
```bash
# PowerShell
.\build.ps1

# veya manuel
npm run build
```

Build dosyaları: `../backend/app/static/dist/`

### 4. Backend ile Çalıştırma
```bash
# Backend'i başlat
python -m uvicorn backend.app.main:app --reload

# Frontend http://localhost:8000 adresinde otomatik olarak serve edilir
```

## 🎯 Kullanım

### 1. Profil Arama
1. Ana sayfada ad ve soyad girin
2. İsteğe bağlı platform seçin
3. "Analizi Başlat" butonuna tıklayın

### 2. Profil Seçimi
1. Bulunan profiller arasından kendi profilinizi seçin
2. Profil kartına tıklayarak analizi başlatın

### 3. Analiz Raporu
1. Dashboard'da tüm analiz sonuçlarını görüntüleyin
2. Risk değerlendirmesi ve önerileri inceleyin
3. Görsel ayak izi ve hesap keşfi sonuçlarını kontrol edin

## 🎨 Tasarım Sistemi

### Renk Paleti
- **Background**: `slate-900`
- **Cards**: `slate-800`
- **Primary**: `blue-500`
- **Success**: `green-400`
- **Warning**: `yellow-400`
- **Error**: `red-400`

### Typography
- **Font**: Inter (Google Fonts)
- **Headings**: `font-bold`
- **Body**: `font-medium`
- **Captions**: `font-normal`

### Animations
- **Page Transitions**: `fadeIn`, `slideUp`
- **Hover Effects**: `scale`, `brightness`
- **Loading States**: `spinner`, `skeleton`
- **Staggered Children**: Dashboard widget'ları

## 🔧 Geliştirme

### Proje Yapısı
```
frontend/
├── src/
│   ├── components/          # UI bileşenleri
│   ├── pages/              # Sayfa bileşenleri
│   ├── context/            # React Context
│   ├── services/           # API servisleri
│   ├── App.jsx             # Ana uygulama
│   └── main.jsx            # Entry point
├── public/                 # Static dosyalar
├── package.json            # Bağımlılıklar
├── vite.config.js          # Vite yapılandırması
├── tailwind.config.js      # Tailwind yapılandırması
└── index.html              # HTML template
```

### API Entegrasyonu
- **Base URL**: `/api`
- **Timeout**: 30 saniye
- **Error Handling**: Merkezi hata yönetimi
- **Loading States**: Tüm API çağrıları için

### State Management
- **React Context**: Global state yönetimi
- **Local State**: Component bazlı state
- **Props Drilling**: Minimal prop geçişi

## 📱 Responsive Design

### Breakpoints
- **Mobile**: `< 768px`
- **Tablet**: `768px - 1024px`
- **Desktop**: `> 1024px`

### Mobile Optimizations
- Touch-friendly buttons
- Optimized image sizes
- Collapsible navigation
- Swipe gestures

## 🔒 Güvenlik

### Etik Kullanım
- Prominent ethical warnings
- Legal compliance notices
- Data handling transparency
- User consent management

### Data Protection
- No sensitive data storage
- Secure API communication
- Input validation
- XSS protection

## 🚀 Deployment

### Production Build
```bash
npm run build
```

### Static Hosting
Build dosyaları herhangi bir static hosting servisinde çalışabilir:
- Vercel
- Netlify
- GitHub Pages
- AWS S3

### Backend Integration
React build dosyaları backend'de serve edilir:
- FastAPI static file serving
- SPA routing support
- API proxy configuration

## 🐛 Troubleshooting

### Common Issues

#### 1. Build Failures
```bash
# Clear cache
rm -rf node_modules package-lock.json
npm install
npm run build
```

#### 2. API Connection Issues
- Backend'in çalıştığından emin olun
- CORS ayarlarını kontrol edin
- Proxy yapılandırmasını kontrol edin

#### 3. Styling Issues
- Tailwind CSS build'ini kontrol edin
- CSS import'larını kontrol edin
- Browser cache'ini temizleyin

### Development Tips
- Hot reload için `npm run dev` kullanın
- Browser DevTools'u aktif tutun
- Network tab'ını izleyin
- Console error'larını kontrol edin

## 📚 Kaynaklar

- [React Documentation](https://react.dev/)
- [Vite Documentation](https://vitejs.dev/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Framer Motion](https://www.framer.com/motion/)
- [Lucide Icons](https://lucide.dev/)

## 🤝 Katkıda Bulunma

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.
