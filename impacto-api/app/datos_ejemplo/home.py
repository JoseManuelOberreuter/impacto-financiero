"""Datos de ejemplo del home.

Se usan mientras los conectores no estén listos. Las cifras son ilustrativas:
los precios de alimentos se inspiran en ODEPA (semana al 9-oct-2026) y el resto
son valores de ejemplo, no datos oficiales.
"""

from datetime import date

from app.modelos.home import Home, Presion, Resumen, Tendencia, Termometro

TERMOMETROS = [
    Termometro(
        id="bolsillo",
        nombre="Bolsillo",
        icono="🛒",
        pregunta="¿Está más cara la vida?",
        presion=Presion.media,
        etiqueta_presion="Presión media",
        tendencia=Tendencia.sube,
        dato_clave="Canasta semanal: $125.600 (+0,7\u00a0%)",
        frase="Subieron el pan y la bencina; bajó un poco el pollo.",
        dato_al=date(2026, 10, 9),
        proxima_actualizacion=date(2026, 10, 16),
        fuentes=["ODEPA", "CNE", "Panel de Expertos"],
    ),
    Termometro(
        id="deudas",
        nombre="Deudas",
        icono="🏦",
        pregunta="¿Está más caro endeudarse?",
        presion=Presion.media,
        etiqueta_presion="Presión media",
        tendencia=Tendencia.estable,
        dato_clave="Tasa del Banco Central: 4,5\u00a0%",
        frase="La tasa se mantiene y los expertos no esperan cambios este año.",
        dato_al=date(2026, 10, 14),
        proxima_actualizacion=date(2026, 10, 28),
        fuentes=["Banco Central", "CMF"],
    ),
    Termometro(
        id="ahorro",
        nombre="Ahorro y pensiones",
        icono="💰",
        pregunta="¿Cómo le va a mi plata?",
        presion=Presion.baja,
        etiqueta_presion="Presión baja",
        tendencia=Tendencia.sube,
        dato_clave="Fondo C: +0,4\u00a0% en el mes",
        frase="Los fondos subieron en el mes, liderados por los más riesgosos.",
        dato_al=date(2026, 10, 13),
        proxima_actualizacion=date(2026, 10, 16),
        fuentes=["Superintendencia de Pensiones"],
    ),
    Termometro(
        id="actividad",
        nombre="Actividad y empleo",
        icono="🏭",
        pregunta="¿Cómo va la economía en general?",
        presion=Presion.alta,
        etiqueta_presion="Presión alta",
        tendencia=Tendencia.sube,
        dato_clave="Desempleo: 8,7\u00a0%",
        frase="El desempleo sigue sobre lo habitual, aunque la actividad crece.",
        dato_al=date(2026, 8, 31),
        proxima_actualizacion=date(2026, 10, 30),
        fuentes=["INE", "Banco Central"],
    ),
    Termometro(
        id="dolar",
        nombre="Dólar y mercados",
        icono="💵",
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
        icono="📰",
        pregunta="¿De qué se está hablando?",
        presion=Presion.alta,
        etiqueta_presion="Más negativo que lo habitual",
        tendencia=Tendencia.baja,
        dato_clave="412 titulares de 6 medios",
        frase="Dominaron el desempleo y el precio de la bencina.",
        dato_al=date(2026, 10, 14),
        proxima_actualizacion=date(2026, 10, 15),
        fuentes=["La Tercera", "BioBio", "Cooperativa", "CIPER", "Ex-Ante", "CMF"],
    ),
]


def home_de_ejemplo() -> Home:
    return Home(
        generado_el=date(2026, 10, 15),
        datos_de_ejemplo=True,
        resumen=Resumen(
            titulo="Hoy en Chile",
            texto=(
                "La canasta subió levemente por el pan y la bencina. "
                "La tasa del Banco Central sigue igual y el dólar bajó."
            ),
        ),
        termometros=TERMOMETROS,
        termometros_por_defecto=["bolsillo", "deudas", "ahorro", "actividad"],
        max_termometros_home=4,
        aviso_legal=(
            "Impacto Financiero informa y explica; no es asesoría financiera, "
            "tributaria ni de inversión."
        ),
    )
