@echo off
setlocal

set "CURL_EXE=curl"
if exist "C:\Users\Mundo Outdoor\Downloads\curl-8.16.0_9-win64a-mingw\bin\curl.exe" set "CURL_EXE=C:\Users\Mundo Outdoor\Downloads\curl-8.16.0_9-win64a-mingw\bin\curl.exe"

echo ========================================
echo   TEST API ESP32
echo ========================================
echo.

echo Consultando: /api/esp32/devices
echo.
"%CURL_EXE%" -s http://190.211.201.217:11113/api/esp32/devices | python -m json.tool

echo.
echo.
pause
