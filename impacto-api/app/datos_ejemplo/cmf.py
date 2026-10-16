"""Datos reales de la CMF, leídos de la foto cmf_snapshot.json.

La foto se genera con scripts/snapshot_cmf.py. Trae la tasa máxima
convencional (TMC) mensual de los últimos años, en todos sus tramos.
"""

import json
from datetime import date
from pathlib import Path

FUENTE = "CMF"
# Créditos en pesos a 90 días o más, entre 50 y 200 UF: el tramo de un crédito de consumo típico.
TMC_CONSUMO = "44"
_FOTO = json.loads((Path(__file__).parent / "cmf_snapshot.json").read_text(encoding="utf-8"))


def tmc(tipo: str = TMC_CONSUMO) -> list[tuple[date, float]]:
    return [(date.fromisoformat(f), v) for f, v in _FOTO["tmc"][tipo]["observaciones"]]
