"""Entidad Tarea del sistema TaskFlow."""

from datetime import datetime
from src.domain.enums import PrioridadTarea, EstadoTarea


class Tarea:
    """Representa una tarea dentro de un proyecto.

    Attributes:
        titulo (str): Título de la tarea.
        descripcion (str | None): Descripción opcional.
        prioridad (PrioridadTarea): Nivel de prioridad.
        estado (EstadoTarea): Estado actual de la tarea.
        fecha_creacion (datetime): Fecha de creación.
        fecha_completado (datetime | None): Fecha de finalización.
    """

    def __init__(
        self,
        titulo: str,
        prioridad: PrioridadTarea,
        descripcion: str | None = None,
    ) -> None:
        """Inicializa una nueva tarea.

        Args:
            titulo: Título de la tarea (mínimo 3 caracteres).
            prioridad: Nivel de prioridad.
            descripcion: Descripción opcional.

        Raises:
            ValueError: Si el título no cumple validación.
        """
        self._validar_titulo(titulo)
        self._titulo = titulo
        self._descripcion = descripcion
        self._prioridad = prioridad
        self._estado = EstadoTarea.PENDIENTE
        self._fecha_creacion = datetime.now()
        self._fecha_completado: datetime | None = None

        #validaciones

    def _validar_titulo(self, titulo: str) -> None:
        """Valida que el título tenga mínimo 3 caracteres."""
        if len(titulo) < 3:
            raise ValueError(
                "El título debe tener mínimo 3 caracteres."
            )

    @property
    def titulo(self) -> str:
        """Obtiene el título de la tarea."""
        return self._titulo

    @property
    def prioridad(self) -> PrioridadTarea:
        """Obtiene la prioridad de la tarea."""
        return self._prioridad

    @property
    def estado(self) -> EstadoTarea:
        """Obtiene el estado actual."""
        return self._estado

    @property
    def fecha_creacion(self) -> datetime:
        """Obtiene la fecha de creación."""
        return self._fecha_creacion

    @property
    def fecha_completado(self) -> datetime | None:
        """Obtiene la fecha de finalización."""
        return self._fecha_completado

    def iniciar(self) -> None:
        """Cambia el estado a EN_PROGRESO."""
        if self._estado == EstadoTarea.COMPLETADA:
            raise ValueError(
                "No se puede iniciar una tarea completada."
            )
        self._estado = EstadoTarea.EN_PROGRESO

    def completar(self) -> None:
        """Marca la tarea como completada."""
        self._estado = EstadoTarea.COMPLETADA
        self._fecha_completado = datetime.now()

    def cambiar_prioridad(
        self, nueva_prioridad: PrioridadTarea
    ) -> None:
        """Cambia la prioridad de la tarea."""
        self._prioridad = nueva_prioridad
        
        #metodos

    def __str__(self) -> str:
        """Representación amigable de la tarea."""
        return (
            f"[{self._prioridad.name}] "
            f"{self._titulo} "
            f"({self._estado.value})"
        )