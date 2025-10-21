@echo off
title Build Frontend y Servir Todo
color 0A

echo.
echo ========================================================================
echo   CONSTRUYENDO FRONTEND PARA PRODUCCION
echo ========================================================================
echo.

echo [1/3] Haciendo build del frontend...
echo Esto puede tomar 2-3 minutos...
cd frontend
call npm run build
cd ..

echo.
echo [2/3] Copiando build al backend...
xcopy /E /I /Y frontend\build backend\static

echo.
echo [3/3] Iniciando servidor completo...
cd backend
python main.py --port 8800

pause
