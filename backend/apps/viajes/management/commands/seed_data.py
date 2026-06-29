from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, timedelta
import uuid

class Command(BaseCommand):
    help = 'Crea datos de prueba para Tottem Hub'

    def handle(self, *args, **kwargs):
        from apps.agencias.models import Agencia
        from apps.autenticacion.models import Usuario
        from apps.viajes.models import Viaje
        from apps.colegios.models import Colegio

        self.stdout.write('Creando datos de prueba...')

        # 1. Agencia
        agencia, _ = Agencia.objects.get_or_create(
            nombre='Tottem Travel',
            defaults={
                'ruc': '20123456789',
                'email': 'contacto@tottemtravel.com',
                'telefono': '999888777',
                'direccion': 'Av. Larco 123, Miraflores, Lima',
            }
        )
        self.stdout.write(f'  ✓ Agencia: {agencia.nombre}')

        # 2. Usuario agente
        agente, created = Usuario.objects.get_or_create(
            email='agente@tottemtravel.com',
            defaults={
                'nombre': 'Carlos',
                'apellidos': 'Mendoza',
                'rol': 'agente',
                'agencia': agencia,
                'email_verificado': True,
                'activo': True,
                'is_staff': False,
            }
        )
        if created:
            agente.set_password('Agente1234!')
            agente.save()
        self.stdout.write(f'  ✓ Agente: {agente.email}')

        # 3. Usuario padre
        padre, created = Usuario.objects.get_or_create(
            email='padre@test.com',
            defaults={
                'nombre': 'María',
                'apellidos': 'González',
                'rol': 'padre',
                'email_verificado': True,
                'activo': True,
            }
        )
        if created:
            padre.set_password('Padre1234!')
            padre.save()
        self.stdout.write(f'  ✓ Padre: {padre.email}')

        # 4. Colegio
        colegio, _ = Colegio.objects.get_or_create(
            nombre='IE San Agustín',
            defaults={
                'departamento': 'Lima',
                'distrito': 'San Isidro',
            }
        )
        self.stdout.write(f'  ✓ Colegio: {colegio.nombre}')

        # 5. Viaje
        viaje, created = Viaje.objects.get_or_create(
            nombre='Cusco Mágico 2026',
            defaults={
                'agencia': agencia,
                'destino': 'Cusco, Peru',
                'fecha_salida': date(2026, 9, 15),
                'fecha_regreso': date(2026, 9, 20),
                'cupo_maximo': 40,
                'precio_total': 1200,
                'estado': 'publicado',
                'descripcion': 'Viaje escolar a la ciudad imperial del Cusco. Incluye Machu Picchu, Valle Sagrado y City Tour.',
                'nivel_educativo': 'secundaria',
                'grado': '5to',
                'colegio': 'IE San Agustín',
                'num_cuotas': 3,
            }
        )
        self.stdout.write(f'  ✓ Viaje: {viaje.nombre} (slug: {viaje.slug})')

        # 6. Segundo viaje
        viaje2, created = Viaje.objects.get_or_create(
            nombre='Arequipa Aventura 2026',
            defaults={
                'agencia': agencia,
                'destino': 'Arequipa, Peru',
                'fecha_salida': date(2026, 10, 10),
                'fecha_regreso': date(2026, 10, 14),
                'cupo_maximo': 30,
                'precio_total': 900,
                'estado': 'publicado',
                'descripcion': 'Descubre la Ciudad Blanca. Colca, volcanes y gastronomia arequipeña.',
                'nivel_educativo': 'secundaria',
                'grado': '4to',
                'colegio': 'IE San Agustín',
                'num_cuotas': 2,
            }
        )
        self.stdout.write(f'  ✓ Viaje: {viaje2.nombre} (slug: {viaje2.slug})')

        self.stdout.write(self.style.SUCCESS('\n✅ Seed data creado exitosamente!'))
        self.stdout.write('\nCredenciales:')
        self.stdout.write('  Agente:  agente@tottemtravel.com / Agente1234!')
        self.stdout.write('  Padre:   padre@test.com / Padre1234!')
        self.stdout.write('  Admin:   admin@tottem.com / (la que creaste)')
        self.stdout.write(f'\nViajes publicados:')
        self.stdout.write(f'  /viajes/{viaje.slug}')
        self.stdout.write(f'  /viajes/{viaje2.slug}')
