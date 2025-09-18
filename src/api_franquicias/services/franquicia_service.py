"""
Servicio de lógica de negocio para Franquicia.

Este módulo implementa la capa de servicios para la entidad Franquicia,
encapsulando la lógica de negocio, validaciones y coordinación entre
repositorios. Es la capa intermedia entre los controladores y los repositorios.

Autor: Darwin Hurtado
Fecha: 2024
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from ..repositories.franquicia_repository import FranquiciaRepository
from ..repositories.sucursal_repository import SucursalRepository
from ..repositories.producto_repository import ProductoRepository
from ..models.franquicia import Franquicia


class FranquiciaService:
    """
    Servicio para lógica de negocio de Franquicia.
    
    Esta clase encapsula toda la lógica de negocio relacionada con franquicias,
    incluyendo validaciones, reglas de negocio y coordinación entre repositorios.
    Actúa como la capa intermedia entre los controladores REST y los repositorios.
    
    Attributes:
        db (Session): Sesión de SQLAlchemy para operaciones de base de datos
        franquicia_repo (FranquiciaRepository): Repositorio para operaciones de franquicia
        sucursal_repo (SucursalRepository): Repositorio para operaciones de sucursal
        producto_repo (ProductoRepository): Repositorio para operaciones de producto
    """

    def __init__(self, db: Session):
        """
        Inicializa el servicio con una sesión de base de datos y repositorios.
        
        Args:
            db (Session): Sesión de SQLAlchemy activa para operaciones de BD
        """
        self.db = db
        self.franquicia_repo = FranquiciaRepository(db)
        self.sucursal_repo = SucursalRepository(db)
        self.producto_repo = ProductoRepository(db)

    def crear_franquicia(self, nombre: str) -> Franquicia:
        """
        Crea una nueva franquicia con validaciones de negocio.
        
        Este método implementa las siguientes reglas de negocio:
        - El nombre no puede estar vacío o ser solo espacios en blanco
        - El nombre debe ser único en el sistema
        - El nombre se normaliza eliminando espacios al inicio y final
        
        Args:
            nombre (str): Nombre de la franquicia a crear
            
        Returns:
            Franquicia: Instancia de la franquicia creada
            
        Raises:
            ValueError: Si el nombre está vacío o ya existe una franquicia con ese nombre
        """
        # Validar que el nombre no esté vacío
        if not nombre or not nombre.strip():
            raise ValueError("El nombre de la franquicia no puede estar vacío")
        
        # Validar que no exista una franquicia con el mismo nombre
        franquicia_existente = self.franquicia_repo.get_by_name(nombre.strip())
        if franquicia_existente:
            raise ValueError(f"Ya existe una franquicia con el nombre '{nombre}'")
        
        return self.franquicia_repo.create(nombre.strip())

    def obtener_franquicia(self, franquicia_id: int) -> Optional[Franquicia]:
        """
        Obtiene una franquicia por su identificador único.
        
        Args:
            franquicia_id (int): ID único de la franquicia
            
        Returns:
            Optional[Franquicia]: La franquicia encontrada o None si no existe
        """
        return self.franquicia_repo.get_by_id(franquicia_id)

    def obtener_todas_franquicias(self) -> List[Franquicia]:
        """
        Obtiene todas las franquicias del sistema.
        
        Returns:
            List[Franquicia]: Lista completa de franquicias
        """
        return self.franquicia_repo.get_all()

    def actualizar_franquicia(self, franquicia_id: int, nombre: str) -> Optional[Franquicia]:
        """
        Actualiza el nombre de una franquicia existente con validaciones.
        
        Este método implementa las siguientes reglas de negocio:
        - La franquicia debe existir
        - El nuevo nombre no puede estar vacío
        - El nuevo nombre debe ser único (excluyendo la franquicia actual)
        
        Args:
            franquicia_id (int): ID de la franquicia a actualizar
            nombre (str): Nuevo nombre para la franquicia
            
        Returns:
            Optional[Franquicia]: La franquicia actualizada o None si no existe
            
        Raises:
            ValueError: Si el nombre está vacío o ya existe otra franquicia con ese nombre
        """
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
        """
        Elimina una franquicia del sistema.
        
        Esta operación también eliminará todas las sucursales y productos
        asociados debido a las restricciones de clave foránea.
        
        Args:
            franquicia_id (int): ID de la franquicia a eliminar
            
        Returns:
            bool: True si la franquicia fue eliminada, False si no existe
        """
        # Validar que la franquicia exista
        if not self.franquicia_repo.exists(franquicia_id):
            return False
        
        return self.franquicia_repo.delete(franquicia_id)

    def obtener_reporte_stock(self, franquicia_id: int) -> List[Dict[str, Any]]:
        """
        Obtiene el producto con más stock de cada sucursal de una franquicia.
        
        Este método genera un reporte de análisis de inventario que muestra
        el producto con mayor stock en cada sucursal de la franquicia especificada.
        
        Args:
            franquicia_id (int): ID de la franquicia para el reporte
            
        Returns:
            List[Dict[str, Any]]: Lista de diccionarios con información detallada:
                - producto_id: ID del producto
                - producto_nombre: Nombre del producto
                - cantidad_stock: Cantidad en stock
                - sucursal_id: ID de la sucursal
                - sucursal_nombre: Nombre de la sucursal
                
        Raises:
            ValueError: Si la franquicia no existe
        """
        # Validar que la franquicia exista
        franquicia = self.franquicia_repo.get_by_id(franquicia_id)
        if not franquicia:
            raise ValueError(f"Franquicia con ID {franquicia_id} no encontrada")
        
        return self.producto_repo.get_max_stock_by_sucursal(franquicia_id)

    def franquicia_existe(self, franquicia_id: int) -> bool:
        """
        Verifica si una franquicia existe en el sistema.
        
        Args:
            franquicia_id (int): ID de la franquicia a verificar
            
        Returns:
            bool: True si la franquicia existe, False en caso contrario
        """
        return self.franquicia_repo.exists(franquicia_id)
