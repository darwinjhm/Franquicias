"""
Tests para el controlador de Productos
"""

import pytest
from fastapi import status


class TestProductoController:
    """Tests para el controlador de Productos"""

    def test_agregar_producto_a_sucursal(self, client, sample_franquicia_data, sample_sucursal_data, sample_producto_data):
        """Test agregar producto a sucursal exitosamente"""
        # Crear franquicia y sucursal
        franquicia_response = client.post("/api/franquicias/", json=sample_franquicia_data)
        franquicia_id = franquicia_response.json()["id"]
        
        sucursal_response = client.post(f"/api/franquicias/{franquicia_id}/sucursales", json=sample_sucursal_data)
        sucursal_id = sucursal_response.json()["id"]
        
        # Agregar producto
        response = client.post(f"/api/sucursales/{sucursal_id}/productos", json=sample_producto_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["nombre"] == sample_producto_data["nombre"]
        assert data["cantidad_stock"] == sample_producto_data["cantidad_stock"]
        assert data["sucursal_id"] == sucursal_id
        assert "id" in data

    def test_agregar_producto_sucursal_no_existe(self, client, sample_producto_data):
        """Test agregar producto a sucursal que no existe"""
        response = client.post("/api/sucursales/999/productos", json=sample_producto_data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Sucursal con ID 999 no encontrada" in response.json()["detail"]

    def test_agregar_producto_nombre_duplicado(self, client, sample_franquicia_data, sample_sucursal_data, sample_producto_data):
        """Test agregar producto con nombre duplicado en la misma sucursal"""
        # Crear franquicia y sucursal
        franquicia_response = client.post("/api/franquicias/", json=sample_franquicia_data)
        franquicia_id = franquicia_response.json()["id"]
        
        sucursal_response = client.post(f"/api/franquicias/{franquicia_id}/sucursales", json=sample_sucursal_data)
        sucursal_id = sucursal_response.json()["id"]
        
        # Agregar primer producto
        client.post(f"/api/sucursales/{sucursal_id}/productos", json=sample_producto_data)
        
        # Intentar agregar segundo producto con mismo nombre
        response = client.post(f"/api/sucursales/{sucursal_id}/productos", json=sample_producto_data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Ya existe un producto" in response.json()["detail"]

    def test_agregar_producto_stock_negativo(self, client, sample_franquicia_data, sample_sucursal_data):
        """Test agregar producto con stock negativo"""
        # Crear franquicia y sucursal
        franquicia_response = client.post("/api/franquicias/", json=sample_franquicia_data)
        franquicia_id = franquicia_response.json()["id"]
        
        sucursal_response = client.post(f"/api/franquicias/{franquicia_id}/sucursales", json=sample_sucursal_data)
        sucursal_id = sucursal_response.json()["id"]
        
        # Intentar agregar producto con stock negativo
        producto_data = {"nombre": "Producto Test", "cantidad_stock": -10}
        response = client.post(f"/api/sucursales/{sucursal_id}/productos", json=producto_data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "La cantidad de stock no puede ser negativa" in response.json()["detail"]

    def test_obtener_productos_por_sucursal(self, client, sample_franquicia_data, sample_sucursal_data, sample_producto_data):
        """Test obtener productos de una sucursal"""
        # Crear franquicia y sucursal
        franquicia_response = client.post("/api/franquicias/", json=sample_franquicia_data)
        franquicia_id = franquicia_response.json()["id"]
        
        sucursal_response = client.post(f"/api/franquicias/{franquicia_id}/sucursales", json=sample_sucursal_data)
        sucursal_id = sucursal_response.json()["id"]
        
        # Agregar productos
        client.post(f"/api/sucursales/{sucursal_id}/productos", json=sample_producto_data)
        client.post(f"/api/sucursales/{sucursal_id}/productos", json={"nombre": "Otro Producto", "cantidad_stock": 50})
        
        # Obtener productos
        response = client.get(f"/api/sucursales/{sucursal_id}/productos")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 2

    def test_obtener_productos_sucursal_no_existe(self, client):
        """Test obtener productos de sucursal que no existe"""
        response = client.get("/api/sucursales/999/productos")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_actualizar_producto(self, client, sample_franquicia_data, sample_sucursal_data, sample_producto_data):
        """Test actualizar producto"""
        # Crear franquicia, sucursal y producto
        franquicia_response = client.post("/api/franquicias/", json=sample_franquicia_data)
        franquicia_id = franquicia_response.json()["id"]
        
        sucursal_response = client.post(f"/api/franquicias/{franquicia_id}/sucursales", json=sample_sucursal_data)
        sucursal_id = sucursal_response.json()["id"]
        
        producto_response = client.post(f"/api/sucursales/{sucursal_id}/productos", json=sample_producto_data)
        producto_id = producto_response.json()["id"]
        
        # Actualizar producto
        update_data = {"nombre": "Producto Actualizado"}
        response = client.patch(f"/api/productos/{producto_id}", json=update_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["nombre"] == update_data["nombre"]

    def test_actualizar_stock_producto(self, client, sample_franquicia_data, sample_sucursal_data, sample_producto_data):
        """Test actualizar stock de producto"""
        # Crear franquicia, sucursal y producto
        franquicia_response = client.post("/api/franquicias/", json=sample_franquicia_data)
        franquicia_id = franquicia_response.json()["id"]
        
        sucursal_response = client.post(f"/api/franquicias/{franquicia_id}/sucursales", json=sample_sucursal_data)
        sucursal_id = sucursal_response.json()["id"]
        
        producto_response = client.post(f"/api/sucursales/{sucursal_id}/productos", json=sample_producto_data)
        producto_id = producto_response.json()["id"]
        
        # Actualizar stock
        stock_data = {"stock": 200}
        response = client.patch(f"/api/productos/{producto_id}/stock", json=stock_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["cantidad_stock"] == stock_data["stock"]

    def test_actualizar_stock_negativo(self, client, sample_franquicia_data, sample_sucursal_data, sample_producto_data):
        """Test actualizar stock con valor negativo"""
        # Crear franquicia, sucursal y producto
        franquicia_response = client.post("/api/franquicias/", json=sample_franquicia_data)
        franquicia_id = franquicia_response.json()["id"]
        
        sucursal_response = client.post(f"/api/franquicias/{franquicia_id}/sucursales", json=sample_sucursal_data)
        sucursal_id = sucursal_response.json()["id"]
        
        producto_response = client.post(f"/api/sucursales/{sucursal_id}/productos", json=sample_producto_data)
        producto_id = producto_response.json()["id"]
        
        # Intentar actualizar stock con valor negativo
        stock_data = {"stock": -50}
        response = client.patch(f"/api/productos/{producto_id}/stock", json=stock_data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "La cantidad de stock no puede ser negativa" in response.json()["detail"]

    def test_eliminar_producto(self, client, sample_franquicia_data, sample_sucursal_data, sample_producto_data):
        """Test eliminar producto"""
        # Crear franquicia, sucursal y producto
        franquicia_response = client.post("/api/franquicias/", json=sample_franquicia_data)
        franquicia_id = franquicia_response.json()["id"]
        
        sucursal_response = client.post(f"/api/franquicias/{franquicia_id}/sucursales", json=sample_sucursal_data)
        sucursal_id = sucursal_response.json()["id"]
        
        producto_response = client.post(f"/api/sucursales/{sucursal_id}/productos", json=sample_producto_data)
        producto_id = producto_response.json()["id"]
        
        # Eliminar producto
        response = client.delete(f"/api/productos/{producto_id}")
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Verificar que se eliminó
        get_response = client.get(f"/api/productos/{producto_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    def test_eliminar_producto_no_existe(self, client):
        """Test eliminar producto que no existe"""
        response = client.delete("/api/productos/999")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
