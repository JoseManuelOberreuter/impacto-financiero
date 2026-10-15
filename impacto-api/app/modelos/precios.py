"""Esquemas de la sección Precios (economía cotidiana)."""

from datetime import date

from pydantic import BaseModel, Field


class PuntoPrecio(BaseModel):
    semana: date = Field(description="Último día de la semana medida")
    precio: int


class PrecioPorTipo(BaseModel):
    tipo: str = Field(description="Panadería, supermercado, feria libre, carnicería…")
    precio: int


class PrecioPorRegion(BaseModel):
    region: str
    precio: int


class Producto(BaseModel):
    id: str
    nombre: str
    unidad: str
    categoria: str
    precio: int = Field(description="Mediana de la Región Metropolitana, en pesos")
    variacion_semanal: float
    variacion_anual: float = Field(description="Variación porcentual desde inicio de año")
    puntos_de_venta: int
    serie: list[PuntoPrecio]
    por_tipo_local: list[PrecioPorTipo]
    por_region: list[PrecioPorRegion] = Field(description="Ordenado de más barato a más caro")
    dato_al: date
    fuente: str


class PrecioReferencia(BaseModel):
    """Precio que no viene de ODEPA (combustibles, transporte)."""

    id: str
    nombre: str
    unidad: str
    precio: int
    fuente: str
    nota: str
    de_ejemplo: bool = Field(description="True si el valor aún no viene de la fuente real")


class ItemCanasta(BaseModel):
    nombre: str
    cantidad: str
    costo: int
    porcentaje: float = Field(description="Participación en el total de la canasta")


class Canasta(BaseModel):
    total: int = Field(description="Costo de la canasta semanal, en pesos")
    variacion_semanal: float
    dato_al: date
    serie: list[PuntoPrecio]
    composicion: list[ItemCanasta]
    nota: str


class Precios(BaseModel):
    canasta: Canasta
    productos: list[Producto]
    energia_y_transporte: list[PrecioReferencia]
