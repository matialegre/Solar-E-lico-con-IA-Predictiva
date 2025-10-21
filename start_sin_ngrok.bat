@echo off
title Sistema Inversor - SIN ngrok (usa el tuyo)
color 0A

echo.
echo ========================================================================
echo   SISTEMA INVERSOR - USA TU NGROK EXISTENTE
echo ========================================================================
echo.

echo [PASO 1] Configurando Frontend...
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

echo [PASO 4] Iniciando Frontend en puerto 3001...
start "Frontend - Puerto 3001" cmd /k "cd frontend && set PORT=3001 && npm start"

echo.
echo ========================================================================
echo   SISTEMA INICIADO! (3 ventanas)
echo ========================================================================
echo.
echo URLs LOCALES:
echo   Backend:   http://localhost:8111
echo   API Docs:  http://localhost:8111/docs
echo   Frontend:  http://localhost:3001
echo.
echo TU NGROK (ya corriendo):
echo   https://argentina.ngrok.pro
echo.
echo IMPORTANTE:
echo   Tu ngrok en puerto 3001 YA FUNCIONA para el frontend!
echo   El frontend se conecta al backend en localhost:8111
echo.
echo Si quieres exponer la API publica:
echo   1. Para tu ngrok actual (Ctrl+C)
echo   2. Ejecuta: ngrok http 8111 --domain=argentina.ngrok.pro --region=sa
echo   3. Edita frontend\.env:
echo      REACT_APP_API_URL=https://argentina.ngrok.pro
echo   4. Reinicia frontend
echo.
echo ========================================================================
pause
