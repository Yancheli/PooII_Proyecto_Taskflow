from fastapi import HTTPException
from sqlalchemy.orm import Session

from api.auth import hash_password
from api.repositories import usuario_repo
from api.schemas.usuario import UsuarioCreate, UsuarioUpdate
from database.modelsalchemy import Usuario


def registrar_usuario(db: Session, datos: UsuarioCreate) -> Usuario:
    """Valida y crea el usuario en la base de datos."""
    if usuario_repo.obtener_por_username(db, datos.username):
        raise HTTPException(status_code=400, detail="El username ya está en uso.")
    if usuario_repo.obtener_por_email(db, datos.email):
        raise HTTPException(status_code=400, detail="El email ya está registrado.")

    nuevo = Usuario(
        username=datos.username,
        email=datos.email,
        hashed_password=hash_password(datos.password),
        activo=True,
        rol=datos.rol,
    )
    return usuario_repo.crear(db, nuevo)


def obtener_usuario(db: Session, usuario_id: int) -> Usuario:
    usuario = usuario_repo.obtener_por_id(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    return usuario


def listar_usuarios(db: Session) -> list[Usuario]:
    return usuario_repo.listar_todos(db)


def actualizar_usuario(db: Session, usuario_id: int, datos: UsuarioUpdate) -> Usuario:
    usuario = obtener_usuario(db, usuario_id)

    if datos.email is not None:
        existente = usuario_repo.obtener_por_email(db, datos.email)
        if existente and existente.id != usuario_id:
            raise HTTPException(status_code=400, detail="El email ya está en uso.")
        usuario.email = datos.email

    if datos.activo is not None:
        usuario.activo = datos.activo

    return usuario_repo.actualizar(db, usuario)


def eliminar_usuario(db: Session, usuario_id: int) -> None:
    usuario = obtener_usuario(db, usuario_id)
    usuario_repo.eliminar(db, usuario)