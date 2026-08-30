# ChainSentinel Localhost Launch Script (PowerShell)
$ErrorActionPreference = "Stop"

Write-Host "=========================================================" -ForegroundColor Cyan
Write-Host "    SHIELDING THE CHAIN — ChainSentinel (SIH26146)" -ForegroundColor Cyan
Write-Host "=========================================================" -ForegroundColor Cyan

$baseDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$backendDir = Join-Path $baseDir "backend"
$frontendDir = Join-Path $baseDir "frontend"
$nodeDist = "C:\Users\UDAY KUMAR\.gemini\antigravity\scratch\node_dist\node-v20.11.1-win-x64"

if (Test-Path $nodeDist) {
    $env:PATH = "$nodeDist;$env:PATH"
}

Write-Host "`n[1/2] Starting FastAPI Backend on http://localhost:8000 ..." -ForegroundColor Yellow
$backendProcess = Start-Process -FilePath "$backendDir\venv\Scripts\python.exe" -ArgumentList "-m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload" -WorkingDirectory $backendDir -PassThru

Start-Sleep -Seconds 2

Write-Host "[2/2] Starting React Frontend on http://localhost:5173 ..." -ForegroundColor Yellow
$frontendProcess = Start-Process -FilePath "cmd.exe" -ArgumentList "/c npm run dev" -WorkingDirectory $frontendDir -PassThru

Write-Host "`n=========================================================" -ForegroundColor Green
Write-Host " ChainSentinel is up and running on Localhost!" -ForegroundColor Green
Write-Host "   -> Frontend App:      http://localhost:5173" -ForegroundColor Green
Write-Host "   -> SIH Judge Demo:    http://localhost:5173/judge-demo" -ForegroundColor Green
Write-Host "   -> Backend REST API:  http://localhost:8000/api/v1/health" -ForegroundColor Green
Write-Host "   -> Swagger API Docs:  http://localhost:8000/docs" -ForegroundColor Green
Write-Host "=========================================================" -ForegroundColor Green
Write-Host "Press Ctrl+C or close the terminal windows to stop servers." -ForegroundColor Gray
