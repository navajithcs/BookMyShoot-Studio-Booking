# BookMyShoot - Startup Script for PowerShell
# Usage: .\run.ps1

$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$venvPython = Join-Path $projectRoot ".venv\Scripts\python.exe"
$backendDir = Join-Path $projectRoot "backend"

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  BookMyShoot - Full Stack Application" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment exists
if (-not (Test-Path $venvPython)) {
    Write-Host "ERROR: Virtual environment not found!" -ForegroundColor Red
    Write-Host "Please run configure_python_environment first." -ForegroundColor Yellow
    exit 1
}

Write-Host "Starting services..." -ForegroundColor Yellow
Write-Host ""

# Kill any existing Flask processes on port 5000
Write-Host "Checking for existing servers on port 5000..." -ForegroundColor Yellow
$connections = Get-NetTCPConnection -LocalPort 5000 -State Listen -ErrorAction SilentlyContinue
if ($connections) {
    foreach ($conn in $connections) {
        $proc = Get-Process -Id $conn.OwningProcess -ErrorAction SilentlyContinue
        if ($proc -and $proc.Name -eq 'python') {
            Write-Host "  Stopping old process PID=$($conn.OwningProcess)..." -ForegroundColor DarkYellow
            Stop-Process -Id $conn.OwningProcess -Force -ErrorAction SilentlyContinue
        }
    }
    Start-Sleep -Seconds 2
}
Write-Host ""

# Start Backend
Write-Host "Starting Backend (Flask) on http://localhost:5000..." -ForegroundColor Green
$backendProcess = Start-Process -FilePath $venvPython `
    -ArgumentList @((Join-Path $backendDir "app.py"), "--no-reload") `
    -WorkingDirectory $backendDir `
    -WindowStyle Normal `
    -PassThru

Start-Sleep -Seconds 2

# Start Frontend
Write-Host "Starting Frontend (HTTP Server) on http://localhost:5173..." -ForegroundColor Green
$frontendProcess = Start-Process -FilePath $venvPython `
    -ArgumentList "serve_frontend.py" `
    -WorkingDirectory $projectRoot `
    -WindowStyle Normal `
    -PassThru

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  All servers started!" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Access the application:" -ForegroundColor Yellow
Write-Host "  Frontend: http://localhost:5173" -ForegroundColor White
Write-Host "  Backend:  http://localhost:5000" -ForegroundColor White
Write-Host ""
Write-Host "Press any key to close this window and stop all servers..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

# Kill the processes
Stop-Process -Id $backendProcess.Id -Force -ErrorAction SilentlyContinue
Stop-Process -Id $frontendProcess.Id -Force -ErrorAction SilentlyContinue

Write-Host "Servers stopped." -ForegroundColor Green
