import pytest
from src.domain.usuario import Usuario
from src.domain.proyecto import Proyecto
from src.domain.tarea import Tarea
from src.domain.enums import PrioridadTarea


@pytest.fixture
def usuario_ejemplo():
    """Usuario válido para pruebas."""
    return Usuario(
        username="testuser",
        email="test@example.com",
        nombre_completo="Usuario Test"
    )


@pytest.fixture
def proyecto_ejemplo(usuario_ejemplo):
    """Proyecto con líder."""
    return Proyecto(
        nombre="Proyecto Test",
        descripcion="Proyecto de prueba",
        lider=usuario_ejemplo
    )


@pytest.fixture
def tarea_ejemplo():
    """Tarea pendiente."""
    return Tarea(
        titulo="Tarea de prueba",
        prioridad=PrioridadTarea.MEDIA,
        descripcion="Descripción"
    )


@pytest.fixture
def proyecto_con_tareas(proyecto_ejemplo, tarea_ejemplo):
    """Proyecto con varias tareas."""
    proyecto_ejemplo.agregar_tarea(tarea_ejemplo)

    otra = Tarea(
        titulo="Otra tarea",
        prioridad=PrioridadTarea.ALTA
    )

    proyecto_ejemplo.agregar_tarea(otra)

    return proyecto_ejemplo