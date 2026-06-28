"""
apps/agencias/views.py — Vistas del módulo de agencias.

AgenciaPerfilAPIView — GET/PATCH /api/v1/agencias/perfil/

  GET:   Devuelve el perfil completo de la agencia del agente autenticado.
  PATCH: Actualiza nombre, logo, telefono o email_contacto (parcialmente).

Invariante #13 (AI_CONTEXT.md): la agencia se obtiene del usuario autenticado,
nunca de un parámetro del request. Esto garantiza el aislamiento multi-tenant.

Queries por request:
  GET:   2 (autenticación + SELECT agencia)
  PATCH: 3 (autenticación + SELECT agencia + UPDATE agencia)
  No hay riesgo de N+1 en este endpoint.
"""

import logging

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .permissions import EsAgente
from .serializers import AgenciaPerfilSerializer

logger = logging.getLogger("tottemhub")


class AgenciaPerfilAPIView(APIView):
    """
    GET  /api/v1/agencias/perfil/ — Perfil de la agencia del agente autenticado.
    PATCH /api/v1/agencias/perfil/ — Actualiza nombre, logo, telefono, email_contacto.
    """

    permission_classes = [EsAgente]

    def get(self, request: Request) -> Response:
        agencia = request.user.agencia
        if agencia is None:
            return Response(
                {"error": "No tienes una agencia asignada. Contacta al administrador."},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = AgenciaPerfilSerializer(agencia, context={"request": request})
        return Response(serializer.data)

    def patch(self, request: Request) -> Response:
        agencia = request.user.agencia
        if agencia is None:
            return Response(
                {"error": "No tienes una agencia asignada. Contacta al administrador."},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = AgenciaPerfilSerializer(
            agencia,
            data=request.data,
            partial=True,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        logger.info(
            "Perfil de agencia actualizado: slug=%s por agente=%s",
            agencia.slug,
            request.user.email,
        )
        return Response(serializer.data)
