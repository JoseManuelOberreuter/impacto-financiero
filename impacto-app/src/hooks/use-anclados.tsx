import AsyncStorage from '@react-native-async-storage/async-storage';
import { createContext, useCallback, useContext, useEffect, useState, type ReactNode } from 'react';

import { enviar, obtener } from '@/api/cliente';
import { useCapacidades } from '@/hooks/use-capacidades';
import { useSesion } from '@/hooks/use-sesion';

// Los datos anclados se guardan en el dispositivo: no necesitan cuenta. Con sesión, además se
// sincronizan con la cuenta (GET/PUT /v1/yo/preferencias).
const CLAVE = 'impacto:anclados';

type ValorContexto = {
  anclados: string[];
  estaAnclado: (id: string) => boolean;
  /** Ancla o desancla. Devuelve false si se alcanzó el límite del plan. */
  alternar: (id: string) => boolean;
  /** Máximo de anclados del plan; null = sin límite. */
  limite: number | null;
};

const Contexto = createContext<ValorContexto>({
  anclados: [],
  estaAnclado: () => false,
  alternar: () => false,
  limite: null,
});

export function ProveedorAnclados({ children }: { children: ReactNode }) {
  const { limite: limiteDe } = useCapacidades();
  const limite = limiteDe('datos.anclados');
  const { token } = useSesion();
  const [anclados, setAnclados] = useState<string[]>([]);

  useEffect(() => {
    AsyncStorage.getItem(CLAVE)
      .then((guardado) => {
        if (guardado) setAnclados(JSON.parse(guardado));
      })
      .catch(() => {});
  }, []);

  // Al iniciar sesión: se unen los anclados de la cuenta con los del dispositivo (no se pierde nada).
  useEffect(() => {
    if (!token) return;
    Promise.all([
      obtener<{ anclados: string[] }>('/yo/preferencias', token),
      AsyncStorage.getItem(CLAVE).then((g) => (g ? (JSON.parse(g) as string[]) : [])),
    ])
      .then(([cuenta, locales]) => {
        const unidos = [...new Set([...cuenta.anclados, ...locales])];
        setAnclados(unidos);
        AsyncStorage.setItem(CLAVE, JSON.stringify(unidos)).catch(() => {});
        if (unidos.length !== cuenta.anclados.length) {
          enviar('/yo/preferencias', 'PUT', token, { ...cuenta, anclados: unidos }).catch(() => {});
        }
      })
      .catch(() => {});
  }, [token]);

  const guardar = useCallback(
    (nuevos: string[]) => {
      setAnclados(nuevos);
      AsyncStorage.setItem(CLAVE, JSON.stringify(nuevos)).catch(() => {});
      if (token) {
        obtener<Record<string, unknown>>('/yo/preferencias', token)
          .then((actuales) => enviar('/yo/preferencias', 'PUT', token, { ...actuales, anclados: nuevos }))
          .catch(() => {});
      }
    },
    [token],
  );

  const alternar = useCallback(
    (id: string) => {
      if (anclados.includes(id)) {
        guardar(anclados.filter((a) => a !== id));
        return true;
      }
      if (limite !== null && anclados.length >= limite) return false;
      guardar([...anclados, id]);
      return true;
    },
    [anclados, limite, guardar],
  );

  return (
    <Contexto.Provider
      value={{ anclados, estaAnclado: (id) => anclados.includes(id), alternar, limite }}>
      {children}
    </Contexto.Provider>
  );
}

export function useAnclados() {
  return useContext(Contexto);
}
