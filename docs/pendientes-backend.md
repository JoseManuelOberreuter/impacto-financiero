# Pendientes del backend

> Estado al 15-oct-2026. La app tiene el front y la API con datos de ejemplo; **todavía no hay ninguna fuente conectada en forma automática ni base de datos.** Solo ODEPA y las AFP tienen datos reales, como foto cargada a mano con un script.
> Fuentes: [fuentes-de-datos.md](fuentes-de-datos.md) y [investigacion-fuentes-ampliadas.md](investigacion-fuentes-ampliadas.md). Arquitectura: [arquitectura.md](arquitectura.md).

## Dónde estamos

| Pieza | Estado |
|---|---|
| API (FastAPI) con todos los endpoints | ✅ Hecha, con datos de ejemplo |
| Fotos reales de ODEPA y AFP (scripts) | ✅ Hechas, manuales |
| Base de datos (Supabase) | ❌ No existe |
| Worker de ingesta programado | ❌ No existe |
| Conectores automáticos | ❌ Ninguno |
| Cálculo real del estado de presión | ❌ Hoy el estado se escribe a mano |
| Recolector y clasificador de noticias | ❌ No existe |
| Despliegue (Railway, Vercel, tiendas) | ❌ No existe |

## Fase 0: cuentas y claves (las debe pedir el usuario)

- [ ] Token de la **API del Banco Central** (BDE).
- [ ] `apikey` de la **API de la CMF**.
- [ ] Token de la **API de la CNE** (`api.cne.cl/register`).
- [ ] Credenciales de la **API del Coordinador Eléctrico** (nuevo).
- [ ] Ticket de **Mercado Público** (con Clave Única; nuevo, opcional).
- [ ] Claves gratuitas de **FRED** y **EIA** (nuevo, opcional: primero revisar si la BDE ya tiene esas series).
- [ ] Clave de la API de un modelo de lenguaje para clasificar noticias. Recomendación: Claude Haiku, por costo.
- [ ] Cuentas de **Supabase**, **Railway** y **Expo/EAS**.
- [ ] Suscribirse a las alertas de **hechos esenciales** de la CMF.

## Fase 1: base del motor de datos

- [ ] **Esquema en Supabase** según [arquitectura.md](arquitectura.md):
  - `fuentes`, `corridas_ingesta`;
  - `series`, `observaciones` (con estado provisional o confirmado y fecha de publicación);
  - `precios_productos`;
  - `noticias`, `clasificaciones_noticias`;
  - `lecturas_termometro`.
- [ ] **Migraciones** versionadas en el repo del backend.
- [ ] **Worker** con tareas programadas (cron de Railway), separado del proceso de la API.
- [ ] **Estructura común de conector:** descargar → guardar crudo → normalizar → guardar. Con reintentos, registro en `corridas_ingesta` y alerta si una fuente falla varias veces.
- [ ] **Guardar los archivos crudos** en Supabase Storage para poder reprocesar.
- [ ] **La API lee de la base** en vez de los datos de ejemplo. Mantener un modo de ejemplo para desarrollo sin claves.
- [ ] **Variables de entorno** para todas las claves; nunca en el código.
- [ ] Desplegar API + worker en **Railway** y la web en **Vercel**.

## Fase 2: conectores, por prioridad

| Prioridad | Conector | Frecuencia | Nota |
|---|---|---|---|
| 1 | Banco Central (BDE) | Diaria + calendario de publicaciones | Armar primero el **catálogo de códigos de serie**: UF, dólar, TPM, IPC, IMACEC, cobre, desempleo, EEE, IPV y series internacionales |
| 1 | ODEPA | Semanal (viernes) | Convertir `snapshot_odepa.py` en conector |
| 1 | Superintendencia de Pensiones (valor cuota) | Diaria | Convertir `snapshot_afp.py`; reprocesar los datos provisionales cuando se confirmen |
| 1 | CMF (TMC, tasas, UTM) | Diaria / mensual | |
| 2 | CNE (bencina y gas) | Diaria | Filtrar estaciones sin actualizar (ver la regla en fuentes-de-datos.md) |
| 2 | ENAP / CNE (paridad MEPCO) | Semanal | Para el aviso "la bencina debería subir o bajar" |
| 2 | Seguro de cesantía | Mensual | Indicador adelantado de empleo |
| 2 | CMF hechos esenciales | Diaria | Desde las alertas por correo |
| 3 | Coordinador Eléctrico | Diaria | Costo marginal; termómetro de presión eléctrica |
| 3 | DIPRES, Aduanas, SII | Mensual | Contexto fiscal y externo |
| 3 | Registro de Empresas, ANAC | Mensual | Vienen en PDF: requieren extraer el texto |
| 4 | FRED, EIA, Banco Mundial | Diaria / anual | Solo lo que no esté en la BDE |
| 4 | Mercado Público | Diaria | Gasto público por región |

## Fase 3: cálculos

- [ ] **Estado de presión real:** comparar cada indicador con su historia de 5 años (percentiles 20/80), como dice [termometros.md](termometros.md). Hoy se escribe a mano.
- [ ] **Regla para combinar indicadores** en el estado de cada termómetro (está pendiente desde el diseño).
- [ ] **Índice de canasta automático,** con bencina y gas reales de la CNE ([indice-canasta.md](indice-canasta.md)).
- [ ] **"Lo que cambió esta semana"** a partir de las observaciones reales.
- [ ] **Datos propios** de [investigacion-fuentes-ampliadas.md](investigacion-fuentes-ampliadas.md), sección 4. Empezar por: horas de trabajo para la canasta, costo de llenar el estanque, aviso de la bencina, sueldo real y rentabilidad real de las AFP.
- [ ] **Tabla de ingreso mínimo** con fechas de vigencia, para los cálculos que lo usan.
- [ ] **Titular del día:** generarlo con IA a partir de los datos y noticias del día, con revisión de reglas: sin opiniones y sin consejos de inversión.
- [ ] **Calendario económico real,** tomado de los calendarios oficiales del Banco Central y del INE.

## Fase 4: noticias

Plan completo en [sentimiento-noticias.md](sentimiento-noticias.md).

- [ ] **Recolector de RSS** cada 30–60 minutos: La Tercera/Pulso, BioBio, Cooperativa, CIPER, Ex-Ante. Guardar solo titular, bajada, medio, fecha y enlace.
- [ ] **Limpieza:** eliminar duplicados, agrupar la misma noticia de varios medios y filtrar solo las económicas.
- [ ] **Clasificación con IA:** tema (termómetro), tono de −2 a +2 e incertidumbre. Validar con 300 titulares etiquetados a mano.
- [ ] **Cálculo del termómetro Ánimo:** tono neto, equilibrio entre medios, promedio de 7 días.
- [ ] **Empezar a guardar titulares cuanto antes:** se necesitan 2–3 meses de historia para saber qué es "lo habitual".
- [ ] **Endpoint de últimas noticias** para el front, con enlaces reales a cada medio.
- [ ] **Acuerdo o agregador con licencia** para El Mercurio y DF; Google News solo sirve en el prototipo.

### Ideas para el front de noticias

- **Cinta de titulares** (estilo teleprompter): una línea en el Inicio que rota los últimos titulares económicos, con el medio y un enlace. Debe ser discreta para no romper el minimalismo; por ejemplo, bajo el titular del día o sobre la barra de pestañas.
- **Feed de noticias** (ya existe en la pestaña Noticias): reemplazar los titulares de ejemplo por reales, con su tono y su tema.
- **Titular del día que se actualiza** cuando cambia algo importante, no solo una vez al día.

## Fase 5: calidad y operación

- [ ] **Tests de cada conector** con archivos de ejemplo guardados, para detectar cuando una fuente cambia su formato.
- [ ] **Monitoreo:** alerta si una fuente lleva más tiempo del esperado sin datos nuevos, según la tabla de desfases.
- [ ] **Página de estado interna:** última actualización de cada fuente.
- [ ] **Cliente TypeScript generado desde OpenAPI** para la app, en vez de tipos escritos a mano.
- [ ] **Revisar la recarga automática** de uvicorn en Windows, que a veces queda con código viejo.

## Para más adelante

- Usuarios (Supabase Auth), preferencias sincronizadas y personalización de termómetros.
- Notificaciones push: resumen del día y alertas ("la bencina sube el jueves").
- Calculadoras: dividendo, sueldo vs. inflación, inflación personal, depósito a plazo.
- Plan Pro: históricos largos, descargas y API para terceros.
- Licencia de datos de la Bolsa (nuam).
- Finanzas Abiertas (desde jul-2027): conectar las cuentas del usuario.
- "Termómetro de la calle": encuesta breve a usuarios o comercios.
- Google Trends como señal experimental de percepción.
- Comparación entre regiones (canasta por región, desempleo regional).
