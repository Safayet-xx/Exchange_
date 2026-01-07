@echo off
setlocal ENABLEDELAYEDEXPANSION

echo ==========================================
echo   Exchange Platform - Docker Run Script
echo ==========================================

REM Go to the folder where this file lives
cd /d "%~dp0"

REM Quick docker check
docker --version >nul 2>&1
if errorlevel 1 (
  echo [ERROR] Docker is not installed or not on PATH.
  echo Install Docker Desktop and try again.
  pause
  exit /b 1
)

REM Start (build + run)
echo [INFO] Building and starting containers...
docker compose up -d --build
if errorlevel 1 (
  echo [ERROR] docker compose failed.
  echo Try: docker compose logs --tail=200 web
  pause
  exit /b 1
)

echo [INFO] Containers are starting. Opening the site...
start "" "http://localhost:8000"

echo.
echo [DONE] If the page is not ready yet, wait 10-20 seconds then refresh.
echo To stop:   docker compose down
echo Logs:      docker compose logs -f web
echo.
pause
