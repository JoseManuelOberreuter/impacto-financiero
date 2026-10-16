from fastapi.testclient import TestClient

from app.main import app

cliente = TestClient(app)


def test_salud():
    respuesta = cliente.get("/salud")
    assert respuesta.status_code == 200
    assert respuesta.json() == {"estado": "ok"}


def test_home_entrega_termometros_por_defecto_validos():
    respuesta = cliente.get("/v1/home")
    assert respuesta.status_code == 200
    datos = respuesta.json()

    ids = {t["id"] for t in datos["termometros"]}
    assert set(datos["termometros_por_defecto"]) <= ids
    assert len(datos["termometros_por_defecto"]) <= datos["max_termometros_home"]
    assert datos["datos_de_ejemplo"] is True


def test_cambios_enlazan_a_su_detalle_y_tienen_serie():
    cambios = cliente.get("/v1/home").json()["cambios"]
    # Un dato por tema: bencina, gas, dólar, UF, tasa máxima, cobre y el alimento que más se movió.
    assert len(cambios) == 7
    assert sum(c["enlace"].startswith("/precios/") for c in cambios) == 1
    for cambio in cambios:
        assert len(cambio["serie"]) >= 2
        assert cliente.get("/v1" + cambio["enlace"]).status_code == 200
