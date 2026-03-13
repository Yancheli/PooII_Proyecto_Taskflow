from behave import given, when, then
from src.domain.usuario import Usuario

@given("que el sistema está inicializado")
def step_sistema_inicializado(context):
    context.usuarios = {}
    context.proyectos = {}
    context.tareas = {}
    context.error = None

@given('que existe un usuario con username "{username}" y email "{email}"')
def step_usuario_existe(context, username, email):
    if not hasattr(context, "usuarios"):
        context.usuarios = {}
    context.usuarios[username] = Usuario(username=username, email=email)

@when('creo un usuario con username "{username}" y email "{email}"')
def step_crear_usuario(context, username, email):
    if not hasattr(context, "usuarios"):
        context.usuarios = {}
    context.error = None
    context.usuarios[username] = Usuario(username=username, email=email)

@when('intento crear un usuario con username "{username}" y email "{email}"')
def step_crear_usuario_invalido(context, username, email):
    context.error = None
    try:
        Usuario(username=username, email=email)
    except ValueError as e:
        context.error = e

@when('intento crear un usuario con username "" y email "test@test.com"')
def step_crear_usuario_vacio(context):
    context.error = None
    try:
        Usuario(username="", email="test@test.com")
    except ValueError as e:
        context.error = e

@when('desactivo al usuario "{username}"')
def step_desactivar_usuario(context, username):
    context.usuarios[username].desactivar()

@when('activo al usuario "{username}"')
def step_activar_usuario(context, username):
    context.usuarios[username].activar()

@then('el usuario debe existir con username "{username}"')
def step_usuario_existe_check(context, username):
    assert username in context.usuarios

@then("el usuario debe estar activo")
def step_usuario_activo(context):
    usuario = list(context.usuarios.values())[-1]
    assert usuario.activo is True

@then("el usuario debe estar inactivo")
def step_usuario_inactivo(context):
    usuario = list(context.usuarios.values())[-1]
    assert usuario.activo is False

@then("debe lanzarse un error de validación")
def step_error_validacion(context):
    assert context.error is not None
    assert isinstance(context.error, ValueError)