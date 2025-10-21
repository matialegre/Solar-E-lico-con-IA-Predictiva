@echo off
echo ========================================
echo  Sistema Inversor Inteligente Hibrido
echo  Inicio Completo del Sistema
echo ========================================
echo.
echo Iniciando todos los componentes...
echo.

REM Iniciar backend en nueva ventana
echo [1/3] Iniciando Backend...
start "Backend - Inversor Inteligente" cmd /k "cd backend && python main.py"
timeout /t 5

REM Iniciar simulador en nueva ventana
echo [2/3] Iniciando Simulador...
start "Simulador de Energia" cmd /k "cd backend && python simulator.py --interval 10"
timeout /t 3

REM Iniciar frontend en nueva ventana
echo [3/3] Iniciando Frontend...
start "Frontend - Dashboard" cmd /k "cd frontend && npm start"

echo.
echo ========================================
echo  Sistema iniciado correctamente
echo ========================================
echo.
echo Backend:    http://localhost:8000
echo Frontend:   http://localhost:3000
echo Docs API:   http://localhost:8000/docs
echo.
echo Presione cualquier tecla para cerrar esta ventana...
echo (Los servicios seguiran corriendo)
echo.
pause > nul
