"""Frases en palabras simples para decir dónde está cada dato comparado con lo normal.

La app ya no muestra "presión": dice "Más cara que lo normal", "Normal" o "Más
barata que lo normal". "Lo normal" es el rango de los últimos 5 años (percentiles
20 a 80, app/calculos/presion.py). Ver docs/termometros.md.

La presión es alta cuando el dato presiona el bolsillo. En los indicadores
"invertidos" (IMACEC, cobre, percepción y confianza) eso pasa cuando el valor está
bajo, así que la frase se da vuelta.
"""

from app.modelos.termometros import Presion

NORMAL = "Normal"

# id del dato: (frase si está sobre lo normal, frase si está bajo lo normal)
_FRASES: dict[str, tuple[str, str]] = {
    "bencina": ("Más cara que lo normal", "Más barata que lo normal"),
    "gas": ("Más caro que lo normal", "Más barato que lo normal"),
    "petroleo": ("Más caro que lo normal", "Más barato que lo normal"),
    "dolar": ("Más caro que lo normal", "Más barato que lo normal"),
    "cobre": ("Más caro que lo normal", "Más barato que lo normal"),
    "uf": ("Más alta que lo normal", "Más baja que lo normal"),
    "tpm": ("Más alta que lo normal", "Más baja que lo normal"),
    "tmc": ("Más alta que lo normal", "Más baja que lo normal"),
    "tasa_hipotecaria": ("Más alta que lo normal", "Más baja que lo normal"),
    "tasa_consumo": ("Más alta que lo normal", "Más baja que lo normal"),
    "ipc_mensual": ("Inflación más alta que lo normal", "Inflación más baja que lo normal"),
    "ipc_alimentos": ("Más alto que lo normal", "Más bajo que lo normal"),
    "ipc_vivienda": ("Más alto que lo normal", "Más bajo que lo normal"),
    "ipc_transporte": ("Más alto que lo normal", "Más bajo que lo normal"),
    "desempleo": ("Más alto que lo normal", "Más bajo que lo normal"),
    "imacec_12m": ("Crece más que lo normal", "Crece menos que lo normal"),
    "ipec": ("Más optimistas que lo normal", "Más pesimistas que lo normal"),
    "imce": ("Más optimistas que lo normal", "Más pesimistas que lo normal"),
    "canasta": ("Más cara que lo normal", "Más barata que lo normal"),
}
# Alimentos de ODEPA: (sobre lo normal, bajo lo normal), con su género y número.
_ALIMENTOS = {
    "marraqueta": ("Más cara que lo normal", "Más barata que lo normal"),
    "hallulla": ("Más cara que lo normal", "Más barata que lo normal"),
    "leche": ("Más cara que lo normal", "Más barata que lo normal"),
    "papa": ("Más cara que lo normal", "Más barata que lo normal"),
    "posta": ("Más cara que lo normal", "Más barata que lo normal"),
    "huevos": ("Más caros que lo normal", "Más baratos que lo normal"),
    "aceite": ("Más caro que lo normal", "Más barato que lo normal"),
    "arroz": ("Más caro que lo normal", "Más barato que lo normal"),
    "pollo": ("Más caro que lo normal", "Más barato que lo normal"),
    "tomate": ("Más caro que lo normal", "Más barato que lo normal"),
}
# Indicadores en los que un valor bajo es el que presiona.
INVERTIDOS = {"imacec_12m", "ipec", "imce", "cobre"}

# Termómetros: (presión alta, media, baja). Su presión ya considera si presiona o no.
_TERMOMETROS = {
    "impacto": ("Inflación más alta que lo normal", "Inflación normal", "Inflación más baja que lo normal"),
    "bolsillo": ("La vida está más cara que lo normal", "Precios normales", "La vida está más barata que lo normal"),
    "deudas": ("Endeudarse está más caro que lo normal", "Créditos normales", "Endeudarse está más barato que lo normal"),
    "ahorro": ("Peor que lo normal", "Normal", "Mejor que lo normal"),
    "actividad": ("Más débil que lo normal", "Normal", "Más fuerte que lo normal"),
    "dolar": ("Dólar más caro que lo normal", "Dólar normal", "Dólar más barato que lo normal"),
    "animo": ("Más pesimistas que lo normal", "Ánimo normal", "Más optimistas que lo normal"),
}


def nivel(id_: str, presion: Presion) -> str:
    """"sobre", "normal" o "bajo" lo normal, según el valor (no según si presiona)."""
    if presion is Presion.media:
        return "normal"
    return "sobre" if (presion is Presion.alta) != (id_ in INVERTIDOS) else "bajo"


def del_dato(id_: str, presion: Presion) -> str:
    """Frase de un dato o indicador según su presión."""
    if presion is Presion.media:
        return NORMAL
    frases = _FRASES.get(id_) or _ALIMENTOS.get(id_) or ("Más alto que lo normal", "Más bajo que lo normal")
    return frases[0] if nivel(id_, presion) == "sobre" else frases[1]


def del_termometro(id_: str, presion: Presion) -> str:
    alta, media, baja = _TERMOMETROS.get(id_, ("Más alto que lo normal", "Normal", "Más bajo que lo normal"))
    return {Presion.alta: alta, Presion.media: media, Presion.baja: baja}[presion]
