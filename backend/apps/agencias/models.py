"""
apps/agencias/models.py — Modelo Agencia (tenant raíz del sistema).

Agencia es el tenant raíz de Tottem Hub. En Fase 1 opera un único tenant:
Totem Travel (slug='totem'). En Fase 2+ se añaden más agencias y el middleware
de tenant inyecta el agencia_id automáticamente en cada request.

Toda consulta de agente debe filtrar por agencia_id (invariante #13).
"""

import uuid

from django.db import models


class Agencia(models.Model):
    """
    Tenant raíz del sistema. Cada agencia tiene sus propios viajes, usuarios
    e inscripciones completamente aislados del resto de tenants.

    DATABASE.md §Agencia
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="ID",
    )
    nombre = models.CharField(
        max_length=200,
        verbose_name="Nombre comercial",
    )
    logo = models.ImageField(
        upload_to="agencias/logos/",
        null=True,
        blank=True,
        verbose_name="Logo",
    )
    email_contacto = models.EmailField(
        unique=True,
        verbose_name="Email de contacto",
    )
    telefono = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Teléfono",
    )
    licencia_agencia = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Nº licencia oficial",
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name="Slug (identificador URL)",
        help_text="Identificador único en URL. Ejemplo: totem",
    )
    activa = models.BooleanField(
        default=True,
        verbose_name="Activa",
        help_text="Desactivar para suspender el acceso del tenant sin eliminar datos.",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación",
    )

    class Meta:
        verbose_name = "Agencia"
        verbose_name_plural = "Agencias"
        ordering = ["nombre"]

    def __str__(self) -> str:
        return f"{self.nombre} ({self.slug})"
