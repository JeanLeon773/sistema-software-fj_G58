"""
PROYECTO FASE 4 - SOFTWARE FJ
MÓDULO DE RESERVAS

Clase Reserva: integra un Cliente, un Servicio, una duración y un estado.
Implementa confirmación, cancelación y procesamiento con manejo de
excepciones (try/except/else/finally), encadenamiento de excepciones
(raise ... from ...) y registro de eventos y errores en el log.

Requiere Cliente.py y Servicio.py en la misma carpeta.
"""

import logging
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

# Cliente.py ya configura el archivo app.log al importarse (basicConfig).
from Cliente import Cliente, EntidadBase
from Servicio import Servicio, ServicioError

logger = logging.getLogger(__name__)


# =====================================================
# EXCEPCIONES PERSONALIZADAS
# =====================================================

class ReservaError(Exception):
    """Excepción base para todos los errores del módulo de reservas."""
    pass


class ReservaInvalidDataError(ReservaError):
    """Datos inválidos al crear o usar una reserva."""
    pass


class EstadoReservaError(ReservaError):
    """Operación no permitida para el estado actual de la reserva."""
    pass


class ReservaProcesamientoError(ReservaError):
    """Fallo al calcular o procesar el costo de la reserva."""
    pass


# =====================================================
# ESTADOS Y TRANSICIONES PERMITIDAS
# =====================================================

class EstadoReserva(Enum):
    PENDIENTE = "Pendiente"
    CONFIRMADA = "Confirmada"
    CANCELADA = "Cancelada"
    PROCESADA = "Procesada"


TRANSICIONES_PERMITIDAS = {
    EstadoReserva.PENDIENTE: {EstadoReserva.CONFIRMADA, EstadoReserva.CANCELADA},
    EstadoReserva.CONFIRMADA: {EstadoReserva.PROCESADA, EstadoReserva.CANCELADA},
    EstadoReserva.CANCELADA: set(),   # estado final
    EstadoReserva.PROCESADA: set(),   # estado final
}


# =====================================================
# CLASE RESERVA
# =====================================================

class Reserva(EntidadBase):
    """Reserva de un Servicio hecha por un Cliente."""

    def __init__(self, id_entidad: str, cliente: Cliente, servicio: Servicio,
                 duracion_horas: float, **parametros_servicio: Any):
        """
        parametros_servicio: parámetros propios de cada servicio, por ejemplo
        numero_personas y recursos_solicitados para ServicioReservaSalas.
        """
        if not isinstance(id_entidad, str) or not id_entidad.strip():
            raise ReservaInvalidDataError("El ID de la reserva no puede estar vacío.")

        if not isinstance(cliente, Cliente):
            raise ReservaInvalidDataError(
                "La reserva requiere un objeto Cliente válido."
            )

        if not isinstance(servicio, Servicio):
            raise ReservaInvalidDataError(
                "La reserva requiere un objeto Servicio válido."
            )

        if (
            isinstance(duracion_horas, bool)
            or not isinstance(duracion_horas, (int, float))
            or duracion_horas <= 0
        ):
            raise ReservaInvalidDataError(
                "La duración debe ser un número mayor que cero."
            )

        # Validación delegada al servicio (polimorfismo); se encadena el error original.
        try:
            servicio.validar_parametros(
                duracion_horas=duracion_horas, **parametros_servicio
            )
        except (ServicioError, TypeError) as error:
            raise ReservaInvalidDataError(
                f"Parámetros inválidos para el servicio '{servicio.nombre}': {error}"
            ) from error

        super().__init__(id_entidad.strip())
        self.__cliente = cliente
        self.__servicio = servicio
        self.__duracion_horas = float(duracion_horas)
        self.__parametros = dict(parametros_servicio)
        self.__estado = EstadoReserva.PENDIENTE
        self.__costo_total: Optional[float] = None
        self.__historial: List[str] = []
        self._registrar_historial("Reserva creada")

        logger.info(
            "Reserva %s creada (cliente %s, servicio %s, %.2f h)",
            self.id_entidad, cliente.id_entidad, servicio.id_servicio,
            self.__duracion_horas,
        )

    # -------------------------------------------------
    # PROPIEDADES (solo lectura: encapsulación)
    # -------------------------------------------------

    @property
    def cliente(self) -> Cliente:
        return self.__cliente

    @property
    def servicio(self) -> Servicio:
        return self.__servicio

    @property
    def duracion_horas(self) -> float:
        return self.__duracion_horas

    @property
    def estado(self) -> EstadoReserva:
        return self.__estado

    @property
    def costo_total(self) -> Optional[float]:
        """Costo final; es None hasta que la reserva se procesa."""
        return self.__costo_total

    @property
    def parametros_servicio(self) -> Dict[str, Any]:
        return dict(self.__parametros)

    @property
    def historial(self) -> List[str]:
        return list(self.__historial)

    # -------------------------------------------------
    # MÉTODOS INTERNOS
    # -------------------------------------------------

    def _registrar_historial(self, evento: str) -> None:
        marca = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.__historial.append(f"{marca} - {evento}")

    def _cambiar_estado(self, nuevo_estado: EstadoReserva) -> None:
        """Aplica una transición solo si está permitida."""
        if nuevo_estado not in TRANSICIONES_PERMITIDAS[self.__estado]:
            raise EstadoReservaError(
                f"No se puede pasar de '{self.__estado.value}' "
                f"a '{nuevo_estado.value}'."
            )
        anterior = self.__estado
        self.__estado = nuevo_estado
        self._registrar_historial(f"{anterior.value} -> {nuevo_estado.value}")

    @staticmethod
    def _validar_porcentaje(nombre: str, valor: float) -> None:
        if isinstance(valor, bool) or not isinstance(valor, (int, float)):
            raise ReservaInvalidDataError(f"El {nombre} debe ser numérico.")
        if not 0 <= valor <= 1:
            raise ReservaInvalidDataError(
                f"El {nombre} debe estar entre 0 y 1 (ej. 0.19 = 19%)."
            )

    # -------------------------------------------------
    # CÁLCULO DE COSTO (variantes por parámetros opcionales)
    #   calcular_costo_total()                      -> costo base
    #   calcular_costo_total(impuesto=0.19)         -> con impuesto
    #   calcular_costo_total(descuento=0.10)        -> con descuento
    #   calcular_costo_total(0.19, 0.10)            -> ambos
    # El descuento se aplica primero y luego el impuesto.
    # -------------------------------------------------

    def calcular_costo_total(self, impuesto: float = 0.0,
                             descuento: float = 0.0) -> float:
        self._validar_porcentaje("impuesto", impuesto)
        self._validar_porcentaje("descuento", descuento)

        try:
            costo_base = self.__servicio.calcular_costo(
                self.__duracion_horas, **self.__parametros
            )
        except (ServicioError, TypeError) as error:
            raise ReservaProcesamientoError(
                f"El servicio no pudo calcular el costo: {error}"
            ) from error

        if (
            isinstance(costo_base, bool)
            or not isinstance(costo_base, (int, float))
            or costo_base <= 0
        ):
            raise ReservaProcesamientoError(
                f"El servicio devolvió un costo inconsistente: {costo_base!r}"
            )

        return costo_base * (1 - descuento) * (1 + impuesto)

    # -------------------------------------------------
    # CONFIRMAR
    # -------------------------------------------------

    def confirmar(self) -> bool:
        try:
            self._cambiar_estado(EstadoReserva.CONFIRMADA)
        except EstadoReservaError as error:
            mensaje = f"[ERROR DE ESTADO] Reserva {self.id_entidad}: {error}"
            print(mensaje)
            logger.error(mensaje)
            return False
        except Exception as error:
            mensaje = f"[ERROR INESPERADO] Confirmando reserva {self.id_entidad}: {error}"
            print(mensaje)
            logger.exception(mensaje)
            return False
        else:
            mensaje = f"[ÉXITO] Reserva {self.id_entidad} confirmada."
            print(mensaje)
            logger.info(mensaje)
            return True
        finally:
            logger.info("Finalizado intento de confirmación de %s", self.id_entidad)

    # -------------------------------------------------
    # CANCELAR
    # -------------------------------------------------

    def cancelar(self, motivo: str = "") -> bool:
        try:
            self._cambiar_estado(EstadoReserva.CANCELADA)
        except EstadoReservaError as error:
            mensaje = f"[ERROR DE ESTADO] Reserva {self.id_entidad}: {error}"
            print(mensaje)
            logger.error(mensaje)
            return False
        except Exception as error:
            mensaje = f"[ERROR INESPERADO] Cancelando reserva {self.id_entidad}: {error}"
            print(mensaje)
            logger.exception(mensaje)
            return False
        else:
            detalle = f" Motivo: {motivo}" if motivo else ""
            mensaje = f"[ÉXITO] Reserva {self.id_entidad} cancelada.{detalle}"
            print(mensaje)
            logger.info(mensaje)
            return True
        finally:
            logger.info("Finalizado intento de cancelación de %s", self.id_entidad)

    # -------------------------------------------------
    # PROCESAR
    # -------------------------------------------------

    def procesar(self, impuesto: float = 0.0, descuento: float = 0.0) -> bool:
        """Procesa una reserva confirmada: calcula el costo y la marca como procesada."""
        costo = None
        try:
            if self.__estado != EstadoReserva.CONFIRMADA:
                raise EstadoReservaError(
                    f"Solo se puede procesar una reserva confirmada "
                    f"(estado actual: '{self.__estado.value}')."
                )
            costo = self.calcular_costo_total(impuesto, descuento)
        except EstadoReservaError as error:
            mensaje = f"[ERROR DE ESTADO] Reserva {self.id_entidad}: {error}"
            print(mensaje)
            logger.error(mensaje)
            return False
        except ReservaProcesamientoError as error:
            causa = f" | Causa: {error.__cause__}" if error.__cause__ else ""
            mensaje = f"[ERROR DE PROCESAMIENTO] Reserva {self.id_entidad}: {error}{causa}"
            print(mensaje)
            logger.error(mensaje)
            return False
        except ReservaError as error:
            mensaje = f"[ERROR DE VALIDACIÓN] Reserva {self.id_entidad}: {error}"
            print(mensaje)
            logger.error(mensaje)
            return False
        except Exception as error:
            mensaje = f"[ERROR INESPERADO] Procesando reserva {self.id_entidad}: {error}"
            print(mensaje)
            logger.exception(mensaje)
            return False
        else:
            # Solo si el cálculo salió bien: se actualiza el estado.
            self._cambiar_estado(EstadoReserva.PROCESADA)
            self.__costo_total = costo
            mensaje = (
                f"[ÉXITO] Reserva {self.id_entidad} procesada. "
                f"Costo total: ${costo:,.2f}"
            )
            print(mensaje)
            logger.info(mensaje)
            return True
        finally:
            print(f"-> Operación de procesamiento finalizada para reserva: {self.id_entidad}\n")
            logger.info("Finalizado procesamiento de reserva %s", self.id_entidad)

    # -------------------------------------------------
    # IMPLEMENTACIÓN DEL MÉTODO ABSTRACTO DE EntidadBase
    # -------------------------------------------------

    def obtener_detalles(self) -> str:
        costo = f"${self.__costo_total:,.2f}" if self.__costo_total is not None else "Sin calcular"
        return (
            f"Reserva [ID: {self.id_entidad}] | "
            f"Cliente: {self.__cliente.nombre} ({self.__cliente.id_entidad}) | "
            f"Servicio: {self.__servicio.nombre} ({self.__servicio.id_servicio}) | "
            f"Duración: {self.__duracion_horas:g} h | "
            f"Estado: {self.__estado.value} | "
            f"Costo: {costo}"
        )


# =====================================================
# CREACIÓN SEGURA (mismo estilo de registrar_cliente_seguro)
# =====================================================

def crear_reserva_segura(id_entidad, cliente, servicio, duracion_horas,
                         **parametros_servicio) -> Optional[Reserva]:
    """Intenta crear una reserva sin detener el programa si hay errores."""
    reserva = None
    try:
        reserva = Reserva(id_entidad, cliente, servicio, duracion_horas,
                          **parametros_servicio)
    except ReservaError as error:
        causa = f" | Causa: {error.__cause__}" if error.__cause__ else ""
        mensaje = f"[ERROR DE RESERVA] No se pudo crear la reserva {id_entidad}: {error}{causa}"
        print(mensaje)
        logger.error(mensaje)
    except Exception as error:
        mensaje = f"[ERROR INESPERADO] Creando reserva {id_entidad}: {error}"
        print(mensaje)
        logger.exception(mensaje)
    else:
        mensaje = f"[ÉXITO] {reserva.obtener_detalles()}"
        print(mensaje)
        logger.info(mensaje)
    finally:
        print(f"-> Operación de creación finalizada para reserva: {id_entidad}\n")
        logger.info("Finalizado intento de creación de reserva %s", id_entidad)
    return reserva


# =====================================================
# PRUEBAS DE FUNCIONAMIENTO
# =====================================================

if __name__ == "__main__":
    from Servicio import ServicioReservaSalas

    print("\n======================================")
    print(" SOFTWARE FJ - MÓDULO DE RESERVAS")
    print("======================================\n")

    cliente = Cliente("CLI01", "Juan Pérez", "juan@mail.com", "3001234567")
    sala = ServicioReservaSalas(
        "SER-SAL-01", "Sala de reuniones", 50000, 12,
        {"proyector": 20000, "videoconferencia": 35000},
    )

    print("1) Reserva válida")
    r1 = crear_reserva_segura("RES01", cliente, sala, 3,
                              numero_personas=8, recursos_solicitados=["proyector"])

    print("2) Confirmar reserva")
    r1.confirmar()

    print("3) Procesar con impuesto 19% y descuento 10%")
    r1.procesar(impuesto=0.19, descuento=0.10)

    print("4) Procesar de nuevo (ya procesada)")
    r1.procesar()

    print("5) Capacidad excedida (20 personas, máximo 12)")
    crear_reserva_segura("RES02", cliente, sala, 2, numero_personas=20)

    print("6) Cliente inválido (None)")
    crear_reserva_segura("RES03", None, sala, 2, numero_personas=4)

    print("7) Duración inválida (-2 horas)")
    crear_reserva_segura("RES04", cliente, sala, -2, numero_personas=4)

    print("8) Recurso inexistente")
    crear_reserva_segura("RES05", cliente, sala, 2, numero_personas=4,
                         recursos_solicitados=["piscina"])

    print("9) Procesar sin confirmar")
    r6 = crear_reserva_segura("RES06", cliente, sala, 2, numero_personas=5)
    r6.procesar()

    print("10) Cancelar, y luego intentar confirmar y procesar")
    r6.cancelar("El cliente ya no la necesita")
    r6.confirmar()
    r6.procesar()

    print("11) Impuesto inválido en una reserva confirmada")
    r7 = crear_reserva_segura("RES07", cliente, sala, 1, numero_personas=2)
    r7.confirmar()
    r7.procesar(impuesto=1.5)
    print(f"Estado tras el error (sigue confirmada): {r7.estado.value}\n")

    print("RESUMEN FINAL")
    for r in (r1, r6, r7):
        print(r.obtener_detalles())

    print("\nHistorial de RES01:")
    for evento in r1.historial:
        print("  ", evento)

    print("\n======================================")
    print(" FIN DE LAS PRUEBAS (revise app.log)")
    print("======================================")
