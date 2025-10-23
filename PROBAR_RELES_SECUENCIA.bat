@echo off
setlocal

set "SERVER_URL=http://190.211.201.217:11113"
set "DEVICE_ID=ESP32_INVERSOR_001"
set "CURL_EXE=curl"
if exist "C:\Users\Mundo Outdoor\Downloads\curl-8.16.0_9-win64a-mingw\bin\curl.exe" set "CURL_EXE=C:\Users\Mundo Outdoor\Downloads\curl-8.16.0_9-win64a-mingw\bin\curl.exe"

echo ========================================
echo   PRUEBA SECUENCIAL DE 4 RELES
echo ========================================
echo.

:: SOLAR ON
echo [1/8] SOLAR ON...
"%CURL_EXE%" -s -X POST "%SERVER_URL%/api/esp32/command/%DEVICE_ID%" -H "Content-Type: application/json" -d "{\"command\":\"solar\",\"parameter\":\"on\"}" >nul
timeout /t 1 /nobreak >nul

:: SOLAR OFF
echo [2/8] SOLAR OFF...
"%CURL_EXE%" -s -X POST "%SERVER_URL%/api/esp32/command/%DEVICE_ID%" -H "Content-Type: application/json" -d "{\"command\":\"solar\",\"parameter\":\"off\"}" >nul
timeout /t 1 /nobreak >nul

:: EOLICA ON
echo [3/8] EOLICA ON...
"%CURL_EXE%" -s -X POST "%SERVER_URL%/api/esp32/command/%DEVICE_ID%" -H "Content-Type: application/json" -d "{\"command\":\"eolica\",\"parameter\":\"on\"}" >nul
timeout /t 1 /nobreak >nul

:: EOLICA OFF
echo [4/8] EOLICA OFF...
"%CURL_EXE%" -s -X POST "%SERVER_URL%/api/esp32/command/%DEVICE_ID%" -H "Content-Type: application/json" -d "{\"command\":\"eolica\",\"parameter\":\"off\"}" >nul
timeout /t 1 /nobreak >nul

:: RED ON
echo [5/8] RED ON...
"%CURL_EXE%" -s -X POST "%SERVER_URL%/api/esp32/command/%DEVICE_ID%" -H "Content-Type: application/json" -d "{\"command\":\"red\",\"parameter\":\"on\"}" >nul
timeout /t 1 /nobreak >nul

:: RED OFF
echo [6/8] RED OFF...
"%CURL_EXE%" -s -X POST "%SERVER_URL%/api/esp32/command/%DEVICE_ID%" -H "Content-Type: application/json" -d "{\"command\":\"red\",\"parameter\":\"off\"}" >nul
timeout /t 1 /nobreak >nul

:: CARGA ON (ya esta on, pero igual)
echo [7/8] CARGA ON...
"%CURL_EXE%" -s -X POST "%SERVER_URL%/api/esp32/command/%DEVICE_ID%" -H "Content-Type: application/json" -d "{\"command\":\"carga\",\"parameter\":\"on\"}" >nul
timeout /t 1 /nobreak >nul

:: CARGA OFF
echo [8/8] CARGA OFF...
"%CURL_EXE%" -s -X POST "%SERVER_URL%/api/esp32/command/%DEVICE_ID%" -H "Content-Type: application/json" -d "{\"command\":\"carga\",\"parameter\":\"off\"}" >nul
timeout /t 1 /nobreak >nul

echo.
echo ========================================
echo   PRUEBA COMPLETADA
echo ========================================
echo.
echo Verifica en el Serial Monitor que todos los reles cambiaron.
echo.
pause
