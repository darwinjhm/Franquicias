"""
Controlador REST para Franquicia
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..services.franquicia_service import FranquiciaService
from ..schemas import (
    FranquiciaCreate, 
    FranquiciaUpdate, 
    FranquiciaResponse, 
    ReporteStockResponse,
    ErrorResponse
)

router = APIRouter(prefix="/api/franquicias", tags=["franquicias"])


@router.post("/", response_model=FranquiciaResponse, status_code=status.HTTP_201_CREATED)
async def crear_franquicia(
    franquicia_data: FranquiciaCreate,
    db: Session = Depends(get_db)
):
    """
    Crea una nueva franquicia.
    
    - **nombre**: Nombre de la franquicia (requerido)
    """
    try:
        service = FranquiciaService(db)
        franquicia = service.crear_franquicia(franquicia_data.nombre)
        return FranquiciaResponse.from_orm(franquicia)
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


@router.get("/{franquicia_id}", response_model=FranquiciaResponse)
async def obtener_franquicia(
    franquicia_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtiene una franquicia por ID.
    
    - **franquicia_id**: ID de la franquicia
    """
    service = FranquiciaService(db)
    franquicia = service.obtener_franquicia(franquicia_id)
    
    if not franquicia:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Franquicia con ID {franquicia_id} no encontrada"
        )
    
    return FranquiciaResponse.from_orm(franquicia)


@router.get("/", response_model=List[FranquiciaResponse])
async def obtener_todas_franquicias(db: Session = Depends(get_db)):
    """
    Obtiene todas las franquicias.
    """
    service = FranquiciaService(db)
    franquicias = service.obtener_todas_franquicias()
    return [FranquiciaResponse.from_orm(f) for f in franquicias]


@router.patch("/{franquicia_id}", response_model=FranquiciaResponse)
async def actualizar_franquicia(
    franquicia_id: int,
    franquicia_data: FranquiciaUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualiza el nombre de una franquicia.
    
    - **franquicia_id**: ID de la franquicia
    - **nombre**: Nuevo nombre de la franquicia
    """
    try:
        service = FranquiciaService(db)
        franquicia = service.actualizar_franquicia(franquicia_id, franquicia_data.nombre)
        
        if not franquicia:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Franquicia con ID {franquicia_id} no encontrada"
            )
        
        return FranquiciaResponse.from_orm(franquicia)
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


@router.delete("/{franquicia_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_franquicia(
    franquicia_id: int,
    db: Session = Depends(get_db)
):
    """
    Elimina una franquicia.
    
    - **franquicia_id**: ID de la franquicia
    """
    service = FranquiciaService(db)
    eliminada = service.eliminar_franquicia(franquicia_id)
    
    if not eliminada:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Franquicia con ID {franquicia_id} no encontrada"
        )


@router.get("/{franquicia_id}/reporte-stock", response_model=List[ReporteStockResponse])
async def obtener_reporte_stock(
    franquicia_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtiene el producto con más stock de cada sucursal de una franquicia.
    
    - **franquicia_id**: ID de la franquicia
    """
    try:
        service = FranquiciaService(db)
        reporte = service.obtener_reporte_stock(franquicia_id)
        return [ReporteStockResponse.from_orm(item) for item in reporte]
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
