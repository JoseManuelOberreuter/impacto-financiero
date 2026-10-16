"""Endpoints de las secciones de la app: termómetros, precios, noticias, herramientas y Mi impacto."""

from fastapi import APIRouter, HTTPException, Response

from app.api.v1.home import CACHE_SEGUNDOS
from app.datos_ejemplo.herramientas import herramientas_de_ejemplo
from app.datos_ejemplo.mi_impacto import referencias
from app.datos_ejemplo.noticias import noticias_de_ejemplo
from app.datos_ejemplo.precios import precios_de_ejemplo, producto_de_ejemplo
from app.datos_ejemplo.termometros import termometro_de_ejemplo, termometros_de_ejemplo
from app.modelos.herramientas import Herramientas
from app.modelos.mi_impacto import ReferenciasMiImpacto
from app.modelos.noticias import Noticias
from app.modelos.precios import Precios, Producto
from app.modelos.termometros import Termometro, TermometroDetalle

router = APIRouter()


def _cache(response: Response) -> None:
    response.headers["Cache-Control"] = f"public, max-age={CACHE_SEGUNDOS}"


@router.get("/termometros", response_model=list[Termometro], tags=["termómetros"])
def listar_termometros(response: Response) -> list[Termometro]:
    _cache(response)
    return termometros_de_ejemplo()


@router.get("/termometros/{id_}", response_model=TermometroDetalle, tags=["termómetros"])
def obtener_termometro(id_: str, response: Response) -> TermometroDetalle:
    detalle = termometro_de_ejemplo(id_)
    if detalle is None:
        raise HTTPException(status_code=404, detail="Termómetro no encontrado")
    _cache(response)
    return detalle


@router.get("/precios", response_model=Precios, tags=["precios"])
def obtener_precios(response: Response) -> Precios:
    _cache(response)
    return precios_de_ejemplo()


@router.get("/precios/{id_}", response_model=Producto, tags=["precios"])
def obtener_producto(id_: str, response: Response) -> Producto:
    producto = producto_de_ejemplo(id_)
    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    _cache(response)
    return producto


@router.get("/noticias", response_model=Noticias, tags=["noticias"])
def obtener_noticias(response: Response) -> Noticias:
    _cache(response)
    return noticias_de_ejemplo()


@router.get("/herramientas", response_model=Herramientas, tags=["herramientas"])
def obtener_herramientas(response: Response) -> Herramientas:
    _cache(response)
    return herramientas_de_ejemplo()


@router.get("/mi-impacto/referencias", response_model=ReferenciasMiImpacto, tags=["mi impacto"])
def obtener_referencias_mi_impacto(response: Response) -> ReferenciasMiImpacto:
    """UF y bencina para que la app calcule el impacto con los datos del usuario, sin enviarlos."""
    _cache(response)
    return referencias()
