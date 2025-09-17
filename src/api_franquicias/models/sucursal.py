"""
Modelo de Sucursal para el sistema de gestión de franquicias
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base


class Sucursal(Base):
    """
    Modelo que representa una sucursal de una franquicia.
    
    Una sucursal pertenece a una franquicia y puede tener múltiples productos.
    """
    __tablename__ = "sucursales"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), nullable=False, index=True)
    franquicia_id = Column(Integer, ForeignKey("franquicias.id"), nullable=False, index=True)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion = Column(DateTime(timezone=True), onupdate=func.now())

    # Relaciones
    franquicia = relationship("Franquicia", back_populates="sucursales")
    productos = relationship("Producto", back_populates="sucursal", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Sucursal(id={self.id}, nombre='{self.nombre}', franquicia_id={self.franquicia_id})>"

    def to_dict(self):
        """Convierte el modelo a diccionario para serialización JSON"""
        return {
            "id": self.id,
            "nombre": self.nombre,
            "franquicia_id": self.franquicia_id,
            "fecha_creacion": self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            "fecha_actualizacion": self.fecha_actualizacion.isoformat() if self.fecha_actualizacion else None,
            "productos": [producto.to_dict() for producto in self.productos] if self.productos else []
        }
