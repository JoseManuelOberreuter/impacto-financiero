from fastapi.testclient import TestClient

from app.main import app

cliente = TestClient(app)


def _indicadores(termometro: str) -> dict:
    detalle = cliente.get(f"/v1/termometros/{termometro}").json()
    return {i["id"]: i for i in detalle["indicadores"]}


def test_deudas_incluye_la_tasa_maxima_de_la_cmf():
    tmc = _indicadores("deudas")["tmc"]
    assert tmc["fuente"] == "CMF"
    assert len(tmc["serie"]) == 12


def test_animo_usa_ipec_e_imce():
    assert set(_indicadores("animo")) == {"ipec", "imce"}


def test_ningun_termometro_tiene_indicadores_de_ejemplo():
    for termometro in cliente.get("/v1/termometros").json():
        for indicador in _indicadores(termometro["id"]).values():
            assert indicador["fuente"] != "Cálculo propio sobre titulares de prensa"
