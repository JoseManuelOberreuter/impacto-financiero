"""Genera una foto de la tasa máxima convencional (TMC) de la CMF para la API.

Primer borrador del conector de la CMF: descarga la TMC de los últimos años,
en todos sus tramos, y la guarda en un JSON. La TMC es el interés máximo que
la ley permite cobrar en un crédito; cambia una vez al mes.

Uso:
    python scripts/snapshot_cmf.py app/datos_ejemplo/cmf_snapshot.json

Lee CMF_API_KEY (variable de entorno o archivo .env).
"""

import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

URL = "https://api.cmfchile.cl/api-sbifv3/recursos_api"
RAIZ = Path(__file__).resolve().parent.parent
ANIOS = 6


def apikey() -> str:
    if os.getenv("CMF_API_KEY"):
        return os.environ["CMF_API_KEY"]
    archivo = RAIZ / ".env"
    if archivo.exists():
        for linea in archivo.read_text(encoding="utf-8").splitlines():
            clave, _, valor = linea.partition("=")
            if clave.strip() == "CMF_API_KEY" and valor.strip():
                return valor.strip().strip("\"'")
    raise SystemExit("Falta CMF_API_KEY en el entorno o en impacto-api/.env")


def pedir(recurso: str) -> dict:
    consulta = urllib.parse.urlencode({"apikey": apikey(), "formato": "json"})
    with urllib.request.urlopen(f"{URL}/{recurso}?{consulta}", timeout=60) as respuesta:
        crudo = respuesta.read()
    try:
        return json.loads(crudo.decode("utf-8"))
    except UnicodeDecodeError:
        return json.loads(crudo.decode("latin-1"))


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    salida = Path(sys.argv[1])
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

    foto = {
        "fuente": "Comisión para el Mercado Financiero (CMF)",
        "descargado_el": hoy.isoformat(),
        "tmc": tramos,
    }
    salida.write_text(json.dumps(foto, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    for tipo, tramo in sorted(tramos.items()):
        print(f"TMC {tipo:>3}: {tramo['observaciones'][-1]}  {tramo['subtitulo'][:70]}")
    print(f"Guardado en {salida} ({salida.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
