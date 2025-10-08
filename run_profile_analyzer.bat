@echo off
echo 🔍 Sosyal Medya Profil Analiz Scripti
echo =====================================

REM Python'un yüklü olup olmadığını kontrol et
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python bulunamadı! Lütfen Python yükleyin.
    pause
    exit /b 1
)

REM .env dosyasının varlığını kontrol et
if not exist ".env" (
    echo ⚠️ .env dosyası bulunamadı!
    echo 📝 env_example.txt dosyasını .env olarak kopyalayın
    echo 🔑 Gerçek API anahtarlarınızı .env dosyasına ekleyin
    pause
    exit /b 1
)

REM Gereksinimleri yükle
echo 📦 Gereksinimler yükleniyor...
pip install -r profile_analyzer_requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Gereksinim yükleme başarısız!
    pause
    exit /b 1
)

REM Script'i çalıştır
echo 🚀 Profil analiz scripti başlatılıyor...
python profile_analyzer.py

pause
