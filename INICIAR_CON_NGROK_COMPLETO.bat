@echo off
title Sistema Inversor Hibrido - HTTPS Completo
color 0A
cls

echo.
echo ================================================
echo    SISTEMA INVERSOR HIBRIDO - MODO NGROK
echo    Backend + Frontend con HTTPS
echo ================================================
echo.

REM Matar procesos previos
echo Limpiando procesos anteriores...
taskkill /F /IM node.exe 2>nul
taskkill /F /IM python.exe 2>nul
taskkill /F /IM ngrok.exe 2>nul
timeout /t 2 /nobreak >nul

REM Backend (puerto 11113)
echo [1/4] Iniciando Backend...
start "Backend" /MIN cmd /c "cd backend && python -m uvicorn main:app --host 0.0.0.0 --port 11113 --reload"
timeout /t 8 /nobreak >nul

REM Ngrok para BACKEND (HTTPS)
echo [2/4] Creando tunel HTTPS para Backend...
start "Ngrok-Backend" /MIN cmd /c "ngrok http 11113 --region sa"
timeout /t 5 /nobreak >nul

echo.
echo ================================================
echo   IMPORTANTE: COPIA LA URL DE NGROK DEL BACKEND
echo ================================================
echo.
echo 1. Abre el panel de ngrok: http://localhost:4040
echo 2. Busca el tunel del puerto 11113
echo 3. Copia la URL HTTPS (ejemplo: https://abc123.sa.ngrok.io)
echo 4. Pega esa URL cuando te la pida
echo.
set /p NGROK_BACKEND_URL="Pega aqui la URL HTTPS de ngrok del backend: "

REM Crear archivo de configuracion para el frontend
echo.
echo Configurando frontend con la URL del backend...
echo REACT_APP_API_URL=%NGROK_BACKEND_URL% > frontend\.env.local
echo PORT=3002 >> frontend\.env.local

REM Frontend
echo [3/4] Iniciando Frontend...
start "Frontend" /MIN cmd /c "cd frontend && set BROWSER=none && npm start"
timeout /t 8 /nobreak >nul

REM Ngrok para FRONTEND (dominio fijo)
echo [4/4] Creando tunel HTTPS para Frontend...
start "Ngrok-Frontend" /MIN cmd /c "ngrok http 3002 --region sa --domain argentina.ngrok.pro"
timeout /t 3 /nobreak >nul

echo.
echo ================================================
echo    SISTEMA INICIADO CORRECTAMENTE
echo ================================================
echo.
echo   Backend Ngrok:  %NGROK_BACKEND_URL%
echo   Backend Local:  http://localhost:11113/docs
echo   Frontend:       https://argentina.ngrok.pro
echo   Panel Ngrok:    http://localhost:4040
echo.
echo IMPORTANTE: Ahora el frontend usara HTTPS para el backend
echo             No habra mas errores de Mixed Content
echo.
echo Abriendo dashboard en 3 segundos...
timeout /t 3 /nobreak >nul
start https://argentina.ngrok.pro

echo.
echo Sistema corriendo con HTTPS completo
echo Para detener ejecuta: DETENER.bat
echo.
pause
