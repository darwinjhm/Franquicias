#!/usr/bin/env python3
"""
Test simple para verificar que la API funciona correctamente
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from api_franquicias.main import app
from fastapi.testclient import TestClient

def test_basic_functionality():
    """Test básico de funcionalidad"""
    print("🧪 Iniciando test básico de la API...")
    
    client = TestClient(app)
    
    # Test 1: Health check
    print("1. Probando health check...")
    response = client.get("/health")
    assert response.status_code == 200
    print("✅ Health check OK")
    
    # Test 2: Root endpoint
    print("2. Probando endpoint raíz...")
    response = client.get("/")
    assert response.status_code == 200
    print("✅ Endpoint raíz OK")
    
    # Test 3: Crear franquicia
    print("3. Probando crear franquicia...")
    franquicia_data = {"nombre": "Franquicia Test"}
    response = client.post("/api/franquicias/", json=franquicia_data)
    assert response.status_code == 201
    franquicia = response.json()
    franquicia_id = franquicia["id"]
    print(f"✅ Franquicia creada con ID: {franquicia_id}")
    
    # Test 4: Obtener franquicia
    print("4. Probando obtener franquicia...")
    response = client.get(f"/api/franquicias/{franquicia_id}")
    assert response.status_code == 200
    print("✅ Franquicia obtenida correctamente")
    
    # Test 5: Agregar sucursal
    print("5. Probando agregar sucursal...")
    sucursal_data = {"nombre": "Sucursal Test"}
    response = client.post(f"/api/franquicias/{franquicia_id}/sucursales", json=sucursal_data)
    assert response.status_code == 201
    sucursal = response.json()
    sucursal_id = sucursal["id"]
    print(f"✅ Sucursal creada con ID: {sucursal_id}")
    
    # Test 6: Agregar producto
    print("6. Probando agregar producto...")
    producto_data = {"nombre": "Producto Test", "cantidad_stock": 100}
    response = client.post(f"/api/sucursales/{sucursal_id}/productos", json=producto_data)
    assert response.status_code == 201
    producto = response.json()
    producto_id = producto["id"]
    print(f"✅ Producto creado con ID: {producto_id}")
    
    # Test 7: Modificar stock
    print("7. Probando modificar stock...")
    stock_data = {"stock": 200}
    response = client.patch(f"/api/productos/{producto_id}/stock", json=stock_data)
    assert response.status_code == 200
    print("✅ Stock modificado correctamente")
    
    # Test 8: Reporte de stock
    print("8. Probando reporte de stock...")
    response = client.get(f"/api/franquicias/{franquicia_id}/reporte-stock")
    assert response.status_code == 200
    reporte = response.json()
    print(f"✅ Reporte de stock obtenido: {len(reporte)} productos")
    
    # Test 9: Actualizar entidades
    print("9. Probando actualizar entidades...")
    
    # Actualizar franquicia
    update_data = {"nombre": "Franquicia Actualizada"}
    response = client.patch(f"/api/franquicias/{franquicia_id}", json=update_data)
    assert response.status_code == 200
    print("✅ Franquicia actualizada")
    
    # Actualizar sucursal
    update_data = {"nombre": "Sucursal Actualizada"}
    response = client.patch(f"/api/sucursales/{sucursal_id}", json=update_data)
    assert response.status_code == 200
    print("✅ Sucursal actualizada")
    
    # Actualizar producto
    update_data = {"nombre": "Producto Actualizado"}
    response = client.patch(f"/api/productos/{producto_id}", json=update_data)
    assert response.status_code == 200
    print("✅ Producto actualizado")
    
    # Test 10: Eliminar producto
    print("10. Probando eliminar producto...")
    response = client.delete(f"/api/productos/{producto_id}")
    assert response.status_code == 204
    print("✅ Producto eliminado correctamente")
    
    print("\n🎉 ¡Todos los tests pasaron exitosamente!")
    print("✅ La API está funcionando correctamente")

if __name__ == "__main__":
    test_basic_functionality()
