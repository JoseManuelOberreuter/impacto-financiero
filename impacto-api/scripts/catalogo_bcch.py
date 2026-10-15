"""Busca series en el catálogo de la Base de Datos Estadísticos del Banco Central.

Descarga el catálogo completo (unas 25.500 series) la primera vez, lo guarda en
un archivo local y filtra por palabras en el título en español o en inglés.
Solo muestra las series con datos vigentes del año indicado.

Uso:
    python scripts/catalogo_bcch.py cobre precio
    python scripts/catalogo_bcch.py "consumer loans" --desde 2026 --actualizar

Lee el token desde BCCH_TOKEN (variable de entorno o archivo .env).
Ver docs/banco-central-series.md.
"""

import argparse
import json
import os
import urllib.parse
import urllib.request
from pathlib import Path

URL = "https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx"
FRECUENCIAS = ["DAILY", "MONTHLY", "QUARTERLY", "ANNUAL"]
RAIZ = Path(__file__).resolve().parent.parent
CACHE = RAIZ / ".cache" / "bcch_catalogo.json"


def token() -> str:
    if os.getenv("BCCH_TOKEN"):
        return os.environ["BCCH_TOKEN"]
    archivo = RAIZ / ".env"
    if archivo.exists():
        for linea in archivo.read_text(encoding="utf-8").splitlines():
            clave, _, valor = linea.partition("=")
            if clave.strip() == "BCCH_TOKEN" and valor.strip():
                return valor.strip().strip("\"'")
    raise SystemExit("Falta BCCH_TOKEN en el entorno o en impacto-api/.env")


def leer_json(crudo: bytes) -> dict:
    try:
        return json.loads(crudo.decode("utf-8"))
    except UnicodeDecodeError:
        return json.loads(crudo.decode("latin-1"))


def descargar_catalogo() -> list[dict]:
    series = []
    for frecuencia in FRECUENCIAS:
        consulta = urllib.parse.urlencode(
            {"token": token(), "function": "SearchSeries", "frequency": frecuencia}
        )
        with urllib.request.urlopen(f"{URL}?{consulta}", timeout=120) as respuesta:
            datos = leer_json(respuesta.read())
        if datos.get("Codigo") != 0:
            raise SystemExit(f"Error del Banco Central: {datos.get('Descripcion')}")
        series.extend(datos.get("SeriesInfos") or [])
    CACHE.parent.mkdir(exist_ok=True)
    CACHE.write_text(json.dumps(series, ensure_ascii=False), encoding="utf-8")
    return series


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("palabras", nargs="+", help="palabras que deben estar en el título")
    parser.add_argument("--desde", default="2026", help="año mínimo de la última observación")
    parser.add_argument("--actualizar", action="store_true", help="vuelve a descargar el catálogo")
    args = parser.parse_args()

    if args.actualizar or not CACHE.exists():
        series = descargar_catalogo()
    else:
        series = json.loads(CACHE.read_text(encoding="utf-8"))

    palabras = [p.lower() for p in args.palabras]
    for serie in series:
        titulo = f"{serie['spanishTitle']} | {serie['englishTitle']}".lower()
        if all(p in titulo for p in palabras) and serie["lastObservation"][-4:] >= args.desde:
            print(
                f"{serie['seriesId']:<40} {serie['frequencyCode'][0]} "
                f"{serie['lastObservation']}  {serie['englishTitle'][:90]}"
            )


if __name__ == "__main__":
    main()
