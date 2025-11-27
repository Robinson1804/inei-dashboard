# Explicación de la Plantilla de Excel para Dashboard de Adquisiciones

## Resumen

Este documento explica la estructura de la plantilla de Excel **`Plantilla_Adquisiciones.xlsx`** y cómo se relacionan sus columnas con los gráficos y visualizaciones del Dashboard de Adquisiciones.

---

## Estructura de la Plantilla

La plantilla contiene **5 hojas**:

### 1. **Instrucciones**
Guía completa de uso de la plantilla con:
- Descripción de cada campo
- Valores permitidos
- Formatos requeridos
- Notas importantes

### 2. **Adquisiciones** (HOJA PRINCIPAL - OBLIGATORIA)
Contiene los datos principales de cada adquisición. Esta es la hoja que alimenta el dashboard.

### 3. **Detalle_Adquisicion** (OPCIONAL)
Información adicional y detallada de cada adquisición.

### 4. **Proceso_Timeline** (OPCIONAL)
Hitos y pasos del proceso de cada adquisición (para el timeline visual).

### 5. **Valores_Permitidos**
Referencia rápida de valores válidos para campos con opciones específicas.

---

## Columnas de la Hoja "Adquisiciones" (Principal)

### Columnas Obligatorias

| Columna | Descripción | Ejemplo | Uso en Dashboard |
|---------|-------------|---------|------------------|
| **Año** | Año de la adquisición | 2025 | Filtro de año, agrupación temporal |
| **UE** | Código de Unidad Ejecutora (DDNNTT) | CIDE, DNCE, DNCN | Filtro de UE, Gráfico de montos por DDNNTT, % Avance por DDNNTT |
| **Meta** | Descripción de la Meta Presupuestal | 0001 - Administración y Planeamiento | Filtro de meta, agrupación |
| **Descripción** | Descripción completa del bien/servicio | Adquisición de equipos de cómputo | Tabla detallada, búsqueda |
| **Estado** | Estado actual de la adquisición | EN PROCESO, CULMINADO, CANCELADO, HISTORICO, NO INICIADO | Gráfico de distribución por estado, filtro, métricas de culminados |
| **Monto_Referencial** | Presupuesto asignado (PIM) en Soles | 125000.00 | Métrica "Monto Total (PIM)", Gráfico de montos, cálculo de % avance |

### Columnas Opcionales

| Columna | Descripción | Ejemplo | Uso en Dashboard |
|---------|-------------|---------|------------------|
| **Código** | Código único de adquisición | ADQ-2025-001 | Identificador único, enlace al modal de detalle |
| **Cantidad** | Cantidad de unidades a adquirir | 25 | Tabla detallada |
| **Tipo_Servicio** | Tipo de adquisición | BIEN, SERVICIO | Filtro de tipo, clasificación |
| **Tipo_Proceso** | Tipo de proceso de contratación | Adjudicación Simplificada, Licitación Pública | Tabla detallada |
| **Monto_Adjudicado** | Monto adjudicado/ejecutado en Soles | 120000.00 | Métrica "Monto Adquiridos", Gráfico de montos, % avance, gráfico mensual |
| **Proveedor** | Nombre del proveedor adjudicado | Imprenta Nacional S.A. | Tabla detallada, búsqueda |
| **Fecha_Convocatoria** | Fecha de convocatoria | 15/03/2024 | Información de timeline |
| **Fecha_Adjudicacion** | Fecha de adjudicación/certificación | 20/05/2024 | Gráfico "Certificado por Mes" |

### Columna Calculada Automáticamente

| Columna | Descripción | Fórmula |
|---------|-------------|---------|
| **Avance_%** | Porcentaje de avance de la adquisición | (Monto_Adjudicado / Monto_Referencial) × 100 |

---

## Relación con Visualizaciones del Dashboard

### 🔢 Métricas del Resumen Ejecutivo

| Métrica | Cálculo | Columnas Usadas |
|---------|---------|-----------------|
| **Total Requerimientos** | Conteo total de filas | Todas las adquisiciones |
| **Total Adquiridos (Culminados)** | Conteo de filas con Estado = "CULMINADO" | Estado |
| **Monto Total (PIM)** | Suma de todos los Monto_Referencial | Monto_Referencial |
| **Monto Adquiridos (Culminados)** | Suma de Monto_Adjudicado donde Estado = "CULMINADO" | Estado, Monto_Adjudicado |
| **% Avance (Adqui. / PIM)** | (Monto Adquiridos / Monto Total) × 100 | Monto_Referencial, Monto_Adjudicado, Estado |

### 📊 Gráfico 1: Adquisiciones por Estado (Pie Chart)

**Columnas usadas:**
- `Estado`: Agrupa y cuenta adquisiciones por estado

**Visualización:** Gráfico circular que muestra la distribución de adquisiciones según su estado (EN PROCESO, CULMINADO, CANCELADO, etc.)

### 📊 Gráfico 2: Montos por DDNNTT (Grouped Bar Chart)

**Columnas usadas:**
- `UE`: Agrupa por Unidad Ejecutora
- `Monto_Referencial`: Barra "PIM"
- `Monto_Adjudicado`: Barra "Monto Adquiridos"

**Visualización:** Gráfico de barras agrupadas comparando PIM vs Monto Adquirido por cada DDNNTT.

### 📊 Gráfico 3: Certificado por Mes (Bar Chart)

**Columnas usadas:**
- `Fecha_Adjudicacion`: Extrae el mes
- `Monto_Adjudicado`: Suma por mes

**Visualización:** Gráfico de barras que muestra las adquisiciones certificadas (adjudicadas) por mes.

### 📊 Gráfico 4: % Avance por DDNNTT (Horizontal Bar Chart)

**Columnas usadas:**
- `UE`: Agrupa por Unidad Ejecutora
- `Monto_Referencial`: Suma por UE
- `Monto_Adjudicado`: Suma por UE
- **Cálculo:** (Suma Monto_Adjudicado / Suma Monto_Referencial) × 100

**Visualización:** Gráfico de barras horizontales mostrando el porcentaje de avance de cada DDNNTT.

### 📋 Tabla Detallada de Adquisiciones

**Columnas mostradas:**
- Año
- UE
- Meta
- Código
- Descripción
- Tipo_Servicio
- Cantidad
- Tipo_Proceso
- Estado
- Monto_Referencial (formateado como S/ X,XXX.XX)
- Monto_Adjudicado (formateado como S/ X,XXX.XX)
- Proveedor
- Avance_%

**Funcionalidades:**
- Búsqueda por Descripción o Proveedor
- Filtro por adquisiciones específicas
- Selección de fila para ver detalle completo en modal

---

## Columnas de la Hoja "Detalle_Adquisicion" (Opcional)

Esta hoja complementa la información de cada adquisición:

| Columna | Descripción | Ejemplo |
|---------|-------------|---------|
| **Código_Adquisicion** | Código que enlaza con la hoja Adquisiciones | ADQ-2025-001 |
| **PIM_Asignado** | PIM específicamente asignado a esta adquisición | 125000.00 |
| **Requerimientos_Total** | Total de requerimientos a adquirir | 5 |
| **Requerimientos_Adquiridos** | Requerimientos ya adquiridos | 3 |
| **Unidad_Responsable** | Unidad organizacional responsable | Oficina de Tecnologías de la Información |
| **Observaciones** | Comentarios adicionales | Proceso en evaluación técnica |

**Uso:** Se muestra en el modal de detalle de adquisición.

---

## Columnas de la Hoja "Proceso_Timeline" (Opcional)

Esta hoja registra los hitos del proceso de adquisición para visualizar el timeline:

| Columna | Descripción | Ejemplo |
|---------|-------------|---------|
| **Código_Adquisicion** | Código que enlaza con la hoja Adquisiciones | ADQ-2025-002 |
| **Orden** | Orden secuencial del hito | 1, 2, 3... |
| **Hito** | Nombre del hito o paso del proceso | Elaboración de TDR |
| **Tipo_Flujo** | Área responsable | OTIN, OTA |
| **Responsable_Area** | Nombre del área responsable | Unidad Solicitante |
| **Responsable_Correo** | Email del responsable | usuario@inei.gob.pe |
| **Fecha_Inicio** | Fecha de inicio del hito | 10/01/2025 |
| **Fecha_Fin** | Fecha de finalización del hito | 17/01/2025 |
| **Dias_Transcurridos** | Días que tomó el hito | 7 |
| **Comentarios** | Comentarios sobre el hito | TDR aprobados |

**Uso:** Se visualiza en el modal de detalle como un timeline horizontal con colores por Tipo_Flujo:
- **OTIN**: Naranja (#FFB84D)
- **OTA**: Verde claro (#90EE90)

---

## Valores Permitidos

### Campo: Estado
- `EN PROCESO`
- `CULMINADO`
- `CANCELADO`
- `HISTORICO`
- `NO INICIADO`

### Campo: Tipo_Servicio
- `BIEN`
- `SERVICIO`

### Campo: Tipo_Flujo
- `OTIN` (Oficina de Tecnologías de la Información)
- `OTA` (Oficina Técnica de Administración)

### Campo: UE (Ejemplos comunes)
- `CIDE` - Centro de Investigación y Desarrollo
- `DNCE` - Dirección Nacional de Censos y Encuestas
- `DNCN` - Dirección Nacional de Cuentas Nacionales
- `DNPD` - Dirección Nacional de Producción de Datos
- `DNIA` - Dirección Nacional de Información Ambiental

---

## Filtros del Dashboard

El dashboard incluye los siguientes filtros (todos multiselección excepto Año):

| Filtro | Origen | Valores |
|--------|--------|---------|
| **Año** | Columna `Año` | Selector único: Todos, 2024, 2025, etc. |
| **Meta** | Columna `Meta` | Multiselección de todas las metas disponibles |
| **DDNNTT (UE)** | Columna `UE` | Multiselección de todas las UE disponibles |
| **Tipo (Bien/Servicio)** | Columna `Tipo_Servicio` | Multiselección: BIEN, SERVICIO |
| **Estado** | Columna `Estado` | Multiselección: EN PROCESO, CULMINADO, etc. |

---

## Formato de Datos Importantes

### Fechas
- **Formato requerido:** DD/MM/YYYY
- **Ejemplo:** 15/03/2024
- Las fechas vacías son permitidas

### Montos
- **Formato:** Números sin símbolos de moneda ni separadores
- **Ejemplo correcto:** 150000.00
- **Ejemplo incorrecto:** S/ 150,000.00
- Se recomienda usar 2 decimales

### Códigos de Adquisición
- **Formato sugerido:** ADQ-YYYY-NNN
- **Ejemplo:** ADQ-2025-001
- Deben ser únicos

---

## Flujo de Importación

1. **Completar la hoja "Adquisiciones"** con los datos principales
2. **(Opcional)** Completar "Detalle_Adquisicion" para información adicional
3. **(Opcional)** Completar "Proceso_Timeline" para visualizar el timeline de procesos
4. **Guardar el archivo Excel**
5. **Importar desde el Dashboard:**
   - Ir a la pestaña "Importar/Exportar"
   - Seleccionar el año de importación
   - Cargar el archivo Excel
   - Hacer clic en "Importar Datos"

---

## Ejemplos Incluidos en la Plantilla

La plantilla incluye **5 ejemplos** de adquisiciones que cubren diferentes escenarios:

1. **ADQ-2025-001:** Adquisición en proceso (BIEN)
2. **ADQ-2025-002:** Adquisición culminada (SERVICIO) con proceso completo
3. **ADQ-2025-003:** Adquisición culminada (SERVICIO) rápida
4. **ADQ-2025-004:** Adquisición no iniciada (SERVICIO)
5. **ADQ-2024-005:** Adquisición histórica del año anterior (BIEN)

Estos ejemplos sirven como guía para completar sus propios datos.

---

## Notas Técnicas

- El campo **Avance_%** se calcula automáticamente y no necesita ser completado manualmente
- Los códigos de UE y Meta deben existir previamente en el sistema o serán creados automáticamente
- Las fechas pueden estar vacías (NULL) si el proceso no ha llegado a esa etapa
- El **Monto_Adjudicado** puede ser 0 si la adquisición no está culminada
- Solo las adquisiciones con **Estado = "CULMINADO"** se consideran en las métricas de "Adquiridos"

---

## Soporte

Para más información sobre el uso del dashboard, consulte:
- **CLAUDE.md** - Documentación técnica del proyecto
- **app.py** - Página principal del dashboard
- **pages/dashboard.py** - Código del dashboard de adquisiciones
- **database.py** - Estructura de la base de datos
