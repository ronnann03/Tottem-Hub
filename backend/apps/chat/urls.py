from django.urls import path
from .views import ConversacionView, MensajeCreateView, MensajesNuevosView

urlpatterns = [
    path('<uuid:inscripcion_id>/', ConversacionView.as_view(), name='conversacion'),
    path('<uuid:inscripcion_id>/mensajes/', MensajeCreateView.as_view(), name='mensaje-create'),
    path('<uuid:inscripcion_id>/mensajes/nuevos/', MensajesNuevosView.as_view(), name='mensajes-nuevos'),
]