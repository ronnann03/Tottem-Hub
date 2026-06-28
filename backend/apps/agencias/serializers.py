"""
apps/agencias/serializers.py — Serializadores del módulo de agencias.

AgenciaPerfilSerializer:
  - GET:  expone id, nombre, logo, email_contacto, telefono, licencia_agencia,
          slug, activa, created_at.
  - PATCH: solo acepta nombre, logo, telefono, email_contacto.
           Los campos id, licencia_agencia, slug, activa, created_at son read_only.
"""

from rest_framework import serializers

from .models import Agencia


class AgenciaPerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agencia
        fields = [
            "id",
            "nombre",
            "logo",
            "email_contacto",
            "telefono",
            "licencia_agencia",
            "slug",
            "activa",
            "created_at",
        ]
        read_only_fields = ["id", "licencia_agencia", "slug", "activa", "created_at"]
