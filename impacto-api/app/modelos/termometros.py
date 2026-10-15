"""Esquemas de los termómetros (ver docs/termometros.md)."""

from datetime import date
from enum import Enum

from pydantic import BaseModel, Field


class Presion(str, Enum):
    """Presión respecto de lo normal del propio indicador."""

    baja = "baja"
    media = "media"
    alta = "alta"


class Tendencia(str, Enum):
    sube = "sube"
    baja = "baja"
    estable = "estable"


class Termometro(BaseModel):
    id: str
    nombre: str
    pregunta: str = Field(description="Pregunta que responde, en lenguaje simple")
    presion: Presion
    etiqueta_presion: str = Field(description="Texto del estado, por ejemplo 'Presión media'")
    tendencia: Tendencia
    dato_clave: str = Field(description="El único número que se muestra en la tarjeta")
    frase: str = Field(description="Explicación en una frase")
    dato_al: date = Field(description="Fecha a la que corresponde el dato")
    proxima_actualizacion: date | None = None
    fuentes: list[str]


class PuntoSerie(BaseModel):
    fecha: date
    valor: float


class BandaNormal(BaseModel):
    """Rango habitual del indicador (por ejemplo, el de los últimos 5 años)."""

    min: float
    max: float


class Indicador(BaseModel):
    id: str
    nombre: str
    valor: str = Field(description="Valor ya formateado para mostrar")
    variacion: str | None = None
    presion: Presion
    descripcion: str
    serie: list[PuntoSerie]
    banda_normal: BandaNormal | None = None
    fuente: str
    dato_al: date


class Percepcion(BaseModel):
    """Cómo lo siente la gente, para contrastar con los datos duros."""

    nombre: str
    valor: str
    descripcion: str
    fuente: str


class Publicacion(BaseModel):
    fecha: date
    nombre: str
    fuente: str


class TermometroDetalle(Termometro):
    explicacion: str = Field(description="Por qué el termómetro está como está")
    indicadores: list[Indicador]
    percepcion: Percepcion | None = None
    proximas_publicaciones: list[Publicacion]
    metodologia: str
    herramienta_relacionada: str | None = None
