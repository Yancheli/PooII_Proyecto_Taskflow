from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from database.modelsalchemy import Tarea
from src.domain.enums import EstadoTarea


def obtener_por_id(db: Session, tarea_id: int) -> Optional[Tarea]:
    return db.get(Tarea, tarea_id)


def listar_por_proyecto(db: Session, proyecto_id: int) -> list[Tarea]:
    return db.query(Tarea).filter(Tarea.proyecto_id == proyecto_id).all()


def contar_por_proyecto(db: Session, proyecto_id: int) -> int:
    return db.query(Tarea).filter(Tarea.proyecto_id == proyecto_id).count()


def crear(db: Session, tarea: Tarea) -> Tarea:
    try:
        db.add(tarea)
        db.commit()
        db.refresh(tarea)
        return tarea
    except Exception:
        db.rollback()
        raise


def actualizar(db: Session, tarea: Tarea) -> Tarea:
    try:
        db.commit()
        db.refresh(tarea)
        return tarea
    except Exception:
        db.rollback()
        raise


def completar(db: Session, tarea: Tarea) -> Tarea:
    try:
        tarea.estado = EstadoTarea.COMPLETADA
        tarea.fecha_completado = datetime.utcnow()
        db.commit()
        db.refresh(tarea)
        return tarea
    except Exception:
        db.rollback()
        raise


def eliminar(db: Session, tarea: Tarea) -> None:
    try:
        db.delete(tarea)
        db.commit()
    except Exception:
        db.rollback()
        raise