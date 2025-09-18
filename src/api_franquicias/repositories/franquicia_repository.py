"""
Repositorio para operaciones de base de datos de Franquicia.

Este módulo implementa el patrón Repository para la entidad Franquicia,
proporcionando una capa de abstracción entre la lógica de negocio
y las operaciones de persistencia de datos. La franquicia es la entidad
raíz del sistema de gestión.

Autor: Darwin Hurtado
Fecha: 2024
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from ..models.franquicia import Franquicia


class FranquiciaRepository:
    """
    Repositorio para operaciones CRUD de Franquicia.
    
    Esta clase encapsula todas las operaciones de base de datos relacionadas
    con la entidad Franquicia, que es la entidad raíz del sistema de gestión
    de franquicias, sucursales y productos.
    
    Attributes:
        db (Session): Sesión de SQLAlchemy para operaciones de base de datos
    """

    def __init__(self, db: Session):
        """
        Inicializa el repositorio con una sesión de base de datos.
        
        Args:
            db (Session): Sesión de SQLAlchemy activa para operaciones de BD
        """
        self.db = db

    def create(self, nombre: str) -> Franquicia:
        """
        Crea una nueva franquicia en la base de datos.
        
        Args:
            nombre (str): Nombre único de la franquicia
            
        Returns:
            Franquicia: Instancia de la franquicia creada con ID asignado
            
        Raises:
            IntegrityError: Si ya existe una franquicia con el mismo nombre
        """
        franquicia = Franquicia(nombre=nombre)
        self.db.add(franquicia)
        self.db.commit()
        self.db.refresh(franquicia)
        return franquicia

    def get_by_id(self, franquicia_id: int) -> Optional[Franquicia]:
        """
        Obtiene una franquicia por su identificador único.
        
        Args:
            franquicia_id (int): ID único de la franquicia
            
        Returns:
            Optional[Franquicia]: La franquicia encontrada o None si no existe
        """
        return self.db.query(Franquicia).filter(Franquicia.id == franquicia_id).first()

    def get_by_name(self, nombre: str) -> Optional[Franquicia]:
        """
        Busca una franquicia por su nombre.
        
        Este método es útil para validar nombres únicos y para búsquedas
        por nombre en lugar de ID.
        
        Args:
            nombre (str): Nombre de la franquicia a buscar
            
        Returns:
            Optional[Franquicia]: La franquicia encontrada o None si no existe
        """
        return self.db.query(Franquicia).filter(Franquicia.nombre == nombre).first()

    def get_all(self) -> List[Franquicia]:
        """
        Obtiene todas las franquicias del sistema.
        
        Returns:
            List[Franquicia]: Lista completa de franquicias ordenadas por ID
            
        Note:
            Este método puede ser costoso en sistemas con muchas franquicias.
            Considera usar paginación para grandes volúmenes de datos.
        """
        return self.db.query(Franquicia).all()

    def update(self, franquicia_id: int, nombre: str) -> Optional[Franquicia]:
        """
        Actualiza el nombre de una franquicia existente.
        
        Args:
            franquicia_id (int): ID de la franquicia a actualizar
            nombre (str): Nuevo nombre para la franquicia
            
        Returns:
            Optional[Franquicia]: La franquicia actualizada o None si no existe
            
        Raises:
            IntegrityError: Si el nuevo nombre ya existe en otra franquicia
        """
        franquicia = self.get_by_id(franquicia_id)
        if franquicia:
            franquicia.nombre = nombre
            self.db.commit()
            self.db.refresh(franquicia)
        return franquicia

    def delete(self, franquicia_id: int) -> bool:
        """
        Elimina una franquicia de la base de datos.
        
        Args:
            franquicia_id (int): ID de la franquicia a eliminar
            
        Returns:
            bool: True si la franquicia fue eliminada, False si no existe
            
        Note:
            Esta operación también eliminará todas las sucursales y productos
            asociados a la franquicia debido a las restricciones de clave foránea.
        """
        franquicia = self.get_by_id(franquicia_id)
        if franquicia:
            self.db.delete(franquicia)
            self.db.commit()
            return True
        return False

    def exists(self, franquicia_id: int) -> bool:
        """
        Verifica si una franquicia existe en la base de datos.
        
        Args:
            franquicia_id (int): ID de la franquicia a verificar
            
        Returns:
            bool: True si la franquicia existe, False en caso contrario
        """
        return self.db.query(Franquicia).filter(Franquicia.id == franquicia_id).first() is not None
