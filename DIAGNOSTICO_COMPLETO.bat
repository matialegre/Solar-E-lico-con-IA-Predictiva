@echo off
setlocal ENABLEDELAYEDEXPANSION

echo ========================================
echo   DIAGNOSTICO COMPLETO DEL SISTEMA
echo ========================================
echo.
echo Fecha: %date% %time%
echo.

set "SERVER_URL=http://190.211.201.217:11113"
set "DEVICE_ID=ESP32_INVERSOR_001"
set "CURL_EXE=curl"
if exist "C:\Users\Mundo Outdoor\Downloads\curl-8.16.0_9-win64a-mingw\bin\curl.exe" set "CURL_EXE=C:\Users\Mundo Outdoor\Downloads\curl-8.16.0_9-win64a-mingw\bin\curl.exe"

echo ========================================
echo 1. VERIFICAR PUERTO 11113 ABIERTO
echo ========================================
netstat -ano | findstr :11113
if %ERRORLEVEL% EQU 0 (
    echo [OK] Puerto 11113 está en LISTENING
) else (
    echo [ERROR] Puerto 11113 NO está abierto
    echo        El backend NO está corriendo o no escucha en ese puerto
)
echo.

echo ========================================
echo 2. VERIFICAR REGLA DE FIREWALL
echo ========================================
netsh advfirewall firewall show rule name="Backend ESP32 Port 11113" >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [OK] Regla de firewall existe
    netsh advfirewall firewall show rule name="Backend ESP32 Port 11113" | findstr "Habilitada Acción"
) else (
    echo [ERROR] Regla de firewall NO existe
)
echo.

echo ========================================
echo 3. TEST: HEALTH CHECK (localhost)
echo ========================================
echo Probando: http://localhost:11113/health
echo.
"%CURL_EXE%" -v http://localhost:11113/health
if %ERRORLEVEL% EQU 0 (
    echo.
    echo [OK] Health check localhost funciona
) else (
    echo.
    echo [ERROR] Health check localhost fallo
)
echo.
echo.

echo ========================================
echo 4. TEST: HEALTH CHECK (127.0.0.1)
echo ========================================
echo Probando: http://127.0.0.1:11113/health
echo.
"%CURL_EXE%" -v http://127.0.0.1:11113/health
if %ERRORLEVEL% EQU 0 (
    echo.
    echo [OK] Health check 127.0.0.1 funciona
) else (
    echo.
    echo [ERROR] Health check 127.0.0.1 fallo
)
echo.
echo.

echo ========================================
echo 5. TEST: HEALTH CHECK (IP PÚBLICA)
echo ========================================
echo Probando: %SERVER_URL%/health
echo.
"%CURL_EXE%" -v %SERVER_URL%/health
if %ERRORLEVEL% EQU 0 (
    echo.
    echo [OK] Health check IP pública funciona
) else (
    echo.
    echo [ERROR] Health check IP pública fallo
    echo        Problema de firewall o router
)
echo.
echo.

echo ========================================
echo 6. TEST: LISTAR DISPOSITIVOS ESP32
echo ========================================
echo Probando: %SERVER_URL%/api/esp32/devices
echo.
"%CURL_EXE%" -s %SERVER_URL%/api/esp32/devices
echo.
echo.

echo ========================================
echo 7. TEST: ESTADO DE UN DISPOSITIVO
echo ========================================
echo Probando: %SERVER_URL%/api/esp32/estado/%DEVICE_ID%
echo.
"%CURL_EXE%" -s %SERVER_URL%/api/esp32/estado/%DEVICE_ID%
echo.
echo.

echo ========================================
echo 8. TEST: ENVIAR COMANDO DE PRUEBA
echo ========================================
echo Enviando comando: eolica on
echo URL: %SERVER_URL%/api/esp32/command/%DEVICE_ID%
echo.

set "BODY={\"command\":\"eolica\",\"parameter\":\"on\"}"
"%CURL_EXE%" -v -X POST "%SERVER_URL%/api/esp32/command/%DEVICE_ID%" -H "Content-Type: application/json" -d "%BODY%"

echo.
echo.

echo ========================================
echo 9. INFORMACIÓN DE RED
echo ========================================
echo.
echo Tu IP local:
ipconfig | findstr /C:"Dirección IPv4"
echo.
echo.

echo ========================================
echo 10. VERIFICAR CONEXIONES ACTIVAS
echo ========================================
echo Conexiones al puerto 11113:
netstat -ano | findstr :11113
echo.
echo.

echo ========================================
echo RESUMEN DEL DIAGNÓSTICO
echo ========================================
echo.
echo Si todos los tests pasaron:
echo   [OK] Sistema funcionando correctamente
echo.
echo Si fallo test 1:
echo   [ERROR] Backend no está corriendo - ejecuta: python main.py
echo.
echo Si fallo test 2:
echo   [ERROR] Firewall bloqueando - ejecuta como admin:
echo          netsh advfirewall firewall add rule name="Backend ESP32 Port 11113" dir=in action=allow protocol=TCP localport=11113
echo.
echo Si test 3 y 4 OK pero test 5 falla:
echo   [ERROR] Router no forwarding puerto 11113 a 192.168.0.122
echo.
echo Si test 8 OK:
echo   [OK] Backend recibe comandos correctamente
echo.
echo ========================================
echo FIN DEL DIAGNÓSTICO
echo ========================================
echo.
pause
