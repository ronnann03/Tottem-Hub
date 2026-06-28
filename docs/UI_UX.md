# UI_UX.md — Contratos de Interfaz y Diseño UX

> Este documento describe las pantallas, estados visuales, componentes y reglas de interacción del sistema. Es el contrato entre diseño y desarrollo. No inventar funciones ni estados adicionales a los documentados aquí.

---

## Principios de Diseño

1. **Mobile-first.** Todas las pantallas deben funcionar en 375px de ancho mínimo.
2. **Deep-links en cada alerta.** Ninguna notificación o alerta es solo texto — siempre lleva a la pantalla de acción.
3. **Estado siempre visible.** El padre nunca debe adivinar si su inscripción está completa.
4. **Progreso explícito.** Barras, contadores y badges en lugar de listas vacías.
5. **Errores con contexto.** Al rechazar un documento o pago, el motivo es visible y accionable.

---

## Portales y URLs Base

| Portal | Layout | Audiencia | URL base |
|--------|--------|-----------|----------|
| Landing pública | `(public)` | Padres no registrados | `/viajes/{slug}/` |
| Portal padre | `(padre)` | Padres / tutores | `/app/` |
| Portal mecenas | `(padre)` | Mecenas (mismo layout) | `/app/mecenas/` |
| Portal alumno | `(alumno)` | Alumnos (si habilitado) | `/app/alumno/` |
| Backoffice agente | `(agente)` | Agentes Totem Travel | `/backoffice/` |

---

## Pantalla 1 — Landing Pública del Viaje

**URL:** `/viajes/{slug}/`  
**Audiencia:** Padres no registrados  
**Objetivo:** Informar y convertir en inscripción

### Secciones Obligatorias (en orden)

```
┌─────────────────────────────────────────────────┐
│  HERO full-width con imagen del destino         │
│  "PRÓXIMA EXPEDICIÓN 2026"                       │
│  [NOMBRE DEL VIAJE EN MAYÚSCULAS]               │
│  Para alumnos de [nivel] del [nombre colegio]   │
│                                                 │
│  [INSCRIBIR A MI HIJ@]    [VER PROGRAMA]        │
├─────────────────────────────────────────────────┤
│  📅 Fechas   📍 Destino   👥 Plazas   🛡 Seguro  │
├─────────────────────────────────────────────────┤
│  ⭐ Gestión Online  ♥ Seguridad  💳 Fraccionado  │
├─────────────────────────────────────────────────┤
│  ITINERARIO RESUMIDO (6 días máx. en landing)   │
├─────────────────────────────────────────────────┤
│  ¿Por qué viajar con TOTEM? (3 cards propuesta) │
├─────────────────────────────────────────────────┤
│  CTA FINAL: "¿Preparados para el despegue?"     │
│  [INSCRIBIR A MI HIJ@]                          │
├─────────────────────────────────────────────────┤
│  FOOTER: contacto, licencia MINCETUR, T&C       │
└─────────────────────────────────────────────────┘
```

### Datos que deben venir de la API
- `viaje.nombre`, `viaje.destino`, `viaje.fecha_salida`, `viaje.fecha_regreso`
- `viaje.cupo_maximo`, inscripciones activas (para badge de plazas)
- `viaje.precio_total` (mostrar "Desde S/ X")
- `viaje.imagen_url` (hero)
- `viaje.itinerario.etapas[]` (resumen de días)

---

## Pantalla 2 — Wizard de Inscripción

**URL:** `/app/inscribir/{viaje_id}/`  
**Audiencia:** Padre autenticado  
**Estructura:** 3 pasos con barra de progreso

### Barra de progreso
```
[●──────────────○──────────────○]
 Paso 1 de 3: Datos básicos
```

### Paso 1 — Datos Básicos del Alumno
- Nombre * (texto)
- Apellidos * (texto)
- DNI / Pasaporte * (texto — tooltip: "Si tiene menos de 14 años escribe NO")
- Fecha de nacimiento * (DD / MM / AAAA)
- Género * (radio: Chico / Chica)

### Paso 2 — Centro Educativo
- Departamento * (select — regiones del Perú)
- Nombre del colegio * (typeahead dinámico por departamento)
- Nivel educativo * (select: Inicial / Primaria / Secundaria)
- Grado / Año * (select: 1° al 6°)

### Validación inteligente tras Paso 2
```
✅ CASO CORRECTO:
   Juan Abarca · 5° Secundaria · Colegio San Agustín
   "¡Perfecto! Este viaje es para alumnos de 5° Sec. de San Agustín."
   [Continuar →]

⚠ CASO NIVEL INCORRECTO:
   "Este viaje es para 5° Secundaria. Juan está en 3° Primaria."
   [Continuar de todas formas]  [Buscar viaje para este alumno]

❌ CASO COLEGIO DIFERENTE:
   "Este viaje es exclusivo para alumnos del Colegio San Agustín."
   [Buscar viajes para mi colegio]
```

### Paso 3 — Salud y Aceptación
- Alergias (14 checkboxes EU: Gluten, Crustáceos, Huevos, Pescado, Cacahuetes, Soja, Lácteos, Frutos cáscara, Apio, Mostaza, Sésamo, Sulfitos, Moluscos, Altramuces)
- Teléfono del alumno durante el viaje [OPCIONAL] — tooltip: "Solo para emergencias durante el viaje"
- ☑ Acepto política de privacidad y T&C *

---

## Pantalla 3 — Búsqueda de Viaje

**URL:** `/app/buscar-viaje/`

### Método 1 — Código de viaje
```
🔑 Tengo un código de viaje: [__________] [Buscar]
```

### Método 2 — Por centro educativo
```
📍 Departamento *        🏫 Nombre del colegio *
[Lima ▾]                [Colegio San Agustín...]

🌍 Destino del viaje *
[Machu Picchu & Cusco ▾]
                                  [Buscar viaje →]
```

### Fallback si no hay resultados
```
"No encontramos viajes para este colegio."
"¿Tu agencia ya tiene el viaje publicado?"
[📞 Contactar soporte]  [📋 Unirme con código]
```

---

## Pantalla 4 — Dashboard del Padre

**URL:** `/app/`  
**Objetivo:** Estado completo de inscripción de un vistazo

### Estructura de la pantalla
```
┌─────────────────────────────────────────────────────┐
│  Bienvenido, Carlos                    [⓪ Ayuda]   │
├─────────────────────────────────────────────────────┤
│  VIAJE ACTIVO                                       │
│  ┌───────────────────────────────────────────────┐  │
│  │  [Imagen miniatura destino]                   │  │
│  │  Machu Picchu & Cusco · Fin de año 2026       │  │
│  │  📅 15–22 nov  │ 🎓 Colegio San Agustín       │  │
│  │  👤 Juan Abarca │ 🟠 Lista de espera           │  │
│  ├───────────────────────────────────────────────┤  │
│  │  PROGRESO DE INSCRIPCIÓN      ███████░░░  65% │  │
│  │  ┌─────────────┬──────────────┬─────────────┐ │  │
│  │  │ 💳 Pagos    │ 📁 Documentos│ 🏨 Alojam.  │ │  │
│  │  │ 1/3 pagados │ 1/4 aprobados│ ✅ Asignado │ │  │
│  │  │ 🔴 Vencido  │ 🟡 Pendiente │             │ │  │
│  │  └─────────────┴──────────────┴─────────────┘ │  │
│  │                                               │  │
│  │  [💳 Ir a Pagos]  [📁 Subir Docs]  [Ver todo] │  │
│  └───────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────┤
│  ALERTAS Y PENDIENTES                               │
│  🔴 Cuota vencida — 2ª cuota S/280  [Pagar ahora →] │
│  🟡 3 documentos pendientes          [Subir ahora →] │
│  🟡 3ª cuota vence en 12 días    [Ver plan pagos →] │
├─────────────────────────────────────────────────────┤
│  HIJOS REGISTRADOS               [+ Nuevo hijo]    │
│  👤 Juan Abarca · San Agustín · 5° Sec             │
│  🟡 Alergias: sin especificar   [✏ Editar]          │
└─────────────────────────────────────────────────────┘
```

### Reglas del componente Dashboard

- La imagen miniatura del destino es obligatoria — no mostrar placeholder en producción
- Las alertas tienen deep-link directo — **nunca** texto genérico sin link
- Los 3 sub-cards (Pagos / Docs / Alojamiento) son siempre visibles aunque estén completos
- El badge de estado de inscripción usa el sistema de 4 estados de UX (ver tabla abajo)

---

## Sistema de Estados de Inscripción (UX)

| Estado UX | Color | Badge | Mensaje | CTA |
|-----------|-------|-------|---------|-----|
| Lista de espera | 🟠 Naranja | `#ef9f27` | "Juan está en lista de espera. Completa pagos y docs para asegurar su plaza." | [Completar inscripción →] |
| Pre-inscrito | 🟡 Amarillo | `#efcf27` | "Falta completar X pagos y Y documentos para confirmar la plaza." | [Ver qué falta →] |
| Confirmado | 🟢 Verde | `#27a050` | "¡La plaza de Juan está confirmada! El viaje sale el DD mmm." | [Ver detalles del viaje →] |
| En camino | 🔵 Azul | `#2780ef` | "Juan está de viaje. Día N de M — [actividad del día]" | [Ver itinerario en vivo →] |

---

## Pantalla 5 — Gestión de Pagos

**URL:** `/app/pagos/{inscripcion_id}/`

### Vista del plan de pagos
```
┌──────────────────────────────────────────────────┐
│  💳 Plan de pagos — Machu Picchu & Cusco         │
│  Juan Abarca · Saldo pendiente: S/ 560           │
├──────────────────────────────────────────────────┤
│  PROGRESO         ████████░░░░  33% pagado       │
├──────────────────────────────────────────────────┤
│  ✅ 1ª cuota — S/ 280  — Pagado el 15 abr        │
│  🔴 2ª cuota — S/ 280  — Vencida el 15 may       │
│     [Pagar ahora →]                              │
│  ⏳ 3ª cuota — S/ 280  — Vence el 15 jun         │
└──────────────────────────────────────────────────┘
```

### Sistema de estados de cuota

| Estado | Color | Ícono | Descripción |
|--------|-------|-------|-------------|
| Pagado y verificado | 🟢 Verde | ✅ | El agente aprobó el pago |
| En revisión | ⬆ Gris | ⏳ | El padre subió comprobante, pendiente de revisión |
| Pendiente | 🟡 Amarillo | ⏳ | Aún no hay pago registrado |
| Vencida | 🔴 Rojo | 🚨 | Pasó la fecha sin pago verificado |

### Formulario de registro de pago

Campos:
- Cuota a la que aplica (select de cuotas pendientes/vencidas)
- Importe (decimal)
- Fecha del pago (date)
- Método: Transferencia / Efectivo / Tarjeta / Otro
- Comprobante (file uploader — PDF o JPG, máx. 10 MB)

---

## Pantalla 6 — Gestión de Documentos

**URL:** `/app/documentos/{inscripcion_id}/`

### Vista del checklist
```
┌──────────────────────────────────────────────────┐
│  📁 Documentación — Juan Abarca                  │
│  Machu Picchu & Cusco                            │
├──────────────────────────────────────────────────┤
│  PROGRESO         ████░░░░░░░░  1/4 aprobados   │
│  [✅ 1 aprobado] [⬆ 0 en revisión] [⏳ 3 pend.] │
├──────────────────────────────────────────────────┤
│  OBLIGATORIO  DNI del alumno         ✅ Aprobado  │
│  Subido: dni_juan.pdf  · validado el 20 abr      │
├──────────────────────────────────────────────────┤
│  OBLIGATORIO  Autorización tutor      ⏳ Pendiente│
│  Fecha límite: 15 may 2026       [Subir archivo] │
├──────────────────────────────────────────────────┤
│  OBLIGATORIO  Seguro médico    🔴 Rechazado       │
│  Motivo: "La póliza venció el 01/03/2025."       │
│  Fecha límite: 01 jun          [Volver a subir]  │
├──────────────────────────────────────────────────┤
│  OPCIONAL     Ficha médica          ⏳ Pendiente  │
│  Fecha límite: 01 jun             [Subir archivo] │
└──────────────────────────────────────────────────┘
```

### Sistema de estados de documento (4 exactos — no inventar más)

| Estado BD | Color | Ícono | CTA del padre | Acción del agente |
|-----------|-------|-------|---------------|-------------------|
| `pendiente` (sin subir) | 🟡 Amarillo | ⏳ | "Subir archivo" | — |
| `pendiente` (subido, en revisión) | ⬆ Gris | ⬆ | — (esperando) | Validar / Rechazar |
| `validado` | 🟢 Verde | ✅ | — | — |
| `rechazado` | 🔴 Rojo | ⊗ | "Volver a subir" | — |

> **Nota:** "en revisión" no es un estado BD separado. Es `pendiente` con `archivo != null`. El frontend infiere esto.

### Uploader de archivos — comportamiento
- Aceptar: `.pdf`, `.jpg`, `.png` (según `formatos_permitidos` del `DocumentoRequerido`)
- Límite: 10 MB — mostrar error antes de hacer upload
- Preview del archivo seleccionado antes de confirmar
- Progress bar durante el upload
- Si el documento anterior fue rechazado → mostrar historial de versiones

---

## Pantalla 7 — Centro de Notificaciones

**URL:** `/app/notificaciones/`

### Vista del panel
```
┌──────────────────────────────────────────────────┐
│  🔔 Notificaciones            Marcar todo leído   │
├──────────────────────────────────────────────────┤
│  🔵 HOY · 09:15                                   │
│  📁 Tu seguro médico fue rechazado                │
│     "La póliza está caducada. Sube la vigente."  │
│     Machu Picchu · Juan Abarca                   │
│                          [Subir documento →]     │
├──────────────────────────────────────────────────┤
│  🔵 AYER · 18:42                                  │
│  💳 Recuerda: el 2° plazo vence en 5 días        │
│     S/ 280 · Vence: 23 may 2026                  │
│                          [Pagar ahora →]         │
├──────────────────────────────────────────────────┤
│  ✓  15 may · 14:30                               │
│  ✅ DNI de Juan Abarca aprobado                   │
│     Tu documento fue validado.                   │
└──────────────────────────────────────────────────┘
```

### Tipos de notificación y sus íconos

| Tipo | Ícono | Deep-link |
|------|-------|-----------|
| `pago_vencido` | 💳🔴 | `/app/pagos/{inscripcion_id}/` |
| `recordatorio` | 💳🟡 | `/app/pagos/{inscripcion_id}/` |
| `doc_rechazado` | 📁🔴 | `/app/documentos/{inscripcion_id}/` |
| `doc_validado` | 📁🟢 | `/app/documentos/{inscripcion_id}/` |
| `comunicado` | 💬 | `/app/viaje/{viaje_id}/comunicados/` |

---

## Pantalla 8 — Chat In-App

**URL:** `/app/mensajes/{viaje_id}/`

### Estructura
```
┌──────────────────────────────────────────────────┐
│  💬 MENSAJES                                     │
│  Machu Picchu · Juan Abarca                      │
│  Agencia Totem Travel · Tiempo respuesta: ~2h    │
├──────────────────────────────────────────────────┤
│  15 may 2026 ────────────────────────────────── │
│                                                  │
│  👤 Carlos · 10:23                               │
│  ┌─────────────────────────────────────────┐     │
│  │ ¿Por qué fue rechazado el seguro?       │ 💬  │
│  └─────────────────────────────────────────┘     │
│                                                  │
│              Totem Travel · 11:05 👤 ──────────  │
│      ┌──────────────────────────────────────┐    │
│  💬  │ Hola Carlos, la póliza venció el     │    │
│      │ 01/03/2025. Necesitamos una vigente  │    │
│      │ que cubra el 15-22 nov 2026.         │    │
│      └──────────────────────────────────────┘    │
│                                       ✓✓ Leído  │
├──────────────────────────────────────────────────┤
│  Quick replies:                                  │
│  [¿Por qué rechazaron mi doc?] [¿Cómo transfiero?] │
├──────────────────────────────────────────────────┤
│  📎 Adjuntar  [________________________] [Enviar] │
└──────────────────────────────────────────────────┘
```

### Características del chat
- Historial persistente por viaje (no por conversación genérica)
- Contexto fijo en el header: viaje + alumno
- Adjuntar archivos: documentos y fotos
- Estados: enviado ✓ / leído ✓✓
- Quick replies predefinidos:
  - "¿Por qué fue rechazado mi documento?"
  - "¿Cómo pago por transferencia?"
  - "¿Cuál es el punto de encuentro?"
  - "Necesito cambiar de compañero de habitación"

---

## Pantalla 9 — Backoffice: Listado de Inscritos (Agente)

**URL:** `/backoffice/viajes/{viaje_id}/inscritos/`

### Panel de métricas del viaje (header)
```
┌──────────────────────────────────────────────────┐
│  Machu Picchu & Cusco — 15-22 nov 2026           │
│  ┌───────────┬───────────┬────────────────────┐  │
│  │ 45 / 50   │  S/12.500 │  30 completos      │  │
│  │ Inscritos │  Recaudado│  de Documentación  │  │
│  │ 90%       │  32.7%    │  66.7%             │  │
│  └───────────┴───────────┴────────────────────┘  │
└──────────────────────────────────────────────────┘
```

### Tabla de inscritos
Columnas: Alumno · Tutor · Estado inscripción · % Pagado · Estado Docs · Grupo · Acciones

Filtros: Estado inscripción / % pagado (< 50%, 50-99%, 100%) / Estado docs (completo, incompleto) / Grupo

Acciones por fila: Ver ficha · Añadir nota · Ver chat

---

## Pantalla 10 — Backoffice: Validación de Documentos (Agente)

**URL:** `/backoffice/viajes/{viaje_id}/documentos/`

```
┌──────────────────────────────────────────────────┐
│  Juan Abarca · Seguro médico · Subido: 20 may    │
│  [👁 Ver documento]  (abre en nueva pestaña)     │
│                                                  │
│  Decisión:  ○ Aprobar   ○ Rechazar               │
│  Motivo (si rechaza): [________________]         │
│                        [Enviar decisión →]        │
└──────────────────────────────────────────────────┘
```

---

## Pantalla 11 — Constructor de Itinerario (Agente)

**URL:** `/backoffice/viajes/{viaje_id}/itinerario/`

### Estructura visual
- Lista de días en columna izquierda (Día 1, Día 2, etc.)
- Actividades del día seleccionado en área central con cards
- Drag & drop para reordenar actividades dentro del día
- Botones: [+ Añadir día] [+ Añadir actividad al día seleccionado]
- Tipos de actividad con ícono por tipo: 🚌 Transporte / 🍽 Comida / 🏛 Visita / 🛏 Alojamiento / 🕰 Tiempo libre

---

## Componentes Transversales

### Badge de estado
- Siempre incluye: color de fondo + ícono + texto
- Nunca solo texto sin color

### Barra de progreso
- Con porcentaje numérico visible
- Color verde cuando completo, azul en progreso, rojo si hay vencidos

### Card de viaje (padre)
- Siempre incluye imagen miniatura del destino
- Estado de inscripción badge en esquina superior derecha
- 3 sub-cards: Pagos / Docs / Alojamiento

### File uploader
- Arrastra o clic para seleccionar
- Preview del nombre y tamaño antes de confirmar
- Progress bar durante upload
- Error claro si: formato no permitido o tamaño > 10 MB

### Alertas del dashboard
- Siempre con deep-link a la acción concreta
- Icono de color semántico (🔴 urgente, 🟡 pendiente)
- Nunca texto genérico como "Tienes documentación pendiente" sin CTA

---

## Preferencias de Notificación (Configuración del Padre)

**URL:** `/app/configuracion/notificaciones/`

```
Canal principal:
● WhatsApp (+51 9XX XXX XXX)
○ SMS
○ Email (carlos@gmail.com)
○ Solo notificaciones in-app

Horario de envío:
● 9:00 – 20:00h (recomendado)
○ Solo días laborables
○ Cualquier hora

Frecuencia máxima:
● 1 mensaje por canal por día
○ Sin límite para eventos críticos
```
