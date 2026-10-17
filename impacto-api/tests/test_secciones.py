from fastapi.testclient import TestClient

from app.main import app

cliente = TestClient(app)


def test_cada_termometro_tiene_detalle():
    termometros = cliente.get("/v1/termometros").json()
    assert len(termometros) == 7
    for t in termometros:
        detalle = cliente.get(f"/v1/termometros/{t['id']}")
        assert detalle.status_code == 200
        assert detalle.json()["indicadores"]


def test_termometro_inexistente_da_404():
    assert cliente.get("/v1/termometros/no-existe").status_code == 404


def test_canasta_coincide_con_su_composicion():
    canasta = cliente.get("/v1/precios").json()["canasta"]
    assert sum(item["costo"] for item in canasta["composicion"]) == canasta["total"]
    assert canasta["serie"][-1]["precio"] == canasta["total"]


def test_cada_producto_tiene_detalle_y_region_ordenada():
    productos = cliente.get("/v1/precios").json()["productos"]
    assert productos
    for p in productos:
        detalle = cliente.get(f"/v1/precios/{p['id']}").json()
        precios_region = [r["precio"] for r in detalle["por_region"]]
        assert precios_region == sorted(precios_region)


def test_home_usa_la_misma_canasta_que_precios():
    home = cliente.get("/v1/home").json()
    precios = cliente.get("/v1/precios").json()
    assert home["canasta"] == precios["canasta"]


def test_noticias_y_herramientas_responden():
    assert cliente.get("/v1/noticias").json()["temas"]
    herramientas = cliente.get("/v1/herramientas").json()
    assert {f["fondo"] for f in herramientas["mi_afp"]["fondos"]} == set("ABCDE")
