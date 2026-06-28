"""
apps/agencias/admin.py — Registro de Agencia en el Django Admin.
"""

from django.contrib import admin

from .models import Agencia


@admin.register(Agencia)
class AgenciaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "slug", "email_contacto", "telefono", "activa", "created_at")
    list_filter = ("activa",)
    search_fields = ("nombre", "slug", "email_contacto")
    readonly_fields = ("id", "created_at")
    prepopulated_fields = {"slug": ("nombre",)}
    fieldsets = (
        (
            "Información principal",
            {
                "fields": ("id", "nombre", "slug", "logo", "activa"),
            },
        ),
        (
            "Contacto",
            {
                "fields": ("email_contacto", "telefono"),
            },
        ),
        (
            "Legal",
            {
                "fields": ("licencia_agencia",),
            },
        ),
        (
            "Auditoría",
            {
                "fields": ("created_at",),
            },
        ),
    )
