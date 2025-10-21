@echo off
title Deteniendo Sistema
color 0C
cls

echo.
echo ================================================
echo    DETENIENDO SISTEMA
echo ================================================
echo.

echo Cerrando procesos...

REM Matar por puerto
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :11113 ^| findstr LISTENING') do (
    echo Cerrando Backend (PID: %%a)
    taskkill /F /PID %%a >nul 2>&1
)
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8801 ^| findstr LISTENING') do (
    echo Cerrando Backend viejo puerto 8801 (PID: %%a)
    taskkill /F /PID %%a >nul 2>&1
)

for /f "tokens=5" %%a in ('netstat -ano ^| findstr :3002 ^| findstr LISTENING') do (
    echo Cerrando Frontend (PID: %%a)
    taskkill /F /PID %%a >nul 2>&1
)

for /f "tokens=5" %%a in ('netstat -ano ^| findstr :4040 ^| findstr LISTENING') do (
    echo Cerrando Ngrok (PID: %%a)
    taskkill /F /PID %%a >nul 2>&1
)

REM Limpiar procesos Node que quedaron
taskkill /F /IM node.exe >nul 2>&1
taskkill /F /IM ngrok.exe >nul 2>&1

echo.
echo ================================================
echo    SISTEMA DETENIDO
echo ================================================
echo.
pause
