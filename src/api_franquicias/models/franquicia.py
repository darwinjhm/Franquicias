"""
Modelo de Franquicia para el sistema de gestión de franquicias
"""

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base


class Franquicia(Base):
    """
    Modelo que representa una franquicia en el sistema.
    
    Una franquicia puede tener múltiples sucursales.
    """
    __tablename__ = "franquicias"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), nullable=False, index=True)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion = Column(DateTime(timezone=True), onupdate=func.now())

    # Relación con sucursales
    sucursales = relationship("Sucursal", back_populates="franquicia", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Franquicia(id={self.id}, nombre='{self.nombre}')>"

    def to_dict(self):
        """Convierte el modelo a diccionario para serialización JSON"""
        return {
            "id": self.id,
            "nombre": self.nombre,
            "fecha_creacion": self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            "fecha_actualizacion": self.fecha_actualizacion.isoformat() if self.fecha_actualizacion else None,
            "sucursales": [sucursal.to_dict() for sucursal in self.sucursales] if self.sucursales else []
        }
