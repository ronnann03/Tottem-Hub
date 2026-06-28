import uuid
from django.db import models
from django.db.models import Sum


class Alumno(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usuario = models.OneToOneField(
        'autenticacion.Usuario',
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='perfil_alumno'
    )
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=150)
    fecha_nacimiento = models.DateField()
    dni = models.CharField(max_length=20)
    num_pasaporte = models.CharField(max_length=30, blank=True)
    necesidades_especiales = models.TextField(blank=True)
    nombre_tutor_legal = models.CharField(max_length=200)
    telefono_emergencia = models.CharField(max_length=20)
    tutores = models.ManyToManyField('autenticacion.PadreTutor', blank=True, related_name='alumnos')
    grupo = models.ForeignKey(
        'viajes.Grupo',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='alumnos_inscritos'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Alumno'
        indexes = [models.Index(fields=['dni'])]

    def __str__(self):
        return self.nombre + ' ' + self.apellidos


class Inscripcion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    alumno = models.ForeignKey(Alumno, on_delete=models.PROTECT, related_name='inscripciones')
    viaje = models.ForeignKey('viajes.Viaje', on_delete=models.PROTECT, related_name='inscripciones')
    padre_tutor = models.ForeignKey('autenticacion.PadreTutor', on_delete=models.PROTECT, related_name='inscripciones')
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(
        max_length=20,
        choices=[('pendiente','Pendiente'),('confirmado','Confirmado'),('cancelado','Cancelado'),('baja','Baja')],
        default='pendiente'
    )
    notas_internas = models.TextField(blank=True)
    precio_final = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Inscripcion'
        unique_together = [('alumno', 'viaje')]
        indexes = [
            models.Index(fields=['viaje', 'estado']),
            models.Index(fields=['padre_tutor']),
        ]

    @property
    def total_pagado(self):
        result = self.pagos.filter(estado='verificado').aggregate(total=Sum('importe'))['total']
        return result or 0

    @property
    def saldo_pendiente(self):
        return self.precio_final - self.total_pagado

    @property
    def porcentaje_pagado(self):
        if self.precio_final == 0:
            return 0
        return round(float(self.total_pagado) / float(self.precio_final) * 100, 2)

    def __str__(self):
        return str(self.alumno) + ' - ' + str(self.viaje)
