"""
Controladores REST para la API de franquicias
"""

from .franquicia_controller import router as franquicia_router
from .sucursal_controller import router as sucursal_router
from .producto_controller import router as producto_router

__all__ = ["franquicia_router", "sucursal_router", "producto_router"]
