@echo off
chcp 65001 >nul
cls
echo ╔═══════════════════════════════════════════════════════════════╗
echo ║  🎯 PRUEBA RÁPIDA RPM - Sistema Inversor Híbrido            ║
echo ╚═══════════════════════════════════════════════════════════════╝
echo.
echo Este script probará el RPM en 3 pasos:
echo.
echo 1️⃣  Ejecuta el backend (si no está corriendo)
echo 2️⃣  Ejecuta el simulador ESP32
echo 3️⃣  Abre el frontend automáticamente
echo.
echo ═══════════════════════════════════════════════════════════════
echo.

echo 🔍 Verificando si el backend está corriendo...
timeout /t 2 >nul

curl -s http://localhost:11113/docs >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Backend NO está corriendo
    echo.
    echo 🚀 Iniciando backend...
    start "Backend ESP32" cmd /k "cd backend && uvicorn main:app --host 0.0.0.0 --port 11113"
    echo ⏳ Esperando 5 segundos para que el backend inicie...
    timeout /t 5 >nul
) else (
    echo ✅ Backend ya está corriendo
)

echo.
echo 🚀 Iniciando simulador ESP32 con RPM...
echo.
echo ═══════════════════════════════════════════════════════════════
echo   VALORES QUE VERÁS:
echo   • RPM: 150-400 RPM (aleatorio pero SIEMPRE visible)
echo   • Frecuencia: 25-65 Hz
echo   • ADCs: Valores estables
echo ═══════════════════════════════════════════════════════════════
echo.
timeout /t 2 >nul

start "Simulador ESP32" cmd /k "python simulador_esp32_completo.py"

echo.
echo ⏳ Esperando 3 segundos para que envíe datos...
timeout /t 3 >nul

echo.
echo 🌐 Abriendo frontend en el navegador...
start http://localhost:3000

echo.
echo ═══════════════════════════════════════════════════════════════
echo   ✅ TODO INICIADO
echo ═══════════════════════════════════════════════════════════════
echo.
echo 📋 Qué hacer ahora:
echo.
echo 1. Ve al navegador que se abrió
echo 2. Haz clic en "Dispositivos" o "Monitor ESP32"
echo 3. Busca la TARJETA MORADA/ROSA arriba de los ADCs
echo 4. Deberías ver:
echo    🎯 RPM Turbina Eólica: XXX RPM
echo    📊 Frecuencia: XX.XX Hz
echo.
echo 💡 Los valores cambian cada 2 segundos
echo.
echo ⌨️  Para detener: Cierra las ventanas del simulador y backend
echo.
echo ═══════════════════════════════════════════════════════════════
pause
