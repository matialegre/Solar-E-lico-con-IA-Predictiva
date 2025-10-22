@echo off
title REINICIO TOTAL DEL SISTEMA
color 0A
cls

echo.
echo ================================================
echo   REINICIO TOTAL - LIMPIEZA COMPLETA
echo ================================================
echo.

REM ===== PASO 1: MATAR TODOS LOS PROCESOS =====
echo [1/5] Deteniendo TODOS los procesos...
taskkill /F /IM node.exe 2>nul
taskkill /F /IM python.exe 2>nul
taskkill /F /IM ngrok.exe 2>nul
taskkill /F /IM chrome.exe 2>nul
timeout /t 2 /nobreak >nul
echo    ✅ Procesos detenidos

REM ===== PASO 2: LIMPIAR PUERTOS =====
echo.
echo [2/5] Liberando puertos 11112 y 11113...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :11112') do taskkill /F /PID %%a 2>nul
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :11113') do taskkill /F /PID %%a 2>nul
timeout /t 2 /nobreak >nul
echo    ✅ Puertos liberados

REM ===== PASO 3: LIMPIAR CACHE =====
echo.
echo [3/5] Limpiando cache y archivos temporales...
cd backend
if exist __pycache__ rd /s /q __pycache__
if exist .pytest_cache rd /s /q .pytest_cache
cd ..
cd frontend
if exist node_modules\.cache rd /s /q node_modules\.cache
cd ..
timeout /t 1 /nobreak >nul
echo    ✅ Cache limpiado

REM ===== PASO 4: INICIAR BACKEND =====
echo.
echo [4/5] Iniciando Backend (puerto 11112)...
echo    URL: http://190.211.201.217:11112
start "Backend HTTP" /MIN cmd /c "cd backend && python -m uvicorn main:app --host 0.0.0.0 --port 11112 --reload"
timeout /t 8 /nobreak >nul
echo    ✅ Backend iniciado

REM ===== PASO 5: INICIAR FRONTEND =====
echo.
echo [5/5] Iniciando Frontend (puerto 11113)...
echo    URL: http://190.211.201.217:11113
cd frontend
set PORT=11113
set BROWSER=none
start "Frontend HTTP" /MIN cmd /c "npm start"
cd ..
timeout /t 12 /nobreak >nul
echo    ✅ Frontend iniciado

REM ===== RESUMEN =====
echo.
echo ================================================
echo   ✅ SISTEMA COMPLETAMENTE REINICIADO
echo ================================================
echo.
echo   📡 Backend:  http://190.211.201.217:11112
echo                http://localhost:11112/docs
echo.
echo   🎨 Frontend: http://190.211.201.217:11113
echo                http://localhost:11113
echo.
echo   🔌 ESP32:    Conectándose automáticamente...
echo.
echo   ⚠️  SIN NGROK - Solo HTTP local/red
echo.
echo ================================================
echo.

REM ===== ABRIR NAVEGADOR =====
timeout /t 3 /nobreak >nul
start http://190.211.201.217:11113

echo.
echo   Sistema corriendo. Para detener: DETENER.bat
echo.
echo   Presiona cualquier tecla para cerrar esta ventana
echo   (El sistema seguirá corriendo en background)
echo.
pause >nul
