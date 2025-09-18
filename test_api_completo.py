#!/usr/bin/env python3
"""
Test completo de la API REST usando TestClient de FastAPI
"""

import sys
import os
sys.path.append('src')

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api_franquicias.main import app
from api_franquicias.database import get_db
from api_franquicias.models.base import Base

def setup_test_db():
    """Configurar base de datos de test"""
    # Crear base de datos en memoria
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    return TestingSessionLocal

def test_health_check():
    """Test del endpoint de salud"""
    print("🔍 Probando health check...")
    
    with TestClient(app) as client:
        response = client.get("/health")
        if response.status_code == 200:
            print("✅ Health check exitoso")
            return True
        else:
            print(f"❌ Health check falló: {response.status_code}")
            return False

def test_root_endpoint():
    """Test del endpoint raíz"""
    print("🔍 Probando endpoint raíz...")
    
    with TestClient(app) as client:
        response = client.get("/")
        if response.status_code == 200:
            data = response.json()
            if "API de Gestión de Franquicias" in data.get("message", ""):
                print("✅ Endpoint raíz funciona correctamente")
                return True
            else:
                print("❌ Respuesta del endpoint raíz incorrecta")
                return False
        else:
            print(f"❌ Endpoint raíz falló: {response.status_code}")
            return False

def test_crear_franquicia():
    """Test crear franquicia"""
    print("🔍 Probando crear franquicia...")
    
    with TestClient(app) as client:
        data = {"nombre": "Franquicia Test API"}
        response = client.post("/api/franquicias/", json=data)
        
        if response.status_code == 201:
            franquicia = response.json()
            if franquicia.get("nombre") == "Franquicia Test API" and "id" in franquicia:
                print(f"✅ Franquicia creada: ID {franquicia['id']}")
                return franquicia["id"]
            else:
                print("❌ Datos de franquicia incorrectos")
                return None
        else:
            print(f"❌ Error al crear franquicia: {response.status_code} - {response.text}")
            return None

def test_obtener_franquicia(franquicia_id):
    """Test obtener franquicia por ID"""
    print("🔍 Probando obtener franquicia...")
    
    with TestClient(app) as client:
        response = client.get(f"/api/franquicias/{franquicia_id}")
        
        if response.status_code == 200:
            franquicia = response.json()
            if franquicia.get("id") == franquicia_id:
                print(f"✅ Franquicia obtenida: {franquicia['nombre']}")
                return True
            else:
                print("❌ Datos de franquicia incorrectos")
                return False
        else:
            print(f"❌ Error al obtener franquicia: {response.status_code}")
            return False

def test_agregar_sucursal(franquicia_id):
    """Test agregar sucursal a franquicia"""
    print("🔍 Probando agregar sucursal...")
    
    with TestClient(app) as client:
        data = {"nombre": "Sucursal Test API"}
        response = client.post(f"/api/franquicias/{franquicia_id}/sucursales", json=data)
        
        if response.status_code == 201:
            sucursal = response.json()
            if sucursal.get("nombre") == "Sucursal Test API" and sucursal.get("franquicia_id") == franquicia_id:
                print(f"✅ Sucursal creada: ID {sucursal['id']}")
                return sucursal["id"]
            else:
                print("❌ Datos de sucursal incorrectos")
                return None
        else:
            print(f"❌ Error al crear sucursal: {response.status_code} - {response.text}")
            return None

def test_agregar_producto(sucursal_id):
    """Test agregar producto a sucursal"""
    print("🔍 Probando agregar producto...")
    
    with TestClient(app) as client:
        data = {"nombre": "Producto Test API", "cantidad_stock": 100}
        response = client.post(f"/api/sucursales/{sucursal_id}/productos", json=data)
        
        if response.status_code == 201:
            producto = response.json()
            if (producto.get("nombre") == "Producto Test API" and 
                producto.get("cantidad_stock") == 100 and 
                producto.get("sucursal_id") == sucursal_id):
                print(f"✅ Producto creado: ID {producto['id']}")
                return producto["id"]
            else:
                print("❌ Datos de producto incorrectos")
                return None
        else:
            print(f"❌ Error al crear producto: {response.status_code} - {response.text}")
            return None

def test_modificar_stock(producto_id):
    """Test modificar stock de producto"""
    print("🔍 Probando modificar stock...")
    
    with TestClient(app) as client:
        data = {"stock": 200}
        response = client.patch(f"/api/productos/{producto_id}/stock", json=data)
        
        if response.status_code == 200:
            producto = response.json()
            if producto.get("cantidad_stock") == 200:
                print("✅ Stock modificado correctamente")
                return True
            else:
                print(f"❌ Stock no se modificó: {producto.get('cantidad_stock')}")
                return False
        else:
            print(f"❌ Error al modificar stock: {response.status_code} - {response.text}")
            return False

def test_reporte_stock(franquicia_id):
    """Test reporte de stock"""
    print("🔍 Probando reporte de stock...")
    
    with TestClient(app) as client:
        response = client.get(f"/api/franquicias/{franquicia_id}/reporte-stock")
        
        if response.status_code == 200:
            reporte = response.json()
            print(f"✅ Reporte de stock obtenido: {len(reporte)} productos")
            return True
        else:
            print(f"❌ Error al obtener reporte: {response.status_code} - {response.text}")
            return False

def test_actualizar_entidades(franquicia_id, sucursal_id, producto_id):
    """Test actualizar franquicia, sucursal y producto"""
    print("🔍 Probando actualizar entidades...")
    
    with TestClient(app) as client:
        # Actualizar franquicia
        data = {"nombre": "Franquicia Actualizada API"}
        response = client.patch(f"/api/franquicias/{franquicia_id}", json=data)
        if response.status_code != 200:
            print(f"❌ Error al actualizar franquicia: {response.status_code}")
            return False
        
        # Actualizar sucursal
        data = {"nombre": "Sucursal Actualizada API"}
        response = client.patch(f"/api/sucursales/{sucursal_id}", json=data)
        if response.status_code != 200:
            print(f"❌ Error al actualizar sucursal: {response.status_code}")
            return False
        
        # Actualizar producto
        data = {"nombre": "Producto Actualizado API"}
        response = client.patch(f"/api/productos/{producto_id}", json=data)
        if response.status_code != 200:
            print(f"❌ Error al actualizar producto: {response.status_code}")
            return False
        
        print("✅ Todas las entidades actualizadas correctamente")
        return True

def test_eliminar_producto(producto_id):
    """Test eliminar producto"""
    print("🔍 Probando eliminar producto...")
    
    with TestClient(app) as client:
        response = client.delete(f"/api/productos/{producto_id}")
        
        if response.status_code == 204:
            print("✅ Producto eliminado correctamente")
            return True
        else:
            print(f"❌ Error al eliminar producto: {response.status_code} - {response.text}")
            return False

def test_validaciones():
    """Test validaciones de datos"""
    print("🔍 Probando validaciones...")
    
    with TestClient(app) as client:
        # Test crear franquicia con nombre vacío
        response = client.post("/api/franquicias/", json={"nombre": ""})
        if response.status_code == 422:
            print("✅ Validación de nombre vacío funciona")
        else:
            print("❌ Debería fallar con nombre vacío")
            return False
        
        # Test crear franquicia duplicada
        client.post("/api/franquicias/", json={"nombre": "Franquicia Duplicada"})
        response = client.post("/api/franquicias/", json={"nombre": "Franquicia Duplicada"})
        if response.status_code == 400:
            print("✅ Validación de nombre duplicado funciona")
        else:
            print("❌ Debería fallar con nombre duplicado")
            return False
        
        return True

def main():
    """Función principal del test"""
    print("🚀 Iniciando test completo de la API REST")
    print("=" * 60)
    
    # Configurar base de datos de test
    setup_test_db()
    
    tests_passed = 0
    total_tests = 0
    
    # Test 1: Health check
    total_tests += 1
    if test_health_check():
        tests_passed += 1
    print()
    
    # Test 2: Endpoint raíz
    total_tests += 1
    if test_root_endpoint():
        tests_passed += 1
    print()
    
    # Test 3: Crear franquicia
    total_tests += 1
    franquicia_id = test_crear_franquicia()
    if franquicia_id:
        tests_passed += 1
    print()
    
    if franquicia_id:
        # Test 4: Obtener franquicia
        total_tests += 1
        if test_obtener_franquicia(franquicia_id):
            tests_passed += 1
        print()
        
        # Test 5: Agregar sucursal
        total_tests += 1
        sucursal_id = test_agregar_sucursal(franquicia_id)
        if sucursal_id:
            tests_passed += 1
        print()
        
        if sucursal_id:
            # Test 6: Agregar producto
            total_tests += 1
            producto_id = test_agregar_producto(sucursal_id)
            if producto_id:
                tests_passed += 1
            print()
            
            if producto_id:
                # Test 7: Modificar stock
                total_tests += 1
                if test_modificar_stock(producto_id):
                    tests_passed += 1
                print()
                
                # Test 8: Reporte de stock
                total_tests += 1
                if test_reporte_stock(franquicia_id):
                    tests_passed += 1
                print()
                
                # Test 9: Actualizar entidades
                total_tests += 1
                if test_actualizar_entidades(franquicia_id, sucursal_id, producto_id):
                    tests_passed += 1
                print()
                
                # Test 10: Eliminar producto
                total_tests += 1
                if test_eliminar_producto(producto_id):
                    tests_passed += 1
                print()
    
    # Test 11: Validaciones
    total_tests += 1
    if test_validaciones():
        tests_passed += 1
    print()
    
    print("=" * 60)
    print(f"📊 Resultados: {tests_passed}/{total_tests} tests pasaron")
    
    if tests_passed == total_tests:
        print("🎉 ¡Todos los tests pasaron exitosamente!")
        print("✅ La API REST está funcionando perfectamente")
        return True
    else:
        print("❌ Algunos tests fallaron")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
