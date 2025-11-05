@echo off
chcp 65001 >nul
cls
echo ═══════════════════════════════════════════════════════════════
echo   🚀 SIMULADOR ESP32 - Sistema Inversor Híbrido
echo ═══════════════════════════════════════════════════════════════
echo.
echo Este simulador emula un ESP32 real enviando telemetría al backend.
echo.
echo 📊 Incluye:
echo    ✓ 4 ADCs (GPIO34, 35, 36, 39) con nombres corregidos
echo    ✓ RPM de turbina eólica (0-450 RPM)
echo    ✓ Frecuencia eléctrica (0-75 Hz)
echo    ✓ Estados de relés aleatorios
echo    ✓ Valores estables y realistas
echo.
echo ⚠️  IMPORTANTE: El backend debe estar corriendo en el puerto 11113
echo.
echo ═══════════════════════════════════════════════════════════════
echo.
pause
cls

echo 🔍 Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Python no encontrado
    echo.
    echo Por favor instala Python desde: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python encontrado
echo.

echo 📦 Verificando biblioteca 'requests'...
python -c "import requests" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  requests no está instalado. Instalando...
    pip install requests
)

echo.
echo 🚀 Iniciando simulador...
echo.
python simulador_esp32_completo.py

if errorlevel 1 (
    echo.
    echo ❌ Error al ejecutar el simulador
    echo.
    pause
)
