@echo off
title Arogya Seva Chatbot - Online Launcher
echo ========================================================
echo   1. Starting Local Chatbot Server (Port 8000)...
echo ========================================================
cd /d "%~dp0"

REM Launch local server in background window
start "Arogya Seva Local Server" cmd /k ".\.venv\Scripts\python.exe server.py"

echo.
echo Waiting 3 seconds for server to initialize...
timeout /t 3 /nobreak >nul

echo.
echo ========================================================
echo   2. Creating Secure Online Tunnel...
echo   Copy the https://... link that appears below!
echo ========================================================
echo.

ssh -o StrictHostKeyChecking=no -R 80:localhost:8000 nokey@localhost.run
pause
