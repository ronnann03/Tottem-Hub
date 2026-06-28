from django.urls import path
from .views import PagoListCreateView, PagoVerificarRechazarView

urlpatterns = [
    path('', PagoListCreateView.as_view(), name='pago-list-create'),
    path('<uuid:pk>/', PagoVerificarRechazarView.as_view(), name='pago-detail'),
]

