# REQUIREMENTS.md — Requerimientos del Sistema

## Convenciones

- **Alta** = bloqueante para el lanzamiento de Fase 1
- **Media** = importante pero no bloqueante
- **Baja** = deseable, puede diferirse
- IDs preservados del documento fuente original

---

## RF — Requerimientos Funcionales

### Actor: Padre / Tutor

| ID | Requerimiento | Prioridad |
|----|---------------|-----------|
| RF-PT-01 | Registrarse con email y contraseña; verificar cuenta vía email antes del primer login | Alta |
| RF-PT-02 | Iniciar sesión con credenciales propias | Alta |
| RF-PT-03 | Visualizar dashboard con resumen de viajes activos, estado de pagos y documentación pendiente | Alta |
| RF-PT-04 | Inscribir a uno o más alumnos a un viaje disponible mediante wizard de 3 pasos | Alta |
| RF-PT-05 | Visualizar el plan de pagos: cuotas, fechas de vencimiento e importes | Alta |
| RF-PT-06 | Registrar un pago manual con comprobante adjunto (PDF / JPG, máx. 10 MB) | Alta |
| RF-PT-07 | Consultar el historial de pagos realizados y pendientes | Alta |
| RF-PT-08 | Cargar documentos requeridos por el viaje (DNI, autorización, seguro médico, etc.) | Alta |
| RF-PT-09 | Consultar el estado de validación de cada documento subido (pendiente / validado / rechazado) | Media |
| RF-PT-10 | Visualizar el itinerario detallado del viaje: etapas por día, hoteles y actividades | Alta |
| RF-PT-11 | Acceder al tablón de anuncios y comunicados del viaje | Media |
| RF-PT-12 | Comunicarse con el agente a través de mensajería interna in-app | Media |
| RF-PT-13 | Registrar solicitudes especiales: necesidades alimentarias, médicas, etc. | Media |
| RF-PT-14 | Descargar el resumen de inscripción en PDF | Media |
| RF-PT-15 | Recibir notificaciones por email y en plataforma sobre vencimientos de pago y documentación | Alta |
| RF-PT-16 | Actualizar datos de perfil y contraseña | Media |
| RF-PT-17 | Ver información del hotel asignado con enlace web y ubicación en mapa | Baja |
| RF-PT-18 | Configurar preferencias de notificación (canal preferido, horario de envío, frecuencia) | Media |

### Actor: Alumno

| ID | Requerimiento | Prioridad |
|----|---------------|-----------|
| RF-AL-01 | Acceder a su perfil de viaje con credenciales propias, si el agente habilita el acceso | Media |
| RF-AL-02 | Visualizar su itinerario asignado: etapas, actividades y horarios | Alta |
| RF-AL-03 | Ver el estado de su documentación personal | Media |
| RF-AL-04 | Ver el estado de los pagos vinculados a su inscripción | Media |
| RF-AL-05 | Acceder a los comunicados y anuncios del grupo | Media |
| RF-AL-06 | Descargar su ficha resumen de viaje en PDF | Baja |
| RF-AL-07 | Ver datos de contacto del agente de viajes responsable | Baja |

### Actor: Agente de Viajes

| ID | Requerimiento | Prioridad |
|----|---------------|-----------|
| RF-AV-01 | Crear un nuevo viaje con nombre, destino, fechas, descripción e imagen de portada | Alta |
| RF-AV-02 | Definir el plan de pagos del viaje: número de cuotas, fechas e importes | Alta |
| RF-AV-03 | Asignar hoteles al viaje con tasa turística, fianza, enlace web y mapa | Alta |
| RF-AV-04 | Construir el itinerario del viaje: etapas por día, actividades y transportes con drag & drop | Alta |
| RF-AV-05 | Crear grupos dentro de un viaje (ej. Grupo A, Bus 2) con capacidad opcional | Alta |
| RF-AV-06 | Asignar alumnos a grupos | Alta |
| RF-AV-07 | Ver listado completo de inscritos con estado de pago y documentación | Alta |
| RF-AV-08 | Validar o rechazar documentos subidos por las familias, con motivo en caso de rechazo | Alta |
| RF-AV-09 | Registrar pagos manuales a nombre de una familia o mecenas | Alta |
| RF-AV-10 | Enviar comunicados masivos a todas las familias de un viaje | Alta |
| RF-AV-11 | Configurar los tipos de documentos requeridos para cada viaje | Media |
| RF-AV-12 | Exportar listados en Excel / CSV: inscritos, pagos, documentación | Alta |
| RF-AV-13 | Generar y descargar informes de estado del viaje en PDF | Media |
| RF-AV-14 | Gestionar el perfil de la agencia: nombre, logo, contacto | Media |
| RF-AV-15 | Ver panel de métricas del viaje: % inscritos, % pagado, % documentado | Alta |
| RF-AV-16 | Activar o desactivar un viaje (visible o no para las familias) | Alta |
| RF-AV-17 | Asignar mecenas a alumnos específicos con monto comprometido | Media |
| RF-AV-18 | Gestionar múltiples viajes simultáneamente desde un panel unificado | Alta |
| RF-AV-19 | Configurar recordatorios automáticos de pago: días previos y canales | Media |
| RF-AV-20 | Añadir notas internas a cada inscripción (invisibles para el padre/alumno) | Baja |
| RF-AV-21 | Responder mensajes del padre desde el backoffice de mensajería | Media |
| RF-AV-22 | Ver alertas cuando el % de documentación incompleta supere un umbral configurable | Media |

### Actor: Mecenas

| ID | Requerimiento | Prioridad |
|----|---------------|-----------|
| RF-ME-01 | Acceder al portal con credenciales propias | Alta |
| RF-ME-02 | Ver el listado de alumnos que patrocina con estado de inscripción | Alta |
| RF-ME-03 | Ver el estado de pago de cada alumno patrocinado | Alta |
| RF-ME-04 | Registrar pagos en nombre de un alumno con comprobante adjunto | Alta |
| RF-ME-05 | Descargar un resumen de su contribución total en PDF | Media |
| RF-ME-06 | Recibir notificaciones cuando un vencimiento de pago se aproxima | Media |
| RF-ME-07 | Ver el itinerario del viaje del alumno patrocinado (solo lectura) | Baja |

### Actor: Sistema (Automatizado — Celery)

| ID | Requerimiento | Prioridad |
|----|---------------|-----------|
| RF-SIS-01 | Enviar recordatorios de pago en cadencia: 30d / 15d / 7d / 3d / día-D / rechazo inmediato | Alta |
| RF-SIS-02 | Marcar cuotas como vencidas automáticamente si `fecha_vencimiento < hoy` sin pago verificado | Alta |
| RF-SIS-03 | Generar notificaciones cuando un documento sea validado o rechazado por el agente | Alta |
| RF-SIS-04 | Calcular el saldo pendiente de cada inscripción en función de los pagos verificados | Alta |
| RF-SIS-05 | Enviar email de confirmación al registrar un pago | Media |
| RF-SIS-06 | Alertar al agente cuando el % de documentación incompleta supere un umbral | Media |
| RF-SIS-07 | Archivar automáticamente los viajes finalizados X días después de `fecha_regreso` | Baja |
| RF-SIS-08 | Mantener log de auditoría inmutable de todas las acciones críticas | Alta |

---

## RNF — Requerimientos No Funcionales

### Rendimiento

| ID | Requerimiento |
|----|---------------|
| RNF-01 | Tiempo de carga del dashboard del padre ≤ 3 segundos |
| RNF-02 | La API debe responder peticiones de listado en ≤ 500 ms bajo carga normal |
| RNF-03 | El envío de comunicados masivos debe procesarse en background (no bloquear al agente) |

### Seguridad

| ID | Requerimiento |
|----|---------------|
| RNF-04 | Todos los archivos subidos deben estar cifrados en reposo (AES-256) |
| RNF-05 | Los tokens JWT deben almacenarse en cookies `httpOnly` en el frontend |
| RNF-06 | Máximo 10 MB por archivo subido — validado en gateway y en backend |
| RNF-07 | Las contraseñas deben hashearse con bcrypt — nunca almacenar en texto plano |
| RNF-08 | Toda cuenta debe verificar su email antes del primer login |
| RNF-09 | El log de auditoría es inmutable — nunca UPDATE ni DELETE sobre `LogAuditoria` |
| RNF-10 | Todas las rutas protegidas requieren JWT válido — ningún endpoint de datos es público |

### Usabilidad

| ID | Requerimiento |
|----|---------------|
| RNF-11 | Interfaz completamente responsive y mobile-first |
| RNF-12 | El wizard de inscripción debe completarse en ≤ 4 minutos (vs. 8 min. formulario único) |
| RNF-13 | Toda alerta del dashboard debe incluir deep-link directo a la acción, no texto genérico |
| RNF-14 | Los estados de documentos y pagos deben comunicarse con color + ícono + texto |

### Disponibilidad y Escalabilidad

| ID | Requerimiento |
|----|---------------|
| RNF-15 | Uptime ≥ 99.5% en producción |
| RNF-16 | El esquema de BD debe soportar multi-agencia (campo `agencia_id`) sin migración disruptiva futura |
| RNF-17 | Las tareas de Celery deben ser idempotentes (reintentables sin efectos duplicados) |

### Formatos y Datos

| ID | Requerimiento |
|----|---------------|
| RNF-18 | Formatos de documento aceptados por defecto: `pdf`, `jpg`, `png` (configurable por viaje) |
| RNF-19 | Exportaciones deben estar disponibles en CSV, XLSX y PDF |
| RNF-20 | Fechas en ISO 8601 (`YYYY-MM-DD`) en toda la API |
| RNF-21 | IDs en formato UUID v4 en todas las entidades |

---

## Cadencia de Recordatorios Automáticos

### Recordatorios de Pago

| Trigger | Canal | Tono |
|---------|-------|------|
| 30 días antes del vencimiento | Email | Informativo |
| 15 días antes del vencimiento | Email + WhatsApp | Recordatorio |
| 7 días antes del vencimiento | Email + WhatsApp + Push | Urgente |
| 3 días antes del vencimiento | WhatsApp directo del agente | Personalizado |
| Día del vencimiento | Email + WhatsApp + Push | Crítico |
| Cuota rechazada (inmediato) | Email + Push (< 1h) | Urgente |

### Recordatorios de Documentación

| Trigger | Canal |
|---------|-------|
| 30 días antes del plazo | Email |
| 15 días antes del plazo | Email + WhatsApp |
| 7 días antes del plazo | Email + WhatsApp + Push |
| 3 días antes del plazo | WhatsApp del agente |
| Día del plazo | Email + WhatsApp + Push |
| Documento rechazado (< 1h) | Email + Push |

### Reglas Anti-spam

- Si el padre completó todos los documentos/pagos: detener la secuencia
- Horario de envío: 9:00–20:00h local
- Máximo 1 mensaje por canal por día
- Opción "snooze" disponible: recordarme en 2 días
- Canal preferido configurable por cada padre

---

## Matriz de Canales por Evento

| Evento | Email | WhatsApp | Push | SMS | In-app |
|--------|-------|----------|------|-----|--------|
| Inscripción creada | ✅ | ✅ | ✅ | ❌ | ✅ |
| Plaza confirmada | ✅ | ✅ | ✅ | ✅ | ✅ |
| Pago confirmado | ✅ | ✅ | ✅ | ❌ | ✅ |
| Pago próximo a vencer | ✅ | ✅ | ✅ | ❌ | ✅ |
| Pago vencido | ✅ | ✅ | ✅ | ✅ | ✅ |
| Documento aprobado | ✅ | ❌ | ✅ | ❌ | ✅ |
| Documento rechazado | ✅ | ✅ | ✅ | ❌ | ✅ |
| Documento por vencer | ✅ | ✅ | ✅ | ❌ | ✅ |
| Comunicado del agente | ✅ | ✅ | ✅ | ❌ | ✅ |
| Cambio de itinerario | ✅ | ✅ | ✅ | ✅ | ✅ |
| Mecenas contribuye | ✅ | ✅ | ✅ | ❌ | ✅ |
| D-7 cuenta atrás | ✅ | ✅ | ✅ | ❌ | ✅ |

> SMS reservado para eventos críticos únicamente: plaza confirmada, pago vencido, cambio de itinerario.
