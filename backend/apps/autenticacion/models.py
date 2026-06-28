"""
apps/autenticacion/models.py — Modelos de autenticación y perfiles de usuario.

Modelos definidos aquí:
  - RolUsuario (TextChoices)
  - RelacionAlumno (TextChoices)
  - Usuario (AbstractBaseUser)
  - PadreTutor (perfil extendido de Usuario con rol='padre')

Decisiones de diseño documentadas:

  I-01: Campo 'activo' (en lugar de 'is_active') con ACTIVE_FIELD = 'activo'
        → Mantiene naming en español de DATABASE.md. Compatible con Django 4.2.

  I-02: Campo 'ultimo_login' sobreescribe 'last_login' de AbstractBaseUser
        → Se gestiona manualmente en el endpoint de login (TASK-010).
        → Naming en español consistente con DATABASE.md.

  I-03: Rol 'agente' no disponible en /auth/registro/ — restricción en serializer
        → El modelo acepta cualquier rol válido; la restricción es de endpoint.

  I-04: PadreTutor.relacion_alumno es blank=True (D-09)
        → API.md /auth/registro/ no incluye relacion_alumno en el payload.
        → El campo se completa en el wizard de inscripción (TASK-009).
        → Decisión reversible: cambiar a blank=False si se extiende el registro.

DATABASE.md §Usuario §PadreTutor
AI_CONTEXT.md §Invariantes #8 (login bloqueado si email_verificado=False)
"""

import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from apps.agencias.models import Agencia

from .managers import CustomUserManager


class RolUsuario(models.TextChoices):
    """
    Roles del sistema. Define el portal al que accede el usuario y sus permisos.
    DATABASE.md §Enumeraciones
    """
    PADRE = "padre", "Padre / Tutor"
    ALUMNO = "alumno", "Alumno"
    AGENTE = "agente", "Agente de viajes"
    MECENAS = "mecenas", "Mecenas"


class RelacionAlumno(models.TextChoices):
    """
    Tipo de vínculo del tutor con el alumno. Usado en PadreTutor.relacion_alumno.
    DATABASE.md §Enumeraciones
    """
    PADRE = "padre", "Padre"
    MADRE = "madre", "Madre"
    TUTOR = "tutor_legal", "Tutor legal"


class Usuario(AbstractBaseUser, PermissionsMixin):
    """
    Modelo de usuario personalizado. Usa email como campo de autenticación.

    Todos los actores del sistema (padre, alumno, agente, mecenas) comparten
    este modelo base. Los perfiles extendidos (PadreTutor, Mecenas) añaden
    campos específicos via OneToOneField.

    INVARIANTE #8: Login bloqueado si email_verificado=False (BR-AUTH-01).
    INVARIANTE #12: JWT en cookies httpOnly — nunca en localStorage (gestionado por el Gateway).
    """

    # ─────────────────────────────────────────────────────────────
    # IDENTIFICACIÓN
    # ─────────────────────────────────────────────────────────────

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="ID",
    )
    email = models.EmailField(
        unique=True,
        verbose_name="Email",
        help_text="Dirección de email — usada como login. Única en todo el sistema.",
    )

    # ─────────────────────────────────────────────────────────────
    # DATOS PERSONALES
    # ─────────────────────────────────────────────────────────────

    nombre = models.CharField(
        max_length=100,
        verbose_name="Nombre",
    )
    apellidos = models.CharField(
        max_length=150,
        verbose_name="Apellidos",
    )
    telefono = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Teléfono",
    )

    # ─────────────────────────────────────────────────────────────
    # ROL Y AGENCIA (MULTI-TENANT)
    # ─────────────────────────────────────────────────────────────

    rol = models.CharField(
        max_length=20,
        choices=RolUsuario.choices,
        verbose_name="Rol",
        help_text="Determina el portal al que accede y sus permisos en el sistema.",
    )
    agencia = models.ForeignKey(
        Agencia,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="usuarios",
        verbose_name="Agencia",
        help_text=(
            "Agencia a la que pertenece el usuario. "
            "Obligatoria para agentes. Nullable para padres, alumnos y mecenas."
        ),
    )

    # ─────────────────────────────────────────────────────────────
    # ESTADO DE LA CUENTA
    # ─────────────────────────────────────────────────────────────

    email_verificado = models.BooleanField(
        default=False,
        verbose_name="Email verificado",
        help_text=(
            "Invariante #8: el login queda bloqueado hasta que este campo sea True. "
            "Se activa mediante el enlace de verificación enviado al registrarse."
        ),
    )
    # Decisión I-01: 'activo' en lugar de 'is_active' para mantener naming en español.
    # Django 4.0+ soporta ACTIVE_FIELD para indicar qué campo representa is_active.
    activo = models.BooleanField(
        default=True,
        verbose_name="Activo",
        help_text="Cuenta activa. Desactivar para suspender acceso sin eliminar el registro.",
    )

    # ─────────────────────────────────────────────────────────────
    # CAMPOS DE DJANGO ADMIN
    # ─────────────────────────────────────────────────────────────

    is_staff = models.BooleanField(
        default=False,
        verbose_name="Es staff",
        help_text="Permite acceso al sitio de administración Django.",
    )
    # is_superuser es heredado de PermissionsMixin — no se redeclara aquí

    # ─────────────────────────────────────────────────────────────
    # TIMESTAMPS
    # ─────────────────────────────────────────────────────────────

    # Decisión I-02: sobreescribe last_login de AbstractBaseUser con naming en español.
    # Se actualiza manualmente en el endpoint de login (TASK-010).
    ultimo_login = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Último login",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación",
    )

    # ─────────────────────────────────────────────────────────────
    # CONFIGURACIÓN DE AUTENTICACIÓN
    # ─────────────────────────────────────────────────────────────

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    # Campos solicitados por createsuperuser además de email y password
    REQUIRED_FIELDS = ["nombre", "apellidos", "rol"]

    # Decisión I-01: indicar a Django que 'activo' es el campo is_active equivalente.
    # Esto permite que el sistema de autenticación de Django funcione correctamente
    # sin renombrar el campo a 'is_active'.
    ACTIVE_FIELD = "activo"

    # AbstractBaseUser usa last_login internamente; lo mapeamos a nuestro campo.
    # Esto evita que Django cree last_login Y ultimo_login como campos separados.
    last_login = property(
        lambda self: self.ultimo_login,
        lambda self, value: setattr(self, "ultimo_login", value),
    )

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        indexes = [
            models.Index(fields=["agencia", "rol"], name="usuario_agencia_rol_idx"),
            models.Index(fields=["email"], name="usuario_email_idx"),
        ]

    def __str__(self) -> str:
        return f"{self.email} ({self.get_rol_display()})"

    # ─────────────────────────────────────────────────────────────
    # PROPIEDADES COMPUTADAS
    # ─────────────────────────────────────────────────────────────

    @property
    def nombre_completo(self) -> str:
        """Retorna nombre y apellidos concatenados. DATABASE.md §Usuario."""
        return f"{self.nombre} {self.apellidos}"

    # ─────────────────────────────────────────────────────────────
    # PROPIEDADES REQUERIDAS POR DJANGO (is_active)
    # ─────────────────────────────────────────────────────────────

    @property
    def is_active(self) -> bool:
        """
        Django necesita is_active para el sistema de autenticación.
        Lo mapeamos al campo 'activo' en español para mantener el naming de DATABASE.md.
        """
        return self.activo

    @is_active.setter
    def is_active(self, value: bool) -> None:
        self.activo = value


class PadreTutor(models.Model):
    """
    Perfil extendido para usuarios con rol='padre'.

    Extiende Usuario via OneToOneField. Permite que un mismo tutor gestione
    múltiples alumnos (relación M:N definida en Alumno.tutores — TASK-008).

    Una inscripción referencia a PadreTutor directamente (FK), registrando
    qué tutor es el responsable de esa inscripción específica.

    DATABASE.md §PadreTutor
    Decisión I-04: relacion_alumno es blank=True — ver docstring del módulo.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="ID",
    )
    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name="perfil_tutor",
        verbose_name="Usuario",
        help_text="Cuenta de usuario asociada. Solo debe usarse con rol='padre'.",
    )
    dni = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="DNI",
        help_text="Documento de identidad del tutor.",
    )
    relacion_alumno = models.CharField(
        max_length=20,
        choices=RelacionAlumno.choices,
        blank=True,
        verbose_name="Relación con el alumno",
        help_text=(
            "Vínculo del tutor con el alumno: padre, madre o tutor legal. "
            "Puede completarse en el wizard de inscripción (D-09)."
        ),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación",
    )

    class Meta:
        verbose_name = "Padre / Tutor"
        verbose_name_plural = "Padres / Tutores"

    def __str__(self) -> str:
        relacion = self.get_relacion_alumno_display() or "sin especificar"
        return f"{self.usuario.nombre_completo} ({relacion})"
