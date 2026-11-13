"""
PROYECTO SOFTWARE FJ
MODULO DE SERVICIOS Y RESERVA DE SALAS
"""

import logging
from abc import ABC, abstractmethod


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
            raise ValueError("El ID de la entidad es obligatorio.")

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
            raise ValueError("El nombre del servicio es obligatorio.")

        try:
            tarifa = float(tarifa)

        except (ValueError, TypeError) as error:
            raise ValueError(
                "La tarifa debe ser un numero valido."
            ) from error

        if tarifa <= 0:
            raise ValueError("La tarifa debe ser mayor que cero.")

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
            raise ValueError(
                "La capacidad maxima debe ser un entero positivo."
            )

        try:
            costo_proyector = float(costo_proyector)
            costo_videoconferencia = float(costo_videoconferencia)

        except (ValueError, TypeError) as error:
            raise ValueError(
                "Los costos adicionales deben ser numericos."
            ) from error

        if costo_proyector < 0 or costo_videoconferencia < 0:
            raise ValueError(
                "Los costos adicionales no pueden ser negativos."
            )

        self.capacidad_maxima = capacidad_maxima
        self.costo_proyector = costo_proyector
        self.costo_videoconferencia = costo_videoconferencia

    def validar_duracion(self, duracion):

        try:
            duracion = float(duracion)

        except (ValueError, TypeError) as error:
            raise ValueError(
                "La duracion debe ser un numero valido."
            ) from error

        if duracion <= 0:
            raise ValueError(
                "La duracion debe ser mayor que cero."
            )

        return duracion

    def validar_parametros(self, **kwargs):

        duracion = kwargs.get("duracion_horas")
        personas = kwargs.get("numero_personas")

        if duracion is None or personas is None:
            raise ValueError(
                "Debe indicar duracion y numero de personas."
            )

        duracion = self.validar_duracion(duracion)

        if (
            not isinstance(personas, int)
            or isinstance(personas, bool)
            or personas <= 0
        ):
            raise ValueError(
                "El numero de personas debe ser un entero positivo."
            )

        if personas > self.capacidad_maxima:
            raise ValueError(
                f"La sala admite maximo {self.capacidad_maxima} personas. "
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
            f"Capacidad maxima: {self.capacidad_maxima} personas\n"
            f"Tarifa por hora: ${self.tarifa:,.0f}\n"
            f"Costo proyector: ${self.costo_proyector:,.0f}\n"
            f"Costo videoconferencia: "
            f"${self.costo_videoconferencia:,.0f}"
        )

    # ======================================
    # MANEJO DE ERRORES
    # ======================================

    def calcular_costo_seguro(self, **kwargs):

        try:

            costo = self.calcular_costo(**kwargs)

        except (ValueError, TypeError) as error:

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

    except (ValueError, TypeError) as error:

        print(f"Error del sistema: {error}")
        logging.error("Error general: %s", error)

    except Exception as error:

        print(f"Error inesperado: {error}")
        logging.exception("Error inesperado durante las pruebas")
