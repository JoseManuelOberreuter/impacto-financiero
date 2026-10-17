# Impacto Financiero: metodología

> Indicador propio, protagonista del Inicio desde el 16-oct-2026. Responde: **¿cuánto más le cuesta la vida a un hogar típico que hace un año, en pesos al mes?** Código: `impacto-api/app/datos_ejemplo/impacto.py`. Fuentes: [catalogo-de-datos.md](catalogo-de-datos.md).

## Por qué este indicador

- La app se llama Impacto Financiero: el dato principal debe ser **cuánto te impacta**, en pesos y no como un índice abstracto.
- Reemplaza a la canasta semanal como protagonista del Inicio. La canasta sigue en Precios.
- No es un "puntaje global" de la economía (lo descartamos al inicio): es la inflación expresada en pesos para un hogar.
- Conecta con el plan Pro ([plan-pro.md](plan-pro.md)): gratis se ve el impacto de **un hogar típico**; en Mi impacto, el usuario calcula **el suyo**.

## Cálculo

1. **Gasto de un hogar típico:** gasto promedio mensual de los hogares del **Gran Santiago** según la **IX Encuesta de Presupuestos Familiares del INE**: $1.590.105 (oct-2021 a sep-2022).
2. **Reparto por rubro:** proporciones de la misma encuesta (capitales regionales):

   | Rubro | % del gasto | IPC que lo mueve | Código del Banco Central |
   |---|---|---|---|
   | Comida | 21,2 % | IPC de alimentos y bebidas no alcohólicas | `F074.IPC.IND.DIV10000.2023.C.M` |
   | Vivienda, luz, agua y gas | 16,0 % | IPC de vivienda y servicios básicos | `F074.IPC.IND.DIV40000.2023.C.M` |
   | Transporte | 15,0 % | IPC de transporte | `F074.IPC.IND.DIV70000.2023.C.M` |
   | Todo lo demás | 47,8 % | IPC general | `G073.IPC.IND.2023.M` |

3. **Llevar a precios de hoy:** gasto × (IPC general del último mes ÷ promedio del IPC general durante la encuesta).
4. **Diferencia con hace un año,** por rubro: gasto de hoy − gasto de hoy ÷ (1 + variación del IPC del rubro en 12 meses).
5. **Diferencia con el mes anterior** (dato secundario): igual, con la variación mensual.
6. **Total:** suma de los rubros. El porcentaje es la diferencia sobre el gasto de hace un año.

## Resultado al 16-oct-2026 (IPC de septiembre)

| Rubro | Gasto al mes | Variación en 12 meses | Diferencia con hace un año |
|---|---|---|---|
| Transporte | $299.809 | +7,9 % | +$21.866 |
| Comida | $423.729 | +4,3 % | +$17.517 |
| Vivienda, luz, agua y gas | $319.796 | +3,6 % | +$11.080 |
| Todo lo demás | $955.390 | +4,1 % | +$37.363 |
| **Total** | **$1.998.724** | **+4,6 %** | **+$87.826 al mes** |

Frente al mes anterior: +$10.369.

## Cómo se muestra

- **Inicio:** tarjeta compacta con "Impacto Financiero · septiembre", la cifra grande en pesos, "más que hace un año para un hogar típico de Santiago", el porcentaje y la diferencia con el mes anterior. Al tocarla se abre el termómetro.
- **Termómetro "Impacto Financiero"** (`/termometros/impacto`, primero de la lista): el detalle con barras por rubro ("En qué se va la diferencia"), el enlace "Calcular el mío en Mi impacto" (Herramientas) y como indicadores el IPC de transporte, alimentos y vivienda en 12 meses, con su presión.
- Siempre como **indicador propio de referencia**, con la fuente (INE y Banco Central).

## Limitaciones y pendientes

- **Proporciones nacionales:** el reparto por rubro es el de todas las capitales regionales, no solo el Gran Santiago. Con la base de gastos de la EPF ([catalogo-de-datos.md](catalogo-de-datos.md), sección 4) se puede calcular el reparto exacto de Santiago.
- **Es un dato mensual:** cambia una vez al mes, cuando el INE publica el IPC (alrededor del día 8 del mes siguiente). La bencina de hoy no se refleja hasta el IPC siguiente.
- **Mejora posible (versión semanal):** mover con datos de alta frecuencia las partes que los tienen: combustibles con la CNE (a diario), alimentos con ODEPA (semanal), arriendos con la UF (a diario) y gas con la CNE. Para saber cuánto pesa cada una dentro de su rubro (por ejemplo, la bencina dentro del transporte) hace falta la base de gastos de la EPF.
- **Promedio, no mediana:** la mediana del Gran Santiago ($1.204.455) representa mejor al hogar del medio; se usa el promedio porque la encuesta publica el reparto por rubro sobre el promedio.
- **El dividendo no está incluido:** la EPF lo considera pago de deuda, no gasto. Va en Mi impacto.
- **Nueva encuesta:** cuando salga la X EPF (levantamiento 2026-2027), se actualiza la base.
