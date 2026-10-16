import { createContext, useContext, useEffect, useState, type ReactNode } from 'react';

import { obtener } from '@/api/cliente';
import type { Capacidades, ModoPlanes, Plan } from '@/api/tipos';

type ValorContexto = {
  modo: ModoPlanes;
  /** Si el usuario puede usar la capacidad ahora. */
  puede: (id: string) => boolean;
  /** Plan más barato que incluye la capacidad, para la etiqueta y el BloquePro. */
  planMinimo: (id: string) => Plan;
};

// Mientras carga, o si la API no responde, todo queda abierto: es el modo del MVP
// y nunca se debe bloquear a alguien por un error de red.
const ABIERTO: ValorContexto = {
  modo: 'abierto',
  puede: () => true,
  planMinimo: () => 'gratis',
};

const Contexto = createContext<ValorContexto>(ABIERTO);

/** Pide las capacidades una vez al abrir la app (GET /v1/yo/capacidades). */
export function ProveedorCapacidades({ children }: { children: ReactNode }) {
  const [valor, setValor] = useState<ValorContexto>(ABIERTO);

  useEffect(() => {
    obtener<Capacidades>('/yo/capacidades')
      .then((datos) =>
        setValor({
          modo: datos.modo,
          puede: (id) => datos.capacidades[id]?.activa ?? true,
          planMinimo: (id) => datos.capacidades[id]?.plan_minimo ?? 'gratis',
        }),
      )
      .catch(() => {});
  }, []);

  return <Contexto.Provider value={valor}>{children}</Contexto.Provider>;
}

export function useCapacidades() {
  return useContext(Contexto);
}
