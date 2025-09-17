"""
Servicio de lógica de negocio para Producto
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from ..repositories.sucursal_repository import SucursalRepository
from ..repositories.producto_repository import ProductoRepository
from ..models.producto import Producto


class ProductoService:
    """Servicio para lógica de negocio de Producto"""

    def __init__(self, db: Session):
        self.db = db
        self.sucursal_repo = SucursalRepository(db)
        self.producto_repo = ProductoRepository(db)

    def crear_producto(self, nombre: str, cantidad_stock: int, sucursal_id: int) -> Producto:
        """Crea un nuevo producto en una sucursal"""
        # Validar que el nombre no esté vacío
        if not nombre or not nombre.strip():
            raise ValueError("El nombre del producto no puede estar vacío")
        
        # Validar que la cantidad de stock sea no negativa
        if cantidad_stock < 0:
            raise ValueError("La cantidad de stock no puede ser negativa")
        
        # Validar que la sucursal exista
        sucursal = self.sucursal_repo.get_by_id(sucursal_id)
        if not sucursal:
            raise ValueError(f"Sucursal con ID {sucursal_id} no encontrada")
        
        # Validar que no exista un producto con el mismo nombre en la sucursal
        producto_existente = self.producto_repo.get_by_name_and_sucursal(nombre.strip(), sucursal_id)
        if producto_existente:
            raise ValueError(f"Ya existe un producto con el nombre '{nombre}' en esta sucursal")
        
        return self.producto_repo.create(nombre.strip(), cantidad_stock, sucursal_id)

    def obtener_producto(self, producto_id: int) -> Optional[Producto]:
        """Obtiene un producto por ID"""
        return self.producto_repo.get_by_id(producto_id)

    def obtener_productos_por_sucursal(self, sucursal_id: int) -> List[Producto]:
        """Obtiene todos los productos de una sucursal"""
        # Validar que la sucursal exista
        if not self.sucursal_repo.exists(sucursal_id):
            raise ValueError(f"Sucursal con ID {sucursal_id} no encontrada")
        
        return self.producto_repo.get_by_sucursal_id(sucursal_id)

    def obtener_todos_productos(self) -> List[Producto]:
        """Obtiene todos los productos"""
        return self.producto_repo.get_all()

    def actualizar_producto(self, producto_id: int, nombre: str) -> Optional[Producto]:
        """Actualiza el nombre de un producto"""
        # Validar que el producto exista
        producto = self.producto_repo.get_by_id(producto_id)
        if not producto:
            return None
        
        # Validar que el nombre no esté vacío
        if not nombre or not nombre.strip():
            raise ValueError("El nombre del producto no puede estar vacío")
        
        # Validar que no exista otro producto con el mismo nombre en la misma sucursal
        producto_existente = self.producto_repo.get_by_name_and_sucursal(nombre.strip(), producto.sucursal_id)
        if producto_existente and producto_existente.id != producto_id:
            raise ValueError(f"Ya existe un producto con el nombre '{nombre}' en esta sucursal")
        
        return self.producto_repo.update(producto_id, nombre.strip())

    def actualizar_stock(self, producto_id: int, cantidad_stock: int) -> Optional[Producto]:
        """Actualiza el stock de un producto"""
        # Validar que el producto exista
        producto = self.producto_repo.get_by_id(producto_id)
        if not producto:
            return None
        
        # Validar que la cantidad de stock sea no negativa
        if cantidad_stock < 0:
            raise ValueError("La cantidad de stock no puede ser negativa")
        
        return self.producto_repo.update_stock(producto_id, cantidad_stock)

    def eliminar_producto(self, producto_id: int) -> bool:
        """Elimina un producto"""
        # Validar que el producto exista
        if not self.producto_repo.exists(producto_id):
            return False
        
        return self.producto_repo.delete(producto_id)

    def producto_existe(self, producto_id: int) -> bool:
        """Verifica si un producto existe"""
        return self.producto_repo.exists(producto_id)

    def producto_pertenece_a_sucursal(self, producto_id: int, sucursal_id: int) -> bool:
        """Verifica si un producto pertenece a una sucursal específica"""
        return self.producto_repo.belongs_to_sucursal(producto_id, sucursal_id)
