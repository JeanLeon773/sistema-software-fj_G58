# Sistema Integral de Gestión de Clientes, Servicios y Reservas - Software FJ

Este proyecto corresponde a la **Fase 4 (Componente Práctico - Prácticas Simuladas)** del curso de **Programación (Código 213023)** de la Universidad Nacional Abierta y a Distancia (UNAD).

## Descripción del Proyecto
La aplicación es un sistema orientado a objetos desarrollado en Python sin el uso de motores de bases de datos. Permite la gestión de clientes, servicios (salas, equipos, asesorías) y reservas para la empresa **Software FJ**, incorporando un manejo robusto y avanzado de excepciones con registro en archivos de logs.

## Integrantes del Grupo
* Jean Pierre Leon - *Cliente y EntidadBase*
* Dublas Coronado - *Servicio Base y Salas*
* [Nombre Compañero 3] - *Equipos y Asesorías*
* [Nombre Compañero 4] - *Módulo de Reservas*
* Miguel Villegas Correa - *Excepciones, Logs y Simulación*

## Estructura del Código
* `Cliente.py`: Clase `EntidadBase` y clase `Cliente` con validaciones y bloque `try/except/else/finally`.
* `Servicio.py`: Clase abstracta `Servicio` y derivada `ServicioReservaSalas` con validaciones de parámetros.
* `Excepciones.py`: Módulo común con la jerarquía única de excepciones del sistema (clase `SoftwareFJError`).
* `LoggerConfig.py`: Configuración centralizada para registrar eventos en `app.log`.
* `Simulacion.py`: Ejecuta las 10 operaciones simuladas aplicando `try/except`, `else`, `finally` y `raise ... from ...`.

## Instrucciones de Ejecución
1. Clonar o descargar este repositorio.
2. Asegurarse de tener instalado Python 3.x.
3. Ejecutar el archivo principal o módulos de prueba desde la terminal:
   ```bash
   python cliente.py 
