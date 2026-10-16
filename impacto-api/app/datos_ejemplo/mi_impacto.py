"""Valores de referencia para Mi impacto: UF (Banco Central) y bencina (CNE)."""

from datetime import date

from app.datos_ejemplo import banco_central as bc
from app.datos_ejemplo import cne
from app.modelos.mi_impacto import ReferenciaBencina, ReferenciaUf, ReferenciasMiImpacto, Valor


def _valor(punto) -> Valor:
    return Valor(fecha=punto.fecha, valor=punto.valor)


def _bencina_hace_un_anio() -> Valor:
    objetivo = cne.DESCARGADO_EL.replace(year=cne.DESCARGADO_EL.year - 1, day=1)
    # El mes de hace un año o, si la CNE no tiene ese dato, el anterior más cercano.
    fecha, valor = next((f, v) for f, v in reversed(cne.mensual("bencina95")) if f <= objetivo)
    return Valor(fecha=fecha, valor=valor)


def referencias() -> ReferenciasMiImpacto:
    uf = bc.SERIES["uf"]
    publicada = bc.ultima_publicada("uf")
    bencina = cne.hoy("bencina95")
    return ReferenciasMiImpacto(
        uf=ReferenciaUf(
            hoy=_valor(uf.ultimo),
            ultima_publicada=Valor(fecha=publicada[0], valor=publicada[1]),
            hace_un_mes=_valor(uf.antes_de(30)),
            hace_un_anio=_valor(uf.antes_de(365)),
            fuente="Banco Central",
        ),
        bencina95=ReferenciaBencina(
            hoy=Valor(fecha=cne.DESCARGADO_EL, valor=bencina["mediana"]),
            hace_un_anio=_bencina_hace_un_anio(),
            estaciones=bencina["estaciones_frescas"],
            region="Región Metropolitana",
            fuente="CNE",
        ),
    )
