#!/usr/bin/env python3
"""
Servidor de prueba simple para verificar que la API funciona
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn

# Crear aplicación simple
app = FastAPI(title="API Franquicias Test", version="1.0.0")

@app.get("/")
async def root():
    return {"message": "API de Franquicias funcionando", "status": "OK"}

@app.get("/health")
async def health():
    return {"status": "healthy", "message": "API funcionando correctamente"}

@app.get("/test")
async def test():
    return {"test": "success", "message": "Test endpoint funcionando"}

if __name__ == "__main__":
    print("🚀 Iniciando servidor de prueba...")
    print("📡 Servidor disponible en: http://localhost:8000")
    print("📋 Documentación en: http://localhost:8000/docs")
    print("🛑 Presiona Ctrl+C para detener")
    
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
