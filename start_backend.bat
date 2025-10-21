@echo off
echo ========================================
echo  Iniciando Backend - Inversor Inteligente
echo ========================================
echo.

cd backend

echo Verificando dependencias...
pip install -r requirements.txt --quiet

echo.
echo Iniciando servidor FastAPI...
echo.
echo URL: http://localhost:8000
echo Documentacion: http://localhost:8000/docs
echo.

python main.py

pause
