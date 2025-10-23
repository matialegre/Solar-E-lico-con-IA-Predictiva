@echo off
setlocal

set "SERVER_URL=http://190.211.201.217:11113"
set "DEVICE_ID=ESP32_INVERSOR_001"
set "CURL_EXE=curl"
if exist "C:\Users\Mundo Outdoor\Downloads\curl-8.16.0_9-win64a-mingw\bin\curl.exe" set "CURL_EXE=C:\Users\Mundo Outdoor\Downloads\curl-8.16.0_9-win64a-mingw\bin\curl.exe"

echo ========================================
echo TEST 1: Puerto 11113 abierto?
echo ========================================
netstat -ano | findstr :11113
echo.
echo.

echo ========================================
echo TEST 2: Health check localhost
echo ========================================
"%CURL_EXE%" -v http://localhost:11113/health
echo.
echo.

echo ========================================
echo TEST 3: Health check 127.0.0.1
echo ========================================
"%CURL_EXE%" -v http://127.0.0.1:11113/health
echo.
echo.

echo ========================================
echo TEST 4: Health check IP publica
echo ========================================
"%CURL_EXE%" -v %SERVER_URL%/health
echo.
echo.

echo ========================================
echo TEST 5: Listar dispositivos
echo ========================================
"%CURL_EXE%" -s %SERVER_URL%/api/esp32/devices
echo.
echo.

echo ========================================
echo TEST 6: Estado dispositivo
echo ========================================
"%CURL_EXE%" -s %SERVER_URL%/api/esp32/estado/%DEVICE_ID%
echo.
echo.

echo ========================================
echo TEST 7: Enviar comando
echo ========================================
set "BODY={\"command\":\"eolica\",\"parameter\":\"on\"}"
"%CURL_EXE%" -v -X POST "%SERVER_URL%/api/esp32/command/%DEVICE_ID%" -H "Content-Type: application/json" -d "%BODY%"
echo.
echo.

echo ========================================
echo FIN DE TESTS
echo ========================================
pause
