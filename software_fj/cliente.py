# cliente.py
# Clase Cliente: datos personales encapsulados y validaciones estrictas.

import re

from .entidad import Entidad
from .excepciones import ClienteInvalidoError, ParametroFaltanteError

# Expresiones regulares usadas en las validaciones
PATRON_CORREO = re.compile(r"^[\w.+-]+@[\w-]+\.[\w.-]+$")
PATRON_DOCUMENTO = re.compile(r"^\d{6,10}$")        # cédula: de 6 a 10 dígitos
PATRON_TELEFONO = re.compile(r"^3\d{9}$")           # celular colombiano: 10 dígitos que empiezan en 3


class Cliente(Entidad):
    """Cliente de Software FJ. Sus datos solo se cambian a través de propiedades validadas."""

    def __init__(self, nombre, documento, correo, telefono=None):
        super().__init__("CLI")
        # Al asignar con "self.nombre = ..." se ejecuta el setter, que valida el dato
        self.nombre = nombre
        self.documento = documento
        self.correo = correo
        self.telefono = telefono
        self._asignar_id()  # solo si todos los datos fueron válidos

    # ---------- nombre ----------
    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        if valor is None or str(valor).strip() == "":
            raise ParametroFaltanteError("nombre")
        valor = str(valor).strip()
        if len(valor) < 3 or any(c.isdigit() for c in valor):
            raise ClienteInvalidoError(f"Nombre inválido: '{valor}' (mínimo 3 letras y sin números)")
        self.__nombre = valor.title()

    # ---------- documento ----------
    @property
    def documento(self):
        return self.__documento

    @documento.setter
    def documento(self, valor):
        if valor is None or str(valor).strip() == "":
            raise ParametroFaltanteError("documento")
        valor = str(valor).strip()
        if not PATRON_DOCUMENTO.match(valor):
            raise ClienteInvalidoError(f"Documento inválido: '{valor}' (debe tener de 6 a 10 dígitos)")
        self.__documento = valor

    # ---------- correo ----------
    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, valor):
        if valor is None or str(valor).strip() == "":
            raise ParametroFaltanteError("correo")
        valor = str(valor).strip().lower()
        if not PATRON_CORREO.match(valor):
            raise ClienteInvalidoError(f"Correo inválido: '{valor}'")
        self.__correo = valor

    # ---------- teléfono (opcional) ----------
    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        if valor is not None and not PATRON_TELEFONO.match(str(valor)):
            raise ClienteInvalidoError(f"Teléfono inválido: '{valor}' (10 dígitos que empiecen en 3)")
        self.__telefono = valor

    def validar(self):
        """Vuelve a pasar todos los datos por sus validaciones."""
        self.nombre = self.nombre
        self.documento = self.documento
        self.correo = self.correo
        self.telefono = self.telefono
        return True

    def describir(self):
        # El documento se muestra enmascarado para proteger el dato personal
        oculto = "*" * (len(self.documento) - 3) + self.documento[-3:]
        return f"{self.id} | {self.nombre} | Doc: {oculto} | {self.correo}"
