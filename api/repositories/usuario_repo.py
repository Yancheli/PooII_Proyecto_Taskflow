from typing import Optional

from sqlalchemy.orm import Session

from database.modelsalchemy import Usuario


def obtener_por_id(db: Session, usuario_id: int) -> Optional[Usuario]:
    return db.get(Usuario, usuario_id)


def obtener_por_username(db: Session, username: str) -> Optional[Usuario]:
    return db.query(Usuario).filter(Usuario.username == username).first()


def obtener_por_email(db: Session, email: str) -> Optional[Usuario]:
    return db.query(Usuario).filter(Usuario.email == email).first()


def listar_todos(db: Session) -> list[Usuario]:
    return db.query(Usuario).all()


def contar(db: Session) -> int:
    return db.query(Usuario).count()


def crear(db: Session, usuario: Usuario) -> Usuario:
    try:
        db.add(usuario)
        db.commit()
        db.refresh(usuario)
        return usuario
    except Exception:
        db.rollback()
        raise


def actualizar(db: Session, usuario: Usuario) -> Usuario:
    try:
        db.commit()
        db.refresh(usuario)
        return usuario
    except Exception:
        db.rollback()
        raise


def eliminar(db: Session, usuario: Usuario) -> None:
    try:
        db.delete(usuario)
        db.commit()
    except Exception:
        db.rollback()
        raise