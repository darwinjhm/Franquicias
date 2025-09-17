"""
Configuración de la base de datos para el sistema de franquicias
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from .models.base import Base
from .models import Franquicia, Sucursal, Producto

# Configuración de la base de datos
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./franquicias.db")

# Configuración especial para SQLite
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
else:
    engine = create_engine(DATABASE_URL)

# Crear sesión de base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_tables():
    """Crea todas las tablas en la base de datos"""
    Base.metadata.create_all(bind=engine)


def get_db():
    """
    Dependency que proporciona una sesión de base de datos.
    Se usa como dependency en FastAPI.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Inicializa la base de datos con datos de ejemplo"""
    create_tables()
    
    # Solo agregar datos de ejemplo si no existen
    db = SessionLocal()
    try:
        # Verificar si ya hay datos
        if db.query(Franquicia).first() is None:
            # Crear franquicia de ejemplo
            franquicia_ejemplo = Franquicia(nombre="Franquicia de Ejemplo")
            db.add(franquicia_ejemplo)
            db.commit()
            db.refresh(franquicia_ejemplo)
            
            # Crear sucursal de ejemplo
            sucursal_ejemplo = Sucursal(
                nombre="Sucursal Centro",
                franquicia_id=franquicia_ejemplo.id
            )
            db.add(sucursal_ejemplo)
            db.commit()
            db.refresh(sucursal_ejemplo)
            
            # Crear productos de ejemplo
            productos_ejemplo = [
                Producto(nombre="Hamburguesa Clásica", cantidad_stock=50, sucursal_id=sucursal_ejemplo.id),
                Producto(nombre="Papas Fritas", cantidad_stock=100, sucursal_id=sucursal_ejemplo.id),
                Producto(nombre="Refresco", cantidad_stock=75, sucursal_id=sucursal_ejemplo.id),
            ]
            
            for producto in productos_ejemplo:
                db.add(producto)
            
            db.commit()
            print("Base de datos inicializada con datos de ejemplo")
    finally:
        db.close()
