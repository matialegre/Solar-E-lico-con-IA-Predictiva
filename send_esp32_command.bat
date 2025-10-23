@echo off
setlocal ENABLEDELAYEDEXPANSION

:: Defaults (can be overridden by args 3 and 4)
set "SERVER_URL=http://190.211.201.217:11113"
set "DEVICE_ID=ESP32_INVERSOR_001"

:: Args
:: %1 = command (eolica|solar|red|carga|freno|reboot|...)
:: %2 = parameter (on|off|1|0|optional)
:: %3 = device_id (optional)
:: %4 = server_url (optional)

if "%~1"=="" (
  echo Uso:
  echo   %~nx0 ^<command^> ^<parameter^> [device_id] [server_url]
  echo.
  echo Ejemplos:
  echo   %~nx0 eolica on
  echo   %~nx0 eolica off ESP32_INVERSOR_001 http://190.211.201.217:11113
  echo   %~nx0 reboot
  exit /b 1
)

set "COMMAND=%~1"
set "PARAM=%~2"
if not "%~3"=="" set "DEVICE_ID=%~3"
if not "%~4"=="" set "SERVER_URL=%~4"

:: Locate curl: prefer user's downloaded curl.exe, fallback to system curl
set "CURL_EXE=curl"
if exist "C:\Users\Mundo Outdoor\Downloads\curl-8.16.0_9-win64a-mingw\bin\curl.exe" set "CURL_EXE=C:\Users\Mundo Outdoor\Downloads\curl-8.16.0_9-win64a-mingw\bin\curl.exe"

set "URL=%SERVER_URL%/api/esp32/command/%DEVICE_ID%"

:: Build JSON body (keep escaped quotes for JSON)
if "%PARAM%"=="" (
  set "BODY={\"command\":\"%COMMAND%\"}"
) else (
  set "BODY={\"command\":\"%COMMAND%\",\"parameter\":\"%PARAM%\"}"
)

echo.
echo ========================================
echo   ENVIANDO COMANDO AL BACKEND
echo ========================================
echo URL: %URL%
echo Comando: %COMMAND% %PARAM%
echo.

:: Enviar comando y capturar respuesta con command_id
set "RESPONSE_FILE=%TEMP%\esp32_response.json"
"%CURL_EXE%" -s -X POST "%URL%" -H "Content-Type: application/json" -d "%BODY%" > "%RESPONSE_FILE%"

:: Mostrar respuesta
type "%RESPONSE_FILE%"
echo.

:: Extraer command_id usando PowerShell (más confiable que findstr)
for /f "delims=" %%i in ('powershell -Command "$json = Get-Content '%RESPONSE_FILE%' | ConvertFrom-Json; $json.command_id"') do set "COMMAND_ID=%%i"

if "%COMMAND_ID%"=="" (
  echo.
  echo [ERROR] No se pudo obtener command_id del backend
  echo La respuesta fue:
  type "%RESPONSE_FILE%"
  del "%RESPONSE_FILE%" 2>nul
  exit /b 1
)

echo.
echo ========================================
echo   ESPERANDO CONFIRMACION (ACK)...
echo ========================================
echo Command ID: %COMMAND_ID%
echo.

:: Esperar hasta 10 segundos por ACK
set /a TIMEOUT_SECONDS=10
set /a COUNTER=0

:WAIT_LOOP
if %COUNTER% GEQ %TIMEOUT_SECONDS% goto TIMEOUT

timeout /t 1 /nobreak >nul
set /a COUNTER+=1

echo [%COUNTER%/%TIMEOUT_SECONDS%] Consultando estado...

:: Consultar estado del comando
set "STATUS_URL=%SERVER_URL%/api/esp32/command/%DEVICE_ID%/status/%COMMAND_ID%"
set "STATUS_FILE=%TEMP%\esp32_status.json"
"%CURL_EXE%" -s "%STATUS_URL%" > "%STATUS_FILE%"

:: Extraer status usando PowerShell
for /f "delims=" %%i in ('powershell -Command "$json = Get-Content '%STATUS_FILE%' 2>$null | ConvertFrom-Json; if($json.status) { $json.status } else { 'error' }"') do set "CMD_STATUS=%%i"

if "%CMD_STATUS%"=="acked" (
  echo.
  echo ========================================
  echo   [EXITO] COMANDO CONFIRMADO!
  echo ========================================
  echo.
  echo El ESP32 ejecuto el comando correctamente.
  echo Estado: %CMD_STATUS%
  echo.
  
  :: Mostrar estado actualizado del ESP32
  echo Estado actual del dispositivo:
  "%CURL_EXE%" -s "%SERVER_URL%/api/esp32/estado/%DEVICE_ID%" | powershell -Command "$json = $input | ConvertFrom-Json; Write-Host 'Reles:'; $json.relays | Format-List; Write-Host 'Telemetria:'; $json.telemetry | Format-List"
  
  del "%RESPONSE_FILE%" 2>nul
  del "%STATUS_FILE%" 2>nul
  exit /b 0
)

if "%CMD_STATUS%"=="sent" (
  echo Estado: Enviado, esperando ejecucion...
  goto WAIT_LOOP
)

if "%CMD_STATUS%"=="pending" (
  echo Estado: Pendiente (ESP32 no conectado?)
  goto WAIT_LOOP
)

:: Si llegamos aquí, hubo un error
echo [ADVERTENCIA] Estado: %CMD_STATUS%
goto WAIT_LOOP

:TIMEOUT
echo.
echo ========================================
echo   [TIMEOUT] NO SE RECIBIO CONFIRMACION
echo ========================================
echo.
echo El comando fue enviado pero no se confirmo en %TIMEOUT_SECONDS% segundos.
echo.
echo Posibles causas:
echo  - ESP32 no esta conectado por WebSocket
echo  - ESP32 perdio WiFi
echo  - Comando invalido
echo.
echo Estado final: %CMD_STATUS%
echo.
del "%RESPONSE_FILE%" 2>nul
del "%STATUS_FILE%" 2>nul
exit /b 1
