@echo off
title Sistema Inversor - Configuracion Completa
color 0A

echo.
echo ========================================================================
echo   SISTEMA INVERSOR INTELIGENTE - CONFIGURACION
echo ========================================================================
echo.

echo [PASO 1] Verificando dependencias del Frontend...
cd frontend
if not exist node_modules (
    echo.
    echo   Instalando dependencias de npm ^(primera vez^)...
    echo   Esto puede tomar 2-3 minutos...
    echo.
    call npm install
    if %ERRORLEVEL% EQU 0 (
        echo.
        echo   [OK] Dependencias instaladas!
    ) else (
        echo.
        echo   [ERROR] Hubo un problema instalando dependencias
        pause
        exit /b 1
    )
) else (
    echo   [OK] Dependencias ya instaladas
)
cd ..

echo.
echo [PASO 2] Configurando puertos...
echo   Backend:  Puerto 8111
echo   Frontend: Puerto 3001
echo.

REM Crear archivo .env para frontend con puerto correcto
echo REACT_APP_API_URL=http://localhost:8111 > frontend\.env
echo PORT=3001 >> frontend\.env

echo [OK] Configuracion lista
echo.

echo [PASO 3] Iniciando servicios...
echo.

REM 1. Iniciar Backend en puerto 8111
echo [1/3] Iniciando Backend en puerto 8111...
start "Backend API - Puerto 8111" cmd /k "cd backend && python main.py --port 8111"
timeout /t 5 /nobreak >nul

REM 2. Iniciar Simulador apuntando al nuevo puerto
echo [2/3] Iniciando Simulador...
start "Simulador" cmd /k "cd backend && python simulator.py --url http://localhost:8111 --interval 10"
timeout /t 3 /nobreak >nul

REM 3. Iniciar Frontend en puerto 3001
echo [3/3] Iniciando Frontend en puerto 3001...
start "Frontend - Puerto 3001" cmd /k "cd frontend && set PORT=3001 && npm start"

echo.
echo ========================================================================
echo   SISTEMA INICIADO CON PUERTOS PERSONALIZADOS!
echo ========================================================================
echo.
echo URLs Locales:
echo   Backend:   http://localhost:8111
echo   API Docs:  http://localhost:8111/docs
echo   Frontend:  http://localhost:3001
echo.
echo Para ngrok (ejecuta en otra terminal):
echo   ngrok http 8111 --region=sa
echo.
echo Tu ngrok ya apunta a 3001, perfecto para el frontend!
echo   https://argentina.ngrok.pro (ya configurado)
echo.
echo ========================================================================
pause
