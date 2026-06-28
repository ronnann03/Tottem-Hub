# PROJECT_OVERVIEW.md — Visión General del Proyecto

## ¿Qué problema resuelve?

Las agencias de viajes escolares gestionan hoy sus viajes grupales con WhatsApp, Excel y formularios en papel. El resultado es:

- Validación manual de cientos de comprobantes de pago (horas de trabajo por viaje)
- Documentación incompleta detectada tarde, generando problemas en el momento del viaje
- Alta morosidad por falta de recordatorios automáticos de cuotas
- Comunicación caótica entre agencia y familias sin historial ni contexto
- Sin visibilidad en tiempo real del estado de cada inscripción

## La Solución — Tottem Hub

Portal SaaS que centraliza y automatiza todo el ciclo de vida del viaje escolar grupal:

```
AGENCIA crea viaje → publica landing pública
    ↓
FAMILIAS se inscriben, pagan cuotas, suben documentos
    ↓
SISTEMA notifica, recuerda, valida automáticamente
    ↓
AGENTE supervisa, valida, comunica desde backoffice
    ↓
MECENAS patrocina desde su portal propio
```

---

## Propuesta de Valor por Actor

### Para la Agencia (Totem Travel)
- Panel único con estado en tiempo real de todos los viajes activos
- Validación de pagos y documentos centralizada (−70% tiempo operativo)
- Recordatorios automáticos que reducen morosidad (−40% meta)
- Exportación de listados en Excel/CSV/PDF con un clic
- Comunicados masivos a todas las familias desde el backoffice

### Para el Padre / Tutor
- Sabe exactamente qué falta para confirmar la plaza de su hijo
- Paga cuotas desde cualquier dispositivo y sube el comprobante
- Recibe notificaciones con deep-links directos a la acción pendiente
- Accede al itinerario, hotel asignado y comunicados del viaje
- Chat directo con el agente en contexto del viaje

### Para el Alumno
- Ve su itinerario, estado de documentación y comunicados
- Acceso habilitado por el agente (no obligatorio)

### Para el Mecenas
- Portal propio para ver el estado de los alumnos que patrocina
- Puede registrar pagos en nombre de un alumno directamente

---

## Ecosistema de Viaje — Flujo Completo

### Fase Pre-viaje (gestionada en la plataforma)
1. Agente crea viaje con itinerario, hoteles, plan de pagos y documentos requeridos
2. Agente activa el viaje → se genera landing pública
3. Agente envía link a familias por WhatsApp o email
4. Padre llega a la landing, se registra e inscribe al alumno
5. Sistema genera plan de cuotas personalizado por inscripción
6. Padre paga cuotas fraccionadas (manual + comprobante)
7. Agente verifica o rechaza cada pago
8. Padre sube documentos obligatorios (DNI, autorización, seguro médico)
9. Agente valida o rechaza cada documento con motivo
10. Sistema envía recordatorios automáticos con cadencia configurada
11. Agente asigna alumnos a grupos y hoteles
12. Estado de inscripción evoluciona: pendiente → confirmado

### Fase Durante el Viaje
- Agente envía comunicados masivos (cambios de programa, puntos de encuentro)
- Familias ven el itinerario en tiempo real
- Estado: "En camino" visible en el dashboard del padre

### Fase Post-viaje
- Sistema archiva el viaje automáticamente X días después del regreso
- Mecenas recibe resumen de su contribución

---

## Competidores de Referencia Analizados

| Plataforma | Fortalezas observadas | Debilidades documentadas |
|------------|----------------------|--------------------------|
| Colegia.es | Flujo de inscripción funcional | Dashboard sin estado del viaje, sin deep-links en alertas, formulario largo en un paso |
| Tottem Hub (prototipo) | Badge de estado, alertas contextuales | Sin barra de progreso global, sin mensajería in-app |

**Decisión de diseño:** Tottem Hub adopta lo mejor de ambos y elimina sus puntos de fricción.

---

## Métricas de Éxito del Producto

| Métrica | Descripción | Meta Fase 1 |
|---------|-------------|-------------|
| Tasa de completado de inscripción | % familias que completan pagos + docs | > 85% |
| Tiempo de validación de pago | Horas entre registro y verificación | < 24h |
| Morosidad en cuotas | % cuotas vencidas sin pago | < 15% |
| Tasa de abandono en wizard inscripción | % familias que no terminan el wizard | < 20% |
| Documentos completos antes del plazo | % inscripciones con docs validados a tiempo | > 90% |
| Tiempo de respuesta del agente en chat | Horas para responder mensaje del padre | < 2h |

---

## Roadmap

### Fase 1 — MVP (actual)
- ✅ Una agencia: Totem Travel
- ✅ Portal público de viaje + inscripción
- ✅ Dashboard padre con progreso de inscripción
- ✅ Gestión de pagos manuales + comprobantes
- ✅ Gestión documental + validación
- ✅ Constructor de itinerario
- ✅ Comunicados masivos
- ✅ Notificaciones in-app + email
- ✅ Recordatorios automáticos por Celery
- ✅ Portal mecenas
- ✅ Chat in-app padre ↔ agente
- ✅ Exportaciones Excel/CSV/PDF
- ✅ Panel de métricas del agente

### Fase 2 — Multi-agencia y Pagos Automáticos
- ❌ Más agencias (campo `agencia_id` ya preparado)
- ❌ Pasarela de pago automática (Culqi / Stripe)
- ❌ WhatsApp Business API con bot de primer nivel
- ❌ Módulo de rooming con selección de compañero

### Fase 3 — Escala y Automatización Avanzada
- ❌ App móvil nativa (iOS / Android)
- ❌ Push notifications nativas
- ❌ IA para detección de documentos inválidos
- ❌ Panel de analítica avanzada

---

## Restricciones de Fase 1 (inamovibles)

| Restricción | Motivo |
|------------|--------|
| Una sola agencia | Simplificar MVP, validar producto con cliente real |
| Pagos manuales | Sin integración de pasarela en esta fase |
| Sin selección de compañero de habitación | Agente asigna manualmente por ahora |
| WhatsApp sin bot | Nivel 1: mensaje pre-cargado enriquecido, sin WhatsApp Business API |
| Sin app móvil | Web responsive es suficiente para Fase 1 |
