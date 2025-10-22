@echo off
title Sistema Inversor - HTTPS con Dominios Fijos
color 0A
cls

echo.
echo ================================================
echo   SISTEMA CON NGROK DOMINIOS FIJOS
echo ================================================
echo.

REM ============================================
REM CONFIGURACION - EDITA TUS DOMINIOS AQUI
REM ============================================
set BACKEND_DOMAIN=PONER_TU_DOMINIO_BACKEND_AQUI
set FRONTEND_DOMAIN=argentina.ngrok.pro

REM ============================================

echo Limpiando procesos anteriores...
taskkill /F /IM node.exe 2>nul
taskkill /F /IM python.exe 2>nul  
taskkill /F /IM ngrok.exe 2>nul
timeout /t 3 /nobreak >nul

REM Verificar que se configuró el dominio del backend
if "%BACKEND_DOMAIN%"=="PONER_TU_DOMINIO_BACKEND_AQUI" (
    echo.
    echo ================================================
    echo   ERROR: FALTA CONFIGURAR DOMINIO DEL BACKEND
    echo ================================================
    echo.
    echo Abre este archivo: INICIAR_HTTPS_FIJO.bat
    echo Y edita la linea:
    echo   set BACKEND_DOMAIN=TU_DOMINIO_AQUI
    echo.
    echo Ejemplo:
    echo   set BACKEND_DOMAIN=backend-argentina.ngrok.pro
    echo.
    pause
    exit /b
)

echo.
echo [1/4] Iniciando Backend (puerto 11113)...
start "Backend-API" /MIN cmd /c "cd backend && python -m uvicorn main:app --host 0.0.0.0 --port 11113 --reload"
timeout /t 10 /nobreak >nul

echo [2/4] Creando tunel HTTPS FIJO para Backend...
echo          Dominio: https://%BACKEND_DOMAIN%
start "Ngrok-Backend" /MIN cmd /c "ngrok http 11113 --region sa --domain %BACKEND_DOMAIN%"
timeout /t 8 /nobreak >nul

echo [3/4] Configurando Frontend...
echo REACT_APP_API_URL=https://%BACKEND_DOMAIN% > frontend\.env.local
echo PORT=3002 >> frontend\.env.local
echo          Frontend usara: https://%BACKEND_DOMAIN%

echo [4/4] Iniciando Frontend y Ngrok...
start "Frontend-React" /MIN cmd /c "cd frontend && set BROWSER=none && npm start"
timeout /t 10 /nobreak >nul

start "Ngrok-Frontend" /MIN cmd /c "ngrok http 3002 --region sa --domain %FRONTEND_DOMAIN%"
timeout /t 5 /nobreak >nul

echo.
echo ================================================
echo    ✅ SISTEMA INICIADO CON DOMINIOS FIJOS
echo ================================================
echo.
echo   🔧 Backend HTTPS:  https://%BACKEND_DOMAIN%
echo   🌐 Frontend HTTPS: https://%FRONTEND_DOMAIN%
echo   📊 Panel Ngrok:    http://localhost:4040
echo   📝 API Docs:       https://%BACKEND_DOMAIN%/docs
echo.
echo   ✅ URLS FIJAS (no cambian al reiniciar)
echo   ✅ Sin errores de Mixed Content
echo.
timeout /t 3 /nobreak >nul
start https://%FRONTEND_DOMAIN%

echo.
echo Sistema corriendo. Para detener: DETENER.bat
echo.
pause
