from django.urls import path
from .views import ViajeListCreateView


urlpatterns = [
    path('', ViajeListCreateView.as_view(), name='viaje-list-create'),
]
