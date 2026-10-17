from fastapi.testclient import TestClient

from app.datos_ejemplo import cne
from app.ingesta import cne as snapshot_cne
from app.main import app

cliente = TestClient(app)


def test_numeros_de_la_cne():
    assert snapshot_cne.numero("2.372,00") == 2372.0
    assert snapshot_cne.numero("1594,3023") == 1594.3023
    assert snapshot_cne.numero("586.000") == 586.0
    assert snapshot_cne.numero("gasolina_95_sp") is None


def test_bencina_y_gas_son_reales():
    energia = {r["id"]: r for r in cliente.get("/v1/precios").json()["energia_y_transporte"]}
    assert energia["bencina95"]["precio"] == round(cne.hoy("bencina95")["mediana"])
    assert not energia["bencina95"]["de_ejemplo"]
    assert not energia["gas15"]["de_ejemplo"]


def test_bencina_en_bolsillo_tiene_historia():
    detalle = cliente.get("/v1/termometros/bolsillo").json()
    bencina = next(i for i in detalle["indicadores"] if i["id"] == "bencina")
    assert len(bencina["serie"]) > 1
    assert bencina["banda_normal"]
