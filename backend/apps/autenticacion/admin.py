"""
apps/autenticacion/admin.py — Registro de modelos de autenticación en Django Admin.

Registra: Usuario, PadreTutor.
Sobreescribe UserAdmin para trabajar con nuestros campos personalizados
(email en lugar de username, activo en lugar de is_active, etc.)
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import PadreTutor, Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    """
    Admin para Usuario personalizado.
    Adapta UserAdmin estándar a nuestros campos en español.
    """

    model = Usuario
    list_display = (
        "email", "nombre_completo", "rol", "agencia",
        "email_verificado", "activo", "is_staff", "created_at",
    )
    list_filter = ("rol", "email_verificado", "activo", "is_staff", "agencia")
    search_fields = ("email", "nombre", "apellidos")
    ordering = ("email",)
    readonly_fields = ("id", "created_at", "ultimo_login")

    # Sobreescribir los fieldsets de UserAdmin (que usa 'username') con los nuestros
    fieldsets = (
        (
            "Credenciales",
            {
                "fields": ("id", "email", "password"),
            },
        ),
        (
            "Datos personales",
            {
                "fields": ("nombre", "apellidos", "telefono"),
            },
        ),
        (
            "Rol y agencia",
            {
                "fields": ("rol", "agencia"),
            },
        ),
        (
            "Estado de la cuenta",
            {
                "fields": ("activo", "email_verificado"),
            },
        ),
        (
            "Permisos de administración",
            {
                "classes": ("collapse",),
                "fields": ("is_staff", "is_superuser", "groups", "user_permissions"),
            },
        ),
        (
            "Auditoría",
            {
                "fields": ("created_at", "ultimo_login"),
            },
        ),
    )

    # Fieldsets para la pantalla de creación de usuario en el admin
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email", "nombre", "apellidos", "rol",
                    "agencia", "password1", "password2",
                ),
            },
        ),
    )

    def nombre_completo(self, obj: Usuario) -> str:
        return obj.nombre_completo
    nombre_completo.short_description = "Nombre completo"  # type: ignore[attr-defined]


@admin.register(PadreTutor)
class PadreTutorAdmin(admin.ModelAdmin):
    """Admin para PadreTutor. Acceso rápido al usuario vinculado."""

    list_display = ("usuario", "relacion_alumno", "dni", "created_at")
    list_filter = ("relacion_alumno",)
    search_fields = (
        "usuario__email",
        "usuario__nombre",
        "usuario__apellidos",
        "dni",
    )
    readonly_fields = ("id", "created_at")
    raw_id_fields = ("usuario",)

    fieldsets = (
        (
            "Perfil del tutor",
            {
                "fields": ("id", "usuario", "relacion_alumno", "dni"),
            },
        ),
        (
            "Auditoría",
            {
                "fields": ("created_at",),
            },
        ),
    )
