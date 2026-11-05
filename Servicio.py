
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
