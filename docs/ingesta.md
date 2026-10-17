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

En Railway va como un servicio cron con la misma imagen de la API y el comando `python -m app.ingesta`, una vez al día (por ejemplo a las 10:00 de Chile, después de que el Banco Central publica el dólar y la UF). Necesita las mismas variables de entorno: las claves de las fuentes y `SUPABASE_URL` y `SUPABASE_SERVICE_ROLE_KEY`.

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
| Superintendencia de Pensiones | 0 | 0 | Error: su sitio de descargas (`/apps/valoresCuotaFondo/`) redirige al portal y no responde. La API sigue con el respaldo del 14-oct. Reintentar en la próxima corrida |

## Pendiente

- Programar el cron en Railway (junto con el despliegue de la API).
- Alerta cuando una fuente falla varios días seguidos (por ahora se ve en `corridas_ingesta`).
- Guardar los archivos crudos en Supabase Storage para poder reprocesar.
- Usar la historia guardada para calcular la presión de la bencina, los alimentos y las AFP, que hoy no tienen 5 años de datos diarios.
