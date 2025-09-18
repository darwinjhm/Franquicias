#!/usr/bin/env python3
"""
Test de la API REST usando requests HTTP
"""

import sys
import os
import time
import threading
import subprocess
sys.path.append('src')

def start_api_server():
    """Iniciar el servidor API en un hilo separado"""
    try:
        # Ejecutar la API
        process = subprocess.Popen([
            sys.executable, "-c", 
            "import sys; sys.path.append('src'); from api_franquicias.main import main; main()"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return process
    except Exception as e:
        print(f"Error iniciando servidor: {e}")
        return None

def test_http_api():
    """Test de la API usando requests HTTP"""
    print("🚀 Iniciando test HTTP de la API REST")
    print("=" * 60)
    
    # Iniciar servidor
    print("1️⃣ Iniciando servidor API...")
    server_process = start_api_server()
    
    if not server_process:
        print("❌ No se pudo iniciar el servidor")
        return False
    
    # Esperar a que el servidor inicie
    print("2️⃣ Esperando que el servidor inicie...")
    time.sleep(8)
    
    try:
        import requests
        
        base_url = "http://localhost:8000"
        
        # Test health check
        print("3️⃣ Probando health check...")
        try:
            response = requests.get(f"{base_url}/health", timeout=5)
            if response.status_code == 200:
                print("✅ Health check exitoso")
            else:
                print(f"❌ Health check falló: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"❌ Error en health check: {e}")
            return False
        
        # Test endpoint raíz
        print("4️⃣ Probando endpoint raíz...")
        try:
            response = requests.get(f"{base_url}/", timeout=5)
            if response.status_code == 200:
                data = response.json()
                if "API de Gestión de Franquicias" in data.get("message", ""):
                    print("✅ Endpoint raíz funciona")
                else:
                    print("❌ Respuesta incorrecta del endpoint raíz")
                    return False
            else:
                print(f"❌ Endpoint raíz falló: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"❌ Error en endpoint raíz: {e}")
            return False
        
        # Test crear franquicia
        print("5️⃣ Creando franquicia...")
        try:
            data = {"nombre": "Franquicia HTTP Test"}
            response = requests.post(f"{base_url}/api/franquicias/", json=data, timeout=5)
            if response.status_code == 201:
                franquicia = response.json()
                franquicia_id = franquicia["id"]
                print(f"✅ Franquicia creada: ID {franquicia_id}")
            else:
                print(f"❌ Error creando franquicia: {response.status_code} - {response.text}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"❌ Error creando franquicia: {e}")
            return False
        
        # Test agregar sucursal
        print("6️⃣ Agregando sucursal...")
        try:
            data = {"nombre": "Sucursal HTTP Test"}
            response = requests.post(f"{base_url}/api/franquicias/{franquicia_id}/sucursales", json=data, timeout=5)
            if response.status_code == 201:
                sucursal = response.json()
                sucursal_id = sucursal["id"]
                print(f"✅ Sucursal creada: ID {sucursal_id}")
            else:
                print(f"❌ Error creando sucursal: {response.status_code} - {response.text}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"❌ Error creando sucursal: {e}")
            return False
        
        # Test agregar producto
        print("7️⃣ Agregando producto...")
        try:
            data = {"nombre": "Producto HTTP Test", "cantidad_stock": 100}
            response = requests.post(f"{base_url}/api/sucursales/{sucursal_id}/productos", json=data, timeout=5)
            if response.status_code == 201:
                producto = response.json()
                producto_id = producto["id"]
                print(f"✅ Producto creado: ID {producto_id}")
            else:
                print(f"❌ Error creando producto: {response.status_code} - {response.text}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"❌ Error creando producto: {e}")
            return False
        
        # Test modificar stock
        print("8️⃣ Modificando stock...")
        try:
            data = {"stock": 200}
            response = requests.patch(f"{base_url}/api/productos/{producto_id}/stock", json=data, timeout=5)
            if response.status_code == 200:
                producto = response.json()
                if producto["cantidad_stock"] == 200:
                    print("✅ Stock modificado correctamente")
                else:
                    print(f"❌ Stock no se modificó: {producto['cantidad_stock']}")
                    return False
            else:
                print(f"❌ Error modificando stock: {response.status_code} - {response.text}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"❌ Error modificando stock: {e}")
            return False
        
        # Test reporte de stock
        print("9️⃣ Obteniendo reporte de stock...")
        try:
            response = requests.get(f"{base_url}/api/franquicias/{franquicia_id}/reporte-stock", timeout=5)
            if response.status_code == 200:
                reporte = response.json()
                print(f"✅ Reporte obtenido: {len(reporte)} productos")
            else:
                print(f"❌ Error obteniendo reporte: {response.status_code} - {response.text}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"❌ Error obteniendo reporte: {e}")
            return False
        
        # Test actualizar entidades
        print("🔟 Actualizando entidades...")
        try:
            # Actualizar franquicia
            data = {"nombre": "Franquicia HTTP Actualizada"}
            response = requests.patch(f"{base_url}/api/franquicias/{franquicia_id}", json=data, timeout=5)
            if response.status_code != 200:
                print(f"❌ Error actualizando franquicia: {response.status_code}")
                return False
            
            # Actualizar sucursal
            data = {"nombre": "Sucursal HTTP Actualizada"}
            response = requests.patch(f"{base_url}/api/sucursales/{sucursal_id}", json=data, timeout=5)
            if response.status_code != 200:
                print(f"❌ Error actualizando sucursal: {response.status_code}")
                return False
            
            # Actualizar producto
            data = {"nombre": "Producto HTTP Actualizado"}
            response = requests.patch(f"{base_url}/api/productos/{producto_id}", json=data, timeout=5)
            if response.status_code != 200:
                print(f"❌ Error actualizando producto: {response.status_code}")
                return False
            
            print("✅ Todas las entidades actualizadas correctamente")
        except requests.exceptions.RequestException as e:
            print(f"❌ Error actualizando entidades: {e}")
            return False
        
        # Test eliminar producto
        print("1️⃣1️⃣ Eliminando producto...")
        try:
            response = requests.delete(f"{base_url}/api/productos/{producto_id}", timeout=5)
            if response.status_code == 204:
                print("✅ Producto eliminado correctamente")
            else:
                print(f"❌ Error eliminando producto: {response.status_code} - {response.text}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"❌ Error eliminando producto: {e}")
            return False
        
        print("\n" + "=" * 60)
        print("🎉 ¡TEST HTTP COMPLETO EXITOSO!")
        print("✅ La API REST está funcionando perfectamente")
        print("✅ Todos los endpoints responden correctamente")
        return True
        
    except ImportError:
        print("❌ requests no está instalado")
        return False
    finally:
        # Terminar el servidor
        if server_process:
            server_process.terminate()
            server_process.wait()
            print("🛑 Servidor terminado")

def main():
    """Función principal"""
    print("🚀 INICIANDO TEST HTTP ROBUSTO")
    print("=" * 80)
    
    success = test_http_api()
    
    print("\n" + "=" * 80)
    if success:
        print("🎉 ¡TEST HTTP COMPLETO EXITOSO!")
        print("✅ La API REST está completamente funcional")
        print("✅ Lista para uso en producción")
        return True
    else:
        print("❌ Test HTTP falló")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
