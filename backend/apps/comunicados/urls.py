from django.urls import path
from .views import ComunicadoListCreateView

urlpatterns = [
    path('<uuid:viaje_id>/comunicados/', ComunicadoListCreateView.as_view(), name='viaje-comunicados'),
]
