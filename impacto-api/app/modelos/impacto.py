"""Esquema del Impacto Financiero: cuánto más le cuesta la vida a un hogar típico."""

from datetime import date

from pydantic import BaseModel, Field


class RubroImpacto(BaseModel):
    id: str
    nombre: str
    gasto_mes: int = Field(description="Gasto mensual del rubro hoy, en pesos")
    diferencia_anual: int = Field(description="Cuánto más (o menos) que hace un año, en pesos al mes")
    diferencia_mensual: int = Field(description="Cuánto más (o menos) que el mes anterior, en pesos al mes")
    variacion_anual: float = Field(description="Variación de precios del rubro en 12 meses, en %")


class ImpactoFinanciero(BaseModel):
    periodo: date = Field(description="Mes del último IPC publicado")
    actualizado_al: date = Field(
        description="Fecha del dato más reciente: la bencina y la UF se actualizan a diario"
    )
    hogar: str = Field(description="A quién representa el cálculo")
    gasto_mes: int
    diferencia_anual: int
    variacion_anual: float
    diferencia_mensual: int
    rubros: list[RubroImpacto] = Field(
        description="De mayor a menor diferencia anual, con \"Todo lo demás\" al final"
    )
    fuente: str
    metodologia: str
