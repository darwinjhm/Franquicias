"""
Servicio de lógica de negocio para Franquicia
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from ..repositories.franquicia_repository import FranquiciaRepository
from ..repositories.sucursal_repository import SucursalRepository
from ..repositories.producto_repository import ProductoRepository
from ..models.franquicia import Franquicia


class FranquiciaService:
    """Servicio para lógica de negocio de Franquicia"""

    def __init__(self, db: Session):
        self.db = db
        self.franquicia_repo = FranquiciaRepository(db)
        self.sucursal_repo = SucursalRepository(db)
        self.producto_repo = ProductoRepository(db)

    def crear_franquicia(self, nombre: str) -> Franquicia:
        """Crea una nueva franquicia"""
        # Validar que el nombre no esté vacío
        if not nombre or not nombre.strip():
            raise ValueError("El nombre de la franquicia no puede estar vacío")
        
        # Validar que no exista una franquicia con el mismo nombre
        franquicia_existente = self.franquicia_repo.get_by_name(nombre.strip())
        if franquicia_existente:
            raise ValueError(f"Ya existe una franquicia con el nombre '{nombre}'")
        
        return self.franquicia_repo.create(nombre.strip())

    def obtener_franquicia(self, franquicia_id: int) -> Optional[Franquicia]:
        """Obtiene una franquicia por ID"""
        return self.franquicia_repo.get_by_id(franquicia_id)

    def obtener_todas_franquicias(self) -> List[Franquicia]:
        """Obtiene todas las franquicias"""
        return self.franquicia_repo.get_all()

    def actualizar_franquicia(self, franquicia_id: int, nombre: str) -> Optional[Franquicia]:
        """Actualiza el nombre de una franquicia"""
        # Validar que la franquicia exista
        franquicia = self.franquicia_repo.get_by_id(franquicia_id)
        if not franquicia:
            return None
        
        # Validar que el nombre no esté vacío
        if not nombre or not nombre.strip():
            raise ValueError("El nombre de la franquicia no puede estar vacío")
        
        # Validar que no exista otra franquicia con el mismo nombre
        franquicia_existente = self.franquicia_repo.get_by_name(nombre.strip())
        if franquicia_existente and franquicia_existente.id != franquicia_id:
            raise ValueError(f"Ya existe una franquicia con el nombre '{nombre}'")
        
        return self.franquicia_repo.update(franquicia_id, nombre.strip())

    def eliminar_franquicia(self, franquicia_id: int) -> bool:
        """Elimina una franquicia"""
        # Validar que la franquicia exista
        if not self.franquicia_repo.exists(franquicia_id):
            return False
        
        return self.franquicia_repo.delete(franquicia_id)

    def obtener_reporte_stock(self, franquicia_id: int) -> List[Dict[str, Any]]:
        """
        Obtiene el producto con más stock de cada sucursal de una franquicia.
        Retorna una lista de diccionarios con información del producto y sucursal.
        """
        # Validar que la franquicia exista
        franquicia = self.franquicia_repo.get_by_id(franquicia_id)
        if not franquicia:
            raise ValueError(f"Franquicia con ID {franquicia_id} no encontrada")
        
        return self.producto_repo.get_max_stock_by_sucursal(franquicia_id)

    def franquicia_existe(self, franquicia_id: int) -> bool:
        """Verifica si una franquicia existe"""
        return self.franquicia_repo.exists(franquicia_id)
