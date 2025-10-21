@echo off
title Sistema Completo - Frontend + Backend + ngrok
color 0A

echo.
echo ========================================================================
echo   SISTEMA INVERSOR - BUILD Y DEPLOY COMPLETO
echo ========================================================================
echo.

echo [PASO 1/6] Configurando API para rutas relativas...
echo REACT_APP_API_URL=/api > frontend\.env
echo PORT=3001 >> frontend\.env

echo [PASO 2/6] Haciendo build del frontend...
echo (Esto toma 2-3 minutos, espera...)
cd frontend
call npm run build
cd ..

echo [PASO 3/6] Copiando frontend al backend...
if exist backend\static rmdir /S /Q backend\static
xcopy /E /I /Y frontend\build backend\static

echo [PASO 4/6] Iniciando Backend + Frontend en puerto 8800...
start "Backend + Frontend - Puerto 8800" cmd /k "cd backend && python main.py --port 8800"
timeout /t 5 /nobreak >nul

echo [PASO 5/6] Iniciando Simulador...
start "Simulador" cmd /k "cd backend && python simulator.py --url http://localhost:8800 --interval 10"
timeout /t 2 /nobreak >nul

echo [PASO 6/6] Iniciando ngrok...
start "ngrok" cmd /k "ngrok http 8800 --domain=argentina.ngrok.pro --region=sa"

echo.
echo ========================================================================
echo   TODO LISTO!
echo ========================================================================
echo.
echo Abre en el navegador:
echo   https://argentina.ngrok.pro
echo.
echo Ahi vas a ver:
echo   - Frontend completo (dashboard, graficos, todo)
echo   - Backend API funcionando
echo   - Clima real de Bahia Blanca
echo   - Mapa geografico
echo.
echo ========================================================================
pause
