"""
config/asgi.py — Punto de entrada ASGI (preparado para WebSockets futuros).

Fase 1 usa WSGI (gunicorn). Este archivo se activa si se añade Channels
en una fase futura para notificaciones en tiempo real.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

application = get_asgi_application()
