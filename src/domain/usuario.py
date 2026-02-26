"""Entidad Usuario del sistema TaskFlow."""

from datetime import datetime


class Usuario:
    """Representa un usuario del sistema TaskFlow.

    Attributes:
        username (str): Identificador único del usuario.
        email (str): Correo electrónico validado.
        nombre_completo (str | None): Nombre real del usuario.
        activo (bool): Estado de la cuenta.
        fecha_registro (datetime): Fecha de creación del usuario.
    """

    def __init__(
        self,
        username: str,
        email: str,
        nombre_completo: str | None = None,
    ) -> None:
        """Inicializa un nuevo usuario.

        Args:
            username: Identificador único (mínimo 3 caracteres alfanuméricos).
            email: Correo electrónico válido.
            nombre_completo: Nombre real del usuario (opcional).

        Raises:
            ValueError: Si el username o email no cumplen las validaciones.
        """
        self._validar_username(username)
        self._username = username

        self._email = ""
        self.email = email  

        self._nombre_completo = nombre_completo
        self._activo = True
        self._fecha_registro = datetime.now()

    # validaciones
    

    def _validar_username(self, username: str) -> None:
        """Valida que el username cumpla las reglas."""
        if len(username) < 3:
            raise ValueError("El username debe tener mínimo 3 caracteres.")
        if not username.isalnum():
            raise ValueError(
                "El username solo debe contener letras y números."
            )

    @property
    def username(self) -> str:
        """Retorna el username (solo lectura)."""
        return self._username

    @property
    def email(self) -> str:
        """Obtiene el email del usuario."""
        return self._email

    @email.setter
    def email(self, value: str) -> None:
        """Valida y asigna el email."""
        if "@" not in value or "." not in value:
            raise ValueError(
                "El email debe contener '@' y un punto."
            )
        self._email = value

    @property
    def activo(self) -> bool:
        """Indica si la cuenta está activa."""
        return self._activo

    @property
    def fecha_registro(self) -> datetime:
        """Fecha en la que el usuario fue registrado."""
        return self._fecha_registro
    
    #metodos

    def activar(self) -> None:
        """Activa la cuenta del usuario."""
        self._activo = True

    def desactivar(self) -> None:
        """Desactiva la cuenta del usuario."""
        self._activo = False

    def __str__(self) -> str:
        """Retorna representación amigable del usuario."""
        return f"@{self._username}"

    def __repr__(self) -> str:
        """Retorna representación técnica del usuario."""
        return f"Usuario('{self._username}', '{self._email}')"