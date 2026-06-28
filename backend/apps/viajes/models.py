import uuid
from django.db import models
from django.db.models import F, Q
from django.utils.translation import gettext_lazy as _


class EstadoViaje(models.TextChoices):
    BORRADOR = "borrador", _("Borrador")
    ACTIVO = "activo", _("Activo")
    CERRADO = "cerrado", _("Cerrado")
    ARCHIVADO = "archivado", _("Archivado")


class Viaje(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    agencia = models.ForeignKey(
        "agencias.Agencia",
        on_delete=models.CASCADE,
        related_name="viajes"
    )
    nombre = models.CharField(max_length=300)
    destino = models.CharField(max_length=200)
    fecha_salida = models.DateField()
    fecha_regreso = models.DateField()
    descripcion = models.TextField(blank=True, default="")
    cupo_maximo = models.PositiveIntegerField()
    precio_total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(
        max_length=20,
        choices=EstadoViaje.choices,
        default=EstadoViaje.BORRADOR
    )
    imagen = models.ImageField(
        upload_to="viajes/portadas/", null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["agencia", "estado"]),
            models.Index(fields=["fecha_salida"]),
        ]
        constraints = [
            models.CheckConstraint(
                check=Q(fecha_regreso__gt=F("fecha_salida")),
                name="viaje_fecha_regreso_mayor_salida",
                violation_error_message=_(
                    "La fecha de regreso debe ser posterior a la de salida."
                )
            )
        ]
        ordering = ["-fecha_salida"]

    def __str__(self):
        return f"{self.nombre} ({self.destino})"

    @property
    def duracion_dias(self):
        if self.fecha_regreso and self.fecha_salida:
            return (self.fecha_regreso - self.fecha_salida).days
        return 0


class PlanPago(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    viaje = models.OneToOneField(
        Viaje,
        on_delete=models.CASCADE,
        related_name="plan_pago"
    )
    descripcion = models.CharField(max_length=300, blank=True, default="")
    total_cuotas = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Plan de pago - {self.viaje.nombre}"


class Cuota(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    plan_pago = models.ForeignKey(
        PlanPago,
        on_delete=models.CASCADE,
        related_name="cuotas"
    )
    numero_cuota = models.PositiveIntegerField()
    descripcion = models.CharField(max_length=200, blank=True, default="")
    importe = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_vencimiento = models.DateField()

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=Q(importe__gt=0),
                name="cuota_importe_positivo",
                violation_error_message=_(
                    "El importe de la cuota debe ser mayor que 0."
                )
            ),
            models.UniqueConstraint(
                fields=["plan_pago", "numero_cuota"],
                name="unique_cuota_por_plan"
            )
        ]
        ordering = ["numero_cuota"]

    def __str__(self):
        return f"Cuota {self.numero_cuota} - {self.plan_pago.viaje.nombre}"
