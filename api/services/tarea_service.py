from fastapi import HTTPException
from sqlalchemy.orm import Session

from api.repositories import tarea_repo, proyecto_repo
from api.schemas.tarea import TareaCreate, TareaUpdate
from database.modelsalchemy import Tarea, Usuario
from src.domain.enums import EstadoTarea


def crear_tarea(
    db: Session, proyecto_id: int, datos: TareaCreate, creador: Usuario
) -> Tarea:
    """Verifica que el proyecto exista y crea la tarea"""
    if not proyecto_repo.obtener_por_id(db, proyecto_id):
        raise HTTPException(status_code=404, detail="Proyecto no encontrado.")

    nueva = Tarea(
        titulo=datos.titulo,
        descripcion=datos.descripcion,
        prioridad=datos.prioridad,
        estado=EstadoTarea.PENDIENTE,
        proyecto_id=proyecto_id,
        creador_id=creador.id,
    )
    return tarea_repo.crear(db, nueva)


def obtener_tarea(db: Session, tarea_id: int) -> Tarea:
    tarea = tarea_repo.obtener_por_id(db, tarea_id)
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada.")
    return tarea


def listar_tareas_de_proyecto(db: Session, proyecto_id: int) -> list[Tarea]:
    if not proyecto_repo.obtener_por_id(db, proyecto_id):
        raise HTTPException(status_code=404, detail="Proyecto no encontrado.")
    return tarea_repo.listar_por_proyecto(db, proyecto_id)


def editar_tarea(
    db: Session, tarea_id: int, datos: TareaUpdate, usuario_actual: Usuario
) -> Tarea:
    tarea = obtener_tarea(db, tarea_id)

    # Solo el creador puede editar la tarea
    if tarea.creador_id != usuario_actual.id:
        raise HTTPException(
            status_code=403, detail="Solo el creador puede editar esta tarea"
        )

    if datos.titulo is not None:
        tarea.titulo = datos.titulo
    if datos.descripcion is not None:
        tarea.descripcion = datos.descripcion
    if datos.prioridad is not None:
        tarea.prioridad = datos.prioridad
    if datos.estado is not None:
        if tarea.estado == EstadoTarea.COMPLETADA:
            raise HTTPException(
                status_code=400, detail="No se puede modificar una tarea completada"
            )
        tarea.estado = datos.estado

    return tarea_repo.actualizar(db, tarea)


def completar_tarea(db: Session, tarea_id: int) -> Tarea:
    tarea = obtener_tarea(db, tarea_id)
    if tarea.estado == EstadoTarea.COMPLETADA:
        raise HTTPException(status_code=400, detail="La tarea ya está completada")
    return tarea_repo.completar(db, tarea)


def eliminar_tarea(
    db: Session, tarea_id: int, usuario_actual: Usuario
) -> None:
    tarea = obtener_tarea(db, tarea_id)

    if tarea.creador_id != usuario_actual.id:
        raise HTTPException(
            status_code=403, detail="Solo el creador puede eliminar esta tarea"
        )

    tarea_repo.eliminar(db, tarea)