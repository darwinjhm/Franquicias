"""
Esquemas Pydantic para validación de datos de entrada y salida
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any
from datetime import datetime


# Esquemas de entrada (request)
class FranquiciaCreate(BaseModel):
    """Esquema para crear una franquicia"""
    nombre: str = Field(..., min_length=1, max_length=255, description="Nombre de la franquicia")


class FranquiciaUpdate(BaseModel):
    """Esquema para actualizar una franquicia"""
    nombre: str = Field(..., min_length=1, max_length=255, description="Nuevo nombre de la franquicia")


class SucursalCreate(BaseModel):
    """Esquema para crear una sucursal"""
    nombre: str = Field(..., min_length=1, max_length=255, description="Nombre de la sucursal")


class SucursalUpdate(BaseModel):
    """Esquema para actualizar una sucursal"""
    nombre: str = Field(..., min_length=1, max_length=255, description="Nuevo nombre de la sucursal")


class ProductoCreate(BaseModel):
    """Esquema para crear un producto"""
    nombre: str = Field(..., min_length=1, max_length=255, description="Nombre del producto")
    cantidad_stock: int = Field(..., ge=0, description="Cantidad en stock")


class ProductoUpdate(BaseModel):
    """Esquema para actualizar un producto"""
    nombre: str = Field(..., min_length=1, max_length=255, description="Nuevo nombre del producto")


class StockUpdate(BaseModel):
    """Esquema para actualizar el stock de un producto"""
    stock: int = Field(..., ge=0, description="Nueva cantidad en stock")


# Esquemas de salida (response)
class ProductoResponse(BaseModel):
    """Esquema de respuesta para un producto"""
    id: int
    nombre: str
    cantidad_stock: int
    sucursal_id: int
    fecha_creacion: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class SucursalResponse(BaseModel):
    """Esquema de respuesta para una sucursal"""
    id: int
    nombre: str
    franquicia_id: int
    fecha_creacion: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None
    productos: List[ProductoResponse] = []

    model_config = ConfigDict(from_attributes=True)


class FranquiciaResponse(BaseModel):
    """Esquema de respuesta para una franquicia"""
    id: int
    nombre: str
    fecha_creacion: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None
    sucursales: List[SucursalResponse] = []

    model_config = ConfigDict(from_attributes=True)


class ReporteStockResponse(BaseModel):
    """Esquema de respuesta para el reporte de stock"""
    producto_id: int
    producto_nombre: str
    cantidad_stock: int
    sucursal_id: int
    sucursal_nombre: str


class ErrorResponse(BaseModel):
    """Esquema de respuesta para errores"""
    error: str
    detail: Optional[str] = None
