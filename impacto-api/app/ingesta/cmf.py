"""Conector de la CMF: la tasa máxima convencional (TMC) de los últimos años, en todos sus tramos.

La TMC es el interés máximo que la ley permite cobrar en un crédito; cambia una vez al mes.

Uso suelto (solo escribe el JSON):
    python -m app.ingesta.cmf app/datos_ejemplo/cmf_snapshot.json

Lee CMF_API_KEY (variable de entorno o archivo .env).
"""

import json
import sys
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

from app.ingesta import Serie, credencial

ID = "cmf"
FUENTE_ID = "cmf"
ARCHIVO = "cmf_snapshot.json"
URL = "https://api.cmfchile.cl/api-sbifv3/recursos_api"
ANIOS = 6


def pedir(recurso: str) -> dict:
    consulta = urllib.parse.urlencode({"apikey": credencial("CMF_API_KEY"), "formato": "json"})
    with urllib.request.urlopen(f"{URL}/{recurso}?{consulta}", timeout=60) as respuesta:
        crudo = respuesta.read()
    try:
        return json.loads(crudo.decode("utf-8"))
    except UnicodeDecodeError:
        return json.loads(crudo.decode("latin-1"))


def generar() -> dict:
    hoy = date.today()
    tramos: dict[str, dict] = {}
    for anio in range(hoy.year - ANIOS, hoy.year + 1):
        for fila in pedir(f"tmc/{anio}").get("TMCs") or []:
            tipo = fila.get("Tipo")
            try:
                valor = float(str(fila["Valor"]).replace(",", "."))
            except (KeyError, ValueError):
                continue
            tramo = tramos.setdefault(
                tipo,
                {"titulo": fila.get("Titulo") or "", "subtitulo": fila.get("SubTitulo") or "", "observaciones": []},
            )
            # La CMF a veces deja el título vacío: se completa con el de otro mes.
            tramo["titulo"] = tramo["titulo"] or fila.get("Titulo") or ""
            tramo["observaciones"].append([fila["Fecha"], valor])
    for tramo in tramos.values():
        tramo["observaciones"].sort()
    print(f"  {len(tramos)} tramos de TMC")

    return {"fuente": "Comisión para el Mercado Financiero (CMF)", "descargado_el": hoy.isoformat(), "tmc": tramos}


def series(foto: dict) -> list[Serie]:
    return [
        Serie(
            id=f"cmf.tmc.{tipo}",
            nombre=f"TMC: {tramo['titulo']}. {tramo['subtitulo']}".strip(". "),
            unidad="%",
            frecuencia="mensual",
            codigo=tipo,
            observaciones=[(f, v) for f, v in tramo["observaciones"]],
        )
        for tipo, tramo in foto["tmc"].items()
    ]


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    Path(sys.argv[1]).write_text(json.dumps(generar(), ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
