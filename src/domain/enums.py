from enum import Enum

class PrioridadTarea(Enum):
    ALTA = 1
    MEDIA = 2
    BAJA = 3

class EstadoTarea(Enum):
    PENDIENTE = "pendiente"
    EN_PROGRESO = "en_progreso"
    COMPLETADA = "completada"

class RolUsuario(Enum):
    LIDER = "lider"
    MIEMBRO = "miembro"