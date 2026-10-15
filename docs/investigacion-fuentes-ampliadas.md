# Investigación: más fuentes de datos e indicadores derivados

> Investigación hecha el 15-oct-2026. Complementa [fuentes-de-datos.md](fuentes-de-datos.md). Las fuentes citadas están al final.
> **Regla:** un dato que afecta a la economía chilena pero que no podemos obtener de forma legal y repetible no nos sirve. Por eso cada fuente indica cómo se obtiene.

## Resumen

- **Ya teníamos cubiertas las fuentes principales:** Banco Central, CMF, AFP, ODEPA, CNE, INE, SII, DIPRES y prensa.
- **Encontramos 12 fuentes chilenas más y 6 internacionales** que se pueden obtener. Las más valiosas:
  - **Coordinador Eléctrico Nacional:** costo marginal de la electricidad. Tiene API con credenciales.
  - **ENAP / CNE:** precio de paridad semanal de los combustibles. Permite **anticipar** si la bencina va a subir o bajar.
  - **Seguro de cesantía** y **constitución de empresas:** son indicadores **adelantados** del empleo y la actividad.
  - **Banco Central:** expectativas de expertos, índice de precios de vivienda y el indicador experimental de compraventas por facturación electrónica.
  - **FRED** (Fed de St. Louis) y **EIA** (petróleo): lo que pasa afuera y mueve a Chile. Ambas tienen API gratuita con clave.
- **El Banco Central ya trae muchas series internacionales** (cobre, petróleo, tasas de EE. UU.). Conviene revisar su catálogo antes de agregar más integraciones.
- **Podemos generar 16 datos propios cruzando fuentes.** Algunos ejemplos:
  - cuántas horas de sueldo mínimo cuesta la canasta;
  - el costo de llenar el estanque;
  - el aviso de "la bencina debería subir la próxima semana";
  - la tasa real;
  - la rentabilidad real de las AFP.

## 1. Nuevas fuentes chilenas

| Fuente | Qué aporta | Por qué importa | Cómo se obtiene | Verificado |
|---|---|---|---|---|
| **Coordinador Eléctrico Nacional** | Costo marginal de la electricidad (por barra, horario) | Anticipa presiones en tarifas eléctricas y costos de la industria | API `sipub.api.coordinador.cl`, con credenciales | Sí: el endpoint existe y pide autenticación |
| **ENAP / CNE: precios de paridad (MEPCO)** | Precio de paridad de importación de los combustibles, cada semana | Permite anticipar el alza o baja de la bencina **antes** de que llegue al surtidor | Informe semanal (jueves) en PDF/web; la CNE fija los precios de referencia | Parcial: confirmado el informe semanal; falta la URL vigente |
| **Seguro de cesantía (Superintendencia de Pensiones)** | Solicitudes aprobadas, beneficiarios y montos | Indicador **adelantado** del desempleo: sube antes que la tasa del INE | Series estadísticas en spensiones.cl (preliminares, con rezago) | Parcial: confirmado el informe mensual y la serie |
| **Registro de Empresas y Sociedades (Ministerio de Economía)** | Empresas constituidas por mes, por tipo de sociedad | Termómetro del emprendimiento y de la confianza empresarial | Informe mensual en PDF (por ejemplo, 16.090 empresas en jul-2024) | Sí: los informes existen; no hay datos tabulares |
| **Servicio Nacional de Aduanas** | Exportaciones e importaciones mensuales | Mide el sector externo (cobre, fruta, importación de bienes) | Datos abiertos en aduana.cl y datos.gob.cl | Parcial: la información es de 2016; hay que revisar el portal actual |
| **Mercado Público (ChileCompra)** | Licitaciones y órdenes de compra del Estado | Gasto público real, día a día, por región y rubro | API oficial con "ticket" (se pide con Clave Única) | Sí: la API y el ticket están documentados |
| **Banco Central: Encuesta de Expectativas Económicas (EEE)** | Lo que esperan los expertos para IPC, PIB y TPM | Permite mostrar "lo que viene" según los expertos | Series en la BDE (hay que confirmar los códigos) | Parcial |
| **Banco Central: Índice de Precios de Vivienda (IPV)** | Precio de las viviendas, nuevas y usadas, por zona (19 series desde 2002) | Vivienda: el gran tema de las familias | BDE, trimestral, con unos 120 días de desfase | Sí |
| **Banco Central: Indicador de Compraventas Regional (ICVR)** | Compraventas a partir de la facturación electrónica | Actividad casi en tiempo real por región; es estadística experimental | Web del Banco Central | Parcial: existe la nota técnica |
| **Cochilco** | Precio del cobre (LME), inventarios, litio | El cobre es la principal exportación de Chile | Informe diario "La Rueda" en la web. **El Banco Central también publica el precio del cobre en la BDE**, que es más fácil de integrar | Parcial |
| **ANAC** | Venta de autos nuevos | Consumo de bienes durables: es de lo primero que cae en una crisis | Informe mensual en PDF y prensa; no tiene API | Sí: los informes existen |
| **SII: boletas electrónicas** | Emisores y montos de boletas | Consumo y actividad de las pymes | Página de estadísticas del SII; no tiene API (la fuente cambió en 2022) | Parcial |

## 2. Fuentes internacionales que afectan a Chile

| Fuente | Qué aporta | Por qué importa para Chile | Cómo se obtiene | Verificado |
|---|---|---|---|---|
| **FRED (Fed de St. Louis)** | Tasa de la Fed, bonos de EE. UU., inflación de EE. UU., S&P 500, VIX | Las tasas de EE. UU. mueven el dólar y el costo del crédito en Chile | API gratuita con clave | Sí: la clave es obligatoria desde nov-2025 |
| **EIA (Departamento de Energía de EE. UU.)** | Precio del petróleo WTI y Brent | Determina el precio de la bencina en Chile | API v2 gratuita con clave (máximo 5.000 filas por consulta) | Parcial: falta confirmar el código de la serie de Brent |
| **Banco Mundial** | PIB, inflación y desempleo anual por país | Comparar a Chile con la región | API pública **sin clave** | Sí: probada, respondió con datos de Chile |
| **FMI y OCDE** | Proyecciones de crecimiento e inflación | Contexto de "lo que viene" | APIs SDMX públicas | No verificado |
| **GDELT** | Tono de las noticias del mundo sobre Chile | Complemento del termómetro Ánimo | API gratuita sin clave (con límite de consultas) | Sí: investigado antes (ver [sentimiento-noticias.md](sentimiento-noticias.md)) |
| **Google Trends** | Búsquedas como "desempleo", "crédito" o "seguro de cesantía" | Percepción en tiempo casi real | **No hay API oficial**: solo librerías no oficiales, que pueden romperse | Riesgoso |

**Antes de integrar FRED o EIA:** revisar el catálogo de la BDE del Banco Central, que ya publica series internacionales (cobre, petróleo, tasas externas). Si están ahí, una sola integración basta.

## 3. Lo que no conviene (o no se puede) obtener

| Dato | Problema | Alternativa |
|---|---|---|
| Precios de acciones en tiempo real (Bolsa) | Requiere licencia de nuam | Pedir acceso a nuam o usar un proveedor licenciado (ver [fuentes-de-datos.md](fuentes-de-datos.md)) |
| Texto completo de noticias (El Mercurio, DF) | Derechos de autor y muro de pago | Solo titular, bajada y enlace |
| Precios de supermercados por scraping | Términos de uso y fragilidad | ODEPA ya los mide |
| Datos personales (SII, bancos) | Ley 21.719 y seguridad | Esperar a Finanzas Abiertas (jul-2027) |
| Google Trends | Sin API oficial | Usarlo solo como experimento, sin depender de él |

## 4. Datos propios: cruzar fuentes para generar información nueva

Esto es lo que más diferencia a la app: nadie lo muestra junto y explicado.

| # | Dato propio | Cómo se calcula | Fuentes | Termómetro |
|---|---|---|---|---|
| 1 | **Horas de trabajo para la canasta** | Costo de la canasta ÷ (ingreso mínimo ÷ horas mensuales) | ODEPA, CNE, Panel de Expertos, Ley de ingreso mínimo | Bolsillo |
| 2 | **Marraquetas por sueldo mínimo** | Ingreso mínimo ÷ precio del kilo de marraqueta × 10 | ODEPA, Ley de ingreso mínimo | Bolsillo |
| 3 | **Costo de llenar el estanque** | Bencina 95 × 45 litros | CNE | Bolsillo |
| 4 | **"La bencina debería subir o bajar"** | Variación del precio de paridad (ENAP/CNE) vs. el precio actual en el surtidor | ENAP/CNE, CNE | Bolsillo |
| 5 | **Tu inflación vs. la oficial** | Variación de la canasta propia vs. IPC | ODEPA, CNE, INE | Bolsillo |
| 6 | **Sueldo real** | Variación de remuneraciones − variación del IPC | INE (vía BDE) | Actividad |
| 7 | **Índice de miseria** | Inflación + desempleo | INE (vía BDE) | Actividad |
| 8 | **Señal temprana de empleo** | Solicitudes del seguro de cesantía + empresas constituidas, contra su historia | Superintendencia de Pensiones, Ministerio de Economía | Actividad |
| 9 | **Dividendo estimado** | Crédito en UF × tasa hipotecaria promedio, recalculado con la UF del día | Banco Central, CMF | Deudas |
| 10 | **Tasa real** | TPM − inflación esperada por los expertos | Banco Central (TPM, EEE) | Deudas |
| 11 | **Margen del crédito** | Tasa máxima convencional − TPM | CMF, Banco Central | Deudas |
| 12 | **Rentabilidad real de las AFP** | Variación del valor cuota − variación de la UF | Superintendencia de Pensiones, Banco Central | Ahorro |
| 13 | **Años de sueldo para una vivienda** | Precio de vivienda (IPV) ÷ ingreso promedio anual | Banco Central (IPV), INE | Ahorro / Deudas |
| 14 | **Dólar vs. cobre** | Comparar sus movimientos; alertar cuando se separan | Banco Central | Dólar y mercados |
| 15 | **Presión eléctrica** | Costo marginal de la electricidad vs. su historia | Coordinador Eléctrico | Bolsillo (futuro) |
| 16 | **Datos vs. percepción** | Tono de las noticias y confianza del consumidor (IPEC) vs. los datos duros | Prensa, Banco Central | Ánimo |

**Cuidados:**
- Todo dato propio se rotula como **cálculo propio, no oficial**, con su fórmula publicada (como el índice de canasta).
- El **ingreso mínimo** cambia por ley: hay que guardarlo con sus fechas de vigencia y confirmar el valor en la ley vigente.

## 5. Tabla maestra de fuentes

**Estado:**
- **Foto real:** dato real cargado a mano con un script, todavía no automático.
- **Ejemplo:** el front lo muestra con valores inventados.
- **Prevista:** ya estaba en el plan, falta conectarla.
- **Nueva:** salió de esta investigación.
- **Bloqueada:** hoy no se puede obtener.

| Fuente | Qué datos | Sector que afecta | Frecuencia | Acceso | Estado |
|---|---|---|---|---|---|
| Banco Central (BDE) | UF, dólar, TPM, IPC, IMACEC, cobre, desempleo y series internacionales | Transversal: precios, crédito, actividad, sector externo | Diaria (UF, dólar, cobre), mensual (IPC, IMACEC), según reunión (TPM) | API REST con token | Prevista (falta el token) |
| Banco Central: EEE | Expectativas de IPC, PIB y TPM | Expectativas | Mensual | BDE | Nueva |
| Banco Central: IPV | Precios de vivienda | Vivienda / construcción | Trimestral (unos 120 días de desfase) | BDE | Nueva |
| Banco Central: ICVR | Compraventas por facturación electrónica | Comercio / actividad regional | Por confirmar (experimental) | Web | Nueva |
| CMF: indicadores | UF, dólar, UTM, IPC, TMC, TIP, TAB | Crédito / banca | Diaria y mensual | API con apikey | Prevista (falta la clave) |
| CMF: hechos esenciales | Hechos relevantes de empresas | Mercado de capitales | Continua | Web + alertas por correo | Prevista |
| Superintendencia de Pensiones: valor cuota | Rentabilidad de las AFP por fondo | Pensiones / ahorro | Diaria (provisional; se confirma después) | CSV | **Foto real** (`snapshot_afp.py`) |
| Superintendencia de Pensiones: seguro de cesantía | Solicitudes y beneficiarios | Empleo (adelantado) | Mensual | Series web | Nueva |
| ODEPA | Precios de alimentos al consumidor | Hogares / agro | Semanal (viernes) | CSV en datos abiertos (CKAN) | **Foto real** (`snapshot_odepa.py`) |
| CNE: combustibles | Bencina, diésel y gas por estación | Energía / transporte / hogares | Continua (según informe cada estación) | API con token Bearer | Ejemplo (falta el token) |
| ENAP / CNE: paridad MEPCO | Precio de paridad de los combustibles | Energía / hogares (anticipa precios) | Semanal | PDF / web | Nueva |
| Coordinador Eléctrico Nacional | Costo marginal de la electricidad | Energía / industria / tarifas | Horaria / diaria | API con credenciales | Nueva |
| Panel de Expertos | Tarifa de Metro y buses | Transporte / hogares | Eventual (1–2 veces al año) | Diario Oficial (manual) | **Real** (carga manual) |
| INE | Desempleo, remuneraciones, desglose del IPC | Empleo / precios | Mensual | Vía BDE; INE.Stat o Excel de respaldo | Prevista |
| SII | UTM, UTA, tabla de impuesto | Impuestos | Mensual | Páginas HTML | Prevista |
| SII: boletas electrónicas | Emisores y montos | Consumo / pymes | Mensual | Página de estadísticas | Nueva (sin API) |
| DIPRES | Ejecución presupuestaria | Fiscal | Mensual (1 mes de desfase) | datos.gob.cl (CKAN) | Prevista |
| Mercado Público | Licitaciones y órdenes de compra | Gasto público | Diaria | API con ticket (Clave Única) | Nueva |
| Aduanas | Exportaciones e importaciones | Sector externo | Mensual | Datos abiertos | Nueva |
| Registro de Empresas y Sociedades | Empresas constituidas | Emprendimiento / actividad | Mensual | Informe PDF | Nueva (sin datos tabulares) |
| Cochilco | Cobre, inventarios, litio | Minería / sector externo | Diaria | Web ("La Rueda"); el cobre también está en la BDE | Nueva |
| ANAC | Venta de autos nuevos | Consumo durable | Mensual | Informe PDF | Nueva (sin API) |
| nuam (Bolsa) | Precios de acciones, IPSA | Mercados | Continua | Licencia | **Bloqueada** |
| Prensa (RSS) | Titulares de La Tercera, BioBio, Cooperativa, CIPER, Ex-Ante | Percepción / ánimo | Minutos | RSS | Ejemplo (falta el recolector) |
| FRED | Tasas, inflación y bolsa de EE. UU., VIX | Mercados globales → dólar y crédito | Diaria | API gratuita con clave | Nueva |
| EIA | Petróleo WTI y Brent | Energía → bencina | Diaria / semanal | API gratuita con clave | Nueva |
| Banco Mundial | Macro anual comparada | Contexto internacional | Anual | API sin clave | Nueva |
| FMI / OCDE | Proyecciones | Contexto internacional | Trimestral / anual | SDMX | Nueva (no verificada) |
| GDELT | Tono de las noticias globales | Percepción | Cada 15 minutos | API sin clave | Nueva |
| Google Trends | Búsquedas | Percepción | Diaria / semanal | No oficial | Nueva (riesgosa) |

## Fuentes

- [Mercado Público: API y ticket](https://www.chilecompra.cl/api/)
- [Open Contracting: API de ChileCompra](https://data.open-contracting.org/en/publication/144)
- [Banco Central: Índice de Precios de Vivienda](https://www.bcentral.cl/areas/estadisticas/estadisticas-experimentales/ipv)
- [Banco Central: nota técnica ICVR](https://www.bcentral.cl/documents/d/banco-central/nota-tecnica-icvr)
- [Superintendencia de Pensiones: seguro de cesantía](https://www.spensiones.cl/portal/institucional/594/w3-article-13252.html)
- [Ministerio de Economía: informe RES julio 2024](https://www.economia.gob.cl/wp-content/uploads/2024/08/informe-res-2024-julio.pdf)
- [Aduanas: información de importaciones y exportaciones](https://www.aduana.cl/aduanas-publica-informacion-de-importaciones-y-exportaciones-en-su-web/aduana/2016-09-30/162849.html)
- [Reporte Minero: Cochilco "La Rueda"](https://www.reporteminero.cl/noticia/noticias/2026/09/precio-cobre-cochilco-lme-baja-inventarios-comex-2026)
- [Informe ENAP de precios de paridad (ejemplo)](https://media.pauta.cl/2024/07/Informe-ENAP.pdf)
- [CNE: informe MEPCO](https://www.cne.cl/wp-content/uploads/2015/06/2014_08_14__informe-mepco.pdf)
- [CNE: Norma Técnica de Coordinación y Operación](https://www.cne.cl/wp-content/uploads/2021/08/NT-de-Coordinacion-y-Operacion-del-SEN.pdf)
- [SII: estadísticas de boletas electrónicas](https://www.sii.cl/servicios_online/3767-3771.html)
- [EIA API v2 (guía de terceros)](https://www.oilpriceapi.com/eia-api)
- [FRED: acceso a la API (foro)](https://www.statalist.org/forums/forum/general-stata-discussion/general/1785609-access-to-fred-federal-reserve-economic-database)
- [ANAC: informes](https://www.anac.cl/wp-content/uploads/2024/09/08-ANAC-Informe-Cero-y-Bajas-Emisiones-Agosto-2024.pdf)
