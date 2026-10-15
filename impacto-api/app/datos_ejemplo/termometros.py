"""Termómetros de ejemplo.

Bolsillo y Ahorro usan las fotos reales de ODEPA y de la Superintendencia de
Pensiones. El resto de las cifras (IPC, TPM, desempleo, dólar, tono de noticias)
son valores de ejemplo.
"""

import json
import statistics
from datetime import date
from pathlib import Path

from app.datos_ejemplo.precios import CANASTA, PRODUCTOS_POR_ID
from app.modelos.termometros import (
    BandaNormal,
    Indicador,
    Percepcion,
    Presion,
    Publicacion,
    PuntoSerie,
    Tendencia,
    Termometro,
    TermometroDetalle,
)

NBSP = " "
_AFP = json.loads((Path(__file__).parent / "afp_snapshot.json").read_text(encoding="utf-8"))
_FONDOS = {f["fondo"]: f["afps"] for f in _AFP["fondos"]}


def _pesos(valor: float) -> str:
    return "$" + f"{round(valor):,}".replace(",", ".")


def _pct(valor: float, decimales: int = 1) -> str:
    signo = "+" if valor > 0 else "−" if valor < 0 else ""
    return f"{signo}{abs(valor):.{decimales}f}".replace(".", ",") + f"{NBSP}%"


def _mensual(valores: list[float], ultimo: tuple[int, int]) -> list[PuntoSerie]:
    """Serie mensual que termina en (año, mes)."""
    anio, mes = ultimo
    puntos = []
    for i, valor in enumerate(reversed(valores)):
        m = (mes - 1 - i) % 12 + 1
        a = anio + (mes - 1 - i) // 12
        puntos.append(PuntoSerie(fecha=date(a, m, 1), valor=valor))
    return list(reversed(puntos))


def _semanal_precios(id_: str) -> list[PuntoSerie]:
    return [PuntoSerie(fecha=p.semana, valor=p.precio) for p in PRODUCTOS_POR_ID[id_].serie]


def _mediana_fondo(fondo: str, campo: str) -> float:
    return statistics.median(a[campo] for a in _FONDOS[fondo])


_AFP_AL = date.fromisoformat(_AFP["dato_al"])
_MARRAQUETA = PRODUCTOS_POR_ID["marraqueta"]

TERMOMETROS = [
    Termometro(
        id="bolsillo",
        nombre="Bolsillo",
        pregunta="¿Está más cara la vida?",
        presion=Presion.media,
        etiqueta_presion="Presión media",
        tendencia=Tendencia.baja,
        dato_clave=f"Canasta semanal: {_pesos(CANASTA.total)} ({_pct(CANASTA.variacion_semanal)})",
        frase="Bajaron el pan, el pollo y el aceite; subieron los huevos.",
        dato_al=CANASTA.dato_al,
        proxima_actualizacion=date(2026, 10, 16),
        fuentes=["ODEPA", "CNE", "Panel de Expertos"],
    ),
    Termometro(
        id="deudas",
        nombre="Deudas",
        pregunta="¿Está más caro endeudarse?",
        presion=Presion.media,
        etiqueta_presion="Presión media",
        tendencia=Tendencia.estable,
        dato_clave=f"Tasa del Banco Central: 4,5{NBSP}%",
        frase="La tasa se mantiene y los expertos no esperan cambios este año.",
        dato_al=date(2026, 10, 14),
        proxima_actualizacion=date(2026, 10, 28),
        fuentes=["Banco Central", "CMF"],
    ),
    Termometro(
        id="ahorro",
        nombre="Ahorro y pensiones",
        pregunta="¿Cómo le va a mi plata?",
        presion=Presion.media,
        etiqueta_presion="Presión media",
        tendencia=Tendencia.estable,
        dato_clave=f"Fondo C: {_pct(_mediana_fondo('C', 'mes'))} en el mes",
        frase="Los fondos riesgosos subieron y los conservadores bajaron en el último mes.",
        dato_al=_AFP_AL,
        proxima_actualizacion=date(2026, 10, 16),
        fuentes=["Superintendencia de Pensiones"],
    ),
    Termometro(
        id="actividad",
        nombre="Actividad y empleo",
        pregunta="¿Cómo va la economía en general?",
        presion=Presion.alta,
        etiqueta_presion="Presión alta",
        tendencia=Tendencia.sube,
        dato_clave=f"Desempleo: 8,7{NBSP}%",
        frase="El desempleo sigue sobre lo habitual, aunque la actividad crece.",
        dato_al=date(2026, 8, 31),
        proxima_actualizacion=date(2026, 10, 30),
        fuentes=["INE", "Banco Central"],
    ),
    Termometro(
        id="dolar",
        nombre="Dólar y mercados",
        pregunta="¿Qué pasa afuera?",
        presion=Presion.media,
        etiqueta_presion="Presión media",
        tendencia=Tendencia.baja,
        dato_clave="Dólar observado: $935",
        frase="El dólar bajó por segundo día, ayudado por el alza del cobre.",
        dato_al=date(2026, 10, 14),
        proxima_actualizacion=date(2026, 10, 15),
        fuentes=["Banco Central"],
    ),
    Termometro(
        id="animo",
        nombre="Ánimo",
        pregunta="¿De qué se está hablando?",
        presion=Presion.alta,
        etiqueta_presion="Más negativo que lo habitual",
        tendencia=Tendencia.baja,
        dato_clave="412 titulares de 6 medios",
        frase="Dominaron el desempleo y el precio de la bencina.",
        dato_al=date(2026, 10, 14),
        proxima_actualizacion=date(2026, 10, 15),
        fuentes=["Prensa", "CMF"],
    ),
]
_POR_ID = {t.id: t for t in TERMOMETROS}

_METODOLOGIA = (
    "Cada indicador se compara con su propia historia de los últimos 5 años: si está en el "
    "20 % más alto, la presión es alta; en el 20 % más bajo, baja; y si no, media. "
    "La presión no dice si algo es bueno o malo, solo si está lejos de lo habitual."
)

_DETALLES = {
    "bolsillo": dict(
        explicacion=(
            "La canasta semanal bajó levemente porque los alimentos se abarataron: el pan "
            f"cayó {_pct(abs(_MARRAQUETA.variacion_semanal)).lstrip('+')} y también bajaron el pollo y el aceite. "
            "La bencina y el gas se mantienen altos y son casi el 40 % de la canasta."
        ),
        indicadores=[
            Indicador(
                id="canasta",
                nombre="Índice de canasta",
                valor=_pesos(CANASTA.total),
                variacion=f"{_pct(CANASTA.variacion_semanal)} semanal",
                presion=Presion.media,
                descripcion="Costo de una canasta semanal típica (indicador propio).",
                serie=[PuntoSerie(fecha=p.semana, valor=p.precio) for p in CANASTA.serie],
                banda_normal=BandaNormal(min=124000, max=128500),
                fuente="ODEPA, CNE, Panel de Expertos",
                dato_al=CANASTA.dato_al,
            ),
            Indicador(
                id="marraqueta",
                nombre="Marraqueta",
                valor=f"{_pesos(_MARRAQUETA.precio)} / kilo",
                variacion=f"{_pct(_MARRAQUETA.variacion_semanal)} semanal",
                presion=Presion.baja,
                descripcion="Mediana de panaderías y supermercados de Santiago.",
                serie=_semanal_precios("marraqueta"),
                banda_normal=BandaNormal(min=2100, max=2300),
                fuente="ODEPA",
                dato_al=_MARRAQUETA.dato_al,
            ),
            Indicador(
                id="ipc",
                nombre="IPC mensual",
                valor=f"0,3{NBSP}%",
                variacion=f"4,1{NBSP}% en 12 meses",
                presion=Presion.media,
                descripcion="Variación mensual del índice de precios al consumidor.",
                serie=_mensual([0.6, 0.4, 0.2, 0.5, 0.3, 0.1, 0.4, 0.3, 0.2, 0.4, 0.5, 0.3], (2026, 9)),
                banda_normal=BandaNormal(min=0.1, max=0.5),
                fuente="INE",
                dato_al=date(2026, 9, 30),
            ),
            Indicador(
                id="bencina",
                nombre="Bencina 95",
                valor="$1.312 / litro",
                variacion=f"+1,2{NBSP}% semanal",
                presion=Presion.alta,
                descripcion="Promedio de estaciones de servicio de Santiago.",
                serie=_mensual([1215, 1228, 1240, 1236, 1250, 1262, 1259, 1270, 1281, 1290, 1296, 1312], (2026, 10)),
                banda_normal=BandaNormal(min=1180, max=1290),
                fuente="CNE",
                dato_al=date(2026, 10, 14),
            ),
        ],
        percepcion=Percepcion(
            nombre="Confianza del consumidor (IPEC)",
            valor="43,6 puntos",
            descripcion="Bajo 50 significa más pesimismo que optimismo.",
            fuente="GfK Chile",
        ),
        proximas_publicaciones=[
            Publicacion(fecha=date(2026, 10, 16), nombre="Precios de alimentos", fuente="ODEPA"),
            Publicacion(fecha=date(2026, 11, 9), nombre="IPC de octubre", fuente="INE"),
        ],
        herramienta_relacionada="Tu inflación personal",
    ),
    "deudas": dict(
        explicacion=(
            "La tasa de política monetaria lleva meses en 4,5 % y los expertos no esperan cambios "
            "este año. Los créditos de consumo e hipotecarios siguen caros comparados con antes de 2022."
        ),
        indicadores=[
            Indicador(
                id="tpm",
                nombre="Tasa de política monetaria",
                valor=f"4,5{NBSP}%",
                variacion="Sin cambio",
                presion=Presion.media,
                descripcion="La tasa que fija el Banco Central y guía al resto de las tasas.",
                serie=_mensual([5.0, 5.0, 4.75, 4.75, 4.75, 4.5, 4.5, 4.5, 4.5, 4.5, 4.5, 4.5], (2026, 10)),
                banda_normal=BandaNormal(min=2.5, max=5.5),
                fuente="Banco Central",
                dato_al=date(2026, 10, 14),
            ),
            Indicador(
                id="hipotecario",
                nombre="Tasa hipotecaria promedio",
                valor=f"UF + 4,2{NBSP}%",
                variacion=f"−0,1{NBSP}% en el mes",
                presion=Presion.media,
                descripcion="Tasa promedio de créditos hipotecarios en UF.",
                serie=_mensual([4.5, 4.4, 4.4, 4.3, 4.3, 4.3, 4.2, 4.3, 4.2, 4.3, 4.3, 4.2], (2026, 9)),
                banda_normal=BandaNormal(min=3.0, max=4.6),
                fuente="CMF",
                dato_al=date(2026, 9, 30),
            ),
        ],
        percepcion=None,
        proximas_publicaciones=[
            Publicacion(fecha=date(2026, 10, 28), nombre="Reunión de política monetaria", fuente="Banco Central"),
        ],
        herramienta_relacionada="¿Cuánto sube mi dividendo?",
    ),
    "ahorro": dict(
        explicacion=(
            "En el último mes los fondos con más acciones (A y B) subieron, mientras los más "
            "conservadores (D y E) bajaron. En lo que va del año, el Fondo A rinde "
            f"{_pct(_mediana_fondo('A', 'anio'))} y el E {_pct(_mediana_fondo('E', 'anio'))}."
        ),
        indicadores=[
            Indicador(
                id=f"fondo_{fondo.lower()}",
                nombre=f"Fondo {fondo}",
                valor=f"{_pct(_mediana_fondo(fondo, 'mes'), 2)} en el mes",
                variacion=f"{_pct(_mediana_fondo(fondo, 'anio'))} en el año",
                presion=Presion.media,
                descripcion="Mediana de la rentabilidad nominal de las 7 AFP (dato provisional).",
                # La foto de AFP aún no guarda historia: sin gráfico por ahora.
                serie=[],
                fuente="Superintendencia de Pensiones",
                dato_al=_AFP_AL,
            )
            for fondo in ["A", "C", "E"]
        ],
        percepcion=None,
        proximas_publicaciones=[
            Publicacion(fecha=date(2026, 10, 16), nombre="Valores cuota", fuente="Superintendencia de Pensiones"),
        ],
        herramienta_relacionada="Mi AFP",
    ),
    "actividad": dict(
        explicacion=(
            "La economía crece a un ritmo moderado, pero el desempleo sigue sobre lo habitual "
            "de los últimos años, sobre todo en la Región Metropolitana."
        ),
        indicadores=[
            Indicador(
                id="desempleo",
                nombre="Tasa de desempleo",
                valor=f"8,7{NBSP}%",
                variacion=f"+0,2 pp en 12 meses",
                presion=Presion.alta,
                descripcion="Trimestre móvil junio-agosto.",
                serie=_mensual([8.5, 8.4, 8.3, 8.5, 8.7, 8.8, 8.9, 8.8, 8.7, 8.6, 8.7, 8.7], (2026, 8)),
                banda_normal=BandaNormal(min=7.0, max=8.5),
                fuente="INE",
                dato_al=date(2026, 8, 31),
            ),
            Indicador(
                id="imacec",
                nombre="IMACEC",
                valor=f"+2,1{NBSP}%",
                variacion="anual",
                presion=Presion.media,
                descripcion="Crecimiento de la actividad económica respecto del mismo mes del año anterior.",
                serie=_mensual([1.8, 2.4, 1.2, 2.9, 2.2, 1.5, 2.6, 1.9, 2.3, 1.7, 2.5, 2.1], (2026, 8)),
                banda_normal=BandaNormal(min=1.0, max=3.5),
                fuente="Banco Central",
                dato_al=date(2026, 8, 31),
            ),
        ],
        percepcion=None,
        proximas_publicaciones=[
            Publicacion(fecha=date(2026, 10, 30), nombre="Desempleo julio-septiembre", fuente="INE"),
            Publicacion(fecha=date(2026, 11, 2), nombre="IMACEC de septiembre", fuente="Banco Central"),
        ],
        herramienta_relacionada="¿Mi sueldo le ganó a la inflación?",
    ),
    "dolar": dict(
        explicacion="El dólar bajó en los últimos días, en parte por el alza del precio del cobre.",
        indicadores=[
            Indicador(
                id="dolar",
                nombre="Dólar observado",
                valor="$935",
                variacion=f"−0,8{NBSP}% semanal",
                presion=Presion.media,
                descripcion="Tipo de cambio que publica el Banco Central cada día hábil.",
                serie=_mensual([948, 955, 961, 952, 944, 939, 950, 958, 962, 949, 942, 935], (2026, 10)),
                banda_normal=BandaNormal(min=880, max=970),
                fuente="Banco Central",
                dato_al=date(2026, 10, 14),
            ),
        ],
        percepcion=None,
        proximas_publicaciones=[
            Publicacion(fecha=date(2026, 10, 15), nombre="Dólar observado", fuente="Banco Central"),
        ],
        herramienta_relacionada=None,
    ),
    "animo": dict(
        explicacion=(
            "Las noticias económicas de la semana fueron más negativas que lo habitual, "
            "dominadas por el desempleo y el precio de los combustibles."
        ),
        indicadores=[
            Indicador(
                id="tono",
                nombre="Tono de las noticias",
                valor="−18",
                variacion="de −100 a +100",
                presion=Presion.alta,
                descripcion="Tono neto de los titulares económicos, promedio de 7 días.",
                serie=_mensual([-4, -6, -2, -8, -10, -7, -12, -9, -11, -14, -16, -18], (2026, 10)),
                banda_normal=BandaNormal(min=-12, max=4),
                fuente="Cálculo propio sobre titulares de prensa",
                dato_al=date(2026, 10, 14),
            ),
        ],
        percepcion=None,
        proximas_publicaciones=[],
        herramienta_relacionada=None,
    ),
}


def termometros_de_ejemplo() -> list[Termometro]:
    return TERMOMETROS


def termometro_de_ejemplo(id_: str) -> TermometroDetalle | None:
    if id_ not in _POR_ID:
        return None
    return TermometroDetalle(
        **_POR_ID[id_].model_dump(), **_DETALLES[id_], metodologia=_METODOLOGIA
    )
