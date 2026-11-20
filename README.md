# Sistema Integral de Gestión de Clientes, Servicios y Reservas - Software FJ

Este proyecto corresponde a la **Fase 4 (Componente Práctico - Prácticas Simuladas)** del curso de **Programación (Código 213023)** de la Universidad Nacional Abierta y a Distancia (UNAD).

## Descripción del Proyecto
La aplicación es un sistema orientado a objetos desarrollado en Python sin el uso de motores de bases de datos. Permite la gestión de clientes, servicios (salas, equipos, asesorías) y reservas para la empresa **Software FJ**, incorporando un manejo robusto y avanzado de excepciones con registro en archivos de logs.

## Integrantes del Grupo
* Jean Pierre Leon - *Cliente y EntidadBase*
* Dublas Coronado - *Servicio Base y Salas*
* Christian Coronado - *Equipos y Asesorías*
* [Nombre Compañero 4] - *Módulo de Reservas*
* [Nombre Compañero 5] - *Excepciones, Logs y Simulación*

## Estructura del Código
* `cliente.py`: Contiene la clase abstracta `EntidadBase`, la clase `Cliente` con validaciones y la función `registrar_cliente_seguro` con manejo de excepciones (`try/except/else/finally`) y almacenamiento de registros en `app.log`.

## Instrucciones de Ejecución
1. Clonar o descargar este repositorio.
2. Asegurarse de tener instalado Python 3.x.
3. Ejecutar el archivo principal o módulos de prueba desde la terminal:
   ```bash
   python cliente.py 
