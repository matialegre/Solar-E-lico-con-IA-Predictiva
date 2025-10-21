@echo off
title Sistema Inversor - Inicio Completo con ngrok
color 0A

echo.
echo ========================================================================
echo   SISTEMA INVERSOR INTELIGENTE - INICIO COMPLETO
echo ========================================================================
echo.

REM Verificar ngrok
where ngrok >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] ngrok no esta instalado!
    echo.
    echo Descargalo desde: https://ngrok.com/download
    pause
    exit /b 1
)

echo [PASO 1] Configurando .env para Frontend...
echo REACT_APP_API_URL=http://localhost:8111 > frontend\.env
echo PORT=3001 >> frontend\.env
echo [OK] Frontend configurado
echo.

echo [PASO 2] Iniciando Backend en puerto 8111...
start "Backend API - Puerto 8111" cmd /k "cd backend && python main.py --port 8111"
timeout /t 5 /nobreak >nul

echo [PASO 3] Iniciando Simulador...
start "Simulador" cmd /k "cd backend && python simulator.py --url http://localhost:8111 --interval 10"
timeout /t 3 /nobreak >nul

echo [PASO 4] Iniciando ngrok para Backend (puerto 8111)...
start "ngrok - Backend 8111" cmd /k "ngrok http 8111 --region=sa"
timeout /t 3 /nobreak >nul

echo [PASO 5] Iniciando ngrok para Frontend (puerto 3001)...
start "ngrok - Frontend 3001" cmd /k "ngrok http 3001 --region=sa"
timeout /t 3 /nobreak >nul

echo [PASO 6] Iniciando Frontend en puerto 3001...
start "Frontend - Puerto 3001" cmd /k "cd frontend && set PORT=3001 && npm start"

echo.
echo ========================================================================
echo   TODO INICIADO! (5 ventanas)
echo ========================================================================
echo.
echo [1] Backend en puerto 8111
echo [2] Simulador
echo [3] ngrok Backend - COPIA LA URL DE AQUI
echo [4] ngrok Frontend - COPIA LA URL DE AQUI
echo [5] Frontend en puerto 3001
echo.
echo URLs LOCALES:
echo   Backend:   http://localhost:8111
echo   Frontend:  http://localhost:3001
echo.
echo PROXIMOS PASOS:
echo   1. Abre la ventana "ngrok - Backend 8111"
echo   2. Copia la URL publica (https://XXXXX.ngrok.io)
echo   3. Edita frontend\.env:
echo      REACT_APP_API_URL=https://XXXXX.ngrok.io
echo   4. Reinicia el Frontend (Ctrl+C y npm start)
echo.
echo Interfaces ngrok:
echo   http://127.0.0.1:4040 (Backend)
echo   http://127.0.0.1:4041 (Frontend)
echo.
echo ========================================================================
pause
