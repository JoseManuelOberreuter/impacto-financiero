// Textos legales de la app: aviso legal y fuentes, términos de uso y política de privacidad.
// Al cambiar un texto de fondo, sube VERSION_LEGAL: la cuenta guarda qué versión aceptó cada usuario.
// Borrador sin revisión de un abogado (docs/legal.md).

export const VERSION_LEGAL = '2026-10-17';
export const FECHA_LEGAL = '17 de octubre de 2026';

/** Correo para consultas y para ejercer los derechos sobre los datos personales. */
export const CORREO_CONTACTO = 'impacto.financiero.app@gmail.com';
export const RESPONSABLE = 'Impacto Financiero, proyecto de una persona natural con domicilio en Chile';

export type SeccionLegal = { titulo: string; parrafos: string[] };
export type DocumentoLegal = { titulo: string; bajada: string; secciones: SeccionLegal[] };

export const FUENTES = [
  'Banco Central de Chile: dólar, euro, UF, UTM, tasa de política monetaria, IPC, IMACEC, desempleo, tasas de crédito, cobre, petróleo y expectativas.',
  'Instituto Nacional de Estadísticas (INE): Encuesta de Presupuestos Familiares, que dice cuánto gasta un hogar típico en cada cosa.',
  'Comisión Nacional de Energía (CNE): precios de la bencina, el diésel, la parafina y el gas licuado.',
  'Comisión para el Mercado Financiero (CMF): tasa máxima convencional de los créditos.',
  'Oficina de Estudios y Políticas Agrarias (ODEPA): precios al consumidor de alimentos.',
  'Superintendencia de Pensiones: valor cuota y rentabilidad de los fondos de las AFP.',
  'Panel de Expertos del Transporte Público: tarifa del Metro.',
];

export const AVISO_LEGAL: DocumentoLegal = {
  titulo: 'Aviso legal y fuentes',
  bajada: 'De dónde salen los datos, cómo calculamos y por qué nada de esto es una recomendación.',
  secciones: [
    {
      titulo: 'Qué es Impacto Financiero',
      parrafos: [
        'Una app informativa que reúne datos públicos de la economía chilena y explica, con palabras simples, cómo podrían afectar el bolsillo de un hogar. Es gratuita y no está afiliada a ninguna de las instituciones que publican los datos.',
      ],
    },
    {
      titulo: 'De dónde salen los datos',
      parrafos: [
        'Todos los datos son públicos y los publica cada institución en su sitio o en su servicio de datos abiertos:',
        ...FUENTES.map((fuente) => `• ${fuente}`),
        'Los descargamos de forma automática una vez al día. Pueden tener atrasos, errores de la fuente, revisiones posteriores o valores provisionales (por ejemplo, el valor cuota de las AFP se confirma días después). Si un dato no coincide con la fuente oficial, vale la fuente oficial.',
      ],
    },
    {
      titulo: 'Cómo calculamos',
      parrafos: [
        'Cuándo un dato está "alto" o "bajo": lo comparamos con lo que fue normal en los últimos 5 años (entre el percentil 20 y el 80).',
        'Impacto Financiero: estima cuánto cambia el gasto mensual de un hogar típico a partir de la Encuesta de Presupuestos Familiares del INE y de la variación de los precios.',
        'Canasta y precios: medianas de los precios de ODEPA y de las estaciones de servicio de la CNE, que pueden diferir de lo que pagas en tu barrio.',
        'Mi impacto: usa los montos que tú escribes y los calcula en tu dispositivo.',
        'Son estimaciones y simplificaciones: no consideran tu situación particular, y la metodología puede cambiar.',
      ],
    },
    {
      titulo: 'No es asesoría financiera',
      parrafos: [
        'Nada de lo que muestra la app es asesoría financiera, de inversión, tributaria, previsional ni legal, ni una recomendación de comprar, vender, ahorrar, endeudarse o cambiarse de fondo o de AFP. No somos asesores de inversión registrados en la CMF.',
        'Antes de tomar una decisión con tu dinero, revisa las fuentes oficiales y consulta con un profesional.',
      ],
    },
    {
      titulo: 'Responsabilidad',
      parrafos: [
        'La información se entrega "tal como está", sin garantía de que sea exacta, completa u oportuna. Las decisiones que tomes con ella son tuyas: en la medida que lo permite la ley, Impacto Financiero no se hace responsable de pérdidas, perjuicios ni decisiones tomadas a partir de los datos, cálculos o textos de la app.',
      ],
    },
  ],
};

export const TERMINOS: DocumentoLegal = {
  titulo: 'Términos de uso',
  bajada: `Versión del ${FECHA_LEGAL}.`,
  secciones: [
    {
      titulo: '1. Aceptación',
      parrafos: [
        'Al usar Impacto Financiero aceptas estos términos. Si creas una cuenta, los aceptas de forma expresa y guardamos la versión y la fecha en que lo hiciste.',
      ],
    },
    {
      titulo: '2. El servicio',
      parrafos: [
        `${RESPONSABLE} ofrece una app con datos públicos de la economía chilena y cálculos propios. Hoy es gratuita. Si en el futuro hay planes de pago, se informarán antes y nadie pagará sin aceptarlo.`,
      ],
    },
    {
      titulo: '3. Información, no asesoría',
      parrafos: [
        'Los datos y cálculos son referenciales y no son asesoría financiera ni de inversión. El Aviso legal y fuentes forma parte de estos términos: ahí se explica de dónde salen los datos, cómo calculamos y los límites de nuestra responsabilidad.',
      ],
    },
    {
      titulo: '4. Tu cuenta',
      parrafos: [
        'La cuenta es opcional. Para crearla debes ser mayor de 18 años o contar con autorización de tu padre, madre o tutor. Eres responsable de cuidar tu contraseña y de lo que se haga con tu cuenta. Puedes borrarla cuando quieras desde Mi cuenta.',
      ],
    },
    {
      titulo: '5. Uso aceptable',
      parrafos: [
        'No está permitido: intentar vulnerar la seguridad de la app o acceder a cuentas ajenas; descargar los datos de forma masiva o automatizada sin permiso; usar la app para fines ilícitos; ni presentar nuestros cálculos o textos como propios.',
      ],
    },
    {
      titulo: '6. Propiedad intelectual',
      parrafos: [
        'El diseño, los textos, los cálculos y el código de la app son de Impacto Financiero. Los datos de las fuentes pertenecen a cada institución y se usan según sus condiciones de publicación.',
      ],
    },
    {
      titulo: '7. Limitación de responsabilidad',
      parrafos: [
        'En la medida que lo permite la ley, no respondemos por daños derivados del uso de la app o de la imposibilidad de usarla, ni por decisiones tomadas a partir de su información. Nada de esto limita los derechos irrenunciables que te da la Ley 19.496 de protección de los derechos de los consumidores.',
      ],
    },
    {
      titulo: '8. Disponibilidad',
      parrafos: [
        'Hacemos lo posible para que la app funcione siempre, pero puede tener fallas, interrupciones o datos atrasados si una fuente no responde.',
      ],
    },
    {
      titulo: '9. Suspensión y término',
      parrafos: [
        'Podemos suspender o cerrar cuentas que no cumplan estos términos. Tú puedes dejar de usar la app y borrar tu cuenta en cualquier momento.',
      ],
    },
    {
      titulo: '10. Cambios',
      parrafos: [
        'Si cambiamos estos términos, publicaremos la nueva versión con su fecha y, si el cambio es importante, te lo avisaremos en la app o por correo.',
      ],
    },
    {
      titulo: '11. Ley aplicable',
      parrafos: [
        'Estos términos se rigen por las leyes de Chile. Cualquier conflicto se verá ante los tribunales de Santiago, sin perjuicio de los derechos que te da la ley como consumidor.',
      ],
    },
    {
      titulo: '12. Contacto',
      parrafos: [`Escríbenos a ${CORREO_CONTACTO}.`],
    },
  ],
};

export const PRIVACIDAD: DocumentoLegal = {
  titulo: 'Política de privacidad',
  bajada: `Versión del ${FECHA_LEGAL}. Cumple con la Ley 19.628 y con la Ley 21.719 de protección de datos personales.`,
  secciones: [
    {
      titulo: '1. Quién es el responsable',
      parrafos: [`${RESPONSABLE}. Contacto: ${CORREO_CONTACTO}.`],
    },
    {
      titulo: '2. Qué datos guardamos',
      parrafos: [
        'Sin cuenta: ningún dato personal en nuestros servidores. Tus datos anclados y la apariencia se guardan solo en tu dispositivo.',
        'Con cuenta: tu correo, tu nombre (si lo escribes), tus datos anclados, la apariencia elegida y la versión y fecha en que aceptaste los términos. La contraseña la guarda cifrada nuestro proveedor de autenticación: nosotros nunca la vemos.',
        'Mi impacto: los montos que escribes (por ejemplo, tu dividendo o los litros de bencina) se calculan en tu dispositivo y no se envían a nuestros servidores.',
        'Datos técnicos: nuestros proveedores registran datos como la dirección IP y la hora de cada conexión, para seguridad y para que el servicio funcione.',
      ],
    },
    {
      titulo: '3. Para qué los usamos',
      parrafos: [
        'Para crear y mantener tu cuenta, guardar tus preferencias en todos tus dispositivos, enviarte los correos de verificación y de recuperación de contraseña, y proteger la app. No los usamos para publicidad, no los vendemos y no los compartimos con terceros para fines propios de ellos.',
      ],
    },
    {
      titulo: '4. Por qué podemos tratarlos',
      parrafos: [
        'Por tu consentimiento, que das al crear la cuenta, y porque son necesarios para darte el servicio que pides. Puedes retirar tu consentimiento borrando tu cuenta.',
      ],
    },
    {
      titulo: '5. Dónde se guardan',
      parrafos: [
        'Usamos proveedores que guardan y procesan los datos por nosotros, con medidas de seguridad: Supabase (base de datos y cuentas, servidores en São Paulo, Brasil), Railway (servidores de la API, Estados Unidos) y Vercel (sitio web). Esto implica una transferencia internacional de datos, que hacemos solo con proveedores que ofrecen un nivel adecuado de protección.',
      ],
    },
    {
      titulo: '6. Cuánto tiempo',
      parrafos: [
        'Mientras tengas tu cuenta. Al borrarla eliminamos de inmediato tu cuenta, tu perfil y tus preferencias. Las copias de respaldo de los proveedores se borran en sus ciclos normales.',
      ],
    },
    {
      titulo: '7. Tus derechos',
      parrafos: [
        'Puedes pedir acceso a tus datos, corregirlos, borrarlos, oponerte a su uso, limitar su tratamiento y recibirlos en un formato que puedas llevar a otro servicio. Para borrar todo, usa "Borrar cuenta" en Mi cuenta. Para lo demás, escríbenos a ' +
          `${CORREO_CONTACTO}: te responderemos en un plazo máximo de 30 días.`,
        'Si no quedas conforme, puedes reclamar ante la Agencia de Protección de Datos Personales.',
      ],
    },
    {
      titulo: '8. Seguridad',
      parrafos: [
        'Las conexiones van cifradas, las contraseñas se guardan cifradas y el acceso a la base está restringido: cada usuario solo puede ver sus propios datos. Si ocurre una filtración que te afecte, te avisaremos a ti y a la autoridad según lo exige la ley.',
      ],
    },
    {
      titulo: '9. Menores de edad',
      parrafos: [
        'La app no está dirigida a menores de 14 años y no guardamos a sabiendas datos de ellos. Si crees que un menor creó una cuenta, escríbenos y la borraremos.',
      ],
    },
    {
      titulo: '10. Cambios',
      parrafos: [
        'Si cambiamos esta política, publicaremos la nueva versión con su fecha y, si el cambio es importante, te lo avisaremos en la app o por correo.',
      ],
    },
  ],
};
