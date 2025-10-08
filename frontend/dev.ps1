# React Frontend Development Script
Write-Host "🚀 React Frontend Development Server Başlatılıyor..." -ForegroundColor Green

# Check if Node.js is installed
try {
    $nodeVersion = node --version
    Write-Host "✅ Node.js bulundu: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js bulunamadı! Lütfen Node.js yükleyin." -ForegroundColor Red
    exit 1
}

# Install dependencies if needed
if (-not (Test-Path "node_modules")) {
    Write-Host "📦 Bağımlılıklar yükleniyor..." -ForegroundColor Yellow
    npm install
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Bağımlılık yükleme başarısız!" -ForegroundColor Red
        exit 1
    }
}

# Start development server
Write-Host "🔧 Development server başlatılıyor..." -ForegroundColor Yellow
Write-Host "🌐 Frontend: http://localhost:3000" -ForegroundColor Cyan
Write-Host "🔗 Backend API: http://localhost:8000" -ForegroundColor Cyan
Write-Host "📚 API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "💡 Backend'i ayrı bir terminalde başlatın:" -ForegroundColor Yellow
Write-Host "   python -m uvicorn backend.app.main:app --reload" -ForegroundColor White
Write-Host ""

npm run dev
