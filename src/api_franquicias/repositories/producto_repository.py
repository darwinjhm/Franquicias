"""
Repositorio para operaciones de base de datos de Producto.

Este módulo implementa el patrón Repository para la entidad Producto,
proporcionando una capa de abstracción entre la lógica de negocio
y las operaciones de persistencia de datos. Incluye funcionalidades
especializadas para reportes de stock y análisis de inventario.

Autor: Darwin Hurtado
Fecha: 2024
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, func, desc
from ..models.producto import Producto
from ..models.sucursal import Sucursal


class ProductoRepository:
    """
    Repositorio para operaciones CRUD de Producto.
    
    Esta clase encapsula todas las operaciones de base de datos relacionadas
    con la entidad Producto, incluyendo operaciones complejas para reportes
    de stock y análisis de inventario por sucursal.
    
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

    def create(self, nombre: str, cantidad_stock: int, sucursal_id: int) -> Producto:
        """
        Crea un nuevo producto en la base de datos.
        
        Args:
            nombre (str): Nombre único del producto dentro de la sucursal
            cantidad_stock (int): Cantidad inicial en stock (debe ser >= 0)
            sucursal_id (int): ID de la sucursal donde se crea el producto
            
        Returns:
            Producto: Instancia del producto creado con ID asignado
            
        Raises:
            IntegrityError: Si ya existe un producto con el mismo nombre
                          en la misma sucursal
            ValueError: Si cantidad_stock es negativa
        """
        producto = Producto(
            nombre=nombre,
            cantidad_stock=cantidad_stock,
            sucursal_id=sucursal_id
        )
        self.db.add(producto)
        self.db.commit()
        self.db.refresh(producto)
        return producto

    def get_by_id(self, producto_id: int) -> Optional[Producto]:
        """
        Obtiene un producto por su identificador único.
        
        Args:
            producto_id (int): ID único del producto
            
        Returns:
            Optional[Producto]: El producto encontrado o None si no existe
        """
        return self.db.query(Producto).filter(Producto.id == producto_id).first()

    def get_by_sucursal_id(self, sucursal_id: int) -> List[Producto]:
        """
        Obtiene todos los productos que pertenecen a una sucursal específica.
        
        Args:
            sucursal_id (int): ID de la sucursal
            
        Returns:
            List[Producto]: Lista de productos de la sucursal (puede estar vacía)
        """
        return self.db.query(Producto).filter(Producto.sucursal_id == sucursal_id).all()

    def get_by_name_and_sucursal(self, nombre: str, sucursal_id: int) -> Optional[Producto]:
        """
        Busca un producto por nombre dentro de una sucursal específica.
        
        Este método es útil para validar nombres únicos dentro del contexto
        de una sucursal, ya que el mismo nombre puede existir en diferentes
        sucursales.
        
        Args:
            nombre (str): Nombre del producto a buscar
            sucursal_id (int): ID de la sucursal donde buscar
            
        Returns:
            Optional[Producto]: El producto encontrado o None si no existe
        """
        return self.db.query(Producto).filter(
            and_(Producto.nombre == nombre, Producto.sucursal_id == sucursal_id)
        ).first()

    def get_all(self) -> List[Producto]:
        """
        Obtiene todos los productos del sistema.
        
        Returns:
            List[Producto]: Lista completa de productos ordenados por ID
            
        Note:
            Este método puede ser costoso en sistemas con muchos productos.
            Considera usar paginación para grandes volúmenes de datos.
        """
        return self.db.query(Producto).all()

    def update(self, producto_id: int, nombre: str) -> Optional[Producto]:
        """
        Actualiza el nombre de un producto existente.
        
        Args:
            producto_id (int): ID del producto a actualizar
            nombre (str): Nuevo nombre para el producto
            
        Returns:
            Optional[Producto]: El producto actualizado o None si no existe
            
        Raises:
            IntegrityError: Si el nuevo nombre ya existe en la misma sucursal
        """
        producto = self.get_by_id(producto_id)
        if producto:
            producto.nombre = nombre
            self.db.commit()
            self.db.refresh(producto)
        return producto

    def update_stock(self, producto_id: int, cantidad_stock: int) -> Optional[Producto]:
        """
        Actualiza el stock de un producto existente.
        
        Args:
            producto_id (int): ID del producto a actualizar
            cantidad_stock (int): Nueva cantidad en stock (debe ser >= 0)
            
        Returns:
            Optional[Producto]: El producto actualizado o None si no existe
            
        Raises:
            ValueError: Si cantidad_stock es negativa
        """
        producto = self.get_by_id(producto_id)
        if producto:
            producto.cantidad_stock = cantidad_stock
            self.db.commit()
            self.db.refresh(producto)
        return producto

    def delete(self, producto_id: int) -> bool:
        """
        Elimina un producto de la base de datos.
        
        Args:
            producto_id (int): ID del producto a eliminar
            
        Returns:
            bool: True si el producto fue eliminado, False si no existe
        """
        producto = self.get_by_id(producto_id)
        if producto:
            self.db.delete(producto)
            self.db.commit()
            return True
        return False

    def exists(self, producto_id: int) -> bool:
        """
        Verifica si un producto existe en la base de datos.
        
        Args:
            producto_id (int): ID del producto a verificar
            
        Returns:
            bool: True si el producto existe, False en caso contrario
        """
        return self.db.query(Producto).filter(Producto.id == producto_id).first() is not None

    def belongs_to_sucursal(self, producto_id: int, sucursal_id: int) -> bool:
        """
        Verifica si un producto pertenece a una sucursal específica.
        
        Este método es útil para validar permisos y asegurar que las
        operaciones se realicen en el contexto correcto.
        
        Args:
            producto_id (int): ID del producto a verificar
            sucursal_id (int): ID de la sucursal esperada
            
        Returns:
            bool: True si el producto pertenece a la sucursal, False en caso contrario
        """
        producto = self.db.query(Producto).filter(
            and_(Producto.id == producto_id, Producto.sucursal_id == sucursal_id)
        ).first()
        return producto is not None

    def get_max_stock_by_sucursal(self, franquicia_id: int) -> List[Dict[str, Any]]:
        """
        Obtiene el producto con más stock de cada sucursal de una franquicia.
        
        Este método implementa una consulta compleja que:
        1. Encuentra el máximo stock por sucursal
        2. Identifica los productos que tienen ese stock máximo
        3. Retorna información detallada del producto y sucursal
        
        Args:
            franquicia_id (int): ID de la franquicia para el reporte
            
        Returns:
            List[Dict[str, Any]]: Lista de diccionarios con información detallada:
                - producto_id: ID del producto
                - producto_nombre: Nombre del producto
                - cantidad_stock: Cantidad en stock
                - sucursal_id: ID de la sucursal
                - sucursal_nombre: Nombre de la sucursal
                
        Note:
            Si múltiples productos tienen el mismo stock máximo en una sucursal,
            se retornarán todos los productos con ese stock.
        """
        # Subconsulta para obtener el máximo stock por sucursal
        max_stock_subquery = self.db.query(
            Producto.sucursal_id,
            func.max(Producto.cantidad_stock).label('max_stock')
        ).join(Sucursal).filter(
            Sucursal.franquicia_id == franquicia_id
        ).group_by(Producto.sucursal_id).subquery()

        # Consulta principal para obtener los productos con máximo stock
        result = self.db.query(
            Producto.id,
            Producto.nombre,
            Producto.cantidad_stock,
            Sucursal.id.label('sucursal_id'),
            Sucursal.nombre.label('sucursal_nombre')
        ).join(Sucursal).join(
            max_stock_subquery,
            and_(
                Producto.sucursal_id == max_stock_subquery.c.sucursal_id,
                Producto.cantidad_stock == max_stock_subquery.c.max_stock
            )
        ).filter(
            Sucursal.franquicia_id == franquicia_id
        ).all()

        return [
            {
                "producto_id": row.id,
                "producto_nombre": row.nombre,
                "cantidad_stock": row.cantidad_stock,
                "sucursal_id": row.sucursal_id,
                "sucursal_nombre": row.sucursal_nombre
            }
            for row in result
        ]
