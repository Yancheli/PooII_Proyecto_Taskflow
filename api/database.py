
# Almacén en memoria compartido entre todas las rutas. Archivo propio para mas limpieza

from fastapi import HTTPException

# Datos en memoria
usuarios: list[dict] = []
proyectos: list[dict] = []


# Funciones de búsqueda

def buscar_usuario(usuario_id: int) -> dict:
    """Retorna el usuario con ese id o lanza 404."""
    for u in usuarios:
        if u["id"] == usuario_id:
            return u
    raise HTTPException(status_code=404, detail="Usuario no encontrado")


def buscar_proyecto(proyecto_id: int) -> dict:
    """Retorna el proyecto con ese id o lanza 404."""
    for p in proyectos:
        if p["id"] == proyecto_id:
            return p
    raise HTTPException(status_code=404, detail="Proyecto no encontrado")


def buscar_tarea(tarea_id: int) -> tuple[dict, dict]:
    """Retorna (proyecto, tarea) para el tarea_id dado o lanza 404."""
    for p in proyectos:
        for t in p.get("tareas", []):
            if t["id"] == tarea_id:
                return p, t
    raise HTTPException(status_code=404, detail="Tarea no encontrada")