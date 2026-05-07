"""
Autenticación JWT con OAuth2PasswordBearer.
Coexiste con el sistema de cookies existente.
"""

from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from api.database import get_db
from database.modelsalchemy import Usuario

# ── Configuración ─────────────────────────────────────────────────────────────

SECRET_KEY = "taskflow-jwt-secret-2026-cambiar-en-produccion"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 8  # 8 horas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# ── Contraseñas ───────────────────────────────────────────────────────────────

def hash_password_bcrypt(password: str) -> str:
    return pwd_context.hash(password)


def verify_password_bcrypt(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


# ── Tokens JWT ────────────────────────────────────────────────────────────────

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


# ── Dependencia get_current_user (JWT) ───────────────────────────────────────

def get_current_user_jwt(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> Usuario:
    """
    Decodifica el JWT del header Authorization: Bearer <token>
    y devuelve el usuario de la base de datos.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar el token.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    usuario_id: Optional[int] = payload.get("sub")
    if usuario_id is None:
        raise credentials_exception

    usuario = db.get(Usuario, int(usuario_id))
    if usuario is None or not usuario.activo:
        raise credentials_exception

    return usuario