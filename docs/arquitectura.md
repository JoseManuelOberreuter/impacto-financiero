# Arquitectura

> Estado: **decisiones principales tomadas (15-oct-2026).** Detalles por definir al implementar.

## Decisiones

| Tema | Decisión | Por qué |
|---|---|---|
| Plataformas | **iPhone, Android y web** | Llegar a la gente donde está; el celular y las notificaciones son clave para que vuelvan cada día |
| Front | **Expo (React Native) + Expo Router**, un solo código para las tres plataformas | Un equipo, un diseño, notificaciones push nativas. La web se exporta desde la misma app |
| Lenguaje del front | **TypeScript** | Estándar en React y React Native |
| Hosting de la web | **Vercel** | Ya está previsto; despliegue simple |
| Publicación en tiendas | **EAS Build / EAS Submit** (Expo) | Compila y publica sin pelear con Xcode ni Android Studio |
| Backend | **Python + FastAPI**, en un repositorio separado | Lo más cómodo para trabajar con datos (pandas, `bcchapi`, CSV pesados) |
| Hosting del backend | **Railway**, empaquetado en **Docker** | Sin administrar servidores. Cobra por uso real (plan Hobby ~USD 5/mes con USD 5 de consumo incluido; confirmar en la página oficial), lo que conviene a tareas cortas y esporádicas. Tiene tareas programadas (cron) por servicio. Render quedó como alternativa: precio fijo por servicio y su plan gratis se apaga tras 15 min sin visitas. Docker evita quedar amarrados: se puede mover a AWS u Oracle sin reescribir |
| Base de datos | **Supabase** (Postgres) | Ya disponible. Incluye Auth para cuando haya usuarios |
| Usuarios (etapa 2) | **Supabase Auth** | Inicio de sesión con correo o Google; el backend valida el token |

**Pendiente:** decidir si el worker parte en **GitHub Actions** (gratis, para el prototipo) o directo en Railway. Como Railway ya incluye tareas programadas a bajo costo, lo más simple es usar Railway para todo.

## Vista general

```
┌──────────────────────────────────────────┐
│ REPO 1: impacto-app  (Expo + Expo Router)│
│   ├─ iPhone   → App Store   (EAS Build)  │
│   ├─ Android  → Play Store  (EAS Build)  │
│   └─ Web      → Vercel                   │
└──────────────────┬───────────────────────┘
                   │ HTTPS · JSON · /v1/...
┌──────────────────▼───────────────────────┐
│ REPO 2: impacto-api  (Python, Docker)    │
│   ├─ API (FastAPI)  → lee datos listos   │
│   └─ Worker         → ingesta + cálculos │
│        Railway                           │
└──────────────────┬───────────────────────┘
                   │
         Supabase (Postgres + Auth + Storage)
                   ▲
                   │ descarga
   Banco Central · CMF · AFP · ODEPA · CNE · INE · SII · RSS de prensa
```

## Python en el backend y React en el front: ¿son compatibles?

Sí. Se comunican por HTTP y JSON, así que el lenguaje de cada lado no importa. Además:
- **FastAPI genera automáticamente la especificación OpenAPI** de la API.
- Con esa especificación se **genera un cliente TypeScript tipado** para la app (por ejemplo, con `openapi-typescript`). Si cambia la API, se regenera y TypeScript avisa en la app qué se rompió.
- Así se obtiene la ventaja de "un solo lenguaje" (tipos compartidos) sin renunciar a Python para los datos.

## Backend (`impacto-api`)

Un repositorio, una imagen Docker y **dos procesos**:

### Worker: ingesta y cálculos

- **Conectores, uno por fuente:** `bcch`, `cmf`, `afp`, `odepa`, `cne`, `sii`, `ine`, `rss`, `cmf_hechos`.
- **Programación según el ritmo de cada fuente** (ver la sección de desfases en [fuentes-de-datos.md](fuentes-de-datos.md)):
  - RSS: cada 30–60 min.
  - AFP, dólar, UF, CNE: diaria.
  - ODEPA: semanal (viernes).
  - IPC, IMACEC, UTM, desempleo: según el calendario oficial de publicación.
- **Flujo de cada corrida:** descargar → guardar crudo → normalizar → calcular → publicar.
- **Calculadoras:** estado de presión de cada termómetro, índice de canasta y sentimiento de noticias.
- **Todo se precalcula.** La API nunca calcula al momento de la consulta.
- **Reintentos y alertas:** si una fuente falla, se reintenta y se avisa. La app sigue mostrando el último dato con su fecha.

### API (FastAPI)

- **Versionada desde el inicio:** `/v1/...`
- **Endpoints iniciales (borrador):**
  - `GET /v1/termometros`: lista con estado, número clave, frase y fecha.
  - `GET /v1/termometros/{id}`: detalle con sus indicadores.
  - `GET /v1/indicadores/{id}/serie`: serie histórica.
  - `GET /v1/canasta`: índice de canasta y precios por producto.
  - `GET /v1/afp/{afp}/{fondo}`: rentabilidad del fondo.
  - `GET /v1/noticias/temas`: temas y tono del día.
  - `GET /v1/resumen`: resumen del día.
- **Caché:** los datos cambian a ritmos conocidos, así que cada respuesta indica cuánto tiempo es válida.
- **Solo lectura** en la etapa 1. Con usuarios se agregan los endpoints de preferencias.

### Estructura de carpetas (propuesta)

```
impacto-api/
├─ app/
│  ├─ api/            # rutas FastAPI (/v1/...)
│  ├─ conectores/     # un módulo por fuente
│  ├─ calculos/       # termómetros, canasta, sentimiento
│  ├─ modelos/        # esquemas (Pydantic) y tablas
│  ├─ db/             # conexión a Supabase/Postgres y migraciones
│  └─ worker/         # programación de tareas
├─ tests/
├─ Dockerfile
└─ pyproject.toml
```

## Base de datos (Supabase)

| Capa | Tablas (borrador) | Para qué |
|---|---|---|
| **Control** | `fuentes`, `corridas_ingesta` | Qué se trajo, cuándo y si falló |
| **Crudo** | Supabase Storage (archivos descargados) | Reprocesar si cambia un cálculo |
| **Normalizado** | `series`, `observaciones` (serie, período, valor, provisional/confirmado, fecha de publicación) | Todos los indicadores en un formato común |
| | `precios_productos` | ODEPA y CNE por producto, región y tipo de local |
| | `noticias`, `clasificaciones_noticias` | Titulares (sin texto completo) y su tema, tono e incertidumbre |
| **Publicado** | `lecturas_termometro`, `indice_canasta`, `resumen_dia` | Lo listo para mostrar |
| **Usuarios** (etapa 2) | `perfiles`, `preferencias` | Termómetros elegidos, AFP, notificaciones |

**Reglas:**
- **La app nunca lee la base de datos directamente:** todo pasa por la API.
- Solo el backend tiene las credenciales de la base.
- Las migraciones de la base se versionan en el repositorio del backend.

## App (`impacto-app`)

- **Expo + Expo Router**, en TypeScript.
- **Cliente de la API** generado desde OpenAPI.
- **Preferencias sin login** (etapa 1): almacenamiento local de la app y del navegador en la web.
- **Notificaciones push** (Expo Notifications) para el resumen del día y las alertas. Requieren registrar el dispositivo en el backend; definir si entra en la etapa 1 o en la 2.
- **Web:** exportada desde Expo y publicada en Vercel. Si más adelante se necesita SEO fuerte (páginas como "valor de la UF hoy"), se evalúa un sitio liviano en Next.js que use la misma API.

## Usuarios (etapa 2)

1. La app inicia sesión con **Supabase Auth** y obtiene un token.
2. Envía el token en cada llamada a la API.
3. El backend valida el token y sabe quién es el usuario y qué plan tiene.
4. La primera vez que el usuario inicia sesión, sus preferencias locales **se migran a su cuenta**.

## Requisitos de las tiendas

- **Aviso visible** de que no es asesoría financiera, y **política de privacidad**.
- **Eliminar la cuenta desde la app** (Apple lo exige cuando hay cuentas).
- **Pagos del plan Pro:** si se cobra dentro de la app, Apple y Google cobran comisión. Evaluar servicios como RevenueCat (etapa 2).

## Ambientes y despliegue

| Ambiente | App web | App móvil | Backend | Base de datos |
|---|---|---|---|---|
| Desarrollo | Local | Expo Go / simulador | Local con Docker | Proyecto Supabase de desarrollo |
| Producción | Vercel | App Store / Play Store | Railway | Proyecto Supabase de producción |

- Las claves (Banco Central, CMF, CNE, Supabase, LLM) van en **variables de entorno**, nunca en el código.
- Repositorios en GitHub (pendiente: acceso del usuario a GitHub).

## Pendiente

- [x] Railway (decidido el 15-oct-2026).
- [ ] Worker en GitHub Actions al inicio, o directo en Railway (recomendado: Railway).
- [ ] Notificaciones push en la etapa 1 o en la 2.
- [ ] Librería de tareas programadas para el worker (cron de la plataforma vs. un programador en Python).
- [ ] Modelo de datos definitivo.
