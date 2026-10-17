"""Esquemas de respuesta del home (/v1/home)."""

from datetime import date

from pydantic import BaseModel, Field

from app.modelos.impacto import ImpactoFinanciero
from app.modelos.precios import Canasta
from app.modelos.termometros import Presion, Tendencia, Termometro


class Resumen(BaseModel):
    titulo: str = Field(description="Titular del día, en una frase corta")
    texto: str = Field(description="Bajada con el contexto, en una frase")


class CambioSemana(BaseModel):
    """Un dato que se movió esta semana, para la lista "Lo que cambió"."""

    id: str
    nombre: str
    detalle: str = Field(description="Variación y valor, ya formateados")
    direccion: Tendencia
    presion: Presion = Field(description="Presión que el cambio pone sobre el bolsillo")
    serie: list[float] = Field(description="Valores recientes para el mini gráfico")
    enlace: str = Field(description="Ruta de la app con el detalle")


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
