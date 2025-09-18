"""
Repositorio para operaciones de base de datos de Sucursal.

Este módulo implementa el patrón Repository para la entidad Sucursal,
proporcionando una capa de abstracción entre la lógica de negocio
y las operaciones de persistencia de datos.

Autor: Darwin Hurtado
Fecha: 2024
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from ..models.sucursal import Sucursal


class SucursalRepository:
    """
    Repositorio para operaciones CRUD de Sucursal.
    
    Esta clase encapsula todas las operaciones de base de datos relacionadas
    con la entidad Sucursal, siguiendo el patrón Repository para mantener
    la separación de responsabilidades y facilitar las pruebas unitarias.
    
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

    def create(self, nombre: str, franquicia_id: int) -> Sucursal:
        """
        Crea una nueva sucursal en la base de datos.
        
        Args:
            nombre (str): Nombre único de la sucursal
            franquicia_id (int): ID de la franquicia a la que pertenece
            
        Returns:
            Sucursal: Instancia de la sucursal creada con ID asignado
            
        Raises:
            IntegrityError: Si ya existe una sucursal con el mismo nombre
                          en la misma franquicia
        """
        sucursal = Sucursal(nombre=nombre, franquicia_id=franquicia_id)
        self.db.add(sucursal)
        self.db.commit()
        self.db.refresh(sucursal)
        return sucursal

    def get_by_id(self, sucursal_id: int) -> Optional[Sucursal]:
        """
        Obtiene una sucursal por su identificador único.
        
        Args:
            sucursal_id (int): ID único de la sucursal
            
        Returns:
            Optional[Sucursal]: La sucursal encontrada o None si no existe
        """
        return self.db.query(Sucursal).filter(Sucursal.id == sucursal_id).first()

    def get_by_franquicia_id(self, franquicia_id: int) -> List[Sucursal]:
        """
        Obtiene todas las sucursales que pertenecen a una franquicia específica.
        
        Args:
            franquicia_id (int): ID de la franquicia
            
        Returns:
            List[Sucursal]: Lista de sucursales de la franquicia (puede estar vacía)
        """
        return self.db.query(Sucursal).filter(Sucursal.franquicia_id == franquicia_id).all()

    def get_by_name_and_franquicia(self, nombre: str, franquicia_id: int) -> Optional[Sucursal]:
        """
        Busca una sucursal por nombre dentro de una franquicia específica.
        
        Este método es útil para validar nombres únicos dentro del contexto
        de una franquicia, ya que el mismo nombre puede existir en diferentes
        franquicias.
        
        Args:
            nombre (str): Nombre de la sucursal a buscar
            franquicia_id (int): ID de la franquicia donde buscar
            
        Returns:
            Optional[Sucursal]: La sucursal encontrada o None si no existe
        """
        return self.db.query(Sucursal).filter(
            and_(Sucursal.nombre == nombre, Sucursal.franquicia_id == franquicia_id)
        ).first()

    def get_all(self) -> List[Sucursal]:
        """
        Obtiene todas las sucursales del sistema.
        
        Returns:
            List[Sucursal]: Lista completa de sucursales ordenadas por ID
            
        Note:
            Este método puede ser costoso en sistemas con muchas sucursales.
            Considera usar paginación para grandes volúmenes de datos.
        """
        return self.db.query(Sucursal).all()

    def update(self, sucursal_id: int, nombre: str) -> Optional[Sucursal]:
        """
        Actualiza el nombre de una sucursal existente.
        
        Args:
            sucursal_id (int): ID de la sucursal a actualizar
            nombre (str): Nuevo nombre para la sucursal
            
        Returns:
            Optional[Sucursal]: La sucursal actualizada o None si no existe
            
        Raises:
            IntegrityError: Si el nuevo nombre ya existe en la misma franquicia
        """
        sucursal = self.get_by_id(sucursal_id)
        if sucursal:
            sucursal.nombre = nombre
            self.db.commit()
            self.db.refresh(sucursal)
        return sucursal

    def delete(self, sucursal_id: int) -> bool:
        """
        Elimina una sucursal de la base de datos.
        
        Args:
            sucursal_id (int): ID de la sucursal a eliminar
            
        Returns:
            bool: True si la sucursal fue eliminada, False si no existe
            
        Note:
            Esta operación también eliminará todos los productos asociados
            a la sucursal debido a las restricciones de clave foránea.
        """
        sucursal = self.get_by_id(sucursal_id)
        if sucursal:
            self.db.delete(sucursal)
            self.db.commit()
            return True
        return False

    def exists(self, sucursal_id: int) -> bool:
        """
        Verifica si una sucursal existe en la base de datos.
        
        Args:
            sucursal_id (int): ID de la sucursal a verificar
            
        Returns:
            bool: True si la sucursal existe, False en caso contrario
        """
        return self.db.query(Sucursal).filter(Sucursal.id == sucursal_id).first() is not None

    def belongs_to_franquicia(self, sucursal_id: int, franquicia_id: int) -> bool:
        """
        Verifica si una sucursal pertenece a una franquicia específica.
        
        Este método es útil para validar permisos y asegurar que las
        operaciones se realicen en el contexto correcto.
        
        Args:
            sucursal_id (int): ID de la sucursal a verificar
            franquicia_id (int): ID de la franquicia esperada
            
        Returns:
            bool: True si la sucursal pertenece a la franquicia, False en caso contrario
        """
        sucursal = self.db.query(Sucursal).filter(
            and_(Sucursal.id == sucursal_id, Sucursal.franquicia_id == franquicia_id)
        ).first()
        return sucursal is not None
