import uuid
from django.db import models
from django.core.exceptions import ValidationError


class Pago(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    inscripcion = models.ForeignKey(
        'inscripciones.Inscripcion',
        on_delete=models.PROTECT,
        related_name='pagos'
    )
    cuota = models.ForeignKey(
        'viajes.Cuota',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='pagos'
    )
    pagado_por = models.ForeignKey(
        'autenticacion.Usuario',
        on_delete=models.PROTECT,
        related_name='pagos_realizados'
    )
    registrado_por = models.ForeignKey(
        'autenticacion.Usuario',
        on_delete=models.PROTECT,
        related_name='pagos_registrados'
    )
    importe = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_pago = models.DateField()
    metodo_pago = models.CharField(
        max_length=20,
        choices=[('transferencia','Transferencia'),('efectivo','Efectivo'),('tarjeta','Tarjeta'),('otro','Otro')]
    )
    comprobante = models.FileField(
        upload_to='pagos/comprobantes/%Y/%m/',
        null=True, blank=True
    )
    estado = models.CharField(
        max_length=20,
        choices=[('pendiente','Pendiente'),('verificado','Verificado'),('rechazado','Rechazado')],
        default='pendiente'
    )
    notas = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Pago'
        verbose_name_plural = 'Pagos'
        constraints = [
            models.CheckConstraint(check=models.Q(importe__gt=0), name='pago_importe_positivo')
        ]

    def __str__(self):
        return str(self.inscripcion) + ' - ' + str(self.importe)
