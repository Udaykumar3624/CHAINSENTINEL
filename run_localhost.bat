@echo off
TITLE ChainSentinel SIH26146 Localhost Launcher
echo =========================================================
echo     SHIELDING THE CHAIN - ChainSentinel (SIH26146)
echo =========================================================
echo.

set PATH=C:\Users\UDAY KUMAR\.gemini\antigravity\scratch\node_dist\node-v20.11.1-win-x64;%PATH%

echo [1/2] Launching FastAPI Backend (http://localhost:8000)...
start "ChainSentinel Backend" cmd /k "cd /d C:\Users\UDAY KUMAR\.gemini\antigravity\scratch\chainsentinel\backend && venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

timeout /t 2 >nul

echo [2/2] Launching React Frontend (http://localhost:5173)...
start "ChainSentinel Frontend" cmd /k "cd /d C:\Users\UDAY KUMAR\.gemini\antigravity\scratch\chainsentinel\frontend && npm run dev"

echo.
echo =========================================================
echo  ChainSentinel is running!
echo    - App Dashboard:     http://localhost:5173
echo    - SIH Judge Demo:    http://localhost:5173/judge-demo
echo    - Backend API Docs:  http://localhost:8000/docs
echo =========================================================
echo.
pause
