"""Datos del home.

Reúne lo que muestran las demás secciones: la canasta y los productos salen de
la foto real de ODEPA (ver precios.py) y los termómetros de termometros.py.
"Lo que cambió esta semana" elige, entre todos los datos, los que más presionan
(ver _cambios).
"""

from dataclasses import dataclass
from datetime import date

from app.calculos.presion import evaluar
from app.datos_ejemplo import banco_central as bc
from app.datos_ejemplo import cne
from app.datos_ejemplo.precios import CANASTA, PRODUCTOS, con_articulo, es_plural
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
# "Lo que cambió esta semana": cuántas filas y cuántas como máximo de un mismo tema.
MAX_CAMBIOS = 7
MAX_POR_TEMA = 2


@dataclass(frozen=True)
class Candidato:
    fila: CambioSemana
    tema: str
    mensual: bool = False


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


def _indicador(termometro: str, id_: str):
    return next(i for i in termometro_de_ejemplo(termometro).indicadores if i.id == id_)


def _cambio_indicador(termometro: str, indicador: str, nombre: str, detalle: str,
                      direccion: Tendencia, presion: Presion | None = None) -> CambioSemana:
    """Fila con el gráfico y la presión de un indicador que ya está en un termómetro."""
    ind = _indicador(termometro, indicador)
    return CambioSemana(
        id=indicador,
        nombre=nombre,
        detalle=detalle,
        direccion=direccion,
        presion=presion or ind.presion,
        serie=[p.valor for p in ind.serie],
        enlace=f"/termometros/{termometro}",
    )


def _cambio_bencina() -> CambioSemana:
    bencina = _indicador("bolsillo", "bencina")
    hoy, mes_anterior = bencina.serie[-1].valor, bencina.serie[-2].valor
    cambio = bc.variacion(hoy, mes_anterior)
    return _cambio_indicador(
        "bolsillo", "bencina", "Bencina 95",
        f"{bc.pesos(hoy)} el litro · {bc.pct(cambio, signo=True)} frente a {bc.mes(bencina.serie[-2].fecha)}",
        bc.tendencia(cambio, 0.5),
    )


def _cambio_gas() -> CambioSemana:
    mensual = cne.mensual("glp15_corriente")
    (fecha, hoy), (_, antes) = mensual[-1], mensual[-2]
    cambio = bc.variacion(hoy, antes)
    desde = fecha.replace(year=fecha.year - 5)
    presion, _ = evaluar(hoy, [v for f, v in mensual if f > desde])
    return CambioSemana(
        id="gas",
        nombre="Gas licuado 15 kg",
        detalle=f"{bc.pesos(round(hoy, -1))} · {bc.pct(cambio, signo=True)} en {bc.mes(fecha)}",
        direccion=bc.tendencia(cambio, 0.5),
        presion=presion,
        serie=[v for _, v in mensual[-12:]],
        enlace="/precios",
    )


def _cambio_uf() -> CambioSemana:
    uf = bc.SERIES["uf"]
    cambio = bc.variacion(uf.ultimo.valor, uf.antes_de(30).valor)
    return CambioSemana(
        id="uf",
        nombre="UF",
        detalle=f"{bc.pesos(uf.ultimo.valor)} · {bc.pct(cambio, 2, signo=True)} en el mes",
        direccion=bc.tendencia(cambio, 0.05),
        # La UF sube siempre con la inflación: su presión es la del IPC en 12 meses.
        presion=bc.SERIES["ipc_12m"].presion()[0],
        serie=[p.valor for p in uf.grafico()],
        enlace="/termometros/deudas",
    )


def _cambio_semanal(termometro: str, id_: str, nombre: str, valor: str) -> CambioSemana:
    serie = bc.SERIES[id_]
    cambio = bc.variacion(serie.ultimo.valor, serie.antes_de(7).valor)
    return _cambio_indicador(termometro, id_, nombre, f"{valor} · {bc.pct(cambio, signo=True)} en la semana",
                             bc.tendencia(cambio, 0.3))


def _cambio_tmc() -> CambioSemana:
    tmc = _indicador("deudas", "tmc")
    hoy, antes = tmc.serie[-1].valor, tmc.serie[-2].valor
    return _cambio_indicador(
        "deudas", "tmc", "Tasa máxima de los créditos",
        f"{bc.tasa(hoy)} al año · {bc.puntos_porcentuales(hoy - antes)} en el mes",
        bc.tendencia(hoy - antes, 0.05),
    )


def _cambio_mensual(termometro: str, id_: str, nombre: str, detalle: str, cambio: float,
                    umbral: float) -> CambioSemana:
    return _cambio_indicador(termometro, id_, nombre, detalle, bc.tendencia(cambio, umbral))


def _puntos(cambio: float) -> str:
    signo = "+" if cambio > 0 else "−" if cambio < 0 else ""
    return f"{signo}{bc.numero(abs(cambio))} en el mes"


def _candidatos() -> list[Candidato]:
    """Todos los datos que pueden entrar a "Lo que cambió esta semana"."""
    s = bc.SERIES
    alimento = max(PRODUCTOS, key=lambda p: abs(p.variacion_semanal))
    tpm, hipotecaria = s["tpm"], s["tasa_hipotecaria"]
    desempleo, imacec = s["desempleo"], s["imacec_12m"]
    ipc, ipc_12m = s["ipc_mensual"].ultimo, s["ipc_12m"]
    ipec, imce = s["ipec"], s["imce"]
    wti = s["petroleo_wti"]
    wti_semana = bc.variacion(wti.ultimo.valor, wti.antes_de(7).valor)
    desempleo_12m = desempleo.ultimo.valor - desempleo.antes_de(365).valor
    return [
        Candidato(_cambio_bencina(), "energia"),
        Candidato(_cambio_gas(), "energia"),
        Candidato(_cambio_producto(alimento), "alimentos"),
        Candidato(_cambio_semanal("dolar", "dolar", "Dólar", bc.pesos(s["dolar"].ultimo.valor)), "afuera"),
        Candidato(_cambio_semanal("dolar", "cobre", "Cobre", f"US$ {bc.numero(s['cobre'].ultimo.valor, 2)} la libra"),
                  "afuera"),
        Candidato(CambioSemana(
            id="petroleo",
            nombre="Petróleo WTI",
            detalle=f"US$ {bc.numero(wti.ultimo.valor)} el barril · {bc.pct(wti_semana, signo=True)} en la semana",
            direccion=bc.tendencia(wti_semana, 0.5),
            presion=wti.presion()[0],
            serie=[p.valor for p in wti.grafico()],
            enlace="/termometros/dolar",
        ), "afuera"),
        Candidato(_cambio_uf(), "deudas"),
        Candidato(_cambio_tmc(), "deudas"),
        Candidato(_cambio_mensual(
            "deudas", "tpm", "Tasa del Banco Central",
            f"{bc.tasa(tpm.ultimo.valor)} · {bc.puntos_porcentuales(tpm.ultimo.valor - tpm.antes_de(30).valor)} en el mes",
            tpm.ultimo.valor - tpm.antes_de(30).valor, 0.01,
        ), "deudas"),
        Candidato(_cambio_mensual(
            "deudas", "tasa_hipotecaria", "Tasa hipotecaria",
            f"UF + {bc.tasa(hipotecaria.ultimo.valor)} · "
            f"{bc.puntos_porcentuales(hipotecaria.ultimo.valor - hipotecaria.antes_de(28).valor)} en 4 semanas",
            hipotecaria.ultimo.valor - hipotecaria.antes_de(28).valor, 0.05,
        ), "deudas"),
        Candidato(_cambio_mensual(
            "bolsillo", "ipc_mensual", "IPC",
            f"{bc.pct(ipc.valor)} en {bc.mes(ipc.fecha)} · {bc.pct(ipc_12m.ultimo.valor)} en 12 meses",
            ipc_12m.ultimo.valor - ipc_12m.puntos[-2].valor, 0.1,
        ), "precios", mensual=True),
        Candidato(_cambio_mensual(
            "actividad", "desempleo", "Desempleo",
            f"{bc.pct(desempleo.ultimo.valor)} · {bc.puntos_porcentuales(desempleo_12m)} en 12 meses",
            desempleo_12m, 0.1,
        ), "empleo", mensual=True),
        Candidato(_cambio_mensual(
            "actividad", "imacec_12m", "IMACEC",
            f"{bc.pct(imacec.ultimo.valor, signo=True)} en 12 meses · {bc.mes(imacec.ultimo.fecha)}",
            imacec.ultimo.valor - imacec.puntos[-2].valor, 0.3,
        ), "empleo", mensual=True),
        Candidato(_cambio_mensual(
            "animo", "ipec", "Percepción de las personas",
            f"{bc.numero(ipec.ultimo.valor)} puntos · {_puntos(ipec.ultimo.valor - ipec.puntos[-2].valor)}",
            ipec.ultimo.valor - ipec.puntos[-2].valor, 1,
        ), "animo", mensual=True),
        Candidato(_cambio_mensual(
            "animo", "imce", "Confianza de las empresas",
            f"{bc.numero(imce.ultimo.valor)} puntos · {_puntos(imce.ultimo.valor - imce.puntos[-2].valor)}",
            imce.ultimo.valor - imce.puntos[-2].valor, 1,
        ), "animo", mensual=True),
    ]


def _cambios() -> list[CambioSemana]:
    """Los datos que más presionan, de todos los temas.

    Reglas (docs/termometros.md):
    - Todos los candidatos compiten; se muestran hasta MAX_CAMBIOS.
    - Orden: presión alta primero; en cada nivel, los que se movieron antes que los
      estables; en empate, el orden de la lista de candidatos.
    - Máximo MAX_POR_TEMA por tema y un solo alimento (la canasta ya los resume).
    - Los datos mensuales entran solo con presión alta, porque no cambian cada semana.
      Cuando guardemos su fecha de publicación, entrarán también la semana en que salen.
    """
    orden = {Presion.alta: 0, Presion.media: 1, Presion.baja: 2}
    candidatos = [c for c in _candidatos() if not c.mensual or c.fila.presion is Presion.alta]
    candidatos = sorted(
        enumerate(candidatos),
        key=lambda par: (orden[par[1].fila.presion], par[1].fila.direccion is Tendencia.estable, par[0]),
    )
    elegidos: list[CambioSemana] = []
    por_tema: dict[str, int] = {}
    for _, c in candidatos:
        if por_tema.get(c.tema, 0) >= MAX_POR_TEMA:
            continue
        por_tema[c.tema] = por_tema.get(c.tema, 0) + 1
        elegidos.append(c.fila)
        if len(elegidos) == MAX_CAMBIOS:
            break
    return elegidos


def _titulo() -> str:
    """Titular del día: cómo se movió la canasta y el alimento que más cambió."""
    cambio = CANASTA.variacion_semanal
    if abs(cambio) < 0.5:
        canasta = "La canasta se mantiene esta semana"
    else:
        canasta = f"La canasta {'sube' if cambio > 0 else 'baja'} {bc.pct(abs(cambio))} esta semana"
    producto = max(PRODUCTOS, key=lambda p: abs(p.variacion_semanal))
    verbo = "sube" if producto.variacion_semanal > 0 else "baja"
    if es_plural(producto):
        verbo += "n"
    return f"{canasta}; {con_articulo(producto)} {verbo} {bc.pct(abs(producto.variacion_semanal))}."


def _texto_resumen() -> str:
    tpm = bc.SERIES["tpm"]
    dolar = bc.SERIES["dolar"]
    semana = bc.variacion(dolar.ultimo.valor, dolar.antes_de(7).valor)
    movimiento = {Tendencia.sube: "subió", Tendencia.baja: "bajó", Tendencia.estable: "se mantuvo"}
    return (
        f"La tasa del Banco Central está en {bc.tasa(tpm.ultimo.valor)} y el dólar "
        f"{movimiento[bc.tendencia(semana, 0.3)]} esta semana, a {bc.pesos(dolar.ultimo.valor)}."
    )


def home_de_ejemplo() -> Home:
    return Home(
        generado_el=date.today(),
        datos_de_ejemplo=True,
        resumen=Resumen(
            titulo=_titulo(),
            texto=_texto_resumen(),
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
