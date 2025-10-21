@echo off
echo ================================================
echo   PREPARAR FIRMWARE PARA ARDUINO IDE 2.0
echo ================================================
echo.

REM Crear config.h si no existe
if not exist "include\config.h" (
    echo [1/3] Copiando config.h...
    copy include\config.h.example include\config.h
    echo    Edita include\config.h con tus credenciales WiFi
) else (
    echo [1/3] config.h ya existe
)

echo.
echo [2/3] Creando archivo .ino para Arduino IDE...

REM Crear carpeta para Arduino
if not exist "main_modular" mkdir main_modular

REM Copiar y renombrar main.cpp a .ino
copy src\main_modular.cpp main_modular\main_modular.ino >nul

echo    Creado: main_modular\main_modular.ino
echo.
echo [3/3] Copiando headers...

REM Copiar archivos .h a la carpeta del sketch
copy include\*.h main_modular\ >nul

echo    Headers copiados a main_modular\
echo.
echo ================================================
echo   LISTO PARA ARDUINO IDE 2.0
echo ================================================
echo.
echo Ahora:
echo   1. Abre Arduino IDE 2.0
echo   2. File -^> Open -^> firmware\main_modular\main_modular.ino
echo   3. Edita config.h con tu WiFi (pestana en IDE)
echo   4. Tools -^> Board -^> ESP32 Dev Module
echo   5. Upload
echo.
pause
