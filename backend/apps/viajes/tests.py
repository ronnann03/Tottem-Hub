from django.test import TestCase
from django.db import transaction
from django.utils import timezone
from datetime import timedelta
from apps.viajes.models import Viaje, Itinerario, EstadoViaje
from apps.agencias.models import Agencia


class ViajeSignalTests(TestCase):
    def setUp(self):
        self.agencia = Agencia.objects.create(
            nombre="Agencia Test",
            slug="agencia-test",
            email_contacto="contacto@agenciatest.com",
            telefono="123456789",
        )
        self.today = timezone.now().date()
        self.tomorrow = self.today + timedelta(days=1)

    def create_viaje(self, suffix="1"):
        return Viaje.objects.create(
            agencia=self.agencia,
            nombre=f"Viaje {suffix}",
            destino=f"Destino {suffix}",
            fecha_salida=self.today,
            fecha_regreso=self.tomorrow,
            cupo_maximo=10,
            precio_total=100.00,
            estado=EstadoViaje.BORRADOR
        )

    def test_crear_viaje_crea_itinerario(self):
        # 1. Crear Viaje -> existe Itinerario
        # 5. La señal funciona desde ORM puro
        viaje = self.create_viaje()
        self.assertTrue(Itinerario.objects.filter(viaje=viaje).exists())

    def test_solo_un_itinerario_por_viaje(self):
        # 2. Crear Viaje -> solo un Itinerario
        viaje = self.create_viaje()
        count = Itinerario.objects.filter(viaje=viaje).count()
        self.assertEqual(count, 1)

    def test_guardar_nuevamente_no_crea_duplicado(self):
        # 3. Guardar nuevamente el Viaje -> no crea otro Itinerario
        viaje = self.create_viaje()
        itinerario_inicial_id = viaje.itinerario.id

        viaje.nombre = "Viaje Actualizado"
        viaje.save()

        count = Itinerario.objects.filter(viaje=viaje).count()
        self.assertEqual(count, 1)
        self.assertEqual(viaje.itinerario.id, itinerario_inicial_id)

    def test_crear_multiples_viajes(self):
        # 4. Crear múltiples Viajes -> cada uno obtiene un Itinerario
        viajes = [self.create_viaje(str(i)) for i in range(5)]

        for viaje in viajes:
            self.assertEqual(Itinerario.objects.filter(viaje=viaje).count(), 1)

        self.assertEqual(Itinerario.objects.count(), 5)

    def test_signal_dentro_de_transaccion(self):
        # 6. La señal funciona dentro de transacciones
        with transaction.atomic():
            viaje = self.create_viaje("transaccion")

        self.assertTrue(Itinerario.objects.filter(viaje=viaje).exists())

    def test_no_consultas_innecesarias(self):
        # 7. No aparecen consultas innecesarias
        viaje = self.create_viaje("q1")

        with self.assertNumQueries(1):
            viaje.nombre = "Modificado"
            viaje.save(update_fields=['nombre'])
