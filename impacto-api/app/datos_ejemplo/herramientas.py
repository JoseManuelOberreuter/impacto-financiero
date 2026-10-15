"""Herramientas de ejemplo.

Mi AFP usa la foto real de la Superintendencia de Pensiones (afp_snapshot.json,
generada con scripts/snapshot_afp.py). Las fechas del calendario marcadas como
estimadas siguen el patrón habitual de publicación y deben confirmarse.
"""

import json
from datetime import date
from pathlib import Path

from app.modelos.herramientas import (
    Calculadora,
    EventoCalendario,
    Herramientas,
    MiAfp,
    SeccionMetodologia,
)

_AFP = json.loads((Path(__file__).parent / "afp_snapshot.json").read_text(encoding="utf-8"))

CALCULADORAS = [
    Calculadora(
        id="dividendo",
        nombre="¿Cuánto sube mi dividendo?",
        descripcion="Estima cómo cambia tu dividendo o crédito en UF con la inflación.",
        disponible=False,
    ),
    Calculadora(
        id="sueldo",
        nombre="¿Mi sueldo le ganó a la inflación?",
        descripcion="Compara la variación de tu sueldo con la del IPC.",
        disponible=False,
    ),
    Calculadora(
        id="inflacion-personal",
        nombre="Tu inflación personal",
        descripcion="Calcula tu inflación según cómo gastas, y compárala con la oficial.",
        disponible=False,
    ),
    Calculadora(
        id="deposito",
        nombre="Depósito a plazo vs. inflación",
        descripcion="Revisa si tu depósito realmente gana o pierde frente al IPC.",
        disponible=False,
    ),
]

CALENDARIO = [
    EventoCalendario(fecha=date(2026, 10, 15), nombre="Dólar observado", fuente="Banco Central", termometro="dolar", estimada=False),
    EventoCalendario(fecha=date(2026, 10, 16), nombre="Precios de alimentos", fuente="ODEPA", termometro="bolsillo", estimada=False),
    EventoCalendario(fecha=date(2026, 10, 28), nombre="Reunión de política monetaria", fuente="Banco Central", termometro="deudas", estimada=True),
    EventoCalendario(fecha=date(2026, 10, 30), nombre="Desempleo julio-septiembre", fuente="INE", termometro="actividad", estimada=True),
    EventoCalendario(fecha=date(2026, 11, 2), nombre="IMACEC de septiembre", fuente="Banco Central", termometro="actividad", estimada=True),
    EventoCalendario(fecha=date(2026, 11, 9), nombre="IPC de octubre", fuente="INE", termometro="bolsillo", estimada=True),
]

METODOLOGIA = [
    SeccionMetodologia(
        titulo="Presión",
        texto=(
            "Cada indicador se compara con su historia de los últimos 5 años. Si está en el 20 % "
            "más alto la presión es alta, en el 20 % más bajo es baja, y si no, media. "
            "No dice si algo es bueno o malo: solo si está lejos de lo habitual."
        ),
    ),
    SeccionMetodologia(
        titulo="Índice de canasta",
        texto=(
            "Costo semanal de una canasta típica: pan, leche, huevos, aceite, carnes, bencina, gas "
            "y pasajes. Es un indicador propio de referencia, no el IPC oficial."
        ),
    ),
    SeccionMetodologia(
        titulo="Ánimo de las noticias",
        texto=(
            "Clasificamos el tono de los titulares económicos de varios medios, equilibrando para "
            "que ninguno domine, y lo comparamos con lo habitual. Mide el tono de las noticias, "
            "no predice la economía."
        ),
    ),
    SeccionMetodologia(
        titulo="Fuentes",
        texto=(
            "Banco Central, CMF, INE, SII, Superintendencia de Pensiones, ODEPA, CNE y prensa. "
            "Cada dato muestra su fuente y su fecha."
        ),
    ),
]


def herramientas_de_ejemplo() -> Herramientas:
    return Herramientas(
        calculadoras=CALCULADORAS,
        mi_afp=MiAfp(
            dato_al=date.fromisoformat(_AFP["dato_al"]),
            provisional=_AFP["provisional"],
            fuente=_AFP["fuente"],
            fondos=_AFP["fondos"],
        ),
        calendario=CALENDARIO,
        metodologia=METODOLOGIA,
    )
