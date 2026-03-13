Feature: Gestión de usuarios

  Como administradora del sistema
  Quiero gestionar usuarios
  Para controlar el acceso al flujo TaskFlow

  Background:
    Given que el sistema está inicializado

  Scenario: Crear un usuario válido
    When creo un usuario con username "yancelly123" y email "yancelly123@gmail.com"
    Then el usuario debe existir con username "yancelly123"
    And el usuario debe estar activo

  Scenario Outline: Crear usuario con username inválido
    When intento crear un usuario con username "<nomuser>" y email "test@test.com"
    Then debe lanzarse un error de validación

    Examples:
      | nomuser  |
      | ab        |
      |           |
      | test@testes |

  Scenario: Desactivar y reactivar un usuario
    Given que existe un usuario con username "luisa123" y email "luisa@gmail.com"
    When desactivo al usuario "luisa123"
    Then el usuario debe estar inactivo
    When activo al usuario "luisa123"
    Then el usuario debe estar activo