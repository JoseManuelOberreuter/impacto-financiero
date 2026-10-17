import asyncio
import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import fotos
from app.api.v1 import home, secciones, yo

log = logging.getLogger(__name__)
# Cada cuánto se revisa si la ingesta dejó fotos nuevas en Supabase (0 = nunca).
REVISAR_FOTOS_MINUTOS = float(os.getenv("REVISAR_FOTOS_MINUTOS", "15"))


async def _vigilar_fotos() -> None:
    while True:
        await asyncio.sleep(REVISAR_FOTOS_MINUTOS * 60)
        try:
            if await asyncio.to_thread(fotos.hay_nuevas):
                await asyncio.to_thread(fotos.recargar)
        except Exception:  # una caída de Supabase no debe botar la API: sigue con los datos que tiene
            log.exception("No se pudieron revisar las fotos")


@asynccontextmanager
async def ciclo_de_vida(_: FastAPI):
    tarea = asyncio.create_task(_vigilar_fotos()) if REVISAR_FOTOS_MINUTOS > 0 else None
    yield
    if tarea:
        tarea.cancel()


app = FastAPI(
    lifespan=ciclo_de_vida,
    title="Impacto Financiero API",
    version="0.1.0",
    description="Datos de la economía chilena explicados según cómo te afectan.",
)

# Orígenes permitidos para la app web (separados por coma).
origenes = os.getenv("CORS_ORIGINS", "http://localhost:8081").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in origenes],
    allow_methods=["GET", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.include_router(home.router, prefix="/v1", tags=["home"])
app.include_router(secciones.router, prefix="/v1")
app.include_router(yo.router, prefix="/v1")


@app.get("/salud", tags=["sistema"])
def salud() -> dict:
    """Estado de la API y versión de cada foto en uso ("archivo" = respaldo JSON)."""
    return {"estado": "ok", "fotos": fotos.en_uso()}
