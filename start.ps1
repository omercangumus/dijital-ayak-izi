# Dijital Ayak Izi - Baslatma Script
# Kullanim: powershell -ExecutionPolicy Bypass .\start.ps1

Write-Host "🚀 Dijital Ayak Izi Uygulamasi Baslatiliyor..." -ForegroundColor Cyan

# Proje dizinine git
Set-Location "D:\SiberGuvenlıkProje"

# Sanal ortami aktif et
Write-Host "📦 Sanal ortam aktif ediliyor..." -ForegroundColor Yellow
. .\.venv\Scripts\Activate.ps1

# API anahtarlarini ayarla
Write-Host "🔑 API anahtarlari yukleniyor..." -ForegroundColor Yellow
$env:SERPAPI_KEY="e210298031773661ca5c3274e2436a3ffcb4c1964ebe3908d8ce33b29f3b3448"
$env:SYNTHETIC_MODE="false"
$env:OFFLINE_MODE="false"
$env:SECRET_KEY="dijital-ayak-izi-secret-2024"

# Backend'e git ve baslat
Write-Host "🌐 Backend sunucu baslatiliyor..." -ForegroundColor Green
Write-Host "📍 URL: http://localhost:8000" -ForegroundColor Cyan
Write-Host "📖 Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "" 
Write-Host "⚡ GERÇEK API MODU AKTİF - SerpAPI ile Google araması yapilacak!" -ForegroundColor Magenta
Write-Host ""

Set-Location backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

