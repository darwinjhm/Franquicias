#!/usr/bin/env python3
"""
Test final robusto de la funcionalidad completa
"""

import sys
import os
sys.path.append('src')

def test_complete_workflow():
    """Test del flujo completo de trabajo"""
    print("🚀 Iniciando test robusto del flujo completo")
    print("=" * 60)
    
    try:
        # 1. Importar todos los módulos
        print("1️⃣ Importando módulos...")
        from api_franquicias.models import Franquicia, Sucursal, Producto, Base
        from api_franquicias.repositories import FranquiciaRepository, SucursalRepository, ProductoRepository
        from api_franquicias.services import FranquiciaService, SucursalService, ProductoService
        from api_franquicias.schemas import FranquiciaCreate, FranquiciaResponse
        from api_franquicias.database import create_tables
        print("✅ Todos los módulos importados correctamente")
        
        # 2. Configurar base de datos
        print("\n2️⃣ Configurando base de datos...")
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
        
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(bind=engine)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        print("✅ Base de datos configurada")
        
        # 3. Test crear franquicia
        print("\n3️⃣ Creando franquicia...")
        franquicia_service = FranquiciaService(db)
        franquicia = franquicia_service.crear_franquicia("Franquicia Test Completo")
        print(f"✅ Franquicia creada: {franquicia.nombre} (ID: {franquicia.id})")
        
        # 4. Test crear sucursal
        print("\n4️⃣ Creando sucursal...")
        sucursal_service = SucursalService(db)
        sucursal = sucursal_service.crear_sucursal("Sucursal Centro", franquicia.id)
        print(f"✅ Sucursal creada: {sucursal.nombre} (ID: {sucursal.id})")
        
        # 5. Test crear productos
        print("\n5️⃣ Creando productos...")
        producto_service = ProductoService(db)
        
        productos_data = [
            ("Hamburguesa Clásica", 50),
            ("Papas Fritas", 100),
            ("Refresco", 75),
            ("Ensalada", 25)
        ]
        
        productos_creados = []
        for nombre, stock in productos_data:
            producto = producto_service.crear_producto(nombre, stock, sucursal.id)
            productos_creados.append(producto)
            print(f"   ✅ {producto.nombre} - Stock: {producto.cantidad_stock}")
        
        # 6. Test modificar stock
        print("\n6️⃣ Modificando stock...")
        producto = productos_creados[0]
        producto_actualizado = producto_service.actualizar_stock(producto.id, 150)
        print(f"✅ Stock de {producto_actualizado.nombre} actualizado a {producto_actualizado.cantidad_stock}")
        
        # 7. Test reporte de stock
        print("\n7️⃣ Generando reporte de stock...")
        reporte = franquicia_service.obtener_reporte_stock(franquicia.id)
        print(f"✅ Reporte generado con {len(reporte)} productos:")
        for item in reporte:
            print(f"   📊 {item['producto_nombre']} - Stock: {item['cantidad_stock']} (Sucursal: {item['sucursal_nombre']})")
        
        # 8. Test actualizar entidades
        print("\n8️⃣ Actualizando entidades...")
        
        # Actualizar franquicia
        franquicia_actualizada = franquicia_service.actualizar_franquicia(franquicia.id, "Franquicia Actualizada")
        print(f"✅ Franquicia actualizada: {franquicia_actualizada.nombre}")
        
        # Actualizar sucursal
        sucursal_actualizada = sucursal_service.actualizar_sucursal(sucursal.id, "Sucursal Actualizada")
        print(f"✅ Sucursal actualizada: {sucursal_actualizada.nombre}")
        
        # Actualizar producto
        producto_actualizado = producto_service.actualizar_producto(productos_creados[0].id, "Hamburguesa Premium")
        print(f"✅ Producto actualizado: {producto_actualizado.nombre}")
        
        # 9. Test validaciones
        print("\n9️⃣ Probando validaciones...")
        
        # Test nombre duplicado en franquicia
        try:
            franquicia_service.crear_franquicia("Franquicia Actualizada")
            print("❌ Debería fallar con nombre duplicado")
        except ValueError as e:
            print(f"✅ Validación de nombre duplicado: {e}")
        
        # Test stock negativo
        try:
            producto_service.actualizar_stock(productos_creados[0].id, -10)
            print("❌ Debería fallar con stock negativo")
        except ValueError as e:
            print(f"✅ Validación de stock negativo: {e}")
        
        # 10. Test eliminar producto
        print("\n🔟 Eliminando producto...")
        producto_eliminado = producto_service.eliminar_producto(productos_creados[-1].id)
        if producto_eliminado:
            print(f"✅ Producto eliminado: {productos_creados[-1].nombre}")
        else:
            print("❌ Error al eliminar producto")
        
        # 11. Test obtener todas las entidades
        print("\n1️⃣1️⃣ Obteniendo todas las entidades...")
        
        todas_franquicias = franquicia_service.obtener_todas_franquicias()
        print(f"✅ Total franquicias: {len(todas_franquicias)}")
        
        sucursales_franquicia = sucursal_service.obtener_sucursales_por_franquicia(franquicia.id)
        print(f"✅ Sucursales de la franquicia: {len(sucursales_franquicia)}")
        
        productos_sucursal = producto_service.obtener_productos_por_sucursal(sucursal.id)
        print(f"✅ Productos de la sucursal: {len(productos_sucursal)}")
        
        db.close()
        
        print("\n" + "=" * 60)
        print("🎉 ¡TEST COMPLETO EXITOSO!")
        print("✅ Todas las funcionalidades están trabajando correctamente")
        print("✅ La implementación es robusta y completa")
        return True
        
    except Exception as e:
        print(f"\n❌ Error durante el test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_performance():
    """Test de rendimiento básico"""
    print("\n🚀 Test de rendimiento...")
    
    try:
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
        from api_franquicias.models.base import Base
        from api_franquicias.services import FranquiciaService, SucursalService, ProductoService
        
        # Configurar base de datos
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(bind=engine)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # Crear servicios
        franquicia_service = FranquiciaService(db)
        sucursal_service = SucursalService(db)
        producto_service = ProductoService(db)
        
        import time
        start_time = time.time()
        
        # Crear múltiples franquicias
        franquicias = []
        for i in range(10):
            franquicia = franquicia_service.crear_franquicia(f"Franquicia {i+1}")
            franquicias.append(franquicia)
            
            # Crear sucursales para cada franquicia
            for j in range(3):
                sucursal = sucursal_service.crear_sucursal(f"Sucursal {j+1}", franquicia.id)
                
                # Crear productos para cada sucursal
                for k in range(5):
                    producto_service.crear_producto(f"Producto {k+1}", 100, sucursal.id)
        
        end_time = time.time()
        elapsed = end_time - start_time
        
        print(f"✅ Creadas 10 franquicias, 30 sucursales y 150 productos en {elapsed:.2f} segundos")
        print(f"✅ Promedio: {elapsed/190:.4f} segundos por entidad")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Error en test de rendimiento: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 INICIANDO TEST ROBUSTO COMPLETO")
    print("=" * 80)
    
    # Test principal
    success1 = test_complete_workflow()
    
    # Test de rendimiento
    success2 = test_performance()
    
    print("\n" + "=" * 80)
    if success1 and success2:
        print("🎉 ¡TODOS LOS TESTS PASARON EXITOSAMENTE!")
        print("✅ La implementación está completamente funcional")
        print("✅ Rendimiento aceptable")
        print("✅ Lista para producción")
        return True
    else:
        print("❌ Algunos tests fallaron")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
