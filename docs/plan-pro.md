# Plan Pro: qué vende y cómo validarlo

> Plan al 16-oct-2026. Resuelve el riesgo de negocio más grande: que la gente no pague porque espera estos datos gratis. Relacionado: [planes.md](planes.md) (capacidades, modos y base de datos) y [riesgos.md](riesgos.md).

## La idea

El plan Pro no vende "más datos". Cada plan responde una pregunta distinta:

| Plan | Pregunta que responde | Ejemplo |
|---|---|---|
| **Gratis** | ¿Qué pasó? | "El dólar está en $984, presión alta" |
| **Pro** | **¿Qué viene, por qué pasó y cuánto me afecta a mí?** | "Este mes pagas $8.400 más entre el dividendo y la bencina; el jueves la bencina sube unos $12" |

Lo gratis sigue siendo útil y se puede compartir: es lo que trae usuarios. Lo Pro es **personal y anticipado**: le ahorra plata o sorpresas a quien lo usa.

## Los 4 pilares

### 1. Mi impacto (lo que más vende)

El usuario ingresa sus datos una vez y la app le dice **en pesos** cuánto le afecta la economía.

| Dato del usuario | Qué le mostramos | Fuente |
|---|---|---|
| Dividendo o crédito en UF | Cuánto paga hoy, cuánto pagará con la última UF publicada (la UF se conoce hasta el día 9 del mes siguiente) y cuánto más que hace un mes y un año | Banco Central (UF) |
| Litros de bencina a la semana | Gasto mensual hoy y cuánto más o menos que hace un año | CNE |
| Sueldo y fecha del último reajuste | Cuánto poder de compra perdió desde entonces | Banco Central (IPC) |
| AFP, fondo y saldo aproximado | Cuánto ganó o perdió en pesos este mes y este año | Superintendencia de Pensiones |

**Los datos se quedan en el teléfono** del usuario (no hay cuentas ni servidor). Es lo que el nombre "Impacto Financiero" promete, y simplifica la ley de datos personales.

**Vista previa gratis:** el dividendo. El resto es Pro.

### 2. Lo que viene (anticiparse)

- **Calendario con expectativas:** "Jueves: IPC de octubre, se espera 0,3 %". Después de la publicación: "Salió 0,5 %, peor de lo esperado".
- **Aviso de la bencina:** estimación de la próxima variación con el petróleo, el dólar y la paridad semanal de ENAP. Siempre rotulado como estimación.
- **Tasas que vienen:** "Los economistas esperan que la TPM baje a 4,25 % en un año; un crédito como el tuyo bajaría unos $X".
- **UF de los próximos días,** ya publicada por el Banco Central.

### 3. Cruces (entender el porqué)

- Bencina frente al petróleo y el dólar.
- Dólar frente al cobre.
- Nuestra canasta frente al IPC oficial de alimentos.
- Lo que la gente dice (IPEC) frente a lo que compra (ventas diarias del comercio).
- Tasa real de un crédito: la tasa menos la inflación esperada.
- Sorpresa del dato: "el IPC sorprendió al alza 4 de los últimos 6 meses".

### 4. Alertas (el motivo para mantener la suscripción)

- **Sobre los datos anclados:** quien ancla un dato (gratis, hasta 3) puede pedir que le avisen cuando se mueva; las alertas son Pro, y en Pro los anclados no tienen límite.

- **Umbrales:** "avísame si el dólar pasa de $1.000" o "si la tasa hipotecaria baja de 4 %".
- **Publicaciones:** "salió el desempleo: 9,6 %, sobre lo esperado".
- **Personales:** "tu dividendo sube $X el próximo mes", "tu fondo cayó más de 3 % esta semana".

Además: historia de hasta 20 años y descarga de series en CSV.

## Gratis y Pro

| Función | Gratis | Pro | Capacidad |
|---|---|---|---|
| Termómetros, canasta, precios y noticias | Sí | Sí | `termometros.basico` |
| "Lo que cambió esta semana" | Sí | Sí | — |
| Mi AFP (rentabilidad) | Sí | Sí, más la ganancia en pesos | `mi_impacto` |
| Calculadoras con tasas reales | Básicas | Con escenarios | `calculadoras.basicas`, `calculadoras.escenarios` |
| Calendario de publicaciones | Fechas | Con lo esperado y la sorpresa | `calendario.basico`, `calendario.expectativas` |
| **Mi impacto en pesos** | Vista previa (dividendo) | Completo | `mi_impacto` |
| **Lo que viene** | — | Sí | `expectativas`, `aviso_bencina` |
| **Cruces** | — | Sí | `cruces`, `sorpresa_dato` |
| **Alertas** | — | Sí | `alertas` |
| Historia larga y descargas | 12 meses | 20 años y CSV | `historia.larga`, `descargas.csv` |

## Cómo validarlo antes de construir el cobro

1. **Puerta falsa:** un botón "Pro" que lleve a "Pronto: déjanos tu correo". Mide cuánta gente lo aprieta.
2. **Modo `vista_previa`** ([planes.md](planes.md)): todo abierto, pero lo Pro con su etiqueta. Medir qué funciones Pro se usan más.
3. **10 entrevistas** mostrando Mi impacto: ¿pagarías $3.990 al mes por esto?
4. **Al lanzar:** 14 días de prueba gratis y medir cuántos se quedan pagando.

## Orden de trabajo

| Paso | Qué | Datos | Estado |
|---|---|---|---|
| 1 | Capacidades y `BloquePro` (la base para marcar lo Pro) | No necesita | ✅ Hecho (16-oct-2026) |
| 2 | Mi impacto: dividendo y bencina, guardados en el teléfono | UF y bencina, ya disponibles | ✅ Hecho (16-oct-2026) |
| 3 | Lo que viene: calendario con expectativas y sorpresa | Expectativas del Banco Central; faltan las fechas oficiales | Pendiente |
| 4 | Cruces en Dólar y Bolsillo | Ya disponibles | Pendiente |
| 5 | Aviso de la bencina | Falta la paridad semanal de ENAP | Pendiente |
| 6 | Puerta falsa del Pro | No necesita | Pendiente |
| 7 | Alertas (notificaciones) | Necesita cuentas y el worker | Pendiente |
| 8 | Mi impacto: sueldo y AFP en pesos | Ya disponibles | Pendiente |

Con los pasos 1 a 4 y el 6 hay un **Pro demostrable** para mostrar a gente real, sin pagos ni cuentas.
