from django.urls import path
from .views import DocumentoEntregadoCreateView

urlpatterns = [
    path('', DocumentoEntregadoCreateView.as_view(), name='documento-list-create'),
]
