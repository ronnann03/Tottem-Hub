"""
apps/autenticacion/managers.py — Manager personalizado para el modelo Usuario.

Django requiere sobreescribir BaseUserManager cuando USERNAME_FIELD != 'username'
para que los comandos create_user y create_superuser funcionen correctamente.
"""

from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    """
    Manager para Usuario con email como identificador único de autenticación.
    Reemplaza el manager default que usa 'username'.
    """

    def create_user(  # type: ignore[override]
        self, email: str, password: str | None = None, **extra_fields
    ) -> "Usuario":  # type: ignore[name-defined]  # noqa: F821
        """
        Crea y guarda un usuario con email y contraseña.

        El email se normaliza (parte del dominio en minúsculas).
        La contraseña se hashea con bcrypt vía set_password() — nunca texto plano.
        """
        if not email:
            raise ValueError("El email es obligatorio")

        email = self.normalize_email(email)

        # Valores por defecto seguros para usuarios regulares
        extra_fields.setdefault("activo", True)
        extra_fields.setdefault("email_verificado", False)  # Requiere verificación (BR-AUTH-01)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Hashea con bcrypt — NUNCA almacenar en texto plano
        user.save(using=self._db)
        return user

    def create_superuser(  # type: ignore[override]
        self, email: str, password: str, **extra_fields
    ) -> "Usuario":  # type: ignore[name-defined]  # noqa: F821
        """
        Crea y guarda un superusuario con acceso completo al Admin.

        Los superusuarios tienen email_verificado=True por defecto
        ya que son creados directamente por consola, no por el flujo de registro.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        # Superusuarios no necesitan verificar email
        extra_fields.setdefault("email_verificado", True)
        extra_fields.setdefault("activo", True)

        # Validaciones de integridad
        if extra_fields.get("is_staff") is not True:
            raise ValueError("El superusuario debe tener is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("El superusuario debe tener is_superuser=True.")

        # rol por defecto para superusuario si no se especifica
        extra_fields.setdefault("rol", "agente")

        return self.create_user(email, password, **extra_fields)
