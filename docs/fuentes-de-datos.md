# Fuentes de datos

> Revisado el 15-oct-2026. Las rutas y condiciones pueden cambiar: confirmar en el sitio oficial antes de integrar.

## Resumen

| Fuente | ¿API oficial? | Cómo la obtenemos | Etapa | Estado |
|---|---|---|---|---|
| Banco Central (BDE) | Sí (REST/SOAP) | API con token | 1 | 🟢 Verificado |
| CMF: indicadores | Sí (REST) | API con `apikey` | 1 | 🟢 Verificado |
| CMF: hechos esenciales | No | Consulta web + suscripción por correo | 1 | 🟡 Por probar |
| Superintendencia de Pensiones (AFP) | No | Descarga CSV directa | 1 | 🟢 Verificado (probado) |
| INE | No | Series vía BDE; INE.Stat y Excel como respaldo | 2 | 🟡 Por probar |
| SII | No | Páginas HTML públicas por año | 2–3 | 🟢 Páginas responden |
| DIPRES | Sí (CKAN de datos.gob.cl) | API de datos.gob.cl + CSV | 2–3 | 🟡 Por probar |
| Bolsa (nuam) | Sí, pero cerrada o de pago | Licencia o proveedor autorizado | 2 | 🔴 Sin acceso hoy |
| Prensa | No | RSS: solo titular, bajada y enlace | 1 | 🟡 Parcial |
| ODEPA (alimentos) | Sí (CKAN) | CSV anual, actualizado semanalmente | 1 | 🟢 Verificado (probado) |
| CNE (bencina y gas) | Sí (REST) | API con token Bearer | 1 | 🟡 Por probar |
| Transporte público | No | Resolución del Panel de Expertos, carga manual | 1 | 🟢 Manual |

---

## 1. Banco Central de Chile: BDE

**Es la fuente principal.** Trae UF, dólar observado, IPC, TPM, IMACEC, tasas y cuentas nacionales. También replica muchas series del INE (IPC, desempleo), que hay que confirmar con `SearchSeries`.

- **REST (JSON):** `https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx`
- **Funciones:**
  - `SearchSeries`: lista las series por frecuencia (`DAILY`, `MONTHLY`, `QUARTERLY`, `ANNUAL`).
  - `GetSeries`: entrega las observaciones de una serie. Parámetros: `timeseries`, más `firstdate` y `lastdate` opcionales (`YYYY-MM-DD`).
- **Autenticación:** parámetro `token` (API Key). Se obtiene registrándose en la BDE y activando las credenciales de API.
- **Ejemplo:** `...SieteRestWS.ashx?token=TOKEN&function=GetSeries&timeseries=F073.TCO.PRE.Z.D&firstdate=2026-01-01`. En este ejemplo de la documentación, `F073.TCO.PRE.Z.D` es el dólar observado.
- **Respuesta:** `Codigo` (0 = OK), `Series.Obs[]` con `indexDateString`, `value` y `statusCode`.
- **Límites:** la documentación no indica límites. Igual conviene consultar una vez al día y guardar en caché.
- **Librería:** `bcchapi` (Python).
- **Condiciones:** se puede reproducir la información citando al Banco Central como dueño de los datos.

**Catálogo de códigos:** hecho y verificado con el token el 15-oct-2026, en [banco-central-series.md](banco-central-series.md). Son unas 25.500 series; ahí están las que usamos por termómetro.

## 2. CMF: API de indicadores

- **Base:** `https://api.cmfchile.cl/api-sbifv3/recursos_api/`
- **Recursos:** `dolar`, `euro`, `uf`, `utm`, `ipc`, `tmc`, `tip`, `tab`, además de reportes bancarios (balances, resultados, adecuación de capital).
- **Patrones de URL** (ejemplo con UF):
  - Valor del día: `.../uf?apikey=KEY&formato=json`
  - Por año, mes o día: `.../uf/2026`, `.../uf/2026/10`, `.../uf/2026/10/dias/15`
  - Rangos: `.../uf/periodo/2026/01/2026/10`, `.../posteriores/...`, `.../anteriores/...`
- **Formato:** XML por defecto; JSON con `formato=json`.
- **Autenticación:** parámetro `apikey`, que se solicita en el portal de la API.
- **Uso:** respaldo del Banco Central para UF, dólar y UTM, y **fuente principal de TMC (tasa máxima convencional) y datos de bancos**.

## 3. CMF: hechos esenciales

No tiene API. Hay una consulta web (`cmfchile.cl/institucional/hechos/hechos.php`, por mercado: `V` valores, `S` seguros, `O` otros) cuyo formulario envía a `hechos2.php` con campos de fecha (`p_fecha_desde`, `p_fecha_hasta`), entidad y materia.

**Propuesta:**
1. **Preferida:** suscribirse a las alertas por correo de la CMF ("suscripción de interés") y procesar esos correos automáticamente.
2. Consultar el formulario una vez al día con el rango de fechas, si el sitio lo permite sin captcha. **Si aparece un captcha, no se evade:** se pide acceso a la CMF.
3. A mediano plazo, escribir a la CMF para pedir un feed o API de hechos esenciales.

**Valor:** son noticias oficiales y públicas, y se pueden mostrar y resumir sin problemas de derechos de autor.

## 4. Superintendencia de Pensiones: valor cuota AFP

No tiene API, pero la descarga CSV es directa y estable. **La probamos y funciona.**

- **URL:** `https://www.spensiones.cl/apps/valoresCuotaFondo/vcfAFPxls.php?aaaaini=2026&aaaafin=2026&tf=A&fecconf=20260930`
  - `tf`: fondo `A`–`E`
  - `aaaaini` / `aaaafin`: rango de años
  - `fecconf`: fecha hasta la que los valores están confirmados (aparece en la página `vcfAFP.php?tf=A`)
- **Formato:** CSV separado por `;`, con decimales con coma y miles con punto. Columnas: fecha, y luego valor cuota y patrimonio por AFP (Capital, Cuprum, Habitat, Modelo, PlanVital, ProVida, Uno).
- **Ojo:**
  - Los valores recientes son **provisionales** ("sujeto a confirmación"); se confirman después, así que hay que reprocesar.
  - El archivo incluye fines de semana con el valor repetido.
  - Cuando entre una AFP nueva (por ejemplo, tras la licitación), cambian las columnas.
- **Frecuencia:** una descarga diaria del año en curso por fondo (5 archivos).
- **Pendiente:** buscar también rentabilidad oficial y comisiones (sección de estadísticas de spensiones.cl).

## 5. INE

No encontramos una API REST documentada.

**Propuesta, en orden:**
1. **Usar la BDE del Banco Central** para las series del INE que replica (IPC, desocupación, remuneraciones). Una sola integración en vez de dos.
2. **INE.Stat** (`stat.ine.cl`): está montado sobre la plataforma .Stat, que suele permitir exportar datos. Hay que probar si expone exportación SDMX o CSV automatizable.
3. Descargar los Excel de cada publicación desde ine.gob.cl, como último recurso.

## 6. SII

No tiene API. Publica páginas HTML por año con URLs estables:
- UTM, UTA e IPC: `https://www.sii.cl/valores_y_fechas/utm/utm2026.htm`
- Tabla del impuesto único de segunda categoría: `https://www.sii.cl/valores_y_fechas/impuesto_2da_categoria/impuesto2026.htm`
- Además: circulares mensuales en PDF y estadísticas de recaudación.

**Propuesta:** leer estas páginas una vez al mes. Son pocos datos y cambian poco. La UTM también viene en la API de la CMF, que conviene usar como fuente principal y dejar el SII como validación.

**Nunca:** datos personales del contribuyente (Clave Tributaria, carpeta tributaria).

## 7. DIPRES

- Publica en **datos.gob.cl**, que usa CKAN y tiene API pública sin clave: `https://datos.gob.cl/api/3/action/package_search?q=dipres`. Encontramos 209 conjuntos de ejecución presupuestaria, en CSV.
- Según DIPRES, se actualiza con un mes de desfase.
- **Ojo:** los primeros resultados de la búsqueda eran de 2022, así que hay que confirmar si datos.gob.cl está al día. Si no, usar la sección de Estadísticas Fiscales de dipres.gob.cl.
- **Uso:** ingresos tributarios y gasto del Gobierno Central (etapa 2–3).

## 8. Bolsa de Santiago (nuam)

**Es el caso más difícil.**
- Existía una API de la Bolsa con API key y cuota diaria (`startup.bolsadesantiago.com`), con índices, resumen por acción, puntas y transacciones. **Hoy el portal no responde**, probablemente por la migración tecnológica de nuam (nueva plataforma en Chile en 2026 e integración completa en 2027).
- El dato en tiempo real se distribuye por FIX y a través de proveedores licenciados (LSEG, ICE, Deutsche Börse). Lo normal es un retraso de unos 20 minutos.
- **El IPSA es un índice S&P/CLX con licencia propia**, distinta de la de los precios.
- En julio de 2026 hubo errores de datos en sitios de terceros por una falla de un proveedor. Solo hay que confiar en datos oficiales o licenciados.

**Propuesta:**
1. **Etapa 1:** no mostrar precios de acciones. Enfocarse en indicadores, AFP y hechos esenciales. Como mucho, enlazar al sitio de la Bolsa.
2. Escribir a nuam (área de datos de mercado) para preguntar por un acceso para startups, por datos de cierre o con retraso, y por su precio.
3. **Alternativa:** contratar un proveedor que ya tenga licencia de redistribución del mercado chileno.
4. **Evitar** el scraping de sitios de la bolsa o de terceros (Yahoo Finance y similares): es un riesgo legal y de calidad.

## 9. Prensa

**Regla general:** solo **titular, bajada (descripción corta), medio, fecha y enlace**. Nunca guardar ni mostrar el texto completo, aunque el RSS lo traiga. La clasificación por tema y tono la hacemos nosotros.

| Medio | RSS | Notas |
|---|---|---|
| La Tercera / Pulso | ✅ `latercera.com/arc/outboundfeeds/rss/?outputType=xml` y `.../rss/category/pulso/?outputType=xml` | El RSS trae el texto completo (`content:encoded`): **descartarlo** y quedarse con título, descripción y enlace |
| BioBioChile | ✅ `feeds.feedburner.com/radiobiobio/NNeJ` | General; hay que filtrar economía |
| Cooperativa | ✅ `cooperativa.cl/noticias/site/tax/port/all/rss_3___1.xml` | General |
| CIPER | ✅ `ciperchile.cl/feed/` | Investigación, poco volumen |
| Ex-Ante | ✅ `ex-ante.cl/feed/` | Política y economía |
| El Mercurio / Emol | ❌ Sin RSS público | Su `robots.txt` **bloquea explícitamente bots de IA** (GPTBot, Google-Extended, etc.). No hacer scraping |
| Diario Financiero | ❌ Sin RSS encontrado | Muro de pago |
| El Mostrador, 24 Horas | ❌ No encontrado | Revisar más adelante |

**Propuesta para Emol y DF:**
1. **Google News RSS por sitio o tema** (por ejemplo, `news.google.com/rss/search?q=site:df.cl&hl=es-419&gl=CL&ceid=CL:es-419`). Funciona, pero sus términos apuntan a uso personal y no comercial, así que **sirve para el prototipo, no para el producto pagado**.
2. **A mediano plazo:** pedir un acuerdo de uso de titulares a El Mercurio y DF, o contratar un agregador de noticias con licencia.
3. Mientras tanto, apoyarse en fuentes primarias que sí podemos usar completas: hechos esenciales de la CMF, comunicados del Banco Central (IPoM, actas de la reunión de política monetaria) e informes del INE.

## 10. Economía cotidiana: precios de la canasta

Precios de productos y servicios del día a día, para mostrar "cuánto cuesta vivir" y cómo cambia semana a semana.

| Producto | Fuente | Acceso | Frecuencia | Estado |
|---|---|---|---|---|
| Marraqueta / hallulla (kilo) | ODEPA | CSV datos abiertos | Semanal | 🟢 Probado |
| Leche entera (litro) | ODEPA | CSV datos abiertos | Semanal | 🟢 Probado |
| Huevos (bandeja de 30) | ODEPA | CSV datos abiertos | Semanal | 🟢 Probado |
| Aceite vegetal (botella de 900 ml) | ODEPA | CSV datos abiertos | Semanal | 🟢 Probado |
| Carne de vacuno (posta) y pollo entero (kilo) | ODEPA | CSV datos abiertos | Semanal | 🟢 Probado |
| Bencina 93/95/97 y diésel (litro) | CNE: Bencina en Línea | API con token | Diaria o más | 🟡 Por probar |
| Gas licuado (cilindro de 15 kg) | CNE: Gas en Línea | API con token | Diaria o más | 🟡 Por probar |
| Pasaje de Metro y buses RED | Panel de Expertos del Transporte Público | Resolución en el Diario Oficial | Cuando cambia | 🟢 Manual |
| UF / UTM | Banco Central / CMF | API (ver secciones 1 y 2) | Diaria / mensual | 🟢 Verificado |

### ODEPA: precios al consumidor

- **Datos abiertos (CKAN):** `https://datos.odepa.gob.cl/api/3/action/package_search?q=consumidor` → conjunto "Precios al Consumidor", con un CSV por año:
  `https://datos.odepa.gob.cl/dataset/d4646b7f-0d2e-4567-b6fa-932b1a6bb3f3/resource/9f885df4-afeb-4b75-8bab-9334f79db00f/download/precio_consumidor_2026.csv`
- **Columnas:** año, mes, semana, fecha de inicio y término, región, sector (Centro, Norte, Oriente…), tipo de punto (supermercado, supermercado en línea, feria libre, panadería, carnicería), grupo, producto, unidad, y precio mínimo, máximo y promedio. Decimales con coma.
- **Cobertura:** 347 productos y varias regiones (Arica, Coquimbo, Valparaíso, RM, Maule, Ñuble, Biobío, Araucanía, Los Lagos). Se publica los viernes.
- **Tamaño:** unos 45 MB por año. Conviene bajarlo una vez por semana y quedarse solo con los productos de la canasta.
- **Ojo:**
  - Los nombres de producto y de unidad no están normalizados ("Aceite vegetal" viene en botella de 900 ml, no por litro). Hay que armar un catálogo propio de equivalencias.
  - Al buscar la URL del recurso conviene usar la API de CKAN, porque cambia cada año.

**Prueba con la semana que terminó el 9-oct-2026 (RM, rango entre sectores):**

| Producto | Unidad | Supermercado | Panadería / feria / carnicería |
|---|---|---|---|
| Marraqueta | kilo | $2.060 – $2.160 | $2.250 – $2.470 |
| Hallulla corriente | kilo | $2.090 – $2.125 | $2.290 – $2.550 |
| Leche fluida entera | caja 1 L | $1.160 – $1.180 | — |
| Huevo blanco grande | bandeja 30 | — | $5.840 – $6.800 (feria) |
| Aceite vegetal | botella 900 ml | $2.180 – $2.380 | — |
| Posta rosada | kilo | $11.270 – $12.330 | $12.230 – $13.290 |
| Pollo entero | kilo | $3.590 – $3.660 | $3.800 – $4.260 |

Los rangos de referencia que teníamos calzan bien con los datos reales. Conviene separar **vacuno** y **pollo**, porque mezclados dan un rango demasiado amplio ($3.600 – $13.300).

### CNE: bencina y gas licuado

- **Portal:** `https://api.cne.cl`. El registro es gratuito en `/register`. La documentación está en `https://apidocs.cne.cl` y el soporte en `soporteapi@cne.cl`.
- **Autenticación:** token tipo `Authorization: Bearer <token>`.
- **Endpoints encontrados en la documentación:**
  - Bencina: `GET /api/v4/estaciones` (estaciones de servicio con precios), `/api/v4/combustible/vehicular/tiposcombustibles`, `/api/v4/combustible/vehicular/distribuidores`.
  - Gas licuado ("calefacción"): `/api/v3/combustible/calefaccion/puntosdeventa`, `/marcas`, `/tamanos`, `/tipos`, `/callcenters`.
- **Uso:** calcular el precio **promedio, mínimo y máximo por región o comuna** de la bencina de 95 y del cilindro de 15 kg. La CNE declara públicos los precios de las estaciones (Rex CNE 492/2023).
- **Pendiente:** registrarse, probar los endpoints y confirmar los campos de precio y los límites de uso.

### Transporte público (RM)

- La tarifa la fija el **Panel de Expertos del Transporte Público** por resolución publicada en el Diario Oficial (la última, vigente desde el 22-feb-2026).
  - Metro y Tren Nos: punta $895, valle $815, baja $735.
  - Buses RED: $795 todo el día.
- **Propuesta:** carga manual cuando se publique una resolución nueva, con una alerta: buscar "Panel de Expertos" en el Diario Oficial o en los hechos de la prensa. Cambia una o dos veces al año.
- **Regiones:** queda para más adelante, porque cada ciudad tiene su propia tarifa.

### Índice propio de canasta

Con estos datos calculamos el **Índice Impacto de la Canasta**, un indicador semanal propio (no oficial). La metodología está en [indice-canasta.md](indice-canasta.md).

## Frecuencia y desfase de los datos

Hay dos tipos de desfase:
- **Natural:** el dato mide un período que ya terminó; por ejemplo, el IPC de septiembre sale en octubre. No es una falla.
- **De actualización:** el dato debería estar al día, pero quien lo informa se atrasa (por ejemplo, estaciones de servicio en la CNE).

### Ranking: de los que menos se actualizan a los que más

| # | Dato | Fuente | Frecuencia | Desfase típico | Tipo | Verificado |
|---|---|---|---|---|---|---|
| 1 | Tarifa de transporte público | Panel de Expertos | 1–2 veces al año | — | — | Sí (feb-2026) |
| 2 | Tabla del impuesto único | SII | Mensual (cambia con la UTM) | Se conoce por adelantado | — | No |
| 3 | TPM | Banco Central | ~8 reuniones al año | — | — | No |
| 4 | Ejecución fiscal | DIPRES | Mensual | ~1 mes | Natural | No |
| 5 | IMACEC | Banco Central | Mensual | ~1 mes después del mes medido | Natural | No |
| 6 | Desempleo | INE | Mensual (trimestre móvil) | ~1 mes | Natural | No |
| 7 | IPC | INE | Mensual | Se publica ~el 8 del mes siguiente | Natural | No |
| 8 | UTM | SII / CMF | Mensual | Se conoce antes de que empiece el mes | — | No |
| 9 | Precios de alimentos | ODEPA | Semanal (viernes) | Hasta 7 días | Natural | Sí (última semana al 9-oct) |
| 10 | Valor cuota AFP | Superintendencia de Pensiones | Diaria | 1–2 días provisional; ~2 semanas confirmado | Natural + revisión | Sí (el 15-oct: disponible al 13-oct, confirmado al 30-sep) |
| 11 | Dólar observado | Banco Central | Diaria (días hábiles) | Usa las operaciones del día hábil anterior | Natural | No |
| 12 | UF | Banco Central / CMF | Diaria | Se conoce por adelantado (cada 9, hasta el 9 del mes siguiente) | — | No |
| 13 | Bencina y gas | CNE | Continua | Depende de que cada estación o distribuidor informe | **Actualización** | No |
| 14 | Precios de la Bolsa | nuam | Continua | 15–20 min (diferido) o al cierre | Licencia | No |
| 15 | Hechos esenciales | CMF | Continua | Casi inmediato | — | No |
| 16 | Titulares de prensa | RSS | Continua | Minutos | — | Sí (feeds activos) |

"Verificado = No" significa que viene de cómo publica normalmente cada institución. Hay que confirmarlo con los calendarios oficiales de publicación del Banco Central y del INE.

### Los más lentos (cuidado al mostrarlos)

Son los datos mensuales con desfase natural: **DIPRES, IMACEC, desempleo e IPC**. Siempre mostrarán el mes anterior, o el antepenúltimo en el caso del IMACEC.

### Reglas para la app

- Cada dato se muestra con **su período y fecha de publicación**: "IPC de septiembre (publicado el 8-oct)".
- Mostrar la **próxima actualización** tomada de los calendarios oficiales: "El próximo IPC sale el 8-nov".
- **Marcar los datos provisionales**, como el valor cuota de las AFP de los últimos días.
- **No cruzar períodos distintos** como si fueran del mismo momento.
- **CNE:** usar solo estaciones actualizadas en los últimos X días y mostrar "promedio de N estaciones".
- Programar cada ingestor según su frecuencia real, no consultar todo a cada rato.

## Respaldo no oficial

- **mindicador.cl:** API gratuita y no oficial de indicadores (UF, dólar, UTM, IPC). Sirve solo como respaldo o para validar cruces, nunca como fuente principal.

## Contexto legal relacionado

- **Ley 21.719 (datos personales):** la fecha legal de entrada en vigencia sigue siendo el **1-dic-2026**. Hay un proyecto (boletín 18.623-07) que la posterga a 2027; a oct-2026 no estaba aprobado.
- **Finanzas Abiertas:** postergadas a julio de 2027 (NCG 569).

## Próximas acciones

1. Pedir el token del Banco Central, la `apikey` de la CMF y el token de la CNE.
2. Armar el catálogo de series del Banco Central.
3. Escribir un script de prueba que baje Banco Central, CMF y AFP y lo guarde.
4. Suscribirse a las alertas de hechos esenciales de la CMF.
5. Escribir a nuam por datos de mercado.
6. Probar el filtrado y la clasificación de titulares desde los RSS disponibles.
