# TECH_DEBT.md — Registro de Deuda Técnica

> Última actualización: 2026-06-28 (TASK-013)

> Solo registra deuda. No resuelve. Cada entrada requiere aprobación antes de ser trabajada.
>
> **Estados:** `Activa` | `En revisión` | `Resuelta`
> **Prioridades:** `Alta` | `Media` | `Baja`

---

## TD-001 — Sin archivos de test automatizados para TASK-008 a TASK-011

**ID:** TD-001  
**Estado:** Activa  
**Prioridad:** Alta  
**Detectado en:** TASK-012 (2026-06-28)

**Descripción:**  
Las tareas TASK-008 (registro), TASK-009 (verificación), TASK-010 (login) y TASK-011
(refresh/logout) documentan tests en sus notas ("7 tests — todos pasan", "9 tests — todos pasan",
etc.), pero no existen archivos `.py` de tests en el repositorio para el módulo
`apps.autenticacion`. La validación fue manual o en sesión interactiva y no quedó persistida.

**Impacto:**  
- Cualquier refactorización del módulo de autenticación puede romper funcionalidad sin detección.
- El total de tests automatizados del módulo es 0 (TASK-008→011) + 13 (TASK-012).
- Cobertura de CI nula en el flujo crítico de login/registro/JWT.

**Prioridad:** Alta — la autenticación es el flujo más crítico del sistema.

**Tarea sugerida:**  
Crear `backend/apps/autenticacion/tests/` con:
- `test_registro.py` (7 casos)
- `test_verificacion.py` (7 casos)
- `test_login.py` (9 casos)
- `test_refresh_logout.py` (11 casos)

---

## TD-002 — JWTAuthentication no lee cookies (requiere Gateway para funcionar en producción)

**ID:** TD-002  
**Estado:** Activa  
**Prioridad:** Media  
**Detectado en:** TASK-012 (2026-06-28)

**Descripción:**  
El `DEFAULT_AUTHENTICATION_CLASSES` usa `JWTAuthentication` de simplejwt, que lee el token
del header `Authorization: Bearer <token>`. Sin embargo, los tokens se almacenan en cookies
`httpOnly` (DEC-002). En producción el Gateway convierte la cookie en header (TASK-015),
por lo que funciona end-to-end. Pero los tests de endpoints autenticados deben usar
`force_authenticate()` porque no pueden emular el Gateway.

**Impacto:**  
- Los tests no ejercen el camino real de autenticación (cookie → Gateway → header → Django).
- Si el Gateway falla en convertir la cookie, Django devuelve 401 y es difícil diagnosticar.
- En desarrollo sin Gateway, los endpoints autenticados son inaccesibles via navegador/curl.

**Prioridad:** Media — aceptable en Fase 1 con Gateway planificado en TASK-015.

**Tarea sugerida:**  
Implementar `CookieJWTAuthentication(JWTAuthentication)` que lea `access_token` de cookies
como fallback cuando no hay header `Authorization`. Activar como clase adicional en
`DEFAULT_AUTHENTICATION_CLASSES`. Permite desarrollo y tests sin Gateway.

---

## TD-003 — Archivos de logo huérfanos al actualizar con PATCH

**ID:** TD-003  
**Estado:** Activa  
**Prioridad:** Baja  
**Detectado en:** TASK-012 (2026-06-28)

**Descripción:**  
Cuando se hace PATCH de `logo` con un nuevo archivo, el archivo anterior queda en storage
(local o S3) sin referencia en la BD. Django no elimina automáticamente archivos de
`ImageField` al actualizarse o borrarse. Con el tiempo esto genera archivos huérfanos
que consumen storage.

**Impacto:**  
- Bajo en Fase 1 (solo un tenant, logo cambia raramente).
- Aumenta en Fase 2+ con múltiples agencias.

**Prioridad:** Baja — no afecta funcionalidad.

**Tarea sugerida:**  
Añadir signal `pre_save` en `Agencia` que elimine el logo anterior del storage cuando
`logo` cambia. Alternativa: task Celery periódica que audite archivos huérfanos en S3.

---

## TD-004 — Errores E501 en migración autogenerada `agencias/migrations/0001_initial.py`

**ID:** TD-004  
**Estado:** Activa  
**Prioridad:** Baja  
**Detectado en:** TASK-012 (2026-06-28)

**Descripción:**  
Flake8 reporta 7 errores E501 (líneas > 100 caracteres) en
`backend/apps/agencias/migrations/0001_initial.py`. El archivo fue generado automáticamente
por Django (`makemigrations`) y nunca formateado.

**Impacto:**  
- Flake8 sobre toda la carpeta `apps/agencias/` falla con exit code 1.
- Los 5 archivos de TASK-012 tienen 0 errores. El ruido es del archivo preexistente.

**Prioridad:** Baja — no afecta funcionalidad ni seguridad.

**Tarea sugerida:**  
Añadir `per-file-ignores = migrations/*:E501` al `.flake8` del proyecto. Esta es la
práctica estándar en proyectos Django para ignorar errores de lint en migraciones
autogeneradas.

---

## TD-005 — Sin linter configurado en el Gateway (JavaScript)

**ID:** TD-005  
**Estado:** Activa  
**Prioridad:** Media  
**Detectado en:** TASK-013 (2026-06-28)

**Descripción:**  
El módulo `gateway/` no tiene ESLint ni Biome configurados. El código JavaScript del
Gateway no pasa por ninguna verificación de estilo o calidad automática. En Python se usa
flake8; en JavaScript no hay equivalente configurado.

**Impacto:**  
- Errores de estilo (variables no usadas, comparaciones débiles `==`, `console.log` olvidados)
  pueden llegar al repositorio sin detección.
- En TASK-014+ el Gateway crece en complejidad; la ausencia de linter aumenta el riesgo de
  errores sutiles.

**Prioridad:** Media — el Gateway es código crítico de seguridad (CORS, auth, rate limiting).

**Tarea sugerida:**  
Añadir ESLint con configuración mínima (`eslint:recommended`) y script `"lint": "eslint ."` en
`gateway/package.json`. Alternativa: Biome (más rápido, sin dependencias de plugins). Configurar
en CI junto con `npm test`.

