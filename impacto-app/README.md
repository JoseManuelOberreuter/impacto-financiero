# impacto-app

App de Impacto Financiero para **iPhone, Android y web**, hecha con Expo (React Native) y Expo Router. Ver [../docs/arquitectura.md](../docs/arquitectura.md).

> Estado: solo existe el **home**, con **datos de ejemplo** entregados por `impacto-api`.

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
├─ app/             # pantallas (Expo Router): por ahora solo index.tsx = home
├─ api/             # cliente y tipos de la API (/v1/home)
├─ components/      # tarjeta de termómetro, resumen del día, Mi AFP, personalizar
├─ constants/       # colores (incluye los de "presión"), espaciado
├─ hooks/           # carga de datos, tema claro/oscuro
└─ utils/           # formato de fechas
```

## Qué hace el home

Sigue [../docs/termometros.md](../docs/termometros.md) y [../docs/investigacion-diseno.md](../docs/investigacion-diseno.md):

- Resumen del día en dos líneas.
- Hasta 4 termómetros: estado de **presión** escrito (no solo color), tendencia, un número clave, una frase, fecha del dato, próxima actualización y fuente.
- **Personalizar**: elegir y ordenar hasta 4 termómetros. Todavía **no se guarda** al recargar.
- Invitación a configurar **Mi AFP** (próximamente).
- Aviso de datos de ejemplo y aviso de que no es asesoría financiera.
- Modo claro y oscuro, pensado primero para el celular.
