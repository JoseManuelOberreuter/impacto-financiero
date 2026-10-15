# Termómetro Ánimo: sentimiento de las noticias

> Estado: **propuesta de metodología.** Investigación hecha el 15-oct-2026; fuentes al final.

## Qué queremos

Leer cada día las noticias económicas de Chile y convertirlas en un termómetro:

```
📰 Ánimo en las noticias            MÁS NEGATIVO QUE LO HABITUAL ▼
"Esta semana dominaron el desempleo y el precio de la bencina."
Basado en 412 titulares de 6 medios · al 15-oct
```

## Cómo lo han hecho otros

| Quién | Método | Fuentes | Resultado | Lección |
|---|---|---|---|---|
| **Fed de San Francisco**: Daily News Sentiment Index | **Diccionario** (léxico) de palabras positivas y negativas, ajustado a noticias económicas. Promedio móvil donde las noticias pierden peso a medida que envejecen. Ajusta por cambios en la mezcla de diarios | 24 diarios de EE. UU. (vía Factiva); artículos de economía de 200 palabras o más | Alta correlación con las encuestas de confianza del consumidor (Michigan, Conference Board) | Promediar en el tiempo y **equilibrar los medios** para que uno no domine |
| **Banco Central de Chile**: DT 938 (2022) | **Diccionario en español** creado para el estudio. Validado comparando su clasificación con una manual sobre una muestra al azar | Principales medios impresos chilenos, 2015–2020 | Alta correlación con las encuestas de confianza y buena capacidad para detectar shocks | **Prueba que funciona en Chile.** Hay que validar contra una clasificación manual |
| **Banco Central de Chile**: DT 862 y DT 930 | Diccionarios en español para analizar el tono de sus propios informes (percepciones de negocios, estabilidad financiera) | Informes del Banco Central | Índices correlacionados con la confianza empresarial | Existen diccionarios económicos en español que podemos usar de referencia |
| **Economic Policy Uncertainty** (Baker, Bloom y Davis) | Cuenta los artículos que contienen a la vez palabras de **economía + política + incertidumbre** | Diarios; versiones para Chile (Cerda et al., Banco de España) y una diaria con Twitter (Banco Central, DT 883) | Indicador de incertidumbre muy citado | Método simple para una **segunda señal: incertidumbre** |
| **GDELT** | Tono automático de noticias de todo el mundo (léxico) | Miles de medios, filtrable por país e idioma; API gratuita con límite de consultas | Gratis, pero poco cubierto en español y el tono no está validado | Útil como **comparación**, no como fuente principal |
| **RavenPack** (y similares) | Análisis de lenguaje en tiempo real sobre más de 40.000 fuentes y 13 idiomas | Comercial; precio no público; clientes institucionales | Estándar en fondos de inversión | Fuera de nuestro alcance por ahora; posible proveedor para el plan Pro |
| **Modelos de lenguaje (LLM)** | Clasificación de cada texto con un modelo de IA y pocos ejemplos | — | En inglés, GPT-4o con pocos ejemplos rindió casi como FinBERT (un modelo especializado en finanzas). En español, los modelos BETO y MarIA lograron un F1 de 68–76 % en titulares económicos | Un LLM permite clasificar **tema y tono a la vez** y en español, sin entrenar un modelo propio. **Hay que validarlo** porque no encontramos estudios en español chileno |

## Nuestra propuesta

**Enfoque híbrido:** un LLM clasifica cada titular, un diccionario sirve de control, y el resultado se valida contra una clasificación manual y contra el IPEC.

### Paso 1: recolección (cada 30–60 minutos)

| Fuente | Cómo | Notas |
|---|---|---|
| La Tercera / Pulso, BioBio, Cooperativa, CIPER, Ex-Ante | RSS (ver [fuentes-de-datos.md](fuentes-de-datos.md)) | Ya probados |
| El Mercurio (Emol), Diario Financiero | Google News RSS por sitio | **Solo en el prototipo** (los términos no permiten uso comercial). Para producción: acuerdo con los medios o un agregador con licencia |
| Hechos esenciales de la CMF, comunicados del Banco Central | Ver fuentes | Fuentes oficiales: se pueden usar completas |

**Qué guardamos:** titular, bajada (descripción corta), medio, fecha, enlace y un identificador único. **Nunca el texto completo**, aunque el RSS lo traiga.

### Paso 2: limpieza

- **Eliminar duplicados:** el mismo titular publicado dos veces.
- **Agrupar la misma noticia** contada por varios medios, para que una gran noticia no cuente 10 veces.
- **Filtrar solo noticias económicas.** Los RSS generales traen deportes y espectáculos; el mismo LLM decide si es económica.

### Paso 3: clasificación con IA

Para cada titular + bajada, el modelo devuelve un JSON:

```json
{
  "es_economica": true,
  "termometro": "bolsillo",
  "tono": -1,
  "incertidumbre": false,
  "entidades": ["ENAP", "bencina"],
  "motivo": "Anuncia alza en el precio de la bencina"
}
```

- **termometro:** bolsillo, deudas, ahorro_pensiones, actividad_empleo, dolar_mercados u otro.
- **tono:** desde **−2** (muy negativo para la economía de los hogares) hasta **+2** (muy positivo). 0 = neutral.
  - Se mide el tono **para el bolsillo de las personas**, no para "los mercados". Un alza del cobre es buena para Chile; un alza de la bencina es mala para el hogar. Hay que definirlo bien en el prompt, con ejemplos.
- **incertidumbre:** sí o no (estilo EPU: ¿la noticia habla de incertidumbre sobre la política económica?).
- **motivo:** una frase, para revisar errores.
- **Modelo:** uno rápido y económico (por ejemplo, Claude Haiku). Son unos pocos cientos de titulares cortos al día, así que el costo es bajo; hay que calcularlo con los precios vigentes antes de lanzar.
- **Respaldo:** un diccionario simple de palabras positivas y negativas, basado en los trabajos del Banco Central. Sirve para detectar si el LLM se desvía.

### Paso 4: cálculo del termómetro

1. **Tono neto del día** = (titulares positivos − negativos) ÷ total de titulares económicos.
2. **Equilibrar medios:** primero se calcula el tono de cada medio y después se promedia, para que el medio que publica más no domine (como hace la Fed de San Francisco).
3. **Suavizar:** promedio móvil de 7 días, con más peso a los días recientes. Evita que una sola noticia mueva todo.
4. **Estado de presión:** se compara con la historia del propio índice, con la misma regla que el resto de los termómetros:
   - 20 % más negativo de su historia → **"Más negativo que lo habitual"**
   - 20 % más positivo → **"Más positivo que lo habitual"**
   - Resto → **"Normal"**
5. **Por termómetro:** el mismo cálculo filtrado por tema da, por ejemplo, "el ánimo de las noticias sobre tu bolsillo".
6. **Incertidumbre:** porcentaje de noticias con incertidumbre, mostrado aparte.

**Importante:** para saber qué es "lo habitual" se necesita historia. Hay que **empezar a recolectar y clasificar cuanto antes**: al menos 2 o 3 meses antes de mostrar estados. Mientras tanto, solo se muestran los temas del día.

### Paso 5: validación

1. **Clasificación manual:** etiquetar a mano entre 300 y 500 titulares (tono y tema) y medir cuánto coincide el LLM. Es lo que hizo el Banco Central en el DT 938.
2. **Comparación con el diccionario:** si el LLM y el diccionario divergen mucho un día, revisar.
3. **Comparación con el IPEC:** cada mes, revisar si nuestro índice se mueve parecido a la confianza del consumidor. No tiene que ser igual, pero no debería ir en dirección contraria por mucho tiempo.
4. **Revisión periódica de errores** usando el campo `motivo`.

### Paso 6: qué se muestra

- **Estado + tendencia** (como todos los termómetros).
- **Los 3 temas que más pesaron** esta semana, con titulares de ejemplo y **enlace a la nota original**.
- **Cuántos titulares y medios** se analizaron.
- Una advertencia de que **es un indicador propio y automático**, con la metodología publicada.
- En la página de detalle: el tono por medio, para que se vea que el resultado no depende de uno solo.

## Riesgos y cómo manejarlos

| Riesgo | Manejo |
|---|---|
| **Sesgo de los medios** (línea editorial) | Varios medios de distintas líneas y equilibrio entre ellos. Mostrar el tono por medio |
| **Derechos de autor** | Solo titular, bajada y enlace. Nunca el texto completo. El tono es nuestro cálculo, no su contenido |
| **Errores de la IA** | Validación manual, diccionario de control y revisión de `motivo` |
| **Titulares sensacionalistas** | El suavizado de 7 días y la agrupación de noticias repetidas reducen su efecto |
| **Picos por una sola noticia grande** | La agrupación hace que cuente una vez, no por cada medio |
| **Que parezca una predicción** | Decir siempre que mide **el tono de las noticias**, no el futuro de la economía |
| **Pocos medios disponibles** (sin Emol ni DF en producción) | Buscar acuerdos o un agregador con licencia. Mientras tanto, complementar con fuentes oficiales |

## Próximos pasos

1. Armar el recolector de RSS y guardar los titulares desde ya.
2. Escribir el prompt de clasificación con 15–20 ejemplos chilenos.
3. Etiquetar 300 titulares a mano para validar.
4. Revisar el DT 938 del Banco Central para reutilizar su diccionario, si está disponible.
5. Definir el umbral de días de historia antes de mostrar estados.

## Fuentes

- [Fed de San Francisco: Daily News Sentiment Index](https://www.frbsf.org/economic-research/indicators-data/daily-news-sentiment-index/)
- [Fed de San Francisco: Measuring News Sentiment (WP 2017-01)](https://www.frbsf.org/wp-content/uploads/wp2017-01.pdf)
- [Banco Central: DT 938, prensa como indicador de confianza](https://www.bcentral.cl/contenido/-/detalle/documento-de-trabajo-n-938)
- [Banco Central: DT 862, sentimiento en el IPN](https://www.bcentral.cl/contenido/-/detalle/documento-de-trabajo-n-862)
- [Banco Central: DT 930, sentimiento en el Informe de Estabilidad Financiera](https://www.bcentral.cl/contenido/-/detalle/documento-de-trabajo-n-930)
- [Banco Central: DT 883, EPU de Chile basado en Twitter](https://si3.bcentral.cl/estadisticas/Principal1/Metodologias/EMF/Incertidumbre/dtbc883.pdf)
- [Banco de España: EPU para América Latina](https://www.bde.es/wbe/en/areas-actuacion/analisis-e-investigacion/america-latina/contenidos/publicaciones-latinoamerica/indices-de-incertidumbre-de-la-politica-economica--epu--para-los-principales-paises-de-america-latina-y-espana.html)
- [Financial Sentiment Analysis using LLMs and FinBERT (arXiv 2410.01987)](https://arxiv.org/abs/2410.01987v1)
- [Smart Analysis of Economics Sentiment in Spanish (Univ. de Murcia)](https://portalinvestigacion.um.es/documentos/640d5e70f0c92964f843e974)
- [CESifo: Building Daily Economic Sentiment Indicators](https://cesifo.org/en/publications/2022/working-paper/building-daily-economic-sentiment-indicators)
- [Guía de GDELT](https://lobehub.com/mcp/cyanheads-gdelt-mcp-server)
- [Risk.net: RavenPack](https://www.risk.net/awards/7930086/risk-markets-technology-awards-2022-alternative-data-vendor-of-the-year)
