import io
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.utils import timezone
from xhtml2pdf import pisa


def _html_a_pdf(html_string):
    output = io.BytesIO()
    pisa.CreatePDF(io.StringIO(html_string), dest=output)
    return output.getvalue()


def exportar_informe_pdf(viaje, inscripciones):
    total_recaudado = sum(getattr(ins, 'total_pagado', 0) for ins in inscripciones)
    html = render_to_string('pdf/informe_viaje.html', {
        'viaje': viaje,
        'inscripciones': inscripciones,
        'total_inscritos': inscripciones.count(),
        'total_recaudado': total_recaudado,
        'docs_completos': 0,
        'fecha_generacion': timezone.localtime().strftime('%d/%m/%Y %H:%M'),
    })
    pdf = _html_a_pdf(html)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="informe_{viaje.id}.pdf"'
    return response


def exportar_ficha_pdf(inscripcion):
    html = render_to_string('pdf/ficha_inscripcion.html', {
        'inscripcion': inscripcion,
        'fecha_generacion': timezone.localtime().strftime('%d/%m/%Y %H:%M'),
    })
    pdf = _html_a_pdf(html)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="ficha_{inscripcion.id}.pdf"'
    return response