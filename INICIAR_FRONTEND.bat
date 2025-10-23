@echo off
echo ========================================
echo   INICIANDO FRONTEND
echo ========================================
echo.

cd frontend

echo Verificando Node.js...
node --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Node.js no esta instalado
    echo.
    echo Descarga Node.js desde: https://nodejs.org/
    echo Instala la version LTS y reinicia esta terminal
    pause
    exit /b 1
)

echo Node.js: OK
echo.

echo Instalando dependencias (si es necesario)...
if not exist "node_modules" (
    echo Primera vez - instalando paquetes...
    call npm install
)

echo.
echo ========================================
echo   ABRIENDO NAVEGADOR...
echo ========================================
echo.
echo Frontend estara disponible en:
echo   - Local:      http://localhost:3000
echo   - Red local:  http://192.168.0.122:3000
echo.
echo Presiona Ctrl+C para detener el servidor
echo.

call npm start
