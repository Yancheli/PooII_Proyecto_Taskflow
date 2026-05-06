"""Rutas de autenticación: login, registro, logout."""

import re

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from api.auth import (
    COOKIE_NAME,
    create_session_cookie,
    get_current_user_optional,
    hash_password,
    verify_password,
)
from api.database import get_db
from database.modelsalchemy import Usuario
from src.domain.enums import RolUsuario

router = APIRouter(tags=["Auth"])
templates = Jinja2Templates(directory="templates")


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request, db: Session = Depends(get_db)):
    """Muestra la página de login/registro. Si ya hay sesión, redirige al inicio."""
    usuario = get_current_user_optional(request, db)
    if usuario:
        return RedirectResponse("/", status_code=302)
    return templates.TemplateResponse(
        request=request,
        name="auth/login.html",
        context={"error": None, "reg_error": None, "reg_success": None},
    )


@router.post("/login", response_class=HTMLResponse)
def do_login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    """Procesa el formulario de login."""
    usuario = db.query(Usuario).filter(Usuario.username == username).first()

    if not usuario or not verify_password(password, usuario.hashed_password):
        return templates.TemplateResponse(
            request=request,
            name="auth/login.html",
            context={
                "error": "Usuario o contraseña incorrectos.",
                "reg_error": None,
                "reg_success": None,
            },
            status_code=401,
        )

    if not usuario.activo:
        return templates.TemplateResponse(
            request=request,
            name="auth/login.html",
            context={
                "error": "Esta cuenta está desactivada.",
                "reg_error": None,
                "reg_success": None,
            },
            status_code=403,
        )

    token = create_session_cookie(usuario.id, usuario.username, usuario.rol.value)
    response = RedirectResponse("/", status_code=302)
    response.set_cookie(
        key=COOKIE_NAME,
        value=token,
        httponly=True,
        samesite="lax",
        max_age=60 * 60 * 8,
    )
    return response


@router.post("/register", response_class=HTMLResponse)
def do_register(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    rol: str = Form(...),
    db: Session = Depends(get_db),
):
    """Procesa el formulario de registro."""

    # Validaciones
    def _error(msg: str):
        return templates.TemplateResponse(
            request=request,
            name="auth/login.html",
            context={"error": None, "reg_error": msg, "reg_success": None},
            status_code=422,
        )

    username = username.strip()
    email = email.strip().lower()

    if len(username) < 3 or not username.isalnum():
        return _error("Username inválido: mínimo 3 caracteres, solo letras y números.")

    if "@" not in email or "." not in email:
        return _error("Email inválido.")

    if len(password) < 6:
        return _error("La contraseña debe tener mínimo 6 caracteres.")

    rol_enum = RolUsuario.LIDER if rol == "lider" else RolUsuario.MIEMBRO

    # Duplicados
    existente = db.query(Usuario).filter(
        (Usuario.username == username) | (Usuario.email == email)
    ).first()
    if existente:
        return _error("Ya existe un usuario con ese username o email.")

    nuevo = Usuario(
        username=username,
        email=email,
        hashed_password=hash_password(password),
        activo=True,
        rol=rol_enum,
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return templates.TemplateResponse(
        request=request,
        name="auth/login.html",
        context={
            "error": None,
            "reg_error": None,
            "reg_success": f"¡Cuenta creada! Inicia sesión como @{nuevo.username}.",
        },
    )


@router.get("/logout")
def logout():
    """Cierra la sesión eliminando la cookie."""
    response = RedirectResponse("/login", status_code=302)
    response.delete_cookie(COOKIE_NAME)
    return response