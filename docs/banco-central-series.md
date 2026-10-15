# Series del Banco Central (BDE)

> Catálogo revisado el 15-oct-2026 con la API de la Base de Datos Estadísticos (BDE). Es la base del conector del Banco Central ([pendientes-backend.md](pendientes-backend.md), fase 2).
> Fuentes relacionadas: [fuentes-de-datos.md](fuentes-de-datos.md), [investigacion-fuentes-ampliadas.md](investigacion-fuentes-ampliadas.md) y [termometros.md](termometros.md).

## Resumen

- Con **un solo token** (`BCCH_TOKEN`) se accede a unas **25.500 series**:

  | Frecuencia | Series |
  |---|---|
  | Diarias | 1.871 |
  | Mensuales | 9.080 |
  | Trimestrales | 8.782 |
  | Anuales | 5.812 |

- Cubre la mayoría de los termómetros: precios, deudas, actividad, dólar y parte del ánimo.
- **FRED y EIA pasan a ser probablemente innecesarias.** El cobre, el WTI, el Brent, el diésel y la bencina de EE. UU. ya están en la BDE.
- **La UTM también está en la BDE.** La CMF sigue haciendo falta para la tasa máxima convencional (TMC) y los hechos esenciales, pero ya no es urgente.
- Los datos que publica el Banco Central se citan como "Fuente: Banco Central de Chile", según sus condiciones de uso.

## Cómo se usa la API

**Autenticación:**
- Se usa el **API Key Token** de "Mi Cuenta" en la BDE (si3.bcentral.cl/siete).
- Dura un año y se puede extender sin cambiarlo.
- Va en `impacto-api/.env` como `BCCH_TOKEN`. Ver [.env.example](../impacto-api/.env.example).

**Endpoint REST:** `https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx`

| Función | Parámetros | Devuelve |
|---|---|---|
| `GetSeries` | `token`, `timeseries` (código), `firstdate` y `lastdate` (AAAA-MM-DD, opcionales) | Observaciones `{indexDateString: "DD-MM-AAAA", value, statusCode}` |
| `SearchSeries` | `token`, `frequency` (`DAILY`, `MONTHLY`, `QUARTERLY`, `ANNUAL`) | Catálogo: código, título en español e inglés, primera y última observación, fecha de actualización |

**Detalles del conector:**
- **Texto:** la respuesta puede venir con acentos mal codificados. Hay que leerla como bytes y decodificar con respaldo a Latin-1.
- **Respuesta:** `Codigo: 0` significa éxito. Cualquier otro código es un error y se registra en `corridas_ingesta`.
- **Valores:** vienen como texto. Los días sin dato pueden venir vacíos o como `NaN`, con un `statusCode` distinto de `OK`.
- **Valores adelantados:** la UF y el IVP se publican hasta el día 9 del mes siguiente. Hay que guardar todas las fechas, pero mostrar el valor de hoy.
- **Desfases:**
  - El índice de ventas diarias aparece con unas 6 semanas de atraso.
  - El IMACEC y el desempleo, con 1 a 2 meses.
  - El índice de precios de viviendas, con un trimestre o más.
  - Estos desfases se agregan a la tabla de desfases de [fuentes-de-datos.md](fuentes-de-datos.md).

**Buscar más series:** el script [`impacto-api/scripts/catalogo_bcch.py`](../impacto-api/scripts/catalogo_bcch.py) descarga el catálogo completo y permite buscar por palabra.

## Series por termómetro

Los códigos están verificados en el catálogo, con datos vigentes en 2026. Frecuencia: D = diaria, S = semanal (viene en la serie diaria), M = mensual, T = trimestral.

### Bolsillo: ¿está más cara la vida?

| Dato | Código | Frec. | Uso |
|---|---|---|---|
| IPC general, variación en 12 meses | `G073.IPC.V12.2023.M` | M | Dato principal de inflación |
| IPC general, variación mensual | `G073.IPC.VAR.2023.M` | M | "El IPC de septiembre fue..." |
| IPC general, índice | `G073.IPC.IND.2023.M` | M | Base para los cálculos propios |
| IPC de alimentos volátiles, variación en 12 meses | `G073.IPCAV.V12.2023.M` | M | Contrastar con nuestra canasta de ODEPA |
| IPC de energía volátil, variación en 12 meses | `G073.IPCEN.V12.2023.M` | M | Bencina, gas y electricidad en el IPC |
| UF | `F073.UFF.PRE.Z.D` | D | Se usa en todo el sistema |
| UTM | `F073.UTR.PRE.Z.M` | M | Multas, impuestos y trámites |
| Índice de ventas diarias del comercio minorista | `F034.VDCM.IND.DBC.2018.0.D` | D | **Nuevo:** termómetro de consumo |
| Lo mismo, promedio móvil de 28 días | `F034.VDCM.IPM28D.DBC.2018.0.D` | D | Versión suavizada para el gráfico |
| Lo mismo, sin estaciones de servicio | `F034.VDCMSES.IND.DBC.2018.0.D` | D | Consumo sin el efecto de la bencina |

### Deudas: ¿está más caro endeudarse?

| Dato | Código | Frec. | Uso |
|---|---|---|---|
| Tasa de política monetaria (TPM) | `F022.TPM.TIN.D001.NO.Z.D` | D | Dato principal |
| Tasa promedio de créditos de consumo, total | `F022.CON.TIP.Z.NO.Z.D` | S | "Pedir un crédito de consumo cuesta X %" |
| Tasa de consumo por plazo (menos de 6 meses, 6 a 12 meses, 1 a 3 años, más de 3 años) | `F022.CON.TIP.P180.NO.Z.D`, `.P1811.`, `.P13.`, `.P3.` | S | Calculadora de crédito |
| Tasa promedio de créditos hipotecarios a más de 3 años, en UF | `F022.VIV.TIP.MA03.UF.Z.D` | S | Calculadora de dividendo |
| Condiciones de crédito de consumo (encuesta a los bancos) | `F089.ECB.IND.CONSCC1.T` y siguientes | T | "¿Está difícil que te presten?" |
| Condiciones de crédito para pymes | `F089.ECB.IND.COMCC6.T` y siguientes | T | Plan pymes (etapa 3) |

### Actividad y empleo: ¿cómo va la economía?

| Dato | Código | Frec. | Uso |
|---|---|---|---|
| IMACEC, índice | `F032.IMC.IND.Z.Z.EP18.Z.Z.0.M` | M | Dato principal |
| IMACEC desestacionalizado | `F032.IMC.IND.Z.Z.EP18.Z.Z.1.M` | M | Comparar con el mes anterior |
| Tasa de desempleo nacional (INE, desestacionalizada) | `F049.DES.TAS.INE.10.M` | M | Dato principal |
| Desempleo de hombres y de mujeres | `F049.DES.TAS.INE.02.M`, `F049.DES.TAS.INE.03.M` | M | Detalle |
| Desempleo, serie histórica desde 1986 | `F049.DES.TAS.HIST.10.M` | M | Banda de "lo normal" con historia larga |
| Índice de remuneraciones reales (INE) | `G049.RMM.IND.INE23.R.M` | M | **Sueldo real:** ¿alcanza más o menos? |
| Remuneraciones nominales por actividad | `G049.RMM.IND.INEEP.*` | M | "Cómo suben los sueldos en tu rubro" |
| Ventas nominales por tamaño de empresa (micro, pequeña, mediana y grande) y rubro | `F034.IVEA*.FLU.BCCH.Z.ET*.M` (`ETMCE` = micro, `ETTOT` = total) | M | **Plan pymes:** cómo les va a las micro de tu rubro |
| Confianza empresarial (IMCE): total, sin minería, comercio | `G089.IME.IND.A0.M`, `.A04.`, `.A1.` | M | Ánimo de las empresas |

### Dólar y mercados: ¿qué pasa afuera?

| Dato | Código | Frec. | Uso |
|---|---|---|---|
| Dólar observado | `F073.TCO.PRE.Z.D` | D | Dato principal |
| Euro | `F072.CLP.EUR.N.O.D` | D | Viajes y compras en Europa |
| Cobre (Bolsa de Metales de Londres, US$ por libra) | `F019.PPB.PRE.100.D` | D | Dato principal externo |
| Petróleo WTI | `F019.PPB.PRE.41B.D` | D | Aviso de la bencina |
| Petróleo Brent | `F019.PPB.PRE.41AB.M` | M | Referencia |
| Bencina en EE. UU. (US$ por m³) | `F019.PPB.PRE.42.M` | M | Precio de paridad de la bencina |
| Diésel (US$ por galón) | `F019.PPB.PRE.35B.M` | M | Paridad del diésel |
| Oro | `F019.PPB.PRE.44B.M` | M | Referencia |
| IPSA | `F013.IBC.IND.N.7.LAC.CL.CLP.BLO.M` | M | **Solo mensual:** no reemplaza el cierre diario |

### Ánimo: ¿cómo lo ve la gente?

| Dato | Código | Frec. | Uso |
|---|---|---|---|
| IPEC (percepción económica de GfK Adimark), total | `F089.IPE.IND.75M2.M` | M | Complementa el tono de la prensa |
| IPEC: situación personal actual | `F089.IPE.IND.70M2.M` | M | "¿Cómo se sienten las personas con su plata?" |
| IPEC: el país a 12 meses | `F089.IPE.IND.72M2.M` | M | Optimismo o pesimismo |
| IPEC: expectativa de comprar electrodomésticos | `F089.IPE.IND.74M2.M` | M | Señal de consumo |

### Lo que viene: expectativas

| Dato | Código | Frec. | Uso |
|---|---|---|---|
| Inflación esperada a 11 meses (encuesta a economistas, EEE) | `F089.IPC.V12.14.M` | M | "Los expertos esperan una inflación de X %" |
| Inflación esperada a diciembre de este año y del próximo | `F089.IPC.V12.2026.M`, `F089.IPC.V12.2027.M` | M | Igual; el año cambia en el código |
| TPM esperada este mes, en 11 meses y en 23 meses | `F089.TPM.TAS.11.M`, `.14.`, `.15.` | M | "¿Bajarán las tasas?" |
| Dólar esperado en 2 y en 11 meses | `F089.TCN.PRE.13.M`, `F089.TCN.PRE.14.M` | M | Expectativa del dólar |
| Dólar esperado a 7 y a 28 días (operadores financieros, EOF) | `F089.EOF.TC.7DA.D`, `F089.EOF.TC.28DA.D` | Quincenal | Expectativa de corto plazo |
| PIB esperado para el próximo año | `F089.PIB.V12.2027.M` | M | Crecimiento esperado |
| Compensación inflacionaria del mercado (BEI) | `F022.BOFW.TAS.E3X2.Z.Z.D` y relacionadas | D | Inflación esperada según el mercado (Pro) |

### Vivienda (termómetro futuro)

| Dato | Código | Frec. | Uso |
|---|---|---|---|
| Índice de precios de viviendas: total, casas y departamentos | `F034.IPV.FLU.BCCH.2008.0.T`, `F034.IPVC.`, `F034.IPVD.` | T | "¿Está más cara la vivienda?" |
| Índice de precios de viviendas por zona | `F034.IPVZ*` | T | Comparación por zona |
| Oferta de viviendas nuevas (sin ejecución, en construcción, terminadas) | `F022.VIVRSE.STO.Z.Z.Z.T`, `.VIVREC.`, `.VIVRT.` | T | Oferta disponible |

### Señales tempranas: comercio exterior semanal

| Dato | Código | Frec. | Uso |
|---|---|---|---|
| Exportaciones de cobre | `F068.B1.FLU.A1.0.C.N.Z.Z.Z.Z.6.0.D` | S | Ingresos del país |
| Exportaciones de carbonato de litio | `F068.B1.FLU.A8.0.C.N.Z.Z.Z.Z.6.0.D` | S | Litio |
| Importaciones de autos | `F068.B1.FLU.C731.0.M.N.B.Z.Z.Z.6.0.D` | S | Señal de consumo de bienes durables |
| Importaciones de celulares, computadores y televisores | `F068.B1.FLU.C742...`, `.C741...`, `.C743...` | S | Señal de consumo |
| Importaciones de diésel | `F068.B1.FLU.P4.0.M.N.G.Z.Z.Z.6.0.D` | S | Energía |

## Datos propios que salen de cruzar estas series

Complementan la sección 4 de [investigacion-fuentes-ampliadas.md](investigacion-fuentes-ampliadas.md).

| Dato propio | Cruce | Para quién |
|---|---|---|
| **Sorpresa del dato** | Dato publicado (IPC, IMACEC, desempleo) vs. lo que esperaban los economistas en la EEE: "el IPC salió peor de lo esperado" | Personas e inversionistas |
| **Consumo vs. ánimo** | Ventas diarias del comercio vs. IPEC: la gente dice que está mal, ¿pero compra? | Personas |
| **Sueldo real** | Índice de remuneraciones reales, y nominales por rubro vs. IPC | Personas |
| **Micro vs. grandes** | Ventas de las micro empresas vs. el total de su rubro | Pymes |
| **Costo de endeudarse en pesos reales** | Tasa de consumo vs. inflación esperada | Personas |
| **Aviso de la bencina** | WTI y bencina en EE. UU. multiplicados por el dólar, frente a la paridad de ENAP y el MEPCO | Personas |
| **Dividendo hoy vs. hace un año** | Tasa hipotecaria en UF y la UF, aplicadas a un crédito típico | Personas |
| **Termómetro de consumo** | Ventas diarias, importaciones de autos y celulares, y expectativa de compra del IPEC | Personas y pymes |

## Siguientes pasos

1. Guardar este catálogo como configuración del conector: una lista de códigos, con el termómetro y la frecuencia de cada uno.
2. Hacer el conector del Banco Central: descarga inicial de 5 años de historia y después actualización diaria.
3. Calcular el estado de presión con percentiles de 5 años, según [termometros.md](termometros.md).
