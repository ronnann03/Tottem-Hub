from rest_framework import serializers
from .models import DocumentoEntregado
from .validators import validar_archivo


class DocumentoEntregadoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentoEntregado
        fields = ['inscripcion', 'documento_requerido', 'archivo']

    def validate_archivo(self, value):
        return validar_archivo(value)

    def create(self, validated_data):
        archivo = validated_data['archivo']
        validated_data['nombre_archivo'] = archivo.name
        validated_data['tamano_bytes'] = archivo.size
        validated_data['estado'] = 'pendiente'
        return super().create(validated_data)


class DocumentoEntregadoDetalleSerializer(serializers.ModelSerializer):
    tamano_legible = serializers.ReadOnlyField()

    class Meta:
        model = DocumentoEntregado
        fields = ['id', 'inscripcion', 'documento_requerido', 'archivo',
                  'nombre_archivo', 'tamano_bytes', 'tamano_legible',
                  'estado', 'motivo_rechazo', 'validado_por',
                  'fecha_validacion', 'uploaded_at']
        read_only_fields = ['id', 'nombre_archivo', 'tamano_bytes', 'estado',
                            'motivo_rechazo', 'validado_por', 'fecha_validacion', 'uploaded_at']
