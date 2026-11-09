
# ============================================================
# SERVICIOS ESPECIALIZADOS
# Autor: Christian Coronado
# Descripcion: Servicios de alquiler de equipos y asesoria.
# ============================================================

import logging
import math

from Servicio import (
    Servicio,
    ServicioError,
    ServicioInvalidDataError,
    ServicioNoDisponibleError
)

logger = logging.getLogger(__name__)


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

# Validar que los impuestos y descuentos tengan valores permitidos
def validar_porcentajes(impuesto, descuento):
    if isinstance(impuesto, bool) or not isinstance(impuesto, (int, float)) or not math.isfinite(impuesto) or not 0 <= impuesto <= 100:
        raise ServicioInvalidDataError("El impuesto debe estar entre 0 y 100.")

    if isinstance(descuento, bool) or not isinstance(descuento, (int, float)) or not math.isfinite(descuento) or not 0 <= descuento <= 100:
        raise ServicioInvalidDataError("El descuento debe estar entre 0 y 100.")


# Aplicar primero el descuento y después el impuesto al costo base
def aplicar_impuestos_descuentos(costo_base, impuesto=0, descuento=0):
    validar_porcentajes(impuesto, descuento)
    costo_con_descuento = costo_base * (1 - descuento / 100)
    costo_total = costo_con_descuento * (1 + impuesto / 100)
    return round(costo_total, 2)


# ============================================================
# SERVICIO DE ALQUILER DE EQUIPOS
# ============================================================

class ServicioAlquilerEquipos(Servicio):
    """Servicio especializado para alquiler de equipos."""

    # Inicializar los datos propios del alquiler de equipos
    def __init__(self, id_servicio, nombre, tarifa_base, tipo_equipo, cantidad_disponible):
        super().__init__(id_servicio, nombre, tarifa_base)

        # Validar el tipo de equipo
        if not isinstance(tipo_equipo, str) or not tipo_equipo.strip():
            raise ServicioInvalidDataError("El tipo de equipo no puede estar vacio.")

        # Validar que la cantidad disponible sea un entero positivo
        if isinstance(cantidad_disponible, bool) or not isinstance(cantidad_disponible, int) or cantidad_disponible <= 0:
            raise ServicioInvalidDataError("La cantidad disponible debe ser un entero positivo.")

        self.__tipo_equipo = tipo_equipo.strip()
        self.__cantidad_disponible = cantidad_disponible
        self.__cantidad_alquilada = 0

    # Consultar el tipo de equipo y las cantidades
    @property
    def tipo_equipo(self):
        return self.__tipo_equipo

    @property
    def cantidad_disponible(self):
        return self.__cantidad_disponible

    @property
    def cantidad_alquilada(self):
        return self.__cantidad_alquilada

    # Validar que la cantidad solicitada sea correcta
    def _validar_cantidad(self, cantidad):
        if isinstance(cantidad, bool) or not isinstance(cantidad, int) or cantidad <= 0:
            raise ServicioInvalidDataError("La cantidad debe ser un entero positivo.")

        if cantidad > self.__cantidad_disponible:
            raise ServicioNoDisponibleError("No hay suficientes equipos disponibles.")

    # Validar la duración y la cantidad de equipos solicitados
    def validar_parametros(self, duracion_horas, cantidad=1):
        if isinstance(duracion_horas, bool) or not isinstance(duracion_horas, (int, float)) or not math.isfinite(duracion_horas) or duracion_horas <= 0:
            raise ServicioInvalidDataError("La duracion debe ser mayor que cero.")

        self._validar_cantidad(cantidad)
        return True

    # Registrar el alquiler y actualizar la disponibilidad
    def registrar_alquiler(self, cantidad=1):
        self._validar_cantidad(cantidad)
        self.__cantidad_disponible -= cantidad
        self.__cantidad_alquilada += cantidad

        logger.info("Alquiler registrado: %s equipos del servicio %s.", cantidad, self.id_servicio)
        return self.__cantidad_disponible

    # Registrar la devolucion y actualizar la disponibilidad
    def registrar_devolucion(self, cantidad=1):
        if isinstance(cantidad, bool) or not isinstance(cantidad, int) or cantidad <= 0:
            raise ServicioInvalidDataError("La cantidad devuelta debe ser un entero positivo.")

        if cantidad > self.__cantidad_alquilada:
            raise ServicioInvalidDataError("La devolucion supera la cantidad de equipos alquilados.")

        self.__cantidad_alquilada -= cantidad
        self.__cantidad_disponible += cantidad

        logger.info("Devolucion registrada: %s equipos del servicio %s.", cantidad, self.id_servicio)
        return self.__cantidad_disponible

    # Calcular el costo del alquiler con impuestos y descuentos opcionales
    def calcular_costo(self, duracion_horas, cantidad=1, impuesto=0, descuento=0):
        self.validar_parametros(duracion_horas, cantidad)
        costo_base = self.tarifa_base * duracion_horas * cantidad
        costo_total = aplicar_impuestos_descuentos(costo_base, impuesto, descuento)

        logger.info("Costo de alquiler calculado para el servicio %s.", self.id_servicio)
        return costo_total

    # Mostrar la descripción del servicio de alquiler
    def describir_servicio(self):
        return (f"Alquiler de equipos: {self.nombre}. Tipo: {self.__tipo_equipo}. "
                f"Cantidad disponible: {self.__cantidad_disponible}. Tarifa por hora: {self.tarifa_base}.")


# ============================================================
# SERVICIO DE ASESORIA ESPECIALIZADA
# ============================================================

class ServicioAsesoriaEspecializada(Servicio):
    """Servicio especializado de asesoria profesional."""

    # Inicializar los datos propios de la asesoria
    def __init__(self, id_servicio, nombre, tarifa_base, especialidad, modalidad):
        super().__init__(id_servicio, nombre, tarifa_base)

        # Validar la especialidad de la asesoria
        if not isinstance(especialidad, str) or not especialidad.strip():
            raise ServicioInvalidDataError("La especialidad no puede estar vacia.")

        # Validar la modalidad de atencion
        if not isinstance(modalidad, str) or not modalidad.strip():
            raise ServicioInvalidDataError("La modalidad no puede estar vacia.")

        self.__especialidad = especialidad.strip()
        self.__modalidad = modalidad.strip()

    # Consultar la especialidad y modalidad de la asesoria
    @property
    def especialidad(self):
        return self.__especialidad

    @property
    def modalidad(self):
        return self.__modalidad

    # Validar la duración de la asesoria
    def validar_parametros(self, duracion_horas):
        if isinstance(duracion_horas, bool) or not isinstance(duracion_horas, (int, float)) or not math.isfinite(duracion_horas) or duracion_horas <= 0:
            raise ServicioInvalidDataError("La duracion de la asesoria debe ser mayor que cero.")

        return True

    # Calcular el costo de la asesoria con impuestos y descuentos opcionales
    def calcular_costo(self, duracion_horas, impuesto=0, descuento=0):
        self.validar_parametros(duracion_horas)
        costo_base = self.tarifa_base * duracion_horas
        costo_total = aplicar_impuestos_descuentos(costo_base, impuesto, descuento)

        logger.info("Costo de asesoria calculado para el servicio %s.", self.id_servicio)
        return costo_total

    # Mostrar la descripción del servicio de asesoria
    def describir_servicio(self):
        return (f"Asesoria especializada: {self.nombre}. Especialidad: {self.__especialidad}. "
                f"Modalidad: {self.__modalidad}. Tarifa por hora: {self.tarifa_base}.")


# ============================================================
# PRUEBAS DE FUNCIONAMIENTO
# ============================================================

if __name__ == "__main__":

    # Configurar el registro de eventos y errores
    logging.basicConfig(filename="app.log", level=logging.INFO,
                        format="%(asctime)s - %(levelname)s - %(message)s", encoding="utf-8")

    print("\n===== SERVICIOS ESPECIALIZADOS =====")

    try:
        # Crear y probar el servicio de alquiler de equipos
        alquiler = ServicioAlquilerEquipos("SE001", "Alquiler de computadores", 25000, "Computador portatil", 5)

        print("\n--- ALQUILER DE EQUIPOS ---")
        print(alquiler.describir_servicio())
        print("Costo base:", alquiler.calcular_costo(4, 2))
        print("Costo con impuesto:", alquiler.calcular_costo(4, 2, impuesto=19))
        print("Costo con descuento:", alquiler.calcular_costo(4, 2, descuento=10))
        print("Costo con ambos:", alquiler.calcular_costo(4, 2, impuesto=19, descuento=10))

        # Crear y probar el servicio de asesoria especializada
        asesoria = ServicioAsesoriaEspecializada("SE002", "Asesoria empresarial", 80000, "Gestion empresarial", "Virtual")

        print("\n--- ASESORIA ESPECIALIZADA ---")
        print(asesoria.describir_servicio())
        print("Costo base:", asesoria.calcular_costo(2))
        print("Costo con impuesto:", asesoria.calcular_costo(2, impuesto=19))
        print("Costo con descuento:", asesoria.calcular_costo(2, descuento=15))
        print("Costo con ambos:", asesoria.calcular_costo(2, impuesto=19, descuento=15))

        # Comprobar el registro de alquiler y la actualizacion del inventario
        print("\n--- PRUEBA DE CONTROL DE INVENTARIO ---")
        alquiler.registrar_alquiler(2)
        print("Equipos disponibles:", alquiler.cantidad_disponible)
        print("Equipos alquilados:", alquiler.cantidad_alquilada)

        # Comprobar el registro de devolucion
        alquiler.registrar_devolucion(1)
        print("Equipos disponibles despues de la devolucion:", alquiler.cantidad_disponible)
        print("Equipos que siguen alquilados:", alquiler.cantidad_alquilada)

        # Comprobar el control de disponibilidad
        print("\n--- PRUEBA DE DISPONIBILIDAD ---")
        try:
            alquiler.validar_parametros(2, 7)
        except ServicioNoDisponibleError as error:
            print("Error controlado:", error)
            logger.error("Prueba de disponibilidad: %s", error)

        # Prueba de herencia y polimorfismo
        print("\n--- PRUEBA DE HERENCIA Y POLIMORFISMO ---")
        for servicio in [alquiler, asesoria]:
            print(isinstance(servicio, Servicio))
            print(servicio.describir_servicio())

        # Prueba de encapsulamiento
        print("\n--- PRUEBA DE ENCAPSULAMIENTO ---")
        try:
            print(alquiler.__cantidad_disponible)
        except AttributeError as error:
            print("Acceso privado bloqueado:", error)

        # Prueba de validacion de porcentajes
        print("\n--- PRUEBA DE VALIDACION DE PORCENTAJES ---")
        try:
            alquiler.calcular_costo(2, 1, impuesto=150)
        except ServicioInvalidDataError as error:
            print("Error controlado:", error)

    except ServicioError as error:
        logger.error("Error en las pruebas de servicios: %s", error)
        print("Error:", error)

    except Exception as error:
        logger.exception("Error inesperado: %s", error)
        print("Error inesperado:", error)

    else:
        print("\nTodas las pruebas finalizaron correctamente.")

    finally:
        print("\nFinalizo la ejecucion de las pruebas.")
