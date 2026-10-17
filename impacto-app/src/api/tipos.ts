// Tipos de las respuestas de impacto-api (app/modelos/*.py).
// Más adelante se generarán automáticamente desde el OpenAPI del backend.

export type Presion = 'baja' | 'media' | 'alta';
export type Tendencia = 'sube' | 'baja' | 'estable';

export type Termometro = {
  id: string;
  nombre: string;
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

export type PuntoSerie = { fecha: string; valor: number };

export type Indicador = {
  id: string;
  nombre: string;
  valor: string;
  variacion: string | null;
  presion: Presion;
  descripcion: string;
  serie: PuntoSerie[];
  banda_normal: { min: number; max: number } | null;
  fuente: string;
  dato_al: string;
  /** Dónde está comparado con lo normal, en palabras: "Más cara que lo normal". */
  estado?: string | null;
};

export type Publicacion = { fecha: string; nombre: string; fuente: string };

export type TermometroDetalle = Termometro & {
  explicacion: string;
  indicadores: Indicador[];
  percepcion: { nombre: string; valor: string; descripcion: string; fuente: string } | null;
  proximas_publicaciones: Publicacion[];
  metodologia: string;
  herramienta_relacionada: string | null;
  /** Solo en el termómetro Impacto Financiero: el detalle por rubro. */
  impacto?: ImpactoFinanciero | null;
};

export type PuntoPrecio = { semana: string; precio: number };

export type Producto = {
  id: string;
  nombre: string;
  unidad: string;
  categoria: string;
  precio: number;
  variacion_semanal: number;
  variacion_anual: number;
  puntos_de_venta: number;
  serie: PuntoPrecio[];
  por_tipo_local: { tipo: string; precio: number }[];
  por_region: { region: string; precio: number }[];
  dato_al: string;
  fuente: string;
};

export type PrecioReferencia = {
  id: string;
  nombre: string;
  unidad: string;
  precio: number;
  fuente: string;
  nota: string;
  de_ejemplo: boolean;
};

export type Canasta = {
  total: number;
  variacion_semanal: number;
  dato_al: string;
  serie: PuntoPrecio[];
  composicion: { nombre: string; cantidad: string; costo: number; porcentaje: number }[];
  nota: string;
};

export type Precios = {
  canasta: Canasta;
  productos: Producto[];
  energia_y_transporte: PrecioReferencia[];
};

export type Titular = { titulo: string; medio: string; fecha: string; enlace: string | null };

export type Noticias = {
  presion: Presion;
  etiqueta: string;
  tendencia: Tendencia;
  tono_semana: number;
  serie_tono: PuntoSerie[];
  incertidumbre: number;
  total_titulares: number;
  medios: number;
  temas: {
    nombre: string;
    termometro: string;
    tono: number;
    cantidad: number;
    titulares: Titular[];
  }[];
  hechos_esenciales: { entidad: string; titulo: string; resumen: string; fecha: string }[];
  dato_al: string;
  nota: string;
};

export type Herramientas = {
  calculadoras: { id: string; nombre: string; descripcion: string; disponible: boolean }[];
  mi_afp: {
    dato_al: string;
    provisional: boolean;
    fuente: string;
    fondos: { fondo: string; afps: { afp: string; anio: number; mes: number }[] }[];
  };
  calendario: {
    fecha: string;
    nombre: string;
    fuente: string;
    termometro: string | null;
    estimada: boolean;
  }[];
  metodologia: { titulo: string; texto: string }[];
};

export type CambioSemana = {
  id: string;
  nombre: string;
  detalle: string;
  direccion: Tendencia;
  presion: Presion;
  serie: number[];
  /** Ruta de la app con el detalle (por ejemplo "/precios/papa"). */
  enlace: string;
  /** energia, alimentos, afuera, deudas, precios, empleo o animo. */
  tema: string;
  /** Qué significa para el bolsillo que el dato suba. */
  efecto: 'sube_malo' | 'sube_bueno' | 'neutro';
  /** Si el último movimiento conviene: colorea la flecha. */
  tono: 'favorable' | 'desfavorable' | 'neutral';
  /** Qué tan inusual fue el último cambio: veces lo que el dato suele moverse. */
  movimiento: number;
  /** Dónde está comparado con lo normal, en palabras: "Más cara que lo normal". */
  estado: string;
  /** sobre, normal o bajo lo normal de los últimos 5 años. */
  nivel: 'sobre' | 'normal' | 'bajo';
};

export type Home = {
  generado_el: string;
  datos_de_ejemplo: boolean;
  resumen: { titulo: string; texto: string };
  impacto: ImpactoFinanciero;
  canasta: Canasta;
  cambios: CambioSemana[];
  termometros: Termometro[];
  termometros_por_defecto: string[];
  max_termometros_home: number;
  aviso_legal: string;
};

/** Planes y capacidades (docs/planes.md). */
export type Plan = 'gratis' | 'pro' | 'empresas';
export type ModoPlanes = 'abierto' | 'vista_previa' | 'activo';

export type EstadoCapacidad = {
  activa: boolean;
  plan_minimo: Plan;
  limite: number | null;
};

export type Capacidades = {
  modo: ModoPlanes;
  plan: Plan;
  capacidades: Record<string, EstadoCapacidad>;
};

/** Valores de referencia para Mi impacto. El cálculo con los datos del usuario se hace en el dispositivo. */
export type ValorFechado = { fecha: string; valor: number };

export type ReferenciasMiImpacto = {
  uf: {
    hoy: ValorFechado;
    ultima_publicada: ValorFechado;
    hace_un_mes: ValorFechado;
    hace_un_anio: ValorFechado;
    fuente: string;
  };
  bencina95: {
    hoy: ValorFechado;
    hace_un_anio: ValorFechado;
    estaciones: number;
    region: string;
    fuente: string;
  };
};

/** Impacto Financiero: la inflación en pesos para un hogar típico (docs/impacto-financiero.md). */
export type RubroImpacto = {
  id: string;
  nombre: string;
  gasto_mes: number;
  diferencia_anual: number;
  diferencia_mensual: number;
  variacion_anual: number;
};

export type ImpactoFinanciero = {
  periodo: string;
  /** Fecha del dato más reciente: la bencina y la UF se actualizan a diario. */
  actualizado_al: string;
  hogar: string;
  gasto_mes: number;
  diferencia_anual: number;
  variacion_anual: number;
  diferencia_mensual: number;
  rubros: RubroImpacto[];
  fuente: string;
  metodologia: string;
};
