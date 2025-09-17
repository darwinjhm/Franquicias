"""
Controladores REST para la API de franquicias
"""

from .franquicia_controller import FranquiciaController
from .sucursal_controller import SucursalController
from .producto_controller import ProductoController

__all__ = ["FranquiciaController", "SucursalController", "ProductoController"]
