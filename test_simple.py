#!/usr/bin/env python3
"""
Test simple para verificar la funcionalidad básica de la API
"""

import sys
import os
sys.path.append('src')

def test_imports():
    """Test que todos los módulos se pueden importar"""
    print("🔍 Probando imports...")
    
    try:
        from api_franquicias.models import Franquicia, Sucursal, Producto, Base
        print("✅ Modelos importados correctamente")
    except Exception as e:
        print(f"❌ Error importando modelos: {e}")
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
        from api_franquicias.schemas import FranquiciaCreate, FranquiciaResponse
        print("✅ Esquemas importados correctamente")
    except Exception as e:
        print(f"❌ Error importando esquemas: {e}")
        return False
    
    try:
        from api_franquicias.database import create_tables, get_db
        print("✅ Base de datos importada correctamente")
    except Exception as e:
        print(f"❌ Error importando base de datos: {e}")
        return False
    
    return True

def test_database_creation():
    """Test creación de base de datos"""
    print("\n🔍 Probando creación de base de datos...")
    
    try:
        from api_franquicias.database import create_tables
        create_tables()
        print("✅ Tablas creadas correctamente")
        return True
    except Exception as e:
        print(f"❌ Error creando tablas: {e}")
        return False

def test_models():
    """Test creación de modelos"""
    print("\n🔍 Probando creación de modelos...")
    
    try:
        from api_franquicias.models import Franquicia, Sucursal, Producto
        
        # Crear franquicia
        franquicia = Franquicia(nombre="Franquicia Test")
        print(f"✅ Franquicia creada: {franquicia}")
        
        # Crear sucursal
        sucursal = Sucursal(nombre="Sucursal Test", franquicia_id=1)
        print(f"✅ Sucursal creada: {sucursal}")
        
        # Crear producto
        producto = Producto(nombre="Producto Test", cantidad_stock=100, sucursal_id=1)
        print(f"✅ Producto creado: {producto}")
        
        return True
    except Exception as e:
        print(f"❌ Error creando modelos: {e}")
        return False

def test_schemas():
    """Test validación de esquemas"""
    print("\n🔍 Probando esquemas Pydantic...")
    
    try:
        from api_franquicias.schemas import FranquiciaCreate, FranquiciaResponse
        
        # Test creación de franquicia
        franquicia_data = FranquiciaCreate(nombre="Franquicia Schema Test")
        print(f"✅ FranquiciaCreate válido: {franquicia_data}")
        
        # Test validación de datos vacíos
        try:
            FranquiciaCreate(nombre="")
            print("❌ Debería fallar con nombre vacío")
            return False
        except:
            print("✅ Validación de nombre vacío funciona")
        
        return True
    except Exception as e:
        print(f"❌ Error con esquemas: {e}")
        return False

def test_repositories():
    """Test repositorios con base de datos en memoria"""
    print("\n🔍 Probando repositorios...")
    
    try:
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
        from api_franquicias.models.base import Base
        from api_franquicias.repositories import FranquiciaRepository
        
        # Crear base de datos en memoria
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(bind=engine)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        
        # Crear sesión
        db = SessionLocal()
        
        # Test repositorio
        repo = FranquiciaRepository(db)
        franquicia = repo.create("Franquicia Repo Test")
        print(f"✅ Franquicia creada en repositorio: {franquicia.nombre}")
        
        # Test obtener por ID
        franquicia_obtenida = repo.get_by_id(franquicia.id)
        if franquicia_obtenida:
            print(f"✅ Franquicia obtenida por ID: {franquicia_obtenida.nombre}")
        else:
            print("❌ No se pudo obtener franquicia por ID")
            return False
        
        db.close()
        return True
    except Exception as e:
        print(f"❌ Error con repositorios: {e}")
        return False

def test_services():
    """Test servicios"""
    print("\n🔍 Probando servicios...")
    
    try:
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
        from api_franquicias.models.base import Base
        from api_franquicias.services import FranquiciaService
        
        # Crear base de datos en memoria
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(bind=engine)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        
        # Crear sesión
        db = SessionLocal()
        
        # Test servicio
        service = FranquiciaService(db)
        franquicia = service.crear_franquicia("Franquicia Service Test")
        print(f"✅ Franquicia creada en servicio: {franquicia.nombre}")
        
        # Test validación de nombre duplicado
        try:
            service.crear_franquicia("Franquicia Service Test")
            print("❌ Debería fallar con nombre duplicado")
            return False
        except ValueError as e:
            print(f"✅ Validación de nombre duplicado funciona: {e}")
        
        db.close()
        return True
    except Exception as e:
        print(f"❌ Error con servicios: {e}")
        return False

def main():
    """Función principal del test"""
    print("🚀 Iniciando test robusto de la API de Franquicias")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_database_creation,
        test_models,
        test_schemas,
        test_repositories,
        test_services
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 60)
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
