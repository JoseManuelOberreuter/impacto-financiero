-- Usuarios, preferencias y planes (docs/planes.md, docs/plan-pro.md).
-- Aplicada en Supabase (proyecto impacto-financiero, sa-east-1) el 16-oct-2026.
--
-- Las cuentas las maneja Supabase Auth (tabla auth.users: correo, inicio de sesión, Google/Apple).
-- Aquí va lo nuestro: el perfil, lo que se sincroniza entre dispositivos y el plan de cada uno.
-- Guardamos lo mínimo (Ley 21.719): sin RUT, sin teléfono, sin datos bancarios.

-- Perfil: uno por cuenta, creado automáticamente al registrarse.
create table public.perfiles (
  id uuid primary key references auth.users (id) on delete cascade,
  nombre text,
  creado_el timestamptz not null default now()
);
comment on table public.perfiles is 'Datos básicos de cada cuenta. Se borra junto con la cuenta.';

-- Preferencias que se sincronizan entre dispositivos.
create table public.preferencias (
  usuario_id uuid primary key references auth.users (id) on delete cascade,
  anclados text[] not null default '{}',                 -- ids de los datos anclados en el Inicio
  apariencia text not null default 'automatico' check (apariencia in ('automatico', 'claro', 'oscuro')),
  -- Mi impacto (dividendo en UF, litros de bencina...). Solo si el usuario elige sincronizarlo:
  -- por defecto se queda en su dispositivo.
  mi_impacto jsonb,
  actualizado_el timestamptz not null default now()
);
comment on table public.preferencias is 'Anclados, apariencia y, si el usuario quiere, sus datos de Mi impacto.';

-- Planes y capacidades: el catálogo que hoy vive en app/planes.py, editable sin código.
create table public.planes (
  id text primary key check (id in ('gratis', 'pro', 'empresas')),
  nombre text not null,
  precio_mensual integer,              -- en pesos; null mientras no se cobre
  precio_anual integer,
  activo boolean not null default true
);

create table public.capacidades (
  id text primary key,                 -- 'mi_impacto', 'datos.anclados', 'historia.larga', ...
  descripcion text not null
);

create table public.plan_capacidades (
  plan_id text not null references public.planes (id) on delete cascade,
  capacidad_id text not null references public.capacidades (id) on delete cascade,
  limite integer,                      -- por ejemplo, 3 anclados en el plan gratis; null = sin límite
  primary key (plan_id, capacidad_id)
);

-- Suscripción de cada usuario. Sin fila = plan gratis.
create table public.suscripciones (
  id bigint generated always as identity primary key,
  usuario_id uuid not null references auth.users (id) on delete cascade,
  plan_id text not null references public.planes (id),
  estado text not null check (estado in ('prueba', 'activa', 'vencida', 'cancelada')),
  origen text not null check (origen in ('google_play', 'app_store', 'web', 'factura', 'regalo')),
  vence_el timestamptz,
  id_externo text,                     -- id del pago en RevenueCat o la tienda
  creada_el timestamptz not null default now()
);
create index suscripciones_usuario_idx on public.suscripciones (usuario_id, estado);

-- Qué capacidades se usan, para decidir precios (docs/planes.md). Sin datos personales.
create table public.uso_capacidades (
  id bigint generated always as identity primary key,
  usuario_id uuid references auth.users (id) on delete set null,
  capacidad_id text not null references public.capacidades (id),
  fecha date not null default current_date
);
create index uso_capacidades_fecha_idx on public.uso_capacidades (capacidad_id, fecha);

-- Seguridad. Perfil y preferencias: cada usuario lee y edita solo lo suyo. El resto, solo el backend.
alter table public.perfiles enable row level security;
alter table public.preferencias enable row level security;
alter table public.planes enable row level security;
alter table public.capacidades enable row level security;
alter table public.plan_capacidades enable row level security;
alter table public.suscripciones enable row level security;
alter table public.uso_capacidades enable row level security;

create policy "Cada usuario ve su perfil" on public.perfiles
  for select to authenticated using ((select auth.uid()) = id);
create policy "Cada usuario edita su perfil" on public.perfiles
  for update to authenticated using ((select auth.uid()) = id) with check ((select auth.uid()) = id);

create policy "Cada usuario ve sus preferencias" on public.preferencias
  for select to authenticated using ((select auth.uid()) = usuario_id);
create policy "Cada usuario crea sus preferencias" on public.preferencias
  for insert to authenticated with check ((select auth.uid()) = usuario_id);
create policy "Cada usuario edita sus preferencias" on public.preferencias
  for update to authenticated using ((select auth.uid()) = usuario_id) with check ((select auth.uid()) = usuario_id);

create policy "Cada usuario ve sus suscripciones" on public.suscripciones
  for select to authenticated using ((select auth.uid()) = usuario_id);

-- Al registrarse, se crean su perfil y sus preferencias.
create function public.crear_perfil_nuevo()
returns trigger
language plpgsql
security definer
set search_path = ''
as $$
begin
  insert into public.perfiles (id, nombre) values (new.id, new.raw_user_meta_data ->> 'nombre');
  insert into public.preferencias (usuario_id) values (new.id);
  return new;
end;
$$;

create trigger al_crear_usuario
  after insert on auth.users
  for each row execute function public.crear_perfil_nuevo();

-- Catálogo inicial (igual que app/planes.py).
insert into public.planes (id, nombre) values
  ('gratis', 'Gratis'), ('pro', 'Pro'), ('empresas', 'Empresas');

insert into public.capacidades (id, descripcion) values
  ('termometros.basico', 'Nivel, dato principal y frase de cada termómetro'),
  ('historia.1_anio', 'Gráficos de hasta 12 meses'),
  ('historia.larga', 'Gráficos de 5, 10 y 20 años'),
  ('expectativas', 'Lo que viene: expectativas de economistas y operadores'),
  ('sorpresa_dato', 'Dato real frente a lo esperado'),
  ('cruces', 'Gráficos que comparan dos series'),
  ('termometro.consumo', 'Detalle del termómetro de Consumo'),
  ('termometro.vivienda', 'Termómetro de Vivienda'),
  ('precios.vs_ipc', 'Canasta frente al IPC de alimentos'),
  ('aviso_bencina', 'Estimación de la próxima variación de la bencina'),
  ('mi_impacto', 'Mi impacto completo en pesos'),
  ('datos.anclados', 'Datos anclados arriba en el Inicio'),
  ('calculadoras.basicas', 'Calculadoras con tasas reales'),
  ('calculadoras.escenarios', 'Calculadoras con escenarios'),
  ('alertas', 'Avisos de umbrales y publicaciones'),
  ('descargas.csv', 'Descarga de series'),
  ('calendario.basico', 'Fechas reales de publicación'),
  ('calendario.expectativas', 'Lo esperado y la sorpresa en cada fecha'),
  ('mi_rubro', 'Ventas, sueldos y crédito del rubro'),
  ('reajustes_ipc', 'Reajustes de contratos por IPC o UF'),
  ('usuarios', 'Usuarios por cuenta'),
  ('api.acceso', 'Claves para usar nuestra API'),
  ('api.limite_diario', 'Consultas a la API por día');

insert into public.plan_capacidades (plan_id, capacidad_id, limite)
select p.id, c.id, null from public.planes p cross join public.capacidades c
where (p.id = 'gratis' and c.id in ('termometros.basico', 'historia.1_anio', 'calculadoras.basicas',
                                    'calendario.basico', 'datos.anclados', 'usuarios'))
   or (p.id = 'pro' and c.id not in ('mi_rubro', 'reajustes_ipc', 'api.acceso', 'api.limite_diario'))
   or (p.id = 'empresas');

update public.plan_capacidades set limite = 3 where plan_id = 'gratis' and capacidad_id = 'datos.anclados';
update public.plan_capacidades set limite = 1 where plan_id in ('gratis', 'pro') and capacidad_id = 'usuarios';
update public.plan_capacidades set limite = 5 where plan_id = 'empresas' and capacidad_id = 'usuarios';
update public.plan_capacidades set limite = 10 where plan_id = 'pro' and capacidad_id = 'alertas';
update public.plan_capacidades set limite = 50 where plan_id = 'empresas' and capacidad_id = 'alertas';
update public.plan_capacidades set limite = 10000 where plan_id = 'empresas' and capacidad_id = 'api.limite_diario';
