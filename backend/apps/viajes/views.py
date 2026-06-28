from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Viaje
from .serializers import ViajeSerializer
from .permissions import EsAgente


class ViajeListCreateView(generics.ListCreateAPIView):
    serializer_class = ViajeSerializer
    permission_classes = [IsAuthenticated, EsAgente]

    def get_queryset(self):
        """
        Retorna únicamente los viajes pertenecientes a la agencia del agente.
        Aplica select_related para evitar consultas N+1 con agencia.
        """
        return Viaje.objects.filter(
            agencia=self.request.user.agencia
        ).select_related('agencia').order_by('fecha_salida')

    def perform_create(self, serializer):
        """
        Inyecta la agencia del usuario autenticado de forma transparente.
        """
        serializer.save(agencia=self.request.user.agencia)
