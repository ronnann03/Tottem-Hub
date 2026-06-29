from celery import shared_task
from django.core.cache import cache
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import date, timedelta

TRIGGERS_DIAS = [30, 15, 7, 3, 0]


@shared_task(bind=True, max_retries=3)
def verificar_cuotas_por_vencer(self):
    hora_actual = timezone.localtime().hour
    if hora_actual < 9 or hora_actual >= 20:
        return 'Fuera del horario de envio (9-20h)'
    from apps.viajes.models import Cuota
    from apps.notificaciones.models import Notificacion
    from apps.inscripciones.models import Inscripcion
    hoy = date.today()
    enviados = 0
    for trigger in TRIGGERS_DIAS:
        fecha_objetivo = hoy + timedelta(days=trigger)
        cuotas = Cuota.objects.filter(fecha_vencimiento=fecha_objetivo).select_related('plan_pago__viaje')
        for cuota in cuotas:
            viaje = cuota.plan_pago.viaje
            inscripciones = Inscripcion.objects.filter(viaje=viaje, estado__in=['pendiente', 'confirmado']).select_related('padre_tutor__usuario')
            for inscripcion in inscripciones:
                if inscripcion.pagos.filter(estado='verificado', cuota=cuota).exists():
                    continue
                tutor = inscripcion.padre_tutor.usuario
                cache_key = 'recordatorio:' + str(cuota.id) + ':' + str(tutor.id) + ':' + str(trigger) + ':' + str(hoy)
                if cache.get(cache_key):
                    continue
                send_mail(subject='Recordatorio - ' + viaje.nombre, message='Tu cuota vence en ' + str(trigger) + ' dias.', from_email=settings.DEFAULT_FROM_EMAIL, recipient_list=[tutor.email], fail_silently=True)
                Notificacion.objects.create(usuario=tutor, tipo='recordatorio', titulo='Recordatorio de pago', mensaje='Cuota de ' + viaje.nombre + ' vence en ' + str(trigger) + ' dias.', referencia_id=cuota.id, referencia_tipo='Cuota')
                cache.set(cache_key, True, timeout=86400)
                enviados += 1
    return 'OK: ' + str(enviados) + ' recordatorios enviados'