# excepciones.py
# Excepciones personalizadas del sistema Software FJ.
# Todas heredan de SoftwareFJError, así el programa principal puede
# atrapar cualquier error propio del sistema con un solo "except".


class SoftwareFJError(Exception):
    """Excepción base de todo el sistema Software FJ."""

    def __init__(self, mensaje, codigo="ERROR_GENERAL"):
        # Guardamos el mensaje legible y un código corto para el log
        super().__init__(mensaje)
        self.mensaje = mensaje
        self.codigo = codigo

    def __str__(self):
        # Formato que se ve en consola y en el archivo de logs
        return f"[{self.codigo}] {self.mensaje}"


class DatosInvalidosError(SoftwareFJError):
    """Un dato tiene un formato o valor incorrecto (correo, documento, tarifa...)."""

    def __init__(self, mensaje):
        super().__init__(mensaje, "DATOS_INVALIDOS")


class ParametroFaltanteError(SoftwareFJError):
    """Falta un parámetro obligatorio para crear un objeto u operar."""

    def __init__(self, parametro):
        super().__init__(f"Falta el parámetro obligatorio: '{parametro}'", "PARAMETRO_FALTANTE")
        self.parametro = parametro


class ClienteInvalidoError(DatosInvalidosError):
    """Error específico al validar los datos de un cliente."""


class ServicioNoDisponibleError(SoftwareFJError):
    """El servicio existe pero no se puede reservar en este momento."""

    def __init__(self, nombre_servicio):
        super().__init__(f"El servicio '{nombre_servicio}' no está disponible", "SERVICIO_NO_DISPONIBLE")


class ReservaInvalidaError(SoftwareFJError):
    """La reserva no se puede crear o procesar con los datos dados."""

    def __init__(self, mensaje):
        super().__init__(mensaje, "RESERVA_INVALIDA")


class OperacionNoPermitidaError(SoftwareFJError):
    """La operación no está permitida en el estado actual (ej.: cancelar algo ya procesado)."""

    def __init__(self, mensaje):
        super().__init__(mensaje, "OPERACION_NO_PERMITIDA")


class CalculoInconsistenteError(SoftwareFJError):
    """El cálculo de un costo dio un resultado sin sentido (negativo, descuento > 100 %...)."""

    def __init__(self, mensaje):
        super().__init__(mensaje, "CALCULO_INCONSISTENTE")
