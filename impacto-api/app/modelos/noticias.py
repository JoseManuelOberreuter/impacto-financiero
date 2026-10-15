"""Esquemas de la sección Noticias (termómetro Ánimo, ver docs/sentimiento-noticias.md)."""

from datetime import date

from pydantic import BaseModel, Field

from app.modelos.termometros import Presion, PuntoSerie, Tendencia


class Titular(BaseModel):
    titulo: str
    medio: str
    fecha: date
    enlace: str | None = Field(default=None, description="Enlace a la nota original")


class Tema(BaseModel):
    nombre: str
    termometro: str = Field(description="Id del termómetro con el que se relaciona")
    tono: float = Field(description="Tono promedio de −2 (muy negativo) a +2 (muy positivo)")
    cantidad: int
    titulares: list[Titular]


class HechoEsencial(BaseModel):
    entidad: str
    titulo: str
    resumen: str = Field(description="Explicación en lenguaje simple")
    fecha: date


class Noticias(BaseModel):
    presion: Presion
    etiqueta: str
    tendencia: Tendencia
    tono_semana: float = Field(description="Tono neto de −100 a +100")
    serie_tono: list[PuntoSerie]
    incertidumbre: float = Field(description="Porcentaje de titulares que hablan de incertidumbre")
    total_titulares: int
    medios: int
    temas: list[Tema]
    hechos_esenciales: list[HechoEsencial]
    dato_al: date
    nota: str
