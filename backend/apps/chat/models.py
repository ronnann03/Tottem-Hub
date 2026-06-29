import uuid
from django.db import models


class Conversacion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    inscripcion = models.OneToOneField(
        'inscripciones.Inscripcion',
        on_delete=models.CASCADE,
        related_name='conversacion'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Conversacion'

    def __str__(self):
        return f"Chat inscripcion {self.inscripcion_id}"


class Mensaje(models.Model):
    ESTADO_CHOICES = [
        ('enviado', 'Enviado'),
        ('leido', 'Leido'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversacion = models.ForeignKey(
        Conversacion,
        on_delete=models.CASCADE,
        related_name='mensajes'
    )
    remitente = models.ForeignKey(
        'autenticacion.Usuario',
        on_delete=models.PROTECT,
        related_name='mensajes_enviados'
    )
    contenido = models.TextField()
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='enviado')
    leido_en = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Mensaje'
        ordering = ['created_at']

    def __str__(self):
        return f"Mensaje de {self.remitente} en {self.conversacion_id}"