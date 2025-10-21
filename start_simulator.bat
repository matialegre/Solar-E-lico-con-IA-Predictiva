@echo off
echo ========================================
echo  Iniciando Simulador de Energia
echo ========================================
echo.

cd backend

echo NOTA: Asegurese de que el backend este corriendo
echo.
timeout /t 3

python simulator.py --interval 10

pause
