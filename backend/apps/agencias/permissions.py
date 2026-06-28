"""
apps/agencias/permissions.py — Permisos del módulo de agencias.

EsAgente: acceso solo a usuarios autenticados con rol='agente'.
No valida que el agente tenga una agencia asignada — eso es responsabilidad de la vista.
"""

from rest_framework.permissions import BasePermission

from apps.autenticacion.models import RolUsuario


class EsAgente(BasePermission):
    """Permite acceso solo a usuarios con rol 'agente'."""

    def has_permission(self, request, view) -> bool:
        return (
            bool(request.user and request.user.is_authenticated)
            and request.user.rol == RolUsuario.AGENTE
        )
