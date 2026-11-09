# -*- coding: utf-8 -*-
"""
PROYECTO FASE 4 - SOFTWARE FJ
ESTUDIANTE 5: SIMULACIÓN DE 10 OPERACIONES (Miguel Villegas Correa)
"""

import Cliente as mod_cliente
import Servicio as mod_servicio
from LoggerConfig import configurar_logs

# Se activa el log
logger = configurar_logs("app.log")

from Excepciones import (
    SoftwareFJError, ClienteInvalidDataError, ServicioError,
    ServicioInvalidDataError, ServicioNoDisponibleError,
    ParametrosFaltantesError, OperacionNoPermitidaError,
    ReservaIncorrectaError, CalculoInconsistenteError
)

# Enlace dinámico para que el código funcione aunque los compañeros no hayan actualizado
mod_cliente.ClienteInvalidDataError = ClienteInvalidDataError
mod_servicio.ServicioError = ServicioError
mod_servicio.ServicioInvalidDataError = ServicioInvalidDataError
mod_servicio.ServicioNoDisponibleError = ServicioNoDisponibleError

EntidadBase = mod_cliente.EntidadBase
Cliente = mod_cliente.Cliente
Servicio = mod_servicio.Servicio
ServicioReservaSalas = mod_servicio.ServicioReservaSalas

# ==============================================================================
# CLASES COMPLEMENTARIAS PARA COMPLETAR EL SISTEMA
# ==============================================================================

class ServicioAlquilerEquipos(Servicio):
    def __init__(self, id_servicio: str, nombre: str, tarifa_base: float, stock: int):
        super().__init__(id_servicio, nombre, tarifa_base)
        if isinstance(stock, bool) or not isinstance(stock, int) or stock <= 0:
            raise ServicioInvalidDataError("El stock debe ser un entero mayor que cero.")
        self.__stock = stock

    def validar_parametros(self, duracion_horas: float, cantidad: int = 1, **kwargs) -> bool:
        if isinstance(duracion_horas, bool) or not isinstance(duracion_horas, (int, float)) or duracion_horas <= 0:
            raise ServicioInvalidDataError("La duración debe ser mayor que cero.")
        if cantidad > self.__stock:
            raise ServicioNoDisponibleError(f"Solo hay {self.__stock} equipos disponibles.")
        return True

    def calcular_costo(self, duracion_horas: float, cantidad: int = 1, **kwargs) -> float:
        self.validar_parametros(duracion_horas, cantidad)
        return self.tarifa_base * duracion_horas * cantidad

    def describir_servicio(self) -> str:
        return f"Alquiler de equipos | ID: {self.id_servicio} | Nombre: {self.nombre} | Stock: {self.__stock}"

class ServicioAsesoria(Servicio):
    def __init__(self, id_servicio: str, nombre: str, tarifa_base: float, especialidad: str):
        super().__init__(id_servicio, nombre, tarifa_base)
        if not isinstance(especialidad, str) or not especialidad.strip():
            raise ParametrosFaltantesError("especialidad")
        self.__especialidad = especialidad.strip()

    def validar_parametros(self, duracion_horas: float, **kwargs) -> bool:
        if isinstance(duracion_horas, bool) or not isinstance(duracion_horas, (int, float)) or duracion_horas <= 0:
            raise ServicioInvalidDataError("Las horas deben ser mayores a cero.")
        return True

    def calcular_costo(self, duracion_horas: float, **kwargs) -> float:
        self.validar_parametros(duracion_horas)
        return self.tarifa_base * duracion_horas * 1.20

    def describir_servicio(self) -> str:
        return f"Asesoría | ID: {self.id_servicio} | Nombre: {self.nombre} | Especialidad: {self.__especialidad}"

class Reserva(EntidadBase):
    def __init__(self, id_reserva: str, cliente: Cliente, servicio: Servicio, duracion_horas: float, **parametros):
        if not isinstance(id_reserva, str) or not id_reserva.strip():
            raise ParametrosFaltantesError("id_reserva")
        super().__init__(id_reserva.strip())
        if not isinstance(cliente, Cliente):
            raise ReservaIncorrectaError("Cliente inválido.")
        if not isinstance(servicio, Servicio):
            raise ReservaIncorrectaError("Servicio inválido.")
        if isinstance(duracion_horas, bool) or not isinstance(duracion_horas, (int, float)) or duracion_horas <= 0:
            raise ReservaIncorrectaError(f"Duración inválida ({duracion_horas}h).")
        
        self.cliente = cliente
        self.servicio = servicio
        self.duracion_horas = float(duracion_horas)
        self.parametros = parametros
        self.estado = "PENDIENTE"
        self.costo_total = 0.0

    def calcular_total_sobrecargado(self, impuesto: float = 0.0, descuento: float = 0.0) -> float:
        if descuento < 0 or descuento > 100:
            raise CalculoInconsistenteError(f"Descuento inválido del {descuento}%.")
        if impuesto < 0:
            raise CalculoInconsistenteError(f"Impuesto negativo ({impuesto}%).")
        
        subtotal = self.servicio.calcular_costo(self.duracion_horas, **self.parametros)
        total = (subtotal * (1 - (descuento / 100.0))) * (1 + (impuesto / 100.0))
        return round(total, 2)

    def confirmar(self, impuesto: float = 19.0, descuento: float = 0.0):
        if self.estado != "PENDIENTE":
            raise OperacionNoPermitidaError("confirmar", f"La reserva ya está {self.estado}.")
        self.costo_total = self.calcular_total_sobrecargado(impuesto, descuento)
        self.estado = "CONFIRMADA"

    def cancelar(self):
        if self.estado == "CANCELADA":
            raise OperacionNoPermitidaError("cancelar", "La reserva ya fue cancelada antes.")
        self.estado = "CANCELADA"

    def obtener_detalles(self) -> str:
        return f"Reserva [{self.id_entidad}] | Cliente: {self.cliente.nombre} | Servicio: {self.servicio.nombre} | Total: ${self.costo_total:,.2f}"

# ==============================================================================
# EJECUCIÓN DE LAS 10 OPERACIONES SIMULADAS
# ==============================================================================

def ejecutar_simulacion():
    clientes, servicios, reservas = [], [], []
    logger.info("=== INICIO DE LA SIMULACIÓN DE 10 OPERACIONES - SOFTWARE FJ ===")

    # OP 1: Registro exitoso (try/except/else)
    try:
        c1 = Cliente("CLI-01", "Miguel Villegas Correa", "miguel.villegas@unad.edu.co", "3001234567")
    except SoftwareFJError as e:
        logger.error(f"[OP-01 ERROR] {e}")
    else:
        clientes.append(c1)
        logger.info(f"[OP-01 ÉXITO] {c1.obtener_detalles()}")

    # OP 2: Registro fallido por correo inválido (try/except/finally)
    try:
        c2 = Cliente("CLI-02", "Pedro Pérez", "correo_sin_arroba", "3109876543")
    except ClienteInvalidDataError as e:
        logger.error(f"[OP-02 CONTROLADA] {e}")
    finally:
        logger.info(f"[OP-02 FINALLY] Total clientes registrados: {len(clientes)}")

    # OP 3: Creación exitosa de los 3 Servicios
    try:
        s_sala = ServicioReservaSalas("SAL-01", "Sala Principal", 50000, 12, {"proyector": 20000})
        s_equipo = ServicioAlquilerEquipos("EQU-01", "Portátil i7", 25000, stock=8)
        s_asesoria = ServicioAsesoria("ASE-01", "Asesoría Python", 90000, especialidad="Backend")
    except SoftwareFJError as e:
        logger.error(f"[OP-03 ERROR] {e}")
    else:
        servicios.extend([s_sala, s_equipo, s_asesoria])
        logger.info("[OP-03 ÉXITO] 3 servicios creados correctamente.")

    # OP 4: Creación inválida con Encadenamiento (raise...from)
    try:
        try:
            tarifa_erronea = float("TEXTO_INVALIDO")
            ServicioReservaSalas("SAL-02", "Sala Norte", tarifa_erronea, 10)
        except ValueError as causa:
            raise ServicioInvalidDataError("La tarifa ingresada no es un número válido.") from causa
    except ServicioInvalidDataError as e:
        logger.error(f"[OP-04 CONTROLADA - ENCADENAMIENTO] {e} | Causa raíz: {e.__cause__}")

    # OP 5: Creación inválida por Parámetro Faltante
    try:
        ServicioAsesoria("ASE-02", "Asesoría Cloud", 80000, especialidad="")
    except ParametrosFaltantesError as e:
        logger.error(f"[OP-05 CONTROLADA] {e}")

    # OP 6: Reserva exitosa (IVA 19% y Descuento 10%)
    try:
        r1 = Reserva("RES-01", clientes[0], servicios[0], duracion_horas=3, numero_personas=8, recursos_solicitados=["proyector"])
        r1.confirmar(impuesto=19.0, descuento=10.0)
    except SoftwareFJError as e:
        logger.error(f"[OP-06 ERROR] {e}")
    else:
        reservas.append(r1)
        logger.info(f"[OP-06 ÉXITO] {r1.obtener_detalles()}")

    # OP 7: Reserva fallida (Servicio No Disponible por exceso de personas)
    try:
        r2 = Reserva("RES-02", clientes[0], servicios[0], duracion_horas=2, numero_personas=25)
        r2.confirmar()
    except ServicioNoDisponibleError as e:
        logger.error(f"[OP-07 CONTROLADA] {e}")

    # OP 8: Reserva fallida (Duración Negativa)
    try:
        Reserva("RES-03", clientes[0], servicios[1], duracion_horas=-4, cantidad=2)
    except ReservaIncorrectaError as e:
        logger.error(f"[OP-08 CONTROLADA] {e}")

    # OP 9: Reserva fallida (Descuento Inconsistente > 100%)
    try:
        r4 = Reserva("RES-04", clientes[0], servicios[2], duracion_horas=2)
        r4.confirmar(impuesto=19.0, descuento=150.0)
    except CalculoInconsistenteError as e:
        logger.error(f"[OP-09 CONTROLADA] {e}")

    # OP 10: Doble cancelación bloqueada
    try:
        r1.cancelar()
        logger.info(f"[OP-10A ÉXITO] Reserva {r1.id_entidad} cancelada.")
        r1.cancelar() # Intento de cancelar por segunda vez
    except OperacionNoPermitidaError as e:
        logger.error(f"[OP-10B CONTROLADA] {e}")
    finally:
        logger.info("=== FIN DE LA SIMULACIÓN - SISTEMA ESTABLE ===")

if __name__ == "__main__":
    ejecutar_simulacion()