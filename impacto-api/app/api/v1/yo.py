"""Endpoints del usuario actual (docs/cuentas.md).

La cuenta es opcional: sin sesión, /yo/capacidades responde como plan gratis y el resto
pide iniciar sesión.
"""

from datetime import UTC, datetime

from fastapi import APIRouter, Depends, Response
from pydantic import BaseModel, Field

from app import planes, supabase
from app.modelos.planes import Capacidades, Plan
from app.sesion import Usuario, usuario_opcional, usuario_requerido

router = APIRouter(prefix="/yo", tags=["usuario"])

MAX_ANCLADOS = 50


class Yo(BaseModel):
    id: str
    correo: str
    verificado: bool
    nombre: str | None
    plan: Plan


class Preferencias(BaseModel):
    anclados: list[str] = Field(default_factory=list, max_length=MAX_ANCLADOS)
    apariencia: str = Field(default="automatico", pattern="^(automatico|claro|oscuro)$")
    mi_impacto: dict | None = Field(default=None, description="Solo si el usuario elige sincronizarlo")


def _plan(usuario: Usuario | None) -> Plan:
    """Plan vigente: el de la suscripción activa o en prueba; si no hay, gratis."""
    if usuario is None:
        return Plan.gratis
    filas = supabase.seleccionar(
        "suscripciones", {"usuario_id": f"eq.{usuario.id}", "estado": "in.(activa,prueba)"}, "plan_id"
    )
    planes_activos = {f["plan_id"] for f in filas}
    for plan in (Plan.empresas, Plan.pro):
        if plan.value in planes_activos:
            return plan
    return Plan.gratis


@router.get("/capacidades", response_model=Capacidades)
def obtener_capacidades(usuario: Usuario | None = Depends(usuario_opcional)) -> Capacidades:
    # Sin caché: el modo puede cambiar con el switch y la app debe verlo al abrir.
    return planes.capacidades(_plan(usuario))


@router.get("", response_model=Yo)
def obtener_yo(usuario: Usuario = Depends(usuario_requerido)) -> Yo:
    return Yo(id=usuario.id, correo=usuario.correo, verificado=usuario.verificado, nombre=usuario.nombre,
              plan=_plan(usuario))


@router.get("/preferencias", response_model=Preferencias)
def obtener_preferencias(usuario: Usuario = Depends(usuario_requerido)) -> Preferencias:
    filas = supabase.seleccionar("preferencias", {"usuario_id": f"eq.{usuario.id}"},
                                 "anclados,apariencia,mi_impacto")
    return Preferencias(**filas[0]) if filas else Preferencias()


@router.put("/preferencias", response_model=Preferencias)
def guardar_preferencias(preferencias: Preferencias, usuario: Usuario = Depends(usuario_requerido)) -> Preferencias:
    fila = supabase.guardar(
        "preferencias",
        {"usuario_id": usuario.id, **preferencias.model_dump(), "actualizado_el": datetime.now(UTC).isoformat()},
        conflicto="usuario_id",
    )
    return Preferencias(**{k: fila[k] for k in ("anclados", "apariencia", "mi_impacto")})


@router.delete("", status_code=204)
def borrar_cuenta(usuario: Usuario = Depends(usuario_requerido)) -> Response:
    """Borra la cuenta y todos sus datos. No se puede deshacer."""
    supabase.borrar_usuario(usuario.id)
    return Response(status_code=204)
