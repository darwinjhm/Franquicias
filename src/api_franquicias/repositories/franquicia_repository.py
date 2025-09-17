"""
Repositorio para operaciones de Franquicia
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from ..models.franquicia import Franquicia


class FranquiciaRepository:
    """Repositorio para operaciones CRUD de Franquicia"""

    def __init__(self, db: Session):
        self.db = db

    def create(self, nombre: str) -> Franquicia:
        """Crea una nueva franquicia"""
        franquicia = Franquicia(nombre=nombre)
        self.db.add(franquicia)
        self.db.commit()
        self.db.refresh(franquicia)
        return franquicia

    def get_by_id(self, franquicia_id: int) -> Optional[Franquicia]:
        """Obtiene una franquicia por ID"""
        return self.db.query(Franquicia).filter(Franquicia.id == franquicia_id).first()

    def get_by_name(self, nombre: str) -> Optional[Franquicia]:
        """Obtiene una franquicia por nombre"""
        return self.db.query(Franquicia).filter(Franquicia.nombre == nombre).first()

    def get_all(self) -> List[Franquicia]:
        """Obtiene todas las franquicias"""
        return self.db.query(Franquicia).all()

    def update(self, franquicia_id: int, nombre: str) -> Optional[Franquicia]:
        """Actualiza el nombre de una franquicia"""
        franquicia = self.get_by_id(franquicia_id)
        if franquicia:
            franquicia.nombre = nombre
            self.db.commit()
            self.db.refresh(franquicia)
        return franquicia

    def delete(self, franquicia_id: int) -> bool:
        """Elimina una franquicia"""
        franquicia = self.get_by_id(franquicia_id)
        if franquicia:
            self.db.delete(franquicia)
            self.db.commit()
            return True
        return False

    def exists(self, franquicia_id: int) -> bool:
        """Verifica si una franquicia existe"""
        return self.db.query(Franquicia).filter(Franquicia.id == franquicia_id).first() is not None
