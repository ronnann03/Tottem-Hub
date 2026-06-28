from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, PermissionDenied
from .models import Pago
from .serializers import PagoCreateSerializer, PagoDetalleSerializer


class PagoListCreateView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.rol == 'agente':
            pagos = Pago.objects.filter(inscripcion__viaje__agencia=request.user.agencia)
        else:
            pagos = Pago.objects.filter(pagado_por=request.user)
        serializer = PagoDetalleSerializer(pagos, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PagoCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            pagado_por=request.user,
            registrado_por=request.user,
            estado='pendiente'
        )
        return Response(PagoDetalleSerializer(serializer.instance).data, status=status.HTTP_201_CREATED)
