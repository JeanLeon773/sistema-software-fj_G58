"""
PROYECTO FASE 4 - SOFTWARE FJ
ESTUDIANTE 2: SERVICIO BASE Y SERVICIO DE RESERVAS DE SALAS

Desarrollo de la clase abstracta Servicio y la clase derivada
ServicioReservaSalas.
"""

import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Optional


# Configuracion de Logs
logger = logging.getLogger(__name__)


# =====================================================
# EXCEPCIONES PERSONALIZADAS
# =====================================================

class ServicioError(Exception):
    """Excepcion general para los servicios."""
    pass


class ServicioInvalidDataError(ServicioError):
    """Error cuando los datos del servicio son incorrectos."""
    pass


class ServicioNoDisponibleError(ServicioError):
    """Error cuando el servicio solicitado no esta disponible."""
    pass


# =====================================================
# CLASE ABSTRACTA SERVICIO
# =====================================================

class Servicio(ABC):

    def __init__(self, id_servicio: str, nombre: str,
                 tarifa_base: float):

        self.id_servicio = id_servicio
        self.nombre = nombre
        self.tarifa_base = tarifa_base

    @property
    def id_servicio(self):
        return self.__id_servicio

    @id_servicio.setter
    def id_servicio(self, valor):

        if not isinstance(valor, str) or not valor.strip():
            raise ServicioInvalidDataError(
                "El ID del servicio no puede estar vacio."
            )

        self.__id_servicio = valor.strip()

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):

        if not isinstance(valor, str) or not valor.strip():
            raise ServicioInvalidDataError(
                "El nombre del servicio no puede estar vacio."
            )

        self.__nombre = valor.strip()

    @property
    def tarifa_base(self):
        return self.__tarifa_base

    @tarifa_base.setter
    def tarifa_base(self, valor):

        if isinstance(valor, bool) or not isinstance(valor, (int, float)):
            raise ServicioInvalidDataError(
                "La tarifa debe ser un valor numerico."
            )

        if valor <= 0:
            raise ServicioInvalidDataError(
                "La tarifa debe ser mayor que cero."
            )

        self.__tarifa_base = float(valor)

    @abstractmethod
    def validar_parametros(self, **kwargs):
        """Valida los parametros del servicio."""
        pass

    @abstractmethod
    def calcular_costo(self, duracion_horas, **kwargs):
        """Calcula el costo del servicio."""
        pass

    @abstractmethod
    def describir_servicio(self):
        """Describe las caracteristicas del servicio."""
        pass

    def obtener_detalles(self):

        return (
            f"Servicio ID: {self.id_servicio} | "
            f"Nombre: {self.nombre} | "
            f"Tarifa por hora: ${self.tarifa_base:,.2f}"
        )


# =====================================================
# CLASE DERIVADA: RESERVA DE SALAS
# =====================================================

class ServicioReservaSalas(Servicio):

    def __init__(self, id_servicio, nombre, tarifa_base,
                 capacidad_maxima,
                 recursos_disponibles=None):

        super().__init__(id_servicio, nombre, tarifa_base)

        if isinstance(capacidad_maxima, bool) or not isinstance(capacidad_maxima, int):
            raise ServicioInvalidDataError(
                "La capacidad debe ser un numero entero."
            )

        if capacidad_maxima <= 0:
            raise ServicioInvalidDataError(
                "La capacidad debe ser mayor que cero."
            )

        self.__capacidad_maxima = capacidad_maxima

        if recursos_disponibles is None:
            recursos_disponibles = {}

        if not isinstance(recursos_disponibles, dict):
            raise ServicioInvalidDataError(
                "Los recursos deben estar en un diccionario."
            )

        self.__recursos_disponibles = {}

        for recurso, costo in recursos_disponibles.items():

            if not isinstance(recurso, str) or not recurso.strip():
                raise ServicioInvalidDataError(
                    "El nombre del recurso no es valido."
                )

            if (
                isinstance(costo, bool)
                or not isinstance(costo, (int, float))
                or costo < 0
            ):
                raise ServicioInvalidDataError(
                    "El costo del recurso debe ser numerico y no negativo."
                )

            self.__recursos_disponibles[recurso.strip().lower()] = float(costo)

        logger.info(
            "Servicio de reserva de salas creado: %s",
            self.id_servicio
        )

    @property
    def capacidad_maxima(self):
        return self.__capacidad_maxima

    @property
    def recursos_disponibles(self):
        return self.__recursos_disponibles.copy()

    # -------------------------------------------------
    # VALIDACION DE PARAMETROS
    # -------------------------------------------------

    def validar_parametros(self, duracion_horas,
                           numero_personas,
                           recursos_solicitados=None):

        if (
            isinstance(duracion_horas, bool)
            or not isinstance(duracion_horas, (int, float))
            or duracion_horas <= 0
        ):
            raise ServicioInvalidDataError(
                "La duracion debe ser mayor que cero."
            )

        if (
            isinstance(numero_personas, bool)
            or not isinstance(numero_personas, int)
        ):
            raise ServicioInvalidDataError(
                "El numero de personas debe ser entero."
            )

        if numero_personas <= 0:
            raise ServicioInvalidDataError(
                "Debe existir al menos una persona."
            )

        if numero_personas > self.capacidad_maxima:
            raise ServicioNoDisponibleError(
                f"La sala admite maximo {self.capacidad_maxima} personas."
            )

        if recursos_solicitados is None:
            recursos_solicitados = []

        if not isinstance(recursos_solicitados, list):
            raise ServicioInvalidDataError(
                "Los recursos solicitados deben estar en una lista."
            )

        for recurso in recursos_solicitados:

            if not isinstance(recurso, str) or not recurso.strip():
                raise ServicioInvalidDataError(
                    "El nombre del recurso no es valido."
                )

            if recurso.strip().lower() not in self.__recursos_disponibles:
                raise ServicioNoDisponibleError(
                    f"El recurso {recurso} no esta disponible."
                )

        return True

    # -------------------------------------------------
    # CALCULO DEL COSTO
    # -------------------------------------------------

    def calcular_costo(self, duracion_horas,
                       numero_personas=1,
                       recursos_solicitados=None):

        self.validar_parametros(
            duracion_horas,
            numero_personas,
            recursos_solicitados
        )

        if recursos_solicitados is None:
            recursos_solicitados = []

        costo_base = self.tarifa_base * duracion_horas

        costo_recursos = sum(
            self.__recursos_disponibles[recurso.strip().lower()]
            for recurso in recursos_solicitados
        )

        costo_total = costo_base + costo_recursos

        logger.info(
            "Costo calculado para el servicio %s: %.2f",
            self.id_servicio,
            costo_total
        )

        return costo_total

    # -------------------------------------------------
    # DESCRIPCION DEL SERVICIO
    # -------------------------------------------------

    def describir_servicio(self):

        if self.__recursos_disponibles:

            recursos = ", ".join(
                f"{nombre} (${costo:,.2f})"
                for nombre, costo in self.__recursos_disponibles.items()
            )

        else:
            recursos = "Sin recursos adicionales"

        return (
            f"Reserva de salas | "
            f"ID: {self.id_servicio} | "
            f"Nombre: {self.nombre} | "
            f"Tarifa por hora: ${self.tarifa_base:,.2f} | "
            f"Capacidad maxima: {self.capacidad_maxima} personas | "
            f"Recursos disponibles: {recursos}"
        )


# =====================================================
# PRUEBAS DE FUNCIONAMIENTO
# =====================================================

if __name__ == "__main__":

    logging.basicConfig(
        filename="app.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        encoding="utf-8"
    )

    print("\n======================================")
    print(" SOFTWARE FJ - RESERVA DE SALAS")
    print("======================================\n")

    try:

        sala = ServicioReservaSalas(
            id_servicio="SER-SAL-01",
            nombre="Sala de reuniones",
            tarifa_base=50000,
            capacidad_maxima=12,
            recursos_disponibles={
                "proyector": 20000,
                "videoconferencia": 35000
            }
        )

        print("INFORMACION DEL SERVICIO:")
        print(sala.describir_servicio())

        print("\nCALCULO DE RESERVA:")

        costo = sala.calcular_costo(
            duracion_horas=3,
            numero_personas=8,
            recursos_solicitados=["proyector"]
        )

        print(f"Duracion: 3 horas")
        print(f"Personas: 8")
        print(f"Costo total: ${costo:,.2f}")

        print("\nPRUEBA DE VALIDACION:")

        try:
            sala.validar_parametros(
                duracion_horas=2,
                numero_personas=20
            )

        except ServicioNoDisponibleError as error:
            print(f"Error controlado: {error}")
            logger.error("Validacion de sala fallida: %s", error)

    except ServicioError as error:

        print(f"Error en el servicio: {error}")
        logger.exception("Error durante la ejecucion del servicio")

    print("\n======================================")
    print(" FIN DE LAS PRUEBAS")
    print("======================================")
"""
PROYECTO SOFTWARE FJ
MODULO DE SERVICIOS Y RESERVA DE SALAS
ESTUDIANTE 2
"""

import logging
from abc import ABC, abstractmethod


# ==========================================
# EXCEPCIONES PERSONALIZADAS
# ==========================================

class SoftwareFJError(Exception):
    """Excepcion general del sistema Software FJ."""

    def __init__(self, mensaje="Error en el sistema Software FJ."):
        super().__init__(mensaje)
        self.mensaje = mensaje


class ServicioError(SoftwareFJError):
    """Excepcion general de servicios."""
    pass


class ServicioInvalidDataError(ServicioError):
    """Error en los datos del servicio."""
    pass


class ServicioNoDisponibleError(ServicioError):
    """Error cuando el servicio no esta disponible."""
    pass


class ParametrosFaltantesError(SoftwareFJError):
    """Error por parametros obligatorios faltantes."""

    def __init__(self, parametro):
        super().__init__(
            f"Parametro obligatorio faltante: '{parametro}'."
        )


class OperacionNoPermitidaError(SoftwareFJError):
    """Error por operaciones no permitidas."""

    def __init__(self, operacion, motivo):
        super().__init__(
            f"Operacion no permitida en '{operacion}': {motivo}."
        )


class ReservaIncorrectaError(SoftwareFJError):
    """Error en los datos de una reserva."""

    def __init__(self, detalle):
        super().__init__(
            f"Intento de reserva incorrecto: {detalle}."
        )


class CalculoInconsistenteError(SoftwareFJError):
    """Error en el calculo de costos."""

    def __init__(self, detalle):
        super().__init__(
            f"Calculo de costos inconsistente: {detalle}."
        )


# ==========================================
# CONFIGURACION DE REGISTROS
# ==========================================

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)


# ==========================================
# CLASE BASE ABSTRACTA
# ==========================================

class EntidadBase(ABC):

    def __init__(self, id_entidad):

        if not isinstance(id_entidad, str) or not id_entidad.strip():
            raise ServicioInvalidDataError(
                "El ID de la entidad es obligatorio."
            )

        self._id_entidad = id_entidad.strip()

    @property
    def id_entidad(self):
        return self._id_entidad

    @abstractmethod
    def obtener_detalles(self):
        pass


# ==========================================
# CLASE ABSTRACTA SERVICIO
# ==========================================

class Servicio(EntidadBase):

    def __init__(self, id_entidad, nombre, tarifa):

        super().__init__(id_entidad)

        if not isinstance(nombre, str) or not nombre.strip():
            raise ServicioInvalidDataError(
                "El nombre del servicio es obligatorio."
            )

        try:
            tarifa = float(tarifa)

        except (ValueError, TypeError) as error:
            raise ServicioInvalidDataError(
                "La tarifa debe ser un numero valido."
            ) from error

        if tarifa <= 0:
            raise ServicioInvalidDataError(
                "La tarifa debe ser mayor que cero."
            )

        self.nombre = nombre.strip()
        self.tarifa = tarifa

    @abstractmethod
    def validar_parametros(self, **kwargs):
        pass

    @abstractmethod
    def calcular_costo(self, **kwargs):
        pass

    @abstractmethod
    def describir_servicio(self):
        pass

    def obtener_detalles(self):

        return (
            f"Servicio: {self.nombre} | "
            f"ID: {self.id_entidad} | "
            f"Tarifa: ${self.tarifa:,.0f}"
        )


# ==========================================
# SERVICIO ESPECIALIZADO: RESERVA DE SALAS
# ==========================================

class ServicioReservaSalas(Servicio):

    def __init__(
        self,
        id_entidad,
        nombre,
        tarifa,
        capacidad_maxima,
        costo_proyector=0,
        costo_videoconferencia=0
    ):

        super().__init__(id_entidad, nombre, tarifa)

        if (
            not isinstance(capacidad_maxima, int)
            or isinstance(capacidad_maxima, bool)
            or capacidad_maxima <= 0
        ):
            raise ServicioInvalidDataError(
                "La capacidad maxima debe ser un entero positivo."
            )

        try:
            costo_proyector = float(costo_proyector)
            costo_videoconferencia = float(costo_videoconferencia)

        except (ValueError, TypeError) as error:
            raise ServicioInvalidDataError(
                "Los costos adicionales deben ser numericos."
            ) from error

        if costo_proyector < 0 or costo_videoconferencia < 0:
            raise ServicioInvalidDataError(
                "Los costos adicionales no pueden ser negativos."
            )

        self.capacidad_maxima = capacidad_maxima
        self.costo_proyector = costo_proyector
        self.costo_videoconferencia = costo_videoconferencia

    # ======================================
    # VALIDAR DURACION
    # ======================================

    def validar_duracion(self, duracion):

        try:
            duracion = float(duracion)

        except (ValueError, TypeError) as error:
            raise ServicioInvalidDataError(
                "La duracion debe ser un numero valido."
            ) from error

        if duracion <= 0:
            raise ReservaIncorrectaError(
                "La duracion debe ser mayor que cero."
            )

        return duracion

    # ======================================
    # VALIDAR PARAMETROS
    # ======================================

    def validar_parametros(self, **kwargs):

        duracion = kwargs.get("duracion_horas")
        personas = kwargs.get("numero_personas")

        if duracion is None:
            raise ParametrosFaltantesError("duracion_horas")

        if personas is None:
            raise ParametrosFaltantesError("numero_personas")

        duracion = self.validar_duracion(duracion)

        if (
            not isinstance(personas, int)
            or isinstance(personas, bool)
            or personas <= 0
        ):
            raise ReservaIncorrectaError(
                "El numero de personas debe ser un entero positivo."
            )

        if personas > self.capacidad_maxima:
            raise ServicioNoDisponibleError(
                f"La sala admite maximo {self.capacidad_maxima} personas. "
                f"Se solicitaron {personas}."
            )

        return duracion

    # ======================================
    # CALCULAR COSTO
    # ======================================

    def calcular_costo(
        self,
        duracion_horas,
        numero_personas,
        proyector=False,
        videoconferencia=False
    ):

        duracion = self.validar_parametros(
            duracion_horas=duracion_horas,
            numero_personas=numero_personas
        )

        costo_total = self.tarifa * duracion

        if proyector:
            costo_total += self.costo_proyector

        if videoconferencia:
            costo_total += self.costo_videoconferencia

        if costo_total <= 0:
            raise CalculoInconsistenteError(
                "El costo calculado no es valido."
            )

        return costo_total

    # ======================================
    # DESCRIBIR SERVICIO
    # ======================================

    def describir_servicio(self):

        return (
            f"Reserva de sala: {self.nombre}\n"
            f"Capacidad maxima: {self.capacidad_maxima} personas\n"
            f"Tarifa por hora: ${self.tarifa:,.0f}\n"
            f"Costo proyector: ${self.costo_proyector:,.0f}\n"
            f"Costo videoconferencia: "
            f"${self.costo_videoconferencia:,.0f}"
        )

    # ======================================
    # MANEJO DE EXCEPCIONES
    # ======================================

    def calcular_costo_seguro(self, **kwargs):

        try:

            costo = self.calcular_costo(**kwargs)

        except SoftwareFJError as error:

            mensaje = f"Error al calcular el costo: {error}"

            print(mensaje)
            logging.error(mensaje)

            return None

        else:

            mensaje = (
                f"Costo calculado correctamente: ${costo:,.0f}"
            )

            print(mensaje)
            logging.info(mensaje)

            return costo

        finally:

            mensaje = "Finalizo la operacion de calculo de reserva."

            print(mensaje)
            logging.info(mensaje)


# ==========================================
# PRUEBAS DEL SISTEMA
# ==========================================

if __name__ == "__main__":

    print("===== PRUEBAS SOFTWARE FJ =====")

    try:

        sala = ServicioReservaSalas(
            id_entidad="SAL01",
            nombre="Sala de reuniones",
            tarifa=50000,
            capacidad_maxima=12,
            costo_proyector=20000,
            costo_videoconferencia=35000
        )

        print("\nINFORMACION DEL SERVICIO")
        print(sala.describir_servicio())

        print("\nPRUEBA 1: RESERVA CORRECTA")

        sala.calcular_costo_seguro(
            duracion_horas=3,
            numero_personas=8,
            proyector=True,
            videoconferencia=True
        )

        print("\nPRUEBA 2: CAPACIDAD EXCEDIDA")

        sala.calcular_costo_seguro(
            duracion_horas=2,
            numero_personas=20
        )

    except SoftwareFJError as error:

        print(f"Error del sistema: {error}")
        logging.error("Error general: %s", error)

    except Exception as error:

        print(f"Error inesperado: {error}")
        logging.exception(
            "Error inesperado durante las pruebas"
        )
main
