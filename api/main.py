from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Routes/rutas de cada entidad
from api.routes import usuarios, proyectos, tareas

# Base de datos compartida 
from api.database import buscar_proyecto, buscar_tarea
from api.database import proyectos as db_proyectos

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
    return templates.TemplateResponse("index.html", {"request": request})


# Endpoints

@app.get("/htmx/proyectos", response_class=HTMLResponse)
def htmx_listar_proyectos(request: Request):
    return templates.TemplateResponse(
        "proyectos/lista.html",
        {"request": request, "proyectos": db_proyectos}
    )


@app.post("/htmx/proyectos", response_class=HTMLResponse)
def htmx_crear_proyecto(
    request: Request,
    nombre: str = Form(...),
    descripcion: str = Form("")
):
    if len(nombre) < 3:
        return HTMLResponse(
            "<p class='error-msg'>El nombre debe tener mínimo 3 caracteres.</p>",
            status_code=422
        )
    nuevo = {
        "id": len(db_proyectos) + 1,
        "nombre": nombre,
        "descripcion": descripcion,
        "tareas": []
    }
    db_proyectos.append(nuevo)
    return templates.TemplateResponse(
        "proyectos/lista.html",
        {"request": request, "proyectos": db_proyectos}
    )


@app.get("/htmx/proyectos/{proyecto_id}/tareas", response_class=HTMLResponse)
def htmx_listar_tareas(request: Request, proyecto_id: int):
    proyecto = buscar_proyecto(proyecto_id)
    return templates.TemplateResponse(
        "tareas/lista.html",
        {"request": request, "tareas": proyecto.get("tareas", []), "proyecto_id": proyecto_id}
    )


@app.post("/htmx/proyectos/{proyecto_id}/tareas", response_class=HTMLResponse)
def htmx_crear_tarea(
    request: Request,
    proyecto_id: int,
    titulo: str = Form(...),
    descripcion: str = Form(""),
    prioridad: str = Form("MEDIA")
):
    if len(titulo) < 3:
        return HTMLResponse(
            "<p class='error-msg'>El título debe tener mínimo 3 caracteres.</p>",
            status_code=422
        )
    proyecto = buscar_proyecto(proyecto_id)
    nueva = {
        "id": len(proyecto["tareas"]) + 1,
        "titulo": titulo,
        "descripcion": descripcion,
        "prioridad": prioridad,
        "estado": "pendiente"
    }
    proyecto["tareas"].append(nueva)
    return templates.TemplateResponse(
        "tareas/lista.html",
        {"request": request, "tareas": proyecto["tareas"], "proyecto_id": proyecto_id}
    )


@app.patch("/htmx/tareas/{tarea_id}/completar", response_class=HTMLResponse)
def htmx_completar_tarea(request: Request, tarea_id: int):
    proyecto, tarea = buscar_tarea(tarea_id)
    tarea["estado"] = "completada"
    return templates.TemplateResponse(
        "tareas/item.html",
        {"request": request, "tarea": tarea, "proyecto_id": proyecto["id"]}
    )


@app.patch("/htmx/tareas/{tarea_id}/prioridad", response_class=HTMLResponse)
def htmx_cambiar_prioridad(
    request: Request,
    tarea_id: int,
    prioridad: str = Form(...)
):
    proyecto, tarea = buscar_tarea(tarea_id)
    tarea["prioridad"] = prioridad
    return templates.TemplateResponse(
        "tareas/item.html",
        {"request": request, "tarea": tarea, "proyecto_id": proyecto["id"]}
    )