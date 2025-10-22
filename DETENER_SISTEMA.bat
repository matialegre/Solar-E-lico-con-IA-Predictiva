@echo off
title Detener Sistema
color 0C
cls

echo.
echo ================================================
echo   DETENIENDO TODO EL SISTEMA
echo ================================================
echo.

echo Cerrando Backend (Python)...
taskkill /F /IM python.exe 2>nul
echo    ✅ Backend detenido

echo.
echo Cerrando Frontend (Node)...
taskkill /F /IM node.exe 2>nul
echo    ✅ Frontend detenido

echo.
echo Liberando puertos 11112 y 11113...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :11112') do taskkill /F /PID %%a 2>nul
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :11113') do taskkill /F /PID %%a 2>nul
echo    ✅ Puertos liberados

timeout /t 2 /nobreak >nul

echo.
echo ================================================
echo   ✅ SISTEMA COMPLETAMENTE DETENIDO
echo ================================================
echo.
echo   Para reiniciar: REINICIO_TOTAL.bat
echo.
pause
