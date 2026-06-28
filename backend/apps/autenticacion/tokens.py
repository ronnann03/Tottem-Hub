"""
apps/autenticacion/tokens.py — Tokens de autenticación.

Módulo centralizado de tokens para evitar strings mágicos dispersos en el código.

Tokens de verificación de email (django.core.signing):
  - Stateless, HMAC firmados, expiran en 24h, sin tabla en BD.
  - POST /auth/registro/  → generar_token_verificacion()
  - GET  /auth/verificar/ → verificar_token_verificacion()

Redis keys para refresh tokens JWT (TASK-010+):
  - REFRESH_REDIS_KEY — template de clave para el allowlist de refresh tokens.
  - Usado en LoginAPIView (set) y LogoutAPIView (delete, TASK-011).
"""

from django.core import signing

_SALT = "email-verificacion-tottemhub"
MAX_AGE_SEGUNDOS = 60 * 60 * 24  # 24 horas

# Template de clave Redis para el allowlist de refresh tokens.
# Uso: REFRESH_REDIS_KEY.format(jti=str(refresh["jti"]))
REFRESH_REDIS_KEY = "refresh:{jti}"


def generar_token_verificacion(usuario) -> str:
    """Genera un token firmado que codifica el UUID del usuario."""
    return signing.dumps(str(usuario.id), salt=_SALT)


def verificar_token_verificacion(token: str) -> str:
    """
    Valida el token y retorna el user_id (str UUID).

    Lanza:
      - signing.SignatureExpired  si han pasado más de 24 h
      - signing.BadSignature      si el token está manipulado o es inválido
    """
    return signing.loads(token, salt=_SALT, max_age=MAX_AGE_SEGUNDOS)
