from behave import given, when, then
from src.domain.proyecto import Proyecto
from src.domain.tarea import Tarea
from src.domain.enums import PrioridadTarea

@given('que existe un proyecto con nombre "{nombre}" y lider "{username}"')
def step_proyecto_existe(context, nombre, username):
    if not hasattr(context, "proyectos"):
        context.proyectos = {}
    lider = context.usuarios[username]
    context.proyectos[nombre] = Proyecto(nombre=nombre, lider=lider)
    context.proyecto_actual = context.proyectos[nombre]

@given('agrego una tarea con titulo "{titulo}" y prioridad "{prioridad}" al proyecto')
def step_agregar_tarea_al_proyecto(context, titulo, prioridad):
    prioridad_enum = PrioridadTarea[prioridad]
    tarea = Tarea(titulo=titulo, prioridad=prioridad_enum)
    if not hasattr(context, "tareas"):
        context.tareas = {}
    context.tareas[titulo] = tarea
    context.proyecto_actual.agregar_tarea(tarea)

@when('creo un proyecto con nombre "{nombre}" y lider "{username}"')
def step_crear_proyecto(context, nombre, username):
    if not hasattr(context, "proyectos"):
        context.proyectos = {}
    context.error = None
    lider = context.usuarios[username]
    proyecto = Proyecto(nombre=nombre, lider=lider)
    context.proyectos[nombre] = proyecto
    context.proyecto_actual = proyecto

@when('intento crear un proyecto con nombre "{nombre}" y lider "{username}"')
def step_crear_proyecto_invalido(context, nombre, username):
    context.error = None
    try:
        lider = context.usuarios[username]
        Proyecto(nombre=nombre, lider=lider)
    except ValueError as e:
        context.error = e

@when('completo la tarea "{titulo}"')
def step_completar_tarea_proyecto(context, titulo):
    context.tareas[titulo].completar()

@when('filtro las tareas por prioridad "{prioridad}"')
def step_filtrar_por_prioridad(context, prioridad):
    prioridad_enum = PrioridadTarea[prioridad]
    context.tareas_filtradas = context.proyecto_actual.obtener_tareas_por_prioridad(prioridad_enum)

@then('el proyecto debe existir con nombre "{nombre}"')
def step_proyecto_existe_check(context, nombre):
    assert nombre in context.proyectos

@then("el proyecto debe tener 0 tareas")
def step_proyecto_sin_tareas(context):
    assert len(context.proyecto_actual.tareas) == 0

@then("debe lanzarse un error de validación en el proyecto")
def step_error_proyecto(context):
    assert context.error is not None
    assert isinstance(context.error, ValueError)

@then("las tareas pendientes del proyecto deben ser {cantidad:d}")
def step_tareas_pendientes(context, cantidad):
    pendientes = context.proyecto_actual.obtener_tareas_pendientes()
    assert len(pendientes) == cantidad

@then("debo obtener {cantidad:d} tarea(s)")
def step_tareas_filtradas_cantidad(context, cantidad):
    assert len(context.tareas_filtradas) == cantidad