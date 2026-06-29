from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.core.cache import cache


@shared_task(bind=True, max_retries=3)
def enviar_comunicado_masivo(self, comunicado_id):
    cache_key = 'comunicado_enviado_' + str(comunicado_id)
    if cache.get(cache_key):
        return 'Ya enviado (idempotente)'
    from apps.comunicados.models import Comunicado
    from apps.notificaciones.models import Notificacion
    try:
        comunicado = Comunicado.objects.select_related('viaje', 'autor').get(id=comunicado_id)
    except Comunicado.DoesNotExist:
        return 'Comunicado no encontrado'
    inscripciones = comunicado.viaje.inscripciones.filter(
        estado__in=['pendiente', 'confirmado']
    ).select_related('padre_tutor__usuario')
    for inscripcion in inscripciones:
        tutor = inscripcion.padre_tutor.usuario
        contexto = {
            'titulo': comunicado.titulo,
            'nombre_tutor': tutor.nombre,
            'nombre_viaje': comunicado.viaje.nombre,
            'cuerpo': comunicado.cuerpo,
        }
        html = render_to_string('emails/comunicado.html', contexto)
        send_mail(
            subject=comunicado.titulo,
            message=comunicado.cuerpo,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[tutor.email],
            html_message=html,
            fail_silently=True,
        )
        Notificacion.objects.create(
            usuario=tutor,
            tipo='comunicado',
            titulo=comunicado.titulo,
            mensaje=comunicado.cuerpo[:200],
            referencia_id=comunicado.id,
            referencia_tipo='Comunicado'
        )
    comunicado.enviado_email = True
    comunicado.save()
    cache.set(cache_key, True, timeout=86400)
    return 'OK: ' + str(inscripciones.count()) + ' emails enviados'
