"""
Repositorios para acceso a datos
"""

from .franquicia_repository import FranquiciaRepository
from .sucursal_repository import SucursalRepository
from .producto_repository import ProductoRepository

__all__ = ["FranquiciaRepository", "SucursalRepository", "ProductoRepository"]
