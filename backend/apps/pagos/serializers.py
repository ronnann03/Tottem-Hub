from rest_framework import serializers
from .models import Pago

FORMATOS_PERMITIDOS = ['application/pdf', 'image/jpeg', 'image/png']
TAMANO_MAXIMO = 10 * 1024 * 1024  # 10 MB


class PagoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pago
        fields = ['inscripcion', 'cuota', 'importe', 'fecha_pago', 'metodo_pago', 'comprobante', 'notas']

    def validate_comprobante(self, value):
        if value:
            if value.size > TAMANO_MAXIMO:
                raise serializers.ValidationError('El archivo no puede superar 10 MB.')
            if hasattr(value, 'content_type') and value.content_type not in FORMATOS_PERMITIDOS:
                raise serializers.ValidationError('Formato no permitido. Use PDF, JPG o PNG.')
        return value

    def validate_importe(self, value):
        if value <= 0:
            raise serializers.ValidationError('El importe debe ser mayor a 0.')
        return value


class PagoDetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pago
        fields = ['id', 'inscripcion', 'cuota', 'pagado_por', 'registrado_por',
                  'importe', 'fecha_pago', 'metodo_pago', 'comprobante', 'estado', 'notas', 'created_at']
        read_only_fields = ['id', 'estado', 'created_at', 'pagado_por', 'registrado_por']
