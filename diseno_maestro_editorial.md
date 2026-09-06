# EDITORIAL_DESIGN_SYSTEM

**Documento:** sistema maestro editorial para manual institucional multipágina en SVG editable para Inkscape  
**Formato de destino:** SVG 1.1 / SVG2 compatible con Inkscape, multipágina mediante `inkscape:page`  
**Unidades maestras:** milímetros (`mm`) en geometría editorial; coordenadas SVG normalizadas a `viewBox="0 0 210 297"` por página  
**Familias tipográficas maestras:** `Noto Serif Display` + `Noto Sans`  
**Principio de normalización:** cuando el archivo fuente presenta pequeñas variaciones entre páginas, se adopta el valor modal o el valor geométrico más consistente con la línea editorial predominante.

---

## DESIGN_PRINCIPLES

### Identidad editorial

- Carácter institucional, técnico y académico.
- Composición sobria, limpia y de alto contraste, con predominio de fondo blanco.
- El azul oscuro funciona como color estructural y tipográfico principal; los azules medios y claros se reservan para jerarquía secundaria, iconografía, reglas, fondos suaves y estados informativos.
- La relación tipográfica es deliberadamente dual:
  - `Noto Serif Display`: títulos de gran jerarquía, numeraciones protagonistas, folios y títulos editoriales.
  - `Noto Sans`: cuerpo, rótulos, tablas, encabezados institucionales, tarjetas, notas y metadatos.
- El sistema privilegia espacio blanco visible sobre la compresión de contenido.
- Las figuras, iconos y diagramas son funcionales: explican estructura, procesos, categorías o relaciones; no son decoración gratuita.
- El ritmo visual se construye con:
  - filetes finos;
  - bloques de azul muy claro;
  - tarjetas con bordes delgados;
  - alternancia entre páginas densas y páginas de respiración;
  - alineación estricta a retícula.
- No usar sombras, degradados, 3D, texturas ni efectos pesados.
- La densidad máxima admisible debe resolverse mediante redistribución, cambio de retícula o división de página antes de reducir tipografía.

---

# PAGE_FORMAT

| Token | Valor |
|---|---:|
| PAGE_SIZE | A4 vertical |
| PAGE_WIDTH | 210 mm |
| PAGE_HEIGHT | 297 mm |
| SVG_VIEWBOX | `0 0 210 297` |
| BACKGROUND | `#FFFFFF` |
| UNIT | mm |
| PAGE_BLEED | 0 mm por defecto |
| SAFE_EDGE_MIN | 15 mm |
| STANDARD_CONTENT_MARGIN | 18 mm |
| TWO_COLUMN_TEXT_MARGIN | 18 mm |
| DENSE_LEGACY_TOLERANCE | 20 mm óptico cuando una composición existente lo requiera |

### Área segura

- Área editorial estándar: `x = 18…192 mm`.
- Ancho útil estándar: `174 mm`.
- Ningún texto principal debe quedar a menos de `15 mm` del borde físico.
- Las únicas excepciones admisibles fuera del área útil son:
  - fondo;
  - ilustraciones deliberadamente a sangre;
  - marcas de página;
  - elementos de portada expresamente diseñados para ello.

---

# PAGE_MARGINS

## Márgenes normalizados

| Token | Valor |
|---|---:|
| MARGIN_LEFT | 18 mm |
| MARGIN_RIGHT | 18 mm |
| MARGIN_TOP_PHYSICAL | 12 mm |
| MARGIN_BOTTOM_PHYSICAL | 8 mm |
| CONTENT_X0 | 18 mm |
| CONTENT_X1 | 192 mm |
| CONTENT_WIDTH | 174 mm |
| HEADER_RULE_Y | 38.14 mm |
| STANDARD_CONTENT_START_Y | 44–48 mm |
| FOOTER_RULE_Y | 274.54 mm |
| FOOTER_TEXT_Y | 280–289 mm |
| CONTENT_SAFE_BOTTOM | 270 mm |

### Área de encabezado

- Zona funcional: `y = 10…38.14 mm`.
- Filete inferior del encabezado: `y = 38.14 mm`.
- Grosor maestro del filete: `0.32 mm`.
- El contenido principal no debe comenzar por encima de `44 mm`, salvo portada o apertura de sección.

### Área de pie

- Filete superior del pie: `y = 274.54 mm`.
- Texto de ciudad/año: dentro de `y = 280…286 mm`.
- Folio: alineado al borde derecho de la retícula, dentro de `x ≈ 183…192 mm`.
- El contenido regular debe terminar antes de `y = 270 mm`.

---

# GRID_SYSTEM

Todas las retículas parten de `CONTENT_X0 = 18 mm` y terminan en `CONTENT_X1 = 192 mm`, salvo excepción declarada.

## GRID_SINGLE_COLUMN

| Parámetro | Valor |
|---|---:|
| x inicial | 18 mm |
| ancho | 174 mm |
| columnas | 1 |
| gutter | 0 mm |
| x final | 192 mm |

**Usos:** aperturas, introducciones, tablas protagonistas, diagramas amplios, figuras hero, textos breves de alta jerarquía.

---

## GRID_TWO_COLUMNS_EQUAL

| Parámetro | Columna 1 | Columna 2 |
|---|---:|---:|
| x inicial | 18 mm | 108 mm |
| ancho | 84 mm | 84 mm |
| x final | 102 mm | 192 mm |

- `GUTTER = 6 mm`.
- Eje del gutter: `105 mm`.
- La alineación izquierda de cada columna es obligatoria.
- Los filetes, títulos y bloques deben respetar el mismo eje de comienzo que su columna.
- **Uso principal:** páginas normativas a dos columnas, texto + panel, dos bloques de contenido equivalentes.

---

## GRID_TWO_COLUMNS_ASYMMETRIC

### Variante A — texto dominante izquierda

| Parámetro | Columna 1 | Columna 2 |
|---|---:|---:|
| x inicial | 18 mm | 108 mm |
| ancho | 90 mm | 84 mm |
| gutter óptico | 6 mm | — |

Aplicar solo cuando el bloque izquierdo requiera mayor línea de lectura; el borde externo derecho nunca debe superar `192 mm`.

### Variante B — panel dominante derecha

| Parámetro | Columna 1 | Columna 2 |
|---|---:|---:|
| x inicial | 18 mm | 102 mm |
| ancho | 78 mm | 90 mm |
| gutter | 6 mm | — |

**Usos:** texto + panel informativo, texto + figura vertical, narrativa + resumen estructurado.

---

## GRID_THREE_COLUMNS

- Área útil: `174 mm`.
- Gutter: `6 mm`.
- Ancho de columna: `54 mm`.

| Columna | x inicial | x final |
|---|---:|---:|
| 1 | 18 mm | 72 mm |
| 2 | 78 mm | 132 mm |
| 3 | 138 mm | 192 mm |

**Usos:** comparaciones, tres categorías, tres bloques analíticos, resúmenes paralelos.

---

## GRID_FOUR_CARDS

- Área útil: `174 mm`.
- Ancho normalizado por tarjeta: `39.5 mm`.
- Gutter: `5.33 mm`.
- Radio: `2.3–2.5 mm`.

| Tarjeta | x inicial aproximado |
|---|---:|
| 1 | 18.00 mm |
| 2 | 62.83 mm |
| 3 | 107.66 mm |
| 4 | 152.49 mm |

**Uso:** principios, etapas, dimensiones o categorías en secuencia de cuatro.

---

## GRID_FIVE_CARDS

- Área útil: `174 mm`.
- Ancho de tarjeta: `30 mm`.
- Gutter: `6 mm`.

| Tarjeta | x inicial |
|---|---:|
| 1 | 18 mm |
| 2 | 54 mm |
| 3 | 90 mm |
| 4 | 126 mm |
| 5 | 162 mm |

**Uso:** áreas, categorías, síntesis de cinco componentes.

---

# TYPOGRAPHY_SYSTEM

> En este sistema, los valores numéricos de `font-size` se expresan en unidades del `viewBox` A4; al usar `viewBox="0 0 210 297"` corresponden geométricamente a mm de composición. Se entrega también una equivalencia aproximada en puntos para documentación.

| Token | Familia | Peso | Tamaño | Equiv. aprox. | Interlineado | Color | Uso |
|---|---|---:|---:|---:|---:|---|---|
| DISPLAY_XL | Noto Serif Display | 600 | 13.2 mm | 37.4 pt | 14.5–15.5 mm | PRIMARY_BLUE | grandes aperturas |
| DISPLAY_L | Noto Serif Display | 600 | 11.85 mm | 33.6 pt | 13.0–14.0 mm | PRIMARY_BLUE | títulos principales |
| DISPLAY_M | Noto Serif Display | 600 | 7.05 mm | 20.0 pt | 8.2–8.8 mm | PRIMARY_BLUE | títulos editoriales medianos |
| SECTION_NUMBER_XL | Noto Serif Display | 500 | 31.5 mm | 89.3 pt | 31.5 mm | PRIMARY_BLUE | número protagonista de sección |
| ARTICLE_TITLE | Noto Serif Display | 600 | 4.59 mm | 13.0 pt | 5.3–5.8 mm | PRIMARY_BLUE | título de artículo/componente |
| ARTICLE_TITLE_COMPACT | Noto Serif Display | 600 | 4.06 mm | 11.5 pt | 4.8–5.2 mm | PRIMARY_BLUE | título compacto |
| SECTION_LABEL | Noto Sans | 700 | 3.53–4.06 mm | 10–11.5 pt | 4.5–5.0 mm | SECONDARY_BLUE | rótulo superior / kicker |
| BODY | Noto Sans | 400 | 3.02–3.18 mm | 8.6–9.0 pt | 3.8–4.35 mm | TEXT_PRIMARY | cuerpo general |
| BODY_SMALL | Noto Sans | 400 | 2.72–2.82 mm | 7.7–8.0 pt | 3.35–3.70 mm | TEXT_PRIMARY | tarjetas, tablas, paneles |
| BODY_XS | Noto Sans | 400 | 2.35–2.55 mm | 6.7–7.2 pt | 2.9–3.25 mm | TEXT_PRIMARY | metadatos y notas breves |
| LABEL | Noto Sans | 700 | 2.70–3.18 mm | 7.7–9.0 pt | 3.3–3.9 mm | TEXT_PRIMARY | etiquetas, cabeceras, nombres de bloque |
| CAPTION | Noto Sans | 400 | 2.35–2.65 mm | 6.7–7.5 pt | 3.0–3.4 mm | TEXT_SECONDARY | caption y fuente descriptiva |
| HEADER_BRAND | Noto Sans | 700 | 3.0–5.0 mm | 8.5–14.2 pt | según lockup | PRIMARY_BLUE | identidad institucional |
| HEADER_META | Noto Sans | 400 | 2.75–3.0 mm | 7.8–8.5 pt | 3.3–3.6 mm | PRIMARY_BLUE | lema / metadata |
| FOOTER_META | Noto Sans | 400 | 3.05–3.18 mm | 8.6–9.0 pt | 3.5–3.9 mm | PRIMARY_BLUE | ciudad/año |
| PAGE_NUMBER | Noto Serif Display | 600 | 8.10–8.11 mm | 23.0 pt | 8.1 mm | PRIMARY_BLUE | folio |
| LARGE_STAT | Noto Serif Display | 500 | 14–18 mm | 39.7–51 pt | 14–19 mm | PRIMARY_BLUE | gran cifra |
| CARD_NUMBER | Noto Serif Display | 500 | 6.0 mm | 17 pt | 6.0 mm | PRIMARY_BLUE | numeración protagonista de tarjeta |

## Reglas tipográficas

- `Noto Serif Display` se usa para:
  - títulos de gran jerarquía;
  - numeración de secciones;
  - títulos editoriales de artículos;
  - folios;
  - grandes cifras.
- `Noto Sans` se usa para:
  - cuerpo;
  - tablas;
  - encabezados institucionales;
  - etiquetas;
  - tarjetas;
  - notas;
  - descripciones;
  - captions.
- No convertir texto a contornos.
- Cuerpo general mínimo: `2.65 mm` (~7.5 pt).
- Cuerpo recomendado: `2.82–3.18 mm`.
- Tamaños `2.15–2.55 mm` solo se admiten en etiquetas muy breves, metadatos o tarjetas; nunca en párrafos largos.
- Interlineado mínimo de cuerpo: `1.20 × font-size`.
- Interlineado recomendado: `1.25–1.38 × font-size`.
- Tracking:
  - cuerpo: `0`;
  - títulos serif: `0`;
  - rótulos en mayúsculas: `0.6–0.9 mm` de letter-spacing en el sistema SVG actual.
- Mayúsculas: solo para rótulos, labels, títulos de sección muy breves y metadata institucional.
- No usar versalitas sintéticas.
- Evitar líneas de cuerpo de más de `70–75 caracteres`.
- Evitar columnas con menos de `35 caracteres` por línea en cuerpo principal.

---

# COLOR_SYSTEM

| Token | HEX | Uso |
|---|---|---|
| PRIMARY_BLUE | `#0A2D69` | texto principal, iconos, títulos, líneas estructurales |
| SECONDARY_BLUE | `#5B94D2` | acentos, bordes de tarjetas, rótulos, numeradores |
| LIGHT_BLUE | `#88B4E3` | acentos secundarios, iconografía suave |
| VERY_LIGHT_BLUE | `#EEF5FC` | fondos de iconos, tarjetas suaves, paneles |
| SOFT_BLUE | `#E8F2FC` | fondos alternativos de tarjetas |
| TABLE_HEADER | `#DDEAF8` | cabecera de tablas |
| PALE_BLUE | `#DCEAF8` | fondos auxiliares |
| RULE_BLUE | `#A8C4E6` | filetes y divisores suaves |
| RULE_BLUE_DARK | `#9FC0E4` | reglas secundarias con algo más de contraste |
| TEXT_PRIMARY | `#0A2D69` | cuerpo principal |
| TEXT_SECONDARY | `#5B94D2` | metadatos, rótulos, ayudas |
| BACKGROUND | `#FFFFFF` | fondo de página |
| CARD_FILL | `#FFFFFF` | tarjeta estándar |
| CARD_FILL_ALT | `#EEF5FC` | tarjeta enfatizada |
| WHITE | `#FFFFFF` | texto invertido y fondos |

## Reglas de color

- El 80–90 % de la superficie de una página estándar debe permanecer blanca.
- `PRIMARY_BLUE` domina la tipografía y la iconografía.
- `SECONDARY_BLUE` no debe competir con títulos principales.
- Fondos coloreados deben ser claros y planos.
- Evitar más de tres intensidades de azul visibles simultáneamente en un mismo componente.

---

# MASTER_PAGES

## MASTER_COVER

- Página A4 vertical.
- Fondo blanco.
- Identidad institucional en franja superior.
- Título principal serif de gran escala.
- Subtítulo sans.
- Figura o ilustración principal en zona media/inferior.
- Filete inferior y pie institucional.
- Folio puede omitirse o integrarse de forma editorial.
- Uso de espacio blanco: alto; ocupación máxima recomendada `65–70 %`.

## MASTER_TOC

- Encabezado institucional.
- Título principal en `DISPLAY_L` o `DISPLAY_M`.
- Índice en una o dos columnas según cantidad.
- Líneas de separación finas (`0.22–0.32 mm`).
- Numeración alineada en eje independiente.
- No usar fondos de alto contraste detrás del índice.

## MASTER_SECTION_OPENING_ODD

- Geometría no espejada por defecto.
- Encabezado institucional.
- `SECTION_LABEL` + `SECTION_NUMBER_XL` opcional + `DISPLAY_XL`.
- Inicio de contenido entre `y = 44–60 mm`.
- Zona de respiración mínima antes del primer bloque: `8 mm`.
- Folio en extremo derecho del pie.

## MASTER_SECTION_OPENING_EVEN

- Misma retícula que la versión impar.
- Mantener identidad no espejada para conservar continuidad institucional.
- Si se activa modo libro/duplex, solo el folio puede migrar al borde exterior izquierdo; el contenido no se espeja automáticamente.

## MASTER_STANDARD_ODD

- Encabezado estándar.
- Área útil `18–192 mm`.
- Contenido desde `y = 44–48 mm`.
- Pie estándar.
- Folio a la derecha.

## MASTER_STANDARD_EVEN

- Mismas cotas que `MASTER_STANDARD_ODD`.
- La línea editorial real es no espejada.
- En impresión encuadernada, permitir variante opcional de folio exterior; no alterar columnas ni encabezado sin orden explícita.

## MASTER_ANNEX_OPENING

- Encabezado institucional completo.
- Título de anexos en serif.
- Ilustración técnica o figura hero opcional.
- Alta proporción de blanco.
- Pie estándar.

---

# HEADER_SYSTEM

## HEADER_FULL_INSTITUTIONAL

- Zona: `x = 18…192 mm`, `y ≈ 10…38.14 mm`.
- Filete inferior: `y = 38.14 mm`.
- Grosor: `0.32 mm`.
- Identidad institucional izquierda.
- Lema o metadata institucional a la derecha.
- Separador vertical interno admitido: `0.25–0.32 mm`.
- Tipografía: `Noto Sans`.
- Color: `PRIMARY_BLUE`.

## HEADER_TEXTUAL_MANUAL

- Para páginas de alta densidad.
- Marca textual compacta.
- Regla horizontal.
- Altura máxima recomendada: `20–24 mm`.

## HEADER_SECTION_OPENING

- Mantiene identidad institucional.
- Puede reducir densidad de metadata.
- Debe dejar más aire antes del título principal.

## HEADER_COVER

- Lockup institucional completo.
- No competir en escala con el título de portada.
- Puede incluir separador vertical y lema.

## HEADER_ANNEX

- Igual estructura institucional base.
- Admite rótulo específico de anexos en el bloque de contenido, no dentro del logotipo.

---

# FOOTER_SYSTEM

| Elemento | Especificación |
|---|---|
| FOOTER_RULE_Y | 274.54 mm |
| FOOTER_RULE_WIDTH | 170–174 mm |
| FOOTER_RULE_STROKE | 0.30–0.32 mm |
| FOOTER_RULE_COLOR | PRIMARY_BLUE o RULE_BLUE |
| FOOTER_META_X | 18–20 mm |
| FOOTER_META_Y | 280–286 mm |
| PAGE_NUMBER_RIGHT_EDGE | 192 mm |
| PAGE_NUMBER_SIZE | 8.10–8.11 mm |
| PAGE_NUMBER_FONT | Noto Serif Display 600 |
| PAGE_NUMBER_COLOR | PRIMARY_BLUE |

- Ciudad/año: alineación izquierda.
- Folio: alineación derecha (`text-anchor="end"`).
- No colocar contenido principal por debajo de `270 mm`.
- En el sistema real, par e impar mantienen el folio a la derecha; la versión espejada es opcional, no predeterminada.

---

# COMPONENT_LIBRARY

## ARTICLE_HEADER

- Ancho: igual a columna activa.
- Título: `ARTICLE_TITLE` o `ARTICLE_TITLE_COMPACT`.
- Acento inferior: `12–16 mm` de longitud.
- Grosor del acento: `0.6–0.9 mm` cuando actúa como marca de sección; `0.22–0.32 mm` como filete.
- Separación título–cuerpo: `4–7 mm`.
- No separar título de las primeras 2 líneas de cuerpo.

## SECTION_LABEL

- `Noto Sans 700`.
- `3.53–4.06 mm`.
- `SECONDARY_BLUE`.
- Mayúsculas.
- Tracking `0.8–0.9 mm`.
- Distancia al título principal: `5–8 mm`.

## SECTION_NUMBER

- `Noto Serif Display 500`.
- Escala protagonista: hasta `31.5 mm`.
- Color `PRIMARY_BLUE`.
- No usar más de una numeración XL por página.

## INFO_CARD

- Ancho recomendado:
  - columna: `39.5–84 mm`;
  - ancho completo: `174 mm`.
- Radio: `2.3–2.5 mm`.
- Borde: `0.28–0.35 mm`, `SECONDARY_BLUE`.
- Fill: `WHITE` o `VERY_LIGHT_BLUE`.
- Padding: `4–6 mm`.
- Título: `LABEL`.
- Cuerpo: `BODY_SMALL`.
- Icono: `8–12 mm`.

## ACTIVITY_CARD

- Variante pequeña: `30 × 52–65 mm`.
- Variante media: `84 × 40 mm`.
- Radio: `2.4–2.5 mm`.
- Borde: `0.28–0.35 mm`.
- Padding mínimo: `4 mm`.
- Si el cuerpo excede la capacidad: aumentar altura o cambiar a retícula de menos columnas; no reducir cuerpo bajo mínimo.

## CALLOUT_BOX

- Ancho: `174–178 mm` en full-width.
- Altura habitual: `18–24 mm`, extensible.
- Fill: `VERY_LIGHT_BLUE` o `WHITE`.
- Borde: `0.25–0.32 mm`.
- Radio: `2.0–2.5 mm`.
- Padding: `5–7 mm`.
- Icono opcional a izquierda.

## BULLET_LIST

- Sangría total: `4–6 mm`.
- Distancia viñeta–texto: `2–3 mm`.
- Viñeta: círculo o símbolo vectorial simple.
- Cuerpo: `BODY` o `BODY_SMALL`.
- Separación vertical: `2.5–4 mm`.

## NUMBERED_LIST

- Número en círculo o numeral serif.
- Diámetro habitual del círculo: `5–8 mm`.
- Espacio número–texto: `3–5 mm`.
- Reglas divisorias opcionales: `RULE_BLUE`, `0.20–0.28 mm`.

## PROCESS_STEP

- Tarjeta típica: `30 × 65 mm`.
- Radio: `2.5 mm`.
- Borde: `0.30 mm`.
- Número superior: `2.7–3.0 mm` sans bold.
- Título: `2.7–3.15 mm` sans bold.
- Cuerpo: `2.15–2.55 mm`, solo texto breve.
- Icono: `8–12 mm`.

## PROCESS_FLOW

- Disposición horizontal preferente.
- Conectores: línea `0.25–0.32 mm`.
- Flecha: path vectorial simple.
- Separación mínima entre pasos: `4–6 mm`.
- Para más de 6 pasos: dividir en dos filas o usar diagrama vertical.

## FORMULA_BOX

- Ancho observado/normalizado: `174–178 mm`.
- Altura flexible, típicamente `40–50 mm`.
- Fill: blanco o azul muy claro.
- Borde: `0.28–0.35 mm`.
- Expresión principal centrada.
- Texto auxiliar: `BODY_SMALL`.

## DATA_TABLE

- Ancho estándar: `174 mm`.
- Cabecera típica: `12 mm` de alto.
- Fill cabecera: `TABLE_HEADER`.
- Borde/reglas: `0.20–0.32 mm`.
- Cuerpo: `2.65–3.02 mm`.
- Padding horizontal: `3–5 mm`.
- Padding vertical: `2.5–4 mm`.

## MATRIX_TABLE

- Ancho: `174 mm`.
- Columnas alineadas a ejes fijos.
- Primera columna puede ser `25–35 %` del ancho.
- Cabecera: `TABLE_HEADER`.
- Usar reglas verticales solo si aumentan comprensión.
- En matrices densas, priorizar ancho de página completo.

## ICON_CARD

- Fondo: `WHITE`.
- Borde: `SECONDARY_BLUE`.
- Radio: `2.3–2.5 mm`.
- Fondo del icono: círculo `VERY_LIGHT_BLUE`.
- Icono lineal `PRIMARY_BLUE`.
- Título centrado o alineado a izquierda según patrón.

## PRINCIPLE_ITEM

- Tarjeta observada: aproximadamente `39.5 × 31.5 mm`.
- Borde: `0.28 mm`.
- Radio: `2.3 mm`.
- Icono superior centrado.
- Título serif o sans bold breve.
- Usar 4 columnas cuando existan 4 elementos por fila.

## LARGE_STAT_OR_NUMBER

- Familia: `Noto Serif Display`.
- Peso: 500.
- Tamaño: `14–31.5 mm` según función.
- Color: `PRIMARY_BLUE`.
- Debe conservar espacio blanco alrededor de al menos `6 mm`.

## DIVIDER_RULE

- Regla estructural: `0.30–0.35 mm`.
- Regla secundaria: `0.20–0.28 mm`.
- Color: `PRIMARY_BLUE`, `SECONDARY_BLUE` o `RULE_BLUE`.
- No usar negro puro.

---

# FIGURE_SYSTEM

Las figuras se producen externamente y se insertan como SVG vectorial editable.

## FIGURE_FULL_WIDTH

- x: `18 mm`.
- ancho máximo: `174 mm`.
- altura recomendada: `70–150 mm`.
- ratio preferente: `1.2:1` a `2.2:1`.
- distancia antes: `6–10 mm`.
- distancia después: `6–10 mm`.

## FIGURE_HALF_WIDTH

- ancho: `84 mm`.
- altura recomendada: `50–120 mm`.
- colocar sobre una columna de `GRID_TWO_COLUMNS_EQUAL`.
- gutter mínimo con texto lateral: `6 mm`.

## FIGURE_COLUMN

- ancho: `54 mm` en retícula de tres columnas o `84 mm` en retícula de dos.
- no exceder el borde de su columna.
- caption bajo figura: `CAPTION`, separación `3–4 mm`.

## FIGURE_TWO_COLUMN_SPAN

- ancho: `174 mm`.
- indicada para diagramas complejos que deben ocupar ambas columnas.
- texto puede continuar bajo la figura; no envolver texto alrededor salvo diseño explícito.

## FIGURE_HERO

- ancho: `150–174 mm`.
- altura: `100–180 mm`.
- reservada a portada, apertura o página de transición.
- mínimo `10 mm` de espacio blanco libre alrededor.

## FIGURE_INLINE

- ancho: `30–60 mm`.
- altura proporcional.
- solo figuras simples.
- no incrustar texto inferior a `2.65 mm`.

## DIAGRAM_HORIZONTAL

- ancho: `174 mm`.
- altura recomendada: `35–90 mm`.
- máximo 6 pasos por fila.
- conectores de `0.25–0.32 mm`.

## DIAGRAM_VERTICAL

- ancho: `84–120 mm`.
- altura: `80–190 mm`.
- alineación central o a una columna.
- pasos separados `6–12 mm`.

## Inserción SVG

- Insertar como grupo SVG editable (`<g>`), no como bitmap.
- Conservar textos como `<text>/<tspan>`.
- Evitar `image href="data:image/..."` salvo autorización.
- Ajustar el `viewBox` de la figura antes de escalarla.
- No aplicar transformaciones no uniformes.
- IDs de figuras: `fig_pXX_tipo_YY`.
- Alinear el bounding box externo exactamente a los ejes de retícula.

---

# TABLE_SYSTEM

## Encabezados

- Fill: `#DDEAF8`.
- Texto: `Noto Sans 700`, `2.65–3.02 mm`.
- Altura recomendada: `10–12 mm`.
- Padding horizontal: `3–5 mm`.

## Filas

- Altura mínima: `9–12 mm`.
- Altura automática según contenido.
- Fill estándar: blanco.
- Alternancia opcional: `#EEF5FC` con baja frecuencia.
- Regla de fila: `0.20–0.28 mm`, `RULE_BLUE`.

## Columnas

- 2 columnas: `55/45`, `60/40` o `50/50` según contenido.
- 3 columnas: base `33/33/34`, ajustable a `25/35/40`.
- 4+ columnas: usar ancho completo y reducir padding antes que tipografía.
- Alineación vertical: centro para labels breves; superior para párrafos.

## Overflow

1. aumentar altura de fila;
2. reducir padding secundario;
3. cambiar proporción de columnas;
4. usar página completa;
5. dividir tabla en páginas;
6. nunca comprimir texto por debajo del mínimo de cuerpo.

---

# TWO_COLUMN_TEXT_RULES

- Retícula base: `GRID_TWO_COLUMNS_EQUAL`.
- Columna 1: `x = 18…102 mm`.
- Columna 2: `x = 108…192 mm`.
- Ancho: `84 mm`.
- Gutter: `6 mm`.
- Inicio vertical preferente: `44–48 mm`.
- Cuerpo: `2.82–3.18 mm`.
- Interlineado: `3.6–4.35 mm`.
- Máximo recomendado por bloque continuo: `45–60 líneas` antes de introducir subtítulo, figura, tarjeta o salto de página.
- Equilibrar columnas por masa visual, no por número exacto de caracteres.
- Evitar una segunda columna con menos de `25 %` de ocupación si la primera está llena; en ese caso cambiar a una columna o redistribuir.
- No cortar título + primera línea del cuerpo entre columnas.
- No dejar viudas/huérfanas de una sola línea.

---

# WHITE_SPACE_AND_VERTICAL_RHYTHM

| Relación | Espacio |
|---|---:|
| encabezado → contenido | 6–10 mm |
| section label → título | 5–8 mm |
| título → cuerpo | 5–7 mm |
| bloque de texto → siguiente sección | 8–14 mm |
| tarjeta → tarjeta vertical | 4–6 mm |
| fila de tarjetas → fila | 5–8 mm |
| texto → figura | 6–10 mm |
| figura → caption | 3–4 mm |
| figura → siguiente contenido | 8–12 mm |
| callout → contenido adyacente | 6–10 mm |

- Páginas de apertura: ocupación ideal `45–65 %`.
- Páginas estándar: `60–78 %`.
- Páginas densas: máximo visual recomendado `82–85 %`.
- Debe mantenerse una zona de respiración visible alrededor de títulos grandes.

---

# ICON_SYSTEM

- Estilo: lineal monocolor.
- Color principal: `#0A2D69`.
- Grosor de línea habitual: `0.22–0.34 mm`.
- Fondo circular opcional: `#EEF5FC`.
- Diámetro habitual de fondo circular: `8–15 mm`.
- Tamaño del icono: `5–12 mm`.
- Alineación:
  - centrado en tarjetas;
  - eje común en listas;
  - baseline óptica con títulos.
- Los iconos deben ser SVG nativo mediante `path`, `line`, `circle`, `rect`.
- No rasterizar.
- No usar emoji ni fuentes de iconos dependientes del sistema.
- Mantener cada icono en grupo semántico independiente.

---

# SVG_EDITABILITY_RULES

Reglas obligatorias:

1. Todo texto debe permanecer como `<text>` y `<tspan>`.
2. Nunca convertir texto a `path`.
3. Toda figura externa debe conservar SVG editable cuando sea posible.
4. Objetos agrupados semánticamente con `<g>`.
5. IDs claros, únicos y estables.
6. Convención recomendada:
   - `pXX_header`
   - `pXX_content`
   - `pXX_footer`
   - `pXX_article_YY`
   - `pXX_card_YY`
   - `pXX_fig_YY`
7. No rasterizar salvo autorización expresa.
8. Evitar `clipPath` salvo necesidad geométrica real.
9. Evitar máscaras.
10. Evitar filtros SVG.
11. Evitar transparencias complejas.
12. No usar sombras.
13. Tablas: cada celda, línea y texto como objetos independientes o subgrupos semánticos.
14. Diagramas: pasos, conectores, iconos y etiquetas independientes.
15. Usar `<g inkscape:groupmode="layer" inkscape:label="…">` para capas editoriales.
16. Mantener cada página como `inkscape:page`.
17. La implementación debe soportar **30 páginas** en el documento final, conservando un `inkscape:page` por página.
18. No depender del orden XML para deducir el número visual de página; conservar un mapa explícito `page_number ↔ inkscape:page id`.
19. Usar `viewBox="0 0 210 297"` en SVG unitario y coordenadas equivalentes por página en el documento multipágina.
20. No aplicar escalado global al texto para resolver overflow.

---

# RESPONSIVE_EDITORIAL_RULES

Cuando un contenido no cabe, aplicar estrictamente este orden:

1. redistribuir espacio vertical;
2. cambiar a una retícula más adecuada;
3. dividir contenido entre páginas;
4. reducir espacios secundarios;
5. reducir padding de tarjetas/tablas;
6. ajustar anchos de columnas;
7. solo al final reducir tipografía.

### Límites

- BODY nunca menor que `2.65 mm` (~7.5 pt).
- BODY_SMALL nunca menor que `2.50 mm` en párrafos.
- BODY_XS puede llegar a `2.20 mm` solo para metadatos o labels muy breves.
- Ningún párrafo normativo debe renderizarse a tamaño microscópico para “hacerlo caber”.
- Si el contenido excede `CONTENT_SAFE_BOTTOM = 270 mm`, debe redistribuirse o pasar a otra página.

---

# PAGE_COMPOSITION_PATTERNS

## PATTERN_A — Apertura de título

- `GRID_SINGLE_COLUMN`.
- Encabezado institucional.
- Section label en `y ≈ 45–50 mm`.
- Título `DISPLAY_L/XL`.
- Acento horizontal.
- Introducción breve.
- Figura hero opcional en mitad inferior.
- Alta proporción de blanco.

## PATTERN_B — Artículos a dos columnas

- `GRID_TWO_COLUMNS_EQUAL`.
- Dos bloques paralelos.
- Títulos alineados a `x=18` y `x=108`.
- Gutter `6 mm`.
- Cuerpo `BODY`.
- Callouts internos permitidos.

## PATTERN_C — Texto + figura

- Grid asimétrico.
- Texto `78–90 mm`.
- Figura `84–90 mm`.
- Gutter `6 mm`.
- Alineación superior compartida.

## PATTERN_D — Figura + texto lateral

- Igual a C, invertido.
- Figura a izquierda.
- Texto a derecha.
- Caption dentro del ancho de figura.

## PATTERN_E — Cuadrícula de tarjetas

- `GRID_FOUR_CARDS` o `GRID_FIVE_CARDS`.
- Alturas iguales por fila.
- Radio común.
- Iconos alineados.
- Títulos con baseline común.

## PATTERN_F — Tabla protagonista

- `GRID_SINGLE_COLUMN`.
- Tabla `174 mm`.
- Título sobre tabla.
- Nota o interpretación debajo.
- Evitar otros componentes de alta densidad en la misma página.

## PATTERN_G — Proceso secuencial

- `DIAGRAM_HORIZONTAL`.
- 4–6 etapas por fila.
- Conectores lineales.
- Tarjetas de ancho consistente.

## PATTERN_H — Página de alta densidad normativa

- Una o dos columnas.
- Body `2.82–3.02 mm`.
- Interlineado ≥ `3.5 mm`.
- Secciones separadas mediante reglas o microespacio.
- No usar tarjetas decorativas innecesarias.

## PATTERN_I — Página de transición

- Título fuerte.
- Gran espacio blanco.
- Figura o número protagonista.
- Máximo 2 bloques secundarios.

## PATTERN_J — Cierre de sección

- Una columna.
- Síntesis breve o componente final.
- Espacio blanco inferior mayor.
- Pie estándar.

---

# QUALITY_CONTROL_RULES

Todo SVG generado debe superar los siguientes controles:

## Geometría

- [ ] Ningún objeto accidental fuera de la página.
- [ ] Ningún texto fuera del área segura.
- [ ] No hay solapes no intencionados.
- [ ] No hay texto cortado.
- [ ] No hay objetos invadiendo el pie.
- [ ] Contenido principal termina antes de `270 mm`.
- [ ] Figuras alineadas a retícula.
- [ ] Gutter entre columnas ≥ `6 mm`.

## Tipografía

- [ ] Body ≥ `2.65 mm`.
- [ ] Familias restringidas a Noto Serif Display / Noto Sans, salvo excepción documentada.
- [ ] Pesos coherentes.
- [ ] Interlineado mínimo respetado.
- [ ] Sin texto convertido a paths.
- [ ] Sin líneas excesivamente largas.

## Color

- [ ] PRIMARY_BLUE = `#0A2D69`.
- [ ] SECONDARY_BLUE = `#5B94D2`.
- [ ] Fondos claros dentro de la paleta.
- [ ] No aparecen colores ajenos sin autorización.
- [ ] No se usa negro puro como color dominante.

## Encabezado y pie

- [ ] Header coherente entre páginas.
- [ ] Filete del header en posición correcta.
- [ ] Footer rule consistente.
- [ ] Folio alineado.
- [ ] Ciudad/año consistente.
- [ ] Par/impar sigue la política no espejada por defecto.

## Componentes

- [ ] Radios coherentes (`2.3–2.5 mm` en tarjetas principales).
- [ ] Bordes entre `0.28–0.35 mm`.
- [ ] Iconos lineales editables.
- [ ] Padding suficiente.
- [ ] Tarjetas de una misma fila comparten altura.

## SVG

- [ ] IDs únicos.
- [ ] Capas semánticas.
- [ ] `inkscape:page` presente para cada página.
- [ ] Sin raster inesperado.
- [ ] Sin máscaras/filtros innecesarios.
- [ ] Sin `clipPath` innecesario.
- [ ] Tablas y diagramas editables.
- [ ] El archivo abre sin advertencias en Inkscape.

---

# IMPLEMENTATION_NOTES_FOR_PYTHON_GENERATOR

## Sistema de coordenadas

Trabajar siempre en mm lógicos:

```python
PAGE_W = 210.0
PAGE_H = 297.0
CONTENT_X0 = 18.0
CONTENT_X1 = 192.0
CONTENT_W = 174.0
HEADER_RULE_Y = 38.14
FOOTER_RULE_Y = 274.54
CONTENT_SAFE_BOTTOM = 270.0
```

## Paleta

```python
PRIMARY_BLUE   = "#0A2D69"
SECONDARY_BLUE = "#5B94D2"
LIGHT_BLUE     = "#88B4E3"
VERY_LIGHT_BLUE= "#EEF5FC"
SOFT_BLUE      = "#E8F2FC"
TABLE_HEADER   = "#DDEAF8"
RULE_BLUE      = "#A8C4E6"
BACKGROUND     = "#FFFFFF"
```

## Reglas de construcción

- Crear funciones reutilizables para encabezado, pie, títulos, artículos, tarjetas, tablas, figuras y procesos.
- Separar contenido de presentación.
- Calcular bounding boxes antes de confirmar una página.
- Ejecutar una fase de validación geométrica antes de guardar.
- Si un componente excede el área disponible, devolver un estado de overflow y recomponer; nunca escalarlo silenciosamente.
- Mantener todos los atributos de texto explícitos: familia, tamaño, peso, fill, anchor.
- Guardar el SVG en UTF-8.
- No serializar texto con conversiones de encoding dependientes de Windows-1252.
- Si se manipula XML desde Python, usar `lxml` o `xml.etree` con escritura UTF-8 explícita.

---

# FINAL_DESIGN_CONTRACT

Una página nueva pertenece a este sistema editorial únicamente si:

1. usa A4 vertical de `210 × 297 mm`;
2. se alinea a la retícula de `18–192 mm`;
3. usa `Noto Serif Display` y `Noto Sans` según jerarquía;
4. usa la paleta azul institucional definida;
5. conserva el encabezado y pie maestro salvo excepción de master;
6. respeta el mínimo tipográfico;
7. mantiene espacio blanco suficiente;
8. usa componentes con radios, bordes y paddings coherentes;
9. mantiene figuras y diagramas vectoriales editables;
10. permanece totalmente editable en Inkscape;
11. no fuerza contenido mediante reducción tipográfica extrema;
12. conserva una estructura semántica de capas, grupos e IDs;
13. respeta el sistema multipágina mediante `inkscape:page`.
