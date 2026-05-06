from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class ProyectoCreate(BaseModel):
    """Datos para crear un proyecto"""

    nombre: str = Field(min_length=3, max_length=100, examples=["Sistema TaskFlow"])
    descripcion: Optional[str] = Field(default=None, max_length=300)


class ProyectoUpdate(BaseModel):
    """Datos opcionales para editar un proyecto"""

    nombre: Optional[str] = Field(default=None, min_length=3, max_length=100)
    descripcion: Optional[str] = Field(default=None, max_length=300)


class ProyectoOut(BaseModel):
    """Respuesta de Proyecto"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    descripcion: Optional[str]
    lider_id: int