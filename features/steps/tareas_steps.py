from behave import given, when, then
from src.domain.tarea import Tarea
from src.domain.enums import PrioridadTarea

@given('que existe una tarea con titulo "{titulo}" y prioridad "{prioridad}"')
def step_tarea_existe(context, titulo, prioridad):
    if not hasattr(context, "tareas"):
        context.tareas = {}
    prioridad_enum = PrioridadTarea[prioridad]
    context.tareas[titulo] = Tarea(titulo=titulo, prioridad=prioridad_enum)
    context.tarea_actual = context.tareas[titulo]

@when('creo una tarea con titulo "{titulo}" y prioridad "{prioridad}"')
def step_crear_tarea(context, titulo, prioridad):
    if not hasattr(context, "tareas"):
        context.tareas = {}
    context.error = None
    prioridad_enum = PrioridadTarea[prioridad]
    tarea = Tarea(titulo=titulo, prioridad=prioridad_enum)
    context.tareas[titulo] = tarea
    context.tarea_actual = tarea

@when('intento crear una tarea con titulo "{titulo}" y prioridad "{prioridad}"')
def step_crear_tarea_invalida(context, titulo, prioridad):
    context.error = None
    try:
        prioridad_enum = PrioridadTarea[prioridad]
        Tarea(titulo=titulo, prioridad=prioridad_enum)
    except ValueError as e:
        context.error = e

@when('intento crear una tarea con titulo "" y prioridad "MEDIA"')
def step_crear_tarea_vacia(context):
    context.error = None
    try:
        Tarea(titulo="", prioridad=PrioridadTarea.MEDIA)
    except ValueError as e:
        context.error = e

@when('intentar iniciar la tarea "{titulo}" debe lanzar un error')
def step_iniciar_tarea_completada_inline(context, titulo):
    try:
        context.tareas[titulo].iniciar()
        context.error = None
    except ValueError as e:
        context.error = e

@then('la tarea debe existir con titulo "{titulo}"')
def step_tarea_existe_check(context, titulo):
    assert titulo in context.tareas

@then('el estado de la tarea debe ser "{estado}"')
def step_estado_tarea(context, estado):
    assert context.tarea_actual.estado.value == estado

@then("la fecha de completado no debe ser nula")
def step_fecha_completado(context):
    assert context.tarea_actual.fecha_completado is not None

@then("debe lanzarse un error de validación en la tarea")
def step_error_tarea(context):
    assert context.error is not None
    assert isinstance(context.error, ValueError)

@then('intentar iniciar la tarea "{titulo}" debe lanzar un error')
def step_iniciar_completada_check(context, titulo):
    try:
        context.tareas[titulo].iniciar()
        assert False, "Se esperaba un ValueError"
    except ValueError:
        pass