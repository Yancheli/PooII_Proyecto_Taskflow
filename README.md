# TaskFlow
Proyecto de: Luisa Builes Roldán, Jessica Treviño y Yancelly Estefannia Molina

Sistema básico de gestión de proyectos desarrollado en Python utilizando Programación Orientada a Objetos.

## Estructura del Proyecto
src/
└── domain/
├── enums.py
├── usuario.py
├── tarea.py
└── proyecto.py


## Características

- Gestión de usuarios
- Creación de proyectos
- Creación y gestión de tareas
- Manejo de prioridades y estados con Enum
- Validaciones con ValueError
- Encapsulamiento con @property
- Uso de type hints

## Cómo ejecutar

Desde la raíz del proyecto:
python test_dominio.py

en la carpeta de dominio hay una linea de codigo comentada para validar errores

## Requisitos

- Python 3.10+

## Dependencias
Para hacer los test se utilizaron dependencias tales como:
- pytest: Sirve para hacer pruebas automáticas al código en Python y comprobar que las funciones y programas funcionan correctamente. 

- pytest-cov: Sirve para ver qué partes del código fueron probadas cuando ejecutas las pruebas. 

- behave: Sirve para probar el programa usando escenarios escritos en lenguaje simple (archivos .feature) para verificar que el sistema se comporta como se espera.

## Comandos para los test
Primero se ejecuta en la terminal "pytest" y despues "pytest --cov=src --cov-report=html --cov-report=term"
