from fastapi.testclient import TestClient

from app.main import app

cliente = TestClient(app)


def test_salud():
    respuesta = cliente.get("/salud")
    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert datos["estado"] == "ok"
    # En las pruebas todas las fotos vienen de los JSON de respaldo.
    assert set(datos["fotos"]) == {"bcch", "cne", "cmf", "odepa", "afp"}
    assert set(datos["fotos"].values()) == {"archivo"}


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


def test_impacto_financiero_suma_sus_rubros():
    impacto = cliente.get("/v1/home").json()["impacto"]
    rubros = impacto["rubros"]
    assert [r["id"] for r in rubros][-1] == "otros"
    assert abs(sum(r["gasto_mes"] for r in rubros) - impacto["gasto_mes"]) <= len(rubros)
    assert sum(r["diferencia_anual"] for r in rubros) == impacto["diferencia_anual"]
    # El gasto de la encuesta (2021-2022) llevado a hoy debe ser mayor que el original.
    assert impacto["gasto_mes"] > 1_590_105


def test_anclados_van_primero_en_el_inicio():
    cambios = cliente.get("/v1/home", params={"anclados": "cobre,huevos,no-existe"}).json()["cambios"]
    assert [c["id"] for c in cambios[:2]] == ["cobre", "huevos"]
    assert len(cambios) == 7
    assert len({c["id"] for c in cambios}) == 7


def test_todos_los_datos_ordenados_por_presion():
    datos = cliente.get("/v1/datos").json()
    orden = {"alta": 0, "media": 1, "baja": 2}
    niveles = [orden[d["presion"]] for d in datos]
    assert niveles == sorted(niveles)
    # Todos los alimentos de ODEPA, no solo el que más se movió.
    assert sum(d["tema"] == "alimentos" for d in datos) == 10


def test_tono_segun_direccion_y_efecto():
    datos = {d["id"]: d for d in cliente.get("/v1/datos").json()}
    for d in datos.values():
        if d["efecto"] == "neutro" or d["direccion"] == "estable":
            assert d["tono"] == "neutral"
        elif (d["direccion"] == "sube") == (d["efecto"] == "sube_bueno"):
            assert d["tono"] == "favorable"
        else:
            assert d["tono"] == "desfavorable"
    assert datos["dolar"]["efecto"] == "neutro"


def test_lo_que_cambio_ordena_por_movimiento():
    cambios = cliente.get("/v1/home").json()["cambios"]
    movimientos = [c["movimiento"] for c in cambios]
    assert movimientos == sorted(movimientos, reverse=True)
