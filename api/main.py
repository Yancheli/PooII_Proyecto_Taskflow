from datetime import datetime

from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from api.routes import usuarios, proyectos, tareas
from api.routes.auth import router as auth_router
from api.database import get_db, buscar_proyecto, buscar_tarea
from api.auth import get_current_user, get_current_user_optional, require_lider
from database.modelsalchemy import Proyecto, Tarea, Usuario
from src.domain.enums import EstadoTarea, RolUsuario


app = FastAPI(
    title="TaskFlow API",
    description="API para gestión de usuarios, proyectos y tareas",
    version="1.0.0"
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Llamada a los routers
app.include_router(auth_router)
app.include_router(usuarios.router)
app.include_router(proyectos.router)
app.include_router(tareas.router)

# Página de inicio

@app.get("/", response_class=HTMLResponse)
def home(
    request: Request,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),   # redirige a /login si no autenticado
):
    usuarios_lista = db.query(Usuario).filter(Usuario.activo == True).all()
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "usuarios": usuarios_lista,
            "current_user": current_user,
            "es_lider": current_user.rol == RolUsuario.LIDER,
        },
    )

# HTMX usuarios

@app.post("/htmx/usuarios", response_class=HTMLResponse)
def htmx_crear_usuario(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    if len(username) < 3 or not username.isalnum():
        return HTMLResponse(
            "<p class='error-msg'><i class='bi bi-x-circle me-1'></i>Username inválido: mínimo 3 caracteres, solo letras y números.</p>",
            status_code=422,
        )
    if "@" not in email or "." not in email:
        return HTMLResponse(
            "<p class='error-msg'><i class='bi bi-x-circle me-1'></i>Email inválido.</p>",
            status_code=422,
        )
    existente = db.query(Usuario).filter(
        (Usuario.username == username) | (Usuario.email == email)
    ).first()
    if existente:
        return HTMLResponse(
            "<p class='error-msg'><i class='bi bi-x-circle me-1'></i>Ya existe un usuario con ese username o email.</p>",
            status_code=422,
        )

    import hashlib
    hashed_pw = hashlib.sha256(username.encode()).hexdigest()
    nuevo = Usuario(username=username, email=email, hashed_password=hashed_pw, activo=True)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return HTMLResponse(
        f"<p style='color: var(--tf-accent2);'><i class='bi bi-check-circle me-1'></i>"
        f"Usuario <strong>@{nuevo.username}</strong> creado.</p>"
    )

# HTMX proyectos

@app.get("/htmx/proyectos", response_class=HTMLResponse)
def htmx_listar_proyectos(
    request: Request,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    lista = db.query(Proyecto).all()
    proyectos_data = [
        {
            "id": p.id,
            "nombre": p.nombre,
            "descripcion": p.descripcion,
            "tareas": [_tarea_a_dict(t) for t in p.tareas],
            "lider_id": p.lider_id,
        }
        for p in lista
    ]
    usuarios_lista = db.query(Usuario).filter(Usuario.activo == True).all()
    return templates.TemplateResponse(
        request=request,
        name="proyectos/lista.html",
        context={
            "proyectos": proyectos_data,
            "current_user": current_user,
            "es_lider": current_user.rol == RolUsuario.LIDER,
            "usuarios": usuarios_lista,
        },
    )


@app.post("/htmx/proyectos", response_class=HTMLResponse)
def htmx_crear_proyecto(
    request: Request,
    nombre: str = Form(...),
    descripcion: str = Form(""),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_lider),   # solo líderes
):
    if len(nombre) < 3:
        return HTMLResponse(
            "<p class='error-msg'>El nombre debe tener mínimo 3 caracteres!</p>",
            status_code=422,
        )

    nuevo = Proyecto(
        nombre=nombre,
        descripcion=descripcion or None,
        lider_id=current_user.id,          # el líder es quien está logueado
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    lista = db.query(Proyecto).all()
    proyectos_data = [
        {
            "id": p.id,
            "nombre": p.nombre,
            "descripcion": p.descripcion,
            "tareas": [_tarea_a_dict(t) for t in p.tareas],
            "lider_id": p.lider_id,
        }
        for p in lista
    ]
    usuarios_lista = db.query(Usuario).filter(Usuario.activo == True).all()
    return templates.TemplateResponse(
        request=request,
        name="proyectos/lista.html",
        context={
            "proyectos": proyectos_data,
            "current_user": current_user,
            "es_lider": current_user.rol == RolUsuario.LIDER,
            "usuarios": usuarios_lista,
        },
    )


@app.get("/htmx/proyectos/{proyecto_id}/tareas", response_class=HTMLResponse)
def htmx_listar_tareas(
    request: Request,
    proyecto_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    proyecto = buscar_proyecto(proyecto_id, db)
    tareas_data = [_tarea_a_dict(t) for t in proyecto.tareas]
    usuarios_lista = db.query(Usuario).filter(Usuario.activo == True).all()
    return templates.TemplateResponse(
        request=request,
        name="tareas/lista.html",
        context={
            "tareas": tareas_data,
            "proyecto_id": proyecto_id,
            "usuarios": usuarios_lista,
            "current_user": current_user,
            "es_lider": current_user.rol == RolUsuario.LIDER,
        },
    )


@app.post("/htmx/proyectos/{proyecto_id}/tareas", response_class=HTMLResponse)
def htmx_crear_tarea(
    request: Request,
    proyecto_id: int,
    titulo: str = Form(...),
    descripcion: str = Form(""),
    prioridad: str = Form("MEDIA"),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    if len(titulo) < 3:
        return HTMLResponse(
            "<p class='error-msg'>El título debe tener mínimo 3 caracteres!</p>",
            status_code=422,
        )

    buscar_proyecto(proyecto_id, db)

    from src.domain.enums import PrioridadTarea
    prioridad_map = {
        "ALTA": PrioridadTarea.ALTA,
        "MEDIA": PrioridadTarea.MEDIA,
        "BAJA": PrioridadTarea.BAJA,
    }
    prioridad_enum = prioridad_map.get(prioridad, PrioridadTarea.MEDIA)

    nueva = Tarea(
        titulo=titulo,
        descripcion=descripcion or None,
        prioridad=prioridad_enum,
        estado=EstadoTarea.PENDIENTE,
        proyecto_id=proyecto_id,
        creador_id=current_user.id,        # el creador es quien está logueado
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)

    proyecto = buscar_proyecto(proyecto_id, db)
    tareas_data = [_tarea_a_dict(t) for t in proyecto.tareas]
    usuarios_lista = db.query(Usuario).filter(Usuario.activo == True).all()
    return templates.TemplateResponse(
        request=request,
        name="tareas/lista.html",
        context={
            "tareas": tareas_data,
            "proyecto_id": proyecto_id,
            "usuarios": usuarios_lista,
            "current_user": current_user,
            "es_lider": current_user.rol == RolUsuario.LIDER,
        },
    )

# HTMX tareas

@app.patch("/htmx/tareas/{tarea_id}/completar", response_class=HTMLResponse)
def htmx_completar_tarea(
    request: Request,
    tarea_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    tarea = buscar_tarea(tarea_id, db)
    tarea.estado = EstadoTarea.COMPLETADA
    tarea.fecha_completado = datetime.utcnow()
    db.commit()
    db.refresh(tarea)
    return templates.TemplateResponse(
        request=request,
        name="tareas/item.html",
        context={
            "tarea": _tarea_a_dict(tarea),
            "proyecto_id": tarea.proyecto_id,
            "current_user": current_user,
            "es_lider": current_user.rol == RolUsuario.LIDER,
        },
    )


@app.patch("/htmx/tareas/{tarea_id}/prioridad", response_class=HTMLResponse)
def htmx_cambiar_prioridad(
    request: Request,
    tarea_id: int,
    prioridad: str = Form(...),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    from src.domain.enums import PrioridadTarea
    tarea = buscar_tarea(tarea_id, db)
    prioridad_map = {
        "ALTA": PrioridadTarea.ALTA,
        "MEDIA": PrioridadTarea.MEDIA,
        "BAJA": PrioridadTarea.BAJA,
    }
    tarea.prioridad = prioridad_map.get(prioridad, PrioridadTarea.MEDIA)
    db.commit()
    db.refresh(tarea)
    return templates.TemplateResponse(
        request=request,
        name="tareas/item.html",
        context={
            "tarea": _tarea_a_dict(tarea),
            "proyecto_id": tarea.proyecto_id,
            "current_user": current_user,
            "es_lider": current_user.rol == RolUsuario.LIDER,
        },
    )

def _tarea_a_dict(t: Tarea) -> dict:
    return {
        "id": t.id,
        "titulo": t.titulo,
        "descripcion": t.descripcion,
        "estado": t.estado.value if hasattr(t.estado, "value") else t.estado,
        "prioridad": t.prioridad.value if hasattr(t.prioridad, "value") else t.prioridad,
        "creador_id": t.creador_id,
    }