"""Impacto Financiero: la inflación en pesos para un hogar típico de Santiago.

Metodología completa en docs/impacto-financiero.md:
1. El gasto de un hogar típico sale de la IX Encuesta de Presupuestos Familiares
   del INE (oct-2021 a sep-2022): gasto promedio del Gran Santiago por rubro,
   calculado con sus microdatos (scripts/resumen_epf.py).
2. Ese gasto se lleva a precios de hoy con el IPC general.
3. Cuánto más cuesta que hace un año se calcula por partes. Las partes que tienen
   datos frecuentes se mueven con ellos (por eso la cifra cambia durante el mes):
   - bencina y diésel, con el precio de hoy de la CNE;
   - arriendo, con la UF de hoy (los arriendos se pactan en UF);
   - gas licuado, con el último promedio mensual de la CNE.
   El resto de cada rubro se mueve con el IPC del rubro, y lo que no es comida,
   vivienda ni transporte, con el IPC general.
"""

import json
from datetime import date
from pathlib import Path

from app.datos_ejemplo import banco_central as bc
from app.datos_ejemplo import cne
from app.modelos.impacto import ImpactoFinanciero, RubroImpacto

# Resultados de la IX EPF (INE) con sus fuentes y el resumen de microdatos: epf_ix.json.
EPF = json.loads((Path(__file__).parent / "epf_ix.json").read_text(encoding="utf-8"))
EPF_DESDE = date.fromisoformat(EPF["periodo"]["desde"])
EPF_HASTA = date.fromisoformat(EPF["periodo"]["hasta"])
_SANTIAGO = EPF["gran_santiago_microdatos"]
GASTO_EPF_SANTIAGO = _SANTIAGO["gasto_promedio"]
_DIVISION = {d: v["gasto"] for d, v in _SANTIAGO["divisiones"].items()}
_COMPONENTE = {c: v["gasto"] for c, v in _SANTIAGO["componentes"].items()}

# id: (nombre, gasto en la EPF, serie de IPC para lo que no tiene dato frecuente)
RUBROS = {
    "alimentos": ("Comida", _DIVISION["01"], "ipc_alimentos"),
    "vivienda": ("Vivienda, luz, agua y gas", _DIVISION["04"], "ipc_vivienda"),
    "transporte": ("Transporte", _DIVISION["07"], "ipc_transporte"),
    "otros": ("Todo lo demás", GASTO_EPF_SANTIAGO - _DIVISION["01"] - _DIVISION["04"] - _DIVISION["07"], "ipc_indice"),
}


def _variacion(serie: bc.Serie, meses: int) -> float:
    """Variación del índice entre el último dato y `meses` antes."""
    actual = serie.ultimo
    objetivo = actual.fecha.replace(year=actual.fecha.year - (meses // 12))
    if meses % 12:
        mes = actual.fecha.month - meses % 12
        objetivo = objetivo.replace(year=objetivo.year - (mes <= 0), month=(mes - 1) % 12 + 1)
    anterior = next(p for p in reversed(serie.puntos) if p.fecha <= objetivo)
    return actual.valor / anterior.valor - 1


def _actualizacion_epf() -> float:
    """Cuánto subieron los precios desde la encuesta (promedio de su período) hasta hoy."""
    ipc = bc.SERIES["ipc_indice"]
    base = [p.valor for p in ipc.puntos if EPF_DESDE <= p.fecha <= EPF_HASTA]
    return ipc.ultimo.valor / (sum(base) / len(base))


def _mensual_hace_un_anio(datos: list[tuple[date, float]], fecha: date) -> float:
    """Valor del mes de hace un año o, si falta, el mes anterior más cercano."""
    objetivo = fecha.replace(year=fecha.year - 1, day=1)
    return next(v for f, v in reversed(datos) if f <= objetivo)


def _partes_frecuentes() -> dict[str, list[tuple[str, float, float, date]]]:
    """Por rubro: (parte, gasto en la EPF, variación en 12 meses, fecha del dato)."""
    bencina_hoy = cne.hoy("bencina95")["mediana"]
    bencina_antes = _mensual_hace_un_anio(cne.mensual("bencina95"), cne.DESCARGADO_EL)
    uf = bc.SERIES["uf"]
    gas = cne.mensual("glp15_corriente")
    gas_fecha, gas_hoy = gas[-1]
    return {
        "transporte": [
            ("combustibles", _COMPONENTE["gasolina"] + _COMPONENTE["diesel"],
             bencina_hoy / bencina_antes - 1, cne.DESCARGADO_EL),
        ],
        "vivienda": [
            ("arriendo", _COMPONENTE["arriendo"], uf.ultimo.valor / uf.antes_de(365).valor - 1, uf.ultimo.fecha),
            ("gas", _COMPONENTE["gas"], gas_hoy / _mensual_hace_un_anio(gas, gas_fecha) - 1, gas_fecha),
        ],
    }


def impacto() -> ImpactoFinanciero:
    actualizacion = _actualizacion_epf()
    frecuentes = _partes_frecuentes()
    fechas = [bc.SERIES["ipc_indice"].ultimo.fecha]
    rubros = []
    for id_, (nombre, gasto_epf, serie) in RUBROS.items():
        gasto = gasto_epf * actualizacion
        partes = frecuentes.get(id_, [])
        resto = gasto_epf - sum(p[1] for p in partes)
        # Cada parte: gasto de hoy y su variación en 12 meses.
        piezas = [(resto * actualizacion, _variacion(bc.SERIES[serie], 12))]
        for _, gasto_parte, variacion, fecha in partes:
            piezas.append((gasto_parte * actualizacion, variacion))
            fechas.append(fecha)
        anual = sum(g - g / (1 + v) for g, v in piezas)
        mensual = gasto - gasto / (1 + _variacion(bc.SERIES[serie], 1))
        rubros.append(
            RubroImpacto(
                id=id_,
                nombre=nombre,
                gasto_mes=round(gasto),
                diferencia_anual=round(anual),
                diferencia_mensual=round(mensual),
                variacion_anual=round(anual / (gasto - anual) * 100, 1),
            )
        )
    total = sum(r.gasto_mes for r in rubros)
    diferencia = sum(r.diferencia_anual for r in rubros)
    return ImpactoFinanciero(
        periodo=bc.SERIES["ipc_indice"].ultimo.fecha,
        actualizado_al=min(max(fechas), date.today()),
        hogar="un hogar típico de Santiago",
        gasto_mes=total,
        diferencia_anual=diferencia,
        variacion_anual=round(diferencia / (total - diferencia) * 100, 1),
        diferencia_mensual=sum(r.diferencia_mensual for r in rubros),
        # Los rubros con nombre, de mayor a menor alza; "Todo lo demás" siempre al final.
        rubros=sorted(rubros, key=lambda r: (r.id == "otros", -r.diferencia_anual)),
        fuente="INE (Encuesta de Presupuestos Familiares e IPC), Banco Central y CNE",
        metodologia=(
            "Gasto de un hogar promedio del Gran Santiago según la IX Encuesta de Presupuestos "
            "Familiares del INE, llevado a precios de hoy con el IPC. La diferencia con hace un año "
            "usa la bencina y el gas de la CNE, la UF para el arriendo y el IPC de cada rubro para "
            "el resto. Indicador propio de referencia."
        ),
    )
