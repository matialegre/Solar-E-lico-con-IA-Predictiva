@echo off
title ngrok Tunnels - Sistema Inversor
color 0B

echo.
echo ========================================================================
echo   INICIANDO TUNNELS NGROK
echo ========================================================================
echo.

REM Verificar si ngrok esta instalado
where ngrok >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] ngrok no esta instalado!
    echo.
    echo Descargalo desde: https://ngrok.com/download
    echo O instalalo con: choco install ngrok
    echo.
    pause
    exit /b 1
)

echo [1] Iniciando ngrok para Backend API (puerto 8000)...
start "ngrok - Backend API (8000)" cmd /k "ngrok http 8000 --region=sa"
timeout /t 2 /nobreak >nul

echo [2] Iniciando ngrok para Frontend (puerto 3000)...
start "ngrok - Frontend (3000)" cmd /k "ngrok http 3000 --region=sa"
timeout /t 2 /nobreak >nul

echo.
echo ========================================================================
echo   TUNNELS ACTIVOS!
echo ========================================================================
echo.
echo Interfaces web de ngrok:
echo   Backend:   http://127.0.0.1:4040
echo   Frontend:  http://127.0.0.1:4041
echo.
echo En cada ventana de ngrok veras la URL publica tipo:
echo   https://XXXXX.ngrok.io
echo.
echo CONFIGURAR FRONTEND:
echo   1. Copia la URL publica del Backend desde ngrok
echo   2. Edita frontend/.env:
echo      REACT_APP_API_URL=https://XXXXX.ngrok.io
echo   3. Reinicia el frontend
echo.
echo ========================================================================
pause
