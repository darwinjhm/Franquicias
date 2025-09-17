"""
Controlador REST para Sucursal
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..services.sucursal_service import SucursalService
from ..schemas import SucursalCreate, SucursalUpdate, SucursalResponse

router = APIRouter(prefix="/api/sucursales", tags=["sucursales"])


@router.post("/{sucursal_id}", response_model=SucursalResponse, status_code=status.HTTP_201_CREATED)
async def actualizar_sucursal(
    sucursal_id: int,
    sucursal_data: SucursalUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualiza el nombre de una sucursal.
    
    - **sucursal_id**: ID de la sucursal
    - **nombre**: Nuevo nombre de la sucursal
    """
    try:
        service = SucursalService(db)
        sucursal = service.actualizar_sucursal(sucursal_id, sucursal_data.nombre)
        
        if not sucursal:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Sucursal con ID {sucursal_id} no encontrada"
            )
        
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


@router.get("/{sucursal_id}", response_model=SucursalResponse)
async def obtener_sucursal(
    sucursal_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtiene una sucursal por ID.
    
    - **sucursal_id**: ID de la sucursal
    """
    service = SucursalService(db)
    sucursal = service.obtener_sucursal(sucursal_id)
    
    if not sucursal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sucursal con ID {sucursal_id} no encontrada"
        )
    
    return SucursalResponse.from_orm(sucursal)


@router.get("/", response_model=List[SucursalResponse])
async def obtener_todas_sucursales(db: Session = Depends(get_db)):
    """
    Obtiene todas las sucursales.
    """
    service = SucursalService(db)
    sucursales = service.obtener_todas_sucursales()
    return [SucursalResponse.from_orm(s) for s in sucursales]


@router.delete("/{sucursal_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_sucursal(
    sucursal_id: int,
    db: Session = Depends(get_db)
):
    """
    Elimina una sucursal.
    
    - **sucursal_id**: ID de la sucursal
    """
    service = SucursalService(db)
    eliminada = service.eliminar_sucursal(sucursal_id)
    
    if not eliminada:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sucursal con ID {sucursal_id} no encontrada"
        )
