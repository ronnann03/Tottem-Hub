"""
config/wsgi.py — Punto de entrada WSGI para servidores síncronos (gunicorn).

Usado en producción con: gunicorn config.wsgi:application
En desarrollo se usa manage.py runserver (que también usa WSGI internamente).
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

application = get_wsgi_application()
