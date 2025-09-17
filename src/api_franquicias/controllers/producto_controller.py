"""
Controlador REST para Producto
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..services.producto_service import ProductoService
from ..schemas import (
    ProductoCreate, 
    ProductoUpdate, 
    StockUpdate, 
    ProductoResponse
)

router = APIRouter(prefix="/api/productos", tags=["productos"])


@router.post("/{producto_id}", response_model=ProductoResponse, status_code=status.HTTP_201_CREATED)
async def actualizar_producto(
    producto_id: int,
    producto_data: ProductoUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualiza el nombre de un producto.
    
    - **producto_id**: ID del producto
    - **nombre**: Nuevo nombre del producto
    """
    try:
        service = ProductoService(db)
        producto = service.actualizar_producto(producto_id, producto_data.nombre)
        
        if not producto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto con ID {producto_id} no encontrado"
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


@router.patch("/{producto_id}/stock", response_model=ProductoResponse)
async def actualizar_stock(
    producto_id: int,
    stock_data: StockUpdate,
    db: Session = Depends(get_db)
):
    """
    Modifica el stock de un producto.
    
    - **producto_id**: ID del producto
    - **stock**: Nueva cantidad en stock
    """
    try:
        service = ProductoService(db)
        producto = service.actualizar_stock(producto_id, stock_data.stock)
        
        if not producto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto con ID {producto_id} no encontrado"
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


@router.get("/{producto_id}", response_model=ProductoResponse)
async def obtener_producto(
    producto_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtiene un producto por ID.
    
    - **producto_id**: ID del producto
    """
    service = ProductoService(db)
    producto = service.obtener_producto(producto_id)
    
    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con ID {producto_id} no encontrado"
        )
    
    return ProductoResponse.from_orm(producto)


@router.get("/", response_model=List[ProductoResponse])
async def obtener_todos_productos(db: Session = Depends(get_db)):
    """
    Obtiene todos los productos.
    """
    service = ProductoService(db)
    productos = service.obtener_todos_productos()
    return [ProductoResponse.from_orm(p) for p in productos]


@router.delete("/{producto_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_producto(
    producto_id: int,
    db: Session = Depends(get_db)
):
    """
    Elimina un producto.
    
    - **producto_id**: ID del producto
    """
    service = ProductoService(db)
    eliminado = service.eliminar_producto(producto_id)
    
    if not eliminado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con ID {producto_id} no encontrado"
        )
