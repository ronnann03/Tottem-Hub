"""
apps/agencias/urls.py — Rutas del módulo de agencias.

Prefijo: /api/v1/agencias/ (registrado en config/urls.py)

TASK-012: GET/PATCH /perfil/
"""

from django.urls import path

from .views import AgenciaPerfilAPIView

app_name = "agencias"

urlpatterns = [
    path("perfil/", AgenciaPerfilAPIView.as_view(), name="perfil"),
]
