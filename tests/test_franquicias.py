"""
Tests para el controlador de Franquicias
"""

import pytest
from fastapi import status


class TestFranquiciaController:
    """Tests para el controlador de Franquicias"""

    def test_crear_franquicia(self, client, sample_franquicia_data):
        """Test crear franquicia exitosamente"""
        response = client.post("/api/franquicias/", json=sample_franquicia_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["nombre"] == sample_franquicia_data["nombre"]
        assert "id" in data
        assert "fecha_creacion" in data

    def test_crear_franquicia_nombre_vacio(self, client):
        """Test crear franquicia con nombre vacío"""
        response = client.post("/api/franquicias/", json={"nombre": ""})
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_crear_franquicia_nombre_duplicado(self, client, sample_franquicia_data):
        """Test crear franquicia con nombre duplicado"""
        # Crear primera franquicia
        client.post("/api/franquicias/", json=sample_franquicia_data)
        
        # Intentar crear segunda franquicia con mismo nombre
        response = client.post("/api/franquicias/", json=sample_franquicia_data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Ya existe una franquicia" in response.json()["detail"]

    def test_obtener_franquicia(self, client, sample_franquicia_data):
        """Test obtener franquicia por ID"""
        # Crear franquicia
        create_response = client.post("/api/franquicias/", json=sample_franquicia_data)
        franquicia_id = create_response.json()["id"]
        
        # Obtener franquicia
        response = client.get(f"/api/franquicias/{franquicia_id}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == franquicia_id
        assert data["nombre"] == sample_franquicia_data["nombre"]

    def test_obtener_franquicia_no_existe(self, client):
        """Test obtener franquicia que no existe"""
        response = client.get("/api/franquicias/999")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_obtener_todas_franquicias(self, client, sample_franquicia_data):
        """Test obtener todas las franquicias"""
        # Crear algunas franquicias
        client.post("/api/franquicias/", json=sample_franquicia_data)
        client.post("/api/franquicias/", json={"nombre": "Otra Franquicia"})
        
        # Obtener todas las franquicias
        response = client.get("/api/franquicias/")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 2

    def test_actualizar_franquicia(self, client, sample_franquicia_data):
        """Test actualizar franquicia"""
        # Crear franquicia
        create_response = client.post("/api/franquicias/", json=sample_franquicia_data)
        franquicia_id = create_response.json()["id"]
        
        # Actualizar franquicia
        update_data = {"nombre": "Franquicia Actualizada"}
        response = client.patch(f"/api/franquicias/{franquicia_id}", json=update_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["nombre"] == update_data["nombre"]

    def test_actualizar_franquicia_no_existe(self, client):
        """Test actualizar franquicia que no existe"""
        update_data = {"nombre": "Franquicia Actualizada"}
        response = client.patch("/api/franquicias/999", json=update_data)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_eliminar_franquicia(self, client, sample_franquicia_data):
        """Test eliminar franquicia"""
        # Crear franquicia
        create_response = client.post("/api/franquicias/", json=sample_franquicia_data)
        franquicia_id = create_response.json()["id"]
        
        # Eliminar franquicia
        response = client.delete(f"/api/franquicias/{franquicia_id}")
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Verificar que se eliminó
        get_response = client.get(f"/api/franquicias/{franquicia_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    def test_eliminar_franquicia_no_existe(self, client):
        """Test eliminar franquicia que no existe"""
        response = client.delete("/api/franquicias/999")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_reporte_stock_franquicia_vacia(self, client, sample_franquicia_data):
        """Test reporte de stock para franquicia sin sucursales"""
        # Crear franquicia
        create_response = client.post("/api/franquicias/", json=sample_franquicia_data)
        franquicia_id = create_response.json()["id"]
        
        # Obtener reporte de stock
        response = client.get(f"/api/franquicias/{franquicia_id}/reporte-stock")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data == []

    def test_reporte_stock_franquicia_no_existe(self, client):
        """Test reporte de stock para franquicia que no existe"""
        response = client.get("/api/franquicias/999/reporte-stock")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
