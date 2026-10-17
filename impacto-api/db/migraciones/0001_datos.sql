-- Datos de las fuentes: series y sus observaciones (docs/arquitectura.md, docs/pendientes-backend.md).
-- Aplicada en Supabase (proyecto impacto-financiero, sa-east-1) el 16-oct-2026.
--
-- Todo dato con historia es una serie: el dólar, la bencina 95 de la RM, la marraqueta, la TMC
-- de consumo, etc. Así un solo conector genérico guarda cualquier fuente y la API calcula la
-- presión, el movimiento y los gráficos igual para todas.
--
-- Seguridad: RLS activado y sin políticas. Solo el backend (clave secreta / service_role) lee
-- y escribe; la app nunca habla directo con la base, siempre a través de la API.

create table public.fuentes (
  id text primary key,                 -- 'bcch', 'cne', 'cmf', 'odepa', 'sp', 'ine'
  nombre text not null,
  sitio text,
  notas text
);
comment on table public.fuentes is 'Instituciones de donde vienen los datos.';

create table public.series (
  id text primary key,                 -- 'bcch.dolar', 'cne.bencina95.13', 'odepa.marraqueta'
  fuente_id text not null references public.fuentes (id),
  codigo text,                         -- código en la fuente, por ejemplo 'F073.TCO.PRE.Z.D'
  nombre text not null,
  unidad text,
  frecuencia text not null check (frecuencia in ('diaria', 'semanal', 'mensual', 'trimestral', 'anual')),
  region text,                         -- código de región (13 = Metropolitana) cuando aplica
  metadatos jsonb not null default '{}'::jsonb,
  creada_el timestamptz not null default now()
);
comment on table public.series is 'Cada dato con historia: dólar, bencina por región, alimentos, tasas, etc.';
create index series_fuente_idx on public.series (fuente_id);

create table public.observaciones (
  serie_id text not null references public.series (id) on delete cascade,
  fecha date not null,
  valor double precision not null,
  provisional boolean not null default false,  -- por ejemplo, el valor cuota de las AFP antes de confirmarse
  actualizado_el timestamptz not null default now(),
  primary key (serie_id, fecha)
);
comment on table public.observaciones is 'Valores de cada serie por fecha. Se escriben con upsert: volver a descargar no duplica.';
create index observaciones_fecha_idx on public.observaciones (fecha);

create table public.corridas_ingesta (
  id bigint generated always as identity primary key,
  fuente_id text not null references public.fuentes (id),
  inicio timestamptz not null default now(),
  fin timestamptz,
  estado text not null default 'en_curso' check (estado in ('en_curso', 'ok', 'error')),
  filas integer not null default 0,
  error text
);
comment on table public.corridas_ingesta is 'Registro de cada descarga: cuándo, cuántas filas y si falló.';
create index corridas_fuente_inicio_idx on public.corridas_ingesta (fuente_id, inicio desc);

alter table public.fuentes enable row level security;
alter table public.series enable row level security;
alter table public.observaciones enable row level security;
alter table public.corridas_ingesta enable row level security;

insert into public.fuentes (id, nombre, sitio) values
  ('bcch', 'Banco Central de Chile', 'https://si3.bcentral.cl/siete'),
  ('cne', 'Comisión Nacional de Energía', 'https://api.cne.cl'),
  ('cmf', 'Comisión para el Mercado Financiero', 'https://api.cmfchile.cl'),
  ('odepa', 'Oficina de Estudios y Políticas Agrarias', 'https://datos.odepa.gob.cl'),
  ('sp', 'Superintendencia de Pensiones', 'https://www.spensiones.cl'),
  ('ine', 'Instituto Nacional de Estadísticas', 'https://www.ine.gob.cl');
