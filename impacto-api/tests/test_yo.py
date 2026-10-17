from fastapi.testclient import TestClient

from app import supabase
from app.main import app

cliente = TestClient(app)
TOKEN = {"Authorization": "Bearer token-de-prueba"}
USUARIO = {"id": "u-1", "email": "ana@ejemplo.cl", "email_confirmed_at": "2026-10-16", "user_metadata": {"nombre": "Ana"}}


def _sin_supabase(monkeypatch, usuario=USUARIO, suscripciones=(), preferencias=()):
    """Reemplaza Supabase por datos en memoria: los tests no tocan la base real."""
    guardadas = {}
    borrados = []
    monkeypatch.setattr(supabase, "usuario_desde_token", lambda token: usuario)

    def seleccionar(tabla, filtros, columnas="*"):
        return list(suscripciones) if tabla == "suscripciones" else list(preferencias)

    def guardar(tabla, fila, conflicto):
        guardadas[tabla] = fila
        return fila

    monkeypatch.setattr(supabase, "seleccionar", seleccionar)
    monkeypatch.setattr(supabase, "guardar", guardar)
    monkeypatch.setattr(supabase, "borrar_usuario", lambda id_: borrados.append(id_))
    return guardadas, borrados


def test_sin_sesion_capacidades_gratis_y_lo_demas_pide_iniciar_sesion():
    assert cliente.get("/v1/yo/capacidades").json()["plan"] == "gratis"
    assert cliente.get("/v1/yo").status_code == 401
    assert cliente.get("/v1/yo/preferencias").status_code == 401


def test_token_invalido_da_401(monkeypatch):
    _sin_supabase(monkeypatch, usuario=None)
    assert cliente.get("/v1/yo", headers=TOKEN).status_code == 401


def test_yo_con_plan_pro(monkeypatch):
    _sin_supabase(monkeypatch, suscripciones=[{"plan_id": "pro"}])
    datos = cliente.get("/v1/yo", headers=TOKEN).json()
    assert datos == {"id": "u-1", "correo": "ana@ejemplo.cl", "verificado": True, "nombre": "Ana", "plan": "pro"}


def test_guardar_y_leer_preferencias(monkeypatch):
    guardadas, _ = _sin_supabase(monkeypatch)
    respuesta = cliente.put("/v1/yo/preferencias", headers=TOKEN, json={"anclados": ["dolar", "uf"]})
    assert respuesta.status_code == 200
    assert guardadas["preferencias"]["usuario_id"] == "u-1"
    assert guardadas["preferencias"]["anclados"] == ["dolar", "uf"]


def test_preferencias_invalidas_se_rechazan(monkeypatch):
    _sin_supabase(monkeypatch)
    assert cliente.put("/v1/yo/preferencias", headers=TOKEN, json={"apariencia": "rosado"}).status_code == 422


def test_borrar_cuenta(monkeypatch):
    _, borrados = _sin_supabase(monkeypatch)
    assert cliente.delete("/v1/yo", headers=TOKEN).status_code == 204
    assert borrados == ["u-1"]
