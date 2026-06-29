from rest_framework import serializers

FORMATOS_PERMITIDOS = {
    'application/pdf': 'pdf',
    'image/jpeg': 'jpg',
    'image/png': 'png',
}
TAMANO_MAXIMO = 10 * 1024 * 1024  # 10 MB


def validar_archivo(archivo):
    if archivo.size > TAMANO_MAXIMO:
        raise serializers.ValidationError('El archivo no puede superar 10 MB.')
    content_type = getattr(archivo, 'content_type', '')
    if content_type not in FORMATOS_PERMITIDOS:
        raise serializers.ValidationError(
            'Formato no permitido. Use PDF, JPG o PNG. Recibido: ' + content_type
        )
    extension = archivo.name.rsplit('.', 1)[-1].lower() if '.' in archivo.name else ''
    if extension not in ['pdf', 'jpg', 'jpeg', 'png']:
        raise serializers.ValidationError('Extension no permitida: ' + extension)
    return archivo
