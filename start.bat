@echo off
title Medical Chatbot Server
echo ========================================================
echo   Starting Demo City Health Clinic Assistant Server
echo ========================================================
echo.

cd /d "%~dp0"

IF NOT EXIST ".venv\Scripts\python.exe" (
    echo Creating virtual environment...
    python -m venv .venv
    echo Installing dependencies...
    .\.venv\Scripts\python.exe -m pip install -r requirements.txt
)

echo Starting FastAPI server at http://127.0.0.1:8000 ...
.\.venv\Scripts\python.exe server.py
pause
