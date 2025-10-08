# Sosyal Medya Profil Analiz Scripti
Write-Host "🔍 Sosyal Medya Profil Analiz Scripti" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green

# Python'un yüklü olup olmadığını kontrol et
try {
    $pythonVersion = python --version
    Write-Host "✅ Python bulundu: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python bulunamadı! Lütfen Python yükleyin." -ForegroundColor Red
    Read-Host "Devam etmek için Enter'a basın"
    exit 1
}

# .env dosyasının varlığını kontrol et
if (-not (Test-Path ".env")) {
    Write-Host "⚠️ .env dosyası bulunamadı!" -ForegroundColor Yellow
    Write-Host "📝 env_example.txt dosyasını .env olarak kopyalayın" -ForegroundColor Cyan
    Write-Host "🔑 Gerçek API anahtarlarınızı .env dosyasına ekleyin" -ForegroundColor Cyan
    Read-Host "Devam etmek için Enter'a basın"
    exit 1
}

# Gereksinimleri yükle
Write-Host "📦 Gereksinimler yükleniyor..." -ForegroundColor Yellow
try {
    pip install -r profile_analyzer_requirements.txt
    Write-Host "✅ Gereksinimler başarıyla yüklendi" -ForegroundColor Green
} catch {
    Write-Host "❌ Gereksinim yükleme başarısız!" -ForegroundColor Red
    Read-Host "Devam etmek için Enter'a basın"
    exit 1
}

# Script'i çalıştır
Write-Host "🚀 Profil analiz scripti başlatılıyor..." -ForegroundColor Yellow
Write-Host ""
try {
    python profile_analyzer.py
} catch {
    Write-Host "❌ Script çalıştırma hatası!" -ForegroundColor Red
}

Write-Host ""
Read-Host "Çıkmak için Enter'a basın"
