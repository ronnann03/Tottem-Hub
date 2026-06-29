from rest_framework import serializers
from .models import Notificacion


class NotificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notificacion
        fields = ['id', 'tipo', 'titulo', 'mensaje', 'leida', 'referencia_id', 'referencia_tipo', 'created_at']
        read_only_fields = ['id', 'tipo', 'titulo', 'mensaje', 'referencia_id', 'referencia_tipo', 'created_at']
