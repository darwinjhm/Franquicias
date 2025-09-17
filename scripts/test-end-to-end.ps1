# Script de testing end-to-end para Windows PowerShell

Write-Host "🚀 Iniciando tests end-to-end para API de Franquicias" -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Green

# Verificar que Python esté instalado
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python encontrado: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python no está instalado" -ForegroundColor Red
    exit 1
}

# Verificar que la API esté ejecutándose
Write-Host "🔍 Verificando que la API esté ejecutándose..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing -TimeoutSec 5
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ API está ejecutándose" -ForegroundColor Green
    } else {
        throw "API no responde correctamente"
    }
} catch {
    Write-Host "❌ La API no está ejecutándose en http://localhost:8000" -ForegroundColor Red
    Write-Host "💡 Ejecuta: python -m api_franquicias" -ForegroundColor Yellow
    exit 1
}

# Ejecutar tests
Write-Host "🧪 Ejecutando tests end-to-end..." -ForegroundColor Yellow
try {
    python scripts/test-end-to-end.py --url http://localhost:8000 --wait 2
    Write-Host "✅ Tests completados" -ForegroundColor Green
} catch {
    Write-Host "❌ Error al ejecutar tests" -ForegroundColor Red
    exit 1
}
