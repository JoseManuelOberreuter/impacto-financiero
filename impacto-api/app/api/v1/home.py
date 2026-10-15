from fastapi import APIRouter, Response

from app.datos_ejemplo.home import home_de_ejemplo
from app.modelos.home import Home

router = APIRouter()


@router.get("/home", response_model=Home)
def obtener_home(response: Response) -> Home:
    """Todo lo que necesita la pantalla de inicio en una sola llamada."""
    # Los datos se precalculan; la respuesta se puede cachear unos minutos.
    response.headers["Cache-Control"] = "public, max-age=300"
    return home_de_ejemplo()
