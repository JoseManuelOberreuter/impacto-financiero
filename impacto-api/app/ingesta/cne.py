"""Conector de la CNE: precios de combustibles y gas.

Descarga tres cosas:
- Precios de hoy en las ~1.800 estaciones de servicio: guarda la mediana por
  combustible, en el país y en cada región, solo con las estaciones que
  actualizaron su precio en los últimos días (ver docs/fuentes-de-datos.md).
- Historia mensual del precio de los combustibles por región (desde 1994).
- Historia mensual del gas licuado en cilindro por región (desde 2000).

Uso suelto (solo escribe el JSON):
    python -m app.ingesta.cne app/datos_ejemplo/cne_snapshot.json

Lee CNE_EMAIL y CNE_PASSWORD (variables de entorno o archivo .env). La API
entrega un token nuevo en cada inicio de sesión.
"""

import gzip
import json
import statistics
import sys
import urllib.parse
import urllib.request
from datetime import date, timedelta
from pathlib import Path

from app.ingesta import Serie, credencial, region

ID = "cne"
FUENTE_ID = "cne"
ARCHIVO = "cne_snapshot.json"
URL = "https://api.cne.cl"
REGION_METROPOLITANA = "13"
# Un precio sin actualizar en estos días se considera viejo y no se usa.
DIAS_FRESCO = 7
# Si en una región hay menos estaciones frescas que esto, se amplía a 30 días.
MINIMO_ESTACIONES = 10
ANIOS_HISTORIA = 6

COMBUSTIBLES_ESTACION = {"93": "bencina93", "95": "bencina95", "97": "bencina97", "DI": "diesel", "KE": "parafina"}
COMBUSTIBLES_MENSUAL = {
    "gasolina_93_sp": "bencina93",
    "gasolina_95_sp": "bencina95",
    "gasolina_97_sp": "bencina97",
    "petroleo_diesel": "diesel",
    "kerosene_domestico": "parafina",
}


def pedir(ruta: str, token: str | None = None, datos: dict | None = None):
    cabeceras = {"Accept": "application/json"}
    if token:
        cabeceras["Authorization"] = f"Bearer {token}"
    cuerpo = urllib.parse.urlencode(datos).encode() if datos else None
    solicitud = urllib.request.Request(URL + ruta, data=cuerpo, headers=cabeceras)
    with urllib.request.urlopen(solicitud, timeout=180) as respuesta:
        crudo = respuesta.read()
    if crudo[:2] == b"\x1f\x8b":  # la CNE responde comprimido con gzip
        crudo = gzip.decompress(crudo)
    return json.loads(crudo)


def numero(texto) -> float | None:
    """Convierte '2.372,00', '1594,30' o '586.000'; devuelve None si no es un número."""
    if isinstance(texto, (int, float)):
        return float(texto)
    texto = str(texto).strip()
    try:
        if "," in texto:
            return float(texto.replace(".", "").replace(",", "."))
        return float(texto)
    except ValueError:
        return None  # la historia trae algunos valores corruptos (texto en vez de precio)


def resumen_estaciones(estaciones: list[dict], hoy: date) -> dict:
    precios: dict[str, dict[str, list[tuple[date, float]]]] = {}
    for estacion in estaciones:
        region = estacion["ubicacion"]["codigo_region"]
        for codigo, dato in (estacion.get("precios") or {}).items():
            id_ = COMBUSTIBLES_ESTACION.get(codigo)
            valor = numero(dato.get("precio"))
            if not id_ or not valor:
                continue
            fecha = date.fromisoformat(dato["fecha_actualizacion"])
            for zona in (region, "pais"):
                precios.setdefault(id_, {}).setdefault(zona, []).append((fecha, valor))

    resumen = {}
    for id_, zonas in precios.items():
        resumen[id_] = {}
        for zona, lista in zonas.items():
            dias = DIAS_FRESCO
            frescos = [v for f, v in lista if hoy - f <= timedelta(days=dias)]
            if len(frescos) < MINIMO_ESTACIONES:
                dias = 30
                frescos = [v for f, v in lista if hoy - f <= timedelta(days=dias)]
            if not frescos:
                continue
            resumen[id_][zona] = {
                "mediana": statistics.median(frescos),
                "estaciones_frescas": len(frescos),
                "estaciones_total": len(lista),
                "dias_fresco": dias,
            }
    return resumen


def historia_mensual(filas: list[dict], clave_tipo, clave_precio: str, desde: date) -> dict:
    """{id: {region: [[fecha, valor], ...]}} con los meses válidos desde `desde`."""
    historia: dict[str, dict[str, list]] = {}
    for fila in filas:
        id_ = clave_tipo(fila)
        valor = numero(fila[clave_precio])
        if not id_ or valor is None or fila["fecha"] < desde.isoformat():
            continue
        historia.setdefault(id_, {}).setdefault(str(fila["region_cod"]), []).append([fila["fecha"], round(valor, 1)])
    for regiones in historia.values():
        for lista in regiones.values():
            lista.sort()
    return historia


def generar() -> dict:
    hoy = date.today()
    desde = date(hoy.year - ANIOS_HISTORIA, 1, 1)

    token = pedir("/api/login", datos={"email": credencial("CNE_EMAIL"), "password": credencial("CNE_PASSWORD")})["token"]

    estaciones = pedir("/api/v4/estaciones", token)
    estaciones = estaciones if isinstance(estaciones, list) else estaciones["data"]
    liquidos = pedir("/api/ea/precio/combustibleliquido", token)["data"]
    glp = pedir("/api/ea/precio/glp", token)["data"]

    foto = {
        "fuente": "Comisión Nacional de Energía (CNE)",
        "descargado_el": hoy.isoformat(),
        "estaciones": resumen_estaciones(estaciones, hoy),
        "mensual_combustibles": historia_mensual(
            liquidos, lambda f: COMBUSTIBLES_MENSUAL.get(f["tipo_combustible"]), "precio_por_litro", desde
        ),
        "mensual_gas": historia_mensual(
            glp, lambda f: f"glp{f['tamanio'].split()[0]}_{f['tipo'].lower()}", "precio_pesos", desde
        ),
    }
    rm = foto["estaciones"]["bencina95"][REGION_METROPOLITANA]
    print(f"  {len(estaciones)} estaciones. Bencina 95 en la RM: ${rm['mediana']:.0f} ({rm['estaciones_frescas']} frescas)")
    return foto


def series(foto: dict) -> list[Serie]:
    """La historia mensual por región y la mediana de hoy en las estaciones.

    La CNE no guarda la historia diaria de las estaciones: se arma aquí, un punto por día de ingesta.
    """
    resultado = []
    for grupo, unidad in (("mensual_combustibles", "$ por litro"), ("mensual_gas", "$ por cilindro")):
        for id_, regiones in foto[grupo].items():
            for codigo, observaciones in regiones.items():
                resultado.append(
                    Serie(
                        id=f"cne.{id_}.{region(codigo)}",
                        nombre=f"{id_}, promedio mensual",
                        unidad=unidad,
                        frecuencia="mensual",
                        region=region(codigo),
                        observaciones=[(f, v) for f, v in observaciones],
                    )
                )
    for id_, zonas in foto["estaciones"].items():
        for zona, dato in zonas.items():
            resultado.append(
                Serie(
                    id=f"cne.estaciones.{id_}.{region(zona)}",
                    nombre=f"{id_}, mediana de las estaciones",
                    unidad="$ por litro",
                    frecuencia="diaria",
                    region=None if zona == "pais" else region(zona),
                    observaciones=[(foto["descargado_el"], dato["mediana"])],
                    metadatos={"estaciones_frescas": dato["estaciones_frescas"], "dias_fresco": dato["dias_fresco"]},
                )
            )
    return resultado


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    Path(sys.argv[1]).write_text(json.dumps(generar(), ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
