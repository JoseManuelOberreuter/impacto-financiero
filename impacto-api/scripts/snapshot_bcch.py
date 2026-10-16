"""Genera una foto de las series principales del Banco Central para la API.

Primer borrador del conector del Banco Central: descarga los últimos años de
cada serie del catálogo de abajo y los guarda en un JSON. La API calcula con
ellos la presión, la banda normal y los gráficos. Cuando exista la base de
datos (Supabase), el mismo catálogo y la misma descarga guardarán ahí.

Uso:
    python scripts/snapshot_bcch.py app/datos_ejemplo/bcch_snapshot.json

Lee el token desde BCCH_TOKEN (variable de entorno o archivo .env).
Códigos y criterios: docs/banco-central-series.md.
"""

import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

URL = "https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx"
RAIZ = Path(__file__).resolve().parent.parent
# 5 años para la banda normal, más 1 de margen para calcular variaciones.
ANIOS = 6

# id: (código, nombre, unidad)
SERIES = {
    "dolar": ("F073.TCO.PRE.Z.D", "Dólar observado", "$ por dólar"),
    "euro": ("F072.CLP.EUR.N.O.D", "Euro", "$ por euro"),
    "uf": ("F073.UFF.PRE.Z.D", "UF", "$"),
    "utm": ("F073.UTR.PRE.Z.M", "UTM", "$"),
    "tpm": ("F022.TPM.TIN.D001.NO.Z.D", "Tasa de política monetaria", "%"),
    "cobre": ("F019.PPB.PRE.100.D", "Cobre", "US$ por libra"),
    "petroleo_wti": ("F019.PPB.PRE.41B.D", "Petróleo WTI", "US$ por barril"),
    "ipc_mensual": ("G073.IPC.VAR.2023.M", "IPC, variación mensual", "%"),
    "ipc_12m": ("G073.IPC.V12.2023.M", "IPC, variación en 12 meses", "%"),
    "imacec_12m": ("F032.IMC.V12.Z.Z.2018.Z.Z.0.M", "IMACEC, variación en 12 meses", "%"),
    "desempleo": ("F049.DES.TAS.INE9.10.M", "Tasa de desempleo", "%"),
    "tasa_hipotecaria": ("F022.VIV.TIP.MA03.UF.Z.D", "Tasa hipotecaria en UF, más de 3 años", "%"),
    "tasa_consumo": ("F022.CON.TIP.Z.NO.Z.D", "Tasa de créditos de consumo", "%"),
    "ipec": ("F089.IPE.IND.75M2.M", "Percepción económica (IPEC)", "puntos"),
    "imce": ("G089.IME.IND.A0.M", "Confianza empresarial (IMCE)", "puntos"),
    "ipc_esperado_11m": ("F089.IPC.V12.14.M", "Inflación esperada en 11 meses", "%"),
    "tpm_esperada_11m": ("F089.TPM.TAS.14.M", "TPM esperada en 11 meses", "%"),
}


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


def descargar(codigo: str, desde: date) -> list[list]:
    consulta = urllib.parse.urlencode(
        {
            "token": token(),
            "function": "GetSeries",
            "timeseries": codigo,
            "firstdate": desde.isoformat(),
        }
    )
    with urllib.request.urlopen(f"{URL}?{consulta}", timeout=60) as respuesta:
        datos = leer_json(respuesta.read())
    if datos.get("Codigo") != 0:
        raise RuntimeError(f"{codigo}: {datos.get('Descripcion')}")
    observaciones = []
    for obs in (datos.get("Series") or {}).get("Obs") or []:
        if obs.get("statusCode") != "OK":
            continue
        try:
            valor = float(obs["value"])
        except (TypeError, ValueError):
            continue
        dia, mes, anio = obs["indexDateString"].split("-")
        observaciones.append([f"{anio}-{mes}-{dia}", valor])
    return observaciones


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    salida = Path(sys.argv[1])
    hoy = date.today()
    desde = date(hoy.year - ANIOS, hoy.month, 1)

    series = {}
    for id_, (codigo, nombre, unidad) in SERIES.items():
        observaciones = descargar(codigo, desde)
        if not observaciones:
            raise SystemExit(f"{id_} ({codigo}) no trajo datos")
        series[id_] = {
            "codigo": codigo,
            "nombre": nombre,
            "unidad": unidad,
            "observaciones": observaciones,
        }
        print(f"{id_:<18} {len(observaciones):>5} obs., último {observaciones[-1]}")

    foto = {
        "fuente": "Banco Central de Chile, Base de Datos Estadísticos",
        "descargado_el": hoy.isoformat(),
        "series": series,
    }
    salida.write_text(json.dumps(foto, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"Guardado en {salida} ({salida.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
