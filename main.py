# main.py
# Sistema Integral de Gestión de Clientes, Servicios y Reservas - Software FJ
# Curso Programación 213023 - Fase 4 (trabajo colaborativo)
#
# Simula más de 10 operaciones completas (válidas e inválidas) y demuestra
# que el programa sigue funcionando aunque ocurran errores.
# Ejecutar con:  python main.py

from software_fj.excepciones import SoftwareFJError
from software_fj.registro import ARCHIVO_LOG, obtener_logger
from software_fj.servicios import IVA
from software_fj.sistema import SistemaSoftwareFJ

log = obtener_logger()
sistema = SistemaSoftwareFJ()

# Aquí guardamos los objetos creados para usarlos en operaciones siguientes
creados = {}

resultados = {"exitosas": 0, "fallidas": 0}


def ejecutar_operacion(numero, descripcion, operacion):
    """
    Ejecuta una operación sin dejar que un error detenga el programa.
    try / except / else / finally en un solo lugar.
    """
    print(f"\n[{numero:02d}] {descripcion}")
    log.info(f"Operación {numero:02d}: {descripcion}")
    try:
        resultado = operacion()
    except SoftwareFJError as error:
        # Error esperado del sistema: se informa y se registra
        resultados["fallidas"] += 1
        print(f"     ✗ Controlado: {error}")
        log.warning(f"Operación {numero:02d} rechazada: {error}"
                    + (f" | causa: {error.__cause__}" if error.__cause__ else ""))
        if error.__cause__:
            print(f"       Causa original: {error.__cause__}")
    except Exception as error:  # noqa: BLE001 - red de seguridad para errores inesperados
        resultados["fallidas"] += 1
        print(f"     ✗ Error inesperado controlado: {type(error).__name__}: {error}")
        log.critical(f"Error inesperado en la operación {numero:02d}: {type(error).__name__}: {error}")
    else:
        resultados["exitosas"] += 1
        print(f"     ✓ {resultado}")
    finally:
        log.info(f"Operación {numero:02d} terminada")


# ---------------- operaciones de la simulación ----------------

def op_cliente_valido_ana():
    creados["ana"] = sistema.registrar_cliente("ana maría gómez", "1032456789", "ana.gomez@correo.com", "3104567890")
    return f"Cliente registrado: {creados['ana']}"


def op_cliente_correo_invalido():
    return sistema.registrar_cliente("Pedro Ruiz", "79845612", "pedro.ruiz-sin-arroba.com")


def op_cliente_sin_nombre():
    return sistema.registrar_cliente("", "52123456", "sin.nombre@correo.com")


def op_cliente_valido_carlos():
    creados["carlos"] = sistema.registrar_cliente("Carlos Pérez", "80123456", "carlos.perez@correo.com")
    return f"Cliente registrado: {creados['carlos']}"


def op_cliente_duplicado():
    return sistema.registrar_cliente("Ana Duplicada", "1032456789", "otra@correo.com")


def op_sala_valida():
    creados["sala"] = sistema.crear_servicio("sala", nombre="Sala Andes", tarifa_hora=80000, capacidad=30)
    return f"Servicio creado: {creados['sala']}"


def op_equipo_tarifa_negativa():
    return sistema.crear_servicio("equipo", nombre="Proyector", tarifa_dia=-5000)


def op_asesoria_valida():
    creados["asesoria"] = sistema.crear_servicio(
        "asesoria", nombre="Arquitectura en la nube", tarifa_hora=150000, especialidad="Cloud", nivel="senior")
    return f"Servicio creado: {creados['asesoria']}"


def op_equipo_no_disponible():
    creados["portatil"] = sistema.crear_servicio("equipo", nombre="Portátil Dell", tarifa_dia=45000, deposito=200000)
    creados["portatil"].cambiar_disponibilidad(False)
    return f"Servicio creado y marcado como NO disponible: {creados['portatil']}"


def op_servicio_tipo_desconocido():
    return sistema.crear_servicio("transporte", nombre="Van", tarifa=100000)


def op_servicio_sin_datos():
    return sistema.crear_servicio("asesoria", nombre="Asesoría incompleta")


def op_reserva_exitosa():
    reserva = sistema.crear_reserva("1032456789", creados["sala"].id, 3)
    reserva.confirmar()
    total = reserva.procesar(impuesto=IVA)
    creados["reserva_ana"] = reserva
    return f"Reserva procesada con IVA (total ${total:,.2f}): {reserva.id}"


def op_reserva_duracion_invalida():
    return sistema.crear_reserva("80123456", creados["sala"].id, 20)


def op_reserva_servicio_no_disponible():
    return sistema.crear_reserva("80123456", creados["portatil"].id, 2)


def op_reserva_cliente_inexistente():
    return sistema.crear_reserva("99999999", creados["asesoria"].id, 2)


def op_procesar_descuento_invalido():
    reserva = sistema.crear_reserva("80123456", creados["asesoria"].id, 2)
    reserva.confirmar()
    creados["reserva_carlos"] = reserva
    return reserva.procesar(impuesto=IVA, descuento=1.5)


def op_procesar_con_descuento_valido():
    reserva = creados["reserva_carlos"]
    total = reserva.procesar(impuesto=IVA, descuento=0.10)
    return f"Reserva procesada con IVA y 10 % de descuento (total ${total:,.2f}): {reserva.id}"


def op_cancelar_reserva_procesada():
    creados["reserva_ana"].cancelar()
    return "Reserva cancelada"


def op_error_inesperado():
    # Simula un fallo que no es del sistema (clave que no existe) para mostrar la red de seguridad
    return creados["reserva_que_no_existe"]


OPERACIONES = [
    ("Registrar cliente válido (Ana)", op_cliente_valido_ana),
    ("Registrar cliente con correo inválido", op_cliente_correo_invalido),
    ("Registrar cliente sin nombre", op_cliente_sin_nombre),
    ("Registrar cliente válido (Carlos)", op_cliente_valido_carlos),
    ("Registrar cliente con documento duplicado", op_cliente_duplicado),
    ("Crear servicio de sala válido", op_sala_valida),
    ("Crear alquiler de equipo con tarifa negativa", op_equipo_tarifa_negativa),
    ("Crear asesoría senior válida", op_asesoria_valida),
    ("Crear equipo y marcarlo como no disponible", op_equipo_no_disponible),
    ("Crear servicio de un tipo que no existe", op_servicio_tipo_desconocido),
    ("Crear asesoría sin tarifa ni especialidad", op_servicio_sin_datos),
    ("Reserva exitosa: confirmar y procesar con IVA", op_reserva_exitosa),
    ("Reserva de sala por 20 horas (máximo 12)", op_reserva_duracion_invalida),
    ("Reserva de un equipo no disponible", op_reserva_servicio_no_disponible),
    ("Reserva para un cliente que no existe", op_reserva_cliente_inexistente),
    ("Procesar reserva con descuento de 150 %", op_procesar_descuento_invalido),
    ("Procesar la misma reserva con descuento válido", op_procesar_con_descuento_valido),
    ("Cancelar una reserva ya procesada", op_cancelar_reserva_procesada),
    ("Provocar un error inesperado", op_error_inesperado),
]


if __name__ == "__main__":
    print("=" * 70)
    print(" SOFTWARE FJ - Sistema de Gestión de Clientes, Servicios y Reservas")
    print("=" * 70)
    log.info("===== Inicio de la simulación =====")

    for numero, (descripcion, operacion) in enumerate(OPERACIONES, start=1):
        ejecutar_operacion(numero, descripcion, operacion)

    print("\n" + "=" * 70)
    print(f" Operaciones: {len(OPERACIONES)} | Exitosas: {resultados['exitosas']} | "
          f"Controladas con error: {resultados['fallidas']}")
    print("=" * 70)
    print(sistema.resumen())
    print(f"\nEl sistema terminó sin interrupciones. Log: {ARCHIVO_LOG}")
    log.info("===== Fin de la simulación =====")
