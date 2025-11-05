@echo off
echo ============================================================
echo   REINICIAR BACKEND Y VERIFICAR
echo ============================================================
echo.
echo PASO 1: Detener backend anterior (si existe)
echo Presiona Ctrl+C en la ventana del backend
echo.
pause
echo.
echo PASO 2: Iniciando backend...
cd backend
start cmd /k "python main.py"
echo.
echo Esperando 5 segundos a que el backend inicie...
timeout /t 5 /nobreak
echo.
echo ============================================================
echo   BUSCANDO MENSAJE: "VERSIÓN NUEVA - BACKEND REINICIADO"
echo ============================================================
echo.
echo Verifica en la ventana del backend que veas:
echo.
echo   ============================================================
echo   🚀 VERSIÓN NUEVA - BACKEND REINICIADO
echo   ============================================================
echo.
pause
echo.
echo ============================================================
echo   PROBANDO ENDPOINT /api/esp32/devices
echo ============================================================
echo.
cd ..
python test_api_response.py
echo.
echo ============================================================
echo   FIN
echo ============================================================
echo.
echo Si viste:
echo   - "VERSIÓN NUEVA" en el backend
echo   - "CONTADOR" con un número
echo   - "RAW_ADC" con valores (no vacío)
echo.
echo Entonces el backend está funcionando correctamente.
echo.
echo Ahora refresca el frontend (F5 en el navegador)
echo.
pause
