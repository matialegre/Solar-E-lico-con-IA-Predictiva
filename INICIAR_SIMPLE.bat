@echo off
title Sistema Inversor - Inicio Simple
color 0A
cls

echo ================================================
echo   INICIANDO SISTEMA
echo ================================================
echo.

REM Limpiar
taskkill /F /IM node.exe 2>nul
taskkill /F /IM ngrok.exe 2>nul
timeout /t 2 /nobreak >nul

REM Backend
echo [1/4] Backend...
start "Backend" /MIN cmd /c "cd backend && python -m uvicorn main:app --host 0.0.0.0 --port 11113 --reload"
timeout /t 10 /nobreak >nul

REM Ngrok Backend (sin dominio fijo)
echo [2/4] Ngrok Backend...
start "Ngrok-Backend" /MIN cmd /c "ngrok http 11113 --region sa"
timeout /t 8 /nobreak >nul

REM Obtener URL
echo [3/4] Obteniendo URL del backend...
powershell -Command "$data = (Invoke-WebRequest -Uri 'http://127.0.0.1:4040/api/tunnels').Content | ConvertFrom-Json; $url = ($data.tunnels | Where-Object {$_.public_url -like 'https://*'} | Select-Object -First 1).public_url; $url | Out-File -FilePath 'frontend\.env.local' -Encoding ASCII -NoNewline; Add-Content -Path 'frontend\.env.local' -Value \"`r`nPORT=3002\"; Write-Host \"Backend: $url\" -ForegroundColor Green"

REM Leer URL
set /p BACKEND_URL=<frontend\.env.local
echo Frontend configurado para: %BACKEND_URL%
echo.

REM Frontend
echo [4/4] Frontend...
start "Frontend" /MIN cmd /c "cd frontend && set BROWSER=none && npm start"
timeout /t 10 /nobreak >nul

REM Ngrok Frontend (dominio fijo)
start "Ngrok-Frontend" /MIN cmd /c "ngrok http 3002 --region sa --domain argentina.ngrok.pro"
timeout /t 5 /nobreak >nul

echo.
echo ================================================
echo   SISTEMA INICIADO
echo ================================================
echo.
echo Backend:  %BACKEND_URL%
echo Frontend: https://argentina.ngrok.pro
echo Panel:    http://localhost:4040
echo.
timeout /t 3 /nobreak >nul
start https://argentina.ngrok.pro

pause
