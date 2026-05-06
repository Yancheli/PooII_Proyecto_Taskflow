from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.auth import get_current_user
from api.database import get_db
from api.schemas.tarea import TareaCreate, TareaOut, TareaUpdate
from api.services import tarea_service
from database.modelsalchemy import Usuario

router = APIRouter(prefix="/api/proyectos", tags=["Tareas CRUD"])


@router.post("/{proyecto_id}/tareas", response_model=TareaOut, status_code=201,
             summary="Crear tarea en proyecto")
def crear(
    proyecto_id: int,
    datos: TareaCreate,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    """Crea una tarea dentro del proyecto indicado."""
    return tarea_service.crear_tarea(db, proyecto_id, datos, usuario_actual)


@router.get("/{proyecto_id}/tareas", response_model=list[TareaOut],
            summary="Listar tareas de un proyecto")
def listar(
    proyecto_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    """Devuelve todas las tareas del proyecto."""
    return tarea_service.listar_tareas_de_proyecto(db, proyecto_id)


@router.get("/tareas/{tarea_id}", response_model=TareaOut,
            summary="Obtener tarea por ID")
def obtener(
    tarea_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    """Devuelve una tarea por su ID."""
    return tarea_service.obtener_tarea(db, tarea_id)


@router.patch("/tareas/{tarea_id}", response_model=TareaOut,
              summary="Editar tarea")
def editar(
    tarea_id: int,
    datos: TareaUpdate,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    """Edita título, descripción, prioridad o estado. Solo el creador puede hacerlo"""
    return tarea_service.editar_tarea(db, tarea_id, datos, usuario_actual)


@router.patch("/tareas/{tarea_id}/completar", response_model=TareaOut,
              summary="Completar tarea")
def completar(
    tarea_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    """Marca la tarea como completada y registra la fecha en que se termina"""
    return tarea_service.completar_tarea(db, tarea_id)


@router.delete("/tareas/{tarea_id}", status_code=204, summary="Eliminar tarea")
def eliminar(
    tarea_id: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    """Elimina una tarea. Solo el creador puede hacerlo"""
    tarea_service.eliminar_tarea(db, tarea_id, usuario_actual)