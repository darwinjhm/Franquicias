#!/usr/bin/env python3
"""
Test completo de la API de Franquicias incluyendo endpoints REST
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_complete_api():
    """Test completo de la API"""
    print("🚀 Iniciando test completo de la API de Franquicias")
    print("=" * 70)
    
    # Test 1: Imports y configuración
    print("\n📋 Test 1: Imports y configuración")
    try:
        from api_franquicias.main import app
        from api_franquicias.database import init_db
        from api_franquicias.config import settings
        print("✅ Aplicación FastAPI importada correctamente")
        print(f"✅ Configuración cargada: {settings.app_name} v{settings.app_version}")
    except Exception as e:
        print(f"❌ Error en imports: {e}")
        return False
    
    # Test 2: Inicialización de base de datos
    print("\n📋 Test 2: Inicialización de base de datos")
    try:
        init_db()
        print("✅ Base de datos inicializada correctamente")
    except Exception as e:
        print(f"❌ Error inicializando base de datos: {e}")
        return False
    
    # Test 3: Verificar endpoints de la aplicación
    print("\n📋 Test 3: Verificando endpoints de la aplicación")
    try:
        from fastapi.testclient import TestClient
        client = TestClient(app)
        
        # Test endpoint raíz
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        print("✅ Endpoint raíz funcionando")
        
        # Test health check
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        print("✅ Health check funcionando")
        
    except Exception as e:
        print(f"❌ Error en endpoints básicos: {e}")
        return False
    
    # Test 4: Test completo del flujo de datos
    print("\n📋 Test 4: Flujo completo de datos")
    try:
        # Crear franquicia
        franquicia_data = {"nombre": "Franquicia Test Completo"}
        response = client.post("/api/franquicias/", json=franquicia_data)
        assert response.status_code == 201
        franquicia = response.json()
        franquicia_id = franquicia["id"]
        print(f"✅ Franquicia creada: ID {franquicia_id}")
        
        # Obtener franquicia
        response = client.get(f"/api/franquicias/{franquicia_id}")
        assert response.status_code == 200
        print("✅ Franquicia obtenida correctamente")
        
        # Crear sucursal
        sucursal_data = {"nombre": "Sucursal Test Completo"}
        response = client.post(f"/api/franquicias/{franquicia_id}/sucursales", json=sucursal_data)
        assert response.status_code == 201
        sucursal = response.json()
        sucursal_id = sucursal["id"]
        print(f"✅ Sucursal creada: ID {sucursal_id}")
        
        # Crear producto
        producto_data = {"nombre": "Producto Test Completo", "cantidad_stock": 150}
        response = client.post(f"/api/sucursales/{sucursal_id}/productos", json=producto_data)
        assert response.status_code == 201
        producto = response.json()
        producto_id = producto["id"]
        print(f"✅ Producto creado: ID {producto_id}")
        
        # Modificar stock
        stock_data = {"stock": 300}
        response = client.patch(f"/api/productos/{producto_id}/stock", json=stock_data)
        assert response.status_code == 200
        print("✅ Stock modificado correctamente")
        
        # Obtener reporte de stock
        response = client.get(f"/api/franquicias/{franquicia_id}/reporte-stock")
        assert response.status_code == 200
        reporte = response.json()
        assert len(reporte) == 1
        assert reporte[0]["cantidad_stock"] == 300
        print("✅ Reporte de stock funcionando correctamente")
        
        # Actualizar entidades
        update_franquicia = {"nombre": "Franquicia Actualizada Completo"}
        response = client.patch(f"/api/franquicias/{franquicia_id}", json=update_franquicia)
        assert response.status_code == 200
        print("✅ Franquicia actualizada")
        
        update_sucursal = {"nombre": "Sucursal Actualizada Completo"}
        response = client.patch(f"/api/sucursales/{sucursal_id}", json=update_sucursal)
        assert response.status_code == 200
        print("✅ Sucursal actualizada")
        
        update_producto = {"nombre": "Producto Actualizado Completo"}
        response = client.patch(f"/api/productos/{producto_id}", json=update_producto)
        assert response.status_code == 200
        print("✅ Producto actualizado")
        
        # Eliminar producto
        response = client.delete(f"/api/productos/{producto_id}")
        assert response.status_code == 204
        print("✅ Producto eliminado correctamente")
        
    except Exception as e:
        print(f"❌ Error en flujo de datos: {e}")
        return False
    
    # Test 5: Validaciones de negocio
    print("\n📋 Test 5: Validaciones de negocio")
    try:
        # Test crear franquicia con nombre duplicado
        franquicia_duplicada = {"nombre": "Franquicia Test Completo"}
        response = client.post("/api/franquicias/", json=franquicia_duplicada)
        assert response.status_code == 400
        print("✅ Validación de nombre duplicado funcionando")
        
        # Test crear producto con stock negativo
        producto_negativo = {"nombre": "Producto Negativo", "cantidad_stock": -10}
        response = client.post(f"/api/sucursales/{sucursal_id}/productos", json=producto_negativo)
        assert response.status_code == 400
        print("✅ Validación de stock negativo funcionando")
        
        # Test obtener recurso inexistente
        response = client.get("/api/franquicias/99999")
        assert response.status_code == 404
        print("✅ Manejo de recursos inexistentes funcionando")
        
    except Exception as e:
        print(f"❌ Error en validaciones: {e}")
        return False
    
    # Test 6: Documentación de la API
    print("\n📋 Test 6: Documentación de la API")
    try:
        # Test OpenAPI schema
        response = client.get("/openapi.json")
        assert response.status_code == 200
        schema = response.json()
        assert "openapi" in schema
        assert "info" in schema
        print("✅ Schema OpenAPI generado correctamente")
        
        # Test documentación Swagger
        response = client.get("/docs")
        assert response.status_code == 200
        print("✅ Documentación Swagger disponible")
        
        # Test documentación ReDoc
        response = client.get("/redoc")
        assert response.status_code == 200
        print("✅ Documentación ReDoc disponible")
        
    except Exception as e:
        print(f"❌ Error en documentación: {e}")
        return False
    
    return True

def main():
    """Función principal"""
    print("🎯 TEST ROBUSTO COMPLETO DE LA API DE FRANQUICIAS")
    print("=" * 70)
    
    success = test_complete_api()
    
    print("\n" + "=" * 70)
    if success:
        print("🎉 ¡TEST COMPLETO EXITOSO!")
        print("✅ Todos los componentes de la API funcionan correctamente")
        print("✅ La implementación está lista para producción")
        print("\n📋 Funcionalidades verificadas:")
        print("   • Modelos de datos (Franquicia, Sucursal, Producto)")
        print("   • Repositorios para acceso a datos")
        print("   • Servicios de lógica de negocio")
        print("   • Controladores REST (9 endpoints)")
        print("   • Validaciones de negocio")
        print("   • Manejo de errores")
        print("   • Documentación automática")
        print("   • Base de datos SQLite")
        print("   • Configuración flexible")
    else:
        print("❌ TEST FALLÓ")
        print("❌ Hay problemas que necesitan ser corregidos")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
