"""Estado de presión de un indicador respecto de su propia historia.

Regla de docs/termometros.md: se compara el valor actual con los últimos 5 años.
Sobre el percentil 80 la presión es alta, bajo el 20 es baja y entre ambos, media.
En los indicadores "invertidos" (por ejemplo, el IMACEC o el cobre) un valor bajo
es el que presiona, así que la regla se da vuelta.
"""

import statistics

from app.modelos.termometros import BandaNormal, Presion

# Con menos datos no hay historia suficiente para decir qué es lo habitual.
MINIMO_OBSERVACIONES = 12


def banda_normal(historia: list[float]) -> BandaNormal:
    """Rango entre los percentiles 20 y 80 de la historia."""
    cortes = statistics.quantiles(historia, n=5, method="inclusive")
    return BandaNormal(min=cortes[0], max=cortes[3])


def evaluar(valor: float, historia: list[float], invertida: bool = False) -> tuple[Presion, BandaNormal | None]:
    if len(historia) < MINIMO_OBSERVACIONES:
        return Presion.media, None
    banda = banda_normal(historia)
    if valor > banda.max:
        presion = Presion.baja if invertida else Presion.alta
    elif valor < banda.min:
        presion = Presion.alta if invertida else Presion.baja
    else:
        presion = Presion.media
    return presion, banda


def la_mas_alta(*presiones: Presion) -> Presion:
    """Presión de un termómetro con varios indicadores: la más alta de ellos."""
    orden = [Presion.baja, Presion.media, Presion.alta]
    return max(presiones, key=orden.index)
