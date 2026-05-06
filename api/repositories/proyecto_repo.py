from typing import Optional

from sqlalchemy.orm import Session

from database.modelsalchemy import Proyecto


def obtener_por_id(db: Session, proyecto_id: int) -> Optional[Proyecto]:
    return db.get(Proyecto, proyecto_id)


def listar_todos(db: Session) -> list[Proyecto]:
    return db.query(Proyecto).all()


def listar_por_lider(db: Session, lider_id: int) -> list[Proyecto]:
    return db.query(Proyecto).filter(Proyecto.lider_id == lider_id).all()


def contar(db: Session) -> int:
    return db.query(Proyecto).count()


def crear(db: Session, proyecto: Proyecto) -> Proyecto:
    try:
        db.add(proyecto)
        db.commit()
        db.refresh(proyecto)
        return proyecto
    except Exception:
        db.rollback()
        raise


def actualizar(db: Session, proyecto: Proyecto) -> Proyecto:
    try:
        db.commit()
        db.refresh(proyecto)
        return proyecto
    except Exception:
        db.rollback()
        raise


def eliminar(db: Session, proyecto: Proyecto) -> None:
    try:
        db.delete(proyecto)
        db.commit()
    except Exception:
        db.rollback()
        raise