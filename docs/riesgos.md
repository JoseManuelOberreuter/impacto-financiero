# Riesgos y bloqueantes

> Revisión al 16-oct-2026, ordenada según cuándo pega cada riesgo. Ninguno impide el MVP gratis; algunos afectan el lanzamiento en tiendas y el cobro. Lo legal es información general: confirmarlo con un abogado fintech antes de cobrar.
> Relacionado: [plan-pro.md](plan-pro.md), [planes.md](planes.md) y [pendientes-backend.md](pendientes-backend.md).

## Pueden bloquear un lanzamiento

| Bloqueante | Cuándo pega | Por qué | Qué hacer |
|---|---|---|---|
| **Apple exige empresa para apps financieras** | Al publicar en iPhone | Sus reglas piden que las apps de servicios financieros las publique una persona jurídica. Una app que solo informa podría pasar, pero es un riesgo real de rechazo | Crear la SpA y pedir el número D-U-N-S antes de iOS. Mientras tanto: Android y web |
| **Vercel gratis no permite uso comercial** | Al cobrar | El plan Hobby es solo para proyectos no comerciales | Pasar a Vercel Pro (US$20 al mes) o servir la web desde Railway |
| **Supabase gratis pausa proyectos inactivos** | Durante el MVP | Si nadie usa la base por un tiempo (alrededor de una semana), se pausa y la app deja de responder | El worker diario la mantiene activa; plan Pro (US$25 al mes) al lanzar |
| **Comisión de las tiendas** | Al cobrar | Google y Apple obligan a cobrar suscripciones digitales con su sistema y cobran 15 % | Incluirlo en el precio; en la web se puede cobrar con otro medio |

## Legales y regulatorios

| Riesgo | Detalle | Qué hacer |
|---|---|---|
| **Parecer asesoría de inversión** (Ley Fintech 21.521) | El plan Pro es el más expuesto. Mostrar y explicar datos está bien; "cámbiate al fondo A" o "compra dólares" es asesoría y exige registro en la CMF | Nunca recomendar, solo explicar. Revisar los textos automáticos y los generados con IA. Avisos legales visibles |
| **Revender datos por la API** (plan Empresas) | El Banco Central permite reproducir citando la fuente, pero revender datos crudos puede no estar permitido; lo mismo con la CMF y la CNE | Vender solo lo calculado por nosotros. Confirmarlo por escrito con cada institución antes de lanzar el plan Empresas |
| **Datos de la Bolsa (nuam)** | Sin licencia no hay IPSA diario ni acciones; el plan para inversionistas pierde valor | Cotizar la licencia temprano |
| **Prensa** | El Mercurio y el DF no tienen RSS abierto y tienen muro de pago. Titular y enlace suelen estar permitidos; copiar contenido no | Empezar con medios que publican RSS. Acuerdo o agregador con licencia para el resto |
| **Ley de datos personales 21.719** (vigente desde dic-2026) | Al guardar correos o cuentas: política de privacidad, seguridad, derecho a borrar la cuenta y aviso de filtraciones. Apple y Google también exigen poder borrar la cuenta | Guardar lo mínimo. Mi impacto guarda los datos en el teléfono, no en el servidor |
| **Ley del consumidor y suscripciones** | Precio claro, cancelación fácil y aviso antes de renovar | El cobro de las tiendas resuelve buena parte |

## Técnicos

| Riesgo | Ejemplo real | Qué hacer |
|---|---|---|
| **Las fuentes cambian o fallan** | La CNE trae meses corruptos; la CMF suspendió la TAB; el Banco Central entrega acentos mal codificados | Tests por conector, alertas si una fuente no se actualiza, y mostrar siempre la fecha del dato |
| **Claves que vencen** | El token del Banco Central dura un año | Recordatorio en el calendario y alerta del worker si la clave falla |
| **Precios viejos** | Solo 36 de 436 estaciones de Santiago tenían la bencina 95 actualizada en la semana | Filtro de frescura y "mediana de N estaciones" |
| **App nativa sin probar** | Todo se probó en la web; el vidrio de iOS y las pestañas nativas no se han visto en un teléfono | Probar pronto en Android con Expo |
| **Textos automáticos o de IA con errores** | Ya se corrigieron signos dobles ("perdió +1,1 %") | Tests de textos y reglas para el titular del día generado con IA |

## De negocio

- **Disposición a pagar:** mucha gente espera estos datos gratis (mindicador, bancos, prensa). Respuesta: [plan-pro.md](plan-pro.md).
- **Retención:** validar que la gente vuelva (hipótesis 1 del README).
- **Una sola persona:** documentar todo reduce la dependencia.

## Qué hacer y cuándo

1. **Ahora:** probar la app en Android y lanzar el MVP gratis en web y Android.
2. **Antes de cobrar:** SpA, consulta legal (asesoría de inversión y reventa de datos), cotizar la licencia de nuam y revisar los planes de Vercel y Supabase.
3. **Antes de iOS:** empresa y número D-U-N-S.
