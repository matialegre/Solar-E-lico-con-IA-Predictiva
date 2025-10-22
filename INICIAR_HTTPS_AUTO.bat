@echo off
title Sistema Inversor Hibrido - HTTPS Automatico
color 0A
cls

echo.
echo ================================================
echo    SISTEMA INVERSOR HIBRIDO - HTTPS AUTO
echo ================================================
echo.

REM Limpiar procesos previos
echo Limpiando procesos anteriores...
taskkill /F /IM node.exe 2>nul
taskkill /F /IM python.exe 2>nul
taskkill /F /IM ngrok.exe 2>nul
timeout /t 3 /nobreak >nul

REM Iniciar Backend
echo [1/4] Iniciando Backend (puerto 11113)...
start "Backend-API" cmd /c "cd backend && python -m uvicorn main:app --host 0.0.0.0 --port 11113 --reload"
timeout /t 10 /nobreak >nul

REM Iniciar Ngrok para Backend
echo [2/4] Creando tunel HTTPS para Backend...
start "Ngrok-Backend" cmd /c "ngrok http 11113 --region sa --log stdout"
timeout /t 8 /nobreak >nul

REM Obtener URL de ngrok usando Python
echo [3/4] Obteniendo URL de ngrok del backend...
python -c "import requests, json; r = requests.get('http://127.0.0.1:4040/api/tunnels'); data = r.json(); url = [t['public_url'] for t in data['tunnels'] if 'https' in t['public_url']][0]; print(url); open('backend_ngrok_url.txt', 'w').write(url)"

REM Leer URL del archivo
set /p BACKEND_URL=<backend_ngrok_url.txt
echo.
echo ✅ Backend disponible en: %BACKEND_URL%
echo.

REM Crear configuracion del frontend
echo Configurando frontend...
echo REACT_APP_API_URL=%BACKEND_URL% > frontend\.env.local
echo PORT=3002 >> frontend\.env.local

REM Iniciar Frontend
echo [4/4] Iniciando Frontend y Ngrok...
start "Frontend-React" cmd /c "cd frontend && set BROWSER=none && npm start"
timeout /t 10 /nobreak >nul

REM Ngrok para Frontend (dominio fijo)
start "Ngrok-Frontend" cmd /c "ngrok http 3002 --region sa --domain argentina.ngrok.pro"
timeout /t 5 /nobreak >nul

echo.
echo ================================================
echo    ✅ SISTEMA INICIADO CON EXITO
echo ================================================
echo.
echo   🔧 Backend HTTPS:  %BACKEND_URL%
echo   🌐 Frontend HTTPS: https://argentina.ngrok.pro
echo   📊 Panel Ngrok:    http://localhost:4040
echo   📝 Docs Backend:   %BACKEND_URL%/docs
echo.
echo   ✅ Sin errores de Mixed Content
echo   ✅ Todas las conexiones son HTTPS
echo.
timeout /t 3 /nobreak >nul
start https://argentina.ngrok.pro

echo.
echo Sistema corriendo. Para detener: DETENER.bat
echo.
pause
