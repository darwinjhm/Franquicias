"""
Configuración de la aplicación
"""

import os
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configuración de la aplicación usando Pydantic Settings"""
    
    # Configuración de la aplicación
    app_name: str = "API Franquicias"
    app_version: str = "1.0.0"
    app_description: str = "API REST para gestión de franquicias, sucursales y productos"
    debug: bool = True
    
    # Configuración del servidor
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Configuración de la base de datos
    database_url: str = "sqlite:///./franquicias.db"
    
    # Configuración de logging
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Configuración de CORS
    cors_origins: List[str] = ["http://localhost:3000", "http://localhost:8080"]
    cors_methods: List[str] = ["GET", "POST", "PUT", "DELETE", "PATCH"]
    cors_headers: List[str] = ["*"]
    
    model_config = {
        "env_file": ".env",
        "case_sensitive": False
    }


# Instancia global de configuración
settings = Settings()
