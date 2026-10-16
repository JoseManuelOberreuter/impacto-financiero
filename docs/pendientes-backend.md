# Pendientes del backend

> Estado al 15-oct-2026. La app tiene el front y la API con datos de ejemplo; **todavía no hay ninguna fuente conectada en forma automática ni base de datos.** ODEPA, las AFP y 16 series del Banco Central tienen datos reales, como fotos cargadas a mano con scripts.
> Fuentes: [fuentes-de-datos.md](fuentes-de-datos.md) y [investigacion-fuentes-ampliadas.md](investigacion-fuentes-ampliadas.md). Arquitectura: [arquitectura.md](arquitectura.md).

## Dónde estamos

| Pieza | Estado |
|---|---|
| API (FastAPI) con todos los endpoints | ✅ Hecha, con datos de ejemplo |
| Fotos reales de ODEPA, AFP y Banco Central (scripts) | ✅ Hechas, manuales |
| Base de datos (Supabase) | ❌ No existe |
| Worker de ingesta programado | ❌ No existe |
| Conectores automáticos | ❌ Ninguno |
| Cálculo real del estado de presión | 🟡 Hecho para los indicadores del Banco Central (`app/calculos/presion.py`); el resto sigue a mano |
| Recolector y clasificador de noticias | ❌ No existe |
| Despliegue (Railway, Vercel, tiendas) | ❌ No existe |

## Fase 0: cuentas y claves (las debe pedir el usuario)

- [x] Token de la **API del Banco Central** (BDE): API Key Token de "Mi Cuenta", vigencia de un año (se puede extender sin cambiarlo). Va en `BCCH_TOKEN`.
- [ ] `apikey` de la **API de la CMF**.
- [x] Cuenta de la **API de la CNE**: el token se pide en `POST https://api.cne.cl/api/login` con correo y clave (`CNE_EMAIL`, `CNE_PASSWORD`); las respuestas vienen comprimidas con gzip. Probada el 15-oct-2026: 1.829 estaciones.
- [ ] Credenciales de la **API del Coordinador Eléctrico** (nuevo).
- [ ] Ticket de **Mercado Público** (con Clave Única; nuevo, opcional).
- [ ] Claves gratuitas de **FRED** y **EIA**: probablemente innecesarias, porque la BDE ya trae el cobre, el WTI, el Brent, el diésel y la bencina de EE. UU. ([banco-central-series.md](banco-central-series.md)).
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
| 1 | Banco Central (BDE) | Diaria + calendario de publicaciones | Catálogo listo en [banco-central-series.md](banco-central-series.md). `scripts/snapshot_bcch.py` ya descarga 16 series a un JSON: **falta que guarde en Supabase** y correrlo a diario en el worker |
| 1 | ODEPA | Semanal (viernes) | Convertir `snapshot_odepa.py` en conector |
| 1 | Superintendencia de Pensiones (valor cuota) | Diaria | Convertir `snapshot_afp.py`; reprocesar los datos provisionales cuando se confirmen |
| 1 | CMF (TMC, tasas, UTM) | Diaria / mensual | |
| 2 | CNE (bencina y gas) | Diaria | `scripts/snapshot_cne.py` ya hace la foto (mediana de estaciones frescas e historia mensual). **Falta guardarla en Supabase y correrla a diario** para tener historia semanal |
| 2 | ENAP / CNE (paridad MEPCO) | Semanal | Para el aviso "la bencina debería subir o bajar" |
| 2 | Seguro de cesantía | Mensual | Indicador adelantado de empleo |
| 2 | CMF hechos esenciales | Diaria | Desde las alertas por correo |
| 3 | Coordinador Eléctrico | Diaria | Costo marginal; termómetro de presión eléctrica |
| 3 | DIPRES, Aduanas, SII | Mensual | Contexto fiscal y externo |
| 3 | Registro de Empresas, ANAC | Mensual | Vienen en PDF: requieren extraer el texto |
| 4 | FRED, EIA, Banco Mundial | Diaria / anual | Solo lo que no esté en la BDE |
| 4 | Mercado Público | Diaria | Gasto público por región |

## Fase 3: cálculos

- [x] **Estado de presión real** para los indicadores del Banco Central: percentiles 20/80 de 5 años ([termometros.md](termometros.md)), en `app/calculos/presion.py`. Falta aplicarlo a ODEPA, AFP y bencina cuando tengan historia guardada.
- [ ] **Regla para combinar indicadores** en el estado de cada termómetro (está pendiente desde el diseño).
- [ ] **Índice de canasta automático:** la bencina y el gas ya son reales, con el precio de hoy. Falta usar el precio de cada semana cuando se guarde a diario ([indice-canasta.md](indice-canasta.md)).
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

## Fase 4b: planes y capacidades

Plan completo en [planes.md](planes.md).

- [ ] Catálogo de capacidades y variable `MODO_PLANES` (empezar en `abierto`).
- [ ] Endpoint `GET /v1/yo/capacidades` y recorte de datos en la API según capacidades.
- [ ] Tablas `planes`, `capacidades`, `plan_capacidades` y `uso_capacidades`.
- [ ] Más adelante: `suscripciones`, RevenueCat, organizaciones y claves de API.

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
