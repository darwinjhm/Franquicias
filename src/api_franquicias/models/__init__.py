"""
Modelos de la base de datos para el sistema de franquicias
"""

from .base import Base
from .franquicia import Franquicia
from .sucursal import Sucursal
from .producto import Producto

__all__ = ["Base", "Franquicia", "Sucursal", "Producto"]
