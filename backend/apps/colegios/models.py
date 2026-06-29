from django.db import models


class Colegio(models.Model):
    codigo_modular = models.CharField(max_length=20, unique=True, db_index=True)
    nombre = models.CharField(max_length=300, db_index=True)
    departamento = models.CharField(max_length=100)
    provincia = models.CharField(max_length=100)
    distrito = models.CharField(max_length=100)
    nivel = models.CharField(max_length=50, blank=True)
    gestion = models.CharField(max_length=20, blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Colegio'
        ordering = ['nombre']
        indexes = [
            models.Index(fields=['departamento', 'nombre']),
        ]

    def __str__(self):
        return f"{self.nombre} ({self.departamento})"