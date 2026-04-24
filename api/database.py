'''
La base de datos en memoria se reemplaza con una base de datos real, 
ya no funciona a base de listas como antes
'''

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi import Depends, HTTPException
from database.modelsalchemy import Base

#Conexión 
DATABASE_URL = (
    "postgresql+psycopg2://neondb_owner:npg_S2PGonkLJcq1"
    "@ep-quiet-hall-any02af2-pooler.c-6.us-east-1.aws.neon.tech"
    "/neondb?sslmode=require"
 )

# Engine de sesiones

engine = create_engine(DATABASE_URL)
 
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,   
    autoflush=False,    # No enviar cambios a la BD antes del commit
)

# fast api
def get_db():
    """
    Genera una sesión de BD  y la cierra al terminar.
    Se usa con Depends(get_db) en los endpoints
    """
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Búsquedas y acciones

# Importamos los modelos aquí para no repetir la lógica en cada ruta.
from database.modelsalchemy import Usuario, Proyecto, Tarea, Membresia
 
 
def buscar_usuario(usuario_id: int, db: Session) -> Usuario:
    usuario = db.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario
 
 
def buscar_proyecto(proyecto_id: int, db: Session) -> Proyecto:
    proyecto = db.get(Proyecto, proyecto_id)
    if not proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    return proyecto
 
 
def buscar_tarea(tarea_id: int, db: Session) -> Tarea:
    tarea = db.get(Tarea, tarea_id)
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return tarea
