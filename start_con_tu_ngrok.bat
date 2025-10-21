@echo off
title Sistema Inversor con argentina.ngrok.pro
color 0A

echo.
echo ========================================================================
echo   SISTEMA INVERSOR - USA argentina.ngrok.pro
echo ========================================================================
echo.

echo [PASO 1] Configurando Frontend para usar tu ngrok...
echo REACT_APP_API_URL=https://argentina.ngrok.pro > frontend\.env
echo PORT=3001 >> frontend\.env
echo [OK] Frontend configurado con argentina.ngrok.pro
echo.

echo [PASO 2] Iniciando Backend en puerto 8111...
start "Backend API - Puerto 8111" cmd /k "cd backend && python main.py --port 8111"
timeout /t 5 /nobreak >nul

echo [PASO 3] Iniciando Simulador...
start "Simulador" cmd /k "cd backend && python simulator.py --url http://localhost:8111 --interval 10"
timeout /t 3 /nobreak >nul

echo [PASO 4] Iniciando Frontend en puerto 3001...
start "Frontend - Puerto 3001" cmd /k "cd frontend && set PORT=3001 && npm start"

echo.
echo ========================================================================
echo   SISTEMA INICIADO!
echo ========================================================================
echo.
echo Backend:   http://localhost:8111
echo Frontend:  http://localhost:3001
echo.
echo IMPORTANTE:
echo   Tu ngrok debe apuntar al puerto 8111 (backend)
echo   
echo   En tu terminal de ngrok ejecuta:
echo   ngrok http 8111 --domain=argentina.ngrok.pro --region=sa
echo.
echo   El frontend ya esta configurado para usar:
echo   https://argentina.ngrok.pro
echo.
echo ========================================================================
pause
