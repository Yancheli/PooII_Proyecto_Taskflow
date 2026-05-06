from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.auth import get_current_user
from api.database import get_db
from api.schemas.usuario import UsuarioCreate, UsuarioOut, UsuarioUpdate
from api.services import usuario_service
from database.modelsalchemy import Usuario

router = APIRouter(prefix="/api/usuarios", tags=["Usuarios CRUD"])


@router.post("", response_model=UsuarioOut, status_code=201,
             summary="Registrar usuario")
def registrar(datos: UsuarioCreate, db: Session = Depends(get_db)):
    """Crea un usuario nuevo. Valida username y email"""
    return usuario_service.registrar_usuario(db, datos)


@router.get("", response_model=list[UsuarioOut], summary="Listar usuarios")
def listar(db: Session = Depends(get_db)):
    """Devuelve todos los usuarios"""
    return usuario_service.listar_usuarios(db)


@router.get("/me", response_model=UsuarioOut, summary="Perfil propio")
def perfil(usuario_actual: Usuario = Depends(get_current_user)):
    """Devuelve el perfil del usuario autenticado."""
    return usuario_actual


@router.get("/{usuario_id}", response_model=UsuarioOut, summary="Obtener usuario")
def obtener(usuario_id: int, db: Session = Depends(get_db)):
    """Busca un usuario por ID."""
    return usuario_service.obtener_usuario(db, usuario_id)


@router.patch("/{usuario_id}", response_model=UsuarioOut, summary="Actualizar usuario")
def actualizar(
    usuario_id: int,
    datos: UsuarioUpdate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),   # requiere sesión activa
):
    """Actualiza email o activo/inactivo"""
    return usuario_service.actualizar_usuario(db, usuario_id, datos)


@router.delete("/{usuario_id}", status_code=204, summary="Eliminar usuario")
def eliminar(
    usuario_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    """Elimina un usuario por ID"""
    usuario_service.eliminar_usuario(db, usuario_id)