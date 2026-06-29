from django.urls import path
from .views import DocumentoEntregadoCreateView, DocumentoValidarRechazarView

urlpatterns = [
    path('', DocumentoEntregadoCreateView.as_view(), name='documento-list-create'),
    path('<uuid:pk>/', DocumentoValidarRechazarView.as_view(), name='documento-detail'),
]
