"""
config/celery.py — Instancia de la aplicación Celery.

Autodescubre tareas en todos los módulos `tasks.py` de cada app Django.
Las tareas concretas se añadirán en TASK-048+ cuando se implementen los signals.

Inicialización:
  celery -A config worker --loglevel=info
  celery -A config beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler
"""

import os

from celery import Celery

# Asegurar que el módulo de settings esté cargado antes de inicializar Celery.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

app = Celery("tottemhub")

# Leer configuración Celery desde Django settings (prefijo CELERY_).
app.config_from_object("django.conf:settings", namespace="CELERY")

# Autodescubrimiento de tareas en el módulo `tasks` de cada app Django instalada.
# Ejemplo: apps/pagos/tasks.py se descubre automáticamente.
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self) -> None:
    """Tarea de diagnóstico — verifica que Celery está operativo."""
    print(f"Request: {self.request!r}")
