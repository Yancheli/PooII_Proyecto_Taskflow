from fastapi import APIRouter
from api.models import TareaUpdate
from api.database import buscar_tarea

router = APIRouter(prefix="/tareas", tags=["Tareas"])


@router.patch("/{tarea_id}/completar", summary="Marcar tarea como completada")
def completar_tarea(tarea_id: int):
    _, tarea = buscar_tarea(tarea_id)
    tarea["estado"] = "completada"
    return tarea


@router.patch("/{tarea_id}/prioridad", summary="Cambiar prioridad de una tarea")
def cambiar_prioridad(tarea_id: int, datos: TareaUpdate):
    _, tarea = buscar_tarea(tarea_id)
    if datos.prioridad:
        tarea["prioridad"] = datos.prioridad.value if hasattr(datos.prioridad, "value") else datos.prioridad
    return tarea