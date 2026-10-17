import type { Session } from '@supabase/supabase-js';
import * as Linking from 'expo-linking';
import { router } from 'expo-router';
import { createContext, useContext, useEffect, useState, type ReactNode } from 'react';
import { Platform } from 'react-native';

import { enviar } from '@/api/cliente';
import { cuentasDisponibles, supabase } from '@/api/supabase';

type Resultado = { ok: true } | { ok: false; error: { message?: string; code?: string } };

type ValorContexto = {
  /** False si la app no tiene configurado Supabase: las cuentas se ocultan. */
  disponible: boolean;
  cargando: boolean;
  sesion: Session | null;
  token: string | null;
  crearCuenta: (nombre: string, correo: string, clave: string) => Promise<Resultado>;
  ingresar: (correo: string, clave: string) => Promise<Resultado>;
  reenviarVerificacion: (correo: string) => Promise<Resultado>;
  recuperar: (correo: string) => Promise<Resultado>;
  cambiarClave: (nueva: string) => Promise<Resultado>;
  salir: (enTodosLosDispositivos?: boolean) => Promise<void>;
  borrarCuenta: () => Promise<Resultado>;
};

const SIN_CUENTAS: Resultado = { ok: false, error: { message: 'Las cuentas no están disponibles' } };

const Contexto = createContext<ValorContexto>({
  disponible: false,
  cargando: false,
  sesion: null,
  token: null,
  crearCuenta: async () => SIN_CUENTAS,
  ingresar: async () => SIN_CUENTAS,
  reenviarVerificacion: async () => SIN_CUENTAS,
  recuperar: async () => SIN_CUENTAS,
  cambiarClave: async () => SIN_CUENTAS,
  salir: async () => {},
  borrarCuenta: async () => SIN_CUENTAS,
});

/** Dirección a la que vuelven los enlaces de los correos (web o app). */
function enlaceDeVuelta(ruta: string): string {
  if (Platform.OS === 'web' && typeof window !== 'undefined') {
    return `${window.location.origin}${ruta}`;
  }
  return Linking.createURL(ruta);
}

function resultado(error: { message?: string; code?: string } | null): Resultado {
  return error ? { ok: false, error } : { ok: true };
}

/** Sesión de Supabase Auth. La cuenta es opcional: sin sesión, la app funciona igual. */
export function ProveedorSesion({ children }: { children: ReactNode }) {
  const [sesion, setSesion] = useState<Session | null>(null);
  const [cargando, setCargando] = useState(cuentasDisponibles);

  useEffect(() => {
    if (!supabase) return;
    supabase.auth.getSession().then(({ data }) => {
      setSesion(data.session);
      setCargando(false);
    });
    const { data } = supabase.auth.onAuthStateChange((evento, nueva) => {
      setSesion(nueva);
      // El enlace del correo de recuperación abre la pantalla para elegir una nueva contraseña.
      if (evento === 'PASSWORD_RECOVERY') router.replace('/cuenta/nueva-clave');
    });
    return () => data.subscription.unsubscribe();
  }, []);

  // En la app nativa, los enlaces de los correos llegan como URL con la sesión en el fragmento.
  const url = Linking.useURL();
  useEffect(() => {
    if (!supabase || !url || Platform.OS === 'web') return;
    const fragmento = new URLSearchParams(url.split('#')[1] ?? '');
    const access_token = fragmento.get('access_token');
    const refresh_token = fragmento.get('refresh_token');
    if (access_token && refresh_token) {
      supabase.auth.setSession({ access_token, refresh_token }).then(() => {
        if (fragmento.get('type') === 'recovery') router.replace('/cuenta/nueva-clave');
      });
    }
  }, [url]);

  const valor: ValorContexto = {
    disponible: cuentasDisponibles,
    cargando,
    sesion,
    token: sesion?.access_token ?? null,
    crearCuenta: async (nombre, correo, clave) => {
      if (!supabase) return SIN_CUENTAS;
      const { error } = await supabase.auth.signUp({
        email: correo.trim(),
        password: clave,
        options: {
          data: nombre.trim() ? { nombre: nombre.trim() } : {},
          emailRedirectTo: enlaceDeVuelta('/cuenta'),
        },
      });
      return resultado(error);
    },
    ingresar: async (correo, clave) => {
      if (!supabase) return SIN_CUENTAS;
      const { error } = await supabase.auth.signInWithPassword({ email: correo.trim(), password: clave });
      return resultado(error);
    },
    reenviarVerificacion: async (correo) => {
      if (!supabase) return SIN_CUENTAS;
      const { error } = await supabase.auth.resend({
        type: 'signup',
        email: correo.trim(),
        options: { emailRedirectTo: enlaceDeVuelta('/cuenta') },
      });
      return resultado(error);
    },
    recuperar: async (correo) => {
      if (!supabase) return SIN_CUENTAS;
      const { error } = await supabase.auth.resetPasswordForEmail(correo.trim(), {
        redirectTo: enlaceDeVuelta('/cuenta/nueva-clave'),
      });
      return resultado(error);
    },
    cambiarClave: async (nueva) => {
      if (!supabase) return SIN_CUENTAS;
      const { error } = await supabase.auth.updateUser({ password: nueva });
      return resultado(error);
    },
    salir: async (enTodosLosDispositivos = false) => {
      await supabase?.auth.signOut({ scope: enTodosLosDispositivos ? 'global' : 'local' });
    },
    borrarCuenta: async () => {
      if (!supabase || !sesion) return SIN_CUENTAS;
      try {
        await enviar('/yo', 'DELETE', sesion.access_token);
      } catch (e) {
        return { ok: false, error: { message: e instanceof Error ? e.message : 'error' } };
      }
      await supabase.auth.signOut({ scope: 'local' });
      return { ok: true };
    },
  };

  return <Contexto.Provider value={valor}>{children}</Contexto.Provider>;
}

export function useSesion() {
  return useContext(Contexto);
}
