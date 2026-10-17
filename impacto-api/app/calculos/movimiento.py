"""Qué tan inusual fue el último cambio de un dato.

"Lo que cambió esta semana" elige por movimiento, no por presión: la presión mide
qué tan lejos de lo normal está el nivel; el movimiento, qué tan grande fue el
último cambio comparado con lo que ese dato suele moverse. Un dólar que se mueve
0,3 % en una semana no es noticia; uno que se mueve 3 %, sí.

    movimiento = |cambio actual| ÷ desviación estándar de sus cambios históricos

Se lee como "veces lo habitual": 2 significa el doble de lo que suele moverse.
"""

import statistics
from datetime import date

# Con menos cambios en la historia no se puede decir qué es lo habitual.
MINIMO_CAMBIOS = 6


def movimiento(actual: float, historia: list[float]) -> float:
    if len(historia) < MINIMO_CAMBIOS:
        return 0.0
    desviacion = statistics.pstdev(historia)
    return abs(actual) / desviacion if desviacion > 0 else 0.0


def por_periodo(puntos: list[tuple[date, float]], clave) -> list[float]:
    """Último valor de cada período (semana o mes), en orden."""
    ultimos: dict = {}
    for fecha, valor in puntos:
        ultimos[clave(fecha)] = valor
    return list(ultimos.values())


def semanal(puntos: list[tuple[date, float]]) -> list[float]:
    return por_periodo(puntos, lambda f: f.isocalendar()[:2])


def mensual(puntos: list[tuple[date, float]]) -> list[float]:
    return por_periodo(puntos, lambda f: (f.year, f.month))


def variaciones(valores: list[float], paso: int = 1) -> list[float]:
    """Variaciones porcentuales entre valores separados por `paso` períodos."""
    return [(b / a - 1) * 100 for a, b in zip(valores, valores[paso:]) if a]


def diferencias(valores: list[float], paso: int = 1) -> list[float]:
    """Diferencias (por ejemplo, en puntos porcentuales) separadas por `paso` períodos."""
    return [b - a for a, b in zip(valores, valores[paso:])]
