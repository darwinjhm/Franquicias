#!/usr/bin/env python3
"""
Script de testing end-to-end para la API de Franquicias
"""

import requests
import json
import time
import sys
from typing import Dict, Any


class APITester:
    """Clase para realizar tests end-to-end de la API"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.created_ids = {
            "franquicias": [],
            "sucursales": [],
            "productos": []
        }
    
    def test_health_check(self) -> bool:
        """Test del endpoint de salud"""
        print("🔍 Probando health check...")
        try:
            response = self.session.get(f"{self.base_url}/health")
            if response.status_code == 200:
                print("✅ Health check exitoso")
                return True
            else:
                print(f"❌ Health check falló: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Error en health check: {e}")
            return False
    
    def test_crear_franquicia(self) -> bool:
        """Test crear franquicia"""
        print("🔍 Probando crear franquicia...")
        try:
            data = {"nombre": "Franquicia de Prueba E2E"}
            response = self.session.post(f"{self.base_url}/api/franquicias/", json=data)
            
            if response.status_code == 201:
                franquicia = response.json()
                self.created_ids["franquicias"].append(franquicia["id"])
                print(f"✅ Franquicia creada con ID: {franquicia['id']}")
                return True
            else:
                print(f"❌ Error al crear franquicia: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"❌ Error en crear franquicia: {e}")
            return False
    
    def test_agregar_sucursal(self) -> bool:
        """Test agregar sucursal a franquicia"""
        print("🔍 Probando agregar sucursal...")
        try:
            if not self.created_ids["franquicias"]:
                print("❌ No hay franquicias creadas")
                return False
            
            franquicia_id = self.created_ids["franquicias"][0]
            data = {"nombre": "Sucursal Centro E2E"}
            response = self.session.post(f"{self.base_url}/api/franquicias/{franquicia_id}/sucursales", json=data)
            
            if response.status_code == 201:
                sucursal = response.json()
                self.created_ids["sucursales"].append(sucursal["id"])
                print(f"✅ Sucursal creada con ID: {sucursal['id']}")
                return True
            else:
                print(f"❌ Error al crear sucursal: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"❌ Error en crear sucursal: {e}")
            return False
    
    def test_agregar_producto(self) -> bool:
        """Test agregar producto a sucursal"""
        print("🔍 Probando agregar producto...")
        try:
            if not self.created_ids["sucursales"]:
                print("❌ No hay sucursales creadas")
                return False
            
            sucursal_id = self.created_ids["sucursales"][0]
            data = {"nombre": "Hamburguesa Clásica E2E", "cantidad_stock": 50}
            response = self.session.post(f"{self.base_url}/api/sucursales/{sucursal_id}/productos", json=data)
            
            if response.status_code == 201:
                producto = response.json()
                self.created_ids["productos"].append(producto["id"])
                print(f"✅ Producto creado con ID: {producto['id']}")
                return True
            else:
                print(f"❌ Error al crear producto: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"❌ Error en crear producto: {e}")
            return False
    
    def test_modificar_stock(self) -> bool:
        """Test modificar stock de producto"""
        print("🔍 Probando modificar stock...")
        try:
            if not self.created_ids["productos"]:
                print("❌ No hay productos creados")
                return False
            
            producto_id = self.created_ids["productos"][0]
            data = {"stock": 100}
            response = self.session.patch(f"{self.base_url}/api/productos/{producto_id}/stock", json=data)
            
            if response.status_code == 200:
                producto = response.json()
                if producto["cantidad_stock"] == 100:
                    print("✅ Stock modificado correctamente")
                    return True
                else:
                    print(f"❌ Stock no se modificó correctamente: {producto['cantidad_stock']}")
                    return False
            else:
                print(f"❌ Error al modificar stock: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"❌ Error en modificar stock: {e}")
            return False
    
    def test_reporte_stock(self) -> bool:
        """Test reporte de stock"""
        print("🔍 Probando reporte de stock...")
        try:
            if not self.created_ids["franquicias"]:
                print("❌ No hay franquicias creadas")
                return False
            
            franquicia_id = self.created_ids["franquicias"][0]
            response = self.session.get(f"{self.base_url}/api/franquicias/{franquicia_id}/reporte-stock")
            
            if response.status_code == 200:
                reporte = response.json()
                print(f"✅ Reporte de stock obtenido: {len(reporte)} productos")
                return True
            else:
                print(f"❌ Error al obtener reporte: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"❌ Error en reporte de stock: {e}")
            return False
    
    def test_actualizar_entidades(self) -> bool:
        """Test actualizar franquicia, sucursal y producto"""
        print("🔍 Probando actualizar entidades...")
        try:
            # Actualizar franquicia
            if self.created_ids["franquicias"]:
                franquicia_id = self.created_ids["franquicias"][0]
                data = {"nombre": "Franquicia Actualizada E2E"}
                response = self.session.patch(f"{self.base_url}/api/franquicias/{franquicia_id}", json=data)
                if response.status_code != 200:
                    print(f"❌ Error al actualizar franquicia: {response.status_code}")
                    return False
            
            # Actualizar sucursal
            if self.created_ids["sucursales"]:
                sucursal_id = self.created_ids["sucursales"][0]
                data = {"nombre": "Sucursal Actualizada E2E"}
                response = self.session.patch(f"{self.base_url}/api/sucursales/{sucursal_id}", json=data)
                if response.status_code != 200:
                    print(f"❌ Error al actualizar sucursal: {response.status_code}")
                    return False
            
            # Actualizar producto
            if self.created_ids["productos"]:
                producto_id = self.created_ids["productos"][0]
                data = {"nombre": "Producto Actualizado E2E"}
                response = self.session.patch(f"{self.base_url}/api/productos/{producto_id}", json=data)
                if response.status_code != 200:
                    print(f"❌ Error al actualizar producto: {response.status_code}")
                    return False
            
            print("✅ Todas las entidades actualizadas correctamente")
            return True
        except Exception as e:
            print(f"❌ Error en actualizar entidades: {e}")
            return False
    
    def test_eliminar_producto(self) -> bool:
        """Test eliminar producto"""
        print("🔍 Probando eliminar producto...")
        try:
            if not self.created_ids["productos"]:
                print("❌ No hay productos creados")
                return False
            
            producto_id = self.created_ids["productos"][0]
            response = self.session.delete(f"{self.base_url}/api/productos/{producto_id}")
            
            if response.status_code == 204:
                print("✅ Producto eliminado correctamente")
                return True
            else:
                print(f"❌ Error al eliminar producto: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"❌ Error en eliminar producto: {e}")
            return False
    
    def run_all_tests(self) -> bool:
        """Ejecutar todos los tests"""
        print("🚀 Iniciando tests end-to-end...")
        print("=" * 50)
        
        tests = [
            self.test_health_check,
            self.test_crear_franquicia,
            self.test_agregar_sucursal,
            self.test_agregar_producto,
            self.test_modificar_stock,
            self.test_reporte_stock,
            self.test_actualizar_entidades,
            self.test_eliminar_producto
        ]
        
        passed = 0
        total = len(tests)
        
        for test in tests:
            if test():
                passed += 1
            print()
        
        print("=" * 50)
        print(f"📊 Resultados: {passed}/{total} tests pasaron")
        
        if passed == total:
            print("🎉 ¡Todos los tests pasaron exitosamente!")
            return True
        else:
            print("❌ Algunos tests fallaron")
            return False


def main():
    """Función principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test end-to-end para API de Franquicias")
    parser.add_argument("--url", default="http://localhost:8000", help="URL base de la API")
    parser.add_argument("--wait", type=int, default=5, help="Segundos a esperar antes de iniciar tests")
    
    args = parser.parse_args()
    
    print(f"⏳ Esperando {args.wait} segundos para que la API esté lista...")
    time.sleep(args.wait)
    
    tester = APITester(args.url)
    success = tester.run_all_tests()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
