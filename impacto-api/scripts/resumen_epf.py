"""Resume la base de gastos de la IX EPF (INE) para el Impacto Financiero.

La base completa pesa ~145 MB y no va al repo: se descarga a .cache/epf/ (ignorada
por git) y este script guarda en epf_ix.json solo el resumen del Gran Santiago:
gasto promedio por división y de los productos que podemos seguir con datos más
frecuentes (bencina, gas, arriendo, alimentos de ODEPA).

Descarga (desde la página de la EPF del INE → Bases de datos → IX EPF):
    base-gastos-ix-epf-(formato-csv).csv → .cache/epf/gastos.csv

Uso:
    python scripts/resumen_epf.py .cache/epf/gastos.csv app/datos_ejemplo/epf_ix.json

Criterios (verificados contra los resultados publicados por el INE):
- Se excluyen los arriendos imputados (CCIF 04.2): con eso el promedio del Gran
  Santiago da $1.590.105, igual que la publicación.
- La macrozona 2 es el Gran Santiago (1 norte, 3 centro, 4 sur).
- Promedios ponderados con el factor de expansión (columna fe).
"""

import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

GRAN_SANTIAGO = "2"
ARRIENDO_IMPUTADO = "04.2"

DIVISIONES = {
    "01": "Alimentos y bebidas no alcohólicas",
    "02": "Bebidas alcohólicas y tabaco",
    "03": "Vestuario y calzado",
    "04": "Vivienda, agua, electricidad, gas y otros combustibles",
    "05": "Muebles y mantención del hogar",
    "06": "Salud",
    "07": "Transporte",
    "08": "Información y comunicaciones",
    "09": "Recreación, deporte y cultura",
    "10": "Educación",
    "11": "Restaurantes y alojamiento",
    "12": "Seguros y servicios financieros",
    "13": "Cuidado personal y otros",
}

# Componentes que seguimos con datos frecuentes: id -> prefijos CCIF que suma.
COMPONENTES = {
    "gasolina": ["07.2.2.02"],
    "diesel": ["07.2.2.01"],
    "gas": ["04.5.2"],
    "electricidad": ["04.5.1"],
    "arriendo": ["04.1.1"],
    "transporte_publico": ["07.3"],
    # Alimentos que mide ODEPA (id del producto en odepa_snapshot.json).
    "pan": ["01.1.1.03.01"],
    "leche": ["01.1.4.01.01"],
    "huevos": ["01.1.4.08.01"],
    "aceite": ["01.1.5.01.01"],
    "arroz": ["01.1.1.01.01"],
    "pollo": ["01.1.2.02.18", "01.1.2.02.19", "01.1.2.02.20", "01.1.2.02.21", "01.1.2.02.22"],
    "posta": ["01.1.2.02.04"],
    "papa": ["01.1.7.05.01"],
    "tomate": ["01.1.7.02.07"],
}


def numero(texto: str) -> float | None:
    try:
        return float(texto.replace(",", "."))
    except ValueError:
        return None


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    gastos, salida = Path(sys.argv[1]), Path(sys.argv[2])

    factor: dict[str, float] = {}
    por_division: dict[str, float] = defaultdict(float)
    por_componente: dict[str, float] = defaultdict(float)
    with gastos.open(encoding="utf-8-sig", newline="") as archivo:
        for fila in csv.DictReader(archivo, delimiter=";"):
            if fila["macrozona"] != GRAN_SANTIAGO or fila["ccif"].startswith(ARRIENDO_IMPUTADO):
                continue
            fe, gasto = numero(fila["fe"]), numero(fila["gasto"])
            if fe is None or gasto is None:
                continue
            factor[fila["folio"]] = fe
            por_division[fila["d"]] += fe * gasto
            for id_, prefijos in COMPONENTES.items():
                if any(fila["ccif"].startswith(p) for p in prefijos):
                    por_componente[id_] += fe * gasto

    hogares = sum(factor.values())
    total = sum(por_division.values())
    resumen = {
        "nota": (
            "Calculado con scripts/resumen_epf.py sobre la base de gastos de la IX EPF. "
            "Gran Santiago (macrozona 2), sin arriendos imputados, ponderado por el factor de expansión. "
            "Montos en pesos de oct-2021 a sep-2022 por hogar y por mes."
        ),
        "hogares_expandidos": round(hogares),
        "gasto_promedio": round(total / hogares),
        "divisiones": {
            d: {"nombre": DIVISIONES.get(d, d), "gasto": round(v / hogares), "porcentaje": round(v / total * 100, 2)}
            for d, v in sorted(por_division.items())
            if d in DIVISIONES
        },
        "componentes": {
            id_: {"ccif": COMPONENTES[id_], "gasto": round(por_componente[id_] / hogares)} for id_ in COMPONENTES
        },
    }

    datos = json.loads(salida.read_text(encoding="utf-8"))
    datos["gran_santiago_microdatos"] = resumen
    salida.write_text(json.dumps(datos, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Gran Santiago: {resumen['hogares_expandidos']:,} hogares, gasto promedio ${resumen['gasto_promedio']:,}")
    for d, v in resumen["divisiones"].items():
        print(f"  {d} {v['nombre'][:45]:<45} {v['porcentaje']:>5} %  ${v['gasto']:,}")
    for id_, v in resumen["componentes"].items():
        print(f"  {id_:<20} ${v['gasto']:,}")


if __name__ == "__main__":
    main()
