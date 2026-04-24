from enum import Enum

class PrioridadTarea(Enum):
    ALTA = "ALTA"
    MEDIA = "MEDIA"
    BAJA = "BAJA"

class EstadoTarea(Enum):
    PENDIENTE = "pendiente"
    EN_PROGRESO = "en_progreso"
    COMPLETADA = "completada"

class RolUsuario(Enum):
    LIDER = "lider"
    MIEMBRO = "miembro"