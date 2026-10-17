# Textos legales

Borrador del 17-oct-2026, **sin revisión de un abogado**. Revisarlo antes de abrir la app al público y, sobre todo, antes de cobrar (ver [riesgos.md](riesgos.md): Ley Fintech 21.521 y Ley 21.719).

## Qué hay

| Documento | Ruta | Para qué |
|---|---|---|
| Aviso legal y fuentes | `/legal/aviso` | El descargo: los datos son públicos (fuentes listadas), cómo calculamos, que pueden tener errores o atrasos, que no es asesoría financiera ni de inversión y que no respondemos por las decisiones que se tomen con ellos |
| Términos de uso | `/legal/terminos` | Reglas de uso. Incluyen el aviso legal como parte de los términos, así que aceptarlos es aceptar también el descargo |
| Política de privacidad | `/legal/privacidad` | Qué datos guardamos, para qué, dónde (Supabase, Railway, Vercel), cuánto tiempo y cómo ejercer los derechos de la Ley 21.719 |

Los textos están en `impacto-app/src/constants/legal.ts`; las páginas los muestran con `components/documento-legal.tsx`.

## Dónde aparecen

- **Pie de todas las páginas** (`components/pie-legal.tsx`, dentro de `Pagina`): una línea con las fuentes y "no es asesoría financiera ni de inversión", y los enlaces a los tres documentos.
- **Crear cuenta**: la casilla obligatoria enlaza a los términos (con el aviso legal) y a la privacidad.

## Prueba del consentimiento

Al crear la cuenta se guardan en los metadatos del usuario de Supabase Auth `terminos_version` (la `VERSION_LEGAL` vigente) y `terminos_aceptados_el` (fecha y hora). Si se cambia un texto de fondo, hay que subir `VERSION_LEGAL` y, si el cambio es importante, avisar a los usuarios.

## Pendiente

- Cuando haya dominio, cambiar el correo de contacto (`CORREO_CONTACTO`, hoy `impacto.financiero.app@gmail.com`) por uno del dominio.
- Revisión de un abogado.
- Cuando exista la SpA, cambiar `RESPONSABLE` por su razón social y RUT.
