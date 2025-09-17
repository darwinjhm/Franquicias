#!/usr/bin/env python3
"""
Test manual para verificar que la API funciona correctamente
"""

import subprocess
import time
import requests
import json
import sys

def test_api_manually():
    """Test manual de la API ejecutando el servidor"""
    print("🚀 Iniciando test manual de la API...")
    
    # Iniciar el servidor en background
    print("1. Iniciando servidor FastAPI...")
    try:
        # Ejecutar el servidor
        process = subprocess.Popen([
            sys.executable, "-m", "api_franquicias"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Esperar a que el servidor inicie
        print("⏳ Esperando a que el servidor inicie...")
        time.sleep(5)
        
        # Verificar que el servidor esté ejecutándose
        try:
            response = requests.get("http://localhost:8000/health", timeout=5)
            if response.status_code == 200:
                print("✅ Servidor iniciado correctamente")
            else:
                print(f"❌ Servidor respondió con código: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"❌ No se pudo conectar al servidor: {e}")
            return False
        
        # Test 1: Health check
        print("\n2. Probando health check...")
        response = requests.get("http://localhost:8000/health")
        assert response.status_code == 200
        print("✅ Health check OK")
        
        # Test 2: Root endpoint
        print("\n3. Probando endpoint raíz...")
        response = requests.get("http://localhost:8000/")
        assert response.status_code == 200
        print("✅ Endpoint raíz OK")
        
        # Test 3: Crear franquicia
        print("\n4. Probando crear franquicia...")
        franquicia_data = {"nombre": "Franquicia Test Manual"}
        response = requests.post("http://localhost:8000/api/franquicias/", json=franquicia_data)
        assert response.status_code == 201
        franquicia = response.json()
        franquicia_id = franquicia["id"]
        print(f"✅ Franquicia creada con ID: {franquicia_id}")
        
        # Test 4: Obtener franquicia
        print("\n5. Probando obtener franquicia...")
        response = requests.get(f"http://localhost:8000/api/franquicias/{franquicia_id}")
        assert response.status_code == 200
        print("✅ Franquicia obtenida correctamente")
        
        # Test 5: Agregar sucursal
        print("\n6. Probando agregar sucursal...")
        sucursal_data = {"nombre": "Sucursal Test Manual"}
        response = requests.post(f"http://localhost:8000/api/franquicias/{franquicia_id}/sucursales", json=sucursal_data)
        assert response.status_code == 201
        sucursal = response.json()
        sucursal_id = sucursal["id"]
        print(f"✅ Sucursal creada con ID: {sucursal_id}")
        
        # Test 6: Agregar producto
        print("\n7. Probando agregar producto...")
        producto_data = {"nombre": "Producto Test Manual", "cantidad_stock": 100}
        response = requests.post(f"http://localhost:8000/api/sucursales/{sucursal_id}/productos", json=producto_data)
        assert response.status_code == 201
        producto = response.json()
        producto_id = producto["id"]
        print(f"✅ Producto creado con ID: {producto_id}")
        
        # Test 7: Modificar stock
        print("\n8. Probando modificar stock...")
        stock_data = {"stock": 200}
        response = requests.patch(f"http://localhost:8000/api/productos/{producto_id}/stock", json=stock_data)
        assert response.status_code == 200
        print("✅ Stock modificado correctamente")
        
        # Test 8: Reporte de stock
        print("\n9. Probando reporte de stock...")
        response = requests.get(f"http://localhost:8000/api/franquicias/{franquicia_id}/reporte-stock")
        assert response.status_code == 200
        reporte = response.json()
        print(f"✅ Reporte de stock obtenido: {len(reporte)} productos")
        
        # Test 9: Actualizar entidades
        print("\n10. Probando actualizar entidades...")
        
        # Actualizar franquicia
        update_data = {"nombre": "Franquicia Actualizada Manual"}
        response = requests.patch(f"http://localhost:8000/api/franquicias/{franquicia_id}", json=update_data)
        assert response.status_code == 200
        print("✅ Franquicia actualizada")
        
        # Actualizar sucursal
        update_data = {"nombre": "Sucursal Actualizada Manual"}
        response = requests.patch(f"http://localhost:8000/api/sucursales/{sucursal_id}", json=update_data)
        assert response.status_code == 200
        print("✅ Sucursal actualizada")
        
        # Actualizar producto
        update_data = {"nombre": "Producto Actualizado Manual"}
        response = requests.patch(f"http://localhost:8000/api/productos/{producto_id}", json=update_data)
        assert response.status_code == 200
        print("✅ Producto actualizado")
        
        # Test 10: Eliminar producto
        print("\n11. Probando eliminar producto...")
        response = requests.delete(f"http://localhost:8000/api/productos/{producto_id}")
        assert response.status_code == 204
        print("✅ Producto eliminado correctamente")
        
        print("\n🎉 ¡Todos los tests pasaron exitosamente!")
        print("✅ La API está funcionando correctamente")
        
        return True
        
    except Exception as e:
        print(f"❌ Error durante el test: {e}")
        return False
    finally:
        # Terminar el proceso del servidor
        try:
            process.terminate()
            process.wait(timeout=5)
            print("\n🛑 Servidor detenido")
        except:
            process.kill()
            print("\n🛑 Servidor forzado a detener")

if __name__ == "__main__":
    success = test_api_manually()
    sys.exit(0 if success else 1)
