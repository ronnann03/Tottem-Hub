from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import DocumentoEntregado
from .serializers import DocumentoEntregadoCreateSerializer, DocumentoEntregadoDetalleSerializer


class DocumentoEntregadoCreateView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = DocumentoEntregadoCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        doc = serializer.save()
        return Response(DocumentoEntregadoDetalleSerializer(doc).data, status=status.HTTP_201_CREATED)

    def get(self, request):
        estado = request.query_params.get('estado')
        viaje_id = request.query_params.get('viaje_id')
        qs = DocumentoEntregado.objects.select_related('inscripcion', 'documento_requerido')
        if estado:
            qs = qs.filter(estado=estado)
        if viaje_id:
            qs = qs.filter(inscripcion__viaje_id=viaje_id)
        if request.user.rol == 'padre':
            qs = qs.filter(inscripcion__padre_tutor__usuario=request.user)
        serializer = DocumentoEntregadoDetalleSerializer(qs, many=True)
        return Response(serializer.data)
