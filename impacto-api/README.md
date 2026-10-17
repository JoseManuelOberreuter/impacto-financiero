# impacto-api

Backend de Impacto Financiero: API (FastAPI) y, más adelante, el worker de ingesta y cálculos. Ver [../docs/arquitectura.md](../docs/arquitectura.md).

> Estado: endpoints de todas las secciones con **datos de ejemplo** (`app/datos_ejemplo/`). Alimentos (ODEPA), AFP (Superintendencia de Pensiones), las series del Banco Central, la bencina y el gas (CNE) y la tasa máxima convencional (CMF) vienen de fotos reales que guarda en Supabase la ingesta (`python -m app.ingesta`, ver [docs/ingesta.md](../docs/ingesta.md)); si Supabase no responde, la API usa los JSON de respaldo de `app/datos_ejemplo/`.

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
| GET | `/v1/datos` | Todos los datos con su último movimiento, presión, tema, efecto y tono, ordenados por presión |
| GET | `/v1/mi-impacto/referencias` | UF (hoy, última publicada, hace un mes y un año) y bencina (hoy y hace un año) para que la app calcule Mi impacto sin enviar los datos del usuario |
| GET | `/v1/yo/capacidades` | Modo de los planes y capacidades del usuario (sin sesión: plan gratis) |
| GET | `/v1/yo` | Datos de la cuenta: correo, nombre, verificado y plan (requiere sesión) |
| GET | `/v1/yo/preferencias` | Datos anclados, apariencia y Mi impacto guardados en la cuenta (requiere sesión) |
| PUT | `/v1/yo/preferencias` | Guarda las preferencias de la cuenta (requiere sesión) |
| DELETE | `/v1/yo` | Borra la cuenta y sus datos (requiere sesión) |

## Ingesta de datos reales

Los conectores están en `app/ingesta/` (Banco Central, CNE, CMF, ODEPA y Superintendencia de Pensiones). Descargan cada fuente, guardan la foto y la historia en Supabase y registran cada corrida. Usan las claves del `.env` (`BCCH_TOKEN`, `CNE_EMAIL`, `CNE_PASSWORD`, `CMF_API_KEY`, `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`).

```bash
.venv/Scripts/python -m app.ingesta              # todas las fuentes
.venv/Scripts/python -m app.ingesta bcch cmf     # solo algunas
.venv/Scripts/python -m app.ingesta --json       # además actualiza los JSON de respaldo
```

La API revisa cada 15 minutos (`REVISAR_FOTOS_MINUTOS`) si hay fotos nuevas y se recarga sola. `GET /salud` muestra qué foto usa de cada fuente. Con `FOTOS_DESDE=archivos` usa solo los JSON de respaldo. Detalle en [docs/ingesta.md](../docs/ingesta.md).

INE, Encuesta de Presupuestos Familiares (resumen del Gran Santiago a partir de la base de gastos, descargada a `.cache/epf/`; ver docs/catalogo-de-datos.md):

```bash
.venv/Scripts/python scripts/resumen_epf.py .cache/epf/gastos.csv app/datos_ejemplo/epf_ix.json
```

Para buscar otros códigos de serie en el catálogo:

```bash
.venv/Scripts/python scripts/catalogo_bcch.py cobre precio
```

Los códigos elegidos por termómetro están en [docs/banco-central-series.md](../docs/banco-central-series.md).
