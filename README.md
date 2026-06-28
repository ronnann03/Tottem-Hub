# Tottem Hub

Portal SaaS para digitalizar el ciclo de vida de viajes escolares grupales de **Totem Travel** (Perú).

## Estructura del monorepo

```
minka-group/
├── frontend/    # Next.js 16.2.6 — portales público, padre, alumno, agente
├── gateway/     # Node.js puro — proxy, auth, rate-limit, validación de archivos
├── backend/     # Django 4.2+ — lógica de negocio, API REST, Celery
└── docs/        # Toda la documentación del proyecto
```

## Documentación

Toda la documentación del proyecto está en `docs/`:

- [`docs/README.md`](docs/README.md) — Resumen del proyecto y stack
- [`docs/MASTER_PLAN.md`](docs/MASTER_PLAN.md) — Plan maestro y roadmap
- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — Arquitectura y decisiones técnicas
- [`docs/DATABASE.md`](docs/DATABASE.md) — Esquema de base de datos
- [`docs/TASKS.md`](docs/TASKS.md) — Tareas de desarrollo con estado
- [`docs/CLAUDE_RULES.md`](docs/CLAUDE_RULES.md) — Reglas del agente de desarrollo

## Inicio rápido

```bash
# (Disponible tras TASK-002 — Docker Compose)
docker compose up
```
