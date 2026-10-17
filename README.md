# Impacto Financiero

> Estado: **idea en validación.** Hay un primer prototipo del home con datos de ejemplo; todavía sin fuentes conectadas ni usuarios.

## Idea

Plataforma 100% chilena que reúne en un solo lugar los datos de la economía (Banco Central, CMF, AFP, SII, Bolsa y prensa) y explica, en lenguaje simple, **qué pasó y cómo le afecta a cada persona**.

## Problema

- La información económica de Chile está repartida en decenas de sitios, formatos y planillas.
- Los datos oficiales son técnicos: la mayoría no sabe qué significa que suba la TPM o el IPC para su bolsillo.
- Nadie cruza las fuentes: dólar, fondos de pensiones, hechos esenciales y noticias se leen por separado.
- Seguir el mercado a diario exige tiempo y conocimientos que personas y pymes no tienen.

## Público por etapas

Una sola base de datos y distintas capas de producto, que se lanzan en orden:

| Etapa | Público | Modelo | Qué recibe |
|---|---|---|---|
| 1 | Personas comunes | Gratis | Resumen diario, su AFP y calculadoras de impacto |
| 2 | Inversionistas | Pago (Pro) | Históricos, alertas, hechos esenciales filtrados, descargas |
| 3 | Pymes y contadores | Pago | Reajuste por IPC, impacto del dólar en costos, calendario tributario |

**Foco actual: etapa 1.** Los planes (Gratis, Pro y Empresas) y cómo se activan están en [docs/planes.md](docs/planes.md).

## Fuentes de datos

| Fuente | Datos | Acceso | Etapa |
|---|---|---|---|
| Banco Central (BDE) | UF, dólar observado, IPC, TPM, IMACEC, tasas | API oficial con token | 1 |
| CMF | Indicadores, tasas, hechos esenciales | API con clave y sitio público | 1 |
| Superintendencia de Pensiones | Valor cuota diario por AFP y fondo (A–E), rentabilidad, comisiones | Descargas públicas | 1 |
| ODEPA | Precios al consumidor de alimentos (pan, leche, huevos, aceite, carnes) | Datos abiertos, CSV semanal | 1 |
| CNE | Precios de bencina y gas licuado por comuna | API con token | 1 |
| Panel de Expertos del Transporte Público | Tarifa de Metro y buses RED | Resolución en el Diario Oficial | 1 |
| Prensa (El Mercurio, La Tercera, DF, otros) | Titulares, tema y tono | RSS: solo titular, enlace y medio | 1 |
| INE | Empleo, desglose del IPC, remuneraciones | Descargas públicas | 2 |
| SII y DIPRES | UTM, UTA, tramos de impuesto, recaudación | Páginas y archivos públicos | 2–3 |
| Bolsa (nuam) | IPSA, precios y volúmenes | Sin API pública; datos licenciados | 1 (solo cierre) / 2 |

Detalle de cada API, cómo se accede y qué hacer con las fuentes sin API: [docs/fuentes-de-datos.md](docs/fuentes-de-datos.md).

## Etapa 1: versión gratis (MVP)

| Sección | Descripción |
|---|---|
| Onboarding | Explica cómo funciona la app y deja al usuario elegir y ordenar sus termómetros (hasta 4) y, opcionalmente, su AFP |
| Home | Resumen del día en 2 líneas y los termómetros elegidos: estado de presión, un número, una frase y la fecha del dato. Detalle en [docs/termometros.md](docs/termometros.md) |
| Economía cotidiana | Precio semanal de pan, leche, huevos, aceite, carne, pollo, bencina, gas y pasaje, con su variación y un índice propio de canasta |
| Mi AFP | El usuario elige AFP y fondo, sin login; ve rentabilidad del día, mes y año, y la compara con otros fondos y AFP |
| Calculadoras | Dividendo o crédito en UF, sueldo vs. inflación, depósito a plazo vs. inflación |
| Qué se está hablando | Titulares agrupados por tema y tono, con enlace a la fuente; hechos esenciales explicados |

### Indicadores propios

Además de mostrar datos oficiales, calculamos indicadores propios a partir de ellos. Siempre se presentan como **referencia propia, no oficial**, con su metodología publicada.

| Indicador | Descripción | Metodología |
|---|---|---|
| Índice Impacto de la Canasta | Costo semanal de una canasta típica (pan, leche, huevos, aceite, carnes, bencina, gas y pasajes) y su variación | [docs/indice-canasta.md](docs/indice-canasta.md) |

**Fuera de la etapa 1:**
- Cuentas de usuario (salvo correo para el resumen diario).
- Datos de bancos y datos personales del SII.
- Precios de la Bolsa en tiempo real.
- Recomendaciones de inversión o de cambio de fondo.

## Código

| Directorio | Qué es | Estado |
|---|---|---|
| [impacto-app/](impacto-app/) | App para iPhone, Android y web (Expo + Expo Router) | 5 secciones con menú y páginas de detalle |
| [impacto-api/](impacto-api/) | Backend: API (FastAPI) y, más adelante, el worker | Endpoints de todas las secciones; ODEPA y AFP con fotos reales |

Cada directorio tiene su README con las instrucciones para correrlo en local.

**Iniciar todo de una vez (Windows):** desde la raíz del proyecto, ejecuta:

```
.\iniciar.cmd
```

- Abre la API en una ventana nueva (`http://localhost:8000`) y deja la app web en la terminal actual (`http://localhost:8081`).
- La primera vez instala lo que falte: el entorno de Python y las dependencias de Node.
- Para detener todo, presiona `Ctrl + C` en cada ventana.

## Documentación

| Documento | Contenido |
|---|---|
| [docs/catalogo-de-datos.md](docs/catalogo-de-datos.md) | **De dónde sale cada dato** que muestra la app: fuente, serie o archivo, script y fecha de la última descarga |
| [docs/impacto-financiero.md](docs/impacto-financiero.md) | Metodología del Impacto Financiero: la inflación en pesos para un hogar típico, con la Encuesta de Presupuestos Familiares del INE |
| [docs/fuentes-de-datos.md](docs/fuentes-de-datos.md) | Cómo se accede a cada fuente, qué hacer con las que no tienen API, y frecuencia y desfase de cada dato |
| [docs/termometros.md](docs/termometros.md) | Termómetros, onboarding, estado de presión y estructura del home |
| [docs/indice-canasta.md](docs/indice-canasta.md) | Metodología del Índice Impacto de la Canasta |
| [docs/sentimiento-noticias.md](docs/sentimiento-noticias.md) | Cómo convertir las noticias diarias en el termómetro Ánimo |
| [docs/investigacion-diseno.md](docs/investigacion-diseno.md) | Investigación internacional y chilena de apps económicas y termómetros: fortalezas, debilidades y qué aplicamos |
| [docs/arquitectura.md](docs/arquitectura.md) | Stack, repositorios, backend, base de datos, app y despliegue |
| [docs/investigacion-fuentes-ampliadas.md](docs/investigacion-fuentes-ampliadas.md) | Más fuentes chilenas e internacionales, datos propios que salen de cruzarlas y tabla maestra de fuentes |
| [docs/banco-central-series.md](docs/banco-central-series.md) | Códigos de las series del Banco Central por termómetro, cómo usar su API y datos propios que salen de cruzarlas |
| [docs/planes.md](docs/planes.md) | Planes Gratis, Pro y Empresas, capacidades por plan, modos de activación y tablas de la base |
| [docs/plan-pro.md](docs/plan-pro.md) | Qué vende el plan Pro (Mi impacto, lo que viene, cruces y alertas), qué queda gratis y cómo validarlo |
| [docs/riesgos.md](docs/riesgos.md) | Bloqueantes y riesgos legales, técnicos y de negocio, y cuándo atenderlos |
| [docs/pendientes-backend.md](docs/pendientes-backend.md) | Lista de pendientes del backend: claves, base de datos, conectores, cálculos y noticias |

## Arquitectura

| Capa | Tecnología | Hosting |
|---|---|---|
| App (iPhone, Android y web) | Expo (React Native) + Expo Router, TypeScript | App Store, Play Store y Vercel (web) |
| Backend: API + worker de ingesta y cálculos | Python + FastAPI, Docker | Railway |
| Base de datos y usuarios | Supabase (Postgres, Auth, Storage) | Supabase |

```
App (Expo: iPhone · Android · Web)
        │  /v1/...
        ▼
API (FastAPI) ◄── lee datos precalculados
        │
     Supabase ◄── Worker: ingesta → normalización → termómetros, canasta, sentimiento
                        ▲
        Banco Central · CMF · AFP · ODEPA · CNE · INE · SII · prensa
```

Detalle completo en [docs/arquitectura.md](docs/arquitectura.md).

## Límites legales

- **CMF / Ley Fintech (21.521):** sin custodia de fondos, sin intermediación y sin recomendaciones personalizadas de inversión.
- **Finanzas Abiertas:** la conexión con bancos queda para después de su entrada en vigencia, postergada a julio de 2027 (NCG 569).
- **Derechos de autor:** no se copian ni republican artículos de prensa; solo titular, enlace y clasificación propia.
- **Datos personales:** cumplir con la Ley 21.719 si se guardan datos de usuarios (vigencia legal: 1-dic-2026; hay un proyecto para postergarla a 2027). En la etapa 1, los datos sensibles se quedan en el navegador del usuario.
- **Fuentes oficiales:** citar a cada institución como dueña de sus datos, según sus términos de uso.

## Competencia y referencias

- **Sitios oficiales** (Banco Central, CMF, SP, SII): datos completos, pero dispersos y técnicos.
- **Prensa económica** (DF, El Mercurio Inversiones): análisis, en general con muro de pago.
- **Sitios de indicadores** (por ejemplo, mindicador.cl): valores sueltos, sin explicación ni cruces.
- **Comparadores de AFP**: centrados en un solo tema.

## Hipótesis a validar

1. Las personas quieren entender cómo la economía afecta su bolsillo y volverían a diario o semanalmente.
2. "Mi AFP" es un gancho suficiente para atraer y retener usuarios.
3. Explicar los datos en lenguaje simple aporta más que mostrarlos.
4. Una parte de los usuarios gratuitos pagaría por un plan Pro (precio por definir).

## Riesgos

- Cambios en las fuentes (APIs, formatos o rutas de descarga).
- Restricciones legales en el uso de noticias y datos de la Bolsa.
- Errores en datos o explicaciones generadas con IA.
- Que el producto se perciba como asesoría financiera.
- Monetizar un público que espera todo gratis.

## Próximos pasos

1. Crear las cuentas de Railway, Supabase, Vercel y Expo, y pedir las claves de API (Banco Central, CMF, CNE).
2. Hacer una prueba de datos: conectar Banco Central, CMF y SP, y guardar sus series.
3. Probar la lectura de titulares por RSS y su clasificación por tema y tono.
4. Diseñar las pantallas de la etapa 1.
5. Mostrar un prototipo a 10 personas y medir si vuelven.

## Notas

- Este proyecto informa y explica; no es asesoría financiera, tributaria ni de inversión.
- Cualquier cifra o regla debe verificarse en fuentes oficiales (Banco Central, CMF, SP, SII).
