from datetime import datetime
 
from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
 
from api.routes import usuarios, proyectos, tareas
from api.database import get_db, buscar_proyecto, buscar_tarea
from database.modelsalchemy import Proyecto, Tarea
from src.domain.enums import EstadoTarea


app = FastAPI(
    title="TaskFlow API",
    description="API para gestión de usuarios, proyectos y tareas",
    version="1.0.0"
)

# static y templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.include_router(usuarios.router)
app.include_router(proyectos.router)
app.include_router(tareas.router)


# Página principal

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name="index.html"
    )


# Endpoints HTMX

@app.get("/htmx/proyectos", response_class=HTMLResponse)
def htmx_listar_proyectos(request: Request, db: Session = Depends(get_db)):
    """Lista todos los proyectos"""
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
    lider_id: int = Form(1),          
    db: Session = Depends(get_db),
):
    """Crea un proyecto y lo guarda en la base"""
    if len(nombre) < 3:
        return HTMLResponse(
            "<p class='error-msg'>El nombre debe tener mínimo 3 caracteres!</p>",
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
 
    # Recarga la lista completa para que la plantilla muestre todos los proyectos
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
    """Lista las tareas de un proyecto"""
    proyecto = buscar_proyecto(proyecto_id, db)
    tareas_data = [_tarea_a_dict(t) for t in proyecto.tareas]
    return templates.TemplateResponse(
        request=request,
        name="tareas/lista.html",
        context={"tareas": tareas_data, "proyecto_id": proyecto_id},
    )


@app.post("/htmx/proyectos/{proyecto_id}/tareas", response_class=HTMLResponse)
def htmx_crear_tarea(
    request: Request,
    proyecto_id: int,
    titulo: str = Form(...),
    descripcion: str = Form(""),
    prioridad: str = Form("MEDIA"),
    creador_id: int = Form(1),        
    db: Session = Depends(get_db),
):
    if len(titulo) < 3:
        return HTMLResponse(
            "<p class='error-msg'>El título debe tener mínimo 3 caracteres!</p>",
            status_code=422,
        )
    buscar_proyecto(proyecto_id, db)  # lanza 404 si no existe
 
    # string de prioridad de enums
    from src.domain.enums import PrioridadTarea
    prioridad_map = {"ALTA": PrioridadTarea.ALTA, "MEDIA": PrioridadTarea.MEDIA, "BAJA": PrioridadTarea.BAJA}
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
    return templates.TemplateResponse(
        request=request,
        name="tareas/lista.html",
        context={"tareas": tareas_data, "proyecto_id": proyecto_id},
    )


@app.patch("/htmx/tareas/{tarea_id}/completar", response_class=HTMLResponse)
def htmx_completar_tarea(
    request: Request,
    tarea_id: int,
    db: Session = Depends(get_db),
):
    """Marca la tarea como completada y guarda la fecha en la base"""
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
    prioridad_map = {"ALTA": PrioridadTarea.ALTA, "MEDIA": PrioridadTarea.MEDIA, "BAJA": PrioridadTarea.BAJA}
    tarea.prioridad = prioridad_map.get(prioridad, PrioridadTarea.MEDIA)
    db.commit()
    db.refresh(tarea)
    return templates.TemplateResponse(
        request=request,
        name="tareas/item.html",
        context={"tarea": _tarea_a_dict(tarea), "proyecto_id": tarea.proyecto_id},
    )

# Helper interno para la ruta anterior
def _tarea_a_dict(t: Tarea) -> dict:
    """
    Convierte un objeto ORM Tarea en el dict que esperan las plantillas Jinja2 que definimos en las primeras fases
    """
    return {
        "id": t.id,
        "titulo": t.titulo,
        "descripcion": t.descripcion,
        "estado": t.estado.value if hasattr(t.estado, "value") else t.estado,
        "prioridad": t.prioridad.value if hasattr(t.prioridad, "value") else t.prioridad,
    }