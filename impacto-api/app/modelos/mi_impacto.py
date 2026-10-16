"""Esquemas de Mi impacto (docs/plan-pro.md).

La API entrega solo los valores de referencia. Los datos del usuario (su
dividendo, sus litros de bencina) se quedan en su teléfono y el cálculo se hace
ahí.
"""

from datetime import date

from pydantic import BaseModel, Field


class Valor(BaseModel):
    fecha: date
    valor: float


class ReferenciaUf(BaseModel):
    hoy: Valor
    ultima_publicada: Valor = Field(description="La UF se publica por adelantado, hasta el día 9 del mes siguiente")
    hace_un_mes: Valor
    hace_un_anio: Valor
    fuente: str


class ReferenciaBencina(BaseModel):
    hoy: Valor = Field(description="Mediana de estaciones con precio actualizado hace poco, en $ por litro")
    hace_un_anio: Valor = Field(description="Promedio mensual de hace un año, en $ por litro")
    estaciones: int
    region: str
    fuente: str


class ReferenciasMiImpacto(BaseModel):
    uf: ReferenciaUf
    bencina95: ReferenciaBencina
