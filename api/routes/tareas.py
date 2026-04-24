from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.models import TareaUpdate,TareaResponse
from api.database import get_db, buscar_tarea
from database.modelsalchemy import Tarea
from src.domain.enums import EstadoTarea

router = APIRouter(prefix="/tareas", tags=["Tareas"])


@router.patch("/{tarea_id}/completar", summary="Marcar tarea como completada", response_model=TareaResponse)
def completar_tarea(tarea_id: int, db: Session = Depends(get_db)):
    
    tarea: Tarea = buscar_tarea(tarea_id, db)
    tarea.estado = EstadoTarea.COMPLETADA
    tarea.fecha_completado = datetime.utcnow()
    db.commit()
    db.refresh(tarea)
    return tarea
 
 
@router.patch("/{tarea_id}/prioridad", summary="Cambiar prioridad de una tarea", response_model=TareaResponse)
def cambiar_prioridad(tarea_id: int, datos: TareaUpdate, db: Session = Depends(get_db)):
    """
    Cambia la prioridad de una tarea y persiste el cambio en la Base
    """
    tarea: Tarea = buscar_tarea(tarea_id, db)
    if datos.prioridad is not None:
        tarea.prioridad = datos.prioridad
    db.commit()
    db.refresh(tarea)
    return tarea