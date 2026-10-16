"""Precios de ejemplo.

Los alimentos vienen de una foto real de ODEPA (odepa_snapshot.json, generada con
scripts/snapshot_odepa.py). La bencina y el gas vienen de la foto real de la CNE
(cne.py). El pasaje de Metro es la tarifa vigente, cargada a mano.
"""

import json
from datetime import date
from pathlib import Path

from app.datos_ejemplo import cne
from app.modelos.precios import (
    Canasta,
    ItemCanasta,
    PrecioReferencia,
    Precios,
    Producto,
    PuntoPrecio,
)

_SNAPSHOT = json.loads((Path(__file__).parent / "odepa_snapshot.json").read_text(encoding="utf-8"))

PRODUCTOS = [Producto(**p, fuente=_SNAPSHOT["fuente"]) for p in _SNAPSHOT["productos"]]
PRODUCTOS_POR_ID = {p.id: p for p in PRODUCTOS}

_BENCINA = cne.hoy("bencina95")
_GAS_FECHA, _GAS_PRECIO = cne.mensual("glp15_corriente")[-1]
_MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
          "septiembre", "octubre", "noviembre", "diciembre"]

ENERGIA_Y_TRANSPORTE = [
    PrecioReferencia(
        id="bencina95",
        nombre="Bencina 95",
        unidad="litro",
        precio=round(_BENCINA["mediana"]),
        fuente="CNE",
        nota=(
            f"Mediana de {_BENCINA['estaciones_frescas']} estaciones de la Región Metropolitana "
            f"que actualizaron su precio en los últimos {_BENCINA['dias_fresco']} días."
        ),
        de_ejemplo=False,
    ),
    PrecioReferencia(
        id="gas15",
        nombre="Gas licuado",
        unidad="cilindro 15 kg",
        precio=int(round(_GAS_PRECIO, -1)),
        fuente="CNE",
        nota=f"Precio promedio de {_MESES[_GAS_FECHA.month - 1]} en la Región Metropolitana, cilindro corriente.",
        de_ejemplo=False,
    ),
    PrecioReferencia(
        id="metro",
        nombre="Pasaje de Metro",
        unidad="hora punta",
        precio=895,
        fuente="Panel de Expertos del Transporte Público",
        nota="Tarifa vigente desde el 22-feb-2026.",
        de_ejemplo=False,
    ),
]
_REFERENCIA_POR_ID = {r.id: r for r in ENERGIA_Y_TRANSPORTE}

# Composición propuesta en docs/indice-canasta.md: (id, cantidad, texto de la cantidad).
_COMPOSICION = [
    ("marraqueta", 4, "4 kg de marraqueta"),
    ("leche", 4, "4 L de leche"),
    ("huevos", 1, "30 huevos"),
    ("aceite", 1, "1 aceite"),
    ("pollo", 2, "2 kg de pollo"),
    ("posta", 1, "1 kg de posta"),
    ("bencina95", 20, "20 L de bencina"),
    ("gas15", 1, "1 cilindro de gas"),
    ("metro", 40, "40 pasajes de Metro"),
]


def _costo_semana(indice: int) -> int:
    """Costo de la canasta en la semana `indice` de la serie de ODEPA."""
    total = 0
    for id_, cantidad, _ in _COMPOSICION:
        if id_ in PRODUCTOS_POR_ID:
            total += PRODUCTOS_POR_ID[id_].serie[indice].precio * cantidad
        else:
            total += _REFERENCIA_POR_ID[id_].precio * cantidad
    return total


def _canasta() -> Canasta:
    semanas = PRODUCTOS_POR_ID["marraqueta"].serie
    serie = [PuntoPrecio(semana=p.semana, precio=_costo_semana(i)) for i, p in enumerate(semanas)]
    total = serie[-1].precio

    composicion = []
    for id_, cantidad, texto in _COMPOSICION:
        precio = (PRODUCTOS_POR_ID.get(id_) or _REFERENCIA_POR_ID[id_]).precio
        costo = precio * cantidad
        composicion.append(
            ItemCanasta(
                nombre=texto,
                cantidad=str(cantidad),
                costo=costo,
                porcentaje=round(costo / total * 100, 1),
            )
        )

    return Canasta(
        total=total,
        variacion_semanal=round((total / serie[-2].precio - 1) * 100, 1),
        dato_al=serie[-1].semana,
        serie=serie,
        composicion=sorted(composicion, key=lambda item: item.costo, reverse=True),
        nota=(
            "Indicador propio de referencia, no es el IPC. Alimentos: ODEPA. "
            "Bencina y gas: CNE, con el precio de hoy en todas las semanas hasta guardar su historia semanal."
        ),
    )


CANASTA = _canasta()


def precios_de_ejemplo() -> Precios:
    return Precios(canasta=CANASTA, productos=PRODUCTOS, energia_y_transporte=ENERGIA_Y_TRANSPORTE)


def producto_de_ejemplo(id_: str) -> Producto | None:
    return PRODUCTOS_POR_ID.get(id_)


def fecha_dato() -> date:
    return CANASTA.dato_al
