# Catálogo de datos: de dónde sale cada dato

> Estado al 17-oct-2026. Cada fuente se descarga con su conector (`impacto-api/app/ingesta/`) a una "foto" que se guarda en Supabase, junto con la historia de cada serie ([ingesta.md](ingesta.md)). La API calcula todo a partir de esas fotos; si Supabase no responde, usa los JSON de respaldo de `impacto-api/app/datos_ejemplo/`. Este documento dice, para cada dato que muestra la app, de qué fuente viene, con qué código o archivo y cómo se actualiza.
> Detalle de cada API: [fuentes-de-datos.md](fuentes-de-datos.md). Códigos del Banco Central: [banco-central-series.md](banco-central-series.md). Metodologías propias: [impacto-financiero.md](impacto-financiero.md), [indice-canasta.md](indice-canasta.md) y [termometros.md](termometros.md).

## 1. Fuentes y cómo se actualizan

| Fuente | Qué entrega | Acceso | Credencial (`impacto-api/.env`) | Conector | Foto de respaldo en el repo | Última descarga |
|---|---|---|---|---|---|---|
| **Banco Central (BDE)** | 20 series: dólar, euro, UF, UTM, TPM, tasas, IPC (general y por división), IMACEC, desempleo, cobre, petróleo, IPEC, IMCE y expectativas | API REST | `BCCH_TOKEN` (vence al año) | `app/ingesta/bcch.py` | `bcch_snapshot.json` | 17-oct-2026 |
| **CNE** | Bencina y diésel por estación (hoy), historia mensual de combustibles y gas licuado por región | API REST (login con correo y clave) | `CNE_EMAIL`, `CNE_PASSWORD` | `app/ingesta/cne.py` | `cne_snapshot.json` | 17-oct-2026 |
| **CMF** | Tasa máxima convencional (TMC) por tramo, 6 años | API REST | `CMF_API_KEY` | `app/ingesta/cmf.py` | `cmf_snapshot.json` | 17-oct-2026 |
| **ODEPA** | Precios al consumidor de 10 alimentos, por semana, región y tipo de local | CSV de datos abiertos (se descarga solo) | No | `app/ingesta/odepa.py` | `odepa_snapshot.json` | Semana al 16-oct-2026 (descargada el 17-oct-2026) |
| **Superintendencia de Pensiones** | Valor cuota de las 7 AFP en los fondos A a E | Descarga pública | No | `app/ingesta/afp.py` | `afp_snapshot.json` | Dato al 14-oct-2026 |
| **INE: IX Encuesta de Presupuestos Familiares** | Gasto promedio de los hogares y su reparto por rubro y producto (oct-2021 a sep-2022) | Publicaciones y bases de datos (CSV) del INE | No | `scripts/resumen_epf.py` (ver sección 4) | `epf_ix.json` | Publicada el 26-oct-2023; microdatos procesados el 16-oct-2026 |
| **Panel de Expertos del Transporte Público** | Tarifa del Metro | Resolución publicada | No | (a mano) | En el código (`precios.py`) | Tarifa vigente desde el 22-feb-2026 |

**Cómo actualizar todo** (desde `impacto-api/`): guarda en Supabase y, con `--json`, también los respaldos del repo.

```bash
.venv/Scripts/python -m app.ingesta --json
```

Detalle, opciones y el cron diario: [ingesta.md](ingesta.md).

## 2. Dato por dato

### Inicio

| Dato | Fuente | Serie, endpoint o archivo | Cálculo |
|---|---|---|---|
| Fecha del encabezado | Servidor | `date.today()` | — |
| Titular del día | ODEPA | Canasta y alimento que más se movió | Propio: texto generado con los datos (`home.py`, `_titulo`) |
| Frase de la tasa y el dólar | Banco Central | `F022.TPM.TIN.D001.NO.Z.D`, `F073.TCO.PRE.Z.D` | Variación del dólar en 7 días |
| **Impacto Financiero** | INE (EPF) y Banco Central (IPC) | `epf_ix.json`; `G073.IPC.IND.2023.M`, `F074.IPC.IND.DIV10000/40000/70000.2023.C.M`; bencina (CNE) y UF a diario | Propio: [impacto-financiero.md](impacto-financiero.md) |
| Lo que cambió esta semana | Banco Central, CNE, CMF, ODEPA | Los 15 candidatos de `home.py` (`_candidatos`) | Propio: elige los que más presionan ([termometros.md](termometros.md)) |
| Termómetros | Ver la sección Termómetros | | |

### Termómetros

| Termómetro | Indicador | Fuente | Serie o archivo |
|---|---|---|---|
| **Bolsillo** | Índice de canasta | ODEPA, CNE, Panel de Expertos | `odepa_snapshot.json`, `cne_snapshot.json`, tarifa del Metro |
| | Marraqueta | ODEPA | `odepa_snapshot.json` |
| | IPC mensual y en 12 meses | Banco Central (dato del INE) | `G073.IPC.VAR.2023.M`, `G073.IPC.V12.2023.M` |
| | Bencina 95 | CNE | Mediana de estaciones de la RM (`/api/v4/estaciones`) e historia mensual (`/api/ea/precio/combustibleliquido`) |
| | Percepción económica (IPEC) | Banco Central (dato de GfK Chile) | `F089.IPE.IND.75M2.M` |
| **Deudas** | Tasa de política monetaria | Banco Central | `F022.TPM.TIN.D001.NO.Z.D` |
| | Tasa máxima convencional | CMF | TMC tramo 44 (`/recursos_api/tmc/{año}`) |
| | Tasa hipotecaria en UF | Banco Central | `F022.VIV.TIP.MA03.UF.Z.D` |
| | Tasa de créditos de consumo (en el texto) | Banco Central | `F022.CON.TIP.Z.NO.Z.D` |
| | Expectativa de TPM (en el texto) | Banco Central (Encuesta de Expectativas Económicas) | `F089.TPM.TAS.14.M` |
| **Ahorro y pensiones** | Fondos A, C y E | Superintendencia de Pensiones | `afp_snapshot.json` (mediana de las 7 AFP) |
| **Actividad y empleo** | Desempleo | Banco Central (dato del INE) | `F049.DES.TAS.INE9.10.M` |
| | IMACEC en 12 meses | Banco Central | `F032.IMC.V12.Z.Z.2018.Z.Z.0.M` |
| **Dólar y mercados** | Dólar observado | Banco Central | `F073.TCO.PRE.Z.D` |
| | Cobre | Banco Central (Bolsa de Metales de Londres) | `F019.PPB.PRE.100.D` |
| **Ánimo** | Percepción de las personas (IPEC) | Banco Central (dato de GfK Chile) | `F089.IPE.IND.75M2.M` |
| | Confianza de las empresas (IMCE) | Banco Central (dato de ICARE y UAI) | `G089.IME.IND.A0.M` |

La **presión** de cada indicador es un cálculo propio: percentiles 20 y 80 de sus últimos 5 años (`app/calculos/presion.py`).

### Precios

| Dato | Fuente | Detalle |
|---|---|---|
| 10 alimentos (precio, 12 semanas, por región y tipo de local) | ODEPA | `odepa_snapshot.json` |
| Canasta semanal | ODEPA, CNE y Panel de Expertos | Propio: [indice-canasta.md](indice-canasta.md) |
| Bencina 95 | CNE | Mediana de las estaciones de la RM con precio de los últimos 7 días |
| Gas licuado 15 kg | CNE | Promedio mensual de la RM, cilindro corriente (`/api/ea/precio/glp`) |
| Pasaje de Metro | Panel de Expertos del Transporte Público | $895, cargado a mano |

### Herramientas

| Dato | Fuente | Detalle |
|---|---|---|
| Mi impacto: dividendo | Banco Central | UF de hoy, última publicada, hace un mes y hace un año (`/v1/mi-impacto/referencias`). Los datos del usuario quedan en su dispositivo |
| Mi impacto: bencina | CNE | Precio de hoy y promedio mensual de hace un año |
| Mi AFP | Superintendencia de Pensiones | `afp_snapshot.json` |
| Calendario económico | Escrito a mano | Fechas habituales; algunas estimadas. Pendiente: calendarios oficiales del Banco Central y el INE |

### Lo que todavía no es real

| Dato | Estado |
|---|---|
| **Noticias** (titulares, temas, tono y hechos esenciales) | Inventadas para el diseño (`noticias.py`). Pendiente: RSS de los medios |
| Fechas de "próximas publicaciones" | Escritas a mano |
| Luz | Hay dato de la CNE (cuenta tipo por comuna, `/api/ea/cuentatipo`), pero todavía no se usa |

## 3. Condiciones de uso

- **Banco Central:** se puede reproducir citando al Banco Central como fuente. La reventa de datos crudos hay que confirmarla ([riesgos.md](riesgos.md)).
- **CNE:** los precios de las estaciones son públicos (Rex CNE 492/2023).
- **INE:** datos abiertos según sus "Términos de Uso y Licencia de Datos Abiertos"; citar al INE.
- **ODEPA, CMF y Superintendencia de Pensiones:** datos públicos; citar la fuente.
- Toda cifra propia (canasta, presión, Impacto Financiero) se presenta como **indicador propio de referencia**, con su metodología publicada.

## 4. Encuesta de Presupuestos Familiares (INE)

**Guardado en el repo:** `impacto-api/app/datos_ejemplo/epf_ix.json`, con los resultados publicados de la IX EPF y los enlaces a cada documento:
- Gasto promedio mensual por hogar: $1.451.782 en las capitales regionales y **$1.590.105 en el Gran Santiago** (mediana: $1.204.455).
- Reparto del gasto en 13 rubros (alimentos 21,2 %, vivienda y servicios 16,0 %, transporte 15,0 %, etc.).
- Período: octubre de 2021 a septiembre de 2022. Publicada el 26-oct-2023.

**Bases de datos completas** (página de la EPF → Bases de datos → IX EPF), en CSV y Stata:

| Archivo | Tamaño | Para qué |
|---|---|---|
| Base Gastos IX EPF (CSV) | 145 MB | Gasto de cada hogar por producto: permite el reparto exacto del Gran Santiago y el peso de la bencina, la luz o el arriendo |
| Base Personas IX EPF (CSV) | 115 MB | Características e ingresos de los hogares, con los factores de expansión |
| Base Cantidades IX EPF (CSV) | 212 MB | Cantidades compradas (por ejemplo, kilos de pan o litros de bencina) |
| CCIF IX EPF (CSV) | 140 KB | Clasificación de productos (divisiones, grupos y subclases) |

Son demasiado grandes para el repositorio. **Hecho el 16-oct-2026:** la base de gastos y la CCIF se descargaron a `impacto-api/.cache/epf/` (ignorada por git) y `scripts/resumen_epf.py` guarda en `epf_ix.json` (clave `gran_santiago_microdatos`) el resumen del Gran Santiago:
- gasto promedio por división (13 rubros), que coincide con lo publicado por el INE;
- gasto en los productos que seguimos con datos frecuentes: gasolina, diésel, gas, electricidad, arriendo, transporte público y los 9 alimentos de ODEPA.

Criterios verificados: la **macrozona 2 es el Gran Santiago** (1 norte, 3 centro, 4 sur) y el INE **excluye los arriendos imputados** (CCIF 04.2) de sus promedios publicados.

Para regenerarlo (desde `impacto-api/`, con el CSV en `.cache/epf/gastos.csv`):

```bash
.venv/Scripts/python scripts/resumen_epf.py .cache/epf/gastos.csv app/datos_ejemplo/epf_ix.json
```

**Próxima edición:** la X EPF se levanta entre septiembre de 2026 y agosto de 2027; sus resultados reemplazarán a los de la IX.
