# Reporte de validación — Manual de Evaluación y Calificación del Desempeño Académico

## Estado de generación

- Páginas procesadas: **30**.
- `manual_desempeno_final.svg`: **generado correctamente**.
- `manual_desempeno_final.pdf`: **generado correctamente**.
- `preview/`: **30 PNG**, una vista por página.
- `inkscape:page`: **30 / 30**.
- Errores automáticos de overflow/exportación/estructura SVG: **0**.
- Texto del generador: **`<text>` / `<tspan>`**, sin conversión a paths.
- Imágenes raster insertadas en el SVG final: **0**.

## Estado de los activos gráficos

El archivo `contenido_manual_desempeno.md` referencia **31 activos externos**. El paquete actualmente disponible, `figuras_manual_desempeno.zip`, contiene únicamente tres archivos **PNG**, no SVG:

1. `FIG_LOGICA_CONSTRUCCION_CDA.png`
2. `FIG_RUBRICA_GENERAL_DESEMPENO.png`
3. `FIG_FLUJO_RECURSOS_APELACION.png`

Por contrato editorial y por instrucción del proyecto, estos tres PNG **no fueron incrustados**: hacerlo rasterizaría las figuras y rompería el requisito de editabilidad vectorial. Tampoco fueron trazados o convertidos a paths, porque el texto dejaría de ser editable.

### Activos raster detectados pero incompatibles

- Página 10 — `FIG_LOGICA_CONSTRUCCION_CDA` → `FIG_LOGICA_CONSTRUCCION_CDA.png`.
- Página 17 — `FIG_RUBRICA_GENERAL_DESEMPENO` → `FIG_RUBRICA_GENERAL_DESEMPENO.png`.
- Página 27 — `FIG_FLUJO_RECURSOS` → `FIG_FLUJO_RECURSOS_APELACION.png` (correspondencia semántica probable por nombre).

### Referencias sin activo SVG disponible

- Página 05: `FIG_GOBERNANZA_INSTANCIAS`
- Página 07: `FIG_CICLO_EVALUATIVO_4_ETAPAS`
- Página 08: `FIG_ETAPAS_CICLO_DETALLE`
- Página 09: `TABLA_CALENDARIO_INSTITUCIONAL`
- Página 10: `FIG_CRITERIOS_FORMULACION_CDA`
- Página 11: `FIG_CONTENIDO_MINIMO_CDA`
- Página 11: `FIG_FLUJO_FORMALIZACION_CDA`
- Página 12: `FIG_CAUSAS_MODIFICACION_CDA`
- Página 12: `FIG_CALCULO_TIEMPO_COMPLEMENTARIO`
- Página 13: `FIG_ESTRUCTURA_REGISTRO_ACTIVIDAD`
- Página 14: `TABLA_TIPOS_EVIDENCIA`
- Página 15: `FIG_CRITERIOS_EVALUACION_ACTIVIDADES`
- Página 16: `FIG_FORMULA_CALIFICACION`
- Página 16: `TABLA_ESCALA_CALIFICACION`
- Página 18: `FIG_AREAS_ACADEMICAS`
- Página 19: `FIG_ACTIVIDADES_DOCENCIA`
- Página 20: `FIG_ACTIVIDADES_INVESTIGACION`
- Página 21: `FIG_ACTIVIDADES_INVESTIGACION_CONT`
- Página 21: `FIG_ACTIVIDADES_VINCULACION`
- Página 22: `FIG_ACTIVIDADES_EDUCACION_CONTINUA`
- Página 23: `FIG_ACTIVIDADES_ASISTENCIA_TECNICA`
- Página 24: `FIG_ACTIVIDADES_ADMINISTRACION`
- Página 24: `FIG_ACTIVIDADES_PERFECCIONAMIENTO`
- Página 25: `FIG_FLUJO_RETROALIMENTACION`
- Página 25: `FIG_PRINCIPIOS_RETROALIMENTACION`
- Página 27: `FIG_EFECTOS_CALIFICACION`
- Página 28: `FIG_REQUISITOS_PLATAFORMA`
- Página 30: `FIG_APERTURA_ANEXOS`

## Controles aplicados

- A4 vertical `210 × 297 mm`.
- Retícula principal `18–192 mm`.
- Header y footer construidos como componentes reutilizables.
- Tipografías del sistema: `Noto Serif Display` y `Noto Sans`.
- Paleta institucional del diseño maestro.
- SVG multipágina mediante `inkscape:page`.
- Capas y grupos semánticos por página y por componente.
- IDs únicos verificados automáticamente.
- Sin `<image>` raster inesperado.
- Sin filtros, máscaras ni `clipPath` añadidos por el generador.
- Sin reducción silenciosa de tipografía para resolver overflow.
- Exportación individual de cada página y ensamblaje posterior del PDF.

## Estado de cierre

La **arquitectura, el SVG multipágina, el PDF y las 30 previsualizaciones están generados y son reproducibles**, pero la integración gráfica no puede considerarse cerrada mientras los activos referenciados no estén disponibles en **SVG vectorial editable**. El generador ya está preparado para detectar e incorporar automáticamente esos SVG cuando se agreguen al repositorio o al ZIP correspondiente.
