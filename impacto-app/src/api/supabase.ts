import 'react-native-url-polyfill/auto';

import AsyncStorage from '@react-native-async-storage/async-storage';
import { createClient, type SupabaseClient } from '@supabase/supabase-js';
import { Platform } from 'react-native';

// Variables en impacto-app/.env.local (ver .env.example). La clave anon es pública:
// todas las tablas tienen RLS y los datos sensibles pasan por nuestra API.
const URL = process.env.EXPO_PUBLIC_SUPABASE_URL;
const CLAVE_PUBLICA = process.env.EXPO_PUBLIC_SUPABASE_ANON_KEY;

/** True si la app tiene configurado Supabase; si no, las cuentas se ocultan. */
export const cuentasDisponibles = Boolean(URL && CLAVE_PUBLICA);

// En la web la página también se arma en el servidor (output "static"), donde no hay
// almacenamiento: ahí el cliente se crea sin sesión persistente.
const enNavegador = Platform.OS !== 'web' || typeof window !== 'undefined';

export const supabase: SupabaseClient | null = cuentasDisponibles
  ? createClient(URL!, CLAVE_PUBLICA!, {
      auth: {
        storage: enNavegador ? AsyncStorage : undefined,
        persistSession: enNavegador,
        autoRefreshToken: enNavegador,
        // En la web, los enlaces de los correos (verificar, recuperar) traen la sesión en la URL.
        detectSessionInUrl: Platform.OS === 'web' && enNavegador,
      },
    })
  : null;
