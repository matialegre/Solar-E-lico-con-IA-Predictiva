@echo off
echo ========================================
echo  Iniciando Frontend - Dashboard React
echo ========================================
echo.

cd frontend

echo Verificando dependencias...
if not exist "node_modules\" (
    echo Instalando dependencias npm...
    call npm install
)

echo.
echo Iniciando aplicacion React...
echo.
echo URL: http://localhost:3000
echo.

call npm start

pause
