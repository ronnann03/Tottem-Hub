from rest_framework.permissions import BasePermission
from apps.autenticacion.models import RolUsuario


class EsAgente(BasePermission):
    """
    Permite acceso solo a usuarios con rol 'agente'.
    """

    def has_permission(self, request, view) -> bool:
        return (
            bool(request.user and request.user.is_authenticated)
            and request.user.rol == RolUsuario.AGENTE
        )
