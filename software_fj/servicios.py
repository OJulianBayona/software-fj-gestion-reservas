# servicios.py
# Clase abstracta Servicio y los tres servicios especializados de Software FJ:
# reserva de salas, alquiler de equipos y asesorías especializadas.

from abc import abstractmethod

from .entidad import Entidad
from .excepciones import CalculoInconsistenteError, DatosInvalidosError, ParametroFaltanteError

IVA = 0.19  # impuesto por defecto en Colombia


class Servicio(Entidad):
    """Servicio general. Cada servicio concreto define cómo se cobra y qué duración acepta."""

    def __init__(self, nombre, tarifa, disponible=True):
        super().__init__("SRV")
        if not nombre or str(nombre).strip() == "":
            raise ParametroFaltanteError("nombre del servicio")
        if not isinstance(tarifa, (int, float)) or tarifa <= 0:
            raise DatosInvalidosError(f"La tarifa debe ser un número mayor que 0 (recibido: {tarifa!r})")
        self._nombre = str(nombre).strip()
        self._tarifa = float(tarifa)
        self._disponible = disponible

    @property
    def nombre(self):
        return self._nombre

    @property
    def disponible(self):
        return self._disponible

    def cambiar_disponibilidad(self, disponible):
        self._disponible = bool(disponible)

    # ---------- métodos que cada servicio sobrescribe (polimorfismo) ----------
    @abstractmethod
    def calcular_costo_base(self, duracion):
        """Costo sin impuestos ni descuentos, según las reglas de cada servicio."""

    @abstractmethod
    def validar_parametros(self, duracion):
        """Revisa que la duración tenga sentido para este servicio."""

    @abstractmethod
    def unidad(self):
        """Unidad en la que se mide la duración (horas, días...)."""

    # ---------- método "sobrecargado" ----------
    def calcular_costo(self, duracion, impuesto=None, descuento=None):
        """
        SOBRECARGA SIMULADA: Python no permite dos métodos con el mismo nombre,
        así que se usan parámetros opcionales. Se puede llamar de tres formas:
            calcular_costo(duracion)                      -> costo base
            calcular_costo(duracion, impuesto)            -> con impuesto
            calcular_costo(duracion, impuesto, descuento) -> con impuesto y descuento
        """
        self.validar_parametros(duracion)
        costo = self.calcular_costo_base(duracion)

        if descuento is not None:
            if not 0 <= descuento < 1:
                raise CalculoInconsistenteError(f"Descuento fuera de rango: {descuento} (debe estar entre 0 y 0.99)")
            costo = costo * (1 - descuento)

        if impuesto is not None:
            if not 0 <= impuesto <= 0.5:
                raise CalculoInconsistenteError(f"Impuesto fuera de rango: {impuesto}")
            costo = costo * (1 + impuesto)

        if costo <= 0:
            raise CalculoInconsistenteError(f"El costo calculado no es válido: {costo}")
        return round(costo, 2)

    def validar(self):
        if self._tarifa <= 0:
            raise DatosInvalidosError("Tarifa inválida")
        return True

    def _validar_duracion(self, duracion, minimo, maximo):
        """Validación común que reutilizan todos los servicios."""
        if duracion is None:
            raise ParametroFaltanteError("duracion")
        if not isinstance(duracion, (int, float)) or not minimo <= duracion <= maximo:
            raise DatosInvalidosError(
                f"Duración inválida para '{self.nombre}': {duracion!r} (entre {minimo} y {maximo} {self.unidad()})")


class ReservaSala(Servicio):
    """Reserva de salas por horas. Las salas grandes (más de 20 personas) tienen recargo."""

    def __init__(self, nombre, tarifa_hora, capacidad, disponible=True):
        super().__init__(nombre, tarifa_hora, disponible)
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise DatosInvalidosError(f"Capacidad inválida: {capacidad!r}")
        self._capacidad = capacidad
        self._asignar_id()

    def unidad(self):
        return "horas"

    def validar_parametros(self, duracion):
        self._validar_duracion(duracion, 1, 12)

    def calcular_costo_base(self, duracion):
        recargo = 1.10 if self._capacidad > 20 else 1.0
        return self._tarifa * duracion * recargo

    def describir(self):
        return f"{self.id} | Sala '{self.nombre}' para {self._capacidad} personas | ${self._tarifa:,.0f}/hora"


class AlquilerEquipo(Servicio):
    """Alquiler de equipos por días, con un depósito fijo que se suma al total."""

    def __init__(self, nombre, tarifa_dia, deposito=0, disponible=True):
        super().__init__(nombre, tarifa_dia, disponible)
        if not isinstance(deposito, (int, float)) or deposito < 0:
            raise DatosInvalidosError(f"Depósito inválido: {deposito!r}")
        self._deposito = float(deposito)
        self._asignar_id()

    def unidad(self):
        return "días"

    def validar_parametros(self, duracion):
        self._validar_duracion(duracion, 1, 30)

    def calcular_costo_base(self, duracion):
        return self._tarifa * duracion + self._deposito

    def describir(self):
        return f"{self.id} | Equipo '{self.nombre}' | ${self._tarifa:,.0f}/día + depósito ${self._deposito:,.0f}"


class Asesoria(Servicio):
    """Asesoría especializada por horas; el nivel senior cuesta 50 % más."""

    NIVELES = {"junior": 1.0, "senior": 1.5}

    def __init__(self, nombre, tarifa_hora, especialidad, nivel="junior", disponible=True):
        super().__init__(nombre, tarifa_hora, disponible)
        if not especialidad:
            raise ParametroFaltanteError("especialidad")
        if nivel not in self.NIVELES:
            raise DatosInvalidosError(f"Nivel inválido: '{nivel}' (use junior o senior)")
        self._especialidad = especialidad
        self._nivel = nivel
        self._asignar_id()

    def unidad(self):
        return "horas"

    def validar_parametros(self, duracion):
        self._validar_duracion(duracion, 1, 8)

    def calcular_costo_base(self, duracion):
        return self._tarifa * duracion * self.NIVELES[self._nivel]

    def describir(self):
        return (f"{self.id} | Asesoría '{self.nombre}' en {self._especialidad} "
                f"({self._nivel}) | ${self._tarifa:,.0f}/hora")
