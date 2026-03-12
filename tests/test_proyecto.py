import pytest
from src.domain.proyecto import Proyecto
from src.domain.tarea import Tarea
from src.domain.enums import PrioridadTarea


class TestProyecto:

    def test_crear_proyecto(self, usuario_ejemplo):
        proyecto = Proyecto(
            nombre="Proyecto Test",
            lider=usuario_ejemplo
        )

        assert proyecto.nombre == "Proyecto Test"
        assert proyecto.lider == usuario_ejemplo


    def test_nombre_invalido(self, usuario_ejemplo):
        with pytest.raises(ValueError):
            Proyecto(nombre="ab", lider=usuario_ejemplo)


    def test_agregar_tarea(self, proyecto_ejemplo, tarea_ejemplo):
        proyecto_ejemplo.agregar_tarea(tarea_ejemplo)

        assert len(proyecto_ejemplo.tareas) == 1


    def test_agregar_tarea_invalida(self, proyecto_ejemplo):
        with pytest.raises(ValueError):
            proyecto_ejemplo.agregar_tarea("no es tarea")


    def test_obtener_tareas_pendientes(self, proyecto_con_tareas):
        pendientes = proyecto_con_tareas.obtener_tareas_pendientes()

        assert len(pendientes) >= 1


    def test_filtrar_por_prioridad(self, proyecto_con_tareas):
        tareas = proyecto_con_tareas.obtener_tareas_por_prioridad(
            PrioridadTarea.ALTA
        )

        for tarea in tareas:
            assert tarea.prioridad == PrioridadTarea.ALTA