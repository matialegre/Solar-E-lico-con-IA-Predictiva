@echo off
title Configuracion del Sistema Hibrido
color 0B
cls

echo.
echo ========================================================================
echo   CONFIGURACION DEL SISTEMA INVERSOR HIBRIDO
echo ========================================================================
echo.
echo Este asistente te ayudara a configurar tu sistema personalizado.
echo.
echo Necesitaras saber:
echo   - Tu ubicacion (latitud y longitud)
echo   - Consumo promedio de tu casa (kWh/dia o Watts)
echo   - Presupuesto aproximado
echo.
echo ========================================================================
echo.
pause

REM Ir al directorio del proyecto
cd /d "%~dp0"

echo.
echo Iniciando configurador interactivo...
echo.

REM Ejecutar el script de Python
python backend\configurador.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================================================
    echo   CONFIGURACION COMPLETADA!
    echo ========================================================================
    echo.
    echo Tu configuracion fue guardada en: configuracion_usuario.json
    echo.
    echo Proximos pasos:
    echo   1. Revisa el archivo configuracion_usuario.json
    echo   2. Ejecuta INICIAR_TODO.bat para arrancar el sistema
    echo   3. El sistema usara tu configuracion personalizada
    echo.
) else (
    echo.
    echo ========================================================================
    echo   ERROR EN LA CONFIGURACION
    echo ========================================================================
    echo.
    echo Hubo un problema al configurar el sistema.
    echo Revisa los errores mostrados arriba.
    echo.
)

pause
