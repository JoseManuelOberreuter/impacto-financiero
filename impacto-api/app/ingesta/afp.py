"""Conector de la Superintendencia de Pensiones: rentabilidad de los fondos de pensiones.

Descarga el CSV de valores cuota del año (fondos A a E) y calcula la rentabilidad
nominal de cada AFP en el año y en los últimos ~30 días.

Uso suelto (solo escribe el JSON):
    python -m app.ingesta.afp app/datos_ejemplo/afp_snapshot.json

Los valores más recientes son provisionales (ver docs/fuentes-de-datos.md).
"""

import json
import sys
import urllib.request
from datetime import date, timedelta
from pathlib import Path

from app.ingesta import Serie

ID = "afp"
FUENTE_ID = "sp"
ARCHIVO = "afp_snapshot.json"

URL = (
    "https://www.spensiones.cl/apps/valoresCuotaFondo/vcfAFPxls.php"
    "?aaaaini={anio}&aaaafin={anio}&tf={fondo}&fecconf={anio}0101"
)
FONDOS = ["A", "B", "C", "D", "E"]


def numero(texto: str) -> float | None:
    texto = texto.strip()
    return float(texto.replace(".", "").replace(",", ".")) if texto else None


def variacion(actual: float, anterior: float) -> float:
    return round((actual / anterior - 1) * 100, 2)


def leer_fondo(anio: int, fondo: str) -> tuple[list[str], list[list[str]]]:
    with urllib.request.urlopen(URL.format(anio=anio, fondo=fondo), timeout=60) as respuesta:
        lineas = respuesta.read().decode("latin-1").splitlines()
    encabezado = next(linea for linea in lineas if linea.startswith("Fecha;")).split(";")
    afps = [nombre for nombre in encabezado[1:] if nombre]
    filas = [linea.split(";") for linea in lineas if linea[:4] == str(anio)]
    return afps, filas


def generar(anio: int | None = None) -> dict:
    anio = anio or date.today().year
    fondos = []
    ultima_fecha = ""
    for fondo in FONDOS:
        afps, filas = leer_fondo(anio, fondo)
        primera, ultima = filas[0], filas[-1]
        hace_un_mes = (date.fromisoformat(ultima[0]) - timedelta(days=29)).isoformat()
        base_mes = next(fila for fila in filas if fila[0] >= hace_un_mes)
        ultima_fecha = ultima[0]

        rentabilidades = []
        for i, afp in enumerate(afps):
            columna = 1 + 2 * i  # cada AFP tiene "valor cuota" y "valor patrimonio"
            actual = numero(ultima[columna])
            inicio = numero(primera[columna])
            mes = numero(base_mes[columna])
            if actual and inicio and mes:
                rentabilidades.append(
                    {
                        "afp": afp.title(),
                        "anio": variacion(actual, inicio),
                        "mes": variacion(actual, mes),
                    }
                )
        fondos.append({"fondo": fondo, "afps": rentabilidades})

    print(f"  {len(fondos)} fondos al {ultima_fecha}")
    return {
        "fuente": "Superintendencia de Pensiones",
        "descargado_el": date.today().isoformat(),
        "dato_al": ultima_fecha,
        "provisional": True,
        "fondos": fondos,
    }


def series(foto: dict) -> list[Serie]:
    """Rentabilidad de cada AFP y fondo al día del dato: en el año y en los últimos 30 días."""
    resultado = []
    for fondo in foto["fondos"]:
        for afp in fondo["afps"]:
            for plazo, nombre in (("anio", "en el año"), ("mes", "en 30 días")):
                resultado.append(
                    Serie(
                        id=f"sp.rentabilidad_{plazo}.{fondo['fondo'].lower()}.{afp['afp'].lower()}",
                        nombre=f"Rentabilidad nominal {nombre}, AFP {afp['afp']}, fondo {fondo['fondo']}",
                        unidad="%",
                        frecuencia="diaria",
                        provisional=foto["provisional"],
                        observaciones=[(foto["dato_al"], afp[plazo])],
                    )
                )
    return resultado


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    Path(sys.argv[1]).write_text(json.dumps(generar(), ensure_ascii=False, indent=2), encoding="utf-8")
