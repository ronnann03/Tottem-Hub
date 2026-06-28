"""
config/settings/base.py — Configuración base compartida entre entornos.

Este módulo lee variables de entorno con python-decouple.
No contiene valores sensibles; todos vienen del entorno o del .env.
"""

import dj_database_url
from datetime import timedelta
from pathlib import Path

from decouple import config

# ─────────────────────────────────────────────────────────────────────────────
# PATHS
# ─────────────────────────────────────────────────────────────────────────────

# BASE_DIR apunta a backend/ (donde vive manage.py)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# ─────────────────────────────────────────────────────────────────────────────
# SEGURIDAD
# ─────────────────────────────────────────────────────────────────────────────

SECRET_KEY = config("SECRET_KEY")

# DEBUG se sobreescribe en local.py (True) y production.py (False).
DEBUG = False

ALLOWED_HOSTS: list[str] = []

# ─────────────────────────────────────────────────────────────────────────────
# APLICACIONES
# INSTALLED_APPS preparado para las 12 apps del proyecto (TASK-004 criterio).
# Las apps propias se añadirán en sus respectivas TASK (TASK-005 en adelante).
# ─────────────────────────────────────────────────────────────────────────────

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "corsheaders",
    "django_celery_beat",
]

# Apps propias del proyecto — se activan a medida que se implementan:
# TASK-005: apps.agencias         ← ACTIVA
# TASK-006: apps.autenticacion    ← ACTIVA
# TASK-021: apps.viajes
# TASK-032: apps.inscripciones
# TASK-036: apps.pagos
# TASK-040: apps.documentos
# TASK-050: apps.comunicados
# TASK-058: apps.notificaciones
# TASK-055: apps.mecenas
# TASK-031: apps.auditoria
# TASK-065: apps.exportaciones
LOCAL_APPS: list[str] = [
    "apps.agencias",        # TASK-005 — Tenant raíz
    "apps.autenticacion",   # TASK-006 — Modelo Usuario custom
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# ─────────────────────────────────────────────────────────────────────────────
# MIDDLEWARE
# CorsMiddleware va ANTES de CommonMiddleware (requerido por django-cors-headers)
# ─────────────────────────────────────────────────────────────────────────────

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",          # CORS — debe ir primero
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ─────────────────────────────────────────────────────────────────────────────
# URLs
# ─────────────────────────────────────────────────────────────────────────────

ROOT_URLCONF = "config.urls"

# ─────────────────────────────────────────────────────────────────────────────
# TEMPLATES
# ─────────────────────────────────────────────────────────────────────────────

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# WSGI / ASGI
# ─────────────────────────────────────────────────────────────────────────────

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# ─────────────────────────────────────────────────────────────────────────────
# BASE DE DATOS — PostgreSQL 16
# Leída desde DATABASE_URL usando dj-database-url.
# UUID como PK en todos los modelos (definido en cada modelo, no aquí).
# ─────────────────────────────────────────────────────────────────────────────

DATABASES = {
    "default": dj_database_url.config(
        default=config("DATABASE_URL"),
        conn_max_age=600,         # Connection pooling: mantener conexiones 10 min
        conn_health_checks=True,  # Verificar salud de conexión antes de reutilizar
    )
}

# ─────────────────────────────────────────────────────────────────────────────
# MODELO DE USUARIO PERSONALIZADO
# Será activado en TASK-006 cuando se cree la app autenticacion.
# Descomentado aquí anticipadamente para evitar conflicto con migraciones.
# ─────────────────────────────────────────────────────────────────────────────

# AUTH_USER_MODEL — Activado en TASK-006
# Debe declararse ANTES de las migraciones iniciales de Django auth.
AUTH_USER_MODEL = "autenticacion.Usuario"

# ─────────────────────────────────────────────────────────────────────────────
# VALIDACIÓN DE CONTRASEÑAS
# ─────────────────────────────────────────────────────────────────────────────

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ─────────────────────────────────────────────────────────────────────────────
# INTERNACIONALIZACIÓN
# ─────────────────────────────────────────────────────────────────────────────

LANGUAGE_CODE = "es-pe"
TIME_ZONE = "America/Lima"
USE_I18N = True
USE_TZ = True  # Siempre True — almacenar timestamps en UTC

# ─────────────────────────────────────────────────────────────────────────────
# ARCHIVOS ESTÁTICOS Y MEDIA
# ─────────────────────────────────────────────────────────────────────────────

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "mediafiles"

# ─────────────────────────────────────────────────────────────────────────────
# PK POR DEFECTO
# UUID como PK — se especifica en cada modelo con UUIDField(primary_key=True).
# Esto define el tipo para modelos que no especifiquen PK explícitamente.
# ─────────────────────────────────────────────────────────────────────────────

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
# Nota: los modelos propios del proyecto usan UUIDField(primary_key=True)
# explícitamente, por lo que este setting solo aplica a modelos de terceros.

# ─────────────────────────────────────────────────────────────────────────────
# DJANGO REST FRAMEWORK
# Autenticación JWT por defecto para todos los endpoints.
# ─────────────────────────────────────────────────────────────────────────────

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        # Por defecto todo requiere autenticación; endpoints públicos
        # sobreescriben con AllowAny explícitamente.
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 25,
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.MultiPartParser",  # Para uploads de archivos
        "rest_framework.parsers.FormParser",
    ],
    # Manejo de excepciones centralizado — se personalizará en TASK-008+
    "EXCEPTION_HANDLER": "rest_framework.views.exception_handler",
}

# ─────────────────────────────────────────────────────────────────────────────
# JWT — djangorestframework-simplejwt
# access: 15 min (invariante arquitectura)
# refresh: 7 días en Redis allowlist (invariante arquitectura)
# NUNCA en localStorage — siempre en cookies httpOnly (gestionado por el Gateway)
# ─────────────────────────────────────────────────────────────────────────────

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(
        minutes=config("JWT_ACCESS_TOKEN_LIFETIME_MINUTES", default=15, cast=int)
    ),
    "REFRESH_TOKEN_LIFETIME": timedelta(
        days=config("JWT_REFRESH_TOKEN_LIFETIME_DAYS", default=7, cast=int)
    ),
    "ROTATE_REFRESH_TOKENS": False,   # Rotación manual en el endpoint /refresh/
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": False,       # El login actualiza ultimo_login en el modelo
    "ALGORITHM": "HS256",
    "SIGNING_KEY": config("JWT_SECRET_KEY"),
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
}

# ─────────────────────────────────────────────────────────────────────────────
# CORS — django-cors-headers
# Los orígenes permitidos se configuran por entorno (local.py / production.py).
# ─────────────────────────────────────────────────────────────────────────────

# CORS_ALLOWED_ORIGINS se define en local.py y production.py.
CORS_ALLOW_CREDENTIALS = True   # Necesario para enviar cookies httpOnly

CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]

CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]

# ─────────────────────────────────────────────────────────────────────────────
# REDIS — Cache y Broker
# Usamos django-redis como backend de caché.
# Base 0: caché general + JWT allowlist
# Base 1: reservada para Celery (CELERY_BROKER_URL)
# ─────────────────────────────────────────────────────────────────────────────

REDIS_URL = config("REDIS_URL", default="redis://redis:6379")

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            # Reconexión automática si Redis se reinicia
            "CONNECTION_POOL_KWARGS": {"max_connections": 50},
            "IGNORE_EXCEPTIONS": False,  # En prod no silenciar errores de Redis
        },
        "KEY_PREFIX": "tottemhub",
        "TIMEOUT": 300,  # 5 min por defecto; cada cache.set() puede sobreescribir
    }
}

# ─────────────────────────────────────────────────────────────────────────────
# CELERY — Configuración base
# Broker: Redis base 0 (mismo que caché)
# Backend de resultados: Redis base 0
# Workers y Beat se definen en sus respectivos docker-compose commands.
# Tareas concretas se añadirán en TASK-048+ (signals las disparan)
# ─────────────────────────────────────────────────────────────────────────────

CELERY_BROKER_URL = config("CELERY_BROKER_URL", default="redis://redis:6379/0")
CELERY_RESULT_BACKEND = config("CELERY_BROKER_URL", default="redis://redis:6379/0")
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "America/Lima"
CELERY_ENABLE_UTC = True

# Beat usa la base de datos para almacenar las tareas programadas
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

# Autodescubrimiento de tareas en los módulos `tasks` de cada app
CELERY_IMPORTS: list[str] = []  # Se pobla en TASK-048+

# ─────────────────────────────────────────────────────────────────────────────
# STORAGE — S3 / GCS (intercambiable vía env var)
# En desarrollo local se usa FileSystemStorage (DEFAULT_FILE_STORAGE no configurado).
# En producción se activa S3 o GCS según DEFAULT_FILE_STORAGE.
# ─────────────────────────────────────────────────────────────────────────────

_default_storage = config("DEFAULT_FILE_STORAGE", default="")

if _default_storage:
    DEFAULT_FILE_STORAGE = _default_storage
    STORAGES = {
        "default": {
            "BACKEND": _default_storage,
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }

AWS_STORAGE_BUCKET_NAME = config("AWS_STORAGE_BUCKET_NAME", default="")
AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID", default="")
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY", default="")
AWS_S3_FILE_OVERWRITE = False   # No sobreescribir archivos con el mismo nombre
AWS_DEFAULT_ACL = None          # Heredar ACL del bucket

# ─────────────────────────────────────────────────────────────────────────────
# EMAIL
# ─────────────────────────────────────────────────────────────────────────────

EMAIL_BACKEND = config(
    "EMAIL_BACKEND",
    default="django.core.mail.backends.console.EmailBackend",
)
EMAIL_HOST = config("EMAIL_HOST", default="localhost")
EMAIL_PORT = config("EMAIL_PORT", default=587, cast=int)
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=True, cast=bool)
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default="noreply@minkagroup.digital")
FRONTEND_URL = config("FRONTEND_URL", default="http://localhost:3000")

# ─────────────────────────────────────────────────────────────────────────────
# REGLAS DE NEGOCIO CONFIGURABLES
# Estas constantes se usan en tareas Celery (TASK-048+).
# ─────────────────────────────────────────────────────────────────────────────

# Días tras fecha_regreso del viaje para archivar documentos automáticamente
DOCS_ARCHIVE_DAYS_AFTER_RETURN = config(
    "DOCS_ARCHIVE_DAYS_AFTER_RETURN", default=30, cast=int
)

# Porcentaje de docs completados por debajo del cual se envía alerta al agente
DOC_INCOMPLETE_ALERT_THRESHOLD = config(
    "DOC_INCOMPLETE_ALERT_THRESHOLD", default=30, cast=int
)

# Tamaño máximo de archivo en bytes (10 MB) — segunda línea de defensa
# La primera línea está en el Gateway (MAX_FILE_SIZE_BYTES env var)
MAX_UPLOAD_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB

# ─────────────────────────────────────────────────────────────────────────────
# LOGGING — Configuración base
# ─────────────────────────────────────────────────────────────────────────────

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[{asctime}] {levelname} {name} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "django.db.backends": {
            # Nivel DEBUG muestra todas las queries SQL — útil en local,
            # se sobreescribe a WARNING en production.py
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
        # Logger específico para el proyecto
        "tottemhub": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
        # Logger para tareas Celery
        "celery": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}
