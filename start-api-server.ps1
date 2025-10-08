# Sosyal Medya Profil Analiz API Server Başlatma Scripti
# PowerShell Script

Write-Host "🚀 Sosyal Medya Profil Analiz API Server" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green

# .env dosyasının varlığını kontrol et
if (-not (Test-Path ".env")) {
    Write-Host "❌ .env dosyası bulunamadı!" -ForegroundColor Red
    Write-Host "📝 env.example dosyasını .env olarak kopyalayın ve API anahtarlarınızı girin" -ForegroundColor Yellow
    Write-Host "   cp env.example .env" -ForegroundColor Cyan
    exit 1
}

# Docker'ın çalışıp çalışmadığını kontrol et
try {
    docker --version | Out-Null
    Write-Host "✅ Docker bulundu" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker bulunamadı! Lütfen Docker'ı yükleyin" -ForegroundColor Red
    exit 1
}

# Container'ı durdur (eğer çalışıyorsa)
Write-Host "🛑 Mevcut container'ı durduruyor..." -ForegroundColor Yellow
docker stop analyzer-api 2>$null
docker rm analyzer-api 2>$null

# Image'ı build et
Write-Host "🔨 Docker image'ı build ediliyor..." -ForegroundColor Yellow
docker build -t analyzer-api .

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Docker build başarısız!" -ForegroundColor Red
    exit 1
}

# Container'ı başlat
Write-Host "🚀 API server başlatılıyor..." -ForegroundColor Green
docker run -d -p 5001:8000 --name analyzer-api --env-file .env analyzer-api

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Container başlatılamadı!" -ForegroundColor Red
    exit 1
}

# Container'ın başlamasını bekle
Write-Host "⏳ Container'ın başlamasını bekliyor..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Health check
Write-Host "🏥 Health check yapılıyor..." -ForegroundColor Cyan
try {
    $response = Invoke-RestMethod -Uri "http://localhost:5001/health" -Method Get -TimeoutSec 10
    if ($response.status -eq "healthy") {
        Write-Host "✅ API server başarıyla başlatıldı!" -ForegroundColor Green
        Write-Host ""
        Write-Host "🌐 API Endpoints:" -ForegroundColor Cyan
        Write-Host "   Ana Sayfa: http://localhost:5001/" -ForegroundColor White
        Write-Host "   API Docs:  http://localhost:5001/docs" -ForegroundColor White
        Write-Host "   Health:    http://localhost:5001/health" -ForegroundColor White
        Write-Host "   Analyze:   POST http://localhost:5001/analyze" -ForegroundColor White
        Write-Host ""
        Write-Host "📝 Test komutu:" -ForegroundColor Cyan
        Write-Host '   curl -X POST "http://localhost:5001/analyze" -H "Content-Type: application/json" -d ''{"profile_url": "https://www.instagram.com/nasa/"}''' -ForegroundColor White
        Write-Host ""
        Write-Host "🛑 Durdurmak için: docker stop analyzer-api" -ForegroundColor Yellow
    } else {
        Write-Host "❌ API server sağlıksız durumda!" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ Health check başarısız! Server henüz hazır değil olabilir." -ForegroundColor Red
    Write-Host "📋 Container loglarını kontrol edin: docker logs analyzer-api" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "📊 Container durumu:" -ForegroundColor Cyan
docker ps --filter name=analyzer-api
