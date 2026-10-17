import { createContext, useContext, useEffect, useState, type ReactNode } from 'react';

import { obtener } from '@/api/cliente';
import type { Capacidades, ModoPlanes, Plan } from '@/api/tipos';
import { useSesion } from '@/hooks/use-sesion';

type ValorContexto = {
  modo: ModoPlanes;
  /** Si el usuario puede usar la capacidad ahora. */
  puede: (id: string) => boolean;
  /** Plan más barato que incluye la capacidad, para la etiqueta y el BloquePro. */
  planMinimo: (id: string) => Plan;
  /** Cantidad máxima en las capacidades con límite (por ejemplo, datos anclados); null = sin límite. */
  limite: (id: string) => number | null;
};

// Mientras carga, o si la API no responde, todo queda abierto: es el modo del MVP
// y nunca se debe bloquear a alguien por un error de red.
const ABIERTO: ValorContexto = {
  modo: 'abierto',
  puede: () => true,
  planMinimo: () => 'gratis',
  limite: () => null,
};

const Contexto = createContext<ValorContexto>(ABIERTO);

/** Pide las capacidades al abrir la app y cada vez que se inicia o cierra sesión. */
export function ProveedorCapacidades({ children }: { children: ReactNode }) {
  const { token } = useSesion();
  const [valor, setValor] = useState<ValorContexto>(ABIERTO);

  useEffect(() => {
    obtener<Capacidades>('/yo/capacidades', token)
      .then((datos) =>
        setValor({
          modo: datos.modo,
          puede: (id) => datos.capacidades[id]?.activa ?? true,
          planMinimo: (id) => datos.capacidades[id]?.plan_minimo ?? 'gratis',
          limite: (id) => datos.capacidades[id]?.limite ?? null,
        }),
      )
      .catch(() => {});
  }, [token]);

  return <Contexto.Provider value={valor}>{children}</Contexto.Provider>;
}

export function useCapacidades() {
  return useContext(Contexto);
}
