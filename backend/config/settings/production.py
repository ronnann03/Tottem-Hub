"""
config/settings/production.py — Overrides de producción.

Aplica hardening de seguridad, CORS restrictivo y logging estructurado.
Activar con: DJANGO_SETTINGS_MODULE=config.settings.production
"""

from decouple import Csv, config

from .base import *  # noqa: F401, F403
from .base import LOGGING  # noqa: F811 — redeclared for mutation

# ─────────────────────────────────────────────────────────────────────────────
# DEBUG — nunca True en producción
# ─────────────────────────────────────────────────────────────────────────────

DEBUG = False

ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())

# ─────────────────────────────────────────────────────────────────────────────
# CORS — solo dominios de producción
# ─────────────────────────────────────────────────────────────────────────────

CORS_ALLOWED_ORIGINS = config("CORS_ORIGINS", cast=Csv())

# ─────────────────────────────────────────────────────────────────────────────
# SEGURIDAD HTTP
# ─────────────────────────────────────────────────────────────────────────────

# TLS terminado en el Gateway — Django detrás del proxy
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = False       # El gateway ya redirige HTTP → HTTPS
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# HSTS — el Gateway también lo envía como primera línea de defensa
SECURE_HSTS_SECONDS = 31536000    # 1 año
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Cabeceras de seguridad adicionales
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = "DENY"

# ─────────────────────────────────────────────────────────────────────────────
# LOGGING — nivel WARNING en producción; queries SQL silenciadas
# ─────────────────────────────────────────────────────────────────────────────

LOGGING["loggers"]["django.db.backends"]["level"] = "WARNING"  # type: ignore[index]
LOGGING["loggers"]["tottemhub"]["level"] = "INFO"              # type: ignore[index]
LOGGING["root"]["level"] = "WARNING"                           # type: ignore[index]
