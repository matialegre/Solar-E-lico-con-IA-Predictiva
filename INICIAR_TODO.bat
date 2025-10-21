@echo off
title SISTEMA INVERSOR - Control Principal
color 0A

echo.
echo ========================================================================
echo   SISTEMA INVERSOR INTELIGENTE - INICIANDO TODO
echo ========================================================================
echo.

echo Configurando puertos...
echo Backend: 8801
echo Frontend: 3002
echo ngrok: argentina.ngrok.pro -^> 3002
echo.

echo [1/4] Iniciando Backend (puerto 8801)...
start "Backend-8801" cmd /k "cd /d X:\PREDICCION DE CLIMA\backend && python main.py --port 8801"
timeout /t 5 /nobreak >nul

echo [2/4] Iniciando Simulador...
start "Simulador" cmd /k "cd /d X:\PREDICCION DE CLIMA\backend && python simulator.py --url http://localhost:8801 --interval 10"
timeout /t 3 /nobreak >nul

echo [3/4] Iniciando Frontend (puerto 3002)...
start "Frontend-3002" cmd /k "cd /d X:\PREDICCION DE CLIMA\frontend && set PORT=3002 && npm start"
timeout /t 5 /nobreak >nul

echo [4/4] Iniciando ngrok...
start "ngrok-argentina" cmd /k "ngrok http 3002 --domain=argentina.ngrok.pro --region=sa"
timeout /t 3 /nobreak >nul

echo.
echo ========================================================================
echo   TODO INICIADO CORRECTAMENTE!
echo ========================================================================
echo.
echo Se abrieron 4 ventanas:
echo   [1] Backend en puerto 8801
echo   [2] Simulador de energia
echo   [3] Frontend en puerto 3002
echo   [4] ngrok - argentina.ngrok.pro
echo.
echo URLs:
echo   Dashboard publico: https://argentina.ngrok.pro
echo   Dashboard local:   http://localhost:3002
echo   Backend local:     http://localhost:8801
echo.
echo ========================================================================
echo   PRESIONA CTRL+C O CIERRA ESTA VENTANA PARA DETENER TODO
echo ========================================================================
echo.

:WAIT_LOOP
timeout /t 60 /nobreak >nul
goto WAIT_LOOP
