from fastapi import HTTPException
from sqlalchemy.orm import Session

from api.repositories import proyecto_repo
from api.schemas.proyecto import ProyectoCreate, ProyectoUpdate
from database.modelsalchemy import Proyecto, Usuario


def crear_proyecto(db: Session, datos: ProyectoCreate, lider: Usuario) -> Proyecto:
    """Solo un líder puede crear proyectos"""
    nuevo = Proyecto(
        nombre=datos.nombre,
        descripcion=datos.descripcion,
        lider_id=lider.id,
    )
    return proyecto_repo.crear(db, nuevo)


def obtener_proyecto(db: Session, proyecto_id: int) -> Proyecto:
    proyecto = proyecto_repo.obtener_por_id(db, proyecto_id)
    if not proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    return proyecto


def listar_proyectos(db: Session) -> list[Proyecto]:
    return proyecto_repo.listar_todos(db)


def listar_proyectos_de_usuario(db: Session, lider_id: int) -> list[Proyecto]:
    return proyecto_repo.listar_por_lider(db, lider_id)


def editar_proyecto(
    db: Session, proyecto_id: int, datos: ProyectoUpdate, usuario_actual: Usuario
) -> Proyecto:
    proyecto = obtener_proyecto(db, proyecto_id)

    # Solo el líder dueño puede editar su proyecto
    if proyecto.lider_id != usuario_actual.id:
        raise HTTPException(
            status_code=403, detail="Solo el líder del proyecto puede editarlo"
        )

    if datos.nombre is not None:
        proyecto.nombre = datos.nombre
    if datos.descripcion is not None:
        proyecto.descripcion = datos.descripcion

    return proyecto_repo.actualizar(db, proyecto)


def eliminar_proyecto(
    db: Session, proyecto_id: int, usuario_actual: Usuario
) -> None:
    proyecto = obtener_proyecto(db, proyecto_id)

    if proyecto.lider_id != usuario_actual.id:
        raise HTTPException(
            status_code=403, detail="Solo el líder del proyecto puede eliminarlo"
        )

    proyecto_repo.eliminar(db, proyecto)