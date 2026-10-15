"""Esquemas de la sección Herramientas: calculadoras, Mi AFP, calendario y metodología."""

from datetime import date

from pydantic import BaseModel, Field


class Calculadora(BaseModel):
    id: str
    nombre: str
    descripcion: str
    disponible: bool


class RentabilidadAfp(BaseModel):
    afp: str
    anio: float = Field(description="Rentabilidad nominal en el año, en porcentaje")
    mes: float = Field(description="Rentabilidad nominal de los últimos ~30 días, en porcentaje")


class FondoAfp(BaseModel):
    fondo: str
    afps: list[RentabilidadAfp]


class MiAfp(BaseModel):
    dato_al: date
    provisional: bool
    fuente: str
    fondos: list[FondoAfp]


class EventoCalendario(BaseModel):
    fecha: date
    nombre: str
    fuente: str
    termometro: str | None = None
    estimada: bool = Field(description="True si la fecha es estimada y no confirmada")


class SeccionMetodologia(BaseModel):
    titulo: str
    texto: str


class Herramientas(BaseModel):
    calculadoras: list[Calculadora]
    mi_afp: MiAfp
    calendario: list[EventoCalendario]
    metodologia: list[SeccionMetodologia]
