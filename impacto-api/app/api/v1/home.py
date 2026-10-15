import os

from fastapi import APIRouter, Response

from app.datos_ejemplo.home import home_de_ejemplo
from app.modelos.home import Home

router = APIRouter()

# Los datos se precalculan, así que la respuesta se puede cachear. En desarrollo conviene 0.
CACHE_SEGUNDOS = int(os.getenv("CACHE_SEGUNDOS", "300"))


@router.get("/home", response_model=Home)
def obtener_home(response: Response) -> Home:
    """Todo lo que necesita la pantalla de inicio en una sola llamada."""
    response.headers["Cache-Control"] = f"public, max-age={CACHE_SEGUNDOS}"
    return home_de_ejemplo()
