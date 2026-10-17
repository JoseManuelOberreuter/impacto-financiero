-- La función que crea el perfil al registrarse solo la usa el trigger: nadie debe poder
-- llamarla por la API (aviso de seguridad de Supabase, 16-oct-2026).
revoke execute on function public.crear_perfil_nuevo() from public, anon, authenticated;
