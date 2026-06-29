import uuid
from django.db import models


class DocumentoEntregado(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    inscripcion = models.ForeignKey(
        'inscripciones.Inscripcion',
        on_delete=models.CASCADE,
        related_name='documentos'
    )
    documento_requerido = models.ForeignKey(
        'viajes.DocumentoRequerido',
        on_delete=models.PROTECT,
        related_name='entregas'
    )
    archivo = models.FileField(upload_to='documentos/%Y/%m/')
    nombre_archivo = models.CharField(max_length=255)
    tamano_bytes = models.PositiveIntegerField()
    estado = models.CharField(
        max_length=20,
        choices=[('pendiente','Pendiente'),('validado','Validado'),('rechazado','Rechazado')],
        default='pendiente'
    )
    motivo_rechazo = models.TextField(blank=True)
    validado_por = models.ForeignKey(
        'autenticacion.Usuario',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='documentos_validados'
    )
    fecha_validacion = models.DateTimeField(null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Documento Entregado'
        indexes = [
            models.Index(fields=['inscripcion', 'estado']),
            models.Index(fields=['documento_requerido', 'estado']),
        ]

    @property
    def tamano_legible(self):
        if self.tamano_bytes < 1024 * 1024:
            return str(round(self.tamano_bytes / 1024, 1)) + ' KB'
        return str(round(self.tamano_bytes / (1024 * 1024), 1)) + ' MB'

    def __str__(self):
        return self.nombre_archivo + ' (' + self.estado + ')'
