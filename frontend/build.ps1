# React Frontend Build Script
Write-Host "🚀 React Frontend Build Scripti Başlatılıyor..." -ForegroundColor Green

# Check if Node.js is installed
try {
    $nodeVersion = node --version
    Write-Host "✅ Node.js bulundu: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js bulunamadı! Lütfen Node.js yükleyin." -ForegroundColor Red
    exit 1
}

# Check if npm is installed
try {
    $npmVersion = npm --version
    Write-Host "✅ npm bulundu: $npmVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ npm bulunamadı! Lütfen npm yükleyin." -ForegroundColor Red
    exit 1
}

# Install dependencies
Write-Host "📦 Bağımlılıklar yükleniyor..." -ForegroundColor Yellow
npm install
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Bağımlılık yükleme başarısız!" -ForegroundColor Red
    exit 1
}

# Build the project
Write-Host "🔨 React uygulaması build ediliyor..." -ForegroundColor Yellow
npm run build
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Build başarısız!" -ForegroundColor Red
    exit 1
}

Write-Host "✅ React frontend başarıyla build edildi!" -ForegroundColor Green
Write-Host "📁 Build dosyaları: ../backend/app/static/dist/" -ForegroundColor Cyan
Write-Host "🌐 Sunucuyu başlatmak için: python -m uvicorn backend.app.main:app --reload" -ForegroundColor Cyan
