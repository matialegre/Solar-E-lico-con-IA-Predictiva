@echo off
title Sistema Inversor - IP Publica
color 0A
cls

echo.
echo ================================================
echo   SISTEMA CON IP PUBLICA
echo ================================================
echo.

REM Limpiar procesos
taskkill /F /IM node.exe 2>nul
taskkill /F /IM python.exe 2>nul
timeout /t 2 /nobreak >nul

REM Backend en puerto 11112
echo [1/2] Iniciando Backend (puerto 11112)...
start "Backend" /MIN cmd /c "cd backend && python -m uvicorn main:app --host 0.0.0.0 --port 11112 --reload"
timeout /t 10 /nobreak >nul

REM Frontend en puerto 11113
echo [2/2] Iniciando Frontend (puerto 11113)...
cd frontend
set PORT=11113
set BROWSER=none
start "Frontend" /MIN cmd /c "npm start"
timeout /t 10 /nobreak >nul

echo.
echo ================================================
echo    SISTEMA INICIADO CON IP PUBLICA
echo ================================================
echo.
echo   Backend:  http://190.211.201.217:11112
echo             http://localhost:11112/docs
echo.
echo   Frontend: http://190.211.201.217:11113
echo             http://localhost:11113
echo.
echo   ACCESO PUBLICO: http://190.211.201.217:11113
echo.
timeout /t 3 /nobreak >nul
start http://190.211.201.217:11113

echo.
echo Sistema corriendo. Para detener: DETENER.bat
echo.
pause
