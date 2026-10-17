"""Datos reales de la CMF, leídos de la foto cmf_snapshot.json.

La foto la arma app/ingesta/cmf.py y se lee con app/fotos.py (Supabase o el JSON de respaldo). Trae la tasa máxima
convencional (TMC) mensual de los últimos años, en todos sus tramos.
"""

from datetime import date

from app import fotos

FUENTE = "CMF"
# Créditos en pesos a 90 días o más, entre 50 y 200 UF: el tramo de un crédito de consumo típico.
TMC_CONSUMO = "44"
_FOTO = fotos.leer("cmf")


def tmc(tipo: str = TMC_CONSUMO) -> list[tuple[date, float]]:
    return [(date.fromisoformat(f), v) for f, v in _FOTO["tmc"][tipo]["observaciones"]]
