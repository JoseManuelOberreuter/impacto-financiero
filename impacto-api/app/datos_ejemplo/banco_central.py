"""Datos reales del Banco Central, leídos de la foto bcch_snapshot.json.

La foto se genera con scripts/snapshot_bcch.py. Aquí se arman los indicadores:
valor, variación, presión respecto de los últimos 5 años, banda normal y gráfico.
Cuando exista la base de datos, estas mismas funciones leerán de ahí.
"""

import json
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

from app.calculos.presion import evaluar
from app.modelos.termometros import Indicador, Presion, PuntoSerie, Tendencia

NBSP = " "
FUENTE = "Banco Central"
_FOTO = json.loads((Path(__file__).parent / "bcch_snapshot.json").read_text(encoding="utf-8"))
DESCARGADO_EL = date.fromisoformat(_FOTO["descargado_el"])


@dataclass(frozen=True)
class Punto:
    fecha: date
    valor: float


class Serie:
    def __init__(self, id_: str):
        datos = _FOTO["series"][id_]
        self.id = id_
        self.nombre = datos["nombre"]
        self.diaria = datos["codigo"].endswith(".D")
        hoy = max(date.today(), DESCARGADO_EL)
        # La UF se publica por adelantado: solo se usa hasta hoy.
        self.puntos = [
            Punto(date.fromisoformat(f), v) for f, v in datos["observaciones"] if date.fromisoformat(f) <= hoy
        ]

    @property
    def ultimo(self) -> Punto:
        return self.puntos[-1]

    def antes_de(self, dias: int) -> Punto:
        """Último dato publicado al menos `dias` antes del más reciente."""
        limite = self.ultimo.fecha - timedelta(days=dias)
        return next(p for p in reversed(self.puntos) if p.fecha <= limite)

    def historia(self, anios: int = 5) -> list[float]:
        desde = self.ultimo.fecha.replace(year=self.ultimo.fecha.year - anios)
        return [p.valor for p in self.puntos if p.fecha > desde]

    def grafico(self) -> list[PuntoSerie]:
        """Últimos 12 meses: un punto por semana en las diarias, por mes en las mensuales."""
        if not self.diaria:
            return [PuntoSerie(fecha=p.fecha, valor=p.valor) for p in self.puntos[-12:]]
        desde = self.ultimo.fecha - timedelta(days=365)
        por_semana: dict[tuple[int, int], Punto] = {}
        for p in self.puntos:
            if p.fecha > desde:
                por_semana[p.fecha.isocalendar()[:2]] = p
        return [PuntoSerie(fecha=p.fecha, valor=p.valor) for p in por_semana.values()]

    def presion(self, invertida: bool = False):
        return evaluar(self.ultimo.valor, self.historia(), invertida)


SERIES = {id_: Serie(id_) for id_ in _FOTO["series"]}


def numero(valor: float, decimales: int = 1) -> str:
    return f"{valor:,.{decimales}f}".replace(",", "_").replace(".", ",").replace("_", ".")


def pct(valor: float, decimales: int = 1, signo: bool = False) -> str:
    texto = numero(abs(valor) if signo else valor, decimales)
    if signo:
        texto = ("+" if valor > 0 else "−" if valor < 0 else "") + texto
    elif valor < 0:
        texto = "−" + texto.lstrip("-")
    return f"{texto}{NBSP}%"


def tasa(valor: float) -> str:
    """Tasa con hasta 2 decimales, sin ceros de más: 4,5 % o 4,25 %."""
    texto = numero(valor, 2).rstrip("0").rstrip(",")
    return f"{texto}{NBSP}%"


def pesos(valor: float) -> str:
    return "$" + numero(valor, 0)


def puntos_porcentuales(diferencia: float) -> str:
    if abs(diferencia) < 0.05:
        return "sin cambio"
    signo = "+" if diferencia > 0 else "−"
    return f"{signo}{numero(abs(diferencia))} pp"


def variacion(actual: float, anterior: float) -> float:
    return (actual / anterior - 1) * 100


def tendencia(cambio: float, umbral: float) -> Tendencia:
    if cambio > umbral:
        return Tendencia.sube
    if cambio < -umbral:
        return Tendencia.baja
    return Tendencia.estable


def verbo(cambio: float, umbral: float, sube: str = "subió", baja: str = "bajó", igual: str = "se mantuvo") -> str:
    t = tendencia(cambio, umbral)
    if t is Tendencia.sube:
        return f"{sube} {pct(abs(cambio))}"
    if t is Tendencia.baja:
        return f"{baja} {pct(abs(cambio))}"
    return igual


def fin_de_mes(fecha: date) -> date:
    siguiente = (fecha.replace(day=28) + timedelta(days=4)).replace(day=1)
    return siguiente - timedelta(days=1)


_MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
          "septiembre", "octubre", "noviembre", "diciembre"]


def mes(fecha: date) -> str:
    return _MESES[fecha.month - 1]


def indicador(id_: str, nombre: str, valor: str, variacion_texto: str | None, descripcion: str,
              invertida: bool = False, serie_presion: str | None = None,
              dato_al: date | None = None) -> tuple[Indicador, Presion]:
    """Indicador con gráfico de su serie y presión de `serie_presion` (por defecto, la misma)."""
    serie = SERIES[id_]
    presion, banda = SERIES[serie_presion or id_].presion(invertida)
    if serie_presion and serie_presion != id_:
        banda = None  # la banda es de otra serie: no se dibuja sobre este gráfico
    resultado = Indicador(
        id=id_,
        nombre=nombre,
        valor=valor,
        variacion=variacion_texto,
        presion=presion,
        descripcion=descripcion,
        serie=serie.grafico(),
        banda_normal=banda,
        fuente=FUENTE,
        dato_al=dato_al or serie.ultimo.fecha,
    )
    return resultado, presion
