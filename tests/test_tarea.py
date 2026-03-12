import pytest
from src.domain.tarea import Tarea
from src.domain.enums import PrioridadTarea, EstadoTarea


class TestTarea:

    def test_crear_tarea_valida(self, tarea_ejemplo):
        assert tarea_ejemplo.titulo == "Tarea de prueba"
        assert tarea_ejemplo.estado == EstadoTarea.PENDIENTE


    @pytest.mark.parametrize("titulo", [
        "ab",
        ""
    ])
    def test_titulo_invalido(self, titulo):
        with pytest.raises(ValueError):
            Tarea(titulo=titulo, prioridad=PrioridadTarea.ALTA)


    def test_iniciar_tarea(self, tarea_ejemplo):
        tarea_ejemplo.iniciar()
        assert tarea_ejemplo.estado == EstadoTarea.EN_PROGRESO


    def test_completar_tarea(self, tarea_ejemplo):
        tarea_ejemplo.completar()

        assert tarea_ejemplo.estado == EstadoTarea.COMPLETADA
        assert tarea_ejemplo.fecha_completado is not None


    def test_cambiar_prioridad(self, tarea_ejemplo):
        tarea_ejemplo.cambiar_prioridad(PrioridadTarea.ALTA)

        assert tarea_ejemplo.prioridad == PrioridadTarea.ALTA


    def test_no_iniciar_tarea_completada(self, tarea_ejemplo):
        tarea_ejemplo.completar()

        with pytest.raises(ValueError):
            tarea_ejemplo.iniciar()