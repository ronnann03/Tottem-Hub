from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Colegio


class ColegioSearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        q = request.query_params.get('q', '').strip()
        departamento = request.query_params.get('departamento', '').strip()
        if len(q) < 2:
            return Response([])
        qs = Colegio.objects.filter(activo=True)
        if departamento:
            qs = qs.filter(departamento__iexact=departamento)
        qs = qs.filter(nombre__icontains=q)[:20]
        return Response([{
            'id': c.id,
            'nombre': c.nombre,
            'codigo_modular': c.codigo_modular,
            'departamento': c.departamento,
            'provincia': c.provincia,
            'distrito': c.distrito,
            'nivel': c.nivel,
        } for c in qs])