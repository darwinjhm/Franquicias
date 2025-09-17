"""
Repositorio para operaciones de Producto
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, func, desc
from ..models.producto import Producto
from ..models.sucursal import Sucursal


class ProductoRepository:
    """Repositorio para operaciones CRUD de Producto"""

    def __init__(self, db: Session):
        self.db = db

    def create(self, nombre: str, cantidad_stock: int, sucursal_id: int) -> Producto:
        """Crea un nuevo producto"""
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
        """Obtiene un producto por ID"""
        return self.db.query(Producto).filter(Producto.id == producto_id).first()

    def get_by_sucursal_id(self, sucursal_id: int) -> List[Producto]:
        """Obtiene todos los productos de una sucursal"""
        return self.db.query(Producto).filter(Producto.sucursal_id == sucursal_id).all()

    def get_by_name_and_sucursal(self, nombre: str, sucursal_id: int) -> Optional[Producto]:
        """Obtiene un producto por nombre y sucursal"""
        return self.db.query(Producto).filter(
            and_(Producto.nombre == nombre, Producto.sucursal_id == sucursal_id)
        ).first()

    def get_all(self) -> List[Producto]:
        """Obtiene todos los productos"""
        return self.db.query(Producto).all()

    def update(self, producto_id: int, nombre: str) -> Optional[Producto]:
        """Actualiza el nombre de un producto"""
        producto = self.get_by_id(producto_id)
        if producto:
            producto.nombre = nombre
            self.db.commit()
            self.db.refresh(producto)
        return producto

    def update_stock(self, producto_id: int, cantidad_stock: int) -> Optional[Producto]:
        """Actualiza el stock de un producto"""
        producto = self.get_by_id(producto_id)
        if producto:
            producto.cantidad_stock = cantidad_stock
            self.db.commit()
            self.db.refresh(producto)
        return producto

    def delete(self, producto_id: int) -> bool:
        """Elimina un producto"""
        producto = self.get_by_id(producto_id)
        if producto:
            self.db.delete(producto)
            self.db.commit()
            return True
        return False

    def exists(self, producto_id: int) -> bool:
        """Verifica si un producto existe"""
        return self.db.query(Producto).filter(Producto.id == producto_id).first() is not None

    def belongs_to_sucursal(self, producto_id: int, sucursal_id: int) -> bool:
        """Verifica si un producto pertenece a una sucursal específica"""
        producto = self.db.query(Producto).filter(
            and_(Producto.id == producto_id, Producto.sucursal_id == sucursal_id)
        ).first()
        return producto is not None

    def get_max_stock_by_sucursal(self, franquicia_id: int) -> List[Dict[str, Any]]:
        """
        Obtiene el producto con más stock de cada sucursal de una franquicia.
        Retorna una lista de diccionarios con información del producto y sucursal.
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
