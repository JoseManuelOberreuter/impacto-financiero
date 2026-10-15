# Investigación: diseño de apps económicas y termómetros

> Investigación hecha el 15-oct-2026. Las fuentes están al final. Lo que es opinión o síntesis propia está marcado como tal.

## Resumen: lo que aplicamos

1. **Primero la vista general y después el detalle**, en capas. Es lo que ya definimos en [termometros.md](termometros.md) y lo que hace Our World in Data.
2. **Medir la presión contra lo "normal" de cada indicador**, igual que la Fed de Nueva York con su índice de presión de cadenas de suministro.
3. **Metodología pública.** El índice Fear & Greed de CNN es atractivo, pero su fórmula no está completamente publicada. Nosotros la publicamos.
4. **Comparar el dato oficial con el "tuyo"**, como las calculadoras de inflación personal del BCE y de la ONS del Reino Unido. Es la idea de "sensación térmica".
5. **Separar datos duros de percepción:** mostrar ambos y no mezclarlos en un solo número.
6. **Nada de gamificación sobre decisiones financieras** (lección de Robinhood). Celebrar el aprendizaje, no las transacciones.
7. **Lenguaje simple sin esconder detalles**, organizado según las preguntas del usuario y no según las fuentes (Monzo, Nubank).
8. **Diseñar primero para el celular** (crítica a la app de FRED).

---

## 1. Referentes de datos económicos

| Referente | Qué hace bien | Puntos débiles | Qué tomamos |
|---|---|---|---|
| **FRED** (Fed de St. Louis, EE. UU.) | Miles de series, gráficos que se actualizan solos, API bien documentada, dashboards temáticos con widgets que llevan al detalle | La app móvil parece "una versión de escritorio achicada": texto pequeño y gráficos ilegibles. Pensado para expertos. Solo EE. UU. | Fichas de indicador con serie, fuente y actualización automática (nivel 3). **Diseñar primero para el celular** |
| **Our World in Data** | Estructura "vista general → filtrar → detalle a pedido". Cada idea clave combina un gráfico con una explicación corta. Cada gráfico enlaza a su fuente y se puede incrustar en otros sitios | Temas amplios y lentos; no es una herramienta diaria | Tarjeta = gráfico + una frase. Fuente visible siempre. **Tarjetas para compartir** (WhatsApp, redes) |
| **Trading Economics** *(observación propia; no encontré críticas documentadas)* | Cubre casi todos los países e indicadores, con calendario de publicaciones | Pantallas densas, tablas largas, mucha publicidad; pensado para analistas | Usar su **calendario de publicaciones** como idea para "próxima actualización". Evitar la densidad |
| **Calculadora de inflación personal** (ONS + BBC, Reino Unido) | El usuario ingresa su gasto por categoría y ve **su** inflación comparada con la oficial. Si salta una categoría, usa el promedio de hogares similares. **No guarda datos** | Es una estimación; algunos usuarios dudaron de los resultados | Calculadora "**Tu inflación**": su canasta vs. el IPC. Valores por defecto razonables y nada guardado en el servidor |
| **Calculadora de inflación personal y dashboard** (BCE) | 12 categorías de gasto con subcategorías opcionales. Reparte las compras grandes (un auto) en meses. Usa datos oficiales actualizados. Advierte que es "una estimación informada". Pensado para daltónicos, con textos simples y gráficos incrustables | Requiere que el usuario conozca su gasto | Misma idea, más **advertir siempre que es una estimación**. Accesibilidad de color desde el inicio |

## 2. Apps de finanzas personales

| Referente | Qué hace bien | Puntos débiles | Qué tomamos |
|---|---|---|---|
| **Monzo** (Reino Unido) | Principios de diseño propios para cada proyecto. **"Fricción buena"**: frena a propósito en decisiones de riesgo. Educación gradual dentro del flujo, no tutoriales largos. Reconoce que cada usuario llega con necesidades distintas. Simplifica sin esconder | — | Onboarding corto y **educación en contexto** ("¿qué es la TPM?" justo donde aparece). Personalización según el punto de partida del usuario |
| **Nubank** (Brasil) | Critica las apps que se organizan según las áreas internas de la empresa en vez de según el usuario. Diseña considerando la **ansiedad financiera** | — | Organizar por **preguntas del usuario** (termómetros), no por fuente (Banco Central, CMF…). **Tono calmado**: informar sin alarmar |
| **Robinhood** (EE. UU.) | Simplicidad extrema para invertir | En 2021 tuvo que **quitar el confeti** que mostraba en las primeras operaciones, tras críticas en el Congreso y una demanda en Massachusetts por "gamificar" la inversión | **Nada de confeti, rachas ni premios** ligados a decisiones financieras. Si celebramos algo, que sea aprender o configurar su AFP |

## 3. Termómetros económicos internacionales

| Termómetro | Qué mide | Cómo se presenta | Fortalezas | Debilidades | Lección para nosotros |
|---|---|---|---|---|---|
| **Fear & Greed Index** (CNN) | Ánimo del mercado bursátil de EE. UU. | Medidor de 0 a 100 (miedo extremo ↔ codicia extrema), con 7 componentes (impulso del S&P 500, volatilidad VIX, put/call, bonos basura, etc.) | Muy fácil de entender, visual, se volvió referencia popular | La fórmula exacta **no está totalmente publicada**; los terceros solo la aproximan. Solo mide la bolsa | El medidor visual funciona. Nosotros **publicamos la fórmula** |
| **Global Supply Chain Pressure Index** (Fed de Nueva York) | Presión en las cadenas de suministro globales (27 indicadores) | En **desviaciones estándar respecto del promedio histórico**: 0 = normal; positivo = más presión de lo normal | Usa la palabra **"presión"** y la mide contra lo normal. El récord (dic-2021, 4,3) se entendió como "evento extremo" | Las desviaciones estándar no son intuitivas para el público | Validación de nuestro enfoque: **presión = distancia a lo normal**. Traducirlo a baja/media/alta, no a números técnicos |
| **Índice de Miseria** (Okun) | Inflación + desempleo | Un solo número | Simplísimo; en Chile lo calcula Clapes UC (11,4 % en el 1T-2026, segundo más alto de la región según ese centro) | Suma dos cosas distintas; ignora salarios y crecimiento | Bueno como **dato de contexto** en el termómetro de Actividad. No usarlo como termómetro principal |
| **Economy Watchers Survey** (Japón) | Percepción de la economía "desde la calle" | Unas 2.000 personas que ven la economía de cerca (taxistas, cajeros, garzones, agentes de empleo) responden en 5 niveles. Índice donde 50 = neutral | Detecta cambios antes que los datos oficiales; según un análisis de 2009, anticipó todos los puntos de quiebre del ciclo desde el año 2000 | Requiere un panel grande y constante | **Idea a futuro:** un "termómetro de la calle" chileno con una encuesta breve a usuarios o a almaceneros, feriantes, conductores |
| **GDPNow** (Fed de Atlanta) | Estimación en tiempo real ("nowcast") del PIB del trimestre | Un número que se actualiza 6–7 veces al mes según llegan datos | Da una lectura temprana; sin ajustes subjetivos | La misma Fed aclara que **no es un pronóstico oficial** y que es poco precisa al inicio del trimestre | Si hacemos estimaciones, **rotularlas como estimación** y mostrar su margen de error |
| **Leading Economic Index** (Conference Board) | Ciclo económico de EE. UU. | Índice compuesto de 10 componentes, con versiones **adelantada, coincidente y rezagada** | Anticipa los cambios de ciclo en unos 7 meses | Para expertos; muchas fuentes | Idea: distinguir datos que **anticipan** (expectativas, permisos de edificación) de los que **confirman** (IPC, desempleo) |
| **Daily News Sentiment Index** (Fed de San Francisco) | Tono de las noticias económicas | Índice diario a partir de 24 diarios de EE. UU. | Alta correlación con las encuestas de confianza del consumidor; diario en vez de mensual | Solo prensa en inglés | Base del termómetro **Ánimo** (ver [sentimiento-noticias.md](sentimiento-noticias.md)) |
| **Economic Policy Uncertainty** (Baker, Bloom y Davis) | Incertidumbre de política económica | Cuenta artículos que mencionan a la vez economía, política e incertidumbre | Método simple y replicable; existe para Chile | Mide incertidumbre, no si las noticias son buenas o malas | Agregar un **indicador de incertidumbre** al termómetro Ánimo |

## 4. Termómetros económicos en Chile

| Termómetro | Quién lo hace | Qué mide | Frecuencia | ¿Lo usamos? |
|---|---|---|---|---|
| **IPEC** (Índice de Percepción de la Economía) | GfK Chile (NIQ) | Confianza del consumidor: 5 preguntas sobre su situación y la del país, unas 1.100 personas. Escala de 0 a 100, donde 50 = neutral | Mensual | **Sí**, como dato de percepción en Bolsillo y Ánimo. La serie aparece en la BDE del Banco Central (confirmar el código) |
| **IMCE** (Índice Mensual de Confianza Empresarial) | ICARE / Universidad Adolfo Ibáñez *(no verificado en esta búsqueda)* | Confianza de las empresas | Mensual | Evaluar para el plan Pymes |
| **Encuesta de Expectativas Económicas (EEE)** | Banco Central | Lo que esperan los expertos para el IPC, el PIB y la TPM | Mensual | **Sí**: "lo que esperan los expertos" en Deudas (TPM) y Bolsillo (IPC) |
| **Informe de Percepciones de Negocios (IPN)** | Banco Central | Percepción de las empresas, con entrevistas y encuesta | Trimestral | Contexto para Pymes |
| **Índice de Miseria** | Clapes UC | Inflación + desempleo | Trimestral | Contexto en Actividad y empleo |
| **EPU Chile** (incertidumbre) | Cerda et al.; Banco de España (América Latina); Banco Central (versión diaria con Twitter, DT 883) | Incertidumbre de política económica en la prensa | Mensual / diaria | Referencia para el componente de incertidumbre de Ánimo |
| **Confianza basada en prensa** | Banco Central (DT 938, 2022) | Tono de las noticias económicas de los principales medios chilenos (2015–2020), con un diccionario en español | Alta frecuencia (estudio, no se publica de forma continua) | **Referencia metodológica directa** para nuestro termómetro Ánimo |

**Hallazgo clave:** en Chile **no existe un termómetro público, diario y fácil de entender** que combine datos duros, percepción y noticias. Existen las piezas por separado, la mayoría pensadas para expertos. Ese es el espacio que ocupa Impacto Financiero.

## 5. Patrones de diseño a aplicar

**Escala y lectura**
- Usar siempre la **misma lógica de lectura**: presión baja / media / alta respecto de lo normal del propio indicador. Esto es lo que ya decidimos.
- Mostrar **dónde está lo "normal"**: una banda sombreada en los gráficos con el rango habitual de los últimos 5 años.
- Indicar **la tendencia** (▲ ▼ ●) además del estado.

**Confianza**
- **Metodología pública** de cada termómetro e índice propio.
- **Fuente y fecha visibles** en cada tarjeta.
- **Rotular las estimaciones** como estimaciones (lección de GDPNow y del BCE).

**Personal vs. oficial ("sensación térmica")**
- Mostrar el dato oficial y, al lado, **cómo te afecta a ti**: el IPC junto a "tu inflación" según tu canasta, o la UF junto a "tu dividendo".
- Es la idea de las calculadoras de la ONS y del BCE, llevada a la portada.

**Datos vs. percepción**
- Cada termómetro puede tener dos lecturas: **lo que dicen los datos** (canasta, IPC) y **lo que siente la gente** (IPEC, tono de las noticias). Se muestran por separado.
- Cuando no coinciden ("los precios se estabilizaron, pero la gente sigue pesimista"), eso es **una historia interesante para el resumen del día**.

**Tono y comportamiento**
- Lenguaje calmado y sin alarmismo, pensando en la ansiedad financiera (Nubank).
- **Educación en contexto**: un "¿qué es esto?" junto a cada término técnico (Monzo).
- **Cero gamificación** ligada a decisiones financieras (Robinhood).

**Formato**
- **Primero el celular**: texto legible y un número por tarjeta (crítica a la app de FRED).
- **Tarjetas para compartir** en WhatsApp y redes, con fuente y fecha incluidas (Our World in Data permite incrustar sus gráficos).
- **Accesibilidad**: colores aptos para daltónicos; el estado no depende solo del color, también va escrito (BCE).

## 6. Ideas para más adelante

- **"Termómetro de la calle":** encuesta breve y periódica a usuarios o a un panel de almaceneros, feriantes y conductores, al estilo del Economy Watchers de Japón.
- **Datos que anticipan vs. datos que confirman**, como el LEI de la Conference Board.
- **Calculadora "Tu inflación"** completa, con categorías de gasto (BCE y ONS).
- **Comparación entre regiones** del costo de vida (índice de canasta por región).

## Fuentes

- [ONS: How is inflation affecting your household costs?](https://www.ons.gov.uk/economy/inflationandpriceindices/articles/howisinflationaffectingyourhouseholdcosts/latest)
- [BCE: How does the personal inflation calculator work?](https://www.euro-area-statistics.org/inflation-calculator/?lang=en)
- [BCE: Statistics Insights: Inflation](https://euro-area-statistics.org/digital-publication/statistics-insights-inflation/?lang=en)
- [Our World in Data: rediseño de páginas temáticas](https://ourworldindata.org/owid-entry-redesign)
- [Reseñas de la app de FRED](https://splitmetrics.com/apps/fred-economic-data/id451715489)
- [Monzo: What's so unique about design and research at Monzo?](https://monzo.com/blog/2022/12/28/whats-so-unique-about-design-and-research-at-monzo)
- [Monzo: How we design magic moments](https://monzo.com/blog/2022/11/04/how-we-design-magic-moments-at-monzo)
- [Nubank: Building the new mobile app header](https://building.nubank.com/es/building-the-new-mobile-app-header/)
- [CNBC: Robinhood gets rid of confetti feature](https://www.cnbc.com/2021/03/31/robinhood-gets-rid-of-confetti-feature-amid-scrutiny-over-gamification.html)
- [Fear & Greed Index: componentes (Hypercall)](https://docs.hypercall.xyz/docs/reference/fear-and-greed)
- [Fed de Nueva York: GSCPI (Liberty Street Economics)](https://libertystreeteconomics.newyorkfed.org/2022/05/global-supply-chain-pressure-index-may-2022-update)
- [Gobierno de Japón: Economy Watchers Survey](https://www5.cao.go.jp/keizai3/watcher-e/index-e.html)
- [NLI Research: análisis del Economy Watchers Survey](https://www.nli-research.co.jp/files/topics/51183_ext_18_en_0.pdf?site=nli)
- [Fed de Atlanta: GDPNow](https://www.atlantafed.org/research-and-data/data/gdpnow/explainer)
- [Conference Board LEI, julio 2026](https://fedprimerate.com/docs/Conference-Board/Fed-Prime-Rate-Conference-Board----LEADING--ECONOMIC--INDEX---JULY---2026.pdf)
- [NIQ: Índice de Percepción de la Economía GfK Chile](https://nielseniq.com/global/es-latam/news-center/2024/indice-percepcion-de-la-economia-gfk-chile/)
- [DF: Índice de miseria de Chile](https://www.df.cl/economia-y-politica/macro/indice-de-miseria-de-chile-cae-por-sexto-mes-gracias-a-control-de-la)
- [Banco Central: Percepciones de Negocios](https://www.bcentral.cl/-/percepciones-de-negocios-medir-las-expectativas-con-un-instrumento-flexible)
- [Chocale: Encuesta de Expectativas Económicas, agosto 2026](https://chocale.cl/2026/08/economia-creceria-un-13-e-inflacion-al-4-la-foto-que-deja-la-ultima-encuesta-del-banco-central-para-2026/)
- [Banco de España: EPU para América Latina](https://www.bde.es/wbe/en/areas-actuacion/analisis-e-investigacion/america-latina/contenidos/publicaciones-latinoamerica/indices-de-incertidumbre-de-la-politica-economica--epu--para-los-principales-paises-de-america-latina-y-espana.html)
- [Banco Central: DT 883, EPU de Chile basado en Twitter](https://si3.bcentral.cl/estadisticas/Principal1/Metodologias/EMF/Incertidumbre/dtbc883.pdf)
- [Banco Central: DT 938, prensa como indicador de confianza](https://www.bcentral.cl/contenido/-/detalle/documento-de-trabajo-n-938)
