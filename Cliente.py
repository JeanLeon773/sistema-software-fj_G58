from abc import ABC, abstractmethod

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


# 2. Clase Cliente con encapsulación y validaciones robustas
class Cliente(EntidadBase):
    def __init__(self, id_entidad: str, nombre: str, email: str, telefono: str):
        super().__init__(id_entidad)
        # Asignamos usando las propiedades para activar las validaciones automáticamente
        self.nombre = nombre
        self.email = email
        self.telefono = telefono

    # Validación y encapsulación para 'nombre'
    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not valor or not isinstance(valor, str) or len(valor.strip()) == 0:
            raise ValueError("El nombre del cliente no puede estar vacío o ser inválido.")
        self.__nombre = valor.strip()

    # Validación y encapsulación para 'email'
    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, valor: str):
        if not valor or "@" not in valor or "." not in valor:
            raise ValueError(f"El correo electrónico '{valor}' no tiene un formato válido.")
        self.__email = valor.strip()

    # Validación y encapsulación para 'telefono'
    @property
    def telefono(self) -> str:
        return self.__telefono

    @telefono.setter
    def telefono(self, valor: str):
        if not valor or not valor.isdigit() or len(valor) < 7:
            raise ValueError("El número de teléfono debe contener solo dígitos y tener al menos 7 caracteres.")
        self.__telefono = valor.strip()

    def obtener_detalles(self) -> str:
        return (f"Cliente [ID: {self.id_entidad}] | Nombre: {self.nombre} | "
                f"Email: {self.email} | Teléfono: {self.telefono}")