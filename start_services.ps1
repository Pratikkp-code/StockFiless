# NIFTY Prediction Services Startup Script
Write-Host "🚀 Starting NIFTY Prediction Services..." -ForegroundColor Green
Write-Host ""

# Check if Python is available
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found. Please install Python 3.11+ and add it to PATH" -ForegroundColor Red
    exit 1
}

# Check if Node.js is available
try {
    $nodeVersion = node --version 2>&1
    Write-Host "✅ Node.js found: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js not found. Please install Node.js and add it to PATH" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "🔧 Starting Backend (Flask API)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\niftypred'; python.exe app/app.py" -WindowStyle Normal

Write-Host "⏳ Waiting for backend to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

Write-Host "🌐 Starting Frontend (React App)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\nifty-prediction-app'; npm start" -WindowStyle Normal

Write-Host ""
Write-Host "🎉 Services are starting!" -ForegroundColor Green
Write-Host "🔧 Backend API: http://localhost:5000" -ForegroundColor Cyan
Write-Host "🌐 Frontend App: http://localhost:3000" -ForegroundColor Cyan
Write-Host ""

# Wait a bit more for services to fully start
Start-Sleep -Seconds 15

# Try to open the application in browser
try {
    Write-Host "🌐 Opening application in browser..." -ForegroundColor Yellow
    Start-Process "http://localhost:3000"
} catch {
    Write-Host "⚠️  Could not open browser automatically. Please manually navigate to:" -ForegroundColor Yellow
    Write-Host "   http://localhost:3000" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "💡 Services are running in separate windows." -ForegroundColor Green
Write-Host "   Close those windows to stop the services." -ForegroundColor Yellow
Write-Host ""
Write-Host "Press any key to exit this startup script..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
