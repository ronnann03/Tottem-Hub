from django.urls import path
from .views import NotificacionListView, NotificacionMarcarLeidaView, NotificacionMarcarTodasView, PreferenciasNotificacionView

urlpatterns = [
    path('', NotificacionListView.as_view(), name='notificacion-list'),
    path('<uuid:pk>/', NotificacionMarcarLeidaView.as_view(), name='notificacion-detail'),
    path('marcar-todas/', NotificacionMarcarTodasView.as_view(), name='notificacion-marcar-todas'),
    path('preferencias/', PreferenciasNotificacionView.as_view(), name='preferencias-notificacion'),
]

