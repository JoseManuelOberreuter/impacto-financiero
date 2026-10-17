# Cuentas de usuario

> Diseño al 16-oct-2026. Relacionado: [planes.md](planes.md) (capacidades y suscripciones), [riesgos.md](riesgos.md) (Ley 21.719) y [plan-pro.md](plan-pro.md).

## Decisiones

| Tema | Decisión |
|---|---|
| ¿Cuenta obligatoria? | **No. Totalmente opcional.** La app funciona completa sin cuenta |
| ¿Para qué sirve la cuenta? | Sincronizar entre dispositivos (anclados, apariencia y, si el usuario quiere, Mi impacto), las alertas y el plan Pro |
| Forma de entrar | **Correo y contraseña.** Google y Apple, después (si la app de iPhone ofrece Google, Apple obliga a ofrecer también "Entrar con Apple") |
| Proveedor | **Supabase Auth**: contraseñas cifradas, tokens, verificación y recuperación. Nunca guardamos contraseñas nosotros |
| Correos | Por ahora, el correo de prueba de Supabase (pocos envíos por hora; solo para desarrollo). Al salir a producción: dominio propio y **Resend** como servidor de correo |
| Datos personales | Lo mínimo: correo y nombre opcional. Sin RUT, teléfono ni datos bancarios |

**Por qué opcional:** más gente prueba la app sin fricción, y quien no crea cuenta no deja datos personales en el servidor (menos riesgo y menos obligaciones legales). Quien no tiene cuenta no ve mensajes de planes: la app le ofrece la cuenta solo cuando toca algo que la necesita.

## Pantallas

Todas viven en `/cuenta/...`, fuera de las 5 pestañas: se abren encima del menú (un Stack en `src/app/_layout.tsx`; las pestañas van en `src/app/(tabs)/`) y "Volver" regresa a donde estabas. En web muestran el mismo menú de las secciones (`components/menu-web.tsx`, con `src/app/cuenta/_layout.web.tsx`); en la app nativa se abren encima de la barra de pestañas, como es habitual en iPhone y Android. Se entra solo desde la burbuja de cuenta, arriba a la derecha junto a la bandera: sin sesión muestra un ícono de persona y con sesión la inicial del nombre o del correo.

| Pantalla | Ruta | Qué hace |
|---|---|---|
| Mi cuenta | `/cuenta` | Siempre: Apariencia (automático, claro u oscuro, guardada en el dispositivo). Sin sesión: qué se gana con una cuenta, "Crear cuenta" e "Iniciar sesión". Con sesión: nombre, correo, plan, cambiar contraseña, cerrar sesión (aquí o en todos los dispositivos) y, abajo y en gris, un enlace discreto a "Borrar cuenta" |
| Crear cuenta | `/cuenta/crear` | Nombre (opcional), correo, contraseña con medidor en vivo, repetir contraseña y aceptar los términos y la política de privacidad |
| Verifica tu correo | `/cuenta/verificar` | "Te enviamos un enlace". Botón para reenviar, con espera de 60 segundos entre envíos |
| Iniciar sesión | `/cuenta/ingresar` | Correo y contraseña, "Mostrar contraseña" y "¿Olvidaste tu contraseña?". El error no dice si el correo existe |
| Recuperar contraseña | `/cuenta/recuperar` | Pide el correo y siempre responde "Si existe una cuenta con ese correo, te enviamos un enlace" |
| Nueva contraseña | `/cuenta/nueva-clave` | Se abre desde el enlace del correo. Mismo medidor y reglas |
| Borrar cuenta | `/cuenta/borrar` | Difícil a propósito, para que nadie la borre sin querer: lista de lo que se pierde, casilla "Entiendo que no se puede deshacer", contraseña actual (se vuelve a verificar), escribir BORRAR y una espera de 5 segundos antes de que se habilite el botón. Siempre muestra "No, mantener mi cuenta". Apple y Google exigen que se pueda borrar desde la app, así que no puede ser más difícil que esto (sin correos ni llamadas) |

## Reglas de la contraseña

- Mínimo **10 caracteres**, con **minúsculas, mayúsculas y números**.
- La app las muestra como lista que se va marcando mientras se escribe, y no deja enviar hasta cumplirlas.
- Supabase las valida también del lado del servidor (configuración abajo): la app no es la única barrera.
- Supabase limita los intentos de inicio de sesión y de envío de correos (fuerza bruta y abuso).
- Pendiente para producción: rechazar contraseñas filtradas (opción de Supabase, puede requerir plan pagado) y CAPTCHA invisible en el registro (Cloudflare Turnstile).

## Por dentro

**App** (`impacto-app`):
- `src/api/supabase.ts`: cliente de Supabase con la sesión guardada en el dispositivo (AsyncStorage).
- `src/hooks/use-sesion.tsx`: sesión actual, crear cuenta, iniciar y cerrar sesión, recuperar y cambiar contraseña.
- Variables en `impacto-app/.env.local` (no se sube a git): `EXPO_PUBLIC_SUPABASE_URL` y `EXPO_PUBLIC_SUPABASE_ANON_KEY`. La clave pública (anon) no da acceso a nada: todas las tablas tienen RLS.
- Al iniciar sesión, los datos anclados del dispositivo se suben a la cuenta (se unen con los que ya tenía) y desde ahí se sincronizan.

**API** (`impacto-api`):
- `app/sesion.py`: valida el token de Supabase que manda la app (`Authorization: Bearer ...`) preguntándole a Supabase Auth quién es el usuario.
- `GET /v1/yo`: perfil, correo, si está verificado y plan.
- `GET /v1/yo/preferencias` y `PUT /v1/yo/preferencias`: anclados, apariencia y Mi impacto.
- `DELETE /v1/yo`: borra la cuenta y todos sus datos (perfil, preferencias, suscripciones), como exigen Apple, Google y la Ley 21.719.
- La API usa la clave secreta (`SUPABASE_SERVICE_ROLE_KEY`) solo en el servidor; nunca va a la app.

**Base de datos** (Supabase, migraciones en `impacto-api/db/migraciones/`):
- `perfiles` y `preferencias`: una fila por usuario, creadas automáticamente al registrarse (trigger `al_crear_usuario`). Cada usuario solo puede ver y editar lo suyo (RLS).
- `suscripciones`: sin fila = plan gratis.
- Al borrar el usuario en Supabase Auth se borra todo lo suyo (`on delete cascade`).

## Configuración de Supabase (en el panel, una vez)

Panel de Supabase → proyecto **impacto-financiero**:

1. **Authentication → Sign In / Providers → Email:** activado, con **Confirm email** activado.
2. **Authentication → Policies (o Password Security):** largo mínimo **10** y requisito **"Lowercase, uppercase letters and digits"**.
3. **Authentication → URL Configuration:**
   - Site URL: `http://localhost:8081` (en producción, el dominio de la web).
   - Redirect URLs: `http://localhost:8081/**` e `impactofinanciero://**` (la app nativa).
4. **Authentication → Emails → Templates:** textos en español (ver abajo). Opcional mientras se desarrolla.

## Correos (plantillas en español)

| Correo | Asunto | Texto del botón |
|---|---|---|
| Confirmar cuenta | Confirma tu cuenta de Impacto Financiero | Confirmar mi correo |
| Restablecer contraseña | Restablece tu contraseña | Elegir una nueva contraseña |
| Cambio de correo | Confirma tu nuevo correo | Confirmar el cambio |

## Pendiente

- Probar el flujo completo con un correo real (crear, verificar, entrar, recuperar, borrar).
- Producción: dominio, Resend, plantillas con la marca, contraseñas filtradas y CAPTCHA.
- Google y Apple.
- Alertas y plan Pro sobre la cuenta.
