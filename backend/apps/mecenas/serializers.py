from rest_framework import serializers
from .models import Mecenas, MecenasInscripcion


class MecenasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mecenas
        fields = ['id', 'nombre', 'email', 'telefono', 'created_at']
        read_only_fields = ['id', 'created_at']


class MecenasInscripcionSerializer(serializers.ModelSerializer):
    mecenas = MecenasSerializer(read_only=True)
    mecenas_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = MecenasInscripcion
        fields = ['id', 'mecenas', 'mecenas_id', 'inscripcion', 'monto_comprometido', 'monto_pagado', 'notas', 'created_at']
        read_only_fields = ['id', 'created_at']