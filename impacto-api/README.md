# impacto-api

Backend de Impacto Financiero: API (FastAPI) y, más adelante, el worker de ingesta y cálculos. Ver [../docs/arquitectura.md](../docs/arquitectura.md).

> Estado: endpoints de todas las secciones con **datos de ejemplo** (`app/datos_ejemplo/`). Alimentos (ODEPA), AFP (Superintendencia de Pensiones), las series del Banco Central, la bencina y el gas (CNE) y la tasa máxima convencional (CMF) vienen de fotos reales generadas con los scripts de `scripts/`. Todavía no hay base de datos ni actualización automática.

## Requisitos

- Python 3.13

## Correr en local

Crear el entorno e instalar dependencias (una sola vez):

```bash
python -m venv .venv
```

```bash
.venv/Scripts/python -m pip install -r requirements-dev.txt
```

Levantar la API en `http://localhost:8000`:

```bash
.venv/Scripts/python -m uvicorn app.main:app --reload --port 8000
```

- Documentación interactiva: `http://localhost:8000/docs`
- Especificación OpenAPI (para generar el cliente TypeScript de la app): `http://localhost:8000/openapi.json`

En macOS o Linux, usar `.venv/bin/python` en vez de `.venv/Scripts/python`.

## Tests

```bash
.venv/Scripts/python -m pytest
```

## Variables de entorno

| Variable | Para qué | Por defecto |
|---|---|---|
| `CORS_ORIGINS` | Orígenes web permitidos, separados por coma | `http://localhost:8081` |
| `PORT` | Puerto (lo define Railway) | `8000` |
| `CACHE_SEGUNDOS` | Segundos que el navegador puede guardar la respuesta (usar `0` en desarrollo) | `300` |
| `MODO_PLANES` | Cómo se aplican los planes: `abierto`, `vista_previa` o `activo` (ver docs/planes.md) | `abierto` |

Las claves de las fuentes (Banco Central, CMF, CNE y otras) van en un archivo `.env`, que no se sube a GitHub. Copia [.env.example](.env.example) como `.env` y completa las que tengas.

## Docker

```bash
docker build -t impacto-api .
```

```bash
docker run -p 8000:8000 impacto-api
```

## Endpoints

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/salud` | Estado del servicio |
| GET | `/v1/home` | Todo lo que necesita el Inicio: resumen, canasta, "lo que cambió esta semana" y termómetros |
| GET | `/v1/termometros` | Lista de termómetros |
| GET | `/v1/termometros/{id}` | Detalle: explicación, indicadores con serie y banda normal, percepción, próximas publicaciones |
| GET | `/v1/precios` | Canasta, productos de ODEPA, energía y transporte |
| GET | `/v1/precios/{id}` | Detalle de un producto: serie, por tipo de local y por región |
| GET | `/v1/noticias` | Ánimo de la prensa, temas, titulares y hechos esenciales (de ejemplo) |
| GET | `/v1/herramientas` | Mi AFP, calculadoras, calendario y metodología |
| GET | `/v1/mi-impacto/referencias` | UF (hoy, última publicada, hace un mes y un año) y bencina (hoy y hace un año) para que la app calcule Mi impacto sin enviar los datos del usuario |
| GET | `/v1/yo/capacidades` | Modo de los planes y capacidades del usuario (sin cuentas: plan gratis) |

## Fotos de datos reales (borradores de conectores)

Generan los JSON que usan los datos de ejemplo. Son el punto de partida de los conectores del worker.

ODEPA (precios al consumidor). Primero descarga el CSV del año desde datos.odepa.gob.cl:

```bash
.venv/Scripts/python scripts/snapshot_odepa.py precio_consumidor_2026.csv app/datos_ejemplo/odepa_snapshot.json
```

Superintendencia de Pensiones (valor cuota de los fondos A a E; descarga sola):

```bash
.venv/Scripts/python scripts/snapshot_afp.py 2026 app/datos_ejemplo/afp_snapshot.json
```

Banco Central (16 series principales, 6 años; usa `BCCH_TOKEN` del `.env`). Para actualizar los datos reales, vuelve a correrlo:

```bash
.venv/Scripts/python scripts/snapshot_bcch.py app/datos_ejemplo/bcch_snapshot.json
```

CNE (precio de hoy de la bencina por región e historia mensual de combustibles y gas; usa `CNE_EMAIL` y `CNE_PASSWORD` del `.env`):

```bash
.venv/Scripts/python scripts/snapshot_cne.py app/datos_ejemplo/cne_snapshot.json
```

CMF (tasa máxima convencional de los últimos 6 años, en todos sus tramos; usa `CMF_API_KEY` del `.env`):

```bash
.venv/Scripts/python scripts/snapshot_cmf.py app/datos_ejemplo/cmf_snapshot.json
```

INE, Encuesta de Presupuestos Familiares (resumen del Gran Santiago a partir de la base de gastos, descargada a `.cache/epf/`; ver docs/catalogo-de-datos.md):

```bash
.venv/Scripts/python scripts/resumen_epf.py .cache/epf/gastos.csv app/datos_ejemplo/epf_ix.json
```

Para buscar otros códigos de serie en el catálogo:

```bash
.venv/Scripts/python scripts/catalogo_bcch.py cobre precio
```

Los códigos elegidos por termómetro están en [docs/banco-central-series.md](../docs/banco-central-series.md).
