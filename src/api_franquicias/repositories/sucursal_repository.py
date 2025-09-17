"""
Repositorio para operaciones de Sucursal
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from ..models.sucursal import Sucursal


class SucursalRepository:
    """Repositorio para operaciones CRUD de Sucursal"""

    def __init__(self, db: Session):
        self.db = db

    def create(self, nombre: str, franquicia_id: int) -> Sucursal:
        """Crea una nueva sucursal"""
        sucursal = Sucursal(nombre=nombre, franquicia_id=franquicia_id)
        self.db.add(sucursal)
        self.db.commit()
        self.db.refresh(sucursal)
        return sucursal

    def get_by_id(self, sucursal_id: int) -> Optional[Sucursal]:
        """Obtiene una sucursal por ID"""
        return self.db.query(Sucursal).filter(Sucursal.id == sucursal_id).first()

    def get_by_franquicia_id(self, franquicia_id: int) -> List[Sucursal]:
        """Obtiene todas las sucursales de una franquicia"""
        return self.db.query(Sucursal).filter(Sucursal.franquicia_id == franquicia_id).all()

    def get_by_name_and_franquicia(self, nombre: str, franquicia_id: int) -> Optional[Sucursal]:
        """Obtiene una sucursal por nombre y franquicia"""
        return self.db.query(Sucursal).filter(
            and_(Sucursal.nombre == nombre, Sucursal.franquicia_id == franquicia_id)
        ).first()

    def get_all(self) -> List[Sucursal]:
        """Obtiene todas las sucursales"""
        return self.db.query(Sucursal).all()

    def update(self, sucursal_id: int, nombre: str) -> Optional[Sucursal]:
        """Actualiza el nombre de una sucursal"""
        sucursal = self.get_by_id(sucursal_id)
        if sucursal:
            sucursal.nombre = nombre
            self.db.commit()
            self.db.refresh(sucursal)
        return sucursal

    def delete(self, sucursal_id: int) -> bool:
        """Elimina una sucursal"""
        sucursal = self.get_by_id(sucursal_id)
        if sucursal:
            self.db.delete(sucursal)
            self.db.commit()
            return True
        return False

    def exists(self, sucursal_id: int) -> bool:
        """Verifica si una sucursal existe"""
        return self.db.query(Sucursal).filter(Sucursal.id == sucursal_id).first() is not None

    def belongs_to_franquicia(self, sucursal_id: int, franquicia_id: int) -> bool:
        """Verifica si una sucursal pertenece a una franquicia específica"""
        sucursal = self.db.query(Sucursal).filter(
            and_(Sucursal.id == sucursal_id, Sucursal.franquicia_id == franquicia_id)
        ).first()
        return sucursal is not None
