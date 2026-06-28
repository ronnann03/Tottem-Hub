# API.md — Endpoints REST

## Convenciones

- **Base URL:** `/api/v1/`
- **Autenticación:** JWT. Header: `Authorization: Bearer <access_token>`
- **Formato:** JSON (request y response)
- **Paginación:** aplicar en listados (offset/limit o page/page_size)
- **Permisos:** indicados por rol. `[agente]` = solo rol agente. `[padre]` = padre/tutor. `[any]` = cualquier autenticado.
- **Refresh:** `POST /auth/refresh/` para renovar access_token usando refresh_token

---

## Auth

### POST `/auth/registro/`
Crea nuevo usuario. Envía email de verificación.

**Payload:**
```json
{
  "email": "string",
  "password": "string",
  "nombre": "string",
  "apellidos": "string",
  "rol": "padre | alumno | mecenas",
  "telefono": "string (opcional)"
}
```
**Respuesta:** `201 Created` `{ "mensaje": "Revisa tu email para activar tu cuenta" }`

---

### GET `/auth/verificar/?token=<TOKEN>`
Activa la cuenta del usuario.

**Respuesta:** Redirect a `/login` con mensaje de éxito.  
**Error:** `400 Bad Request` si token inválido o expirado.

---

### POST `/auth/login/`
Genera par de tokens JWT. Los tokens se establecen como cookies `httpOnly` (DEC-002).

**Payload:**
```json
{ "email": "string", "password": "string" }
```
**Respuesta:** `200 OK`
```json
{ "rol": "padre | agente | alumno | mecenas", "agencia_id": "uuid | null" }
```
**Cookies establecidas:**
- `access_token` — `HttpOnly; Secure; SameSite=Strict; Path=/; Max-Age=900`
- `refresh_token` — `HttpOnly; Secure; SameSite=Strict; Path=/api/v1/auth/; Max-Age=604800`

**Errores:**
- `401` — credenciales inválidas (email no registrado o contraseña incorrecta — misma respuesta)
- `403` — email no verificado
- `403` — cuenta inactiva

---

### POST `/auth/refresh/`
Renueva el access_token.

**Payload:** `{ "refresh_token": "string" }`  
**Respuesta:** `{ "access_token": "string" }`

---

### POST `/auth/logout/`
Invalida el refresh_token en Redis.

---

## Agencia

### GET `/agencias/perfil/` `[agente]`
Obtiene el perfil de la agencia del agente autenticado.

**Respuesta:** `200 OK`
```json
{
  "id": "uuid",
  "nombre": "Totem Travel",
  "logo": "http://host/media/agencias/logos/logo.png",
  "email_contacto": "info@totemtravel.com",
  "telefono": "+51 999 000 000",
  "licencia_agencia": "LIC-001",
  "slug": "totem",
  "activa": true,
  "created_at": "2026-06-28T00:00:00Z"
}
```

**Errores:**
- `401` — sin autenticación
- `403` — rol distinto de `agente`
- `404` — agente sin agencia asignada

---

### PATCH `/agencias/perfil/` `[agente]`
Actualiza nombre, logo, teléfono o email_contacto. Todos los campos son opcionales (PATCH parcial).

**Payload:** `multipart/form-data` (si incluye logo) o `application/json`
```json
{
  "nombre": "string (opcional)",
  "logo": "file (opcional, ImageField)",
  "telefono": "string (opcional)",
  "email_contacto": "email (opcional)"
}
```
**Respuesta:** `200 OK` — objeto `Agencia` completo (mismo schema que GET)

**Campos read-only** (ignorados si se envían): `id`, `slug`, `licencia_agencia`, `activa`, `created_at`

**Errores:**
- `400` — `email_contacto` inválido o ya existe en otra agencia
- `401` — sin autenticación
- `403` — rol distinto de `agente`
- `404` — agente sin agencia asignada

---

## Viajes

### GET `/viajes/` `[agente]`
Lista todos los viajes de la agencia. Filtros: `estado`, `fecha_salida`.

### POST `/viajes/` `[agente]`
Crea nuevo viaje. El estado inicial es `borrador`. Crea `Itinerario` vacío automáticamente.

**Payload:**
```json
{
  "nombre": "string",
  "destino": "string",
  "fecha_salida": "YYYY-MM-DD",
  "fecha_regreso": "YYYY-MM-DD",
  "cupo_maximo": 50,
  "precio_total": "850.00",
  "descripcion": "string (opcional)",
  "imagen": "file (multipart, opcional)"
}
```
**Respuesta:** `201 Created` `{ "viaje_id": "uuid", "estado": "borrador" }`

---

### GET `/viajes/{viaje_id}/` `[agente | padre | alumno]`
Detalle del viaje. Para padre/alumno: solo si el viaje está `activo` y tienen inscripción.

### PATCH `/viajes/{viaje_id}/` `[agente]`
Actualiza campos. Para activar: `{ "estado": "activo" }`.

### DELETE `/viajes/{viaje_id}/` `[agente]`
Solo si estado es `borrador` y sin inscripciones.

---

### GET `/viajes/{viaje_id}/metricas/` `[agente]`
Panel de métricas del viaje.

**Respuesta:**
```json
{
  "total_inscritos": 45,
  "cupo_maximo": 50,
  "porcentaje_inscripcion": 90.0,
  "total_pagado": 12500.00,
  "total_esperado": 38250.00,
  "porcentaje_pagado": 32.7,
  "documentos_completos": 30,
  "documentos_pendientes": 15,
  "porcentaje_documentado": 66.7
}
```

---

## Plan de Pagos

### POST `/viajes/{viaje_id}/plan-pago/` `[agente]`
Crea el plan de pagos del viaje.

**Payload:**
```json
{
  "descripcion": "string (opcional)",
  "total_cuotas": 3,
  "cuotas": [
    { "numero_cuota": 1, "descripcion": "Reserva", "importe": "200.00", "fecha_vencimiento": "YYYY-MM-DD" },
    { "numero_cuota": 2, "descripcion": "2ª cuota", "importe": "300.00", "fecha_vencimiento": "YYYY-MM-DD" },
    { "numero_cuota": 3, "descripcion": "Saldo final", "importe": "350.00", "fecha_vencimiento": "YYYY-MM-DD" }
  ]
}
```

### GET `/viajes/{viaje_id}/plan-pago/` `[any]`
Obtiene el plan de pagos con sus cuotas.

### PATCH `/viajes/{viaje_id}/plan-pago/` `[agente]`
Actualiza plan (solo si no hay pagos verificados).

---

## Hoteles

### GET `/viajes/{viaje_id}/hoteles/` `[agente]`
Lista hoteles del viaje.

**Respuesta:** `200 OK` — array de objetos `Hotel`
```json
[
  {
    "id": "uuid",
    "nombre": "Hotel Sol",
    "descripcion": "string",
    "tasa_turistica": "15.00 | null",
    "fianza": "100.00 | null",
    "web_url": "string",
    "maps_url": "string",
    "imagen": "url | null"
  }
]
```

---

### POST `/viajes/{viaje_id}/hoteles/` `[agente]`
Crea un hotel vinculado al viaje.

**Payload:** `multipart/form-data` (si incluye imagen) o `application/json`
```json
{
  "nombre": "Hotel Sol",
  "descripcion": "string (opcional)",
  "tasa_turistica": "15.00 (opcional)",
  "fianza": "100.00 (opcional)",
  "web_url": "string (opcional)",
  "maps_url": "string (opcional)",
  "imagen": "file (opcional)"
}
```
**Respuesta:** `201 Created` — objeto `Hotel` creado

**Errores:**
- `401` — sin autenticación
- `403` — rol distinto de `agente`
- `404` — viaje no existe en la agencia

---

### GET `/viajes/{viaje_id}/hoteles/{hotel_id}/` `[agente]`
Detalle de un hotel.

---

### PATCH `/viajes/{viaje_id}/hoteles/{hotel_id}/` `[agente]`
Actualiza campos del hotel (PATCH parcial).

**Respuesta:** `200 OK` — objeto `Hotel` actualizado

**Errores:**
- `404` — hotel no pertenece a este viaje/agencia

---

### DELETE `/viajes/{viaje_id}/hoteles/{hotel_id}/` `[agente]`
Elimina el hotel.

**Respuesta:** `204 No Content`

---

## Grupos

### GET `/viajes/{viaje_id}/grupos/` `[agente]`
Lista grupos del viaje.

**Respuesta:** `200 OK` — array de objetos `Grupo`
```json
[
  {
    "id": "uuid",
    "nombre": "Grupo A",
    "descripcion": "string",
    "capacidad": 25,
    "created_at": "2026-06-28T00:00:00Z"
  }
]
```

---

### POST `/viajes/{viaje_id}/grupos/` `[agente]`
Crea un grupo en el viaje.

**Payload:**
```json
{
  "nombre": "Grupo A",
  "descripcion": "string (opcional)",
  "capacidad": 25
}
```
**Respuesta:** `201 Created` — objeto `Grupo` creado

**Errores:**
- `400` — `nombre` ya existe en este viaje
- `404` — viaje no existe en la agencia

---

### GET `/viajes/{viaje_id}/grupos/{grupo_id}/` `[agente]`
Detalle de un grupo.

---

### PATCH `/viajes/{viaje_id}/grupos/{grupo_id}/` `[agente]`
Actualiza campos del grupo (PATCH parcial).

**Errores:**
- `400` — `nombre` duplicado en este viaje
- `404` — grupo no pertenece a este viaje/agencia

---

### DELETE `/viajes/{viaje_id}/grupos/{grupo_id}/` `[agente]`
Elimina el grupo.

**Respuesta:** `204 No Content`

---

### POST `/viajes/{viaje_id}/grupos/{grupo_id}/alumnos/` `[agente]`
Asigna una lista de alumnos al grupo. La operación es **idempotente**: añadir un alumno ya asignado es un no-op.

**Payload:**
```json
{ "alumno_ids": ["uuid1", "uuid2"] }
```

**Respuesta:** `200 OK`
```json
{ "asignados": 2, "total_en_grupo": 3 }
```

**Errores:**
- `400` — IDs duplicados en el payload
- `400` — algún ID no pertenece a un alumno de esta agencia
- `400` — la asignación excedería la `capacidad` del grupo (si está definida)
- `404` — viaje o grupo no pertenecen a la agencia

---

## Itinerario

### GET `/viajes/{viaje_id}/itinerario/` `[agente]`
Retorna el itinerario completo con etapas y actividades anidadas.

**Respuesta:** `200 OK`
```json
{
  "id": "uuid",
  "viaje": "uuid",
  "created_at": "2026-06-28T00:00:00Z",
  "updated_at": "2026-06-28T00:00:00Z",
  "etapas": [
    {
      "id": "uuid",
      "dia_numero": 1,
      "titulo": "Llegada a Madrid",
      "descripcion": "string",
      "imagen": "url | null",
      "actividades": [
        {
          "id": "uuid",
          "hora": "09:00:00 | null",
          "titulo": "Traslado al hotel",
          "descripcion": "string",
          "tipo": "vuelo | bus | hotel | comida | excursion | libre | otro | null",
          "orden": 0
        }
      ]
    }
  ]
}
```

**Errores:**
- `401` — sin autenticación
- `403` — rol distinto de `agente`
- `404` — viaje no existe en la agencia o itinerario no existe

---

### GET `/viajes/{viaje_id}/etapas/` `[agente]`
Lista las etapas del itinerario (sin actividades anidadas).

**Respuesta:** `200 OK` — array de objetos `EtapaItinerario`

---

### POST `/viajes/{viaje_id}/etapas/` `[agente]`
Crea una nueva etapa en el itinerario.

**Payload:**
```json
{
  "dia_numero": 1,
  "titulo": "Llegada a Madrid",
  "descripcion": "string (opcional)",
  "imagen": "file (multipart, opcional)"
}
```

**Respuesta:** `201 Created` — objeto `EtapaItinerario` creado

**Errores:**
- `400` — `dia_numero` ya existe en este itinerario
- `400` — `dia_numero` < 1

---

### GET `/viajes/{viaje_id}/etapas/{etapa_id}/` `[agente]`
Detalle de una etapa.

---

### PATCH `/viajes/{viaje_id}/etapas/{etapa_id}/` `[agente]`
Actualiza campos de la etapa (PATCH parcial).

**Payload:** cualquier subconjunto de `{ "dia_numero", "titulo", "descripcion", "imagen" }`

**Errores:**
- `400` — `dia_numero` ya existe en este itinerario

---

### DELETE `/viajes/{viaje_id}/etapas/{etapa_id}/` `[agente]`
Elimina la etapa y todas sus actividades (CASCADE).

**Respuesta:** `204 No Content`

---

### GET `/viajes/{viaje_id}/etapas/{etapa_id}/actividades/` `[agente]`
Lista actividades de la etapa, ordenadas por `orden`, `hora`.

---

### POST `/viajes/{viaje_id}/etapas/{etapa_id}/actividades/` `[agente]`
Crea una actividad en la etapa.

**Payload:**
```json
{
  "titulo": "Traslado al hotel",
  "hora": "09:00 (opcional)",
  "descripcion": "string (opcional)",
  "tipo": "vuelo | bus | hotel | comida | excursion | libre | otro (opcional)"
}
```

> `orden` es ignorado en este endpoint — se asigna automáticamente (default 0).

**Respuesta:** `201 Created`

---

### GET `/viajes/{viaje_id}/etapas/{etapa_id}/actividades/{actividad_id}/` `[agente]`
Detalle de una actividad.

---

### PATCH `/viajes/{viaje_id}/etapas/{etapa_id}/actividades/{actividad_id}/` `[agente]`
Actualiza campos de la actividad (PATCH parcial). El campo `orden` es **read-only** y será ignorado.

**Payload:** cualquier subconjunto de `{ "titulo", "hora", "descripcion", "tipo" }`

---

### DELETE `/viajes/{viaje_id}/etapas/{etapa_id}/actividades/{actividad_id}/` `[agente]`
Elimina la actividad.

**Respuesta:** `204 No Content`

---

### PATCH `/viajes/{viaje_id}/etapas/{etapa_id}/actividades/reordenar/` `[agente]`
Actualiza el campo `orden` de múltiples actividades en una sola transacción. Es el **único** endpoint que modifica `orden`.

**Payload:**
```json
{
  "actividades": [
    { "id": "uuid", "orden": 0 },
    { "id": "uuid", "orden": 1 },
    { "id": "uuid", "orden": 2 }
  ]
}
```

**Respuesta:** `200 OK` — array completo de actividades de la etapa con `orden` actualizado

**Errores:**
- `400` — IDs duplicados en el payload
- `400` — algún ID no pertenece a esta etapa
- `400` — payload `actividades` vacío

---

## Documentos Requeridos

### GET `/viajes/{viaje_id}/documentos-requeridos/` `[any autenticado]`
Lista documentos requeridos del viaje.

### POST `/viajes/{viaje_id}/documentos-requeridos/` `[agente]`
```json
{ "nombre": "DNI alumno", "descripcion": "", "obligatorio": true, "formatos_permitidos": "pdf,jpg,png" }
```

### PATCH `/documentos-requeridos/{id}/` `[agente]`
### DELETE `/documentos-requeridos/{id}/` `[agente]`

---

## Inscripciones

### GET `/inscripciones/` `[agente]`
Lista de inscripciones. Filtros: `viaje_id`, `estado`, `alumno_id`.

### POST `/inscripciones/` `[padre]`
Inscribe alumno a viaje.

**Payload:**
```json
{
  "viaje_id": "uuid",
  "alumno": {
    "nombre": "string",
    "apellidos": "string",
    "fecha_nacimiento": "YYYY-MM-DD",
    "dni": "string",
    "necesidades_especiales": "string (opcional)",
    "nombre_tutor_legal": "string",
    "telefono_emergencia": "string"
  },
  "padre_tutor_id": "uuid"
}
```
**Errores:** `409 Conflict` sin plazas · `409` alumno ya inscrito  
**Respuesta:** `201 Created` `{ "inscripcion_id": "uuid", "saldo_pendiente": "850.00" }`

### GET `/inscripciones/{id}/` `[agente | padre propietario]`
Detalle de inscripción con pagos, documentos y estado.

### PATCH `/inscripciones/{id}/` `[agente]`
Actualiza `estado` o `notas_internas`.

---

## Pagos

### GET `/inscripciones/{id}/pagos/` `[agente | padre propietario]`
Lista pagos de la inscripción con cuotas pendientes.

### POST `/pagos/` `[padre | mecenas | agente]`
Registra un pago con comprobante (multipart/form-data).

**Campos:**
- `inscripcion_id` (uuid)
- `cuota_id` (uuid, opcional)
- `importe` (decimal)
- `fecha_pago` (date)
- `metodo_pago` (transferencia|efectivo|tarjeta|otro)
- `comprobante` (file, opcional)
- `pagado_por` (uuid usuario, solo agente puede especificarlo)

**Respuesta:** `201 Created` `{ "pago_id": "uuid", "estado": "pendiente" }`

### GET `/pagos/?estado=pendiente&viaje_id={id}` `[agente]`
Lista pagos pendientes de verificación de un viaje.

### PATCH `/pagos/{pago_id}/` `[agente]`
Verifica o rechaza un pago.

```json
{ "estado": "verificado" }
// o
{ "estado": "rechazado", "notas": "El comprobante no corresponde al importe indicado." }
```

---

## Documentos Entregados

### GET `/inscripciones/{id}/documentos/` `[agente | padre propietario]`
Checklist de documentos con estado por documento.

### POST `/documentos/` `[padre]`
Sube un documento (multipart/form-data).

**Campos:**
- `inscripcion_id` (uuid)
- `documento_requerido_id` (uuid)
- `archivo` (file, max 10 MB, formatos según `DocumentoRequerido`)

**Errores:** `400` formato inválido · `400` tamaño excedido  
**Respuesta:** `201 Created` `{ "documento_id": "uuid", "estado": "pendiente" }`

### GET `/documentos/?estado=pendiente&viaje_id={id}` `[agente]`
Lista documentos pendientes de revisión.

### PATCH `/documentos/{id}/` `[agente]`
Valida o rechaza un documento.

```json
{ "estado": "validado" }
// o
{ "estado": "rechazado", "motivo_rechazo": "La póliza está caducada." }
```

---

## Comunicados

### GET `/viajes/{viaje_id}/comunicados/` `[any autenticado con inscripción]`
Lista comunicados del viaje.

### POST `/viajes/{viaje_id}/comunicados/` `[agente]`
Envía comunicado masivo (Celery async).

```json
{ "titulo": "Punto de encuentro Día 1", "cuerpo": "..." }
```

---

## Notificaciones

### GET `/notificaciones/` `[any autenticado]`
Lista notificaciones del usuario autenticado. Filtro: `leida=false`.

### PATCH `/notificaciones/{id}/` `[any autenticado]`
Marca como leída. `{ "leida": true }`

### POST `/notificaciones/marcar-todas/` `[any autenticado]`
Marca todas como leídas.

---

## Mecenas

### GET `/mecenas/{mecenas_id}/alumnos/` `[mecenas]`
Lista alumnos patrocinados.

### POST `/viajes/{viaje_id}/inscripciones/{id}/mecenas/` `[agente]`
Asigna mecenas a inscripción.
```json
{ "mecenas_id": "uuid", "monto_comprometido": "200.00" }
```

---

## Exportaciones

### GET `/viajes/{viaje_id}/exportar/inscritos/` `[agente]`
Exporta listado de inscritos en CSV/Excel. Query param: `formato=csv|xlsx`

### GET `/viajes/{viaje_id}/exportar/pagos/` `[agente]`
Exporta reporte de pagos.

### GET `/viajes/{viaje_id}/exportar/documentacion/` `[agente]`
Exporta estado de documentación.

### GET `/viajes/{viaje_id}/exportar/informe-pdf/` `[agente]`
Genera PDF de estado general del viaje.

---

## Resumen de Inscripción (PDF)

### GET `/inscripciones/{id}/resumen-pdf/` `[padre | alumno]`
Genera y descarga PDF con resumen de inscripción del alumno.

---

## Códigos de Error Estándar

| Código | Significado |
|--------|-------------|
| 400 | Bad Request — validación fallida |
| 401 | Unauthorized — token inválido o ausente |
| 403 | Forbidden — sin permisos para esta acción |
| 404 | Not Found |
| 409 | Conflict — unicidad violada (alumno ya inscrito, sin cupo) |
| 413 | Payload Too Large — archivo > 10 MB |
| 422 | Unprocessable Entity — lógica de negocio |
| 500 | Internal Server Error |
