# sistema.py
# Gestor central de Software FJ. Guarda clientes, servicios y reservas en
# LISTAS internas (sin base de datos) y registra cada evento en el log.

from .cliente import Cliente
from .excepciones import (DatosInvalidosError, ParametroFaltanteError, ReservaInvalidaError,
                          ServicioNoDisponibleError, SoftwareFJError)
from .registro import obtener_logger
from .reserva import Reserva
from .servicios import AlquilerEquipo, Asesoria, ReservaSala

log = obtener_logger()


class SistemaSoftwareFJ:
    """Administra las listas del sistema y ofrece las operaciones principales."""

    # Tipos de servicio que se pueden crear. Para añadir uno nuevo basta con
    # crear su clase en servicios.py y agregarla aquí.
    TIPOS_SERVICIO = {"sala": ReservaSala, "equipo": AlquilerEquipo, "asesoria": Asesoria}

    def __init__(self):
        self._clientes = []
        self._servicios = []
        self._reservas = []

    # ---------------- clientes ----------------
    def registrar_cliente(self, nombre, documento, correo, telefono=None):
        """Crea un cliente validado y lo guarda. Lanza una excepción si los datos fallan."""
        try:
            if self.buscar_cliente(documento, lanzar=False):
                raise DatosInvalidosError(f"Ya existe un cliente con el documento {documento}")
            cliente = Cliente(nombre, documento, correo, telefono)
        except SoftwareFJError as error:
            log.error(f"Registro de cliente rechazado: {error}")
            raise
        else:
            self._clientes.append(cliente)
            log.info(f"Cliente registrado: {cliente.describir()}")
            return cliente

    def buscar_cliente(self, documento, lanzar=True):
        for cliente in self._clientes:
            if cliente.documento == str(documento):
                return cliente
        if lanzar:
            raise DatosInvalidosError(f"No existe un cliente con el documento {documento}")
        return None

    # ---------------- servicios ----------------
    def crear_servicio(self, tipo, **datos):
        """Crea un servicio del tipo indicado (sala, equipo o asesoria)."""
        try:
            if tipo not in self.TIPOS_SERVICIO:
                raise DatosInvalidosError(f"Tipo de servicio desconocido: '{tipo}'")
            servicio = self.TIPOS_SERVICIO[tipo](**datos)
        except TypeError as error:
            # Un TypeError aquí significa que faltó un argumento: lo convertimos en error propio
            nuevo = ParametroFaltanteError(f"datos del servicio '{tipo}'")
            log.error(f"Creación de servicio rechazada: {nuevo} ({error})")
            raise nuevo from error
        except SoftwareFJError as error:
            log.error(f"Creación de servicio rechazada: {error}")
            raise
        else:
            self._servicios.append(servicio)
            log.info(f"Servicio creado: {servicio.describir()}")
            return servicio

    def buscar_servicio(self, id_servicio):
        for servicio in self._servicios:
            if servicio.id == id_servicio:
                return servicio
        raise DatosInvalidosError(f"No existe el servicio {id_servicio}")

    # ---------------- reservas ----------------
    def crear_reserva(self, documento, id_servicio, duracion):
        """Crea una reserva pendiente uniendo cliente, servicio y duración."""
        try:
            cliente = self.buscar_cliente(documento)
            servicio = self.buscar_servicio(id_servicio)
            if not servicio.disponible:
                raise ServicioNoDisponibleError(servicio.nombre)
            reserva = Reserva(cliente, servicio, duracion)
        except ReservaInvalidaError as error:
            log.error(f"Reserva rechazada: {error} | causa: {error.__cause__}")
            raise
        except SoftwareFJError as error:
            log.error(f"Reserva rechazada: {error}")
            raise
        else:
            self._reservas.append(reserva)
            log.info(f"Reserva creada: {reserva.describir()}")
            return reserva

    # ---------------- consultas ----------------
    def resumen(self):
        """Devuelve un texto con todo lo que hay registrado en las listas."""
        lineas = [f"Clientes ({len(self._clientes)}):"]
        lineas += [f"  {c.describir()}" for c in self._clientes]
        lineas.append(f"Servicios ({len(self._servicios)}):")
        lineas += [f"  {s.describir()}" for s in self._servicios]
        lineas.append(f"Reservas ({len(self._reservas)}):")
        lineas += [f"  {r.describir()}" for r in self._reservas]
        return "\n".join(lineas)
