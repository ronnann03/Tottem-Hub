import uuid
from django.db import models


class Notificacion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usuario = models.ForeignKey(
        'autenticacion.Usuario',
        on_delete=models.CASCADE,
        related_name='notificaciones'
    )
    tipo = models.CharField(
        max_length=20,
        choices=[
            ('pago_vencido','Pago vencido'),
            ('doc_rechazado','Documento rechazado'),
            ('doc_validado','Documento validado'),
            ('comunicado','Comunicado'),
            ('recordatorio','Recordatorio'),
        ]
    )
    titulo = models.CharField(max_length=200)
    mensaje = models.TextField()
    leida = models.BooleanField(default=False)
    referencia_id = models.UUIDField(null=True, blank=True)
    referencia_tipo = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Notificacion'
        ordering = ['-created_at']

    def __str__(self):
        return self.titulo + ' -> ' + str(self.usuario)
