from pydantic import BaseModel


class UsuarioCreate(BaseModel):
    nombre: str
    email: str

class ProyectoCreate(BaseModel):
    nombre: str
    descripcion: str

class TareaCreate(BaseModel):
    titulo: str
    descripcion: str
        