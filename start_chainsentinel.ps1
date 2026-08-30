# ChainSentinel Full Stack Launcher (PowerShell)
$ErrorActionPreference = "Stop"

Write-Host "=========================================================" -ForegroundColor Cyan
Write-Host "    SHIELDING THE CHAIN — ChainSentinel (SIH26146)" -ForegroundColor Cyan
Write-Host "=========================================================" -ForegroundColor Cyan

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# 1. Start Backend in separate PowerShell process
Write-Host "`n[1/2] Launching Backend Server process..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-ExecutionPolicy", "Bypass", "-File", "`"$scriptDir\start_backend.ps1`""

Start-Sleep -Seconds 3

# 2. Start Frontend in separate PowerShell process
Write-Host "[2/2] Launching Frontend Server process..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-ExecutionPolicy", "Bypass", "-File", "`"$scriptDir\start_frontend.ps1`""

Write-Host "`n=========================================================" -ForegroundColor Green
Write-Host " ChainSentinel Services Launched Successfully!" -ForegroundColor Green
Write-Host "   -> Frontend Web Application: http://localhost:5173" -ForegroundColor Green
Write-Host "   -> SIH Judge Demo Workflow:  http://localhost:5173/judge-demo" -ForegroundColor Green
Write-Host "   -> FastAPI REST API:         http://localhost:8000/api/v1/health" -ForegroundColor Green
Write-Host "   -> OpenAPI Swagger Docs:     http://localhost:8000/docs" -ForegroundColor Green
Write-Host "=========================================================" -ForegroundColor Green
