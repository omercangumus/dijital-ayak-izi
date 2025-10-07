# Dijital Ayak Izi - DEBUG Mod ile Baslat
Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "  Dijital Ayak Izi - DEBUG MOD" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Dizine git
Set-Location "D:\SiberGuvenlıkProje"

# Sanal ortam
Write-Host "[1/4] Sanal ortam aktif ediliyor..." -ForegroundColor Yellow
. .\.venv\Scripts\Activate.ps1

# API Anahtarlari
Write-Host "[2/4] API anahtarlari yukleniyor..." -ForegroundColor Yellow
$env:SERPAPI_KEY="e210298031773661ca5c3274e2436a3ffcb4c1964ebe3908d8ce33b29f3b3448"
$env:SYNTHETIC_MODE="false"
$env:OFFLINE_MODE="false"
$env:SECRET_KEY="dijital-ayak-izi-2024"

Write-Host ""
Write-Host "API Ayarlari:" -ForegroundColor Green
Write-Host "  - SerpAPI Key: AYARLANDI" -ForegroundColor Green
Write-Host "  - Synthetic Mode: KAPALI (Gercek API aktif)" -ForegroundColor Green
Write-Host "  - Offline Mode: KAPALI" -ForegroundColor Green
Write-Host ""

Write-Host "[3/4] Backend dizinine geciliyor..." -ForegroundColor Yellow
Set-Location backend

Write-Host "[4/4] Sunucu baslatiliyor..." -ForegroundColor Yellow
Write-Host ""
Write-Host "================================" -ForegroundColor Magenta
Write-Host "  SUNUCU BILGILERI" -ForegroundColor Magenta
Write-Host "================================" -ForegroundColor Magenta
Write-Host "  Ana Sayfa: http://localhost:8000" -ForegroundColor Cyan
Write-Host "  API Docs:  http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "  DEBUG: Acik (Terminal loglarini takip et)" -ForegroundColor Yellow
Write-Host "================================" -ForegroundColor Magenta
Write-Host ""

uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

