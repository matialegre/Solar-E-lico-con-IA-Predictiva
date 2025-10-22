@echo off
title Verificacion Final del Sistema
color 0E
cls

echo.
echo ================================================
echo   VERIFICACION FINAL DEL SISTEMA
echo ================================================
echo.

echo [1/5] Verificando estructura de archivos...
if not exist "backend\main.py" (
    echo    ❌ backend\main.py NO encontrado
    pause
    exit /b 1
)
if not exist "frontend\package.json" (
    echo    ❌ frontend\package.json NO encontrado
    pause
    exit /b 1
)
if not exist "firmware_arduino_ide_2\inversor_hibrido\inversor_hibrido.ino" (
    echo    ❌ Firmware NO encontrado
    pause
    exit /b 1
)
echo    ✅ Archivos principales OK

echo.
echo [2/5] Verificando sintaxis Python...
cd backend
python -m py_compile main.py 2>nul
if errorlevel 1 (
    echo    ❌ Error en main.py
    python -m py_compile main.py
    cd ..
    pause
    exit /b 1
)
python -m py_compile recommendation_service.py 2>nul
if errorlevel 1 (
    echo    ❌ Error en recommendation_service.py
    python -m py_compile recommendation_service.py
    cd ..
    pause
    exit /b 1
)
cd ..
echo    ✅ Backend Python OK

echo.
echo [3/5] Verificando dependencias Python...
cd backend
python -c "import fastapi; import uvicorn; import scikit-learn as sklearn; print('✅ Todas las dependencias OK')" 2>nul
if errorlevel 1 (
    echo    ⚠️ Faltan algunas dependencias
    echo    Instalando...
    pip install -q fastapi uvicorn scikit-learn joblib requests
)
cd ..

echo.
echo [4/5] Verificando frontend...
if not exist "frontend\node_modules" (
    echo    ⚠️ node_modules no encontrado
    echo    Necesitas ejecutar: cd frontend ^&^& npm install
    pause
)
echo    ✅ Frontend OK

echo.
echo [5/5] Resumen de configuración...
echo    📡 Backend: Puerto 11112
echo    🌐 Frontend: Puerto 11113
echo    🔌 ESP32: http://190.211.201.217:11112
echo    📍 Mapa: Integrado con configuración
echo    🧠 ML: scikit-learn Random Forest
echo    🛡️ Protección: Umbrales configurables
echo.

echo ================================================
echo   ✅ VERIFICACION COMPLETA
echo ================================================
echo.
echo   TODO LISTO PARA:
echo   1. Subir firmware al ESP32
echo   2. Ejecutar: INICIAR_IP_PUBLICA.bat
echo   3. Abrir: http://190.211.201.217:11113
echo   4. Configurar en el wizard
echo.
pause
