# BASIT BASLAT SCRIPT
Write-Host "Backend baslatiliyor..." -ForegroundColor Cyan
Set-Location backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

