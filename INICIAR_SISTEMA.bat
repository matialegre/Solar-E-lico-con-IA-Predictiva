@echo off
echo ========================================
echo   SISTEMA INVERSOR INTELIGENTE
echo   Iniciar Backend + Frontend
echo ========================================
echo.

echo [1/2] Iniciando Backend (FastAPI)...
echo.
start "Backend - FastAPI" cmd /k "cd /d X:\PREDICCION DE CLIMA\backend && python main.py"
echo Backend iniciado en nueva ventana
echo URL: http://localhost:11113
echo.
timeout /t 3 /nobreak >nul

echo [2/2] Iniciando Frontend (React)...
echo.
start "Frontend - React" cmd /k "cd /d X:\PREDICCION DE CLIMA\frontend && npm start"
echo Frontend iniciado en nueva ventana
echo URL: http://localhost:3002 (se abrira automaticamente)
echo.

echo.
echo ========================================
echo   SISTEMA INICIADO
echo ========================================
echo.
echo Backend:  http://localhost:11113
echo Frontend: http://localhost:3002
echo.
echo Para probar comandos, ejecuta:
echo   test_reles.bat
echo.
pause
