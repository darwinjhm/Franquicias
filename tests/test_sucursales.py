"""
Tests para el controlador de Sucursales
"""

import pytest
from fastapi import status


class TestSucursalController:
    """Tests para el controlador de Sucursales"""

    def test_agregar_sucursal_a_franquicia(self, client, sample_franquicia_data, sample_sucursal_data):
        """Test agregar sucursal a franquicia exitosamente"""
        # Crear franquicia
        franquicia_response = client.post("/api/franquicias/", json=sample_franquicia_data)
        franquicia_id = franquicia_response.json()["id"]
        
        # Agregar sucursal
        response = client.post(f"/api/franquicias/{franquicia_id}/sucursales", json=sample_sucursal_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["nombre"] == sample_sucursal_data["nombre"]
        assert data["franquicia_id"] == franquicia_id
        assert "id" in data

    def test_agregar_sucursal_franquicia_no_existe(self, client, sample_sucursal_data):
        """Test agregar sucursal a franquicia que no existe"""
        response = client.post("/api/franquicias/999/sucursales", json=sample_sucursal_data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Franquicia con ID 999 no encontrada" in response.json()["detail"]

    def test_agregar_sucursal_nombre_duplicado(self, client, sample_franquicia_data, sample_sucursal_data):
        """Test agregar sucursal con nombre duplicado en la misma franquicia"""
        # Crear franquicia
        franquicia_response = client.post("/api/franquicias/", json=sample_franquicia_data)
        franquicia_id = franquicia_response.json()["id"]
        
        # Agregar primera sucursal
        client.post(f"/api/franquicias/{franquicia_id}/sucursales", json=sample_sucursal_data)
        
        # Intentar agregar segunda sucursal con mismo nombre
        response = client.post(f"/api/franquicias/{franquicia_id}/sucursales", json=sample_sucursal_data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Ya existe una sucursal" in response.json()["detail"]

    def test_obtener_sucursales_por_franquicia(self, client, sample_franquicia_data, sample_sucursal_data):
        """Test obtener sucursales de una franquicia"""
        # Crear franquicia
        franquicia_response = client.post("/api/franquicias/", json=sample_franquicia_data)
        franquicia_id = franquicia_response.json()["id"]
        
        # Agregar sucursales
        client.post(f"/api/franquicias/{franquicia_id}/sucursales", json=sample_sucursal_data)
        client.post(f"/api/franquicias/{franquicia_id}/sucursales", json={"nombre": "Otra Sucursal"})
        
        # Obtener sucursales
        response = client.get(f"/api/franquicias/{franquicia_id}/sucursales")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 2

    def test_obtener_sucursales_franquicia_no_existe(self, client):
        """Test obtener sucursales de franquicia que no existe"""
        response = client.get("/api/franquicias/999/sucursales")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_actualizar_sucursal(self, client, sample_franquicia_data, sample_sucursal_data):
        """Test actualizar sucursal"""
        # Crear franquicia y sucursal
        franquicia_response = client.post("/api/franquicias/", json=sample_franquicia_data)
        franquicia_id = franquicia_response.json()["id"]
        
        sucursal_response = client.post(f"/api/franquicias/{franquicia_id}/sucursales", json=sample_sucursal_data)
        sucursal_id = sucursal_response.json()["id"]
        
        # Actualizar sucursal
        update_data = {"nombre": "Sucursal Actualizada"}
        response = client.patch(f"/api/sucursales/{sucursal_id}", json=update_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["nombre"] == update_data["nombre"]

    def test_actualizar_sucursal_no_existe(self, client):
        """Test actualizar sucursal que no existe"""
        update_data = {"nombre": "Sucursal Actualizada"}
        response = client.patch("/api/sucursales/999", json=update_data)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_eliminar_sucursal(self, client, sample_franquicia_data, sample_sucursal_data):
        """Test eliminar sucursal"""
        # Crear franquicia y sucursal
        franquicia_response = client.post("/api/franquicias/", json=sample_franquicia_data)
        franquicia_id = franquicia_response.json()["id"]
        
        sucursal_response = client.post(f"/api/franquicias/{franquicia_id}/sucursales", json=sample_sucursal_data)
        sucursal_id = sucursal_response.json()["id"]
        
        # Eliminar sucursal
        response = client.delete(f"/api/sucursales/{sucursal_id}")
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Verificar que se eliminó
        get_response = client.get(f"/api/sucursales/{sucursal_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    def test_eliminar_sucursal_no_existe(self, client):
        """Test eliminar sucursal que no existe"""
        response = client.delete("/api/sucursales/999")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
