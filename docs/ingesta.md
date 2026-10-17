# Ingesta de datos

Cómo llegan los datos de las fuentes a Supabase y de ahí a la API. Puesta en marcha el 17-oct-2026.

## Resumen

```
Fuentes (Banco Central, CNE, CMF, ODEPA, Superintendencia de Pensiones)
   │  python -m app.ingesta   (una vez al día, cron de Railway)
   ▼
Supabase
   ├─ fotos            lo último de cada fuente, en el formato que usa la API (1 fila por fuente)
   ├─ series           cada dato con historia (dólar, bencina 95 en la RM, TMC de consumo...)
   ├─ observaciones    los valores por fecha; se acumulan día a día
   └─ corridas_ingesta registro de cada descarga: cuándo, cuántas filas y si falló
   │
   ▼
API (FastAPI)  lee las fotos al arrancar y se recarga sola cuando cambian
```

## Conectores

Viven en `impacto-api/app/ingesta/`, uno por fuente. Cada uno tiene:

- `generar()`: descarga y arma la foto, el mismo JSON que antes generaban los scripts de `scripts/`.
- `series(foto)`: saca de la foto los valores con fecha para guardarlos en `series` y `observaciones`.

| Conector | Foto (`fotos.id`) | Fuente | Claves | Series que guarda |
|---|---|---|---|---|
| `bcch.py` | `bcch` | Banco Central | `BCCH_TOKEN` | `bcch.<id>`: 21 series, 6 años |
| `cne.py` | `cne` | CNE | `CNE_EMAIL`, `CNE_PASSWORD` | `cne.<combustible>.<región>` (mensual, 6 años) y `cne.estaciones.<combustible>.<región o pais>` (mediana de hoy, un punto por día) |
| `cmf.py` | `cmf` | CMF | `CMF_API_KEY` | `cmf.tmc.<tramo>`: 14 tramos, 6 años |
| `odepa.py` | `odepa` | ODEPA | No | `odepa.<producto>`: mediana semanal en la RM (descarga sola el CSV del año, ~50 MB) |
| `afp.py` | `afp` | Superintendencia de Pensiones | No | `sp.rentabilidad_<anio o mes>.<fondo>.<afp>`, provisional |

La historia diaria de las estaciones de la CNE y de la rentabilidad de las AFP no la guarda la fuente: se arma aquí, un punto por cada día que corre la ingesta. Por eso conviene correrla todos los días.

## Correr la ingesta

Desde `impacto-api/`:

```bash
.venv/Scripts/python -m app.ingesta                 # todas las fuentes
.venv/Scripts/python -m app.ingesta bcch cne        # solo algunas
.venv/Scripts/python -m app.ingesta --json          # además actualiza los JSON de respaldo en app/datos_ejemplo
```

- Repetirla no duplica nada: todo se guarda con upsert.
- Si una fuente falla, las demás siguen. La corrida queda con `estado = 'error'` y el mensaje, y el comando sale con código 1 para que el cron lo marque.
- Un conector suelto también se puede correr para generar solo el JSON, por ejemplo `python -m app.ingesta.cne app/datos_ejemplo/cne_snapshot.json`.

### En Railway (desde el 17-oct-2026)

Proyecto `impacto-financiero`, entorno `production`, con dos servicios que se construyen desde `JoseManuelOberreuter/impacto-financiero` (rama `main`, carpeta `/impacto-api`, su Dockerfile). Cada push a `main` que toque `impacto-api/` los vuelve a construir.

| Servicio | Qué hace | Configuración |
|---|---|---|
| `api` | La API, siempre encendida | `https://api-production-9df1b.up.railway.app`. Healthcheck en `/salud`; se reinicia si falla (hasta 5 veces) |
| `ingesta` | `python -m app.ingesta` una vez al día | Cron `0 13 * * *` (13:00 UTC = 10:00 en Chile con horario de verano, 09:00 en invierno). No se reinicia si falla: el error queda en `corridas_ingesta` y en los logs de Railway |

**Variables.** Las claves van una sola vez en las *Shared Variables* del entorno (Project Settings → Shared Variables → Raw Editor) y cada servicio las referencia con `${{shared.NOMBRE}}`:

- Compartidas: `SUPABASE_URL` (ya cargada), `SUPABASE_SERVICE_ROLE_KEY`, `BCCH_TOKEN`, `CNE_EMAIL`, `CNE_PASSWORD` y `CMF_API_KEY`.
- `api` usa `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY` y `CORS_ORIGINS` (por ahora `http://localhost:8081`; agregar la dirección de Vercel cuando se publique la web).
- `ingesta` usa las seis compartidas.

Sin las claves la API igual funciona, con los JSON de respaldo: `/salud` muestra `"archivo"` en cada fuente.

## Cómo la API usa las fotos

- `app/fotos.py` lee la foto de cada fuente desde Supabase. Si Supabase no responde o falta la foto, usa el JSON de respaldo de `app/datos_ejemplo/` (y lo registra en el log).
- Cada `REVISAR_FOTOS_MINUTOS` (15 por defecto; 0 lo apaga) la API revisa si alguna foto cambió y, si es así, vuelve a armar los datos sin reiniciar.
- `GET /salud` muestra la versión de cada foto en uso: la fecha en que se guardó, o `"archivo"` si viene del respaldo.
- `FOTOS_DESDE=archivos` hace que la API use solo los JSON (las pruebas lo usan así, sin conexión).

## Primera carga (17-oct-2026)

| Fuente | Series | Observaciones | Estado |
|---|---|---|---|
| Banco Central | 21 | 11.137 | Ok |
| CNE | 292 | 16.077 | Ok |
| CMF | 14 | 984 | Ok |
| ODEPA | 10 | 120 | Ok |
| Superintendencia de Pensiones | 0 | 0 | Error: ese sábado el sitio estuvo apagado de 10:00 a 17:00 por un corte de luz programado de ENEL (aviso en su portal), y `/apps/valoresCuotaFondo/` redirigía a la portada. La API siguió con el respaldo del 14-oct |

La primera corrida desde Railway ("Run now", 17-oct-2026 a las 21:06 UTC) trajo las 5 fuentes, incluida la Superintendencia de Pensiones (70 observaciones, dato al 15-oct), y la API publicada se recargó sola en la revisión siguiente.

## Pendiente

- Alerta cuando una fuente falla varios días seguidos (por ahora se ve en `corridas_ingesta`).
- Guardar los archivos crudos en Supabase Storage para poder reprocesar.
- Usar la historia guardada para calcular la presión de la bencina, los alimentos y las AFP, que hoy no tienen 5 años de datos diarios.
