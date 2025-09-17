"""
Tests para el reporte de stock
"""

import pytest
from fastapi import status


class TestReporteStock:
    """Tests para el reporte de stock"""

    def test_reporte_stock_con_productos(self, client, sample_franquicia_data, sample_sucursal_data):
        """Test reporte de stock con productos en múltiples sucursales"""
        # Crear franquicia
        franquicia_response = client.post("/api/franquicias/", json=sample_franquicia_data)
        franquicia_id = franquicia_response.json()["id"]
        
        # Crear sucursales
        sucursal1_response = client.post(f"/api/franquicias/{franquicia_id}/sucursales", json=sample_sucursal_data)
        sucursal1_id = sucursal1_response.json()["id"]
        
        sucursal2_response = client.post(f"/api/franquicias/{franquicia_id}/sucursales", json={"nombre": "Sucursal 2"})
        sucursal2_id = sucursal2_response.json()["id"]
        
        # Agregar productos a sucursal 1
        client.post(f"/api/sucursales/{sucursal1_id}/productos", json={"nombre": "Producto A", "cantidad_stock": 100})
        client.post(f"/api/sucursales/{sucursal1_id}/productos", json={"nombre": "Producto B", "cantidad_stock": 50})
        
        # Agregar productos a sucursal 2
        client.post(f"/api/sucursales/{sucursal2_id}/productos", json={"nombre": "Producto C", "cantidad_stock": 200})
        client.post(f"/api/sucursales/{sucursal2_id}/productos", json={"nombre": "Producto D", "cantidad_stock": 75})
        
        # Obtener reporte de stock
        response = client.get(f"/api/franquicias/{franquicia_id}/reporte-stock")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        # Debe tener 2 productos (uno por sucursal con mayor stock)
        assert len(data) == 2
        
        # Verificar que cada sucursal tiene su producto con mayor stock
        sucursales_en_reporte = {item["sucursal_id"] for item in data}
        assert sucursal1_id in sucursales_en_reporte
        assert sucursal2_id in sucursales_en_reporte
        
        # Verificar que los productos son los de mayor stock
        for item in data:
            if item["sucursal_id"] == sucursal1_id:
                assert item["producto_nombre"] == "Producto A"
                assert item["cantidad_stock"] == 100
            elif item["sucursal_id"] == sucursal2_id:
                assert item["producto_nombre"] == "Producto C"
                assert item["cantidad_stock"] == 200

    def test_reporte_stock_sucursal_sin_productos(self, client, sample_franquicia_data, sample_sucursal_data):
        """Test reporte de stock con sucursal sin productos"""
        # Crear franquicia
        franquicia_response = client.post("/api/franquicias/", json=sample_franquicia_data)
        franquicia_id = franquicia_response.json()["id"]
        
        # Crear sucursal sin productos
        client.post(f"/api/franquicias/{franquicia_id}/sucursales", json=sample_sucursal_data)
        
        # Obtener reporte de stock
        response = client.get(f"/api/franquicias/{franquicia_id}/reporte-stock")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data == []

    def test_reporte_stock_productos_mismo_stock(self, client, sample_franquicia_data, sample_sucursal_data):
        """Test reporte de stock con productos que tienen el mismo stock máximo"""
        # Crear franquicia y sucursal
        franquicia_response = client.post("/api/franquicias/", json=sample_franquicia_data)
        franquicia_id = franquicia_response.json()["id"]
        
        sucursal_response = client.post(f"/api/franquicias/{franquicia_id}/sucursales", json=sample_sucursal_data)
        sucursal_id = sucursal_response.json()["id"]
        
        # Agregar productos con el mismo stock máximo
        client.post(f"/api/sucursales/{sucursal_id}/productos", json={"nombre": "Producto A", "cantidad_stock": 100})
        client.post(f"/api/sucursales/{sucursal_id}/productos", json={"nombre": "Producto B", "cantidad_stock": 100})
        client.post(f"/api/sucursales/{sucursal_id}/productos", json={"nombre": "Producto C", "cantidad_stock": 50})
        
        # Obtener reporte de stock
        response = client.get(f"/api/franquicias/{franquicia_id}/reporte-stock")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        # Debe tener 2 productos (los que tienen el stock máximo)
        assert len(data) == 2
        
        # Verificar que ambos productos tienen stock de 100
        for item in data:
            assert item["cantidad_stock"] == 100
            assert item["producto_nombre"] in ["Producto A", "Producto B"]

    def test_reporte_stock_franquicia_no_existe(self, client):
        """Test reporte de stock para franquicia que no existe"""
        response = client.get("/api/franquicias/999/reporte-stock")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
