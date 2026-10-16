"""Endpoints del usuario actual. Sin cuentas todavía: todos son plan gratis."""

from fastapi import APIRouter

from app import planes
from app.modelos.planes import Capacidades

router = APIRouter(prefix="/yo", tags=["usuario"])


@router.get("/capacidades", response_model=Capacidades)
def obtener_capacidades() -> Capacidades:
    # Sin caché: el modo puede cambiar con el switch y la app debe verlo al abrir.
    return planes.capacidades()
