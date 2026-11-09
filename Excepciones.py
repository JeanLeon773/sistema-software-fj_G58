# -*- coding: utf-8 -*-
"""
PROYECTO FASE 4 - SOFTWARE FJ
ESTUDIANTE 5: MÓDULO COMÚN DE EXCEPCIONES (Miguel Villegas Correa)
"""

# Clase base única exigida por el tutor para todo el sistema
class SoftwareFJError(Exception):
    """Excepción general del sistema Software FJ."""
    def __init__(self, mensaje: str = "Error en el sistema Software FJ."):
        super().__init__(mensaje)
        self.mensaje = mensaje

# Excepciones de Clientes y Servicios unificadas a la base
class ClienteInvalidDataError(SoftwareFJError):
    pass

class ServicioError(SoftwareFJError):
    pass

class ServicioInvalidDataError(ServicioError):
    pass

class ServicioNoDisponibleError(ServicioError):
    pass

# Excepciones específicas de la simulación y reservas
class ParametrosFaltantesError(SoftwareFJError):
    def __init__(self, parametro: str):
        super().__init__(f"Parámetro obligatorio faltante: '{parametro}'.")

class OperacionNoPermitidaError(SoftwareFJError):
    def __init__(self, operacion: str, motivo: str):
        super().__init__(f"Operación no permitida en '{operacion}': {motivo}.")

class ReservaIncorrectaError(SoftwareFJError):
    def __init__(self, detalle: str):
        super().__init__(f"Intento de reserva incorrecto: {detalle}.")

class CalculoInconsistenteError(SoftwareFJError):
    def __init__(self, detalle: str):
        super().__init__(f"Cálculo de costos inconsistente: {detalle}.")