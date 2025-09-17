"""
Controlador REST para operaciones de Sucursales en Franquicias
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..services.sucursal_service import SucursalService
from ..schemas import SucursalCreate, SucursalResponse

router = APIRouter(prefix="/api/franquicias", tags=["franquicias-sucursales"])


@router.post("/{franquicia_id}/sucursales", response_model=SucursalResponse, status_code=status.HTTP_201_CREATED)
async def agregar_sucursal(
    franquicia_id: int,
    sucursal_data: SucursalCreate,
    db: Session = Depends(get_db)
):
    """
    Agrega una sucursal a una franquicia.
    
    - **franquicia_id**: ID de la franquicia
    - **nombre**: Nombre de la sucursal
    """
    try:
        service = SucursalService(db)
        sucursal = service.crear_sucursal(sucursal_data.nombre, franquicia_id)
        return SucursalResponse.from_orm(sucursal)
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


@router.get("/{franquicia_id}/sucursales", response_model=List[SucursalResponse])
async def obtener_sucursales_por_franquicia(
    franquicia_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtiene todas las sucursales de una franquicia.
    
    - **franquicia_id**: ID de la franquicia
    """
    try:
        service = SucursalService(db)
        sucursales = service.obtener_sucursales_por_franquicia(franquicia_id)
        return [SucursalResponse.from_orm(s) for s in sucursales]
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
