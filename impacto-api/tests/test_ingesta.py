import json
from pathlib import Path

import pytest

from app import fotos, supabase
from app.ingesta import __main__ as ingesta
from app.ingesta import afp, bcch, cmf, cne, odepa

RESPALDO = Path(__file__).parent.parent / "app" / "datos_ejemplo"


def _foto(conector) -> dict:
    return json.loads((RESPALDO / conector.ARCHIVO).read_text(encoding="utf-8"))


@pytest.mark.parametrize("conector", [bcch, cne, cmf, odepa, afp])
def test_cada_foto_se_convierte_en_series(conector):
    series = conector.series(_foto(conector))
    assert series
    frecuencias = {"diaria", "semanal", "mensual", "trimestral", "anual"}
    for serie in series:
        assert serie.id.split(".")[0] in {"bcch", "cne", "cmf", "odepa", "sp"}
        assert serie.frecuencia in frecuencias
        assert serie.observaciones
        assert all(isinstance(v, (int, float)) for _, v in serie.observaciones)
    assert len({s.id for s in series}) == len(series)


def test_series_del_banco_central_y_la_cne():
    dolar = next(s for s in bcch.series(_foto(bcch)) if s.id == "bcch.dolar")
    assert dolar.frecuencia == "diaria" and dolar.codigo == "F073.TCO.PRE.Z.D"
    ids = {s.id for s in cne.series(_foto(cne))}
    # La región va sin cero a la izquierda, igual en la historia mensual y en las estaciones.
    assert "cne.bencina95.13" in ids and "cne.estaciones.bencina95.13" in ids
    assert "cne.estaciones.bencina95.1" in ids and "cne.estaciones.bencina95.pais" in ids


def test_la_ingesta_guarda_series_observaciones_y_foto(monkeypatch):
    guardado = {}
    monkeypatch.setattr(supabase, "guardar_lote", lambda tabla, filas, conflicto: guardado.setdefault(tabla, filas))
    monkeypatch.setattr(supabase, "guardar", lambda tabla, fila, conflicto: guardado.setdefault(tabla, fila))
    foto = _foto(cmf)
    filas = ingesta.guardar(cmf, foto)
    assert filas == len(guardado["observaciones"]) > 0
    assert {o["serie_id"] for o in guardado["observaciones"]} == {s["id"] for s in guardado["series"]}
    assert guardado["fotos"]["id"] == "cmf" and guardado["fotos"]["contenido"] is foto


def test_una_fuente_que_falla_no_frena_a_las_demas(monkeypatch):
    cambios = []
    monkeypatch.setattr(supabase, "insertar", lambda tabla, fila: {"id": 1})
    monkeypatch.setattr(supabase, "actualizar", lambda tabla, filtros, c: cambios.append(c))

    def falla():
        raise RuntimeError("fuente caída")

    monkeypatch.setattr(cmf, "generar", falla)
    assert ingesta.correr(cmf, con_json=False) is False
    assert cambios[-1]["estado"] == "error" and "fuente caída" in cambios[-1]["error"]


def test_fotos_usa_supabase_y_si_falla_el_respaldo(monkeypatch):
    monkeypatch.setenv("FOTOS_DESDE", "supabase")
    monkeypatch.setattr(
        supabase, "seleccionar", lambda tabla, filtros, columnas: [{"contenido": {"de": "supabase"}, "actualizado_el": "v2"}]
    )
    assert fotos.leer("cmf") == {"de": "supabase"}
    assert fotos.en_uso()["cmf"] == "v2"

    def sin_conexion(*_):
        raise supabase.SinConfiguracion("sin claves")

    monkeypatch.setattr(supabase, "seleccionar", sin_conexion)
    assert fotos.leer("cmf") == _foto(cmf)
    assert fotos.en_uso()["cmf"] == "archivo"


def test_hay_nuevas_compara_versiones(monkeypatch):
    monkeypatch.setenv("FOTOS_DESDE", "supabase")
    monkeypatch.setitem(fotos._en_uso, "cmf", "v1")
    monkeypatch.setattr(supabase, "seleccionar", lambda *_: [{"id": "cmf", "actualizado_el": "v1"}])
    assert not fotos.hay_nuevas()
    monkeypatch.setattr(supabase, "seleccionar", lambda *_: [{"id": "cmf", "actualizado_el": "v2"}])
    assert fotos.hay_nuevas()


def test_recargar_vuelve_a_armar_los_datos():
    from fastapi.testclient import TestClient

    from app.main import app

    antes = TestClient(app).get("/v1/home").json()
    fotos.recargar()
    assert TestClient(app).get("/v1/home").json() == antes
