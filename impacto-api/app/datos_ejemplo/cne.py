"""Datos reales de la CNE, leídos de la foto cne_snapshot.json.

La foto se genera con scripts/snapshot_cne.py. Trae la mediana de hoy en las
estaciones de servicio (solo precios actualizados hace poco) y la historia
mensual por región de los combustibles y del gas licuado.
"""

import json
from datetime import date
from pathlib import Path

FUENTE = "CNE"
REGION_METROPOLITANA = "13"
_FOTO = json.loads((Path(__file__).parent / "cne_snapshot.json").read_text(encoding="utf-8"))
DESCARGADO_EL = date.fromisoformat(_FOTO["descargado_el"])


def hoy(combustible: str, region: str = REGION_METROPOLITANA) -> dict:
    """Mediana de hoy: {'mediana', 'estaciones_frescas', 'estaciones_total', 'dias_fresco'}."""
    return _FOTO["estaciones"][combustible][region]


def mensual(id_: str, region: str = REGION_METROPOLITANA) -> list[tuple[date, float]]:
    """Promedios mensuales válidos (la historia de la CNE tiene meses sin dato)."""
    datos = _FOTO["mensual_combustibles"].get(id_) or _FOTO["mensual_gas"][id_]
    return [(date.fromisoformat(f), v) for f, v in datos[region]]
