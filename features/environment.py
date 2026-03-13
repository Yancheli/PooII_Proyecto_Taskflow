def before_scenario(context, scenario):
    context.usuarios = {}
    context.proyectos = {}
    context.tareas = {}
    context.error = None
    context.proyecto_actual = None
    context.tarea_actual = None
    context.tareas_filtradas = []