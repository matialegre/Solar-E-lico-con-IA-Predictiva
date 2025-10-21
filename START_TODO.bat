@echo off
title Sistema Inversor Completo
color 0A

echo.
echo ========================================================================
echo   SISTEMA INVERSOR - INICIO COMPLETO
echo ========================================================================
echo.

echo [1/4] Iniciando Backend en puerto 8800...
start "Backend - Puerto 8800" cmd /k "cd backend && python main.py --port 8800"
timeout /t 5 /nobreak >nul

echo [2/4] Iniciando Simulador...
start "Simulador" cmd /k "cd backend && python simulator.py --url http://localhost:8800 --interval 10"
timeout /t 3 /nobreak >nul

echo [3/4] Iniciando Frontend en puerto 3001...
start "Frontend - Puerto 3001" cmd /k "cd frontend && set PORT=3001 && npm start"
timeout /t 3 /nobreak >nul

echo [4/4] Iniciando ngrok...
start "ngrok - argentina.ngrok.pro" cmd /k "ngrok http 8800 --domain=argentina.ngrok.pro --region=sa"

echo.
echo ========================================================================
echo   TODO INICIADO!
echo ========================================================================
echo.
echo Backend:  http://localhost:8800
echo Frontend: http://localhost:3001
echo Publico:  https://argentina.ngrok.pro
echo.
echo ========================================================================
pause
