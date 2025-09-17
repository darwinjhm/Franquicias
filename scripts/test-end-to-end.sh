#!/bin/bash
# Script de testing end-to-end para Linux/Mac

set -e

echo "🚀 Iniciando tests end-to-end para API de Franquicias"
echo "=================================================="

# Verificar que Python esté instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 no está instalado"
    exit 1
fi

# Verificar que la API esté ejecutándose
echo "🔍 Verificando que la API esté ejecutándose..."
if ! curl -s http://localhost:8000/health > /dev/null; then
    echo "❌ La API no está ejecutándose en http://localhost:8000"
    echo "💡 Ejecuta: python -m api_franquicias"
    exit 1
fi

echo "✅ API está ejecutándose"

# Ejecutar tests
echo "🧪 Ejecutando tests end-to-end..."
python3 scripts/test-end-to-end.py --url http://localhost:8000 --wait 2

echo "✅ Tests completados"
