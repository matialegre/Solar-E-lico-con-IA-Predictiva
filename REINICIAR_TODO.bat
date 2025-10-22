@echo off
title Reiniciando Sistema Completo
color 0C
cls

echo.
echo ================================================
echo   REINICIANDO TODO EL SISTEMA
echo ================================================
echo.

echo [1/3] Deteniendo procesos anteriores...
taskkill /F /IM node.exe 2>nul
taskkill /F /IM python.exe 2>nul
echo    ✓ Procesos detenidos

timeout /t 3 /nobreak >nul

echo.
echo [2/3] Limpiando puertos...
netstat -ano | findstr :11112
netstat -ano | findstr :11113
timeout /t 2 /nobreak >nul

echo.
echo [3/3] Iniciando sistema actualizado...
call INICIAR_IP_PUBLICA.bat
