# MASTER_PLAN.md — Plan Maestro: Tottem Hub (Fase 1)

> Documento de referencia ejecutiva. Para el detalle técnico ver `DEVELOPMENT_PLAN.md`.
> Para el tracking de tareas ver `TASKS.md`.

---

## 1. Resumen Ejecutivo

**Tottem Hub** es un portal SaaS que digitaliza y automatiza el ciclo de vida completo de los viajes escolares grupales de la agencia **Totem Travel** (Perú).

Reemplaza el flujo actual de WhatsApp + Excel + papel por un sistema centralizado que conecta a la agencia con padres/tutores, alumnos y mecenas. El MVP (Fase 1) opera con una sola agencia y pagos 100% manuales con comprobante.

**Cliente:** Totem Travel — agencia de viajes escolares, Perú (`totemstravel.com.pe`)  
**Fase actual:** Fase 1 — MVP mono-agencia  
**Repositorio:** Monorepo `minka-group/` con tres subcarpetas: `frontend/`, `gateway/`, `backend/`

---

## 2. Objetivos

### KPIs de éxito del MVP

| KPI | Meta |
|---|---|
| Reducción en tiempo de validación de pagos y documentos | −70% |
| Reducción de morosidad en cuotas (recordatorios automáticos) | −40% |
| Tasa de completado de inscripción (pagos + docs) | > 85% |
| Tiempo de validación de pago (registro → verificación) | < 24h |
| Morosidad en cuotas | < 15% |
| Abandono en wizard de inscripción | < 20% |
| Documentos completos antes del plazo | > 90% |

### Objetivos técnicos

- Sistema completamente **responsive y mobile-first** (375px mínimo)
- Uptime en producción **≥ 99.5%**
- Dashboard del padre carga en **≤ 3 segundos**
- API responde listados en **≤ 500 ms**
- Arquitectura preparada para **multi-agencia en Fase 2** sin migraciones disruptivas

---

## 3. Arquitectura

### Capas del sistema

```
FRONTEND          GATEWAY            BACKEND           INFRA
─────────         ───────            ───────           ─────
Next.js           Node.js puro       Django 4.2+       PostgreSQL
16.2.6            (node:http)        + DRF             Redis
React 19          Sin Express        + Signals         Celery
TailwindCSS 4     Sin Fastify        + Celery          S3/GCS
Framer Motion     CORS manual        dispatch          Email SMTP
                  Rate limit         LogAuditoria
                  Auth forward       inmutable
                  Multipart parse
                  10 MB validation
```

### Portales frontend

| Portal | Ruta | Audiencia |
|---|---|---|
| Público | `/viajes/{slug}/` | Padres sin cuenta |
| Padre / Mecenas | `/app/` | Padres, tutores, mecenas |
| Alumno | `/app/alumno/` | Alumnos (acceso habilitado por agente) |
| Backoffice | `/backoffice/` | Agentes Totem Travel |

### Principios arquitectónicos clave

- **JWT en cookies `httpOnly`** — nunca en `localStorage`
- **Server Components por defecto** — `'use client'` solo donde necesario
- **`saldo_pendiente` nunca en BD** — propiedad Python computada en tiempo real
- **`LogAuditoria` inmutable** — solo INSERT, nunca UPDATE/DELETE
- **Todas las consultas del agente filtradas por `agencia_id`**
- **Tareas Celery idempotentes** — con cache key anti-duplicado en Redis
- **Doble validación de archivos** — Gateway (primera línea) + Backend (segunda línea)

---

## 4. Actores del Sistema

| Actor | Rol | Portal |
|---|---|---|
| **Agente de Viajes** | Operador del backoffice. Crea viajes, valida pagos y documentos. | `/backoffice/` |
| **Padre / Tutor** | Usuario primario. Inscribe alumnos, paga cuotas, sube documentación. | `/app/` |
| **Alumno** | Solo lectura sobre su perfil e itinerario. | `/app/alumno/` |
| **Mecenas** | Patrocinador. Paga en nombre de uno o más alumnos. | `/app/mecenas/` |
| **Sistema** | Actor automatizado: recordatorios, vencimientos, archivados, logs. | Celery |

---

## 5. Ciclos de Vida de Entidades

```
Viaje:       BORRADOR → ACTIVO → CERRADO → ARCHIVADO
                         (sin retroceso)

Inscripción: PENDIENTE → CONFIRMADO
                       → CANCELADO
                       → BAJA

Pago:        PENDIENTE → VERIFICADO
                       → RECHAZADO

Documento:   PENDIENTE → VALIDADO
                       → RECHAZADO (padre puede resubir)
```

---

## 6. Roadmap

### Fase 1 — MVP (en desarrollo)

| Módulo | Estado |
|---|---|
| Infraestructura (Docker, CI) | Pending |
| Autenticación JWT + verificación email | Pending |
| API Gateway Node.js puro | Pending |
| CRUD de viajes + plan de pagos + itinerario | Pending |
| Wizard de inscripción (padre) | Pending |
| Gestión de pagos manuales + comprobantes | Pending |
| Gestión documental + validación | Pending |
| Dashboard padre (progreso + alertas deep-link) | Pending |
| Backoffice agente (listados, verificación, comunicados) | Pending |
| Recordatorios automáticos (Celery) | Pending |
| Notificaciones in-app + email | Pending |
| Portal mecenas | Pending |
| Chat in-app padre ↔ agente | Pending |
| Exportaciones CSV/XLSX/PDF | Pending |

### Fase 2 — Multi-agencia y Pagos Automáticos (futura)

- Múltiples agencias (campo `agencia_id` ya preparado)
- Pasarela de pago automática (Culqi / Stripe)
- WhatsApp Business API con bot
- Módulo de rooming con selección de compañero

### Fase 3 — Escala y Automatización Avanzada (futura)

- App móvil nativa (iOS / Android)
- Push notifications nativas
- IA para detección de documentos inválidos
- Panel de analítica avanzada

---

## 7. Orden de Implementación

El desarrollo sigue 6 fases ordenadas por dependencias:

```
FASE A — Cimientos
  ├── A1: Monorepo + Docker Compose
  ├── A2: Django project + settings
  ├── A3: Modelos Agencia + Usuario
  ├── A4: Auth JWT completo (backend)
  ├── A5: Gateway Node.js completo
  ├── A6: Next.js setup + TailwindCSS 4
  └── A7: Auth frontend (login, registro, verificación)

FASE B — Dominio Core (backend)
  ├── B1-B6: Modelos y APIs de viajes
  ├── B7-B9: Inscripciones
  ├── B10-B12: Pagos + signals
  ├── B13-B15: Documentos + signals
  └── B16: LogAuditoria

FASE C — Frontend Core (padre, público, alumno)

FASE D — Backoffice Agente

FASE E — Automatización Celery

FASE F — Características Avanzadas
  (Mecenas, Chat, Exportaciones, WhatsApp Nivel 1)
```

Ver `DEVELOPMENT_PLAN.md` para el detalle completo de cada fase.

---

## 8. Dependencias Principales

| Dependencia | Tipo | Afecta |
|---|---|---|
| PostgreSQL + Redis corriendo | Infra | Todo |
| `Agencia` y `Usuario` creados | BD | Todos los demás modelos |
| Auth JWT funcional (backend) | Backend | Todos los endpoints protegidos |
| Gateway funcionando | Gateway | Toda comunicación frontend → backend |
| `Notificacion` model | Backend | Signals de Pago y Documento |
| `LogAuditoria` model | Backend | Signals de Pago, Documento, Inscripcion |
| Celery Beat configurado | Infra | Recordatorios automáticos |
| Dudas D-01 a D-08 resueltas | Docs | Módulos bloqueados por falta de spec |

---

## 9. Estado General del Proyecto

| Área | Estado | Notas |
|---|---|---|
| Documentación | ✅ Completa (11 docs) | Dudas críticas detectadas (ver DEVELOPMENT_PLAN.md §6) |
| Plan de desarrollo | ✅ Generado | Pendiente aprobación |
| Código — Infra | ⏳ Pending | Sin iniciar |
| Código — Backend | ⏳ Pending | Sin iniciar |
| Código — Gateway | ⏳ Pending | Sin iniciar |
| Código — Frontend | ⏳ Pending | Sin iniciar |
| Tests | ⏳ Pending | Sin iniciar |
| Deployment | ⏳ Pending | Sin iniciar |

**Bloqueadores actuales:**
1. Aprobación del plan de desarrollo
2. Respuestas a dudas críticas D-01 (Chat), D-02 (Slug), D-03 (Colegios), D-04/D-05 (campos Alumno)

---

## 10. Restricciones Inamovibles de Fase 1

| Restricción | Motivo |
|---|---|
| Una sola agencia (Totem Travel) | Validar MVP con cliente real |
| Pagos 100% manuales (sin Stripe/Culqi) | Pasarela va en Fase 2 |
| Sin selección de compañero de habitación | El agente asigna manualmente |
| WhatsApp = link wa.me (sin bot) | WhatsApp Business API va en Fase 2 |
| Sin app móvil nativa | Web responsive suficiente para Fase 1 |
| Sin Web Push notifications | Notificaciones in-app son suficientes |
| Gateway sin Express/Fastify/Koa | Solo `node:http` / `node:https` |
| TailwindCSS con `@theme {}` en CSS | Sin `tailwind.config.js` para tokens |
| JWT en cookies `httpOnly` | Nunca en `localStorage` |
