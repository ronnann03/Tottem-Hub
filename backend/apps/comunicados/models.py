import uuid
from django.db import models


class Comunicado(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    viaje = models.ForeignKey(
        'viajes.Viaje',
        on_delete=models.CASCADE,
        related_name='comunicados'
    )
    autor = models.ForeignKey(
        'autenticacion.Usuario',
        on_delete=models.PROTECT,
        related_name='comunicados_enviados'
    )
    titulo = models.CharField(max_length=300)
    cuerpo = models.TextField()
    enviado_email = models.BooleanField(default=False)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Comunicado'
        ordering = ['-fecha_publicacion']

    def __str__(self):
        return self.titulo
