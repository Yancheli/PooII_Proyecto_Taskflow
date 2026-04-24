'''enum nativo de python y sqlalchemy con modelos modernos (2.0)'''
from datetime import datetime
from typing import Optional, List
 
from sqlalchemy import String, Boolean, ForeignKey, DateTime, Enum as SAEnum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
 
from src.domain.enums import EstadoTarea, RolUsuario, PrioridadTarea

#base

class Base(DeclarativeBase):
    """Clase base de la que heredan todos los modelos."""


#Modelo de Usuario

class Usuario(Base):
    """Representa un usuario registrado en el sistema.

    Atributos:
        id: Clave primaria autoincremental
        username: Nombre de usuario único (máx. 50 caracteres)
        email: Correo electrónico único (máx. 100 caracteres, debe tener @)
        hashed_password: Contraseña oculta
        activo: Indica si la cuenta está activa
        rol: Rol del usuario — LIDER o MIEMBRO
        proyectos_liderados: Proyectos creados por este usuario (solo LIDER)
        membresías: Proyectos a los que pertenece como MIEMBRO
        fecha_registro: datetime automático para cuando se crea el usuario
    """

    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    fecha_registro: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )


    # Roles del usuario
    rol: Mapped[RolUsuario] = mapped_column(
        SAEnum(RolUsuario, values_callable=lambda e: [i.value for i in e]),
        default=RolUsuario.MIEMBRO,
        nullable=False
    )

    # Proyectos asociados SOLO a lider
    proyectos_liderados: Mapped[List["Proyecto"]] = relationship(
        "Proyecto",
        back_populates="lider"
    )

    # Proyectos donde pertenece
    membresias: Mapped[List["Membresia"]] = relationship(
        "Membresia",
        back_populates="usuario"
    )

    # Rol lider
    def es_lider(self) -> bool:
        """Retorna True si el usuario tiene rol de LIDER."""
        return self.rol == RolUsuario.LIDER

    def __repr__(self) -> str:
        return (
            f"Usuario(id={self.id!r}, username={self.username!r}, "
            f"email={self.email!r}, rol={self.rol!r}, activo={self.activo!r})"
        )


# Modelo de proyecto

class Proyecto(Base):
    """Representa un proyecto que agrupa tareas y pertenece a un líder

    Attributes:
        id: Clave primaria autoincremental
        nombre: Nombre del proyecto (máx. 100 caracteres)
        descripcion: Descripción opcional
        lider_id: FK hacia el usuario LIDER 
        lider: Relación inversa hacia Usuario
        tareas: Relación uno-a-muchos hacia Tarea
        membresias: participantes asignados al proyecto
    """

    __tablename__ = "proyectos"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)

    # FK hacia el líder 
    lider_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), nullable=False)

    # Relaciones
    lider: Mapped["Usuario"] = relationship(
        "Usuario",
        back_populates="proyectos_liderados"
    )

    tareas: Mapped[List["Tarea"]] = relationship(
        "Tarea",
        back_populates="proyecto"
    )

    # tabla intermedia de participantes
    membresias: Mapped[List["Membresia"]] = relationship(
        "Membresia",
        back_populates="proyecto"
    )

    def __repr__(self) -> str:
        return (
            f"Proyecto(id={self.id!r}, nombre={self.nombre!r}, "
            f"lider_id={self.lider_id!r})"
        )
class Membresia(Base):
    """Tabla intermedia que representa la pertenencia de un MIEMBRO a un Proyecto.

    Un líder asigna y quita miembros, aquí se muestra esa información

    Atributos:
        id: Clave primaria autoincremental.
        usuario_id: FK hacia el usuario miembro
        proyecto_id: FK hacia el proyecto
        usuario: Relación hacia Usuario
        proyecto: Relación hacia Proyecto
    """

    __tablename__ = "membresias"

    id: Mapped[int] = mapped_column(primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), nullable=False)
    proyecto_id: Mapped[int] = mapped_column(ForeignKey("proyectos.id"), nullable=False)

    usuario: Mapped["Usuario"] = relationship(
        "Usuario",
        back_populates="membresias"
    )
    proyecto: Mapped["Proyecto"] = relationship(
        "Proyecto",
        back_populates="membresias"
    )

    def __repr__(self) -> str:
        return (
            f"Membresia(id={self.id!r}, usuario_id={self.usuario_id!r}, "
            f"proyecto_id={self.proyecto_id!r})"
        )




# Modelo Tarea

class Tarea(Base):
    """Representa una tarea dentro de un proyecto
    Tanto líderes como miembros pueden crear y eliminar tareas

    Attributes:
        id: Clave primaria autoincremental
        titulo: Título de la tarea (máx. 100 caracteres)
        descripcion: Descripción opcional
        estado: Estado actual (enum)
        proyecto_id: FK hacia el proyecto
        creador_id: FK hacia el usuario que creó la tarea (líder o miembro) por id
        proyecto: Relación inversa hacia Proyecto
        creador: Relación hacia Usuario (quien creó la tarea)
        prioridad: basada en enums de urgencia de la tarea (alta,media,baja)
        fecha_creacion: datetime automatico para cuando se crea la tarea
        fecha_completado: fecha de finalización de la tarea
    """

    __tablename__ = "tareas"

    id: Mapped[int] = mapped_column(primary_key=True)
    titulo: Mapped[str] = mapped_column(String(100), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)


    estado: Mapped[EstadoTarea] = mapped_column(
        SAEnum(EstadoTarea, values_callable=lambda e: [i.value for i in e]),
        default=EstadoTarea.PENDIENTE,
        nullable=False
    )

    prioridad: Mapped[PrioridadTarea] = mapped_column(
        SAEnum(PrioridadTarea, values_callable=lambda e: [i.value for i in e]),
        default=PrioridadTarea.MEDIA,
        nullable=False,
    )

    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    fecha_completado: Mapped[Optional[datetime]] = mapped_column(
        DateTime, nullable=True
    )

    proyecto_id: Mapped[int] = mapped_column(ForeignKey("proyectos.id"), nullable=False)

    # Autoría
    creador_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), nullable=False)

    # Relaciones
    proyecto: Mapped["Proyecto"] = relationship(
        "Proyecto",
        back_populates="tareas"
    )
    creador: Mapped["Usuario"] = relationship(
        "Usuario",
        foreign_keys=[creador_id]
    )

    def __repr__(self) -> str:
        return (
            f"Tarea(id={self.id!r}, titulo={self.titulo!r}, "
            f"estado={self.estado!r}, proyecto_id={self.proyecto_id!r}, "
            f"creador_id={self.creador_id!r})"
        )