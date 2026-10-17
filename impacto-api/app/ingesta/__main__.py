"""Ingesta diaria: descarga cada fuente y la guarda en Supabase (docs/ingesta.md).

Uso:
    python -m app.ingesta                 # todas las fuentes
    python -m app.ingesta bcch cne        # solo algunas
    python -m app.ingesta --json          # además actualiza los JSON de respaldo en app/datos_ejemplo

Por cada fuente: abre una corrida en `corridas_ingesta`, descarga, guarda las series y sus
observaciones (upsert: repetir no duplica), reemplaza la foto en `fotos` y cierra la corrida
con el número de filas o el error. Si una fuente falla, las demás siguen. Sale con código 1
si alguna falló, para que el cron lo marque.
"""

import json
import sys
import traceback
from datetime import UTC, datetime
from pathlib import Path

from app import supabase
from app.ingesta import afp, bcch, cmf, cne, odepa

CONECTORES = {c.ID: c for c in (bcch, cne, cmf, odepa, afp)}
RESPALDO = Path(__file__).resolve().parent.parent / "datos_ejemplo"


def _ahora() -> str:
    return datetime.now(UTC).isoformat()


def guardar(conector, foto: dict) -> int:
    """Guarda series, observaciones y la foto. Devuelve cuántas observaciones escribió."""
    series = conector.series(foto)
    supabase.guardar_lote(
        "series",
        [
            {
                "id": s.id,
                "fuente_id": conector.FUENTE_ID,
                "codigo": s.codigo,
                "nombre": s.nombre,
                "unidad": s.unidad,
                "frecuencia": s.frecuencia,
                "region": s.region,
                "metadatos": s.metadatos,
            }
            for s in series
        ],
        conflicto="id",
    )
    ahora = _ahora()
    # Una misma fecha repetida en la fuente haría fallar el upsert de la tanda: gana la última.
    unicas = {
        (s.id, f): {"serie_id": s.id, "fecha": f, "valor": v, "provisional": s.provisional, "actualizado_el": ahora}
        for s in series
        for f, v in s.observaciones
    }
    observaciones = list(unicas.values())
    supabase.guardar_lote("observaciones", observaciones, conflicto="serie_id,fecha")
    supabase.guardar(
        "fotos",
        {
            "id": conector.ID,
            "fuente_id": conector.FUENTE_ID,
            "contenido": foto,
            "descargado_el": foto["descargado_el"],
            "actualizado_el": ahora,
        },
        conflicto="id",
    )
    return len(observaciones)


def correr(conector, con_json: bool) -> bool:
    print(f"{conector.ID}: descargando...")
    corrida = supabase.insertar("corridas_ingesta", {"fuente_id": conector.FUENTE_ID})
    try:
        foto = conector.generar()
        filas = guardar(conector, foto)
        if con_json:
            (RESPALDO / conector.ARCHIVO).write_text(
                json.dumps(foto, ensure_ascii=False, separators=(",", ":")), encoding="utf-8"
            )
    except Exception as error:  # una fuente caída no debe frenar a las demás
        traceback.print_exc()
        supabase.actualizar(
            "corridas_ingesta",
            {"id": f"eq.{corrida['id']}"},
            {"fin": _ahora(), "estado": "error", "error": f"{type(error).__name__}: {error}"[:2000]},
        )
        print(f"{conector.ID}: ERROR {error}")
        return False
    supabase.actualizar(
        "corridas_ingesta", {"id": f"eq.{corrida['id']}"}, {"fin": _ahora(), "estado": "ok", "filas": filas}
    )
    print(f"{conector.ID}: ok, {filas} observaciones")
    return True


def main(argumentos: list[str]) -> int:
    con_json = "--json" in argumentos
    ids = [a for a in argumentos if not a.startswith("--")] or list(CONECTORES)
    desconocidos = [i for i in ids if i not in CONECTORES]
    if desconocidos:
        print(f"Fuentes desconocidas: {', '.join(desconocidos)}. Opciones: {', '.join(CONECTORES)}")
        return 2
    resultados = [correr(CONECTORES[i], con_json) for i in ids]
    return 0 if all(resultados) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
