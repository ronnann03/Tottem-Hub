# Este archivo hace que `config/` sea un paquete Python.
# También importa la app Celery para que los workers la descubran
# automáticamente al iniciar Django.
from .celery import app as celery_app  # noqa: F401

__all__ = ("celery_app",)
