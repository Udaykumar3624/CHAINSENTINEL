# ChainSentinel Backend Start Script (PowerShell)
$ErrorActionPreference = "Stop"

Write-Host "=========================================================" -ForegroundColor Cyan
Write-Host "    Starting ChainSentinel FastAPI Backend (Port 8000)..." -ForegroundColor Cyan
Write-Host "=========================================================" -ForegroundColor Cyan

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

if (Test-Path ".\.venv\Scripts\Activate.ps1") {
    Write-Host "Activating .venv virtual environment..." -ForegroundColor Yellow
    & ".\.venv\Scripts\Activate.ps1"
} elseif (Test-Path ".\venv\Scripts\Activate.ps1") {
    Write-Host "Activating venv virtual environment..." -ForegroundColor Yellow
    & ".\venv\Scripts\Activate.ps1"
} else {
    Write-Host "Virtual environment not found. Please create .venv first." -ForegroundColor Red
    exit 1
}

$env:DATABASE_URL = "sqlite:///./chainsentinel.db"
$env:ENVIRONMENT = "development"
$env:ENABLE_DOCS = "true"

Write-Host "Launching Uvicorn server on http://localhost:8000 ..." -ForegroundColor Green
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
