# Software FJ — Sistema Integral de Gestión de Clientes, Servicios y Reservas

Curso **Programación (213023) — UNAD** · Fase 4: Prácticas simuladas (trabajo colaborativo).

Sistema orientado a objetos en Python, **sin base de datos**: toda la información vive en
listas de objetos y solo se usa un archivo de texto para el registro (log) de eventos y errores.

## Cómo ejecutarlo

Requiere Python 3.10 o superior. No necesita librerías externas.

```bash
python main.py
```

El programa ejecuta 19 operaciones (válidas e inválidas), muestra el resultado de cada una y
al final imprime el resumen de clientes, servicios y reservas. Los eventos quedan en
`logs/software_fj.log`.

## Estructura

```
software_fj/
├── main.py                  # Simulación de 19 operaciones (punto de entrada)
├── README.md
├── .gitignore
├── logs/                    # Se crea al ejecutar: software_fj.log
└── software_fj/             # Paquete con el modelo del sistema
    ├── __init__.py
    ├── excepciones.py       # Excepciones personalizadas (jerarquía SoftwareFJError)
    ├── registro.py          # Configuración del archivo de logs
    ├── entidad.py           # Clase abstracta Entidad (id único, describir, validar)
    ├── cliente.py           # Cliente con encapsulación y validaciones
    ├── servicios.py         # Servicio abstracto + ReservaSala, AlquilerEquipo, Asesoria
    ├── reserva.py           # Reserva: confirmar, cancelar, procesar
    └── sistema.py           # Gestor central con las listas internas
```

## Requisitos de la guía y dónde se cumplen

| Requisito | Dónde |
|---|---|
| Clase abstracta general | `entidad.py` → `Entidad(ABC)` |
| Cliente con validaciones y encapsulación | `cliente.py` → propiedades con atributos privados |
| Servicio abstracto + 3 servicios especializados | `servicios.py` |
| Polimorfismo (costo, descripción, validación) | `calcular_costo_base`, `describir`, `validar_parametros` |
| Métodos sobrecargados | `Servicio.calcular_costo(duracion, impuesto=None, descuento=None)` |
| Reserva con confirmar / cancelar / procesar | `reserva.py` |
| Excepciones personalizadas | `excepciones.py` |
| try/except, try/except/else, try/except/finally | `sistema.py`, `reserva.procesar`, `main.ejecutar_operacion` |
| Encadenamiento de excepciones (`raise ... from`) | `Reserva.validar`, `Reserva.procesar`, `Sistema.crear_servicio` |
| Registro de eventos y errores en archivo | `registro.py` → `logs/software_fj.log` |
| Más de 10 operaciones simuladas sin detener el programa | `main.py` |

## Reparto sugerido para el equipo (5 integrantes)

Cada integrante documenta y sube su parte con commits propios:

| Integrante | Módulos | Qué documenta |
|---|---|---|
| 1 | `excepciones.py`, `registro.py` | Jerarquía de errores y el log |
| 2 | `entidad.py`, `cliente.py` | Abstracción, encapsulación y validaciones |
| 3 | `servicios.py` | Herencia, polimorfismo y sobrecarga |
| 4 | `reserva.py`, `sistema.py` | Estados de la reserva y manejo de excepciones |
| 5 | `main.py`, `README.md` | Simulación de operaciones y pruebas |

## Flujo de trabajo en GitHub

1. Clonar el repositorio: `git clone <url-del-repo>`
2. Crear una rama propia: `git checkout -b integrante-N`
3. Hacer cambios y commits pequeños con mensajes claros.
4. Subir la rama (`git push origin integrante-N`) y abrir un Pull Request hacia `main`.
5. Antes de unir, ejecutar `python main.py` y verificar que termina sin interrupciones.
