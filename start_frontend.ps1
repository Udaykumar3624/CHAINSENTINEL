# ChainSentinel Frontend Start Script (PowerShell)
$ErrorActionPreference = "Stop"

Write-Host "=========================================================" -ForegroundColor Cyan
Write-Host "    Starting ChainSentinel Vite Frontend (Port 5173)..." -ForegroundColor Cyan
Write-Host "=========================================================" -ForegroundColor Cyan

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$frontendDir = Join-Path $scriptDir "frontend"

Set-Location $frontendDir

$nodeDist = "C:\Users\UDAY KUMAR\.gemini\antigravity\scratch\node_dist\node-v20.11.1-win-x64"
if (Test-Path $nodeDist) {
    $env:PATH = "$nodeDist;$env:PATH"
}

Write-Host "Launching Vite dev server on http://localhost:5173 ..." -ForegroundColor Green
npm run dev
