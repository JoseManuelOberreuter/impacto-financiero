"""Fotos de las fuentes que usa la API: de Supabase, o de los JSON de respaldo (docs/ingesta.md).

La ingesta diaria (python -m app.ingesta) deja en la tabla `fotos` lo último de cada fuente.
Los módulos de app/datos_ejemplo leen su foto al importarse. Cuando la ingesta trae algo
nuevo, `recargar()` vuelve a importarlos para que la API muestre los datos al día sin
reiniciar.

FOTOS_DESDE elige el origen: "supabase" (por defecto si está configurado) o "archivos"
(las pruebas y el desarrollo sin conexión).
"""

import importlib
import json
import logging
import os
import sys
import threading
from pathlib import Path

import httpx

from app import supabase

_RESPALDO = Path(__file__).resolve().parent / "datos_ejemplo"
ARCHIVOS = {
    "bcch": "bcch_snapshot.json",
    "cne": "cne_snapshot.json",
    "cmf": "cmf_snapshot.json",
    "odepa": "odepa_snapshot.json",
    "afp": "afp_snapshot.json",
}
# Orden de recarga: cada módulo después de los que importa.
MODULOS = [
    "app.datos_ejemplo.banco_central",
    "app.datos_ejemplo.cmf",
    "app.datos_ejemplo.cne",
    "app.datos_ejemplo.precios",
    "app.datos_ejemplo.impacto",
    "app.datos_ejemplo.herramientas",
    "app.datos_ejemplo.mi_impacto",
    "app.datos_ejemplo.noticias",
    "app.datos_ejemplo.termometros",
    "app.datos_ejemplo.home",
]

log = logging.getLogger(__name__)
# Versión de cada foto en uso: el actualizado_el de Supabase, o "archivo" si vino del respaldo.
_en_uso: dict[str, str] = {}
_cerrojo = threading.Lock()


def _desde_supabase() -> bool:
    return os.getenv("FOTOS_DESDE", "supabase") == "supabase"


def leer(id_: str) -> dict:
    """La foto más reciente de una fuente. Si Supabase no responde, usa el JSON de respaldo."""
    if _desde_supabase():
        try:
            filas = supabase.seleccionar("fotos", {"id": f"eq.{id_}"}, "contenido,actualizado_el")
            if filas:
                _en_uso[id_] = filas[0]["actualizado_el"]
                return filas[0]["contenido"]
            log.warning("La foto %s no está en Supabase: se usa el respaldo", id_)
        except (supabase.SinConfiguracion, httpx.HTTPError) as error:
            log.warning("No se pudo leer la foto %s de Supabase (%s): se usa el respaldo", id_, error)
    _en_uso[id_] = "archivo"
    return json.loads((_RESPALDO / ARCHIVOS[id_]).read_text(encoding="utf-8"))


def hay_nuevas() -> bool:
    """True si alguna foto de Supabase es distinta de la que está en uso."""
    if not _desde_supabase():
        return False
    filas = supabase.seleccionar("fotos", {}, "id,actualizado_el")
    return any(_en_uso.get(f["id"], f["actualizado_el"]) != f["actualizado_el"] for f in filas)


def recargar() -> None:
    """Vuelve a importar los módulos de datos con las fotos nuevas."""
    with _cerrojo:
        for nombre in MODULOS:
            if nombre in sys.modules:
                importlib.reload(sys.modules[nombre])
    log.info("Datos recargados: %s", _en_uso)


def en_uso() -> dict[str, str]:
    return dict(_en_uso)
