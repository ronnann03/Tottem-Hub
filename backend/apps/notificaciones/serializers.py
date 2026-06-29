from rest_framework import serializers
from .models import Notificacion, PreferenciasNotificacion


class NotificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notificacion
        fields = ['id', 'tipo', 'titulo', 'mensaje', 'leida', 'referencia_id', 'referencia_tipo', 'created_at']
        read_only_fields = ['id', 'tipo', 'titulo', 'mensaje', 'referencia_id', 'referencia_tipo', 'created_at']


class PreferenciasNotificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreferenciasNotificacion
        fields = ['canal_preferido', 'horario_inicio', 'horario_fin', 'max_por_dia', 'recibir_recordatorios', 'recibir_comunicados', 'recibir_alertas_docs']