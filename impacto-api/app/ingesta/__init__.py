"""Conectores de las fuentes de datos y la ingesta diaria (docs/ingesta.md).

Cada conector expone:
- ID, FUENTE_ID y ARCHIVO: nombre de la foto, fuente en la tabla `fuentes` y JSON de respaldo.
- generar() -> dict: descarga y arma la foto en el formato que usa la API.
- series(foto) -> list[Serie]: los valores con fecha, para guardar la historia en Supabase.

La ingesta completa se corre con `python -m app.ingesta` (ver __main__.py).
"""

from dataclasses import dataclass, field


@dataclass
class Serie:
    id: str
    nombre: str
    unidad: str | None
    frecuencia: str  # 'diaria', 'semanal', 'mensual', 'trimestral' o 'anual'
    observaciones: list[tuple[str, float]]
    codigo: str | None = None
    region: str | None = None
    provisional: bool = False
    metadatos: dict = field(default_factory=dict)


class FaltaCredencial(RuntimeError):
    """Falta una clave de la fuente en el entorno o en impacto-api/.env."""


def credencial(nombre: str) -> str:
    from app.supabase import variable

    valor = variable(nombre)
    if not valor:
        raise FaltaCredencial(f"Falta {nombre} en el entorno o en impacto-api/.env")
    return valor


def region(codigo: str) -> str:
    """'01' y '1' son la misma región: se guarda sin cero a la izquierda."""
    return str(int(codigo)) if codigo.isdigit() else codigo
