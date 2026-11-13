"""
PROYECTO SOFTWARE FJ
CLASE ABSTRACTA SERVICIO Y RESERVA DE SALAS
"""

import logging
from abc import ABC, abstractmethod

from excepciones import (
    ServicioError,
    ServicioInvalidDataError,
    ServicioNoDisponibleError
)

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)


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
                "La tarifa debe ser un número válido."
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
                "La capacidad máxima debe ser un entero positivo."
            )

        try:
            costo_proyector = float(costo_proyector)
            costo_videoconferencia = float(costo_videoconferencia)
        except (ValueError, TypeError) as error:
            raise ServicioInvalidDataError(
                "Los costos adicionales deben ser numéricos."
            ) from error

        if costo_proyector < 0 or costo_videoconferencia < 0:
            raise ServicioInvalidDataError(
                "Los costos adicionales no pueden ser negativos."
            )

        self.capacidad_maxima = capacidad_maxima
        self.costo_proyector = costo_proyector
        self.costo_videoconferencia = costo_videoconferencia

    def validar_duracion(self, duracion):

        try:
            duracion = float(duracion)
        except (ValueError, TypeError) as error:
            raise ServicioInvalidDataError(
                "La duración debe ser un número válido."
            ) from error

        if duracion <= 0:
            raise ServicioInvalidDataError(
                "La duración debe ser mayor que cero."
            )

        return duracion

    def validar_parametros(self, **kwargs):

        duracion = kwargs.get("duracion_horas")
        personas = kwargs.get("numero_personas")

        if duracion is None or personas is None:
            raise ServicioInvalidDataError(
                "Debe indicar duración y número de personas."
            )

        duracion = self.validar_duracion(duracion)

        if (
            not isinstance(personas, int)
            or isinstance(personas, bool)
            or personas <= 0
        ):
            raise ServicioInvalidDataError(
                "El número de personas debe ser un entero positivo."
            )

        if personas > self.capacidad_maxima:
            raise ServicioNoDisponibleError(
                f"La sala admite máximo {self.capacidad_maxima} personas. "
                f"Se solicitaron {personas}."
            )

        return duracion

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

        return costo_total

    def describir_servicio(self):

        return (
            f"Reserva de sala: {self.nombre}\n"
            f"Capacidad máxima: {self.capacidad_maxima} personas\n"
            f"Tarifa por hora: ${self.tarifa:,.0f}\n"
            f"Costo proyector: ${self.costo_proyector:,.0f}\n"
            f"Costo videoconferencia: "
            f"${self.costo_videoconferencia:,.0f}"
        )

    def calcular_costo_seguro(self, **kwargs):

        try:
            costo = self.calcular_costo(**kwargs)

        except ServicioError as error:
            mensaje = f"Error al calcular el costo: {error}"
            print(mensaje)
            logging.error(mensaje)
            return None

        else:
            mensaje = f"Costo calculado correctamente: ${costo:,.0f}"
            print(mensaje)
            logging.info(mensaje)
            return costo

        finally:
            mensaje = "Finalizó la operación de cálculo de reserva."
            print(mensaje)
            logging.info(mensaje)


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

        print("\nINFORMACIÓN DEL SERVICIO")
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

    except ServicioError as error:
        print(f"Error del sistema: {error}")
        logging.error("Error general: %s", error)

    except Exception as error:
        print(f"Error inesperado: {error}")
        logging.exception("Error inesperado durante las pruebas")
