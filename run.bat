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

REM Make sure .env exists (prof-proof)
if not exist ".env" (
  if exist ".env.docker.example" (
    echo [INFO] .env not found. Creating from .env.docker.example...
    copy /Y ".env.docker.example" ".env" >nul
    echo [OK] Created .env
  ) else (
    echo [WARN] .env not found and .env.docker.example not found.
    echo Create a .env file manually before running.
  )
) else (
  echo [OK] .env exists
)

REM Use a clean project name to avoid invalid image name like exchange_-web
set PROJECT_NAME=exchange

REM Start (build + run)
echo [INFO] Building and starting containers (project: %PROJECT_NAME%)...
docker compose -p %PROJECT_NAME% up -d --build
if errorlevel 1 (
  echo [ERROR] docker compose failed.

  REM Most common cause: Postgres port 5432 already allocated
  echo.
  echo If you see: "Bind for 0.0.0.0:5432 failed: port is already allocated"
  echo Fix: remove/comment the db ports mapping in docker-compose.yml:
  echo   db:
  echo     # ports:
  echo     #   - "5432:5432"
  echo.
  echo Then rerun this script.

  echo.
  echo Logs (web):
  docker compose -p %PROJECT_NAME% logs --tail=200 web
  pause
  exit /b 1
)

REM Run migrations automatically (first run / safe to rerun)
echo [INFO] Running migrations...
docker compose -p %PROJECT_NAME% exec web python manage.py migrate
if errorlevel 1 (
  echo [WARN] Migration step failed. Showing logs:
  docker compose -p %PROJECT_NAME% logs --tail=200 web
  echo You can retry manually:
  echo   docker compose -p %PROJECT_NAME% exec web python manage.py migrate
  pause
  exit /b 1
)

echo [INFO] Containers are up. Opening the site...
start "" "http://localhost:8000"

echo.
echo [DONE] If the page is not ready yet, wait 10-20 seconds then refresh.
echo To stop:   docker compose -p %PROJECT_NAME% down
echo Logs:      docker compose -p %PROJECT_NAME% logs -f web
echo.
pause
