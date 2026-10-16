from fastapi.testclient import TestClient

from app import planes
from app.main import app
from app.modelos.planes import Plan

cliente = TestClient(app)


def test_modo_abierto_por_defecto_activa_todo(monkeypatch):
    monkeypatch.delenv("MODO_PLANES", raising=False)
    datos = cliente.get("/v1/yo/capacidades").json()
    assert datos["modo"] == "abierto"
    assert datos["plan"] == "gratis"
    assert all(c["activa"] for c in datos["capacidades"].values())
    assert datos["capacidades"]["mi_impacto"]["plan_minimo"] == "pro"


def test_modo_activo_respeta_el_plan(monkeypatch):
    monkeypatch.setenv("MODO_PLANES", "activo")
    assert planes.puede("termometros.basico")
    assert not planes.puede("mi_impacto")
    assert planes.puede("mi_impacto", Plan.pro)
    assert not planes.puede("mi_rubro", Plan.pro)
    assert planes.puede("mi_rubro", Plan.empresas)


def test_limites_por_plan(monkeypatch):
    monkeypatch.setenv("MODO_PLANES", "activo")
    assert planes.capacidades(Plan.pro).capacidades["alertas"].limite == 10
    assert planes.capacidades(Plan.empresas).capacidades["alertas"].limite == 50
    # Sin el plan, se informa el límite del plan mínimo para mostrarlo en el BloquePro.
    gratis = planes.capacidades(Plan.gratis).capacidades["alertas"]
    assert not gratis.activa and gratis.limite == 10


def test_vista_previa_activa_todo(monkeypatch):
    monkeypatch.setenv("MODO_PLANES", "vista_previa")
    assert planes.puede("mi_rubro")


def test_referencias_de_mi_impacto():
    datos = cliente.get("/v1/mi-impacto/referencias").json()
    uf = datos["uf"]
    assert uf["ultima_publicada"]["fecha"] >= uf["hoy"]["fecha"]
    assert uf["hace_un_anio"]["valor"] < uf["hoy"]["valor"]
    assert datos["bencina95"]["hoy"]["valor"] > 0
    assert datos["bencina95"]["hace_un_anio"]["fecha"] < datos["bencina95"]["hoy"]["fecha"]
