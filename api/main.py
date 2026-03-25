from fastapi import FastAPI
from src.domain.usuario import Usuario
from api.models import UsuarioCreate
from fastapi import HTTPException
from api.models import ProyectoCreate
from api.models import TareaCreate


app = FastAPI(
    title="TaskFlow API",
    description="API para gestión de usuarios, proyectos y tareas",
    version="1.0.0"
)

# Base de datos temporal (memoria)
usuarios = []
proyectos = []

@app.get("/")
def home():
    return {"mensaje": "API TaskFlow funcionando correctamente"}


@app.get("/usuarios")
def listar_usuarios():
    return usuarios

@app.post("/usuarios", status_code=201)
def crear_usuario(usuario: UsuarioCreate):
    nuevo_usuario = usuario.dict()
    nuevo_usuario["id"] = len(usuarios) + 1
    usuarios.append(nuevo_usuario)
    return nuevo_usuario

@app.get("/usuarios/{usuario_id}")
def obtener_usuario(usuario_id: int):
    for usuario in usuarios:
        if usuario["id"] == usuario_id:
            return usuario
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

@app.get("/proyectos")
def listar_proyectos():
    return proyectos

@app.post("/proyectos", status_code=201)
def crear_proyecto(proyecto: ProyectoCreate):
    nuevo_proyecto = proyecto.dict()
    nuevo_proyecto["id"] = len(proyectos) + 1
    proyectos.append(nuevo_proyecto)
    return nuevo_proyecto

@app.get("/proyectos/{proyecto_id}")
def obtener_proyecto(proyecto_id: int):
    for proyecto in proyectos:
        if proyecto["id"] == proyecto_id:
            return proyecto
    return {"error": "Proyecto no encontrado"}

@app.post("/proyectos/{proyecto_id}/tareas", status_code=201)
def crear_tarea(proyecto_id: int, tarea: TareaCreate):

    for proyecto in proyectos:
        if proyecto["id"] == proyecto_id:

            if "tareas" not in proyecto:
                proyecto["tareas"] = []

            nueva_tarea = tarea.dict()
            nueva_tarea["id"] = len(proyecto["tareas"]) + 1

            proyecto["tareas"].append(nueva_tarea)

            return nueva_tarea

    return {"error": "Proyecto no encontrado"}

@app.get("/proyectos/{proyecto_id}/tareas")
def listar_tareas(proyecto_id: int):

    for proyecto in proyectos:
        if proyecto["id"] == proyecto_id:

            if "tareas" not in proyecto:
                return []

            return proyecto["tareas"]

    return {"error": "Proyecto no encontrado"}
