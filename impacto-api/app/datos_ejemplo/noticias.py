"""Noticias de ejemplo.

Los titulares y hechos esenciales son inventados para mostrar el diseño: no se
atribuyen a medios ni a empresas reales.
"""

from datetime import date

from app.modelos.noticias import HechoEsencial, Noticias, Tema, Titular
from app.modelos.termometros import Presion, PuntoSerie, Tendencia

MEDIO = "Medio de ejemplo"


def _titular(titulo: str, dia: int) -> Titular:
    return Titular(titulo=titulo, medio=MEDIO, fecha=date(2026, 10, dia))


def noticias_de_ejemplo() -> Noticias:
    return Noticias(
        presion=Presion.alta,
        etiqueta="Más negativo que lo habitual",
        tendencia=Tendencia.baja,
        tono_semana=-18,
        serie_tono=[
            PuntoSerie(fecha=date(2026, 10, d), valor=v)
            for d, v in [(8, -9), (9, -11), (10, -10), (11, -13), (12, -15), (13, -16), (14, -18)]
        ],
        incertidumbre=22.5,
        total_titulares=412,
        medios=6,
        temas=[
            Tema(
                nombre="Desempleo",
                termometro="actividad",
                tono=-1.2,
                cantidad=58,
                titulares=[
                    _titular("Desempleo se mantiene sobre 8,5 % en la Región Metropolitana", 14),
                    _titular("Gremios piden medidas para recuperar empleos en la construcción", 13),
                ],
            ),
            Tema(
                nombre="Combustibles",
                termometro="bolsillo",
                tono=-1.0,
                cantidad=41,
                titulares=[
                    _titular("Bencinas suben por cuarta semana consecutiva", 14),
                    _titular("Qué explica el alza del gas licuado antes del invierno", 12),
                ],
            ),
            Tema(
                nombre="Tasas de interés",
                termometro="deudas",
                tono=-0.2,
                cantidad=27,
                titulares=[
                    _titular("Expertos no esperan cambios en la tasa del Banco Central este año", 13),
                ],
            ),
            Tema(
                nombre="Cobre y dólar",
                termometro="dolar",
                tono=0.6,
                cantidad=22,
                titulares=[
                    _titular("Alza del cobre ayuda a bajar el dólar", 14),
                ],
            ),
        ],
        hechos_esenciales=[
            HechoEsencial(
                entidad="Empresa de ejemplo S.A.",
                titulo="Informa reparto de dividendo provisorio",
                resumen="La empresa pagará a sus accionistas parte de las utilidades del año.",
                fecha=date(2026, 10, 14),
            ),
            HechoEsencial(
                entidad="Banco de ejemplo",
                titulo="Comunica cambio de gerente general",
                resumen="El banco cambió a su máxima autoridad ejecutiva; no informa cambios de estrategia.",
                fecha=date(2026, 10, 13),
            ),
        ],
        dato_al=date(2026, 10, 14),
        nota=(
            "Titulares y hechos esenciales de ejemplo. En producción se mostrará solo el titular "
            "con enlace a la nota original (ver docs/sentimiento-noticias.md)."
        ),
    )
