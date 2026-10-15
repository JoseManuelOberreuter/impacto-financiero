# impacto-api

Backend de Impacto Financiero: API (FastAPI) y, más adelante, el worker de ingesta y cálculos. Ver [../docs/arquitectura.md](../docs/arquitectura.md).

> Estado: solo existe `GET /v1/home`, con **datos de ejemplo** (`app/datos_ejemplo/home.py`). Todavía no hay conectores a las fuentes ni base de datos.

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
| GET | `/v1/home` | Todo lo que necesita la pantalla de inicio: resumen, termómetros, termómetros por defecto y aviso legal |
