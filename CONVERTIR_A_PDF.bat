@echo off
title Convertir Manual a PDF
color 0A
cls

echo.
echo ================================================
echo    CONVERTIR MANUAL TECNICO A PDF
echo ================================================
echo.
echo Este script convierte los archivos Markdown
echo del manual tecnico a un PDF completo.
echo.
echo Archivos a convertir:
echo   - MANUAL_COMPLETO_PARTE_1.md
echo   - MANUAL_COMPLETO_PARTE_2.md
echo   - MANUAL_COMPLETO_PARTE_3.md (cuando este)
echo   - MANUAL_COMPLETO_PARTE_4.md (cuando este)
echo   - MANUAL_COMPLETO_PARTE_5.md (cuando este)
echo.
echo ================================================
echo.

echo Verificando si Pandoc esta instalado...
where pandoc >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Pandoc no esta instalado.
    echo.
    echo Para instalar Pandoc:
    echo   1. Descarga desde: https://pandoc.org/installing.html
    echo   2. O instala con Chocolatey: choco install pandoc
    echo   3. Reinicia la terminal
    echo.
    pause
    exit /b 1
)

echo [OK] Pandoc encontrado
echo.

echo Convirtiendo archivos a PDF...
echo.

REM Combinar todos los archivos MD en uno solo
type MANUAL_COMPLETO_PARTE_1.md > MANUAL_TECNICO_COMPLETO_TEMP.md
if exist MANUAL_COMPLETO_PARTE_2.md type MANUAL_COMPLETO_PARTE_2.md >> MANUAL_TECNICO_COMPLETO_TEMP.md
if exist MANUAL_COMPLETO_PARTE_3.md type MANUAL_COMPLETO_PARTE_3.md >> MANUAL_TECNICO_COMPLETO_TEMP.md
if exist MANUAL_COMPLETO_PARTE_4.md type MANUAL_COMPLETO_PARTE_4.md >> MANUAL_TECNICO_COMPLETO_TEMP.md
if exist MANUAL_COMPLETO_PARTE_5.md type MANUAL_COMPLETO_PARTE_5.md >> MANUAL_TECNICO_COMPLETO_TEMP.md

echo Generando PDF...
pandoc MANUAL_TECNICO_COMPLETO_TEMP.md ^
    -o "MANUAL_TECNICO_SISTEMA_HIBRIDO.pdf" ^
    --pdf-engine=xelatex ^
    --toc ^
    --toc-depth=3 ^
    -V geometry:margin=2cm ^
    -V fontsize=11pt ^
    -V documentclass=article ^
    -V lang=es ^
    --highlight-style=tango

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ================================================
    echo    [EXITO] PDF GENERADO
    echo ================================================
    echo.
    echo Archivo creado: MANUAL_TECNICO_SISTEMA_HIBRIDO.pdf
    echo.
    
    REM Limpiar archivo temporal
    del MANUAL_TECNICO_COMPLETO_TEMP.md
    
    REM Abrir PDF
    start MANUAL_TECNICO_SISTEMA_HIBRIDO.pdf
) else (
    echo.
    echo [ERROR] No se pudo generar el PDF
    echo.
    echo Posibles causas:
    echo   - Falta LaTeX (necesario para PDF)
    echo   - Instalar MiKTeX: https://miktex.org/download
    echo   - O usar: pandoc file.md -o file.docx (genera Word)
    echo.
)

echo.
pause
