"""Datos de ejemplo del home.

Reúne lo que muestran las demás secciones: la canasta y los productos salen de
la foto real de ODEPA (ver precios.py) y los termómetros de termometros.py.
"""

from datetime import date

from app.datos_ejemplo.precios import CANASTA, PRODUCTOS, PRODUCTOS_POR_ID
from app.datos_ejemplo.termometros import TERMOMETROS, termometro_de_ejemplo
from app.modelos.home import CambioSemana, Home, Resumen
from app.modelos.precios import Producto
from app.modelos.termometros import Presion, Tendencia

NBSP = "\u00a0"
# Cómo se lee el precio según la unidad del producto ("$1.596 el kilo").
_ARTICULO_UNIDAD = {
    "kilo": "el kilo",
    "litro": "el litro",
    "bandeja de 30": "la bandeja",
    "botella 900 ml": "la botella",
}
# Bajo este cambio porcentual se considera que el precio se mantuvo.
_UMBRAL_ESTABLE = 0.5


def _pesos(valor: float) -> str:
    return "$" + f"{round(valor):,}".replace(",", ".")


def _pct(valor: float) -> str:
    signo = "+" if valor > 0 else "−" if valor < 0 else ""
    return f"{signo}{abs(valor):.1f}".replace(".", ",") + f"{NBSP}%"


def _cambio_producto(p: Producto) -> CambioSemana:
    if abs(p.variacion_semanal) < _UMBRAL_ESTABLE:
        direccion, presion = Tendencia.estable, Presion.media
    elif p.variacion_semanal > 0:
        # Un alimento más caro presiona el bolsillo.
        direccion, presion = Tendencia.sube, Presion.alta
    else:
        direccion, presion = Tendencia.baja, Presion.baja
    unidad = _ARTICULO_UNIDAD.get(p.unidad, p.unidad)
    return CambioSemana(
        id=p.id,
        nombre=p.nombre,
        detalle=f"{_pct(p.variacion_semanal)} · {_pesos(p.precio)} {unidad}",
        direccion=direccion,
        presion=presion,
        serie=[punto.precio for punto in p.serie],
        enlace=f"/precios/{p.id}",
    )


def _cambio_indicador(termometro: str, indicador: str, nombre: str, detalle: str,
                      direccion: Tendencia, presion: Presion) -> CambioSemana:
    detalle_termometro = termometro_de_ejemplo(termometro)
    serie = next(i.serie for i in detalle_termometro.indicadores if i.id == indicador)
    return CambioSemana(
        id=indicador,
        nombre=nombre,
        detalle=detalle,
        direccion=direccion,
        presion=presion,
        serie=[p.valor for p in serie],
        enlace=f"/termometros/{termometro}",
    )


def _cambios() -> list[CambioSemana]:
    # Los 3 alimentos que más se movieron más la marraqueta (siempre, por ser el precio
    # de referencia), y dos indicadores de contexto (de ejemplo).
    otros = [p for p in PRODUCTOS if p.id != "marraqueta"]
    mas_movidos = sorted(otros, key=lambda p: abs(p.variacion_semanal), reverse=True)[:3]
    alimentos = sorted(mas_movidos + [PRODUCTOS_POR_ID["marraqueta"]],
                       key=lambda p: abs(p.variacion_semanal), reverse=True)
    return [_cambio_producto(p) for p in alimentos] + [
        _cambio_indicador("actividad", "desempleo", "Desempleo", f"Sigue en 8,7{NBSP}%",
                          Tendencia.estable, Presion.alta),
        _cambio_indicador("dolar", "dolar", "Dólar", f"−0,8{NBSP}% · $935",
                          Tendencia.baja, Presion.media),
    ]


def home_de_ejemplo() -> Home:
    return Home(
        generado_el=date(2026, 10, 15),
        datos_de_ejemplo=True,
        resumen=Resumen(
            titulo="La canasta baja un poco: el pan cae 1 % esta semana.",
            texto=f"La tasa del Banco Central sigue en 4,5{NBSP}% y el dólar bajó.",
        ),
        canasta=CANASTA,
        cambios=_cambios(),
        termometros=TERMOMETROS,
        termometros_por_defecto=["bolsillo", "deudas", "ahorro", "actividad"],
        max_termometros_home=4,
        aviso_legal=(
            "Impacto Financiero informa y explica; no es asesoría financiera, "
            "tributaria ni de inversión."
        ),
    )
