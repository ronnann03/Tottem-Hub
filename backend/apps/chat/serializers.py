from rest_framework import serializers
from .models import Conversacion, Mensaje


class MensajeSerializer(serializers.ModelSerializer):
    remitente_nombre = serializers.SerializerMethodField()

    class Meta:
        model = Mensaje
        fields = ['id', 'contenido', 'estado', 'leido_en', 'created_at', 'remitente', 'remitente_nombre']
        read_only_fields = ['id', 'estado', 'leido_en', 'created_at', 'remitente', 'remitente_nombre']

    def get_remitente_nombre(self, obj):
        return obj.remitente.nombre if obj.remitente else ''


class ConversacionSerializer(serializers.ModelSerializer):
    mensajes = MensajeSerializer(many=True, read_only=True)

    class Meta:
        model = Conversacion
        fields = ['id', 'inscripcion', 'created_at', 'updated_at', 'mensajes']
        read_only_fields = ['id', 'created_at', 'updated_at']