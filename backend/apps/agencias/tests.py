"""
apps/agencias/tests.py — Tests de TASK-012: GET/PATCH /api/v1/agencias/perfil/

Suite: 10 tests
Cobertura: autenticación, autorización, GET (perfil completo, aislamiento tenant,
           agente sin agencia), PATCH (parcial, campos read-only, email duplicado,
           email inválido).

Estrategia de auth: force_authenticate() — el mecanismo JWT cookie→header
se valida en los tests de autenticación de TASK-010. Aquí se testa la lógica
de negocio de los endpoints de agencia.
"""

import uuid

from django.test import TestCase
from rest_framework.test import APIClient

from apps.agencias.models import Agencia
from apps.autenticacion.models import RolUsuario, Usuario

URL = "/api/v1/agencias/perfil/"


# ─── Helpers ──────────────────────────────────────────────────────────────────

def _agencia(**kwargs) -> Agencia:
    defaults = {
        "nombre": "Totem Travel",
        "email_contacto": f"info+{uuid.uuid4().hex[:8]}@totem.com",
        "telefono": "+51 999 000 000",
        "slug": f"totem-{uuid.uuid4().hex[:6]}",
    }
    defaults.update(kwargs)
    return Agencia.objects.create(**defaults)


def _agente(agencia=None, **kwargs) -> Usuario:
    defaults = {
        "email": f"agente+{uuid.uuid4().hex[:8]}@totem.com",
        "nombre": "Carlos",
        "apellidos": "Pérez",
        "rol": RolUsuario.AGENTE,
        "email_verificado": True,
        "activo": True,
        "agencia": agencia,
    }
    defaults.update(kwargs)
    return Usuario.objects.create_user(password="Pass1234!", **defaults)


def _padre(**kwargs) -> Usuario:
    defaults = {
        "email": f"padre+{uuid.uuid4().hex[:8]}@test.com",
        "nombre": "Ana",
        "apellidos": "García",
        "rol": RolUsuario.PADRE,
        "email_verificado": True,
        "activo": True,
    }
    defaults.update(kwargs)
    return Usuario.objects.create_user(password="Pass1234!", **defaults)


# ─── GET /agencias/perfil/ ────────────────────────────────────────────────────

class AgenciaPerfilGetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.agencia = _agencia()
        self.agente = _agente(agencia=self.agencia)

    def test_retorna_perfil_completo_con_todos_los_campos(self):
        self.client.force_authenticate(user=self.agente)
        response = self.client.get(URL)

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["nombre"], self.agencia.nombre)
        self.assertEqual(data["email_contacto"], self.agencia.email_contacto)
        self.assertEqual(data["slug"], self.agencia.slug)
        for campo in ("id", "telefono", "licencia_agencia", "activa", "created_at"):
            self.assertIn(campo, data)

    def test_sin_autenticacion_retorna_401(self):
        response = self.client.get(URL)
        self.assertEqual(response.status_code, 401)

    def test_rol_padre_retorna_403(self):
        self.client.force_authenticate(user=_padre())
        response = self.client.get(URL)
        self.assertEqual(response.status_code, 403)

    def test_agente_sin_agencia_retorna_404(self):
        self.client.force_authenticate(user=_agente(agencia=None))
        response = self.client.get(URL)
        self.assertEqual(response.status_code, 404)

    def test_aislamiento_tenant_agente_solo_ve_su_agencia(self):
        otra_agencia = _agencia(nombre="Otra Agencia")
        otro_agente = _agente(agencia=otra_agencia)
        self.client.force_authenticate(user=otro_agente)

        response = self.client.get(URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["nombre"], otra_agencia.nombre)
        self.assertNotEqual(response.json()["nombre"], self.agencia.nombre)


# ─── PATCH /agencias/perfil/ ─────────────────────────────────────────────────

class AgenciaPerfilPatchTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.agencia = _agencia(nombre="Original", telefono="+51 111 111")
        self.agente = _agente(agencia=self.agencia)

    def test_patch_nombre_actualiza_y_retorna_200(self):
        self.client.force_authenticate(user=self.agente)
        response = self.client.patch(URL, data={"nombre": "Nuevo Nombre"}, format="json")

        self.assertEqual(response.status_code, 200)
        self.agencia.refresh_from_db()
        self.assertEqual(self.agencia.nombre, "Nuevo Nombre")

    def test_patch_telefono_y_email_contacto_simultaneos(self):
        nuevo_email = f"nuevo+{uuid.uuid4().hex[:6]}@totem.com"
        self.client.force_authenticate(user=self.agente)
        response = self.client.patch(
            URL,
            data={"telefono": "+51 999 777", "email_contacto": nuevo_email},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.agencia.refresh_from_db()
        self.assertEqual(self.agencia.telefono, "+51 999 777")
        self.assertEqual(self.agencia.email_contacto, nuevo_email)

    def test_patch_es_parcial_no_modifica_campos_no_enviados(self):
        nombre_original = self.agencia.nombre
        self.client.force_authenticate(user=self.agente)
        response = self.client.patch(URL, data={"telefono": "+51 888"}, format="json")

        self.assertEqual(response.status_code, 200)
        self.agencia.refresh_from_db()
        self.assertEqual(self.agencia.nombre, nombre_original)
        self.assertEqual(self.agencia.telefono, "+51 888")

    def test_patch_slug_es_ignorado_campo_read_only(self):
        slug_original = self.agencia.slug
        self.client.force_authenticate(user=self.agente)
        response = self.client.patch(URL, data={"slug": "slug-inyectado"}, format="json")

        self.assertEqual(response.status_code, 200)
        self.agencia.refresh_from_db()
        self.assertEqual(self.agencia.slug, slug_original)

    def test_patch_email_contacto_invalido_retorna_400(self):
        self.client.force_authenticate(user=self.agente)
        response = self.client.patch(
            URL, data={"email_contacto": "no-es-un-email"}, format="json"
        )
        self.assertEqual(response.status_code, 400)

    def test_patch_email_contacto_duplicado_retorna_400(self):
        otra_agencia = _agencia()
        self.client.force_authenticate(user=self.agente)
        response = self.client.patch(
            URL,
            data={"email_contacto": otra_agencia.email_contacto},
            format="json",
        )
        self.assertEqual(response.status_code, 400)

    def test_patch_sin_autenticacion_retorna_401(self):
        response = self.client.patch(URL, data={"nombre": "X"}, format="json")
        self.assertEqual(response.status_code, 401)

    def test_patch_rol_padre_retorna_403(self):
        self.client.force_authenticate(user=_padre())
        response = self.client.patch(URL, data={"nombre": "X"}, format="json")
        self.assertEqual(response.status_code, 403)
