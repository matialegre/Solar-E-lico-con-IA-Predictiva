@echo off
echo ========================================
echo   LIMPIANDO CACHE Y REINICIANDO
echo ========================================
echo.

REM Ir al directorio del proyecto
cd /d "%~dp0"

echo [1/5] Deteniendo procesos...
taskkill /F /IM node.exe 2>nul
taskkill /F /IM python.exe 2>nul
timeout /t 2 /nobreak >nul

echo [2/5] Limpiando cache de npm...
cd frontend
if exist node_modules\.cache (
    rmdir /s /q node_modules\.cache
    echo Cache de npm eliminado
) else (
    echo No habia cache de npm
)

echo [3/5] Limpiando build...
if exist build (
    rmdir /s /q build
    echo Build eliminado
)

echo [4/5] Esperando 3 segundos...
timeout /t 3 /nobreak >nul

echo [5/5] Reiniciando todo...
cd ..
call INICIAR_TODO.bat

echo.
echo ========================================
echo   REINICIO COMPLETO
echo ========================================
echo.
echo IMPORTANTE: 
echo 1. Espera a que ambos servidores arranquen
echo 2. En el navegador presiona Ctrl+Shift+R
echo    (hard refresh para limpiar cache del navegador)
echo.
pause
