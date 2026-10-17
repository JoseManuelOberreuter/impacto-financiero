"""Acceso a Supabase desde el backend: Auth (quién es el usuario) y la base (vía PostgREST).

Usa la clave secreta (SUPABASE_SERVICE_ROLE_KEY), que solo vive en el servidor. Lee la
configuración de las variables de entorno o, en desarrollo, del archivo impacto-api/.env.
"""

import os
from functools import lru_cache
from pathlib import Path

import httpx

_ENV = Path(__file__).resolve().parent.parent / ".env"


def _variable(nombre: str) -> str | None:
    if os.getenv(nombre):
        return os.environ[nombre]
    if _ENV.exists():
        for linea in _ENV.read_text(encoding="utf-8").splitlines():
            clave, _, valor = linea.partition("=")
            if clave.strip() == nombre and valor.strip():
                return valor.strip().strip("\"'")
    return None


class SinConfiguracion(RuntimeError):
    """Faltan SUPABASE_URL o SUPABASE_SERVICE_ROLE_KEY."""


@lru_cache
def _config() -> tuple[str, str]:
    url, clave = _variable("SUPABASE_URL"), _variable("SUPABASE_SERVICE_ROLE_KEY")
    if not url or not clave:
        raise SinConfiguracion("Faltan SUPABASE_URL o SUPABASE_SERVICE_ROLE_KEY")
    return url.rstrip("/"), clave


def _cabeceras(token: str | None = None) -> dict[str, str]:
    _, clave = _config()
    return {"apikey": clave, "Authorization": f"Bearer {token or clave}"}


def usuario_desde_token(token: str) -> dict | None:
    """Pregunta a Supabase Auth de quién es el token. None si es inválido o venció."""
    url, _ = _config()
    respuesta = httpx.get(f"{url}/auth/v1/user", headers=_cabeceras(token), timeout=10)
    return respuesta.json() if respuesta.status_code == 200 else None


def seleccionar(tabla: str, filtros: dict[str, str], columnas: str = "*") -> list[dict]:
    url, _ = _config()
    respuesta = httpx.get(
        f"{url}/rest/v1/{tabla}", params={"select": columnas, **filtros}, headers=_cabeceras(), timeout=10
    )
    respuesta.raise_for_status()
    return respuesta.json()


def guardar(tabla: str, fila: dict, conflicto: str) -> dict:
    """Inserta o actualiza (upsert) una fila según la columna de conflicto."""
    url, _ = _config()
    respuesta = httpx.post(
        f"{url}/rest/v1/{tabla}",
        params={"on_conflict": conflicto},
        json=fila,
        headers={**_cabeceras(), "Prefer": "resolution=merge-duplicates,return=representation"},
        timeout=10,
    )
    respuesta.raise_for_status()
    return respuesta.json()[0]


def borrar_usuario(usuario_id: str) -> None:
    """Borra la cuenta en Supabase Auth; perfil, preferencias y suscripciones se borran en cascada."""
    url, _ = _config()
    respuesta = httpx.delete(f"{url}/auth/v1/admin/users/{usuario_id}", headers=_cabeceras(), timeout=10)
    respuesta.raise_for_status()
