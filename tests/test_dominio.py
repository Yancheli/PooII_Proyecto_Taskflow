from src.domain.usuario import Usuario
from src.domain.tarea import Tarea
from src.domain.enums import PrioridadTarea
from src.domain.proyecto import Proyecto

usuario = Usuario("jessica123", "jessica@gmail.com")
print(usuario)
print(repr(usuario))
print(usuario.email)
print(usuario.activo)
print(usuario.fecha_registro)


tarea = Tarea("Hacer informe", PrioridadTarea.ALTA)

print(tarea)

tarea.iniciar()
print(tarea)

tarea.completar()
print(tarea)
print(tarea.fecha_completado)


proyecto = Proyecto("Sistema TaskFlow", usuario)

tarea1 = Tarea("Backend", PrioridadTarea.ALTA)
tarea2 = Tarea("Frontend", PrioridadTarea.MEDIA)
tarea3 = Tarea("Documentación", PrioridadTarea.BAJA)

proyecto.agregar_tarea(tarea1)
proyecto.agregar_tarea(tarea2)
proyecto.agregar_tarea(tarea3)

tarea1.completar()

print("\nTareas pendientes:")
for t in proyecto.obtener_tareas_pendientes():
    print(t)

print("\nTareas prioridad MEDIA:")
for t in proyecto.obtener_tareas_por_prioridad(PrioridadTarea.MEDIA):
    print(t)

#python test_dominio.py

# Esto debería fallar
#proyecto.agregar_tarea("no soy tarea")