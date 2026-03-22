@echo off
setlocal
color 0B
title Test Automation Dashboard

echo.
echo  ============================================================
echo    TEST AUTOMATION DASHBOARD - Web Interface
echo  ============================================================
echo.

REM --- Check Python ---
python --version >nul 2>&1
if %errorlevel% neq 0 (
    color 0C
    echo  [ERROR] Python is not installed or not in PATH.
    echo          Install Python 3.9+ from https://www.python.org/
    pause
    exit /b 1
)
echo  [OK] Python found

REM --- Install web dependencies ---
echo  [..] Installing web dependencies...
python -m pip install fastapi uvicorn python-multipart >nul 2>&1
echo  [OK] Dependencies ready
echo.

echo  ============================================================
echo    Starting server at  http://localhost:5000
echo    Press Ctrl+C to stop the server
echo  ============================================================
echo.

REM --- Open browser after 2 seconds ---
start /b cmd /c "timeout /t 2 /nobreak >nul && start http://localhost:5000"

REM --- Start the FastAPI server ---
cd /d "%~dp0web_app"
python -m uvicorn app:app --host 0.0.0.0 --port 5000

pause
