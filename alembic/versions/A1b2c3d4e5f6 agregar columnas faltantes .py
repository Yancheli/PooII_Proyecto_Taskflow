"""agrega columnas faltantes en usuarios y tareas

Revision ID: a1b2c3d4e5f6
Revises: 73b66aa07473
Create Date: 2026-04-24 10:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, Sequence[str], None] = "73b66aa07473"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # En usuarios: fecha_registro
    op.add_column(
        "usuarios",
        sa.Column(
            "fecha_registro",
            sa.DateTime(),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
    )

    # En tareas: prioridad
    prioridad_enum = sa.Enum(
        "ALTA", "MEDIA", "BAJA",
        name="prioridad_tarea",
    )
    prioridad_enum.create(op.get_bind(), checkfirst=True)

    op.add_column(
        "tareas",
        sa.Column(
            "prioridad",
            sa.Enum("ALTA", "MEDIA", "BAJA", name="prioridad_tarea"),
            nullable=False,
            server_default="MEDIA",
        ),
    )

    # En tareas: fecha_creacion
    op.add_column(
        "tareas",
        sa.Column(
            "fecha_creacion",
            sa.DateTime(),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
    )

    # En tareas: fecha_completado
    op.add_column(
        "tareas",
        sa.Column(
            "fecha_completado",
            sa.DateTime(),
            nullable=True,
        ),
    )


def downgrade() -> None:
    op.drop_column("tareas", "fecha_completado")
    op.drop_column("tareas", "fecha_creacion")
    op.drop_column("tareas", "prioridad")

    prioridad_enum = sa.Enum(name="prioridad_tarea")
    prioridad_enum.drop(op.get_bind(), checkfirst=True)

    op.drop_column("usuarios", "fecha_registro")