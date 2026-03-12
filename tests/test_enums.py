from src.domain.enums import PrioridadTarea, EstadoTarea


def test_prioridades():
    assert PrioridadTarea.ALTA.value == 1
    assert PrioridadTarea.MEDIA.value == 2
    assert PrioridadTarea.BAJA.value == 3


def test_estados():
    assert EstadoTarea.PENDIENTE.value == "pendiente"
    assert EstadoTarea.EN_PROGRESO.value == "en_progreso"
    assert EstadoTarea.COMPLETADA.value == "completada"