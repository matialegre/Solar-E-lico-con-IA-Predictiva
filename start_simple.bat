@echo off
title Sistema Inversor - Inicio Simple
color 0A

echo.
echo ========================================================================
echo   SISTEMA INVERSOR INTELIGENTE - INICIO SIMPLE
echo ========================================================================
echo.

REM 1. Iniciar Backend
echo [1/3] Iniciando Backend en puerto 8000...
start "Backend API" cmd /k "cd backend && python main.py"
timeout /t 5 /nobreak >nul

REM 2. Iniciar Simulador
echo [2/3] Iniciando Simulador...
start "Simulador" cmd /k "cd backend && python simulator.py --interval 10"
timeout /t 3 /nobreak >nul

REM 3. Iniciar Frontend
echo [3/3] Iniciando Frontend en puerto 3000...
start "Frontend" cmd /k "cd frontend && npm start"

echo.
echo ========================================================================
echo   SISTEMA INICIADO!
echo ========================================================================
echo.
echo URLs Locales:
echo   Backend:   http://localhost:8000
echo   Frontend:  http://localhost:3000
echo.
echo Si ya tienes ngrok corriendo, asegurate de que apunte a:
echo   - Backend: puerto 8000
echo   - Frontend: puerto 3000
echo.
echo Y configura frontend/.env con la URL publica de ngrok
echo.
pause
