from django.urls import path
from .views import PagoListCreateView

urlpatterns = [
    path('', PagoListCreateView.as_view(), name='pago-list-create'),
]
