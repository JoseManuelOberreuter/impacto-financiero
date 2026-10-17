# Impacto Financiero: metodología

> Indicador propio, protagonista del Inicio desde el 16-oct-2026. Responde: **¿cuánto más le cuesta la vida a un hogar típico que hace un año, en pesos al mes?** Código: `impacto-api/app/datos_ejemplo/impacto.py`. Fuentes: [catalogo-de-datos.md](catalogo-de-datos.md).

## Por qué este indicador

- La app se llama Impacto Financiero: el dato principal debe ser **cuánto te impacta**, en pesos y no como un índice abstracto.
- Reemplaza a la canasta semanal como protagonista del Inicio. La canasta sigue en Precios.
- No es un "puntaje global" de la economía (lo descartamos al inicio): es la inflación expresada en pesos para un hogar.
- Conecta con el plan Pro ([plan-pro.md](plan-pro.md)): gratis se ve el impacto de **un hogar típico**; en Mi impacto, el usuario calcula **el suyo**.

## Cálculo

1. **Gasto de un hogar típico:** gasto promedio mensual de los hogares del **Gran Santiago** según la **IX Encuesta de Presupuestos Familiares del INE**: $1.590.105 (oct-2021 a sep-2022).
2. **Reparto por rubro, del propio Gran Santiago:** calculado con los **microdatos** de la encuesta (`scripts/resumen_epf.py`, guardado en `epf_ix.json` → `gran_santiago_microdatos`). Se excluyen los arriendos imputados, igual que el INE; con eso el promedio coincide exacto con el publicado.

   | Rubro | Gasto en la EPF | % | IPC para lo que no tiene dato frecuente |
   |---|---|---|---|
   | Comida | $324.193 | 20,4 % | IPC de alimentos (`F074.IPC.IND.DIV10000.2023.C.M`) |
   | Vivienda, luz, agua y gas | $259.412 | 16,3 % | IPC de vivienda y servicios básicos (`F074.IPC.IND.DIV40000.2023.C.M`) |
   | Transporte | $227.028 | 14,3 % | IPC de transporte (`F074.IPC.IND.DIV70000.2023.C.M`) |
   | Todo lo demás | $779.472 | 49,0 % | IPC general (`G073.IPC.IND.2023.M`) |

3. **Partes con datos frecuentes** (por eso la cifra cambia durante el mes):

   | Parte | Gasto en la EPF | Peso en su rubro | Se mueve con | Frecuencia |
   |---|---|---|---|---|
   | Bencina y diésel | $53.455 | 23,5 % del transporte | Precio de hoy de la bencina 95 (CNE) frente al promedio del mismo mes hace un año | Diaria |
   | Arriendo | $113.191 | 43,6 % de la vivienda | UF de hoy frente a la de hace un año (los arriendos se pactan en UF) | Diaria |
   | Gas licuado | $30.401 | 11,7 % de la vivienda | Último promedio mensual del cilindro de 15 kg (CNE) frente a hace un año | Mensual |

4. **Llevar a precios de hoy:** gasto × (IPC general del último mes ÷ promedio del IPC general durante la encuesta).
5. **Diferencia con hace un año,** por parte: gasto de hoy − gasto de hoy ÷ (1 + variación en 12 meses). La diferencia del rubro es la suma de sus partes.
6. **Diferencia con el mes anterior** (dato secundario): con la variación mensual del IPC de cada rubro.
7. **Total:** suma de los rubros. El porcentaje es la diferencia sobre el gasto de hace un año. La fecha que se muestra ("al 16-oct") es la del dato más reciente.

## Resultado al 16-oct-2026

| Rubro | Gasto al mes | Variación en 12 meses | Diferencia con hace un año |
|---|---|---|---|
| Transporte | $285.369 | +11,5 % | +$29.501 |
| Comida | $407.503 | +4,3 % | +$16.846 |
| Vivienda, luz, agua y gas | $326.075 | +3,6 % | +$11.414 |
| Todo lo demás | $979.778 | +4,1 % | +$38.316 |
| **Total** | **$1.998.725** | **+5,0 %** | **+$96.077 al mes** |

Frente al mes anterior: +$10.261. El transporte sube más que su IPC (+7,9 %) porque la bencina de hoy está 25 % sobre la de octubre de 2025.

Primera versión (solo IPC y proporciones nacionales, 16-oct-2026): +$87.826 (+4,6 %).

## Cómo se muestra

- **Inicio:** tarjeta compacta con "Impacto Financiero · septiembre", la cifra grande en pesos, "más que hace un año para un hogar típico de Santiago", el porcentaje y la diferencia con el mes anterior. Al tocarla se abre el termómetro.
- **Termómetro "Impacto Financiero"** (`/termometros/impacto`, primero de la lista): el detalle con barras por rubro ("En qué se va la diferencia"), el enlace "Calcular el mío en Mi impacto" (Herramientas) y como indicadores el IPC de transporte, alimentos y vivienda en 12 meses, con su presión.
- Siempre como **indicador propio de referencia**, con la fuente (INE y Banco Central).

## Limitaciones y pendientes

- **Qué cambia a diario y qué una vez al mes:** la bencina y la UF se mueven a diario (cuando se actualizan sus fotos); el resto cambia cuando el INE publica el IPC (alrededor del día 8). El 77 % del transporte, el 45 % de la vivienda, toda la comida y "todo lo demás" siguen siendo mensuales.
- **Comida semanal, pendiente:** ODEPA tiene precios semanales, pero solo guardamos 12 semanas y su "variación anual" es desde enero, no en 12 meses. Con el CSV de ODEPA del año pasado, los alimentos de ODEPA (pan, pollo, huevos, papa, tomate, aceite, leche, arroz y posta: $63.472, el 20 % de la comida) se pueden mover cada semana. Sus pesos ya están en `epf_ix.json`.
- **Luz y transporte público:** sin historia frecuente por ahora (la cuenta tipo de la CNE es una sola foto; el pasaje se carga a mano). Siguen con el IPC.
- **Promedio, no mediana:** la mediana del Gran Santiago ($1.204.455) representa mejor al hogar del medio; se usa el promedio porque la encuesta publica el reparto por rubro sobre el promedio.
- **El dividendo no está incluido:** la EPF lo considera pago de deuda, no gasto. Va en Mi impacto.
- **Nueva encuesta:** cuando salga la X EPF (levantamiento 2026-2027), se actualiza la base.
