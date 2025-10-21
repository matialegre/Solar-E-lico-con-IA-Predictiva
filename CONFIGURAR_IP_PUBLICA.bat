@echo off
echo ================================================
echo   CONFIGURAR FRONTEND PARA IP PUBLICA
echo ================================================
echo.
echo Este script configura el frontend para usar tu
echo IP publica en el backend en lugar de localhost
echo.
echo Tu configuracion:
echo   Frontend:  https://argentina.ngrok.pro (ngrok)
echo   Backend:   http://190.211.201.217:11113 (IP publica)
echo.
echo Presiona cualquier tecla para editar...
pause >nul

echo.
echo Abriendo archivo de configuracion del frontend...
echo.
echo CAMBIA esta linea:
echo   REACT_APP_API_URL=http://localhost:8801
echo.
echo POR esta:
echo   REACT_APP_API_URL=http://190.211.201.217:11113
echo.
echo Guarda y cierra el archivo cuando termines.
echo.
pause

notepad frontend\.env

echo.
echo ================================================
echo   AHORA NECESITAS:
echo ================================================
echo.
echo 1. Reiniciar el sistema:
echo    DETENER.bat
echo    INICIAR.bat
echo.
echo 2. Verificar que el puerto 11113 este abierto
echo    en tu router/firewall
echo.
echo 3. Verificar que el backend este escuchando en
echo    0.0.0.0:11113 (no solo localhost)
echo.
pause
