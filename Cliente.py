import logging
from abc import ABC, abstractmethod

# Configuración del registro de eventos (Logs)
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

# Excepción personalizada para validación de datos de clientes
class ClienteInvalidDataError(Exception):
    """Excepción lanzada cuando los datos del cliente no cumplen los requerimientos."""
    pass

# 1. Clase abstracta que representa entidades generales del sistema
class EntidadBase(ABC):
    def __init__(self, id_entidad: str):
        self._id_entidad = id_entidad

    @property
    def id_entidad(self) -> str:
        return self._id_entidad

    @abstractmethod
    def obtener_detalles(self) -> str:
        """Método abstracto que implementarán las clases hijas."""
        pass

# 2. Clase Cliente con encapsulación y validaciones estrictas
class Cliente(EntidadBase):
    def __init__(self, id_entidad: str, nombre: str, email: str, telefono: str):
        super().__init__(id_entidad)
        self.nombre = nombre
        self.email = email
        self.telefono = telefono

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not valor or not isinstance(valor, str) or len(valor.strip()) == 0:
            raise ClienteInvalidDataError("El nombre del cliente no puede estar vacío.")
        self.__nombre = valor.strip()

    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, valor: str):
        if not valor or "@" not in valor or "." not in valor:
            raise ClienteInvalidDataError(f"El correo '{valor}' no tiene un formato válido.")
        self.__email = valor.strip()

    @property
    def telefono(self) -> str:
        return self.__telefono

    @telefono.setter
    def telefono(self, valor: str):
        if not valor or not valor.isdigit() or len(valor) < 7:
            raise ClienteInvalidDataError("El teléfono debe contener solo números (mínimo 7 dígitos).")
        self.__telefono = valor.strip()

    def obtener_detalles(self) -> str:
        return f"Cliente [ID: {self.id_entidad}] | Nombre: {self.nombre} | Email: {self.email} | Teléfono: {self.telefono}"


# 3. Función de creación segura con try / except / else / finally y Logs
def registrar_cliente_seguro(id_entidad: str, nombre: str, email: str, telefono: str):
    """Función para intentar registrar un cliente manejando excepciones sin detener el programa."""
    cliente_creado = None
    try:
        # Intento de instanciación que puede generar excepciones
        cliente_creado = Cliente(id_entidad, nombre, email, telefono)
    except ClienteInvalidDataError as e:
        # Manejo específico de error de validación
        mensaje_error = f"[ERROR DE VALIDACIÓN] No se pudo crear cliente {id_entidad}: {e}"
        print(mensaje_error)
        logging.error(mensaje_error)
    except Exception as e:
        # Manejo de cualquier otro error no contemplado
        mensaje_error = f"[ERROR INESPERADO] Error procesando cliente {id_entidad}: {e}"
        print(mensaje_error)
        logging.error(mensaje_error)
    else:
        # Se ejecuta SOLO si NO hubo errores
        mensaje_exito = f"[ÉXITO] Cliente registrado correctamente: {cliente_creado.obtener_detalles()}"
        print(mensaje_exito)
        logging.info(mensaje_exito)
    finally:
        # Se ejecuta SIEMPRE para asegurar la estabilidad
        print(f"-> Operación de registro finalizada para ID: {id_entidad}\n")
        logging.info(f"Finalizado procesamiento de cliente ID: {id_entidad}")
    
    return cliente_creado

# Ejemplo de prueba local para verificar funcionamiento
if __name__ == "__main__":
    print("--- PRUEBAS DE REGISTRO DE CLIENTES ---\n")
    # Caso exitoso
    registrar_cliente_seguro("CLI01", "Juan Pérez", "juan@mail.com", "3001234567")
    # Caso con error de validación (email inválido)
    registrar_cliente_seguro("CLI02", "Maria Gomez", "correo_invalido", "3001234567")        
