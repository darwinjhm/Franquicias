@echo off
REM Script de testing end-to-end para Windows

echo 🚀 Iniciando tests end-to-end para API de Franquicias
echo ==================================================

REM Verificar que Python esté instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no está instalado
    exit /b 1
)

REM Verificar que la API esté ejecutándose
echo 🔍 Verificando que la API esté ejecutándose...
curl -s http://localhost:8000/health >nul 2>&1
if errorlevel 1 (
    echo ❌ La API no está ejecutándose en http://localhost:8000
    echo 💡 Ejecuta: python -m api_franquicias
    exit /b 1
)

echo ✅ API está ejecutándose

REM Ejecutar tests
echo 🧪 Ejecutando tests end-to-end...
python scripts/test-end-to-end.py --url http://localhost:8000 --wait 2

echo ✅ Tests completados
