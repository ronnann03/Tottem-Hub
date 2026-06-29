from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.viajes.permissions import EsAgente
from apps.viajes.models import Viaje
from rest_framework.exceptions import NotFound
from .models import Comunicado
from .serializers import ComunicadoSerializer
from .tasks import enviar_comunicado_masivo


class ComunicadoListCreateView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, EsAgente]
    serializer_class = ComunicadoSerializer

    def get(self, request, viaje_id):
        try:
            viaje = Viaje.objects.get(id=viaje_id, agencia=request.user.agencia)
        except Viaje.DoesNotExist:
            raise NotFound('Viaje no encontrado.')
        comunicados = viaje.comunicados.all()
        return Response(ComunicadoSerializer(comunicados, many=True).data)

    def post(self, request, viaje_id):
        try:
            viaje = Viaje.objects.get(id=viaje_id, agencia=request.user.agencia)
        except Viaje.DoesNotExist:
            raise NotFound('Viaje no encontrado.')
        serializer = ComunicadoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        comunicado = serializer.save(viaje=viaje, autor=request.user)
        enviar_comunicado_masivo.delay(str(comunicado.id))
        return Response(ComunicadoSerializer(comunicado).data, status=status.HTTP_201_CREATED)
