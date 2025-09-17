"""
Servicio de lógica de negocio para Sucursal
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from ..repositories.franquicia_repository import FranquiciaRepository
from ..repositories.sucursal_repository import SucursalRepository
from ..models.sucursal import Sucursal


class SucursalService:
    """Servicio para lógica de negocio de Sucursal"""

    def __init__(self, db: Session):
        self.db = db
        self.franquicia_repo = FranquiciaRepository(db)
        self.sucursal_repo = SucursalRepository(db)

    def crear_sucursal(self, nombre: str, franquicia_id: int) -> Sucursal:
        """Crea una nueva sucursal en una franquicia"""
        # Validar que el nombre no esté vacío
        if not nombre or not nombre.strip():
            raise ValueError("El nombre de la sucursal no puede estar vacío")
        
        # Validar que la franquicia exista
        franquicia = self.franquicia_repo.get_by_id(franquicia_id)
        if not franquicia:
            raise ValueError(f"Franquicia con ID {franquicia_id} no encontrada")
        
        # Validar que no exista una sucursal con el mismo nombre en la franquicia
        sucursal_existente = self.sucursal_repo.get_by_name_and_franquicia(nombre.strip(), franquicia_id)
        if sucursal_existente:
            raise ValueError(f"Ya existe una sucursal con el nombre '{nombre}' en esta franquicia")
        
        return self.sucursal_repo.create(nombre.strip(), franquicia_id)

    def obtener_sucursal(self, sucursal_id: int) -> Optional[Sucursal]:
        """Obtiene una sucursal por ID"""
        return self.sucursal_repo.get_by_id(sucursal_id)

    def obtener_sucursales_por_franquicia(self, franquicia_id: int) -> List[Sucursal]:
        """Obtiene todas las sucursales de una franquicia"""
        # Validar que la franquicia exista
        if not self.franquicia_repo.exists(franquicia_id):
            raise ValueError(f"Franquicia con ID {franquicia_id} no encontrada")
        
        return self.sucursal_repo.get_by_franquicia_id(franquicia_id)

    def obtener_todas_sucursales(self) -> List[Sucursal]:
        """Obtiene todas las sucursales"""
        return self.sucursal_repo.get_all()

    def actualizar_sucursal(self, sucursal_id: int, nombre: str) -> Optional[Sucursal]:
        """Actualiza el nombre de una sucursal"""
        # Validar que la sucursal exista
        sucursal = self.sucursal_repo.get_by_id(sucursal_id)
        if not sucursal:
            return None
        
        # Validar que el nombre no esté vacío
        if not nombre or not nombre.strip():
            raise ValueError("El nombre de la sucursal no puede estar vacío")
        
        # Validar que no exista otra sucursal con el mismo nombre en la misma franquicia
        sucursal_existente = self.sucursal_repo.get_by_name_and_franquicia(nombre.strip(), sucursal.franquicia_id)
        if sucursal_existente and sucursal_existente.id != sucursal_id:
            raise ValueError(f"Ya existe una sucursal con el nombre '{nombre}' en esta franquicia")
        
        return self.sucursal_repo.update(sucursal_id, nombre.strip())

    def eliminar_sucursal(self, sucursal_id: int) -> bool:
        """Elimina una sucursal"""
        # Validar que la sucursal exista
        if not self.sucursal_repo.exists(sucursal_id):
            return False
        
        return self.sucursal_repo.delete(sucursal_id)

    def sucursal_existe(self, sucursal_id: int) -> bool:
        """Verifica si una sucursal existe"""
        return self.sucursal_repo.exists(sucursal_id)

    def sucursal_pertenece_a_franquicia(self, sucursal_id: int, franquicia_id: int) -> bool:
        """Verifica si una sucursal pertenece a una franquicia específica"""
        return self.sucursal_repo.belongs_to_franquicia(sucursal_id, franquicia_id)
