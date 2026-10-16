"""Esquemas de planes y capacidades (ver docs/planes.md)."""

from enum import Enum

from pydantic import BaseModel, Field


class Plan(str, Enum):
    gratis = "gratis"
    pro = "pro"
    empresas = "empresas"


class ModoPlanes(str, Enum):
    """Cómo se aplican los planes: el "switch" de docs/planes.md."""

    abierto = "abierto"
    vista_previa = "vista_previa"
    activo = "activo"


class EstadoCapacidad(BaseModel):
    activa: bool = Field(description="Si el usuario puede usarla ahora")
    plan_minimo: Plan = Field(description="Plan más barato que la incluye, para la etiqueta y el BloquePro")
    limite: int | None = Field(default=None, description="Cantidad máxima, en las capacidades con límite")


class Capacidades(BaseModel):
    modo: ModoPlanes
    plan: Plan
    capacidades: dict[str, EstadoCapacidad]
