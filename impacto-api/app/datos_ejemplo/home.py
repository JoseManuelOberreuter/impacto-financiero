"""Datos del home.

Reúne lo que muestran las demás secciones: la canasta y los productos salen de
la foto real de ODEPA (ver precios.py) y los termómetros de termometros.py.
"Lo que cambió esta semana" elige, entre todos los datos, los que más presionan
(ver _cambios).
"""

from dataclasses import dataclass
from datetime import date

from app.calculos import movimiento as mov
from app.calculos.presion import evaluar
from app.datos_ejemplo import banco_central as bc
from app.datos_ejemplo import cmf, cne
from app.datos_ejemplo.impacto import impacto
from app.datos_ejemplo.precios import CANASTA, PRODUCTOS, PRODUCTOS_POR_ID, con_articulo, es_plural
from app.datos_ejemplo.termometros import TERMOMETROS, termometro_de_ejemplo
from app.modelos.home import CambioSemana, Efecto, Home, Resumen, Tono
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


# Cuántos datos se pueden anclar como máximo en el Inicio (el límite por plan lo da la app).
MAX_ANCLADOS = 10

# Qué significa que cada dato suba, para el color de la flecha (docs/termometros.md).
_EFECTO = {
    "bencina": Efecto.sube_malo, "gas": Efecto.sube_malo, "uf": Efecto.sube_malo,
    "tmc": Efecto.sube_malo, "tpm": Efecto.sube_malo, "tasa_hipotecaria": Efecto.sube_malo,
    "ipc_mensual": Efecto.sube_malo, "desempleo": Efecto.sube_malo,
    "imacec_12m": Efecto.sube_bueno, "ipec": Efecto.sube_bueno, "imce": Efecto.sube_bueno,
    "dolar": Efecto.neutro, "cobre": Efecto.neutro, "petroleo": Efecto.neutro,
}


def _tono(direccion: Tendencia, efecto: Efecto) -> Tono:
    if efecto is Efecto.neutro or direccion is Tendencia.estable:
        return Tono.neutral
    sube = direccion is Tendencia.sube
    return Tono.favorable if sube == (efecto is Efecto.sube_bueno) else Tono.desfavorable


def _puntos_serie(id_: str) -> list[tuple]:
    return [(p.fecha, p.valor) for p in bc.SERIES[id_].puntos]


def _movimiento(id_: str) -> float:
    """Movimiento inusual del dato (app/calculos/movimiento.py), con el mismo cambio que muestra la fila."""
    s = bc.SERIES
    if id_ in PRODUCTOS_POR_ID:
        p = PRODUCTOS_POR_ID[id_]
        return mov.movimiento(p.variacion_semanal, mov.variaciones([x.precio for x in p.serie]))
    if id_ in ("dolar", "cobre", "petroleo"):
        clave = "petroleo_wti" if id_ == "petroleo" else id_
        serie = s[clave]
        actual = bc.variacion(serie.ultimo.valor, serie.antes_de(7).valor)
        return mov.movimiento(actual, mov.variaciones(mov.semanal(_puntos_serie(clave))))
    if id_ == "uf":
        uf = s["uf"]
        actual = bc.variacion(uf.ultimo.valor, uf.antes_de(30).valor)
        return mov.movimiento(actual, mov.variaciones(mov.mensual(_puntos_serie("uf"))))
    if id_ in ("tpm", "tasa_hipotecaria"):
        serie = s[id_]
        dias = 30 if id_ == "tpm" else 28
        actual = serie.ultimo.valor - serie.antes_de(dias).valor
        return mov.movimiento(actual, mov.diferencias(mov.mensual(_puntos_serie(id_))))
    if id_ == "bencina":
        mensual = [v for _, v in cne.mensual("bencina95")]
        actual = bc.variacion(cne.hoy("bencina95")["mediana"], mensual[-1])
        return mov.movimiento(actual, mov.variaciones(mensual))
    if id_ == "gas":
        mensual = [v for _, v in cne.mensual("glp15_corriente")]
        cambios = mov.variaciones(mensual)
        return mov.movimiento(cambios[-1], cambios)
    if id_ == "tmc":
        valores = [v for _, v in cmf.tmc()]
        return mov.movimiento(valores[-1] - valores[-2], mov.diferencias(valores))
    if id_ == "ipc_mensual":
        valores = [p.valor for p in s["ipc_12m"].puntos]
        return mov.movimiento(valores[-1] - valores[-2], mov.diferencias(valores))
    if id_ == "desempleo":
        valores = [p.valor for p in s["desempleo"].puntos]
        cambios = mov.diferencias(valores, paso=12)
        return mov.movimiento(cambios[-1], cambios)
    if id_ in ("imacec_12m", "ipec", "imce"):
        valores = [p.valor for p in s[id_].puntos]
        return mov.movimiento(valores[-1] - valores[-2], mov.diferencias(valores))
    return 0.0


@dataclass(frozen=True)
class Candidato:
    fila: CambioSemana
    tema: str
    mensual: bool = False

    def __post_init__(self) -> None:
        # Los alimentos (id del producto de ODEPA) suben = malo para el bolsillo.
        efecto = Efecto.sube_malo if self.tema == "alimentos" else _EFECTO.get(self.fila.id, Efecto.neutro)
        fila = self.fila.model_copy(
            update={
                "tema": self.tema,
                "efecto": efecto,
                "tono": _tono(self.fila.direccion, efecto),
                "movimiento": round(_movimiento(self.fila.id), 2),
            }
        )
        object.__setattr__(self, "fila", fila)


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


def _candidatos(todos_los_alimentos: bool = False) -> list[Candidato]:
    """Todos los datos que pueden entrar a "Lo que cambió esta semana".

    En el Inicio compite un solo alimento (el que más se movió); en "Todos los datos" van los 10.
    """
    s = bc.SERIES
    mas_movido = max(PRODUCTOS, key=lambda p: abs(p.variacion_semanal))
    alimentos = PRODUCTOS if todos_los_alimentos else [mas_movido]
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
        *[Candidato(_cambio_producto(p), "alimentos") for p in alimentos],
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


_ORDEN_PRESION = {Presion.alta: 0, Presion.media: 1, Presion.baja: 2}


def _por_presion(candidatos: list[Candidato]) -> list[Candidato]:
    """Presión alta primero; en cada nivel, los que se movieron antes que los estables."""
    return [
        c for _, c in sorted(
            enumerate(candidatos),
            key=lambda par: (_ORDEN_PRESION[par[1].fila.presion], par[1].fila.direccion is Tendencia.estable, par[0]),
        )
    ]


def todos_los_datos() -> list[CambioSemana]:
    """Todos los datos, ordenados por presión (pantalla "Todos los datos")."""
    return [c.fila for c in _por_presion(_candidatos(todos_los_alimentos=True))]


# Un dato mensual entra solo si su último cambio fue al menos así de inusual: si no,
# aparecería todo el mes con el mismo cambio. Pendiente: usar su fecha de publicación.
MOVIMIENTO_MINIMO_MENSUAL = 1.0
# Por tema, cuántos datos como máximo (los alimentos ya los resume la canasta).
_MAX_POR_TEMA = {"alimentos": 1}


def _cambios(anclados: list[str] | None = None) -> list[CambioSemana]:
    """Los anclados por el usuario arriba, y después lo que más se movió.

    Reglas (docs/termometros.md):
    - Los anclados van siempre primero, en el orden en que se anclaron, y cuentan para MAX_CAMBIOS.
    - El resto se ordena por movimiento inusual (veces lo habitual), suba o baje.
    - Máximo MAX_POR_TEMA por tema y un solo alimento.
    - Los datos mensuales entran solo si su último cambio fue inusual (MOVIMIENTO_MINIMO_MENSUAL).
    """
    todos = _candidatos(todos_los_alimentos=True)
    por_id = {c.fila.id: c for c in todos}
    elegidos = [por_id[id_].fila for id_ in (anclados or [])[:MAX_ANCLADOS] if id_ in por_id]
    ya = {f.id for f in elegidos}

    candidatos = [
        c for c in todos
        if c.fila.id not in ya and (not c.mensual or c.fila.movimiento >= MOVIMIENTO_MINIMO_MENSUAL)
    ]
    por_tema: dict[str, int] = {}
    for c in sorted(candidatos, key=lambda c: c.fila.movimiento, reverse=True):
        if len(elegidos) >= MAX_CAMBIOS:
            break
        if por_tema.get(c.tema, 0) >= _MAX_POR_TEMA.get(c.tema, MAX_POR_TEMA):
            continue
        por_tema[c.tema] = por_tema.get(c.tema, 0) + 1
        elegidos.append(c.fila)
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


def home_de_ejemplo(anclados: list[str] | None = None) -> Home:
    return Home(
        generado_el=date.today(),
        datos_de_ejemplo=True,
        resumen=Resumen(
            titulo=_titulo(),
            texto=_texto_resumen(),
        ),
        impacto=impacto(),
        canasta=CANASTA,
        cambios=_cambios(anclados),
        termometros=TERMOMETROS,
        termometros_por_defecto=["bolsillo", "deudas", "ahorro", "actividad"],
        max_termometros_home=4,
        aviso_legal=(
            "Impacto Financiero informa y explica; no es asesoría financiera, "
            "tributaria ni de inversión."
        ),
    )
