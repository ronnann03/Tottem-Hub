# ARCHITECTURE.md — Decisiones de Arquitectura

## Visión General

Arquitectura de tres capas con separación explícita entre frontend, API gateway y backend de lógica de negocio. Multi-tenant por campo (`agencia_id`). Fase 1 opera con un único tenant: Totem Travel.

---

## Diagrama de Componentes

```
┌─────────────────────────────────────────────────────────────────────┐
│                            CLIENTES                                 │
│   Browser / Mobile (Web — responsive mobile-first)                  │
│                                                                     │
│   Next.js 16.2.6 · React 19 · TailwindCSS 4 · Framer Motion        │
│                                                                     │
│  ┌──────────────────┐  ┌─────────────────────┐  ┌───────────────┐  │
│  │  (public)        │  │  (padre) (mecenas)  │  │  (agente)     │  │
│  │  Landing viaje   │  │  Dashboard, pagos   │  │  Backoffice   │  │
│  │  /viajes/{slug}/ │  │  docs, mensajes     │  │  /backoffice/ │  │
│  └────────┬─────────┘  └──────────┬──────────┘  └──────┬────────┘  │
└───────────┼────────────────────────┼───────────────────┼────────────┘
            └────────────────────────┼───────────────────┘
                                     │ HTTPS · JWT (cookie httpOnly)
┌────────────────────────────────────▼────────────────────────────────┐
│                     API GATEWAY — Node.js puro                      │
│              node:http · node:https  (sin Express/Fastify)          │
│                                                                     │
│  • Routing hacia backend Django                                     │
│  • CORS (headers manuales por origen)                               │
│  • Rate limiting (por IP + por endpoint)                            │
│  • Headers de seguridad (HSTS, X-Frame-Options, etc.)               │
│  • Auth forwarding (cookie → Authorization: Bearer)                 │
│  • Multipart upload parsing antes de reenviar                       │
│  • Validación tamaño de archivo (10 MB — primera línea de defensa)  │
│  • Health check: GET /health → 200                                  │
│                                                                     │
│  ⚠ Sin lógica de negocio. Todo el dominio vive en Django.           │
└────────────────────────────────────┬────────────────────────────────┘
                                     │ HTTP interno
┌────────────────────────────────────▼────────────────────────────────┐
│                    BACKEND — Django 4.2+ + DRF                      │
│                                                                     │
│  Endpoints REST · Permisos por rol · Django Signals                 │
│  Celery task dispatch · LogAuditoria · Multi-tenant filter          │
└────┬───────────────────┬──────────────────────────┬─────────────────┘
     │                   │                          │
┌────▼──────┐   ┌────────▼──────────┐   ┌──────────▼──────────────┐
│PostgreSQL │   │   Redis           │   │   Celery Workers        │
│           │   │                   │   │                         │
│ Datos     │   │ • Allowlist JWT   │   │ • enviar_comunicado     │
│ Índices   │   │ • Celery broker   │   │ • recordatorios_pago    │
│ Constraints│  │ • Rate limit data │   │ • recordatorios_docs    │
└───────────┘   └───────────────────┘   │ • marcar_vencidas       │
                                        │ • archivar_viajes       │
                                        │ • alerta_docs_umbral    │
                                        └────────────┬────────────┘
                                                     │
                                          ┌──────────▼──────────┐
                                          │  Servicios externos │
                                          │  Email SMTP / SES   │
                                          │  S3 / GCS (storage) │
                                          │  WhatsApp (futuro)  │
                                          └─────────────────────┘
```

---

## Stack — Versiones Fijadas

| Capa | Tecnología | Versión | Notas clave |
|------|-----------|---------|-------------|
| Frontend | Next.js | 16.2.6 | App Router obligatorio |
| Frontend | React | 19 | Server Components por defecto |
| Frontend | TailwindCSS | 4 | `@theme {}` en CSS, no `tailwind.config.js` |
| Frontend | Framer Motion | latest | Solo para UI — nunca lógica de negocio |
| Gateway | Node.js (`node:http/https`) | LTS | Sin Express, Fastify ni ningún framework |
| Backend | Django | 4.2+ | DRF para API REST |
| Base de datos | PostgreSQL | — | UUID PKs, índices explícitos, constraints |
| Cache / Broker | Redis | — | Tokens JWT allowlist + Celery broker |
| Tareas async | Celery | — | Beat para cron + workers para tasks |
| Storage | S3 / GCS | configurable | Backend intercambiable vía `FileField` |
| Auth | JWT | — | access 15 min · refresh 7 días en Redis |

---

## Decisiones de Arquitectura

### DA-01 — App Router de Next.js con grupos de layout por portal

Cada portal vive en su propio route group para separar autenticación, layouts y middleware:

```
frontend/app/
├── (public)/            # Landing pública — sin auth
│   └── viajes/[slug]/
├── (padre)/             # Dashboard padre y mecenas
│   ├── layout.tsx       # Verifica rol: padre | mecenas
│   └── app/
├── (agente)/            # Backoffice completo
│   ├── layout.tsx       # Verifica rol: agente
│   └── backoffice/
└── (alumno)/            # Solo lectura
    ├── layout.tsx       # Verifica rol: alumno + acceso habilitado
    └── app/alumno/
```

**Regla:** `middleware.ts` en la raíz verifica JWT y redirige según rol antes de renderizar cualquier layout protegido.

---

### DA-02 — Server Components por defecto, Client Components solo donde necesario

| Usar Server Component | Usar Client Component (`'use client'`) |
|----------------------|----------------------------------------|
| Fetch de datos desde gateway | Formularios con estado |
| Listados, páginas estáticas | Drag & drop del itinerario |
| Layouts y páginas de solo lectura | Uploader de archivos |
| Redirect según estado | Notificaciones en tiempo real |
| — | Animaciones con Framer Motion |

**No usar `useEffect` para fetching.** Usar Server Components o `use()` de React 19.

---

### DA-03 — TailwindCSS 4 con `@theme {}`

```css
/* CORRECTO en TailwindCSS 4 */
@theme {
  --color-primary: #0d4f7c;
  --color-warning: #ef9f27;
  --radius-card: 12px;
}

/* INCORRECTO — no usar tailwind.config.js para design tokens */
```

---

### DA-04 — Framer Motion con LazyMotion

```tsx
// CORRECTO — bundle mínimo
import { LazyMotion, domAnimation, m } from 'framer-motion'

export function PageWrapper({ children }) {
  return (
    <LazyMotion features={domAnimation}>
      <m.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
        {children}
      </m.div>
    </LazyMotion>
  )
}

// INCORRECTO — importa todo Framer Motion
import { motion } from 'framer-motion'
```

---

### DA-05 — API Gateway Node.js sin frameworks

El gateway es un servidor HTTP minimalista. Estructura:

```
gateway/
├── server.js          # createServer(node:http) → punto de entrada
├── router.js          # Map path+method → handler function
├── middleware/
│   ├── cors.js        # Headers CORS manuales por origin
│   ├── rateLimit.js   # Contador en Redis por IP
│   ├── auth.js        # Lee cookie JWT → header Authorization
│   └── security.js    # HSTS, X-Frame-Options, X-Content-Type-Options
├── proxy/
│   ├── django.js      # http.request al backend + pipe de response
│   └── multipart.js   # Parseo multipart/form-data antes de reenviar
└── config.js          # Variables de entorno centralizadas
```

**El gateway no importa lógica de negocio.** Si una condición de negocio necesita evaluarse, va en Django.

---

### DA-06 — JWT en cookies httpOnly (nunca localStorage)

```
LOGIN FLOW:
1. Frontend → POST /auth/login/ → Gateway → Django
2. Django responde con {access_token, refresh_token, rol}
3. Gateway escribe: Set-Cookie: access_token=...; HttpOnly; Secure; SameSite=Strict
4. Frontend recibe cookie automáticamente (no accesible desde JS)
5. Cada request siguiente: Gateway lee cookie, agrega Authorization: Bearer al forward
```

---

### DA-07 — Multi-tenant por campo (preparado para Fase 2)

```python
# TODA consulta del agente debe filtrar por agencia
Viaje.objects.filter(agencia=request.user.agencia)

# NUNCA sin filtro en endpoints del agente
Viaje.objects.all()  # ❌ INCORRECTO
```

- Campo `agencia_id` en todos los modelos raíz: `Viaje`, `Usuario`
- Fase 1: un tenant, Slug: `totem`
- Fase 2+: middleware de tenant que inyecte `agencia_id` automáticamente

---

### DA-08 — Signals Django para efectos secundarios

Los signals garantizan que los efectos secundarios ocurran aunque el código del endpoint no los llame explícitamente:

```python
# apps/pagos/signals.py
@receiver(post_save, sender=Pago)
def on_pago_save(sender, instance, created, **kwargs):
    if created:
        LogAuditoria.objects.create(accion='PAGO_REGISTRADO', ...)
        notify_agente_new_payment(instance)
    elif instance.estado == EstadoPago.VERIFICADO:
        LogAuditoria.objects.create(accion='PAGO_ACTUALIZADO', ...)
        Notificacion.objects.create(usuario=instance.inscripcion.padre_tutor.usuario, ...)
        send_payment_confirmed_email.delay(instance.id)
    elif instance.estado == EstadoPago.RECHAZADO:
        ...
```

---

### DA-09 — Tareas Celery idempotentes

Todas las tareas Celery deben ser reintentables sin efectos duplicados:

```python
@shared_task(bind=True, max_retries=3)
def enviar_recordatorio_pago(self, cuota_id, tutor_id, trigger_dias):
    # Verificar si ya se envió este recordatorio hoy (anti-spam)
    cache_key = f'recordatorio:{cuota_id}:{tutor_id}:{trigger_dias}:{today}'
    if cache.get(cache_key):
        return  # Ya enviado — no duplicar
    # ... enviar
    cache.set(cache_key, True, timeout=86400)
```

---

## Seguridad — Capas y Responsabilidades

| Aspecto | Capa | Implementación |
|---------|------|----------------|
| HTTPS | Infra | TLS terminado en el gateway |
| CORS | Gateway | Headers manuales, `CORS_ORIGINS` por env |
| Rate limiting | Gateway | Por IP + por endpoint, contadores en Redis |
| Headers de seguridad | Gateway | HSTS, X-Frame-Options, X-Content-Type-Options |
| JWT almacenado | Frontend | Cookie `httpOnly; Secure; SameSite=Strict` |
| JWT validado | Backend | DRF — `IsAuthenticated` + verificación de firma |
| Expiración tokens | Backend | access 15 min; refresh 7 días en allowlist Redis |
| Verificación email | Backend | Token one-time; cuenta inactiva hasta verificación |
| Control de acceso | Backend | Permisos DRF por rol; filtro por `agencia_id` |
| Contraseñas | Backend | bcrypt — `AbstractBaseUser.set_password()` |
| Archivos en tránsito | Gateway | HTTPS |
| Archivos en reposo | Storage | AES-256 (S3/GCS) |
| Tamaño de archivo | Gateway + Backend | 10 MB — doble validación |
| Auditoría | Backend | `LogAuditoria` inmutable vía signals |

---

## Variables de Entorno

### Frontend (`frontend/.env.local`)
```env
NEXT_PUBLIC_GATEWAY_URL=https://api.minkagroup.digital
NEXT_PUBLIC_APP_URL=https://minkagroup.digital
```

### Gateway (`gateway/.env`)
```env
PORT=3001
BACKEND_URL=http://backend:8000
CORS_ORIGINS=https://minkagroup.digital,https://www.minkagroup.digital
RATE_LIMIT_WINDOW_MS=60000
RATE_LIMIT_MAX=100
MAX_FILE_SIZE_BYTES=10485760
REDIS_URL=redis://redis:6379
```

### Backend (`backend/.env`)
```env
DATABASE_URL=postgresql://user:pass@db:5432/minka
REDIS_URL=redis://redis:6379
DEFAULT_FILE_STORAGE=storages.backends.s3boto3.S3Boto3Storage
AWS_STORAGE_BUCKET_NAME=minka-files
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
JWT_SECRET_KEY=...
JWT_ACCESS_TOKEN_LIFETIME_MINUTES=15
JWT_REFRESH_TOKEN_LIFETIME_DAYS=7
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.sendgrid.net
CELERY_BROKER_URL=redis://redis:6379/0
DOCS_ARCHIVE_DAYS_AFTER_RETURN=30
DOC_INCOMPLETE_ALERT_THRESHOLD=30
```

---

## Estructura del Repositorio

```
minka-group/
├── frontend/                        # Next.js 16.2.6
│   ├── app/
│   │   ├── (public)/viajes/[slug]/  # Landing pública del viaje
│   │   ├── (padre)/app/             # Portal padre/tutor/mecenas
│   │   ├── (agente)/backoffice/     # Backoffice agente
│   │   └── (alumno)/app/alumno/     # Portal alumno (solo lectura)
│   ├── components/
│   │   ├── ui/                      # Componentes base Tailwind
│   │   ├── motion/                  # Wrappers LazyMotion
│   │   └── forms/                   # Wizards, uploaders
│   ├── lib/
│   │   ├── api.ts                   # Fetch al gateway
│   │   └── auth.ts                  # Helpers JWT/cookie
│   └── middleware.ts                # Auth guard por portal
│
├── gateway/                         # Node.js puro
│   ├── server.js
│   ├── router.js
│   ├── middleware/
│   │   ├── cors.js
│   │   ├── rateLimit.js
│   │   ├── auth.js
│   │   └── security.js
│   └── proxy/
│       ├── django.js
│       └── multipart.js
│
└── backend/                         # Django 4.2+
    ├── config/
    │   └── settings/
    │       ├── base.py
    │       ├── local.py
    │       └── production.py
    ├── apps/
    │   ├── autenticacion/   # Usuario custom, JWT, registro, verificación
    │   ├── agencias/        # Agencia, perfil
    │   ├── viajes/          # Viaje, Grupo, PlanPago, Cuota, Itinerario, Hotel
    │   ├── inscripciones/   # Inscripcion, Alumno, PadreTutor
    │   ├── pagos/           # Pago
    │   ├── documentos/      # DocumentoRequerido, DocumentoEntregado
    │   ├── comunicados/     # Comunicado
    │   ├── notificaciones/  # Notificacion
    │   ├── mecenas/         # Mecenas, MecenasInscripcion
    │   ├── auditoria/       # LogAuditoria
    │   └── exportaciones/   # Generadores Excel/CSV/PDF
    ├── celery.py
    └── tasks/               # Tareas Celery por módulo
```

---

## Performance

| Métrica | Target | Implementación |
|---------|--------|----------------|
| Dashboard del padre | ≤ 3 seg | Server Components + índices PostgreSQL |
| API listados | ≤ 500 ms | Índices + select_related + prefetch_related |
| Emails masivos | No bloquea UI | Celery async |
| Bundle JS | Mínimo | Server Components + LazyMotion |
| `saldo_pendiente` | No en BD | Propiedad Python — computada, no almacenada |
