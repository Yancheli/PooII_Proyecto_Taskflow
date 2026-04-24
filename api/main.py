from datetime import datetime
import hashlib

from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from api.routes import usuarios, proyectos, tareas
from api.database import get_db, buscar_proyecto, buscar_tarea
from database.modelsalchemy import Proyecto, Tarea, Usuario
from src.domain.enums import EstadoTarea


app = FastAPI(
    title="TaskFlow API",
    description="API para gestión de usuarios, proyectos y tareas",
    version="1.0.0"
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.include_router(usuarios.router)
app.include_router(proyectos.router)
app.include_router(tareas.router)


def _obtener_o_crear_usuario_default(db: Session) -> Usuario:
    """Si no hay usuarios, crea uno por defecto para poder operar."""
    usuario = db.query(Usuario).first()
    if not usuario:
        hashed_pw = hashlib.sha256(b"admin").hexdigest()
        usuario = Usuario(
            username="admin",
            email="admin@taskflow.com",
            hashed_password=hashed_pw,
            activo=True,
        )
        db.add(usuario)
        db.commit()
        db.refresh(usuario)
    return usuario


# Página principal

@app.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    usuarios_lista = db.query(Usuario).filter(Usuario.activo == True).all()
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"usuarios": usuarios_lista},
    )

@app.post("/htmx/usuarios", response_class=HTMLResponse)
def htmx_crear_usuario(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    db: Session = Depends(get_db),
):
    import re
    # Validaciones
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

    # Verificar duplicados
    existente = db.query(Usuario).filter(
        (Usuario.username == username) | (Usuario.email == email)
    ).first()
    if existente:
        return HTMLResponse(
            "<p class='error-msg'><i class='bi bi-x-circle me-1'></i>Ya existe un usuario con ese username o email.</p>",
            status_code=422,
        )

    hashed_pw = hashlib.sha256(username.encode()).hexdigest()
    nuevo = Usuario(
        username=username,
        email=email,
        hashed_password=hashed_pw,
        activo=True,
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return HTMLResponse(
        f"<p style='color: var(--tf-accent2);'><i class='bi bi-check-circle me-1'></i>"
        f"Usuario <strong>@{nuevo.username}</strong> creado. "
        f"<span style='color: var(--tf-muted); font-size:0.8rem;'>Recarga la página para verlo en el selector de líder.</span></p>"
    )

# Endpoints HTMX

@app.get("/htmx/proyectos", response_class=HTMLResponse)
def htmx_listar_proyectos(request: Request, db: Session = Depends(get_db)):
    lista = db.query(Proyecto).all()
    proyectos_data = [
        {
            "id": p.id,
            "nombre": p.nombre,
            "descripcion": p.descripcion,
            "tareas": [_tarea_a_dict(t) for t in p.tareas],
        }
        for p in lista
    ]
    return templates.TemplateResponse(
        request=request,
        name="proyectos/lista.html",
        context={"proyectos": proyectos_data},
    )


@app.post("/htmx/proyectos", response_class=HTMLResponse)
def htmx_crear_proyecto(
    request: Request,
    nombre: str = Form(...),
    descripcion: str = Form(""),
    lider_id: int = Form(...),
    db: Session = Depends(get_db),
):
    if len(nombre) < 3:
        return HTMLResponse(
            "<p class='error-msg'>El nombre debe tener mínimo 3 caracteres!</p>",
            status_code=422,
        )

    # Verificar que el usuario líder existe
    lider = db.get(Usuario, lider_id)
    if not lider:
        return HTMLResponse(
            "<p class='error-msg'>El usuario seleccionado no existe.</p>",
            status_code=422,
        )

    nuevo = Proyecto(
        nombre=nombre,
        descripcion=descripcion or None,
        lider_id=lider_id,
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
        }
        for p in lista
    ]
    return templates.TemplateResponse(
        request=request,
        name="proyectos/lista.html",
        context={"proyectos": proyectos_data},
    )


@app.get("/htmx/proyectos/{proyecto_id}/tareas", response_class=HTMLResponse)
def htmx_listar_tareas(
    request: Request,
    proyecto_id: int,
    db: Session = Depends(get_db),
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
        },
    )


@app.post("/htmx/proyectos/{proyecto_id}/tareas", response_class=HTMLResponse)
def htmx_crear_tarea(
    request: Request,
    proyecto_id: int,
    titulo: str = Form(...),
    descripcion: str = Form(""),
    prioridad: str = Form("MEDIA"),
    creador_id: int = Form(...),
    db: Session = Depends(get_db),
):
    if len(titulo) < 3:
        return HTMLResponse(
            "<p class='error-msg'>El título debe tener mínimo 3 caracteres!</p>",
            status_code=422,
        )

    # Verificar que el creador existe
    creador = db.get(Usuario, creador_id)
    if not creador:
        return HTMLResponse(
            "<p class='error-msg'>El usuario creador no existe.</p>",
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
        creador_id=creador_id,
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
        },
    )


@app.patch("/htmx/tareas/{tarea_id}/completar", response_class=HTMLResponse)
def htmx_completar_tarea(
    request: Request,
    tarea_id: int,
    db: Session = Depends(get_db),
):
    tarea = buscar_tarea(tarea_id, db)
    tarea.estado = EstadoTarea.COMPLETADA
    tarea.fecha_completado = datetime.utcnow()
    db.commit()
    db.refresh(tarea)
    return templates.TemplateResponse(
        request=request,
        name="tareas/item.html",
        context={"tarea": _tarea_a_dict(tarea), "proyecto_id": tarea.proyecto_id},
    )


@app.patch("/htmx/tareas/{tarea_id}/prioridad", response_class=HTMLResponse)
def htmx_cambiar_prioridad(
    request: Request,
    tarea_id: int,
    prioridad: str = Form(...),
    db: Session = Depends(get_db),
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
        context={"tarea": _tarea_a_dict(tarea), "proyecto_id": tarea.proyecto_id},
    )


def _tarea_a_dict(t: Tarea) -> dict:
    return {
        "id": t.id,
        "titulo": t.titulo,
        "descripcion": t.descripcion,
        "estado": t.estado.value if hasattr(t.estado, "value") else t.estado,
        "prioridad": t.prioridad.value if hasattr(t.prioridad, "value") else t.prioridad,
    }