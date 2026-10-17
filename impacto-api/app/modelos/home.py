"""Esquemas de respuesta del home (/v1/home)."""

from datetime import date

from enum import Enum

from pydantic import BaseModel, Field

from app.modelos.impacto import ImpactoFinanciero
from app.modelos.precios import Canasta
from app.modelos.termometros import Presion, Tendencia, Termometro


class Resumen(BaseModel):
    titulo: str = Field(description="Titular del día, en una frase corta")
    texto: str = Field(description="Bajada con el contexto, en una frase")


class Efecto(str, Enum):
    """Qué significa para el bolsillo que el dato suba (docs/termometros.md)."""

    sube_malo = "sube_malo"
    sube_bueno = "sube_bueno"
    neutro = "neutro"


class Tono(str, Enum):
    """Si el último movimiento conviene al bolsillo: colorea la flecha."""

    favorable = "favorable"
    desfavorable = "desfavorable"
    neutral = "neutral"


class CambioSemana(BaseModel):
    """Un dato con su último movimiento, para "Lo que cambió" y "Todos los datos"."""

    id: str
    nombre: str
    detalle: str = Field(description="Variación y valor, ya formateados")
    direccion: Tendencia
    presion: Presion = Field(description="Presión que el cambio pone sobre el bolsillo")
    serie: list[float] = Field(description="Valores recientes para el mini gráfico")
    enlace: str = Field(description="Ruta de la app con el detalle")
    tema: str = Field(default="otros", description="energia, alimentos, afuera, deudas, precios, empleo o animo")
    efecto: Efecto = Efecto.neutro
    tono: Tono = Field(default=Tono.neutral, description="Calculado con la dirección y el efecto")
    estado: str = Field(
        default="Normal", description="Dónde está comparado con lo normal, en palabras: \"Más cara que lo normal\""
    )
    nivel: str = Field(default="normal", description="sobre, normal o bajo lo normal de los últimos 5 años")
    movimiento: float = Field(
        default=0.0,
        description="Qué tan inusual fue el último cambio: veces lo que el dato suele moverse",
    )


class Home(BaseModel):
    generado_el: date
    datos_de_ejemplo: bool = Field(
        description="True mientras los datos no vengan de las fuentes reales"
    )
    resumen: Resumen
    impacto: ImpactoFinanciero = Field(description="Protagonista del Inicio: la inflación en pesos para un hogar típico")
    canasta: Canasta
    cambios: list[CambioSemana]
    termometros: list[Termometro] = Field(description="Todos los termómetros disponibles")
    termometros_por_defecto: list[str] = Field(
        description="Ids que se muestran si el usuario no personalizó su home"
    )
    max_termometros_home: int
    aviso_legal: str
