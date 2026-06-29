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


class PreferenciasNotificacion(models.Model):
    CANAL_CHOICES = [
        ('email', 'Email'),
        ('push', 'Push'),
        ('ambos', 'Email y Push'),
        ('ninguno', 'Ninguno'),
    ]
    usuario = models.OneToOneField(
        'autenticacion.Usuario',
        on_delete=models.CASCADE,
        related_name='preferencias_notificacion'
    )
    canal_preferido = models.CharField(max_length=10, choices=CANAL_CHOICES, default='email')
    horario_inicio = models.TimeField(default='08:00')
    horario_fin = models.TimeField(default='21:00')
    max_por_dia = models.PositiveIntegerField(default=5)
    recibir_recordatorios = models.BooleanField(default=True)
    recibir_comunicados = models.BooleanField(default=True)
    recibir_alertas_docs = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Preferencias de Notificacion'

    def __str__(self):
        return 'Prefs de ' + str(self.usuario)
