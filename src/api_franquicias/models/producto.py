"""
Modelo de Producto para el sistema de gestión de franquicias
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base


class Producto(Base):
    """
    Modelo que representa un producto en una sucursal.
    
    Un producto pertenece a una sucursal y tiene un stock específico.
    """
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), nullable=False, index=True)
    cantidad_stock = Column(Integer, nullable=False, default=0)
    sucursal_id = Column(Integer, ForeignKey("sucursales.id"), nullable=False, index=True)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion = Column(DateTime(timezone=True), onupdate=func.now())

    # Relaciones
    sucursal = relationship("Sucursal", back_populates="productos")

    def __repr__(self):
        return f"<Producto(id={self.id}, nombre='{self.nombre}', stock={self.cantidad_stock}, sucursal_id={self.sucursal_id})>"

    def to_dict(self):
        """Convierte el modelo a diccionario para serialización JSON"""
        return {
            "id": self.id,
            "nombre": self.nombre,
            "cantidad_stock": self.cantidad_stock,
            "sucursal_id": self.sucursal_id,
            "fecha_creacion": self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            "fecha_actualizacion": self.fecha_actualizacion.isoformat() if self.fecha_actualizacion else None
        }
