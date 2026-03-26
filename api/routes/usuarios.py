from fastapi import APIRouter
from api.models import UsuarioCreate
from api.database import usuarios, buscar_usuario

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.get("", summary="Listar usuarios")
def listar_usuarios():
    return usuarios


@router.post("", status_code=201, summary="Crear usuario")
def crear_usuario(usuario: UsuarioCreate):
    nuevo = usuario.model_dump()
    nuevo["id"] = len(usuarios) + 1
    nuevo["activo"] = True
    usuarios.append(nuevo)
    return nuevo


@router.get("/{usuario_id}", summary="Obtener usuario por ID")
def obtener_usuario(usuario_id: int):
    return buscar_usuario(usuario_id)