import hashlib

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.models import UsuarioCreate, UsuarioResponse
from api.database import get_db, buscar_usuario
from database.modelsalchemy import Usuario

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.get("", summary="Listar usuarios", response_model=list[UsuarioResponse])
def listar_usuarios(db: Session = Depends(get_db)):
    """Devuelve todos los usuarios registrados en la Base de datos"""
    return db.query(Usuario).all()


@router.post("", status_code=201, summary="Crear usuario", response_model=UsuarioResponse)
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    
    # Contraseña placeholder (proyecto no-serio)
    hashed_pw = hashlib.sha256(usuario.username.encode()).hexdigest()

    nuevo = Usuario(
        username=usuario.username,
        email=usuario.email,
        hashed_password=hashed_pw,
        activo=True,
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)   
    return nuevo


@router.get("/{usuario_id}", summary="Obtener usuario por ID", response_model=UsuarioResponse)
def obtener_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """Busca un usuario por su id"""
    return buscar_usuario(usuario_id, db)