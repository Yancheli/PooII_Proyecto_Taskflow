"""DTOs Pydantic v2 para Usuario."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, ConfigDict

from src.domain.enums import RolUsuario


class UsuarioCreate(BaseModel):
    """Datos para registrar un usuario nuevo"""

    username: str = Field(
        min_length=3,
        max_length=50,
        pattern=r"^[a-zA-Z0-9]+$",
        examples=["jessica123"],
    )
    email: EmailStr
    password: str = Field(min_length=6, examples=["segura123"])
    rol: RolUsuario = RolUsuario.MIEMBRO


class UsuarioUpdate(BaseModel):
    """Datos opcionales para actualizar un usuario"""

    email: Optional[EmailStr] = None
    activo: Optional[bool] = None


class UsuarioOut(BaseModel):
    """Respuesta pública de Usuario"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: str
    activo: bool
    rol: RolUsuario
    fecha_registro: datetime