@echo off
title Sistema Inversor Inteligente - Inicio con ngrok
color 0A

echo.
echo ========================================================================
echo   SISTEMA INVERSOR INTELIGENTE HIBRIDO - INICIO CON NGROK
echo ========================================================================
echo.
echo Este script iniciara:
echo   [1] Backend FastAPI (puerto 8000)
echo   [2] Simulador de Energia
echo   [3] Frontend React (puerto 3000)
echo   [4] ngrok tunnel para Backend (puerto 8000)
echo   [5] ngrok tunnel para Frontend (puerto 3000)
echo.
echo ========================================================================
echo.

REM Verificar si ngrok esta instalado
where ngrok >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] ngrok no esta instalado!
    echo.
    echo Descargalo desde: https://ngrok.com/download
    echo.
    echo O instalalo con chocolatey: choco install ngrok
    echo.
    pause
    exit /b 1
)

echo [OK] ngrok detectado correctamente
echo.

REM 1. Iniciar Backend
echo [1/5] Iniciando Backend FastAPI...
start "Backend API - Puerto 8000" cmd /k "cd /d backend && python main.py"
timeout /t 5 /nobreak >nul

REM 2. Iniciar Simulador
echo [2/5] Iniciando Simulador de Energia...
start "Simulador de Energia" cmd /k "cd /d backend && python simulator.py --interval 10"
timeout /t 3 /nobreak >nul

REM 3. Iniciar Frontend
echo [3/5] Iniciando Frontend React...
start "Frontend Dashboard - Puerto 3000" cmd /k "cd /d frontend && npm start"
timeout /t 5 /nobreak >nul

REM 4. Iniciar ngrok para Backend (puerto 8000)
echo [4/5] Iniciando ngrok para Backend API (puerto 8000)...
start "ngrok - Backend API" cmd /k "ngrok http 8000 --region=sa"
timeout /t 3 /nobreak >nul

REM 5. Iniciar ngrok para Frontend (puerto 3000)
echo [5/5] Iniciando ngrok para Frontend (puerto 3000)...
start "ngrok - Frontend Dashboard" cmd /k "ngrok http 3000 --region=sa"
timeout /t 3 /nobreak >nul

echo.
echo ========================================================================
echo   SISTEMA INICIADO CORRECTAMENTE!
echo ========================================================================
echo.
echo URLs LOCALES:
echo   Backend API:        http://localhost:8000
echo   API Docs:           http://localhost:8000/docs
echo   Frontend:           http://localhost:3000
echo.
echo URLs PUBLICAS (ngrok):
echo   Abre las ventanas de ngrok para ver las URLs publicas:
echo   - Backend API:      https://XXXXX.ngrok.io  (ventana "ngrok - Backend API")
echo   - Frontend:         https://XXXXX.ngrok.io  (ventana "ngrok - Frontend Dashboard")
echo.
echo IMPORTANTE:
echo   1. Copia la URL de ngrok del Backend
echo   2. Actualiza REACT_APP_API_URL en frontend/.env con esa URL
echo   3. Reinicia el frontend para que use la URL publica
echo.
echo INTERFAZ WEB DE NGROK:
echo   http://127.0.0.1:4040  (Backend)
echo   http://127.0.0.1:4041  (Frontend)
echo.
echo ========================================================================
echo.
echo Se han abierto 5 ventanas:
echo   [1] Backend API
echo   [2] Simulador
echo   [3] Frontend
echo   [4] ngrok Backend
echo   [5] ngrok Frontend
echo.
echo Presiona cualquier tecla para cerrar ESTA ventana...
echo (Los servicios seguiran corriendo)
echo.
pause >nul
