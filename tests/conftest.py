"""
Configuración de pytest para tests
"""

import pytest
import tempfile
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from src.api_franquicias.main import app
from src.api_franquicias.database import get_db
from src.api_franquicias.models.base import Base


# Crear base de datos temporal para tests
@pytest.fixture(scope="session")
def test_db():
    """Crear base de datos temporal para tests"""
    # Crear archivo temporal
    db_fd, db_path = tempfile.mkstemp()
    
    # Configurar base de datos de test
    SQLALCHEMY_DATABASE_URL = f"sqlite:///{db_path}"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Crear tablas
    Base.metadata.create_all(bind=engine)
    
    yield TestingSessionLocal
    
    # Limpiar
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture(scope="function")
def db_session(test_db):
    """Crear sesión de base de datos para cada test"""
    session = test_db()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(scope="function")
def client(db_session):
    """Crear cliente de test para FastAPI"""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()


@pytest.fixture
def sample_franquicia_data():
    """Datos de ejemplo para franquicia"""
    return {"nombre": "Franquicia de Prueba"}


@pytest.fixture
def sample_sucursal_data():
    """Datos de ejemplo para sucursal"""
    return {"nombre": "Sucursal de Prueba"}


@pytest.fixture
def sample_producto_data():
    """Datos de ejemplo para producto"""
    return {"nombre": "Producto de Prueba", "cantidad_stock": 100}
