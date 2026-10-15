"""Esquemas de respuesta del home (/v1/home)."""

from datetime import date
from enum import Enum

from pydantic import BaseModel, Field


class Presion(str, Enum):
    """Presión respecto de lo normal del propio indicador (ver docs/termometros.md)."""

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
    icono: str = Field(description="Emoji que identifica al termómetro")
    pregunta: str = Field(description="Pregunta que responde, en lenguaje simple")
    presion: Presion
    etiqueta_presion: str = Field(description="Texto del estado, por ejemplo 'Presión media'")
    tendencia: Tendencia
    dato_clave: str = Field(description="El único número que se muestra en la tarjeta")
    frase: str = Field(description="Explicación en una frase")
    dato_al: date = Field(description="Fecha a la que corresponde el dato")
    proxima_actualizacion: date | None = None
    fuentes: list[str]


class Resumen(BaseModel):
    titulo: str
    texto: str = Field(description="Resumen del día en dos líneas como máximo")


class Home(BaseModel):
    generado_el: date
    datos_de_ejemplo: bool = Field(
        description="True mientras los datos no vengan de las fuentes reales"
    )
    resumen: Resumen
    termometros: list[Termometro] = Field(description="Todos los termómetros disponibles")
    termometros_por_defecto: list[str] = Field(
        description="Ids que se muestran si el usuario no personalizó su home"
    )
    max_termometros_home: int
    aviso_legal: str
