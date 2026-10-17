import os

from fastapi import APIRouter, Query, Response

# Se llama a través del módulo para que una recarga de los datos (app/fotos.py) se vea al tiro.
from app.datos_ejemplo import home as datos_home
from app.modelos.home import CambioSemana, Home

router = APIRouter()

# Los datos se precalculan, así que la respuesta se puede cachear. En desarrollo conviene 0.
CACHE_SEGUNDOS = int(os.getenv("CACHE_SEGUNDOS", "300"))


@router.get("/home", response_model=Home)
def obtener_home(
    response: Response,
    anclados: str | None = Query(
        default=None, description="Ids de los datos anclados, separados por coma; van primero en \"Lo que cambió\""
    ),
) -> Home:
    """Todo lo que necesita la pantalla de inicio en una sola llamada."""
    response.headers["Cache-Control"] = f"public, max-age={CACHE_SEGUNDOS}"
    ids = [a.strip() for a in anclados.split(",") if a.strip()] if anclados else None
    return datos_home.home_de_ejemplo(ids)


@router.get("/datos", response_model=list[CambioSemana])
def obtener_datos(response: Response) -> list[CambioSemana]:
    """Todos los datos con su último movimiento, ordenados por presión."""
    response.headers["Cache-Control"] = f"public, max-age={CACHE_SEGUNDOS}"
    return datos_home.todos_los_datos()
