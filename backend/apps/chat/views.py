from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound, PermissionDenied
from django.utils import timezone
from apps.inscripciones.models import Inscripcion
from .models import Conversacion, Mensaje
from .serializers import ConversacionSerializer, MensajeSerializer


class ConversacionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, inscripcion_id):
        try:
            inscripcion = Inscripcion.objects.get(id=inscripcion_id)
        except Inscripcion.DoesNotExist:
            raise NotFound('Inscripcion no encontrada.')
        conversacion, _ = Conversacion.objects.get_or_create(inscripcion=inscripcion)
        Mensaje.objects.filter(
            conversacion=conversacion,
            estado='enviado'
        ).exclude(remitente=request.user).update(estado='leido', leido_en=timezone.now())
        serializer = ConversacionSerializer(conversacion)
        return Response(serializer.data)


class MensajeCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, inscripcion_id):
        try:
            inscripcion = Inscripcion.objects.get(id=inscripcion_id)
        except Inscripcion.DoesNotExist:
            raise NotFound('Inscripcion no encontrada.')
        contenido = request.data.get('contenido', '').strip()
        if not contenido:
            return Response({'error': 'El contenido no puede estar vacio.'}, status=400)
        conversacion, _ = Conversacion.objects.get_or_create(inscripcion=inscripcion)
        mensaje = Mensaje.objects.create(
            conversacion=conversacion,
            remitente=request.user,
            contenido=contenido,
        )
        return Response(MensajeSerializer(mensaje).data, status=201)


class MensajesNuevosView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, inscripcion_id):
        try:
            inscripcion = Inscripcion.objects.get(id=inscripcion_id)
            conversacion = inscripcion.conversacion
        except (Inscripcion.DoesNotExist, Conversacion.DoesNotExist):
            return Response([])
        desde = request.query_params.get('desde')
        qs = conversacion.mensajes.exclude(remitente=request.user)
        if desde:
            qs = qs.filter(created_at__gt=desde)
        qs = qs.filter(estado='enviado')
        qs.update(estado='leido', leido_en=timezone.now())
        return Response(MensajeSerializer(qs, many=True).data)