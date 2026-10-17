-- Fotos: lo último de cada fuente, tal como lo usa la API (docs/ingesta.md).
-- Aplicada en Supabase (proyecto impacto-financiero, sa-east-1) el 17-oct-2026.
--
-- La ingesta diaria (python -m app.ingesta) guarda dos cosas por fuente:
-- 1. La foto completa en esta tabla (un documento por fuente, se reemplaza en cada corrida).
--    La API la lee al arrancar y se recarga sola cuando cambia actualizado_el.
-- 2. Cada valor con fecha en series/observaciones, para que la historia se acumule
--    (por ejemplo, la mediana diaria de las estaciones de la CNE, que la fuente no guarda).
--
-- Seguridad: RLS activado y sin políticas; solo el backend (service_role) lee y escribe.

create table public.fotos (
  id text primary key,                 -- 'bcch', 'cne', 'cmf', 'odepa', 'afp'
  fuente_id text not null references public.fuentes (id),
  contenido jsonb not null,
  descargado_el date not null,
  actualizado_el timestamptz not null default now()
);
comment on table public.fotos is 'Última foto de cada fuente, en el formato que usa la API.';

alter table public.fotos enable row level security;
