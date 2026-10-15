// Tipos de la respuesta de GET /v1/home (impacto-api/app/modelos/home.py).
// Más adelante se generarán automáticamente desde el OpenAPI del backend.

export type Presion = 'baja' | 'media' | 'alta';
export type Tendencia = 'sube' | 'baja' | 'estable';

export type Termometro = {
  id: string;
  nombre: string;
  icono: string;
  pregunta: string;
  presion: Presion;
  etiqueta_presion: string;
  tendencia: Tendencia;
  dato_clave: string;
  frase: string;
  /** Fecha ISO (YYYY-MM-DD) a la que corresponde el dato. */
  dato_al: string;
  proxima_actualizacion: string | null;
  fuentes: string[];
};

export type Home = {
  generado_el: string;
  datos_de_ejemplo: boolean;
  resumen: { titulo: string; texto: string };
  termometros: Termometro[];
  termometros_por_defecto: string[];
  max_termometros_home: number;
  aviso_legal: string;
};
