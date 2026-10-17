# Termómetros económicos

> Estado: **diseño acordado, por implementar.**

## Idea central

El home no muestra muchos datos. Cada **termómetro** agrupa varios indicadores y los resume en **un estado de presión, un número y una frase**. El detalle está una capa más abajo para quien lo quiera.

**El usuario elige qué termómetros ver en su home** durante el onboarding, y puede cambiarlos después.

## Los termómetros

| Termómetro | Pregunta que responde | Indicadores detrás | Etapa |
|---|---|---|---|
| 🛒 **Bolsillo** | ¿Está más cara la vida? | Índice de canasta, IPC, bencina, gas, pasaje | 1 |
| 🏦 **Deudas** | ¿Está más caro endeudarse? | TPM, tasa máxima convencional (CMF), tasa hipotecaria y de consumo | 1 |
| 💰 **Ahorro y pensiones** | ¿Cómo le va a mi plata? | Fondos AFP A–E, UF vs. depósito a plazo | 1 |
| 🏭 **Actividad y empleo** | ¿Cómo va la economía en general? | IMACEC, desempleo, remuneraciones | 1 |
| 💵 **Dólar y mercados** | ¿Qué pasa afuera? | Dólar, cobre, IPSA (cuando tengamos licencia) | 1 (sin IPSA) |
| 📰 **Ánimo** | ¿Cómo se siente la gente? | Hoy: percepción de las personas (IPEC) y confianza de las empresas (IMCE). Después: tono de la prensa, incertidumbre y hechos esenciales (ver [sentimiento-noticias.md](sentimiento-noticias.md)) | 1 |

## Onboarding y personalización

El onboarding explica en pocas pantallas cómo funciona la app y deja al usuario armar su home.

1. **Bienvenida:** qué es la app en una frase ("La economía chilena explicada según cómo te afecta a ti").
2. **Qué es un termómetro:** una tarjeta de ejemplo explicando estado de presión, número, frase y fecha del dato.
3. **Elige tus termómetros:** el usuario marca los que quiere ver en su home.
   - Se pueden elegir **hasta 4**, para mantener el home liviano. Esto se puede ajustar después de probar con usuarios.
   - Cada opción muestra su pregunta ("¿Está más cara la vida?") para que se entienda sin saber economía.
   - Puede ordenarlos.
4. **Mi AFP (opcional):** elegir AFP y fondo para ver cómo le va. Se puede saltar.
5. **Listo:** se muestra su home armado.

**Reglas:**
- **Se puede saltar todo.** Si el usuario salta, ve el home por defecto: Bolsillo, Deudas, Ahorro y pensiones y Actividad y empleo.
- **Se puede cambiar después** desde un botón "Personalizar" en el home.
- Los termómetros no elegidos **siguen disponibles** en el menú; solo no aparecen en el home.
- **Sin login en la etapa 1:** las preferencias se guardan en el navegador del usuario. Si cambia de dispositivo o borra datos, vuelve al home por defecto. Cuando haya cuentas (etapa 2), las preferencias se sincronizan.

## Inicio actual (propuesta G, 15-oct-2026)

Se eligió la **propuesta G** entre 7 diseños hechos en Figma ([Impacto Financiero — Inicio (propuestas)](https://www.figma.com/design/WRgfk96kZ7FSh4UNc0TFuC)), con los termómetros en tarjetas tal como los ajustó el usuario:

```
Impacto                               Jueves 15 de octubre   ← fecha arriba a la derecha

Hoy en Chile
La canasta baja un poco: el pan cae 1 % esta semana.         ← titular grande
La tasa del Banco Central sigue en 4,5 % y el dólar bajó.    ← bajada

┌ vidrio ─────────────────────────────────────────┐
│ Canasta semanal                                 │
│ $126.626                    ~~ mini gráfico ~~  │
│ −0,2 %                                          │
└─────────────────────────────────────────────────┘

Lo que cambió esta semana
┌ vidrio ─────────────────────────────────────────┐
│ ↘ Bencina 95   $1.559 el litro · −2,2 %  ~~~~~  │
│ ↘ Gas 15 kg    $31.530 · −3,3 %          ~~~~~  │
│ ↗ Papa         +4,2 % · $1.596 el kilo   ~~~~~  │
│ ↗ Petróleo     US$ 101,9 · +7,3 %        ~~~~~  │
│ ↗ Desempleo    9,6 % · +1,1 pp           ~~~~~  │
│ ↗ IMACEC       −1,0 % en 12 meses        ~~~~~  │
│ — Dólar        $984 · +0,3 %             ~~~~~  │
└─────────────────────────────────────────────────┘

Termómetros
[Bolsillo  Presión Media ↘] [Deudas     Presión Media —]
[Ahorro    Presión Media —] [Actividad  Presión Alta  ↗]
```

- **Lo que más le gustó al usuario:** el titular grande, que haya gráficos y las flechas de "lo que cambió".
- **Selector de país:** bandera de Chile dibujada (no emoji), fija en la esquina superior derecha de toda la app, igual que el aviso de "Datos de ejemplo" (`components/selector-pais.tsx`, puesto en `app/_layout.tsx`). Al tocarla muestra "Chile" marcado y "Próximamente más países".
- **Encabezado del Inicio:** en escritorio, "Hoy en Chile" va en la misma fila que la fecha; en el teléfono, la fila lleva "Impacto" y la fecha (con espacio para la bandera), y "Hoy en Chile" queda sobre el titular.
- **Impacto Financiero** (desde el 16-oct-2026): reemplaza a la tarjeta de la canasta como protagonista del Inicio. En el Inicio va solo la cifra (cuánto más le cuesta la vida a un hogar típico de Santiago que hace un año); el detalle por rubro y "Calcular el mío" están en su termómetro (`/termometros/impacto`). Metodología: [impacto-financiero.md](impacto-financiero.md).
- **"Lo que cambió esta semana"** (`cambios` en `GET /v1/home`), desde el 16-oct-2026: **todos los datos compiten** y se muestran los que más presionan. Código: `_candidatos` y `_cambios` en `impacto-api/app/datos_ejemplo/home.py`.
  - **Candidatos (15):** bencina 95, gas licuado 15 kg, el alimento que más se movió en la semana, dólar, cobre, petróleo WTI, UF, tasa máxima de los créditos, TPM, tasa hipotecaria, IPC, desempleo, IMACEC, percepción de las personas (IPEC) y confianza de las empresas (IMCE).
  - **Orden:** presión alta primero, después media y baja. En cada nivel, los que se movieron van antes que los estables.
  - **Límites:** hasta 7 filas, máximo 2 por tema (energía, alimentos, afuera, deudas, precios, empleo, ánimo) y un solo alimento, porque la canasta ya los resume.
  - **Datos mensuales** (IPC, desempleo, IMACEC, IPEC, IMCE): entran solo con presión alta. **Pendiente:** que entren también la semana en que se publican, cuando guardemos la fecha de publicación de cada dato.
  - **Bencina:** se compara con el último mes con dato de la CNE hasta guardar el precio diario.
  - **Color:** según la presión sobre el bolsillo. Un alimento que sube = alta; uno que baja = baja; un cambio menor a 0,5 % = estable.
  - **Enlace:** cada fila lleva a su detalle.
- **Descartados:** el panel de presión como protagonista (B) y el carrusel tipo historias (D).
- **Mi AFP** no está en el Inicio por ahora, para no sobrecargarlo.

### Estilo visual

- **Minimalista y moderno**, inspirado en el **Liquid Glass** de iOS 26: superficies de vidrio sobre un fondo con luces difusas.
- **Fondo "pizarra azul"** (`#E8ECF2` en claro, `#0A0E16` en oscuro), elegido el 16-oct-2026: azul grisáceo, serio y financiero, con manchas difusas azul acero (claro) y azul marino (oscuro). Igual en todas las pestañas. Las otras paletas probadas (piedra cálida, piedra fresca y verde azulado) quedaron guardadas en `impacto-app/src/constants/theme.ts`.
- En **iPhone con iOS 26** se usa el vidrio nativo (`expo-glass-effect`). En **web** se imita con desenfoque (`backdrop-filter`). En el resto de las plataformas se usa una superficie translúcida.
- **Tipografía grande** para el titular y el precio; textos secundarios en gris.
- **Íconos de Lucide** con el color del nivel de presión. Nunca emojis.

## Navegación y páginas (15-oct-2026)

**Menú de 5 secciones:**
- **iPhone y Android:** barra de pestañas nativa abajo (`NativeTabs` de Expo Router). En iOS 26 usa Liquid Glass. Los íconos son SF Symbols en iOS y Material Symbols en Android.
- **Web en escritorio:** barra de vidrio arriba, con la marca a la izquierda.
- **Web en pantallas angostas:** barra de vidrio abajo, igual que en el celular.

| Sección | Ruta | Contenido |
|---|---|---|
| Inicio | `/` | Minimalista: titular del día, marraqueta con canasta y termómetros compactos |
| Termómetros | `/termometros` | Los 6 termómetros con nivel, dato clave y frase |
| ↳ Detalle | `/termometros/[id]` | Explicación, indicadores con gráfico y banda de "lo normal", percepción, próximas publicaciones, herramienta relacionada y metodología |
| Precios | `/precios` | Canasta (total, evolución y en qué se va), productos por categoría, energía y transporte |
| ↳ Detalle | `/precios/[id]` | Precio, 12 semanas, dónde se compra (tipo de local) y comparación por región |
| Noticias | `/noticias` | Ánimo de la semana (tono, incertidumbre), temas que dominan con titulares, hechos esenciales |
| Herramientas | `/herramientas` | Mi AFP (rentabilidad por fondo y AFP), calculadoras (pronto), calendario económico, metodología y Ajustes (apariencia: automático, claro u oscuro) |

**Datos reales y de ejemplo en estas páginas:**
- **Reales**, como foto fija:
  - Precios de alimentos de ODEPA (semana al 9-oct-2026). Se generan con `impacto-api/scripts/snapshot_odepa.py`.
  - Rentabilidad de las AFP, provisional al 13-oct-2026. Se genera con `impacto-api/scripts/snapshot_afp.py`.
  - Tarifa del Metro.
- **De ejemplo:** IPC, TPM, desempleo, IMACEC, dólar, bencina, gas, tono de las noticias y titulares. Los titulares no se atribuyen a medios reales.

## Tres niveles de profundidad

```
HOME  (30 segundos)
├─ Resumen del día: 2 líneas
├─ Termómetros elegidos por el usuario (hasta 4): estado + 1 número + 1 frase + fecha
└─ Mi AFP (si la configuró; si no, invitación a configurarla)
      │
      ▼
PÁGINA DEL TERMÓMETRO  (2 minutos)
├─ Por qué está así: explicación simple
├─ Los 3–6 indicadores que lo componen, con gráfico corto
└─ Calculadora relacionada (ej. Deudas → "¿cuánto sube mi dividendo?")
      │
      ▼
FICHA DEL INDICADOR  (para curiosos e inversionistas; base del plan Pro)
└─ Serie histórica, fuente, metodología, desfase, próxima actualización
```

Ejemplo de tarjeta:

```
🛒 Presión en tu bolsillo        MEDIA ▲
Canasta: $48.300 (+0,7 % semanal)
"Subieron el pan y la bencina; bajó el pollo."
Dato al 9-oct · próxima actualización 16-oct
```

## Estado de presión

- Se habla de **presión** (baja / media / alta), **no de "bueno" o "malo"**. Un mismo dato puede ser bueno para unos y malo para otros (un dólar alto perjudica a quien importa y beneficia a quien exporta).
- **Cómo se calcula (implementado en `impacto-api/app/calculos/presion.py`):** cada indicador se compara con su propia historia de los últimos 5 años.
  - El valor actual está sobre el percentil 80 → presión **alta**.
  - Bajo el percentil 20 → presión **baja**.
  - En el resto → presión **media**. La franja gris de los gráficos es ese rango normal (percentiles 20 a 80).
  - **Indicadores invertidos:** en el IMACEC, el cobre, el IPEC y el IMCE un valor *bajo* es el que presiona, así que la regla se da vuelta.
  - **Estado del termómetro:** manda la presión más alta de sus indicadores principales (Bolsillo: IPC y bencina; Deudas: TPM y tasa máxima; Actividad: desempleo e IMACEC; Ánimo: IPEC e IMCE).
  - **Historia corta:** la marraqueta y la canasta usan sus últimas 12 semanas hasta guardar más historia. Las AFP quedan en presión media hasta guardar la historia de sus valores cuota.
- Las reglas se **publican** en la app, igual que la metodología de la canasta.
- Además del estado se muestra la **tendencia** (▲ ▼ ●) respecto del dato anterior.

## Aprendizajes de la investigación

Ver [investigacion-diseno.md](investigacion-diseno.md). Los más relevantes para los termómetros:
- **Presión = distancia a lo normal**, como el índice de presión de cadenas de suministro de la Fed de Nueva York. Mostrar en los gráficos la banda de lo "normal".
- **Separar datos duros de percepción** (por ejemplo, la canasta vs. el IPEC) y mostrar ambos.
- **Dato oficial vs. "cómo te afecta a ti"** ("sensación térmica"), como las calculadoras de inflación personal del BCE y de la ONS.
- **Metodología pública** (a diferencia del Fear & Greed de CNN).
- El estado se **escribe** además del color, por accesibilidad.

## Decisiones tomadas

- ✅ **La personalización espera a la base de datos (15-oct-2026):** el primer home muestra solo los 4 termómetros por defecto. Elegir y ordenar termómetros se implementa cuando se puedan guardar las preferencias.
- ✅ **Íconos de librería, nunca emojis:** se usa [Lucide](https://lucide.dev), que permite configurar el color y el tamaño.
- ✅ El usuario elige y ordena sus termómetros en el onboarding, y puede cambiarlos después.
- ✅ Se habla de "presión", no de "bueno o malo".
- ❌ **Sin puntaje global** de la economía (tipo "6,2/10"): es demasiado opinable.

## Pendiente

- [ ] Regla exacta para combinar los indicadores en el estado de cada termómetro.
- [ ] Confirmar el máximo de termómetros en el home (4) con pruebas de usuarios.
- [ ] Texto final de cada pantalla del onboarding.
- [ ] Si "Dólar y mercados" y "Ánimo" van como termómetros completos o como una línea en el resumen del día.
