@echo off
title Sistema Inversor Hibrido
color 0A
cls

echo.
echo ================================================
echo    SISTEMA INVERSOR HIBRIDO - INICIANDO
echo ================================================
echo.

REM Backend (puerto configurable)
echo [1/3] Backend...
start "Backend" /MIN cmd /c "cd backend && python -m uvicorn main:app --host 0.0.0.0 --port 11113"
timeout /t 8 /nobreak >nul

REM Frontend  
echo [2/3] Frontend...
start "Frontend" /MIN cmd /c "cd frontend && set BROWSER=none && npm start"
timeout /t 5 /nobreak >nul

REM Ngrok (apunta al FRONTEND para ver el dashboard)
echo [3/3] Ngrok...
start "Ngrok" /MIN cmd /c "ngrok http 3002 --region sa --domain argentina.ngrok.pro"
timeout /t 3 /nobreak >nul

echo.
echo ================================================
echo    SISTEMA INICIADO CORRECTAMENTE
echo ================================================
echo.
echo   Backend:  http://localhost:11113/docs
echo             http://190.211.201.217:11113/docs (publico)
echo   Frontend: http://localhost:3002
echo   Ngrok:    https://argentina.ngrok.pro (frontend)
echo.
echo Abriendo dashboard en 3 segundos...
timeout /t 3 /nobreak >nul
start http://localhost:3002

echo.
echo Sistema corriendo. Para detener ejecuta: DETENER.bat
echo.
pause
