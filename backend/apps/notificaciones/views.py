from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from .models import Notificacion
from .serializers import NotificacionSerializer


class NotificacionListView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = Notificacion.objects.filter(usuario=request.user)
        leida = request.query_params.get('leida')
        if leida == 'false':
            qs = qs.filter(leida=False)
        elif leida == 'true':
            qs = qs.filter(leida=True)
        serializer = NotificacionSerializer(qs, many=True)
        return Response(serializer.data)


class NotificacionMarcarLeidaView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            notif = Notificacion.objects.get(pk=pk, usuario=request.user)
        except Notificacion.DoesNotExist:
            raise NotFound('Notificacion no encontrada.')
        notif.leida = True
        notif.save()
        return Response(NotificacionSerializer(notif).data)


class NotificacionMarcarTodasView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        Notificacion.objects.filter(usuario=request.user, leida=False).update(leida=True)
        return Response({'detail': 'Todas las notificaciones marcadas como leidas.'}, status=status.HTTP_200_OK)


from .models import PreferenciasNotificacion
from .serializers import PreferenciasNotificacionSerializer


class PreferenciasNotificacionView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PreferenciasNotificacionSerializer

    def get(self, request):
        prefs, _ = PreferenciasNotificacion.objects.get_or_create(usuario=request.user)
        return Response(PreferenciasNotificacionSerializer(prefs).data)

    def patch(self, request):
        prefs, _ = PreferenciasNotificacion.objects.get_or_create(usuario=request.user)
        serializer = PreferenciasNotificacionSerializer(prefs, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
