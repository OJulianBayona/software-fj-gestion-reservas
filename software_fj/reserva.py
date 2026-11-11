# reserva.py
# Clase Reserva: une un cliente, un servicio, una duración y un estado.
# Implementa confirmar, cancelar y procesar con manejo de excepciones.

from .entidad import Entidad
from .excepciones import (CalculoInconsistenteError, DatosInvalidosError, OperacionNoPermitidaError,
                          ParametroFaltanteError, ReservaInvalidaError, ServicioNoDisponibleError)
from .registro import obtener_logger

log = obtener_logger()


class Reserva(Entidad):
    """Reserva de un servicio por parte de un cliente."""

    PENDIENTE = "PENDIENTE"
    CONFIRMADA = "CONFIRMADA"
    CANCELADA = "CANCELADA"
    PROCESADA = "PROCESADA"

    def __init__(self, cliente, servicio, duracion):
        super().__init__("RES")
        if cliente is None or servicio is None:
            raise ReservaInvalidaError("Una reserva necesita un cliente y un servicio")
        self._cliente = cliente
        self._servicio = servicio
        self._duracion = duracion
        self._estado = Reserva.PENDIENTE
        self._total = None
        self.validar()
        self._asignar_id()  # la reserva solo recibe número si es válida

    @property
    def estado(self):
        return self._estado

    @property
    def total(self):
        return self._total

    def validar(self):
        """Valida la duración según las reglas del servicio (polimorfismo)."""
        try:
            self._servicio.validar_parametros(self._duracion)
        except (DatosInvalidosError, ParametroFaltanteError) as error:
            # ENCADENAMIENTO: se lanza un error de reserva, conservando la causa original
            raise ReservaInvalidaError(f"No se puede reservar '{self._servicio.nombre}'") from error
        return True

    def confirmar(self):
        """Confirma la reserva solo si está pendiente y el servicio está disponible."""
        if self._estado != Reserva.PENDIENTE:
            raise OperacionNoPermitidaError(f"La reserva {self.id} no se puede confirmar: está {self._estado}")
        if not self._servicio.disponible:
            raise ServicioNoDisponibleError(self._servicio.nombre)
        self._estado = Reserva.CONFIRMADA
        log.info(f"Reserva {self.id} confirmada")

    def cancelar(self):
        """Cancela la reserva; no se permite si ya fue procesada o cancelada."""
        if self._estado in (Reserva.PROCESADA, Reserva.CANCELADA):
            raise OperacionNoPermitidaError(f"La reserva {self.id} no se puede cancelar: está {self._estado}")
        self._estado = Reserva.CANCELADA
        log.info(f"Reserva {self.id} cancelada")

    def procesar(self, impuesto=None, descuento=None):
        """
        Calcula el total y deja la reserva PROCESADA.
        Demuestra try / except / else / finally y encadenamiento de excepciones.
        """
        if self._estado != Reserva.CONFIRMADA:
            raise OperacionNoPermitidaError(f"Solo se procesan reservas confirmadas ({self.id} está {self._estado})")

        try:
            total = self._servicio.calcular_costo(self._duracion, impuesto, descuento)
        except CalculoInconsistenteError as error:
            # Encadenamos: el que llama ve un error de reserva y, como causa, el error de cálculo
            raise ReservaInvalidaError(f"No se pudo procesar la reserva {self.id}") from error
        else:
            # Solo se ejecuta si el cálculo no falló
            self._total = total
            self._estado = Reserva.PROCESADA
            log.info(f"Reserva {self.id} procesada por ${total:,.2f}")
            return total
        finally:
            # Se ejecuta siempre, haya error o no
            log.info(f"Intento de procesamiento de la reserva {self.id} finalizado (estado: {self._estado})")

    def describir(self):
        total = f"${self._total:,.2f}" if self._total is not None else "sin calcular"
        return (f"{self.id} | {self._cliente.nombre} -> {self._servicio.nombre} | "
                f"{self._duracion} {self._servicio.unidad()} | {self._estado} | Total: {total}")
