@echo off
title Verificacion ESP32
color 0E
cls

echo.
echo ================================================
echo   VERIFICACION ESTADO ESP32
echo ================================================
echo.

echo Consultando backend...
echo.

curl -s http://localhost:11112/api/esp32/devices

echo.
echo.
echo ================================================
echo   Si ves "is_online": true entonces funciona!
echo ================================================
echo.

pause
