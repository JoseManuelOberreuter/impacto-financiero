"""Genera una foto (snapshot) de precios al consumidor de ODEPA para la API.

Primer borrador del conector de ODEPA: lee el CSV anual de datos abiertos y
calcula, por producto, la mediana semanal de la Región Metropolitana, el
desglose por tipo de local y la comparación entre regiones.

Uso:
    python scripts/snapshot_odepa.py ruta/precio_consumidor_2026.csv app/datos_ejemplo/odepa_snapshot.json

El CSV se descarga desde datos.odepa.gob.cl (ver docs/fuentes-de-datos.md).
"""

import csv
import json
import statistics
import sys
from collections import defaultdict

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


def main(ruta_csv: str, ruta_salida: str) -> None:
    with open(ruta_csv, encoding="utf-8-sig") as archivo:
        filas = list(csv.DictReader(archivo))

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

    with open(ruta_salida, "w", encoding="utf-8") as salida:
        json.dump({"fuente": "ODEPA", "productos": productos}, salida, ensure_ascii=False, indent=2)
    print(f"{len(productos)} productos -> {ruta_salida}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
