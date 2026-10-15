"""Termómetros de ejemplo.

Bolsillo y Ahorro usan las fotos reales de ODEPA y de la Superintendencia de
Pensiones. IPC, TPM, tasa hipotecaria, desempleo, IMACEC, dólar, cobre e IPEC
vienen de la foto real del Banco Central (banco_central.py), con la presión
calculada sobre 5 años. La bencina y el tono de las noticias siguen de ejemplo.
"""

import json
import statistics
from datetime import date, timedelta
from pathlib import Path

from app.calculos.presion import la_mas_alta
from app.datos_ejemplo import banco_central as bc
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

# --- Datos reales del Banco Central (bcch_snapshot.json) ---

_TPM = bc.SERIES["tpm"]
_TPM_CAMBIO = _TPM.ultimo.valor - _TPM.antes_de(30).valor
_TPM_ESPERADA = bc.SERIES["tpm_esperada_11m"].ultimo.valor
_HIPOTECARIA = bc.SERIES["tasa_hipotecaria"]
_DESEMPLEO = bc.SERIES["desempleo"]
_DESEMPLEO_12M = _DESEMPLEO.ultimo.valor - _DESEMPLEO.antes_de(365).valor
_IMACEC = bc.SERIES["imacec_12m"].ultimo
_IPC = bc.SERIES["ipc_mensual"].ultimo
_IPC_12M = bc.SERIES["ipc_12m"].ultimo
_DOLAR = bc.SERIES["dolar"]
_DOLAR_SEMANA = bc.variacion(_DOLAR.ultimo.valor, _DOLAR.antes_de(7).valor)
_COBRE = bc.SERIES["cobre"]
_COBRE_SEMANA = bc.variacion(_COBRE.ultimo.valor, _COBRE.antes_de(7).valor)
_IPEC = bc.SERIES["ipec"].ultimo


def _texto_tpm() -> str:
    actual = bc.tasa(_TPM.ultimo.valor)
    if abs(_TPM_CAMBIO) < 0.01:
        hoy = f"La tasa del Banco Central se mantiene en {actual}"
    else:
        hoy = f"La tasa del Banco Central {'subió' if _TPM_CAMBIO > 0 else 'bajó'} a {actual}"
    diferencia = _TPM_ESPERADA - _TPM.ultimo.valor
    if abs(diferencia) < 0.125:
        futuro = "los economistas no esperan cambios en el próximo año"
    else:
        accion = "suba" if diferencia > 0 else "baje"
        futuro = f"los economistas esperan que {accion} a {bc.tasa(_TPM_ESPERADA)} en un año"
    return f"{hoy} y {futuro}."


def _texto_actividad() -> str:
    desempleo = bc.verbo(_DESEMPLEO_12M, 0.1, igual="se mantiene").replace(NBSP + "%", " pp")
    economia = (
        f"creció {bc.pct(_IMACEC.valor)}" if _IMACEC.valor >= 0 else f"se contrajo {bc.pct(abs(_IMACEC.valor))}"
    )
    return (
        f"El desempleo llegó a {bc.pct(_DESEMPLEO.ultimo.valor)} ({desempleo} en un año) y la economía "
        f"{economia} en 12 meses, según el IMACEC de {bc.mes(_IMACEC.fecha)}."
    )


def _texto_dolar() -> str:
    return (
        f"El dólar {bc.verbo(_DOLAR_SEMANA, 0.3)} en la semana y el cobre "
        f"{bc.verbo(_COBRE_SEMANA, 0.5)}."
    )


_IND_TPM, _PRESION_TPM = bc.indicador(
    "tpm", "Tasa de política monetaria", bc.tasa(_TPM.ultimo.valor),
    bc.puntos_porcentuales(_TPM_CAMBIO).capitalize() + " en el mes",
    "La tasa que fija el Banco Central y guía al resto de las tasas. La franja es su rango de los últimos 5 años.",
)
_IND_HIPOTECARIA, _ = bc.indicador(
    "tasa_hipotecaria", "Tasa hipotecaria promedio", f"UF + {bc.tasa(_HIPOTECARIA.ultimo.valor)}",
    f"{bc.puntos_porcentuales(_HIPOTECARIA.ultimo.valor - _HIPOTECARIA.antes_de(28).valor)} en 4 semanas",
    "Tasa promedio de los créditos para vivienda en UF a más de 3 años (dato semanal).",
)
_IND_DESEMPLEO, _PRESION_DESEMPLEO = bc.indicador(
    "desempleo", "Tasa de desempleo", bc.pct(_DESEMPLEO.ultimo.valor),
    f"{bc.puntos_porcentuales(_DESEMPLEO_12M)} en 12 meses",
    f"Trimestre móvil terminado en {bc.mes(_DESEMPLEO.ultimo.fecha)} (INE).",
    dato_al=bc.fin_de_mes(_DESEMPLEO.ultimo.fecha),
)
_IND_IMACEC, _PRESION_IMACEC = bc.indicador(
    "imacec_12m", "IMACEC", bc.pct(_IMACEC.valor, signo=True), "en 12 meses",
    "Crecimiento de la actividad económica respecto del mismo mes del año anterior.",
    invertida=True, dato_al=bc.fin_de_mes(_IMACEC.fecha),
)
_IND_IPC, _PRESION_IPC = bc.indicador(
    "ipc_mensual", "IPC mensual", bc.pct(_IPC.valor), f"{bc.pct(_IPC_12M.valor)} en 12 meses",
    f"Variación de los precios al consumidor en {bc.mes(_IPC.fecha)}. La presión se mide con la variación en 12 meses.",
    serie_presion="ipc_12m", dato_al=bc.fin_de_mes(_IPC.fecha),
)
_IND_DOLAR, _PRESION_DOLAR = bc.indicador(
    "dolar", "Dólar observado", bc.pesos(_DOLAR.ultimo.valor), f"{bc.pct(_DOLAR_SEMANA, signo=True)} semanal",
    "Tipo de cambio que publica el Banco Central cada día hábil.",
)
_IND_COBRE, _ = bc.indicador(
    "cobre", "Cobre", f"US$ {bc.numero(_COBRE.ultimo.valor, 2)} la libra",
    f"{bc.pct(_COBRE_SEMANA, signo=True)} semanal",
    "Precio del cobre refinado en la Bolsa de Metales de Londres. Un cobre alto suele bajar el dólar.",
    invertida=True,
)
_PRESION_ACTIVIDAD = la_mas_alta(_PRESION_DESEMPLEO, _PRESION_IMACEC)


def _etiqueta(presion: Presion) -> str:
    return f"Presión {presion.value}"

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
        presion=_PRESION_TPM,
        etiqueta_presion=_etiqueta(_PRESION_TPM),
        tendencia=bc.tendencia(_TPM_CAMBIO, 0.01),
        dato_clave=f"Tasa del Banco Central: {bc.tasa(_TPM.ultimo.valor)}",
        frase=_texto_tpm(),
        dato_al=_TPM.ultimo.fecha,
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
        presion=_PRESION_ACTIVIDAD,
        etiqueta_presion=_etiqueta(_PRESION_ACTIVIDAD),
        tendencia=bc.tendencia(_DESEMPLEO_12M, 0.1),
        dato_clave=f"Desempleo: {bc.pct(_DESEMPLEO.ultimo.valor)}",
        frase=_texto_actividad(),
        dato_al=bc.fin_de_mes(_DESEMPLEO.ultimo.fecha),
        proxima_actualizacion=date(2026, 10, 30),
        fuentes=["INE", "Banco Central"],
    ),
    Termometro(
        id="dolar",
        nombre="Dólar y mercados",
        pregunta="¿Qué pasa afuera?",
        presion=_PRESION_DOLAR,
        etiqueta_presion=_etiqueta(_PRESION_DOLAR),
        tendencia=bc.tendencia(_DOLAR_SEMANA, 0.3),
        dato_clave=f"Dólar observado: {bc.pesos(_DOLAR.ultimo.valor)}",
        frase=_texto_dolar(),
        dato_al=_DOLAR.ultimo.fecha,
        proxima_actualizacion=_DOLAR.ultimo.fecha + timedelta(days=3 if _DOLAR.ultimo.fecha.weekday() == 4 else 1),
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
            _IND_IPC,
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
            nombre="Percepción económica (IPEC)",
            valor=f"{bc.numero(_IPEC.valor)} puntos en {bc.mes(_IPEC.fecha)}",
            descripcion="Bajo 50 significa más pesimismo que optimismo.",
            fuente="GfK Chile, vía Banco Central",
        ),
        proximas_publicaciones=[
            Publicacion(fecha=date(2026, 10, 16), nombre="Precios de alimentos", fuente="ODEPA"),
            Publicacion(fecha=date(2026, 11, 9), nombre="IPC de octubre", fuente="INE"),
        ],
        herramienta_relacionada="Tu inflación personal",
    ),
    "deudas": dict(
        explicacion=(
            f"{_texto_tpm()} Un crédito de consumo cuesta en promedio "
            f"{bc.tasa(bc.SERIES['tasa_consumo'].ultimo.valor)} al año y uno hipotecario, "
            f"UF + {bc.tasa(_HIPOTECARIA.ultimo.valor)}."
        ),
        indicadores=[_IND_TPM, _IND_HIPOTECARIA],
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
        explicacion=_texto_actividad(),
        indicadores=[_IND_DESEMPLEO, _IND_IMACEC],
        percepcion=None,
        proximas_publicaciones=[
            Publicacion(fecha=date(2026, 10, 30), nombre="Desempleo julio-septiembre", fuente="INE"),
            Publicacion(fecha=date(2026, 11, 2), nombre="IMACEC de septiembre", fuente="Banco Central"),
        ],
        herramienta_relacionada="¿Mi sueldo le ganó a la inflación?",
    ),
    "dolar": dict(
        explicacion=_texto_dolar() + " Un cobre más caro trae más dólares al país y suele bajar su precio.",
        indicadores=[_IND_DOLAR, _IND_COBRE],
        percepcion=None,
        proximas_publicaciones=[
            Publicacion(fecha=_DOLAR.ultimo.fecha + timedelta(days=3 if _DOLAR.ultimo.fecha.weekday() == 4 else 1), nombre="Dólar observado", fuente="Banco Central"),
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
