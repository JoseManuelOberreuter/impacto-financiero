# Termómetros económicos

> Estado: **diseño acordado, por implementar.**

## Idea central

El home no muestra muchos datos. Cada **termómetro** agrupa varios indicadores y los resume en **un estado de presión, un número y una frase**. El detalle está una capa más abajo para quien lo quiera.

**El usuario elige qué termómetros ver en su home** durante el onboarding, y puede cambiarlos después.

## Los termómetros

| Termómetro | Pregunta que responde | Indicadores detrás | Etapa |
|---|---|---|---|
| 🛒 **Bolsillo** | ¿Está más cara la vida? | Índice de canasta, IPC, bencina, gas, pasaje | 1 |
| 🏦 **Deudas** | ¿Está más caro endeudarse? | UF, TPM, tasas de crédito (CMF), TMC | 1 |
| 💰 **Ahorro y pensiones** | ¿Cómo le va a mi plata? | Fondos AFP A–E, UF vs. depósito a plazo | 1 |
| 🏭 **Actividad y empleo** | ¿Cómo va la economía en general? | IMACEC, desempleo, remuneraciones | 1 |
| 💵 **Dólar y mercados** | ¿Qué pasa afuera? | Dólar, cobre, IPSA (cuando tengamos licencia) | 1 (sin IPSA) |
| 📰 **Ánimo** | ¿De qué se está hablando? | Tono de la prensa, incertidumbre, hechos esenciales, IPEC (ver [sentimiento-noticias.md](sentimiento-noticias.md)) | 1 |

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
- **Cómo se calcula (propuesta):** cada indicador se compara con su propia historia de los últimos 5 años.
  - La variación actual está en el 20 % más alto → presión **alta**.
  - En el 20 % más bajo → presión **baja**.
  - En el resto → presión **media**.
  - El estado del termómetro combina el de sus indicadores. La regla exacta está por definir.
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

- ✅ El usuario elige y ordena sus termómetros en el onboarding, y puede cambiarlos después.
- ✅ Se habla de "presión", no de "bueno o malo".
- ❌ **Sin puntaje global** de la economía (tipo "6,2/10"): es demasiado opinable.

## Pendiente

- [ ] Regla exacta para combinar los indicadores en el estado de cada termómetro.
- [ ] Confirmar el máximo de termómetros en el home (4) con pruebas de usuarios.
- [ ] Texto final de cada pantalla del onboarding.
- [ ] Si "Dólar y mercados" y "Ánimo" van como termómetros completos o como una línea en el resumen del día.
