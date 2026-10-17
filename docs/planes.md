# Planes y capacidades

> Plan general al 15-oct-2026. Todavía no se cobra ni hay empresa (la SpA se crea antes del primer cobro). El objetivo es organizar la data y las secciones desde ya, para que activar el cobro sea cambiar una configuración y no reescribir código.
> Relacionado: [plan-pro.md](plan-pro.md) (qué vende el Pro), [riesgos.md](riesgos.md), [pendientes-backend.md](pendientes-backend.md), [arquitectura.md](arquitectura.md) y [banco-central-series.md](banco-central-series.md).

## 1. Los planes

Los planes se dividen **por tipo de cliente**, no por cantidad de funciones. Coinciden con las etapas del [README](../README.md#público-por-etapas).

| Plan | Para quién | Qué compra | Precio de referencia (hipótesis) |
|---|---|---|---|
| **Gratis** | Personas | Entender el día: termómetros, canasta, Mi AFP, noticias y calculadoras básicas | $0 |
| **Pro** | Personas informadas e inversionistas | Profundidad: expectativas, sorpresa del dato, historia larga, cruces, alertas, descargas y escenarios | ~$3.990 al mes o ~$39.990 al año |
| **Empresas** | Pymes, contadores, medios y fintech | Todo Pro, más "Mi rubro", reajustes por IPC, varios usuarios, factura y acceso a la API | Desde ~$24.990 al mes, más uso de la API por tramos |

**Decisiones:**
- **No hay un tercer plan para personas** ("Super Pro"). Es difícil explicar qué tendría de más. Empresas responde a una necesidad distinta: factura, varios usuarios e integración.
- **La API va dentro de Empresas**, no como plan aparte. Vendemos lo que calculamos nosotros (canasta, presión de cada termómetro, sorpresa del dato), **no los datos crudos** de las fuentes oficiales. Antes de venderla hay que revisar qué permite redistribuir cada fuente según sus términos de uso.
- **Los precios son hipótesis.** Se definen con los datos de uso del modo `abierto` y con entrevistas.

## 2. Capacidades

El código **nunca pregunta por el plan**. Pregunta si el usuario tiene una capacidad: `puede("expectativas")`. Cada plan es una lista de capacidades, guardada en la base de datos.

Así, mover una función de plan, regalarla en una promoción o crear un plan nuevo se hace sin tocar el código.

| Capacidad | Qué habilita | Gratis | Pro | Empresas |
|---|---|---|---|---|
| `termometros.basico` | Nivel de presión, dato principal y frase | Sí | Sí | Sí |
| `historia.1_anio` | Gráficos de hasta 12 meses | Sí | Sí | Sí |
| `historia.larga` | Gráficos de 5, 10 y 20 años | — | Sí | Sí |
| `expectativas` | "Lo que viene": EEE, EOF e inflación esperada | — | Sí | Sí |
| `sorpresa_dato` | Dato real vs. lo esperado, e historial de sorpresas | — | Sí | Sí |
| `cruces` | Gráficos que comparan dos series (por ejemplo, IPEC vs. ventas diarias) | — | Sí | Sí |
| `termometro.consumo` | Detalle del termómetro de Consumo | Nivel | Sí | Sí |
| `termometro.vivienda` | Termómetro de Vivienda | — | Sí | Sí |
| `precios.vs_ipc` | Nuestra canasta vs. el IPC de alimentos | — | Sí | Sí |
| `aviso_bencina` | Estimación de la próxima variación de la bencina | — | Sí | Sí |
| `mi_impacto` | Mi impacto completo en pesos: bencina, sueldo y AFP (el dividendo es la vista previa gratis). Ver [plan-pro.md](plan-pro.md) | Vista previa | Sí | Sí |
| `datos.anclados` | Datos anclados arriba en "Lo que cambió esta semana" (con límite) | 3 | Sin límite | Sin límite |
| `calculadoras.basicas` | Dividendo, crédito y sueldo vs. inflación con tasas reales | Sí | Sí | Sí |
| `calculadoras.escenarios` | Calculadoras con escenarios de TPM e inflación esperadas | — | Sí | Sí |
| `alertas` | Avisos de umbrales y publicaciones (con límite) | — | 10 | 50 |
| `descargas.csv` | Descargar series con la fuente citada | — | Sí | Sí |
| `calendario.basico` | Fechas reales de publicación | Sí | Sí | Sí |
| `calendario.expectativas` | Lo esperado y la sorpresa en cada fecha | — | Sí | Sí |
| `mi_rubro` | Ventas, sueldos, confianza y crédito del rubro y tamaño de empresa | — | — | Sí |
| `reajustes_ipc` | Reajustes de contratos y arriendos por IPC o UF | — | — | Sí |
| `usuarios` | Usuarios por cuenta (con límite) | 1 | 1 | 5 |
| `api.acceso` | Claves para usar nuestra API | — | — | Sí |
| `api.limite_diario` | Consultas a la API por día (con límite) | — | — | 10.000 |

**Reglas:**
1. **Toda función nueva nace con su capacidad.** Si no tiene una, es de `termometros.basico` o de otra capacidad gratis.
2. **La API es la que recorta, no la app.** A quien no tiene `historia.larga`, la API le entrega 12 meses aunque pida 20 años. Si solo se ocultara en la app, cualquiera podría sacar los datos Pro mirando las respuestas.
3. **La app pide sus capacidades una sola vez** (`GET /v1/yo/capacidades`) y con eso decide si muestra el contenido o el `BloquePro`.
4. **Las capacidades con límite** (alertas, usuarios, API) guardan el número en la relación plan–capacidad.

## 3. El switch: modos de los planes

La variable de entorno `MODO_PLANES` del backend define cómo se aplican:

| Modo | Qué pasa | Cuándo |
|---|---|---|
| `abierto` | Todos tienen todas las capacidades, sin etiquetas | **Ahora**, durante el MVP: medir qué se usa |
| `vista_previa` | Todos tienen todo, pero lo Pro y lo de Empresas lleva una etiqueta | Antes de cobrar: ver qué despierta interés |
| `activo` | Cada usuario recibe las capacidades de su plan; el resto aparece con `BloquePro` | Con la SpA y el cobro funcionando |

El endpoint de capacidades devuelve el modo junto con la lista. La app no tiene lógica propia de planes.

```json
{
  "modo": "abierto",
  "plan": "gratis",
  "capacidades": {
    "historia.larga": { "activa": true, "plan_minimo": "pro" },
    "alertas": { "activa": true, "plan_minimo": "pro", "limite": 10 }
  }
}
```

- `plan_minimo` le sirve a la app para la etiqueta y el `BloquePro`: "Disponible en Pro".
- En modo `abierto` todo viene con `activa: true`. En modo `activo` solo lo del plan del usuario.

## 4. Base de datos (Supabase)

### Configuración de planes (se edita sin código)

| Tabla | Columnas principales |
|---|---|
| `planes` | `id` (`gratis`, `pro`, `empresas`), `nombre`, `precio_mensual`, `precio_anual`, `activo` |
| `capacidades` | `id` (`expectativas`, `historia.larga`, ...), `descripcion` |
| `plan_capacidades` | `plan_id`, `capacidad_id`, `limite` (opcional) |

### Usuarios y pagos

| Tabla | Columnas principales | Cuándo se crea |
|---|---|---|
| `usuarios` | La entrega Supabase Auth | Con las cuentas |
| `suscripciones` | `usuario_id` u `organizacion_id`, `plan_id`, `estado` (`prueba`, `activa`, `vencida`, `cancelada`), `origen` (`google_play`, `app_store`, `web`, `factura`), `vence_el`, `id_externo` | Con el cobro |
| `organizaciones` y `miembros` | Cuenta de Empresas con varios usuarios y sus roles | Con el plan Empresas |
| `claves_api` | `organizacion_id`, clave guardada solo como hash, `creada_el`, `revocada_el` | Con la API para terceros |
| `uso_api` | `clave_id`, `dia`, `consultas` | Con la API para terceros |
| `uso_capacidades` | `usuario_id` (o anónimo), `capacidad_id`, `fecha` | **Desde el MVP:** dice qué vale la pena cobrar |

**Los datos no cambian por plan.** Las tablas de series y observaciones ([pendientes-backend.md](pendientes-backend.md), fase 1) son una sola. La API recorta según las capacidades; no se duplican datos por plan.

### Pagos

- **App (Android e iPhone):** las suscripciones digitales dentro de la app deben cobrarse con Google Play Billing y la App Store.
- **RevenueCat:** se recomienda para unificar Google Play, la App Store y la web en un solo lugar. Es gratis hasta unos US$2.500 de ingresos al mes. Cuando alguien paga, RevenueCat avisa a la API con un webhook, y la API actualiza `suscripciones`.
- **Web:** un procesador que sea vendedor registrado (Paddle o Lemon Squeezy) se encarga de los impuestos. Con Mercado Pago o Webpay, la empresa emite la boleta y paga el IVA.
- **Empresas y API:** se cobran con factura de la SpA.
- **Prueba gratis:** 14 días de Pro.

## 5. En la app

| Pieza | Archivo | Qué hace |
|---|---|---|
| `ProveedorCapacidades` y `useCapacidades()` | `impacto-app/src/hooks/use-capacidades.tsx` | Carga `/v1/yo/capacidades` una vez al abrir la app y expone `modo`, `puede(id)` y `planMinimo(id)`. Si la API no responde, todo queda abierto: nunca se bloquea a alguien por un error de red |
| `<Capacidad id="mi_impacto">` | `impacto-app/src/components/capacidad.tsx` | Muestra su contenido si hay acceso; si no, el `BloquePro`. En `vista_previa` agrega la etiqueta del plan |
| `BloquePro` y `EtiquetaPlan` | `impacto-app/src/components/bloque-pro.tsx` | Tarjeta "Disponible en Pro" con candado y descripción; etiqueta pequeña "Pro". Pendiente: botón para conocer el plan (la puerta falsa de [plan-pro.md](plan-pro.md)) |

**Backend:** el catálogo vive en `impacto-api/app/planes.py` hasta que exista Supabase, con `puede(capacidad, plan)` y `capacidades(plan)`. Sin cuentas, todos son plan gratis.

**Probado el 16-oct-2026:** con `MODO_PLANES=activo`, la parte de bencina de Mi impacto aparece como "Disponible en Pro"; con `abierto` (el valor por defecto), se ve completa.

Las funciones nuevas que salen de las [series del Banco Central](banco-central-series.md) nacen con su capacidad:
- capa Pro de los termómetros;
- termómetros de Consumo y Vivienda;
- calculadoras con escenarios;
- "Mi rubro";
- calendario con expectativas.

## 6. Orden de trabajo

| Paso | Qué | ¿Necesita cuentas o empresa? |
|---|---|---|
| 1 | ✅ Catálogo de capacidades en el backend, `MODO_PLANES=abierto` y endpoint `/v1/yo/capacidades` (16-oct-2026). Falta el recorte en la API cuando exista contenido Pro en las respuestas (por ejemplo, `historia.larga`) | No |
| 2 | ✅ `useCapacidades`, `<Capacidad>` y `BloquePro` en la app (16-oct-2026) | No |
| 3 | Construir cada función nueva ya etiquetada con su capacidad | No |
| 4 | Tablas de planes y capacidades en Supabase; registro de `uso_capacidades` | No |
| 5 | Cuentas (Supabase Auth), tabla `suscripciones` y modo `vista_previa` | Cuentas |
| 6 | RevenueCat, Google Play Billing, prueba gratis y modo `activo` | SpA |
| 7 | Organizaciones, claves y límites de la API, y portal para desarrolladores | SpA |

## Pendiente de decidir

- Precios finales y descuento anual.
- Qué queda gratis del termómetro de Consumo (hoy: solo el nivel).
- Si el plan Empresas tiene un tramo sin API, más barato, para pymes que solo quieren "Mi rubro".
- Términos de uso de cada fuente para redistribuir datos por la API.
