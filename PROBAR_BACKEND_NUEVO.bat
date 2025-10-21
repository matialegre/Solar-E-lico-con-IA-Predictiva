@echo off
title Backend - Nuevas Funcionalidades
color 0A
cls

echo.
echo ================================================
echo    BACKEND - NUEVAS FUNCIONALIDADES
echo ================================================
echo.
echo Funcionalidades agregadas:
echo.
echo 1. Registro de dispositivos ESP32
echo 2. Heartbeat y estado online/offline
echo 3. Configuracion dinamica (lat/lon)
echo 4. NASA POWER API (historicos 40 anos)
echo 5. Dimensionamiento solar (pvlib)
echo 6. Dimensionamiento eolico (Betz)
echo 7. Calculos con ecuaciones mostradas
echo.
echo ================================================
echo.

cd backend

echo Instalando dependencias nuevas...
pip install httpx==0.25.2

echo.
echo Iniciando backend...
echo.
python -m uvicorn main:app --host 0.0.0.0 --port 11113 --reload

pause
