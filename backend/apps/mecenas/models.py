import uuid
from django.db import models
from django.core.validators import MinValueValidator


class Mecenas(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=200)
    email = models.EmailField()
    telefono = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Mecenas'
        ordering = ['-created_at']

    def __str__(self):
        return self.nombre


class MecenasInscripcion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    mecenas = models.ForeignKey(Mecenas, on_delete=models.CASCADE, related_name='inscripciones_patrocinadas')
    inscripcion = models.ForeignKey('inscripciones.Inscripcion', on_delete=models.CASCADE, related_name='mecenas')
    monto_comprometido = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    monto_pagado = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notas = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Mecenas Inscripcion'
        unique_together = [('mecenas', 'inscripcion')]
        ordering = ['-created_at']

    def __str__(self):
        return self.mecenas.nombre + ' -> ' + str(self.inscripcion)