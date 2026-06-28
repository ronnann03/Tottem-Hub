from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Viaje, Itinerario


@receiver(post_save, sender=Viaje)
def create_itinerario_for_viaje(sender, instance, created, **kwargs):
    """
    Crea un Itinerario automáticamente cuando se crea un nuevo Viaje.
    Utiliza get_or_create para asegurar la idempotencia y evitar
    violaciones de la restricción OneToOne.
    """
    if created:
        Itinerario.objects.get_or_create(viaje=instance)
