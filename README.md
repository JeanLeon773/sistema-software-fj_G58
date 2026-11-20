# Sistema Integral de Gestión de Clientes, Servicios y Reservas - Software FJ

Este proyecto corresponde a la **Fase 4 (Componente Práctico - Prácticas Simuladas)** del curso de **Programación (Código 213023)** de la Universidad Nacional Abierta y a Distancia (UNAD).

## Descripción del Proyecto

La aplicación es un sistema orientado a objetos desarrollado en Python sin el uso de motores de bases de datos. Permite la gestión de clientes, servicios (salas, equipos, asesorías) y reservas para la empresa **Software FJ**, incorporando un manejo robusto y avanzado de excepciones con registro en archivos de logs.

## Integrantes del Grupo 58

* Jean Pierre León - *Cliente y EntidadBase*
* Dublas José Coronado Aparicio - *Servicio Base y Salas*
* Christian David Coronado - *Servicios Especializados*
* Jesús Elías Rodríguez - *Módulo de Reservas*
* Miguel Ángel Villegas Correa - *Excepciones, Logs, Simulación y `main.py`*

## Estructura del Código

* `Cliente.py`: Clase `EntidadBase` y clase `Cliente` con validaciones y bloque `try/except/else/finally`.
* `Servicio.py`: Clase abstracta `Servicio` y derivada `ServicioReservaSalas` con validaciones de parámetros.
*  `ServiciosEspecializados.py`: Módulo de alquiler de equipos y asesorías con cálculo de costos, impuestos y descuentos.
* `Excepciones.py`: Módulo común con la jerarquía única de excepciones del sistema (clase `SoftwareFJError`).
* `LoggerConfig.py`: Configuración centralizada para registrar eventos en `app.log`.
* `main.py`: Ejecuta las 10 operaciones simuladas aplicando `try/except`, `else`, `finally` y `raise ... from ...`.
* `app.log`: Archivo de registro de eventos y excepciones generadas durante la ejecución.

## Instrucciones de Ejecución

1. Clonar este repositorio.
2. Asegurarse de tener instalado Python 3.x.
3. Ejecutar el archivo principal desde la terminal:
   ```bash
   python main.py
