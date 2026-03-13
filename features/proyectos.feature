Feature: Gestión de proyectos
  Como líder de equipo
  Quiero crear y administrar proyectos
  Para organizar las tareas del equipo que manejo

 Background:
    Given que existe un usuario con username "lider01" y email "lider@gmail.com"

  Scenario: Crear un proyecto válido
    When creo un proyecto con nombre "TFApp" y lider "lider01"
    Then el proyecto debe existir con nombre "TFApp"
    And el proyecto debe tener 0 tareas

  Scenario: Crear proyecto con nombre muy corto
    When intento crear un proyecto con nombre "ab" y lider "lider01"
    Then debe lanzarse un error de validación en el proyecto

  Scenario: Agregar tareas y filtrar pendientes
    Given que existe un proyecto con nombre "Mi Proyecto" y lider "lider01"
    And agrego una tarea con titulo "Tarea uno" y prioridad "ALTA" al proyecto
    And agrego una tarea con titulo "Tarea dos" y prioridad "MEDIA" al proyecto
    When completo la tarea "Tarea uno"
    Then las tareas pendientes del proyecto deben ser 1

  Scenario Outline: Filtrar tareas por prioridad
    Given que existe un proyecto con nombre "Proyecto Filtros" y lider "lider01"
    And agrego una tarea con titulo "Tarea alta" y prioridad "ALTA" al proyecto
    And agrego una tarea con titulo "Tarea baja" y prioridad "BAJA" al proyecto
    When filtro las tareas por prioridad "<prioridad>"
    Then debo obtener <cantidad> tarea(s)

    Examples:
      | prioridad | cantidad |
      | ALTA      | 1        |
      | BAJA      | 1        |
      | MEDIA     | 0        |