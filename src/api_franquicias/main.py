"""
Aplicación principal FastAPI para el sistema de gestión de franquicias
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import uvicorn
import os

from .config import settings
from .database import init_db
from .controllers.franquicia_controller import router as franquicia_router
from .controllers.sucursal_controller import router as sucursal_router
from .controllers.producto_controller import router as producto_router
from .controllers.franquicia_sucursal_controller import router as franquicia_sucursal_router
from .controllers.sucursal_producto_controller import router as sucursal_producto_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gestión del ciclo de vida de la aplicación.
    Inicializa la base de datos al arrancar la aplicación.
    """
    # Inicializar base de datos
    init_db()
    yield


# Crear aplicación FastAPI
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=settings.app_description,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=settings.cors_methods,
    allow_headers=settings.cors_headers,
)


# Incluir routers
app.include_router(franquicia_router)
app.include_router(sucursal_router)
app.include_router(producto_router)
app.include_router(franquicia_sucursal_router)
app.include_router(sucursal_producto_router)


@app.get("/", tags=["root"])
async def root():
    """
    Endpoint raíz que proporciona información básica de la API.
    """
    return {
        "message": "API de Gestión de Franquicias",
        "version": settings.app_version,
        "description": settings.app_description,
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health", tags=["health"])
async def health_check():
    """
    Endpoint de verificación de salud de la API.
    """
    return {
        "status": "healthy",
        "version": settings.app_version,
        "database": "connected"
    }


@app.exception_handler(404)
async def not_found_handler(request, exc):
    """
    Manejador personalizado para errores 404.
    """
    return JSONResponse(
        status_code=404,
        content={
            "error": "Not Found",
            "detail": "El recurso solicitado no fue encontrado",
            "path": str(request.url.path)
        }
    )


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    """
    Manejador personalizado para errores 500.
    """
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "detail": "Ha ocurrido un error interno del servidor"
        }
    )


def main():
    """
    Función principal para ejecutar la aplicación.
    """
    uvicorn.run(
        "api_franquicias.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )


if __name__ == "__main__":
    main()
