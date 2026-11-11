# entidad.py
# Clase abstracta que representa cualquier entidad general del sistema
# (clientes, servicios y reservas). Define lo que todas comparten.

from abc import ABC, abstractmethod


class Entidad(ABC):
    """Entidad general con un identificador único y métodos obligatorios."""

    # Contador por prefijo para generar identificadores: CLI-001, SRV-001, RES-001...
    _contadores = {}

    def __init__(self, prefijo):
        # El id se asigna al FINAL de la construcción (con _asignar_id) para que
        # un objeto que falla en sus validaciones no "gaste" un número
        self._prefijo = prefijo
        self._id = None

    def _asignar_id(self):
        """Se llama como última línea del __init__ de cada clase concreta."""
        numero = Entidad._contadores.get(self._prefijo, 0) + 1
        Entidad._contadores[self._prefijo] = numero
        # Atributo protegido: solo se lee con la propiedad "id"
        self._id = f"{self._prefijo}-{numero:03d}"

    @property
    def id(self):
        """Identificador único de la entidad (solo lectura)."""
        return self._id

    @abstractmethod
    def describir(self):
        """Cada entidad debe saber describirse en texto."""

    @abstractmethod
    def validar(self):
        """Cada entidad debe validar sus propios datos y lanzar una excepción si algo falla."""

    def __str__(self):
        return self.describir()
