@echo off
echo ========================================
echo   PRUEBA DE CONTROL DE RELES ESP32
echo ========================================
echo.

:menu
echo Seleccione una accion:
echo.
echo === PANEL SOLAR ===
echo 1. Encender Panel Solar
echo 2. Apagar Panel Solar
echo.
echo === EOLICA ===
echo 3. Encender Eolica
echo 4. Apagar Eolica
echo.
echo === RED BACKUP ===
echo 5. Encender Red Backup
echo 6. Apagar Red Backup
echo.
echo === CARGA ===
echo 7. Encender Carga
echo 8. Apagar Carga
echo.
echo === EMERGENCIA ===
echo 9. APAGAR TODO
echo.
echo 0. Salir
echo.

set /p opcion="Ingrese numero (0-9): "

if "%opcion%"=="1" (
    echo.
    echo Encendiendo Panel Solar...
    call send_esp32_command.bat solar on
    goto espera
)
if "%opcion%"=="2" (
    echo.
    echo Apagando Panel Solar...
    call send_esp32_command.bat solar off
    goto espera
)
if "%opcion%"=="3" (
    echo.
    echo Encendiendo Eolica...
    call send_esp32_command.bat eolica on
    goto espera
)
if "%opcion%"=="4" (
    echo.
    echo Apagando Eolica...
    call send_esp32_command.bat eolica off
    goto espera
)
if "%opcion%"=="5" (
    echo.
    echo Encendiendo Red Backup...
    call send_esp32_command.bat red on
    goto espera
)
if "%opcion%"=="6" (
    echo.
    echo Apagando Red Backup...
    call send_esp32_command.bat red off
    goto espera
)
if "%opcion%"=="7" (
    echo.
    echo Encendiendo Carga...
    call send_esp32_command.bat carga on
    goto espera
)
if "%opcion%"=="8" (
    echo.
    echo Apagando Carga...
    call send_esp32_command.bat carga off
    goto espera
)
if "%opcion%"=="9" (
    echo.
    echo *** APAGANDO TODOS LOS RELES ***
    call send_esp32_command.bat apagar_todo
    goto espera
)
if "%opcion%"=="0" (
    echo.
    echo Saliendo...
    exit /b 0
)

echo Opcion invalida
pause
goto menu

:espera
echo.
echo *** Espere 2 segundos para que el ESP reciba el comando ***
timeout /t 2 /nobreak >nul
echo.
pause
cls
goto menu
