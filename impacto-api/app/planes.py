"""Catálogo de capacidades por plan y reglas del switch MODO_PLANES.

El código nunca pregunta por el plan: pregunta si el usuario tiene una
capacidad (`puede`). Mientras no exista Supabase, el catálogo vive aquí; después
se leerá de las tablas planes, capacidades y plan_capacidades (docs/planes.md).
"""

import os

from app.modelos.planes import Capacidades, EstadoCapacidad, ModoPlanes, Plan

_ORDEN = [Plan.gratis, Plan.pro, Plan.empresas]

# id: (plan mínimo, límite por plan o None)
CATALOGO: dict[str, tuple[Plan, dict[Plan, int] | None]] = {
    "termometros.basico": (Plan.gratis, None),
    "historia.1_anio": (Plan.gratis, None),
    "historia.larga": (Plan.pro, None),
    "expectativas": (Plan.pro, None),
    "sorpresa_dato": (Plan.pro, None),
    "cruces": (Plan.pro, None),
    "termometro.consumo": (Plan.pro, None),
    "termometro.vivienda": (Plan.pro, None),
    "precios.vs_ipc": (Plan.pro, None),
    "aviso_bencina": (Plan.pro, None),
    "mi_impacto": (Plan.pro, None),
    # Datos anclados arriba en el Inicio: 3 en el plan gratis, sin límite desde Pro.
    "datos.anclados": (Plan.gratis, {Plan.gratis: 3}),
    "calculadoras.basicas": (Plan.gratis, None),
    "calculadoras.escenarios": (Plan.pro, None),
    "alertas": (Plan.pro, {Plan.pro: 10, Plan.empresas: 50}),
    "descargas.csv": (Plan.pro, None),
    "calendario.basico": (Plan.gratis, None),
    "calendario.expectativas": (Plan.pro, None),
    "mi_rubro": (Plan.empresas, None),
    "reajustes_ipc": (Plan.empresas, None),
    "usuarios": (Plan.gratis, {Plan.gratis: 1, Plan.pro: 1, Plan.empresas: 5}),
    "api.acceso": (Plan.empresas, None),
    "api.limite_diario": (Plan.empresas, {Plan.empresas: 10_000}),
}


def modo() -> ModoPlanes:
    return ModoPlanes(os.getenv("MODO_PLANES", ModoPlanes.abierto.value))


def _incluida(capacidad: str, plan: Plan) -> bool:
    minimo, _ = CATALOGO[capacidad]
    return _ORDEN.index(plan) >= _ORDEN.index(minimo)


def puede(capacidad: str, plan: Plan = Plan.gratis) -> bool:
    """En modo abierto o vista previa todos pueden todo; en modo activo, según el plan."""
    if capacidad not in CATALOGO:
        raise KeyError(f"Capacidad desconocida: {capacidad}")
    return modo() is not ModoPlanes.activo or _incluida(capacidad, plan)


def capacidades(plan: Plan = Plan.gratis) -> Capacidades:
    estados = {}
    for id_, (minimo, limites) in CATALOGO.items():
        # El límite que se informa es el del plan del usuario o, si no lo tiene, el del plan mínimo.
        limite = None
        if limites:
            limite = limites.get(plan) if _incluida(id_, plan) else limites.get(minimo)
        estados[id_] = EstadoCapacidad(activa=puede(id_, plan), plan_minimo=minimo, limite=limite)
    return Capacidades(modo=modo(), plan=plan, capacidades=estados)
