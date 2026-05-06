from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.auth import get_current_user, require_lider
from api.database import get_db
from api.schemas.proyecto import ProyectoCreate, ProyectoOut, ProyectoUpdate
from api.services import proyecto_service
from database.modelsalchemy import Usuario

router = APIRouter(prefix="/api/proyectos", tags=["Proyectos CRUD"])


@router.post("", response_model=ProyectoOut, status_code=201,
             summary="Crear proyecto")
def crear(
    datos: ProyectoCreate,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(require_lider),   # solo líderes
):
    """Crea un proyecto. El líder queda como dueño"""
    return proyecto_service.crear_proyecto(db, datos, usuario_actual)


@router.get("", response_model=list[ProyectoOut], summary="Listar proyectos")
def listar(db: Session = Depends(get_db)):
    """Devuelve todos los proyectos existentes."""
    return proyecto_service.listar_proyectos(db)


@router.get("/mios", response_model=list[ProyectoOut],
            summary="Proyectos del usuario autenticado")
def mis_proyectos(
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    """Lista los proyectos creados por el usuario"""
    return proyecto_service.listar_proyectos_de_usuario(db, usuario_actual.id)


@router.get("/{proyecto_id}", response_model=ProyectoOut,
            summary="Obtener proyecto")
def obtener(proyecto_id: int, db: Session = Depends(get_db)):
    """Devuelve un proyecto por su ID."""
    return proyecto_service.obtener_proyecto(db, proyecto_id)


@router.patch("/{proyecto_id}", response_model=ProyectoOut,
              summary="Editar proyecto")
def editar(
    proyecto_id: int,
    datos: ProyectoUpdate,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(require_lider),
):
    """Edita nombre y/o descripción. Solo el líder dueño puede hacerlo"""
    return proyecto_service.editar_proyecto(db, proyecto_id, datos, usuario_actual)


@router.delete("/{proyecto_id}", status_code=204, summary="Eliminar proyecto")
def eliminar(
    proyecto_id: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(require_lider),
):
    """Elimina un proyecto. Solo el líder dueño puede hacerlo"""
    proyecto_service.eliminar_proyecto(db, proyecto_id, usuario_actual)