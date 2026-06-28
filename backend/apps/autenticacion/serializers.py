"""
apps/autenticacion/serializers.py — Serializadores de autenticación.

RegistroSerializer:
  - Valida payload de POST /auth/registro/ (API.md §Auth).
  - Restricción I-03: rol 'agente' no disponible en registro público.
  - Crea Usuario y, si rol='padre', crea PadreTutor con campos vacíos.
  - Todo en una transacción atómica.

LoginSerializer:
  - Valida schema del payload de POST /auth/login/ (email + password).
  - Sin lógica de negocio: credenciales, email_verificado y activo se
    verifican en LoginAPIView para controlar los status HTTP de error.

Decisiones:
  I-03 — 'agente' solo puede crearse desde el panel de administración.
  D-09  — PadreTutor se crea con relacion_alumno='' (blank=True).
"""

from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from rest_framework import serializers

from .models import PadreTutor, RolUsuario, Usuario


class RegistroSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        validators=[validate_password],
        style={"input_type": "password"},
    )

    class Meta:
        model = Usuario
        fields = ["email", "password", "nombre", "apellidos", "rol", "telefono"]
        extra_kwargs = {
            "telefono": {"required": False, "default": ""},
        }

    def validate_rol(self, value: str) -> str:
        if value == RolUsuario.AGENTE:
            raise serializers.ValidationError(
                "El rol 'agente' no está disponible en el registro público. "
                "Contacta a tu agencia para obtener acceso."
            )
        return value

    @transaction.atomic
    def create(self, validated_data: dict) -> Usuario:
        password = validated_data.pop("password")
        usuario = Usuario.objects.create_user(password=password, **validated_data)
        if usuario.rol == RolUsuario.PADRE:
            PadreTutor.objects.create(usuario=usuario)
        return usuario


class LoginSerializer(serializers.Serializer):
    """
    Valida el schema del payload de POST /auth/login/.

    Validaciones de negocio (credenciales, email_verificado, activo) están
    en LoginAPIView para poder retornar 401/403 diferenciados.
    """

    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True,
        style={"input_type": "password"},
    )
