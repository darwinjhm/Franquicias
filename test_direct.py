#!/usr/bin/env python3
"""
Test directo de la funcionalidad sin servidor
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test que todos los módulos se pueden importar"""
    print("🧪 Probando imports de módulos...")
    
    try:
        from api_franquicias.models import Franquicia, Sucursal, Producto, Base
        print("✅ Modelos importados correctamente")
    except Exception as e:
        print(f"❌ Error importando modelos: {e}")
        return False
    
    try:
        from api_franquicias.database import create_tables, get_db
        print("✅ Base de datos importada correctamente")
    except Exception as e:
        print(f"❌ Error importando base de datos: {e}")
        return False
    
    try:
        from api_franquicias.repositories import FranquiciaRepository, SucursalRepository, ProductoRepository
        print("✅ Repositorios importados correctamente")
    except Exception as e:
        print(f"❌ Error importando repositorios: {e}")
        return False
    
    try:
        from api_franquicias.services import FranquiciaService, SucursalService, ProductoService
        print("✅ Servicios importados correctamente")
    except Exception as e:
        print(f"❌ Error importando servicios: {e}")
        return False
    
    try:
        from api_franquicias.schemas import FranquiciaCreate, FranquiciaResponse, SucursalCreate, ProductoCreate
        print("✅ Esquemas importados correctamente")
    except Exception as e:
        print(f"❌ Error importando esquemas: {e}")
        return False
    
    return True

def test_models():
    """Test de creación de modelos"""
    print("\n🧪 Probando creación de modelos...")
    
    try:
        from api_franquicias.models import Franquicia, Sucursal, Producto
        
        # Crear franquicia
        franquicia = Franquicia(nombre="Franquicia Test")
        assert franquicia.nombre == "Franquicia Test"
        print("✅ Modelo Franquicia creado correctamente")
        
        # Crear sucursal
        sucursal = Sucursal(nombre="Sucursal Test", franquicia_id=1)
        assert sucursal.nombre == "Sucursal Test"
        assert sucursal.franquicia_id == 1
        print("✅ Modelo Sucursal creado correctamente")
        
        # Crear producto
        producto = Producto(nombre="Producto Test", cantidad_stock=100, sucursal_id=1)
        assert producto.nombre == "Producto Test"
        assert producto.cantidad_stock == 100
        assert producto.sucursal_id == 1
        print("✅ Modelo Producto creado correctamente")
        
        return True
    except Exception as e:
        print(f"❌ Error creando modelos: {e}")
        return False

def test_schemas():
    """Test de esquemas Pydantic"""
    print("\n🧪 Probando esquemas Pydantic...")
    
    try:
        from api_franquicias.schemas import FranquiciaCreate, FranquiciaResponse, SucursalCreate, ProductoCreate
        
        # Test FranquiciaCreate
        franquicia_data = FranquiciaCreate(nombre="Franquicia Schema Test")
        assert franquicia_data.nombre == "Franquicia Schema Test"
        print("✅ FranquiciaCreate funciona correctamente")
        
        # Test SucursalCreate
        sucursal_data = SucursalCreate(nombre="Sucursal Schema Test")
        assert sucursal_data.nombre == "Sucursal Schema Test"
        print("✅ SucursalCreate funciona correctamente")
        
        # Test ProductoCreate
        producto_data = ProductoCreate(nombre="Producto Schema Test", cantidad_stock=50)
        assert producto_data.nombre == "Producto Schema Test"
        assert producto_data.cantidad_stock == 50
        print("✅ ProductoCreate funciona correctamente")
        
        return True
    except Exception as e:
        print(f"❌ Error probando esquemas: {e}")
        return False

def test_database_creation():
    """Test de creación de base de datos"""
    print("\n🧪 Probando creación de base de datos...")
    
    try:
        from api_franquicias.database import create_tables
        from api_franquicias.models.base import Base
        from sqlalchemy import create_engine
        
        # Crear base de datos en memoria
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(bind=engine)
        print("✅ Base de datos creada correctamente")
        
        return True
    except Exception as e:
        print(f"❌ Error creando base de datos: {e}")
        return False

def test_repositories():
    """Test de repositorios"""
    print("\n🧪 Probando repositorios...")
    
    try:
        from api_franquicias.repositories import FranquiciaRepository, SucursalRepository, ProductoRepository
        from api_franquicias.database import SessionLocal
        from api_franquicias.models.base import Base
        from sqlalchemy import create_engine
        
        # Crear base de datos en memoria
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(bind=engine)
        
        # Crear sesión
        SessionLocal.configure(bind=engine)
        db = SessionLocal()
        
        # Test FranquiciaRepository
        franquicia_repo = FranquiciaRepository(db)
        franquicia = franquicia_repo.create("Franquicia Repo Test")
        assert franquicia.nombre == "Franquicia Repo Test"
        print("✅ FranquiciaRepository funciona correctamente")
        
        # Test SucursalRepository
        sucursal_repo = SucursalRepository(db)
        sucursal = sucursal_repo.create("Sucursal Repo Test", franquicia.id)
        assert sucursal.nombre == "Sucursal Repo Test"
        assert sucursal.franquicia_id == franquicia.id
        print("✅ SucursalRepository funciona correctamente")
        
        # Test ProductoRepository
        producto_repo = ProductoRepository(db)
        producto = producto_repo.create("Producto Repo Test", 100, sucursal.id)
        assert producto.nombre == "Producto Repo Test"
        assert producto.cantidad_stock == 100
        assert producto.sucursal_id == sucursal.id
        print("✅ ProductoRepository funciona correctamente")
        
        db.close()
        return True
    except Exception as e:
        print(f"❌ Error probando repositorios: {e}")
        return False

def test_services():
    """Test de servicios"""
    print("\n🧪 Probando servicios...")
    
    try:
        from api_franquicias.services import FranquiciaService, SucursalService, ProductoService
        from api_franquicias.database import SessionLocal
        from api_franquicias.models.base import Base
        from sqlalchemy import create_engine
        
        # Crear base de datos en memoria
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(bind=engine)
        
        # Crear sesión
        SessionLocal.configure(bind=engine)
        db = SessionLocal()
        
        # Test FranquiciaService
        franquicia_service = FranquiciaService(db)
        franquicia = franquicia_service.crear_franquicia("Franquicia Service Test")
        assert franquicia.nombre == "Franquicia Service Test"
        print("✅ FranquiciaService funciona correctamente")
        
        # Test SucursalService
        sucursal_service = SucursalService(db)
        sucursal = sucursal_service.crear_sucursal("Sucursal Service Test", franquicia.id)
        assert sucursal.nombre == "Sucursal Service Test"
        assert sucursal.franquicia_id == franquicia.id
        print("✅ SucursalService funciona correctamente")
        
        # Test ProductoService
        producto_service = ProductoService(db)
        producto = producto_service.crear_producto("Producto Service Test", 100, sucursal.id)
        assert producto.nombre == "Producto Service Test"
        assert producto.cantidad_stock == 100
        assert producto.sucursal_id == sucursal.id
        print("✅ ProductoService funciona correctamente")
        
        db.close()
        return True
    except Exception as e:
        print(f"❌ Error probando servicios: {e}")
        return False

def main():
    """Función principal de test"""
    print("🚀 Iniciando test robusto de la API de Franquicias")
    print("=" * 60)
    
    tests = [
        ("Imports", test_imports),
        ("Modelos", test_models),
        ("Esquemas", test_schemas),
        ("Base de Datos", test_database_creation),
        ("Repositorios", test_repositories),
        ("Servicios", test_services)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Ejecutando test: {test_name}")
        if test_func():
            passed += 1
            print(f"✅ {test_name} - PASÓ")
        else:
            print(f"❌ {test_name} - FALLÓ")
    
    print("\n" + "=" * 60)
    print(f"📊 Resultados: {passed}/{total} tests pasaron")
    
    if passed == total:
        print("🎉 ¡Todos los tests pasaron exitosamente!")
        print("✅ La implementación está funcionando correctamente")
        return True
    else:
        print("❌ Algunos tests fallaron")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
