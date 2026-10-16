# Índice Impacto de la Canasta

> Estado: **borrador de metodología.** Es un indicador **propio**, calculado por nosotros a partir de datos públicos. **No es el IPC ni un dato oficial.**

## Qué es

Un indicador semanal que responde a la pregunta: **¿cuánto cuesta esta semana una canasta típica del día a día y cuánto cambió?**

Se muestra de dos formas:
- **En pesos:** "La canasta cuesta $XX.XXX esta semana (+$350 vs. la semana pasada)".
- **Como índice:** base 100 en una semana de referencia, para ver la tendencia en el tiempo.

## Por qué hacerlo

- El IPC es mensual, sale con un mes de atraso y mide una canasta muy amplia que la gente no siente como propia.
- Este índice es **semanal**, usa productos que todos compran y se entiende sin saber economía.
- Es un dato **propio y difícil de copiar**: es parte de lo que diferencia la app.

## Composición (propuesta inicial)

| Producto | Cantidad | Unidad de la fuente | Fuente |
|---|---|---|---|
| Marraqueta | 4 kg | $/kilo | ODEPA |
| Leche fluida entera | 4 L | $/caja 1 L | ODEPA |
| Huevos (blanco grande, primera) | 1 bandeja | $/bandeja 30 unidades | ODEPA |
| Aceite vegetal | 1 botella | $/botella 900 ml | ODEPA |
| Pollo entero | 2 kg | $/kilo | ODEPA |
| Carne de vacuno (posta rosada) | 1 kg | $/kilo | ODEPA |
| Bencina 95 | 20 L | $/litro | CNE |
| Gas licuado | 1 cilindro | $/cilindro 15 kg | CNE |
| Pasaje de Metro (hora punta) | 40 viajes | $/viaje | Panel de Expertos |

Las cantidades son un punto de partida para un hogar tipo y una semana, y **hay que revisarlas**. Una opción es tomar como referencia las proporciones de la canasta básica del Ministerio de Desarrollo Social o las ponderaciones del IPC del INE.

## Cálculo

1. **Precio por producto:** para cada producto se toma el "Precio promedio" de ODEPA de la semana. Luego se calcula la **mediana** entre los sectores de la región y los tipos de local (supermercado, feria, panadería, carnicería). La mediana evita que un sector o local extremo distorsione el resultado.
2. **Bencina y gas:**
   - **Bencina 95:** mediana de las estaciones de la región que actualizaron su precio en los últimos 7 días (ver la regla de la CNE en [fuentes-de-datos.md](fuentes-de-datos.md)).
   - **Gas:** promedio mensual de la CNE del cilindro corriente de 15 kg en la región.
3. **Pasaje:** tarifa vigente; se cambia solo cuando hay una resolución nueva.
4. **Costo de la canasta** = Σ (precio × cantidad).
5. **Índice** = costo de la semana ÷ costo de la semana base × 100.
6. **Variaciones:** semanal, mensual (4 semanas) y anual (52 semanas).

## Alcance

- **Etapa 1:** solo Región Metropolitana.
- **Después:** otras regiones donde ODEPA y la CNE tengan datos (Valparaíso, Biobío, etc.), para comparar el costo de vida entre ciudades. El transporte será el más difícil, porque cada ciudad tiene su tarifa.

## Historia disponible

- ODEPA publica CSV por año (al menos desde 2023), así que la parte de alimentos se puede **calcular hacia atrás** desde el día uno.
- **La CNE sí entrega historia,** pero solo mensual: bencina desde 1994 y gas desde 2000, por región. Sirve para el gráfico y la presión, pero no para la serie semanal de la canasta.
- **Mientras no guardemos el precio diario,** la canasta usa el precio de hoy de la bencina y el gas en todas las semanas. Su variación semanal refleja solo los alimentos. Hay que empezar a guardar el precio diario cuanto antes.

## Reglas de comunicación

- Siempre decir que es un **indicador propio de referencia** y citar las fuentes (ODEPA, CNE, Panel de Expertos).
- Mostrarlo **junto al IPC oficial** para comparar, nunca en su lugar.
- Publicar la **metodología** (esta ficha) en la app, para que cualquiera pueda revisar cómo se calcula.
- Si un producto no tiene dato en una semana, usar el de la semana anterior y **marcarlo**.
- Si cambia la composición o el método, avisarlo y recalcular la serie con el método nuevo.

## Decisiones pendientes

- [ ] Cantidades definitivas de cada producto.
- [ ] Semana base del índice (por ejemplo, la primera semana de 2026).
- [ ] Qué tipos de local incluir: todos, o separar un índice de supermercado y otro de feria y almacén.
- [ ] Si se agregan productos (frutas y verduras de temporada, arroz, fideos, luz, agua).
- [ ] Nombre definitivo del indicador.
