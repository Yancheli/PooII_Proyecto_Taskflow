"""
Manejo de sesiones con cookies firmadas (HMAC-SHA256).
No requiere base de datos adicional ni librerías externas de JWT.
"""

import hashlib
import hmac
import json
import time
from typing import Optional

from fastapi import Cookie, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from api.database import get_db
from database.modelsalchemy import Usuario
from src.domain.enums import RolUsuario

# Clave secreta para firmar cookies (en producción usar variable de entorno)
SECRET_KEY = "taskflow-secret-2026-cambiar-en-produccion"
COOKIE_NAME = "tf_session"
SESSION_TTL = 60 * 60 * 8  # 8 horas


# ── Contraseñas ──────────────────────────────────────────────────────────────

def hash_password(password: str) -> str:
    """SHA-256 simple. Para producción usar bcrypt/argon2."""
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(plain: str, hashed: str) -> bool:
    return hmac.compare_digest(hash_password(plain), hashed)


# ── Cookies firmadas ──────────────────────────────────────────────────────────

def _sign(payload: str) -> str:
    sig = hmac.new(SECRET_KEY.encode(), payload.encode(), hashlib.sha256).hexdigest()
    return f"{payload}:{sig}"


def _verify(token: str) -> Optional[dict]:
    try:
        payload, sig = token.rsplit(":", 1)
        expected = hmac.new(SECRET_KEY.encode(), payload.encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(sig, expected):
            return None
        data = json.loads(payload)
        if data.get("exp", 0) < time.time():
            return None
        return data
    except Exception:
        return None


def create_session_cookie(usuario_id: int, username: str, rol: str) -> str:
    payload = json.dumps({
        "uid": usuario_id,
        "usr": username,
        "rol": rol,
        "exp": int(time.time()) + SESSION_TTL,
    })
    return _sign(payload)


def decode_session_cookie(token: str) -> Optional[dict]:
    return _verify(token)


# ── Dependencias FastAPI ──────────────────────────────────────────────────────

def get_current_user_optional(
    request: Request,
    db: Session = Depends(get_db),
) -> Optional[Usuario]:
    """Devuelve el usuario autenticado o None si no hay sesión."""
    token = request.cookies.get(COOKIE_NAME)
    if not token:
        return None
    data = decode_session_cookie(token)
    if not data:
        return None
    usuario = db.get(Usuario, data["uid"])
    if not usuario or not usuario.activo:
        return None
    return usuario


def get_current_user(
    request: Request,
    db: Session = Depends(get_db),
) -> Usuario:
    """Requiere sesión activa. Redirige a /login si no la hay."""
    usuario = get_current_user_optional(request, db)
    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_307_TEMPORARY_REDIRECT,
            headers={"Location": "/login"},
        )
    return usuario


def require_lider(usuario: Usuario = Depends(get_current_user)) -> Usuario:
    """Requiere rol LIDER."""
    if usuario.rol != RolUsuario.LIDER:
        raise HTTPException(status_code=403, detail="Solo líderes pueden realizar esta acción.")
    return usuario