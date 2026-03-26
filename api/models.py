from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from src.domain.enums import PrioridadTarea, EstadoTarea


# Usuarios

class UsuarioCreate(BaseModel):
    """Datos para crear un usuario"""

    username: str = Field(
        min_length=3,
        max_length=50,
        pattern=r"^[a-zA-Z0-9]+$",
        examples=["jessica123"],
        description="Identificador único (solo letras y números y cumpliendo el minimo de caracteres)"
    )
    email: EmailStr = Field(
        examples=["jessica@gmail.com"],
        description="Correo electrónico válido"
    )
    nombre_completo: Optional[str] = Field(
        default=None,
        max_length=100,
        examples=["Jessica Treviño"],
        description="Nombre completo del usuario (opcional)"
    )


class UsuarioResponse(BaseModel):
    """Datos que devuelve la Api"""

    id: int
    username: str
    email: str
    nombre_completo: Optional[str] = None
    activo: bool
    fecha_registro: datetime

    model_config = {"from_attributes": True}


# Proyectos

class ProyectoCreate(BaseModel):
    """Datos para crear un proyecto."""

    nombre: str = Field(
        min_length=3,
        max_length=50,
        examples=["Sistema TaskFlow"],
        description="Nombre del proyecto (con minimo 3 car.)"
    )
    descripcion: Optional[str] = Field(
        default=None,
        max_length=300,
        examples=["Sistema de gestión de tareas"],
        description="Descripción opcional del proyecto"
    )


class ProyectoResponse(BaseModel):
    """Datos que se devuelven al consultar un proyecto en la api"""

    id: int
    nombre: str
    descripcion: Optional[str] = None
    lider_id: int

    model_config = {"from_attributes": True}


# Tareas

class TareaCreate(BaseModel):
    """Datos para crear una tarea"""

    titulo: str = Field(
        min_length=3,
        max_length=50,
        examples=["Hacer informe"],
        description="Título de la tarea"
    )
    descripcion: Optional[str] = Field(
        default=None,
        max_length=300,
        examples=["Redactar el informe final del sprint"],
        description="Descripción opcional"
    )
    prioridad: PrioridadTarea = Field(
        default=PrioridadTarea.MEDIA,
        examples=[PrioridadTarea.ALTA],
        description="Prioridad de la tarea: ALTA, MEDIA o BAJA"
    )


class TareaUpdate(BaseModel):
    """Datos para actualizar una tarea (todos opcionales)"""

    prioridad: Optional[PrioridadTarea] = Field(
        default=None,
        examples=[PrioridadTarea.BAJA],
        description="Nueva prioridad de la tarea"
    )


class TareaResponse(BaseModel):
    """Datos que se devuelven al consultar una tarea en la api"""

    id: int
    titulo: str
    descripcion: Optional[str] = None
    prioridad: PrioridadTarea
    estado: EstadoTarea
    fecha_creacion: datetime
    fecha_completado: Optional[datetime] = None

    model_config = {"from_attributes": True}