# impacto-app

App de Impacto Financiero para **iPhone, Android y web**, hecha con Expo (React Native) y Expo Router. Ver [../docs/arquitectura.md](../docs/arquitectura.md).

> Estado: menú con 5 secciones (Inicio, Termómetros, Precios, Noticias y Herramientas) y páginas de detalle, con datos de `impacto-api` (parte reales, parte de ejemplo).

## Requisitos

- Node.js 20 o superior.
- `impacto-api` corriendo en `http://localhost:8000` (ver [../impacto-api/README.md](../impacto-api/README.md)).

## Correr en local

```bash
npm install
```

Versión web (se abre en `http://localhost:8081`):

```bash
npm run web
```

En el celular, con la app Expo Go y la misma red wifi que el PC:

```bash
npx expo start
```

En el celular o en el emulador de Android, `localhost` no apunta a tu PC. Crea un archivo `.env.local` con la IP local del PC:

```
EXPO_PUBLIC_API_URL=http://192.168.1.10:8000
```

En ese caso, la API también debe aceptar conexiones de la red: `uvicorn app.main:app --host 0.0.0.0 --port 8000`.

## Revisiones

```bash
npx tsc --noEmit
```

```bash
npx expo lint
```

## Estructura

```
src/
├─ app/                 # pantallas (Expo Router)
│  ├─ index.tsx         # Inicio
│  ├─ termometros/      # lista y detalle (/termometros/[id])
│  ├─ precios/          # lista y detalle de producto (/precios/[id])
│  ├─ noticias.tsx
│  └─ herramientas.tsx
├─ api/                 # cliente y tipos de la API (/v1/...)
├─ components/          # menú (app-tabs nativo y web), vidrio, página, gráficos, filas, termómetros
├─ constants/           # colores, presión, espaciado
├─ hooks/               # carga de datos (useApi), diseño responsivo, tema claro/oscuro
└─ utils/               # formato de fechas, pesos y porcentajes
```

## Navegación

- **iPhone y Android:** pestañas nativas abajo (`src/components/app-tabs.tsx`), con Liquid Glass en iOS 26.
- **Web:** barra de vidrio propia (`src/components/app-tabs.web.tsx`), arriba en escritorio y abajo en pantallas angostas.
- Secciones: Inicio, Termómetros, Precios, Noticias y Herramientas. El detalle de cada sección está en [../docs/termometros.md](../docs/termometros.md).

## Diseño

Sigue [../docs/termometros.md](../docs/termometros.md) y [../docs/investigacion-diseno.md](../docs/investigacion-diseno.md):

- Minimalista, con superficies de **vidrio** (Liquid Glass nativo en iOS 26; desenfoque en web) sobre un fondo de luces difusas.
- El **Inicio** sigue la propuesta G de Figma: fecha arriba a la derecha, titular del día, canasta con mini gráfico, "Lo que cambió esta semana" con flechas y mini gráficos, y termómetros en tarjetas. El detalle vive en las otras secciones.
- **Fondo "piedra cálida"** en claro y oscuro, el mismo en todas las pestañas. La paleta activa se elige en `src/constants/theme.ts` (también están verde azulado y piedra fresca).
- Nivel de **presión** siempre escrito (no solo con color), con su tendencia.
- Gráficos con la **banda de lo normal** en el detalle de cada indicador.
- Íconos de [Lucide](https://lucide.dev) en web y en la app; SF Symbols y Material Symbols en las pestañas nativas. **No se usan emojis.**
- La personalización de termómetros queda para cuando haya base de datos donde guardarla.
- Aviso de datos de ejemplo y de que no es asesoría financiera.
- Modo claro y oscuro, pensado primero para el celular. Se elige en **Herramientas → Ajustes → Apariencia** (Automático, Claro u Oscuro); la elección se guarda en el dispositivo (`src/hooks/use-preferencia-tema.tsx`).

## Rutas tipadas

Expo genera `.expo/types/router.d.ts` con las rutas válidas. Si `npx tsc --noEmit` reclama por rutas que sí existen, borra ese archivo y vuelve a levantar `npm run web` para que se regenere.
