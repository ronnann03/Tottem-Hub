import csv
import io
from django.http import HttpResponse


def exportar_inscritos_csv(inscripciones):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Nombre', 'Apellidos', 'DNI', 'Tutor', 'Email Tutor', 'Estado', '% Pagado', 'Docs Validados', 'Grupo'])
    for ins in inscripciones:
        writer.writerow([
            ins.alumno.nombre,
            ins.alumno.apellidos,
            ins.alumno.dni,
            ins.padre_tutor.usuario.nombre if ins.padre_tutor else '',
            ins.padre_tutor.usuario.email if ins.padre_tutor else '',
            ins.estado,
            ins.porcentaje_pagado,
            '',
            '',
        ])
    response = HttpResponse(output.getvalue(), content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="inscritos.csv"'
    return response


def exportar_pagos_csv(pagos):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Alumno', 'Importe', 'Fecha', 'Metodo', 'Estado'])
    for pago in pagos:
        writer.writerow([
            pago.inscripcion.alumno.nombre + ' ' + pago.inscripcion.alumno.apellidos,
            pago.importe,
            pago.fecha_pago,
            pago.metodo_pago,
            pago.estado,
        ])
    response = HttpResponse(output.getvalue(), content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="pagos.csv"'
    return response


def exportar_documentacion_csv(documentos):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Alumno', 'Documento', 'Estado', 'Archivo', 'Motivo Rechazo'])
    for doc in documentos:
        writer.writerow([
            doc.inscripcion.alumno.nombre + ' ' + doc.inscripcion.alumno.apellidos,
            doc.documento_requerido.nombre,
            doc.estado,
            doc.nombre_archivo,
            doc.motivo_rechazo,
        ])
    response = HttpResponse(output.getvalue(), content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="documentacion.csv"'
    return response