from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict

from src.domain.enums import PrioridadTarea, EstadoTarea


class TareaCreate(BaseModel):
    """Datos para crear una tarea"""

    titulo: str = Field(min_length=3, max_length=100, examples=["Hacer informe"])
    descripcion: Optional[str] = Field(default=None, max_length=300)
    prioridad: PrioridadTarea = PrioridadTarea.MEDIA


class TareaUpdate(BaseModel):
    """Datos opcionales para editar una tarea"""

    titulo: Optional[str] = Field(default=None, min_length=3, max_length=100)
    descripcion: Optional[str] = Field(default=None, max_length=300)
    prioridad: Optional[PrioridadTarea] = None
    estado: Optional[EstadoTarea] = None


class TareaOut(BaseModel):
    """Respuesta"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    titulo: str
    descripcion: Optional[str]
    prioridad: PrioridadTarea
    estado: EstadoTarea
    proyecto_id: int
    creador_id: int
    fecha_creacion: datetime
    fecha_completado: Optional[datetime]