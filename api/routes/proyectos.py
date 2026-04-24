from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.models import ProyectoCreate, TareaCreate, ProyectoResponse, TareaResponse
from api.database import get_db, buscar_proyecto
from database.modelsalchemy import Proyecto, Tarea
from src.domain.enums import EstadoTarea

router = APIRouter(prefix="/proyectos", tags=["Proyectos"])

@router.get("", summary="Listar proyectos", response_model=list[ProyectoResponse])
def listar_proyectos(db: Session = Depends(get_db)):
    """Devuelve todos los proyectos en la base"""
    return db.query(Proyecto).all()
 
 
@router.post("", status_code=201, summary="Crear proyecto", response_model=ProyectoResponse)
def crear_proyecto(proyecto: ProyectoCreate, lider_id: int, db: Session = Depends(get_db)):
    """
    Por ahora no hay autenticación, asi que se utiliza un parametro provisional
    """
    nuevo = Proyecto(
        nombre=proyecto.nombre,
        descripcion=proyecto.descripcion,
        lider_id=lider_id,
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo
 
 
@router.get("/{proyecto_id}", summary="Obtener proyecto por ID", response_model=ProyectoResponse)
def obtener_proyecto(proyecto_id: int, db: Session = Depends(get_db)):
    return buscar_proyecto(proyecto_id, db)
 
 
@router.post(
    "/{proyecto_id}/tareas",
    status_code=201,
    summary="Crear tarea en proyecto",
    response_model=TareaResponse,
)
def crear_tarea(
    proyecto_id: int,
    tarea: TareaCreate,
    creador_id: int,
    db: Session = Depends(get_db),
):

    buscar_proyecto(proyecto_id, db)   # lanza 404 si no existe
 
    nueva = Tarea(
        titulo=tarea.titulo,
        descripcion=tarea.descripcion,
        prioridad=tarea.prioridad,
        estado=EstadoTarea.PENDIENTE,
        proyecto_id=proyecto_id,
        creador_id=creador_id,
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva
 
 
@router.get(
    "/{proyecto_id}/tareas",
    summary="Listar tareas de un proyecto",
    response_model=list[TareaResponse],
)
def listar_tareas(proyecto_id: int, db: Session = Depends(get_db)):
    proyecto = buscar_proyecto(proyecto_id, db)
    return proyecto.tareas