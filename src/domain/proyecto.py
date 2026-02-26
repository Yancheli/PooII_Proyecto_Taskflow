"""Entidad Proyecto del sistema TaskFlow."""

from datetime import datetime
from typing import List

from src.domain.usuario import Usuario
from src.domain.tarea import Tarea
from src.domain.enums import PrioridadTarea, EstadoTarea


class Proyecto:
    """Representa un proyecto que agrupa múltiples tareas.

    Attributes:
        nombre (str): Nombre del proyecto.
        descripcion (str | None): Descripción opcional.
        lider (Usuario): Usuario líder del proyecto.
        tareas (list[Tarea]): Lista de tareas del proyecto.
        fecha_creacion (datetime): Fecha de creación del proyecto.
    """

    def __init__(
        self,
        nombre: str,
        lider: Usuario,
        descripcion: str | None = None,
    ) -> None:
        """Inicializa un nuevo proyecto.

        Args:
            nombre: Nombre del proyecto (mínimo 3 caracteres).
            lider: Usuario líder del proyecto.
            descripcion: Descripción opcional.

        Raises:
            ValueError: Si el nombre no cumple validación.
        """
        self._validar_nombre(nombre)
        self._nombre = nombre
        self._descripcion = descripcion
        self._lider = lider
        self._tareas: List[Tarea] = []
        self._fecha_creacion = datetime.now()

        #validaciones

    def _validar_nombre(self, nombre: str) -> None:
        """Valida que el nombre tenga mínimo 3 caracteres."""
        if len(nombre) < 3:
            raise ValueError(
                "El nombre del proyecto debe tener mínimo 3 caracteres."
            )

    @property
    def nombre(self) -> str:
        """Obtiene el nombre del proyecto."""
        return self._nombre

    @property
    def lider(self) -> Usuario:
        """Obtiene el líder del proyecto."""
        return self._lider

    @property
    def tareas(self) -> List[Tarea]:
        """Obtiene la lista de tareas."""
        return self._tareas

    @property
    def fecha_creacion(self) -> datetime:
        """Obtiene la fecha de creación."""
        return self._fecha_creacion
    #metodos

    def agregar_tarea(self, tarea: Tarea) -> None:
    
        if not isinstance(tarea, Tarea):
             raise ValueError(
            "Solo se pueden agregar objetos de tipo Tarea."
        )

        self._tareas.append(tarea)

    def obtener_tareas_pendientes(self) -> List[Tarea]:
        """Retorna tareas que no están completadas."""
        return [
            tarea
            for tarea in self._tareas
            if tarea.estado != EstadoTarea.COMPLETADA
        ]

    def obtener_tareas_por_prioridad(
        self, prioridad: PrioridadTarea
    ) -> List[Tarea]:
        """Retorna tareas filtradas por prioridad."""
        return [
            tarea
            for tarea in self._tareas
            if tarea.prioridad == prioridad
        ]

    def __str__(self) -> str:
        """Representación amigable del proyecto."""
        return self._nombre