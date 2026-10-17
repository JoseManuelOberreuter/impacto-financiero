"""Termómetros de ejemplo.

Todos los indicadores vienen de fotos reales de las fuentes: ODEPA (alimentos),
Superintendencia de Pensiones (AFP), Banco Central (IPC, TPM, tasas, desempleo,
IMACEC, dólar, cobre, IPEC e IMCE), CNE (bencina) y CMF (tasa máxima
convencional). La presión se calcula sobre la historia de cada indicador.
Pendientes: el tono de las noticias (falta la prensa) y la presión de las AFP
(falta guardar su historia).
"""

import json
import statistics
from datetime import date, timedelta
from pathlib import Path

from app.calculos.presion import evaluar, la_mas_alta
from app.datos_ejemplo import banco_central as bc
from app.datos_ejemplo import cmf, cne
from app.datos_ejemplo.impacto import impacto
from app.datos_ejemplo.precios import CANASTA, PRODUCTOS, PRODUCTOS_POR_ID, con_articulo
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
# --- Bencina: foto real de la CNE ---

_BENCINA_HOY = cne.hoy("bencina95")
_BENCINA_MES = cne.mensual("bencina95")
_BENCINA_ULTIMO_MES = _BENCINA_MES[-1]
_PRESION_BENCINA, _BANDA_BENCINA = evaluar(
    _BENCINA_HOY["mediana"],
    [v for f, v in _BENCINA_MES if f > cne.DESCARGADO_EL.replace(year=cne.DESCARGADO_EL.year - 5)],
)
_IND_BENCINA = Indicador(
    id="bencina",
    nombre="Bencina 95",
    valor=f"{_pesos(_BENCINA_HOY['mediana'])} / litro",
    variacion=(
        f"{_pct(bc.variacion(_BENCINA_HOY['mediana'], _BENCINA_ULTIMO_MES[1]))} frente a "
        f"{bc.mes(_BENCINA_ULTIMO_MES[0])}"
    ),
    presion=_PRESION_BENCINA,
    descripcion=(
        f"Hoy: mediana de {_BENCINA_HOY['estaciones_frescas']} estaciones de Santiago con precio actualizado "
        "en la última semana. El gráfico muestra el promedio mensual de la Región Metropolitana."
    ),
    serie=[PuntoSerie(fecha=f, valor=v) for f, v in _BENCINA_MES if f > cne.DESCARGADO_EL - timedelta(days=365)]
    + [PuntoSerie(fecha=cne.DESCARGADO_EL, valor=_BENCINA_HOY["mediana"])],
    banda_normal=_BANDA_BENCINA,
    fuente="CNE",
    dato_al=cne.DESCARGADO_EL,
)
_PCT_ENERGIA = round(
    sum(i.porcentaje for i in CANASTA.composicion if "bencina" in i.nombre or "gas" in i.nombre)
)

# --- Tasa máxima convencional: foto real de la CMF ---

_TMC = cmf.tmc()
_TMC_FECHA, _TMC_HOY = _TMC[-1]
_TMC_HACE_UN_ANIO = next(v for f, v in reversed(_TMC) if f <= _TMC_FECHA.replace(year=_TMC_FECHA.year - 1))
_PRESION_TMC, _BANDA_TMC = evaluar(
    _TMC_HOY, [v for f, v in _TMC if f > _TMC_FECHA.replace(year=_TMC_FECHA.year - 5)]
)
_IND_TMC = Indicador(
    id="tmc",
    nombre="Tasa máxima convencional",
    valor=f"{bc.tasa(_TMC_HOY)} al año",
    variacion=f"{bc.puntos_porcentuales(_TMC_HOY - _TMC_HACE_UN_ANIO)} en 12 meses",
    presion=_PRESION_TMC,
    descripcion=(
        "Lo máximo que la ley permite cobrar en un crédito en pesos de 50 a 200 UF a más de 90 días, "
        "como un crédito de consumo. La fija la CMF cada mes."
    ),
    serie=[PuntoSerie(fecha=f, valor=v) for f, v in _TMC[-12:]],
    banda_normal=_BANDA_TMC,
    fuente=cmf.FUENTE,
    dato_al=_TMC_FECHA,
)
_PRESION_DEUDAS = la_mas_alta(_PRESION_TPM, _PRESION_TMC)

# --- Ánimo: percepción de personas (IPEC) y empresas (IMCE), del Banco Central ---

_IMCE = bc.SERIES["imce"]
_IPEC_SERIE = bc.SERIES["ipec"]


def _cambio_mensual(serie: bc.Serie) -> float:
    return serie.ultimo.valor - serie.puntos[-2].valor


def _puntos(cambio: float) -> str:
    signo = "+" if cambio > 0 else "−" if cambio < 0 else ""
    return f"{signo}{bc.numero(abs(cambio))} puntos frente al mes anterior"


_IND_IPEC, _PRESION_IPEC = bc.indicador(
    "ipec", "Percepción de las personas (IPEC)", f"{bc.numero(_IPEC.valor)} puntos",
    _puntos(_cambio_mensual(_IPEC_SERIE)),
    "Encuesta de GfK Chile sobre cómo ven las personas su situación y la del país. "
    "Bajo 50 hay más pesimismo que optimismo.",
    invertida=True, dato_al=bc.fin_de_mes(_IPEC.fecha),
)
_IND_IMCE, _PRESION_IMCE = bc.indicador(
    "imce", "Confianza de las empresas (IMCE)", f"{bc.numero(_IMCE.ultimo.valor)} puntos",
    _puntos(_cambio_mensual(_IMCE)),
    "Indicador de ICARE y la Universidad Adolfo Ibáñez sobre la confianza de los empresarios. "
    "Bajo 50 hay más pesimismo que optimismo.",
    invertida=True, dato_al=bc.fin_de_mes(_IMCE.ultimo.fecha),
)
_PRESION_ANIMO = la_mas_alta(_PRESION_IPEC, _PRESION_IMCE)


def _texto_animo() -> str:
    def lectura(valor: float) -> str:
        return "pesimistas" if valor < 45 else "optimistas" if valor > 55 else "en un punto neutro"

    return (
        f"Las personas están {lectura(_IPEC.valor)} ({bc.numero(_IPEC.valor)} puntos) y las empresas, "
        f"{lectura(_IMCE.ultimo.valor)} ({bc.numero(_IMCE.ultimo.valor)}), en una escala donde 50 es neutro."
    )


# --- Textos de Bolsillo y Ahorro a partir de los datos ---


def _nombres(lista: list) -> str:
    nombres = [con_articulo(p) for p in lista]
    return nombres[0] if len(nombres) == 1 else ", ".join(nombres[:-1]) + " y " + nombres[-1]


def _texto_alimentos() -> str:
    bajaron = sorted([p for p in PRODUCTOS if p.variacion_semanal <= -0.5], key=lambda p: p.variacion_semanal)[:3]
    subieron = sorted([p for p in PRODUCTOS if p.variacion_semanal >= 0.5], key=lambda p: -p.variacion_semanal)[:3]
    partes = []
    if bajaron:
        partes.append(f"bajaron {_nombres(bajaron)}")
    if subieron:
        partes.append(f"subieron {_nombres(subieron)}")
    if not partes:
        return "Los alimentos casi no cambiaron de precio esta semana."
    texto = "; ".join(partes)
    return texto[0].upper() + texto[1:] + "."


def _texto_canasta() -> str:
    cambio = CANASTA.variacion_semanal
    if abs(cambio) < 0.5:
        return f"La canasta se mantuvo esta semana ({_pct(cambio)})."
    return f"La canasta {'subió' if cambio > 0 else 'bajó'} {bc.pct(abs(cambio))} esta semana."


def _texto_fondos() -> str:
    a, e = _mediana_fondo("A", "mes"), _mediana_fondo("E", "mes")
    return (
        f"En el último mes el Fondo A, el más riesgoso, {'ganó' if a >= 0 else 'perdió'} {bc.pct(abs(a))} "
        f"y el Fondo E, el más conservador, {'ganó' if e >= 0 else 'perdió'} {bc.pct(abs(e))}."
    )


_PRESION_MARRAQUETA, _BANDA_MARRAQUETA = evaluar(_MARRAQUETA.precio, [p.precio for p in _MARRAQUETA.serie])
_PRESION_CANASTA, _ = evaluar(CANASTA.total, [p.precio for p in CANASTA.serie])

# --- Impacto Financiero: la inflación en pesos para un hogar típico (impacto.py) ---

_IMPACTO = impacto()


def _ipc_12m(id_: str, nombre: str, descripcion: str) -> tuple[Indicador, Presion]:
    """Variación en 12 meses de un índice de IPC por división, con su historia como gráfico."""
    puntos = bc.SERIES[id_].puntos
    por_mes = {(p.fecha.year, p.fecha.month): p.valor for p in puntos}
    serie = [
        PuntoSerie(fecha=p.fecha, valor=(p.valor / por_mes[(p.fecha.year - 1, p.fecha.month)] - 1) * 100)
        for p in puntos
        if (p.fecha.year - 1, p.fecha.month) in por_mes
    ]
    presion, banda = evaluar(serie[-1].valor, [p.valor for p in serie])
    return Indicador(
        id=id_,
        nombre=nombre,
        valor=bc.pct(serie[-1].valor, signo=True),
        variacion="en 12 meses",
        presion=presion,
        descripcion=descripcion,
        serie=serie[-12:],
        banda_normal=banda,
        fuente="INE, vía Banco Central",
        dato_al=bc.fin_de_mes(serie[-1].fecha),
    ), presion


_IND_IPC_TRANSPORTE, _ = _ipc_12m("ipc_transporte", "IPC de transporte", "Combustibles, pasajes y vehículos.")
_IND_IPC_ALIMENTOS, _ = _ipc_12m("ipc_alimentos", "IPC de alimentos", "Alimentos y bebidas no alcohólicas.")
_IND_IPC_VIVIENDA, _ = _ipc_12m("ipc_vivienda", "IPC de vivienda y servicios básicos", "Arriendo, luz, agua y gas.")
_PRESION_IMPACTO = bc.SERIES["ipc_12m"].presion()[0]


def _signo_pesos(valor: float) -> str:
    return ("+" if valor > 0 else "−" if valor < 0 else "") + _pesos(abs(valor))


def _texto_impacto() -> str:
    mayor = max((r for r in _IMPACTO.rubros if r.id != "otros"), key=lambda r: r.diferencia_anual)
    return (
        f"Un hogar típico de Santiago gasta {_pesos(abs(_IMPACTO.diferencia_anual))} "
        f"{'más' if _IMPACTO.diferencia_anual >= 0 else 'menos'} al mes que hace un año. "
        f"Lo que más subió fue {mayor.nombre.lower()} ({bc.pct(mayor.variacion_anual, signo=True)})."
    )


_PRESION_BOLSILLO = la_mas_alta(_PRESION_IPC, _PRESION_BENCINA)
_PRESION_ACTIVIDAD = la_mas_alta(_PRESION_DESEMPLEO, _PRESION_IMACEC)


def _etiqueta(presion: Presion) -> str:
    return f"Presión {presion.value}"

TERMOMETROS = [
    Termometro(
        id="impacto",
        nombre="Impacto Financiero",
        pregunta="¿Cuánto más me cuesta vivir?",
        presion=_PRESION_IMPACTO,
        etiqueta_presion=_etiqueta(_PRESION_IMPACTO),
        tendencia=bc.tendencia(_IMPACTO.diferencia_mensual, 0),
        dato_clave=f"{_signo_pesos(_IMPACTO.diferencia_anual)} al mes que hace un año",
        frase=_texto_impacto(),
        dato_al=_IMPACTO.actualizado_al,
        proxima_actualizacion=None,
        fuentes=["INE", "Banco Central"],
    ),
    Termometro(
        id="bolsillo",
        nombre="Bolsillo",
        pregunta="¿Está más cara la vida?",
        presion=_PRESION_BOLSILLO,
        etiqueta_presion=_etiqueta(_PRESION_BOLSILLO),
        tendencia=bc.tendencia(CANASTA.variacion_semanal, 0.5),
        dato_clave=f"Canasta semanal: {_pesos(CANASTA.total)} ({_pct(CANASTA.variacion_semanal)})",
        frase=_texto_alimentos(),
        dato_al=CANASTA.dato_al,
        proxima_actualizacion=date(2026, 10, 16),
        fuentes=["ODEPA", "CNE", "Panel de Expertos"],
    ),
    Termometro(
        id="deudas",
        nombre="Deudas",
        pregunta="¿Está más caro endeudarse?",
        presion=_PRESION_DEUDAS,
        etiqueta_presion=_etiqueta(_PRESION_DEUDAS),
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
        frase=_texto_fondos(),
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
        pregunta="¿Cómo se siente la gente?",
        presion=_PRESION_ANIMO,
        etiqueta_presion=_etiqueta(_PRESION_ANIMO),
        tendencia=bc.tendencia(_cambio_mensual(_IPEC_SERIE), 1),
        dato_clave=f"Percepción de las personas: {bc.numero(_IPEC.valor)} puntos",
        frase=_texto_animo(),
        dato_al=bc.fin_de_mes(_IPEC.fecha),
        proxima_actualizacion=None,
        fuentes=["GfK Chile", "ICARE y UAI", "Banco Central"],
    ),
]
_POR_ID = {t.id: t for t in TERMOMETROS}

_METODOLOGIA = (
    "Cada indicador se compara con su propia historia de los últimos 5 años: si está en el "
    "20 % más alto, la presión es alta; en el 20 % más bajo, baja; y si no, media. "
    "La presión no dice si algo es bueno o malo, solo si está lejos de lo habitual."
)

_DETALLES = {
    "impacto": dict(
        explicacion=(
            f"{_texto_impacto()} Frente al mes anterior, la diferencia es de "
            f"{_signo_pesos(_IMPACTO.diferencia_mensual)}. {_IMPACTO.metodologia}"
        ),
        indicadores=[_IND_IPC_TRANSPORTE, _IND_IPC_ALIMENTOS, _IND_IPC_VIVIENDA],
        percepcion=None,
        proximas_publicaciones=[
            Publicacion(fecha=date(2026, 11, 9), nombre="IPC de octubre", fuente="INE"),
        ],
        herramienta_relacionada="Mi impacto",
        impacto=_IMPACTO,
    ),
    "bolsillo": dict(
        explicacion=(
            f"{_texto_canasta()} {_texto_alimentos()} "
            f"La bencina y el gas son el {_PCT_ENERGIA} % de la canasta; la bencina 95 está en "
            f"{_pesos(_BENCINA_HOY['mediana'])} el litro en Santiago."
        ),
        indicadores=[
            Indicador(
                id="canasta",
                nombre="Índice de canasta",
                valor=_pesos(CANASTA.total),
                variacion=f"{_pct(CANASTA.variacion_semanal)} semanal",
                presion=_PRESION_CANASTA,
                descripcion="Costo de una canasta semanal típica (indicador propio).",
                serie=[PuntoSerie(fecha=p.semana, valor=p.precio) for p in CANASTA.serie],
                # Sin banda hasta guardar la historia de la canasta completa.
                fuente="ODEPA, CNE, Panel de Expertos",
                dato_al=CANASTA.dato_al,
            ),
            Indicador(
                id="marraqueta",
                nombre="Marraqueta",
                valor=f"{_pesos(_MARRAQUETA.precio)} / kilo",
                variacion=f"{_pct(_MARRAQUETA.variacion_semanal)} semanal",
                presion=_PRESION_MARRAQUETA,
                descripcion=(
                    "Mediana de panaderías y supermercados de Santiago. La franja es su rango de las últimas "
                    "12 semanas, hasta tener más historia guardada."
                ),
                serie=_semanal_precios("marraqueta"),
                banda_normal=_BANDA_MARRAQUETA,
                fuente="ODEPA",
                dato_al=_MARRAQUETA.dato_al,
            ),
            _IND_IPC,
            _IND_BENCINA,
        ],
        percepcion=Percepcion(
            nombre="Percepción económica (IPEC)",
            valor=f"{bc.numero(_IPEC.valor)} puntos en {bc.mes(_IPEC.fecha)}",
            descripcion="Bajo 50 significa más pesimismo que optimismo.",
            fuente="GfK Chile, vía Banco Central",
        ),
        proximas_publicaciones=[
            Publicacion(fecha=CANASTA.dato_al + timedelta(days=7), nombre="Precios de alimentos", fuente="ODEPA"),
            Publicacion(fecha=date(2026, 11, 9), nombre="IPC de octubre", fuente="INE"),
        ],
        herramienta_relacionada="Tu inflación personal",
    ),
    "deudas": dict(
        explicacion=(
            f"{_texto_tpm()} Un crédito de consumo cuesta en promedio "
            f"{bc.tasa(bc.SERIES['tasa_consumo'].ultimo.valor)} al año y uno hipotecario, "
            f"UF + {bc.tasa(_HIPOTECARIA.ultimo.valor)}. Lo máximo que la ley permite cobrar en un crédito "
            f"de consumo es {bc.tasa(_TMC_HOY)} al año."
        ),
        indicadores=[_IND_TPM, _IND_TMC, _IND_HIPOTECARIA],
        percepcion=None,
        proximas_publicaciones=[
            Publicacion(fecha=date(2026, 10, 28), nombre="Reunión de política monetaria", fuente="Banco Central"),
        ],
        herramienta_relacionada="¿Cuánto sube mi dividendo?",
    ),
    "ahorro": dict(
        explicacion=(
            f"{_texto_fondos()} En lo que va del año, el Fondo A rinde "
            f"{_pct(_mediana_fondo('A', 'anio'))} y el E {_pct(_mediana_fondo('E', 'anio'))}. "
            "La presión de los fondos se calculará cuando guardemos su historia."
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
            f"{_texto_animo()} El tono de las noticias económicas se sumará cuando conectemos la prensa."
        ),
        indicadores=[_IND_IPEC, _IND_IMCE],
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
    return TermometroDetalle(**_POR_ID[id_].model_dump(), **_DETALLES[id_], metodologia=_METODOLOGIA)
