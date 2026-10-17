"""Impacto Financiero: la inflación en pesos para un hogar típico de Santiago.

Metodología completa en docs/impacto-financiero.md:
1. El gasto de un hogar típico sale de la IX Encuesta de Presupuestos Familiares
   del INE (oct-2021 a sep-2022): gasto promedio del Gran Santiago y la
   proporción de cada rubro.
2. Ese gasto se lleva a precios de hoy con el IPC general.
3. Cuánto más cuesta que hace un año (y que el mes anterior) se calcula con el
   IPC de cada rubro: alimentos, vivienda y servicios básicos, y transporte. El
   resto del gasto usa el IPC general.
"""

import json
from datetime import date
from pathlib import Path

from app.datos_ejemplo import banco_central as bc
from app.modelos.impacto import ImpactoFinanciero, RubroImpacto

# Resultados publicados de la IX EPF (INE), guardados con sus fuentes en epf_ix.json.
EPF = json.loads((Path(__file__).parent / "epf_ix.json").read_text(encoding="utf-8"))
GASTO_EPF_SANTIAGO = EPF["gasto_mensual_promedio"]["gran_santiago"]
EPF_DESDE = date.fromisoformat(EPF["periodo"]["desde"])
EPF_HASTA = date.fromisoformat(EPF["periodo"]["hasta"])
_ESTRUCTURA = EPF["estructura_gasto_por_division"]
_ALIMENTOS = _ESTRUCTURA["alimentos_y_bebidas_no_alcoholicas"] / 100
_VIVIENDA = _ESTRUCTURA["vivienda_agua_electricidad_gas_y_combustibles"] / 100
_TRANSPORTE = _ESTRUCTURA["transporte"] / 100

# id: (nombre, proporción del gasto según la IX EPF, serie de IPC que lo mueve)
RUBROS = {
    "alimentos": ("Comida", _ALIMENTOS, "ipc_alimentos"),
    "vivienda": ("Vivienda, luz, agua y gas", _VIVIENDA, "ipc_vivienda"),
    "transporte": ("Transporte", _TRANSPORTE, "ipc_transporte"),
    "otros": ("Todo lo demás", 1 - _ALIMENTOS - _VIVIENDA - _TRANSPORTE, "ipc_indice"),
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


def impacto() -> ImpactoFinanciero:
    gasto_hoy = GASTO_EPF_SANTIAGO * _actualizacion_epf()
    rubros = []
    for id_, (nombre, proporcion, serie) in RUBROS.items():
        gasto = gasto_hoy * proporcion
        anual = _variacion(bc.SERIES[serie], 12)
        mensual = _variacion(bc.SERIES[serie], 1)
        rubros.append(
            RubroImpacto(
                id=id_,
                nombre=nombre,
                gasto_mes=round(gasto),
                diferencia_anual=round(gasto - gasto / (1 + anual)),
                diferencia_mensual=round(gasto - gasto / (1 + mensual)),
                variacion_anual=round(anual * 100, 1),
            )
        )
    total = sum(r.gasto_mes for r in rubros)
    diferencia = sum(r.diferencia_anual for r in rubros)
    return ImpactoFinanciero(
        periodo=bc.SERIES["ipc_indice"].ultimo.fecha,
        hogar="un hogar típico de Santiago",
        gasto_mes=total,
        diferencia_anual=diferencia,
        variacion_anual=round(diferencia / (total - diferencia) * 100, 1),
        diferencia_mensual=sum(r.diferencia_mensual for r in rubros),
        # Los rubros con nombre, de mayor a menor alza; "Todo lo demás" siempre al final.
        rubros=sorted(rubros, key=lambda r: (r.id == "otros", -r.diferencia_anual)),
        fuente="INE (Encuesta de Presupuestos Familiares e IPC), vía Banco Central",
        metodologia=(
            "Gasto de un hogar promedio del Gran Santiago según la IX Encuesta de Presupuestos "
            "Familiares del INE, llevado a precios de hoy con el IPC. La diferencia con hace un año "
            "usa el IPC de cada rubro. Indicador propio de referencia."
        ),
    )
