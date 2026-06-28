from django.urls import path
from .views import AlumnoListCreateView, AlumnoRetrieveUpdateView

urlpatterns = [
    path('', AlumnoListCreateView.as_view(), name='alumno-list-create'),
    path('<uuid:pk>/', AlumnoRetrieveUpdateView.as_view(), name='alumno-detail'),  # noqa: E501
]
