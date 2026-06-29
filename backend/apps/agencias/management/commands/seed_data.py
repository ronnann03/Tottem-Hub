import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.agencias.models import Agencia
from apps.autenticacion.models import Usuario
from apps.viajes.models import Viaje, Itinerario, EtapaItinerario, Actividad, EstadoViaje, TipoActividad

class Command(BaseCommand):
    help = 'Genera datos semilla para Tottem Hub (Agencia, Viaje, Itinerario)'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Eliminando datos existentes de prueba...'))
        
        # Limpiar datos para que sea idempotente
        Agencia.objects.filter(slug='agencia-tottem-demo').delete()
        Usuario.objects.filter(email='agente@tottem.com').delete()
        
        self.stdout.write('Creando Agencia Demo...')
        agencia = Agencia.objects.create(
            nombre='Tottem Viajes Demo',
            slug='agencia-tottem-demo',
            email_contacto='contacto@tottemdemo.com',
            telefono='999888777',
            activa=True
        )

        self.stdout.write('Creando Usuario Agente...')
        Usuario.objects.create_user(
            email='agente@tottem.com',
            password='password123',
            nombre='Agente',
            apellidos='Demo',
            rol='agente',
            agencia=agencia
        )

        self.stdout.write('Creando Viaje de Fin de Curso...')
        fecha_salida = timezone.now().date() + timedelta(days=60)
        fecha_regreso = fecha_salida + timedelta(days=5)
        
        viaje = Viaje.objects.create(
            agencia=agencia,
            nombre='Viaje de Fin de Curso a Bariloche',
            destino='Bariloche, Argentina',
            fecha_salida=fecha_salida,
            fecha_regreso=fecha_regreso,
            descripcion='El mejor viaje de egresados, con todas las actividades incluidas y máxima seguridad.',
            cupo_maximo=50,
            precio_total=1500.00,
            estado=EstadoViaje.ACTIVO,
            colegio='Colegio San Agustin',
            nivel_educativo='Secundaria',
            grado='5to'
        )

        self.stdout.write('Creando Itinerario del Viaje...')
        itinerario = viaje.itinerario
        
        # Día 1
        etapa1 = EtapaItinerario.objects.create(
            itinerario=itinerario,
            dia_numero=1,
            titulo='Llegada a Bariloche y Bienvenida',
            descripcion='Recepción en el aeropuerto y traslado al hotel exclusivo.',
            codigo='DIA-1',
            slug='dia-1'
        )
        Actividad.objects.create(etapa=etapa1, titulo='Vuelo a Bariloche', tipo=TipoActividad.VUELO, orden=1)
        Actividad.objects.create(etapa=etapa1, titulo='Check-in Hotel', tipo=TipoActividad.HOTEL, orden=2)
        Actividad.objects.create(etapa=etapa1, titulo='Cena de Bienvenida', tipo=TipoActividad.COMIDA, orden=3)

        # Día 2
        etapa2 = EtapaItinerario.objects.create(
            itinerario=itinerario,
            dia_numero=2,
            titulo='Aventura en la Nieve',
            descripcion='Día completo en Cerro Catedral aprendiendo a esquiar.',
            codigo='DIA-2',
            slug='dia-2'
        )
        Actividad.objects.create(etapa=etapa2, titulo='Desayuno', tipo=TipoActividad.COMIDA, orden=1)
        Actividad.objects.create(etapa=etapa2, titulo='Clases de Ski en Cerro Catedral', tipo=TipoActividad.EXCURSION, orden=2)
        
        self.stdout.write(self.style.SUCCESS('==========================================='))
        self.stdout.write(self.style.SUCCESS('¡Seed Data generado correctamente!'))
        self.stdout.write(self.style.SUCCESS(f'Viaje creado: {viaje.nombre}'))
        self.stdout.write(self.style.SUCCESS(f'ID del Viaje para la URL del Wizard: {viaje.id}'))
        self.stdout.write(self.style.SUCCESS('==========================================='))
