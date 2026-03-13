Feature: Gestión de tareas
  Como miembro del equipo
  Quiero gestionar las tareas de un proyecto
  Para llevar el control del trabajo

  Background:
    Given que el sistema está inicializado

  Scenario: Crear una tarea válida
    When creo una tarea con titulo "Hacer informe" y prioridad "ALTA"
    Then la tarea debe existir con titulo "Hacer informe"
    And el estado de la tarea debe ser "pendiente"

  Scenario Outline: Crear tarea con título inválido
    When intento crear una tarea con titulo "<titulo>" y prioridad "MEDIA"
    Then debe lanzarse un error de validación en la tarea

    Examples:
      | titulo |
      | ab     |
      |        |
  Scenario: Completar una tarea registra la fecha
    Given que existe una tarea con titulo "Revisar codigo" y prioridad "BAJA"
    When completo la tarea "Revisar codigo"
    Then el estado de la tarea debe ser "completada"
    And la fecha de completado no debe ser nula

  Scenario: No se puede iniciar una tarea ya completada
    Given que existe una tarea con titulo "Tarea vieja" y prioridad "MEDIA"
    When completo la tarea "Tarea vieja"
    Then intentar iniciar la tarea "Tarea vieja" debe lanzar un error