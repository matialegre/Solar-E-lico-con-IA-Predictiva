@echo off
title Deteniendo Sistema Inversor
color 0C

echo.
echo ========================================================================
echo   DETENIENDO TODOS LOS SERVICIOS
echo ========================================================================
echo.

echo [1/5] Cerrando puertos 8801 y 3002...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":8801" ^| findstr "LISTENING"') do taskkill /F /PID %%a 2>nul
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":3002" ^| findstr "LISTENING"') do taskkill /F /PID %%a 2>nul

echo [2/5] Cerrando procesos de Python (Backend + Simulador)...
taskkill /F /FI "WINDOWTITLE eq Backend-8801*" 2>nul
taskkill /F /FI "WINDOWTITLE eq Simulador*" 2>nul
taskkill /F /IM python.exe 2>nul

echo [3/5] Cerrando proceso de Node (Frontend)...
taskkill /F /FI "WINDOWTITLE eq Frontend-3002*" 2>nul
taskkill /F /IM node.exe 2>nul

echo [4/5] Cerrando ngrok...
taskkill /F /FI "WINDOWTITLE eq ngrok-argentina*" 2>nul
taskkill /F /IM ngrok.exe 2>nul

echo [5/5] Limpieza final...
timeout /t 2 /nobreak >nul

echo.
echo ========================================================================
echo   TODOS LOS SERVICIOS DETENIDOS
echo ========================================================================
echo.
pause
