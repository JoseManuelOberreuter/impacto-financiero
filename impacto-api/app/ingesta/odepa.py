"""Conector de ODEPA: precios al consumidor de alimentos.

Descarga el CSV anual de datos abiertos (datos.odepa.gob.cl, ~50 MB, se actualiza cada
semana) y calcula, por producto, la mediana semanal de la Región Metropolitana, el
desglose por tipo de local y la comparación entre regiones.

Uso suelto (solo escribe el JSON):
    python -m app.ingesta.odepa app/datos_ejemplo/odepa_snapshot.json [ruta/precio_consumidor_2026.csv]
"""

import csv
import io
import json
import statistics
import sys
import urllib.request
from collections import defaultdict
from collections.abc import Iterable
from datetime import date
from pathlib import Path

from app.ingesta import Serie

ID = "odepa"
FUENTE_ID = "odepa"
ARCHIVO = "odepa_snapshot.json"
# Conjunto "Precios al Consumidor" en el CKAN de ODEPA: un CSV por año.
CONJUNTO = "https://datos.odepa.gob.cl/api/3/action/package_show?id=d4646b7f-0d2e-4567-b6fa-932b1a6bb3f3"

REGION_BASE = "13"  # Región Metropolitana
SEMANAS_SERIE = 12
# El "supermercado en línea" tiene un solo punto: se excluye para no distorsionar.
TIPOS_EXCLUIDOS = {"Supermercado en Línea"}

PRODUCTOS = [
    # id, nombre visible, producto ODEPA, unidad ODEPA, unidad visible, categoría
    ("marraqueta", "Marraqueta", "Marraqueta", "$/kilo", "kilo", "Pan"),
    ("hallulla", "Hallulla", "Hallulla corriente", "$/kilo", "kilo", "Pan"),
    ("leche", "Leche entera", "Leche Fluida Entera", "$/Caja de 1 Litro", "litro", "Lácteos y huevos"),
    ("huevos", "Huevos", "Huevo blanco grande (primera)", "$/bandeja 30 unidades", "bandeja de 30", "Lácteos y huevos"),
    ("aceite", "Aceite vegetal", "Aceite vegetal", "$/botella 900 ml", "botella 900 ml", "Despensa"),
    ("arroz", "Arroz", "Arroz grano ancho grado 2", "$/kilo", "kilo", "Despensa"),
    ("pollo", "Pollo entero", "Pollo Entero", "$/kilo", "kilo", "Carnes"),
    ("posta", "Posta rosada", "Posta Rosada", "$/kilo", "kilo", "Carnes"),
    ("papa", "Papa", "Papa|Asterix|Primera", "$/kilo", "kilo", "Verduras"),
    ("tomate", "Tomate", "Tomate|Larga vida|Primera", "$/kilo", "kilo", "Verduras"),
]


def numero(texto: str) -> float:
    return float(texto.replace(",", "."))


def variacion(actual: float, anterior: float) -> float:
    return round((actual / anterior - 1) * 100, 1) if anterior else 0.0


def url_csv(anio: int) -> str:
    with urllib.request.urlopen(CONJUNTO, timeout=60) as respuesta:
        recursos = json.loads(respuesta.read())["result"]["resources"]
    return next(r["url"] for r in recursos if r["url"].endswith(f"precio_consumidor_{anio}.csv"))


def filas_csv(ruta_csv: str | None = None) -> Iterable[dict]:
    """Lee el CSV fila a fila (de un archivo o descargándolo), sin cargarlo entero en memoria."""
    if ruta_csv:
        with open(ruta_csv, encoding="utf-8-sig") as archivo:
            yield from csv.DictReader(archivo)
        return
    with urllib.request.urlopen(url_csv(date.today().year), timeout=300) as respuesta:
        yield from csv.DictReader(io.TextIOWrapper(respuesta, encoding="utf-8-sig"))


def generar(ruta_csv: str | None = None) -> dict:
    filas = filas_csv(ruta_csv)

    # (producto, unidad) → semana → región → [(tipo, precio)]
    datos: dict = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    nombres_region = {}
    for fila in filas:
        if fila["Tipo de punto monitoreo"] in TIPOS_EXCLUIDOS:
            continue
        clave = (fila["Producto"], fila["Unidad"])
        datos[clave][fila["Fecha termino"]][fila["ID region"]].append(
            (fila["Tipo de punto monitoreo"], numero(fila["Precio promedio"]))
        )
        nombres_region[fila["ID region"]] = (
            fila["Region"]
            .replace("Región Metropolitana de Santiago", "Metropolitana")
            .replace("Región de ", "")
            .replace("Región del ", "")
        )

    productos = []
    for id_, nombre, producto, unidad, unidad_visible, categoria in PRODUCTOS:
        semanas = datos[(producto, unidad)]
        fechas = sorted(f for f in semanas if semanas[f].get(REGION_BASE))
        if not fechas:
            print(f"Sin datos para {producto} ({unidad})", file=sys.stderr)
            continue

        def mediana_rm(fecha: str) -> float:
            return statistics.median(p for _, p in semanas[fecha][REGION_BASE])

        ultima = fechas[-1]
        precio = mediana_rm(ultima)

        por_tipo: dict = defaultdict(list)
        for tipo, valor in semanas[ultima][REGION_BASE]:
            por_tipo[tipo].append(valor)

        productos.append(
            {
                "id": id_,
                "nombre": nombre,
                "unidad": unidad_visible,
                "categoria": categoria,
                "precio": round(precio),
                "variacion_semanal": variacion(precio, mediana_rm(fechas[-2])) if len(fechas) > 1 else 0.0,
                "variacion_anual": variacion(precio, mediana_rm(fechas[0])),
                "puntos_de_venta": len(semanas[ultima][REGION_BASE]),
                "serie": [
                    {"semana": f, "precio": round(mediana_rm(f))} for f in fechas[-SEMANAS_SERIE:]
                ],
                "por_tipo_local": [
                    {"tipo": tipo, "precio": round(statistics.median(valores))}
                    for tipo, valores in sorted(por_tipo.items())
                ],
                "por_region": sorted(
                    (
                        {
                            "region": nombres_region[region],
                            "precio": round(statistics.median(p for _, p in puntos)),
                        }
                        for region, puntos in semanas[ultima].items()
                    ),
                    key=lambda r: r["precio"],
                ),
                "dato_al": ultima,
            }
        )

    if not productos:
        raise RuntimeError("El CSV de ODEPA no trajo ningún producto")
    print(f"  {len(productos)} productos, al {max(p['dato_al'] for p in productos)}")
    return {"fuente": "ODEPA", "descargado_el": date.today().isoformat(), "productos": productos}


def series(foto: dict) -> list[Serie]:
    """Mediana semanal en la Región Metropolitana de cada producto (las últimas semanas de la foto)."""
    return [
        Serie(
            id=f"odepa.{p['id']}",
            nombre=p["nombre"],
            unidad=p["unidad"],
            frecuencia="semanal",
            region=REGION_BASE,
            observaciones=[(s["semana"], s["precio"]) for s in p["serie"]],
            metadatos={"categoria": p["categoria"]},
        )
        for p in foto["productos"]
    ]


if __name__ == "__main__":
    if len(sys.argv) not in (2, 3):
        raise SystemExit(__doc__)
    foto = generar(sys.argv[2] if len(sys.argv) == 3 else None)
    Path(sys.argv[1]).write_text(json.dumps(foto, ensure_ascii=False, indent=2), encoding="utf-8")
