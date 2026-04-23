# TaskFlow
Proyecto de: Luisa Builes Roldán, Jessica Treviño y Yancelly Estefannia Molina

Sistema básico de gestión de proyectos desarrollado en Python utilizando Programación Orientada a Objetos.

## Estructura del Proyecto
src/                    
├── __init__.py
└── domain/
    ├── __init__.py
    ├── enums.py
    ├── usuario.py
    ├── proyecto.py
    └── tarea.py

tests/                      
├── __init__.py
├── conftest.py           
├── test_usuario.py       
├── test_proyecto.py      
├── test_tarea.py         
└── test_enums.py         

features/                   
├── environment.py        
├── steps/
│   ├── __init__.py
│   ├── usuarios_steps.py
│   ├── proyectos_steps.py
│   └── tareas_steps.py
├── usuarios.feature      
├── proyectos.feature     
└── tareas.feature        
pytest.ini                 
.coveragerc                # (fuera de la rama base)
requirements.txt          
README.md         

## Requisitos
- Python 3.10+

## Características
- Gestión de usuarios
- Creación de proyectos
- Creación y gestión de tareas
- Manejo de prioridades y estados con Enum
- Validaciones con ValueError
- Encapsulamiento con @property
- Uso de type hints
- test con pytest y por medio de behave

## Dependencias
Para hacer los test se utilizaron dependencias tales como:
- pytest: Sirve para hacer pruebas automáticas al código en Python y comprobar que las funciones y programas funcionan correctamente. 

- pytest-cov: Sirve para ver qué partes del código fueron probadas cuando ejecutas las pruebas.

- behave: Sirve para probar el programa usando escenarios escritos en lenguaje simple (archivos .feature) para verificar que el sistema se comporta como se espera.

- FastAPI: Framework moderno de Python para crear APIs rápidas y eficientes, basado en tipado estático. Facilita validación automática y documentación interactiva.

- Uvicorn: Servidor ASGI ligero y rápido que ejecuta aplicaciones como FastAPI. Maneja las peticiones HTTP de forma asíncrona.

- Pydantic[email]: Librería para validación de datos usando tipos de Python; la opción [email] añade validación específica para correos electrónicos.

## Comandos para los test
Primero se ejecuta en la terminal "pytest" y despues "pytest --cov=src --cov-report=html --cov-report=term"
Para hacer uso de las pruebas con behave solo debe escribirse el comando "behave" en la terminal del proyecto

((Es recomendable no ejecutar ambos tipos de test al mismo tiempo porque la dimensión de la información a cargar puede ser algo grande y afectar el tiempo de respuesta))

## Comando para ejecutar la aplicacion
uvicorn api.main:app --reload



