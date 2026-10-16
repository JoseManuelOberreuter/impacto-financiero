import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import home, secciones, yo

app = FastAPI(
    title="Impacto Financiero API",
    version="0.1.0",
    description="Datos de la economía chilena explicados según cómo te afectan.",
)

# Orígenes permitidos para la app web (separados por coma).
origenes = os.getenv("CORS_ORIGINS", "http://localhost:8081").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in origenes],
    allow_methods=["GET"],
    allow_headers=["*"],
)

app.include_router(home.router, prefix="/v1", tags=["home"])
app.include_router(secciones.router, prefix="/v1")
app.include_router(yo.router, prefix="/v1")


@app.get("/salud", tags=["sistema"])
def salud() -> dict[str, str]:
    return {"estado": "ok"}
