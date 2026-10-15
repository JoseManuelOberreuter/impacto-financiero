import AsyncStorage from '@react-native-async-storage/async-storage';
import { createContext, useCallback, useContext, useEffect, useState, type ReactNode } from 'react';
import { Appearance, Platform } from 'react-native';

export type PreferenciaTema = 'automatico' | 'claro' | 'oscuro';

// Preferencia del dispositivo: se guarda localmente, no necesita cuenta ni base de datos.
const CLAVE = 'impacto:preferencia-tema';

type ValorContexto = {
  preferencia: PreferenciaTema;
  cambiarPreferencia: (preferencia: PreferenciaTema) => void;
};

const Contexto = createContext<ValorContexto>({
  preferencia: 'automatico',
  cambiarPreferencia: () => {},
});

export function ProveedorTema({ children }: { children: ReactNode }) {
  const [preferencia, setPreferencia] = useState<PreferenciaTema>('automatico');

  useEffect(() => {
    AsyncStorage.getItem(CLAVE)
      .then((guardada) => {
        if (guardada === 'claro' || guardada === 'oscuro') setPreferencia(guardada);
      })
      .catch(() => {});
  }, []);

  // En iPhone y Android también se fuerza el tema nativo (barra de pestañas, teclado, etc.).
  useEffect(() => {
    if (Platform.OS === 'web') return;
    Appearance.setColorScheme(
      preferencia === 'claro' ? 'light' : preferencia === 'oscuro' ? 'dark' : 'unspecified',
    );
  }, [preferencia]);

  const cambiarPreferencia = useCallback((nueva: PreferenciaTema) => {
    setPreferencia(nueva);
    AsyncStorage.setItem(CLAVE, nueva).catch(() => {});
  }, []);

  return (
    <Contexto.Provider value={{ preferencia, cambiarPreferencia }}>{children}</Contexto.Provider>
  );
}

export function usePreferenciaTema() {
  return useContext(Contexto);
}

/** Aplica la preferencia sobre el modo del sistema. */
export function resolverEsquema<T extends string | null | undefined>(
  preferencia: PreferenciaTema,
  sistema: T,
): 'light' | 'dark' | T {
  if (preferencia === 'claro') return 'light';
  if (preferencia === 'oscuro') return 'dark';
  return sistema;
}
