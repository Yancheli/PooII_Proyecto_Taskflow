"""
Endpoints JWT: POST /auth/register y POST /auth/login
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session

from api.database import get_db
from api.jwt_auth import (
    create_access_token,
    hash_password_bcrypt,
    verify_password_bcrypt,
)
from database.modelsalchemy import Usuario
from src.domain.enums import RolUsuario

router = APIRouter(prefix="/auth", tags=["JWT Auth"])


# ── Schemas ───────────────────────────────────────────────────────────────────

class RegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50, pattern=r"^[a-zA-Z0-9]+$")
    email: EmailStr
    password: str = Field(min_length=6)
    rol: RolUsuario = RolUsuario.MIEMBRO


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    id: int
    username: str
    email: str
    rol: RolUsuario

    model_config = {"from_attributes": True}


# ── Endpoints ─────────────────────────────────────────────────────────────────

@router.post(
    "/register",
    response_model=UserOut,
    status_code=201,
    summary="Registrar usuario con contraseña bcrypt",
)
def register(datos: RegisterRequest, db: Session = Depends(get_db)):
    """
    Crea un usuario nuevo con contraseña hasheada con bcrypt.
    Devuelve los datos del usuario creado (sin contraseña).
    """
    # Verificar duplicados
    if db.query(Usuario).filter(Usuario.username == datos.username).first():
        raise HTTPException(status_code=400, detail="El username ya está en uso.")
    if db.query(Usuario).filter(Usuario.email == datos.email).first():
        raise HTTPException(status_code=400, detail="El email ya está registrado.")

    nuevo = Usuario(
        username=datos.username,
        email=datos.email,
        hashed_password=hash_password_bcrypt(datos.password),
        activo=True,
        rol=datos.rol,
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Login — retorna access_token JWT",
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """
    Recibe username + password (form-urlencoded).
    Valida credenciales y retorna el JWT.
    Compatible con el botón Authorize de Swagger UI.
    """
    usuario = db.query(Usuario).filter(Usuario.username == form_data.username).first()

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Soporta tanto bcrypt (nuevos) como sha256 (usuarios legacy del sistema de cookies)
    password_ok = verify_password_bcrypt(form_data.password, usuario.hashed_password)
    if not password_ok:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not usuario.activo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Esta cuenta está desactivada.",
        )

    token = create_access_token(data={"sub": str(usuario.id)})
    return {"access_token": token, "token_type": "bearer"}