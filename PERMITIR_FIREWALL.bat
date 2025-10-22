@echo off
title Configurar Firewall para Backend
color 0A

echo.
echo ================================================
echo   PERMITIR BACKEND EN FIREWALL DE WINDOWS
echo ================================================
echo.

echo Permitiendo puerto 11113 (Backend)...
netsh advfirewall firewall add rule name="Backend Inversor - Puerto 11113" dir=in action=allow protocol=TCP localport=11113

echo.
echo Permitiendo puerto 3002 (Frontend)...
netsh advfirewall firewall add rule name="Frontend Inversor - Puerto 3002" dir=in action=allow protocol=TCP localport=3002

echo.
echo ================================================
echo   REGLAS DE FIREWALL AGREGADAS
echo ================================================
echo.
echo Puertos permitidos:
echo   - 11113 (Backend)
echo   - 3002 (Frontend)
echo.
echo El ESP32 ahora deberia poder conectarse
echo.
pause
