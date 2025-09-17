"""
Controlador REST para operaciones de Productos en Sucursales
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..services.producto_service import ProductoService
from ..schemas import ProductoCreate, ProductoResponse

router = APIRouter(prefix="/api/sucursales", tags=["sucursales-productos"])


@router.post("/{sucursal_id}/productos", response_model=ProductoResponse, status_code=status.HTTP_201_CREATED)
async def agregar_producto(
    sucursal_id: int,
    producto_data: ProductoCreate,
    db: Session = Depends(get_db)
):
    """
    Agrega un producto a una sucursal.
    
    - **sucursal_id**: ID de la sucursal
    - **nombre**: Nombre del producto
    - **cantidad_stock**: Cantidad en stock
    """
    try:
        service = ProductoService(db)
        producto = service.crear_producto(
            producto_data.nombre, 
            producto_data.cantidad_stock, 
            sucursal_id
        )
        return ProductoResponse.from_orm(producto)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )


@router.get("/{sucursal_id}/productos", response_model=List[ProductoResponse])
async def obtener_productos_por_sucursal(
    sucursal_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtiene todos los productos de una sucursal.
    
    - **sucursal_id**: ID de la sucursal
    """
    try:
        service = ProductoService(db)
        productos = service.obtener_productos_por_sucursal(sucursal_id)
        return [ProductoResponse.from_orm(p) for p in productos]
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )
