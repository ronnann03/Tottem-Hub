from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from apps.viajes.permissions import EsAgente
from apps.viajes.models import Viaje
from apps.inscripciones.models import Inscripcion
from apps.pagos.models import Pago
from apps.documentos.models import DocumentoEntregado
from .generators.csv import exportar_inscritos_csv, exportar_pagos_csv, exportar_documentacion_csv
from .generators.xlsx import exportar_inscritos_xlsx, exportar_pagos_xlsx, exportar_documentacion_xlsx
from .generators.pdf import exportar_informe_pdf, exportar_ficha_pdf


class ExportarInscritosView(APIView):
    permission_classes = [IsAuthenticated, EsAgente]

    def get(self, request, viaje_id):
        try:
            viaje = Viaje.objects.get(id=viaje_id)
        except Viaje.DoesNotExist:
            raise NotFound('Viaje no encontrado.')
        inscripciones = Inscripcion.objects.filter(viaje=viaje).select_related('alumno', 'padre_tutor__usuario')
        formato = request.query_params.get('formato', 'csv')
        if formato == 'xlsx':
            return exportar_inscritos_xlsx(inscripciones)
        return exportar_inscritos_csv(inscripciones)


class ExportarPagosView(APIView):
    permission_classes = [IsAuthenticated, EsAgente]

    def get(self, request, viaje_id):
        try:
            viaje = Viaje.objects.get(id=viaje_id)
        except Viaje.DoesNotExist:
            raise NotFound('Viaje no encontrado.')
        pagos = Pago.objects.filter(inscripcion__viaje=viaje).select_related('inscripcion__alumno')
        formato = request.query_params.get('formato', 'csv')
        if formato == 'xlsx':
            return exportar_pagos_xlsx(pagos)
        return exportar_pagos_csv(pagos)


class ExportarDocumentacionView(APIView):
    permission_classes = [IsAuthenticated, EsAgente]

    def get(self, request, viaje_id):
        try:
            viaje = Viaje.objects.get(id=viaje_id)
        except Viaje.DoesNotExist:
            raise NotFound('Viaje no encontrado.')
        documentos = DocumentoEntregado.objects.filter(inscripcion__viaje=viaje).select_related('inscripcion__alumno', 'documento_requerido')
        formato = request.query_params.get('formato', 'csv')
        if formato == 'xlsx':
            return exportar_documentacion_xlsx(documentos)
        return exportar_documentacion_csv(documentos)


class ExportarInformePDFView(APIView):
    permission_classes = [IsAuthenticated, EsAgente]

    def get(self, request, viaje_id):
        try:
            viaje = Viaje.objects.get(id=viaje_id)
        except Viaje.DoesNotExist:
            raise NotFound('Viaje no encontrado.')
        inscripciones = Inscripcion.objects.filter(viaje=viaje).select_related('alumno', 'padre_tutor__usuario')
        return exportar_informe_pdf(viaje, inscripciones)


class ExportarFichaPDFView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, inscripcion_id):
        try:
            inscripcion = Inscripcion.objects.select_related('viaje', 'alumno', 'padre_tutor__usuario').get(id=inscripcion_id)
        except Inscripcion.DoesNotExist:
            raise NotFound('Inscripcion no encontrada.')
        return exportar_ficha_pdf(inscripcion)