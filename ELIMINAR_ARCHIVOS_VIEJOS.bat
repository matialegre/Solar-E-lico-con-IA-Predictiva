@echo off
echo ================================================
echo    LIMPIEZA DE ARCHIVOS REDUNDANTES
echo ================================================
echo.
echo Este script eliminara archivos .bat, .md y .txt viejos
echo Dejara solo los archivos esenciales
echo.
echo ARCHIVOS A ELIMINAR:
echo   - Todos los .bat viejos (menos INICIAR.bat y DETENER.bat)
echo   - Documentos .md redundantes
echo   - Scripts .py de prueba
echo.
echo Presiona Ctrl+C para CANCELAR
echo O presiona cualquier tecla para CONTINUAR...
pause >nul

echo.
echo Eliminando archivos...

REM Eliminar .bat viejos (mantener solo INICIAR y DETENER)
del /Q BUILD_Y_SERVIR.bat 2>nul
del /Q CONFIGURAR_SISTEMA.bat 2>nul
del /Q configurar_api_key.bat 2>nul
del /Q DETENER_TODO.bat 2>nul
del /Q INICIAR_COMPLETO.bat 2>nul
del /Q INICIAR_RAPIDO.bat 2>nul
del /Q INICIAR_TODO.bat 2>nul
del /Q LIMPIAR_Y_REINICIAR.bat 2>nul
del /Q quick_test.bat 2>nul
del /Q start_all.bat 2>nul
del /Q start_backend.bat 2>nul
del /Q start_completo_ngrok.bat 2>nul
del /Q start_con_puertos.bat 2>nul
del /Q start_con_tu_ngrok.bat 2>nul
del /Q start_frontend.bat 2>nul
del /Q start_ngrok_only.bat 2>nul
del /Q start_simple.bat 2>nul
del /Q start_simulator.bat 2>nul
del /Q start_sin_ngrok.bat 2>nul
del /Q START.bat 2>nul
del /Q START_TODO.bat 2>nul
del /Q start_with_ngrok.bat 2>nul
del /Q STOP.bat 2>nul
del /Q test_backend_manual.bat 2>nul
del /Q verificar_puertos.bat 2>nul
del /Q ver_error_backend.bat 2>nul

REM Eliminar .md redundantes (mantener README.md y esenciales)
del /Q ARQUITECTURA_HTTP_SIN_MQTT.md 2>nul
del /Q CHANGELOG.md 2>nul
del /Q CHECKLIST_IMPLEMENTACION.md 2>nul
del /Q DEPLOY_NGROK.md 2>nul
del /Q ESTRATEGIA_INTELIGENTE.md 2>nul
del /Q GUIA_COMPLETA_INICIO.md 2>nul
del /Q GUIA_CONFIGURACION.md 2>nul
del /Q INSTALACION_CASA_PRUEBA.md 2>nul
del /Q LINE_COUNT.md 2>nul
del /Q MEDICION_CONSUMOS.md 2>nul
del /Q MODO_2_COMPONENTES.md 2>nul
del /Q MONITOR_EFICIENCIA.md 2>nul
del /Q PROJECT_SUMMARY.md 2>nul
del /Q QUICKSTART.md 2>nul
del /Q README_FINAL.md 2>nul
del /Q RESPUESTAS_FINALES.md 2>nul
del /Q RESUMEN_EJECUTIVO.md 2>nul
del /Q RESUMEN_PARA_TI.md 2>nul
del /Q SETUP_RAPIDO.md 2>nul
del /Q SOLUCION_ERROR_404.md 2>nul
del /Q SOLUCION_PROBLEMAS_INMEDIATA.md 2>nul
del /Q STATUS.md 2>nul
del /Q STRUCTURE.txt 2>nul
del /Q TESTING.md 2>nul
del /Q TODO_LISTO.txt 2>nul

REM Eliminar .txt innecesarios
del /Q IMPORTANTE_LEER_PRIMERO.txt 2>nul
del /Q INSTRUCCIONES_NGROK.txt 2>nul

REM Eliminar scripts Python de prueba
del /Q diagnostico.py 2>nul
del /Q start_system.py 2>nul
del /Q stop_system.py 2>nul
del /Q test_api.py 2>nul
del /Q test_completo.py 2>nul

REM Eliminar archivos temporales
del /Q .system_pids.json 2>nul
del /Q configuracion_usuario.json 2>nul

echo.
echo ================================================
echo    LIMPIEZA COMPLETADA
echo ================================================
echo.
echo Archivos eliminados. Ahora tienes una carpeta limpia.
echo.
echo ARCHIVOS ESENCIALES QUE QUEDARON:
echo   - INICIAR.bat       (Iniciar sistema)
echo   - DETENER.bat       (Detener sistema)
echo   - README.md         (Documentacion principal)
echo   - LICENSE           (Licencia)
echo   - simulador_esp32.py (Simulador ESP32)
echo   + carpetas: backend, frontend, firmware
echo.
pause
