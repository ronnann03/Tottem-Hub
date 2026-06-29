from django.urls import path
from .views import MecenasAlumnosView, AsignarMecenasView

urlpatterns = [
    path('<uuid:pk>/alumnos/', MecenasAlumnosView.as_view(), name='mecenas-alumnos'),
    path('inscripciones/<uuid:inscripcion_id>/mecenas/', AsignarMecenasView.as_view(), name='asignar-mecenas'),
]