import AsyncStorage from '@react-native-async-storage/async-storage';
import { createContext, useCallback, useContext, useEffect, useState, type ReactNode } from 'react';

import { useCapacidades } from '@/hooks/use-capacidades';

// Los datos anclados se guardan en el dispositivo: no necesitan cuenta.
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
  const [anclados, setAnclados] = useState<string[]>([]);

  useEffect(() => {
    AsyncStorage.getItem(CLAVE)
      .then((guardado) => {
        if (guardado) setAnclados(JSON.parse(guardado));
      })
      .catch(() => {});
  }, []);

  const alternar = useCallback(
    (id: string) => {
      if (anclados.includes(id)) {
        const nuevos = anclados.filter((a) => a !== id);
        setAnclados(nuevos);
        AsyncStorage.setItem(CLAVE, JSON.stringify(nuevos)).catch(() => {});
        return true;
      }
      if (limite !== null && anclados.length >= limite) return false;
      const nuevos = [...anclados, id];
      setAnclados(nuevos);
      AsyncStorage.setItem(CLAVE, JSON.stringify(nuevos)).catch(() => {});
      return true;
    },
    [anclados, limite],
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
