# registro.py
# Configura el archivo de logs donde se guardan TODOS los eventos y errores.
# Usamos el módulo estándar "logging": no hace falta ninguna base de datos.

import logging
import os

# Carpeta y archivo donde quedan los registros (se crean solos si no existen)
CARPETA_LOGS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
ARCHIVO_LOG = os.path.join(CARPETA_LOGS, "software_fj.log")


def obtener_logger():
    """
    Devuelve el logger del sistema. La primera vez lo configura para
    escribir en logs/software_fj.log con fecha, hora, nivel y mensaje.
    """
    logger = logging.getLogger("software_fj")

    # Si ya tiene un manejador configurado, lo reutilizamos (evita líneas duplicadas)
    if logger.handlers:
        return logger

    os.makedirs(CARPETA_LOGS, exist_ok=True)
    logger.setLevel(logging.INFO)

    manejador = logging.FileHandler(ARCHIVO_LOG, encoding="utf-8")
    manejador.setFormatter(logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
    logger.addHandler(manejador)
    return logger
