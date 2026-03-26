from fastapi import APIRouter
from api.models import ProyectoCreate, TareaCreate
from api.database import proyectos, buscar_proyecto

router = APIRouter(prefix="/proyectos", tags=["Proyectos"])


@router.get("", summary="Listar proyectos")
def listar_proyectos():
    return proyectos


@router.post("", status_code=201, summary="Crear proyecto")
def crear_proyecto(proyecto: ProyectoCreate):
    nuevo = proyecto.model_dump()
    nuevo["id"] = len(proyectos) + 1
    nuevo["tareas"] = []
    proyectos.append(nuevo)
    return nuevo


@router.get("/{proyecto_id}", summary="Obtener proyecto por ID")
def obtener_proyecto(proyecto_id: int):
    return buscar_proyecto(proyecto_id)


@router.post("/{proyecto_id}/tareas", status_code=201, summary="Crear tarea en proyecto")
def crear_tarea(proyecto_id: int, tarea: TareaCreate):
    proyecto = buscar_proyecto(proyecto_id)
    nueva = tarea.model_dump()
    nueva["id"] = len(proyecto["tareas"]) + 1
    nueva["estado"] = "pendiente"
    nueva["prioridad"] = nueva["prioridad"].value if hasattr(nueva["prioridad"], "value") else nueva["prioridad"]
    proyecto["tareas"].append(nueva)
    return nueva


@router.get("/{proyecto_id}/tareas", summary="Listar tareas de un proyecto")
def listar_tareas(proyecto_id: int):
    proyecto = buscar_proyecto(proyecto_id)
    return proyecto.get("tareas", [])