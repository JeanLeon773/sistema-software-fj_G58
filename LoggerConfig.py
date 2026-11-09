# -*- coding: utf-8 -*-
"""
PROYECTO FASE 4 - SOFTWARE FJ
ESTUDIANTE 5: CONFIGURACIÓN DEL ARCHIVO DE LOGS (Miguel Villegas Correa)
"""

import logging
import sys

def configurar_logs(nombre_archivo: str = "app.log") -> logging.Logger:
    """Configura el guardado automático de eventos y errores en 'app.log'."""
    formato = "%(asctime)s - %(levelname)s - %(message)s"

    manejador_archivo = logging.FileHandler(nombre_archivo, mode="a", encoding="utf-8")
    manejador_consola = logging.StreamHandler(sys.stdout)

    logging.basicConfig(
        level=logging.INFO,
        format=formato,
        handlers=[manejador_archivo, manejador_consola],
        force=True
    )

    return logging.getLogger("SoftwareFJ")