import os

from fastapi import APIRouter, Query, Response

from app.datos_ejemplo.home import home_de_ejemplo, todos_los_datos
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
    return home_de_ejemplo(ids)


@router.get("/datos", response_model=list[CambioSemana])
def obtener_datos(response: Response) -> list[CambioSemana]:
    """Todos los datos con su último movimiento, ordenados por presión."""
    response.headers["Cache-Control"] = f"public, max-age={CACHE_SEGUNDOS}"
    return todos_los_datos()
