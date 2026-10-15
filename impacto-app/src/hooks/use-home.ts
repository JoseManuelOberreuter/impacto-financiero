import { useCallback, useEffect, useState } from 'react';

import { obtenerHome } from '@/api/cliente';
import type { Home } from '@/api/tipos';

type Estado =
  | { tipo: 'cargando' }
  | { tipo: 'error'; mensaje: string }
  | { tipo: 'listo'; home: Home };

function aEstado(promesa: Promise<Home>): Promise<Estado> {
  return promesa.then(
    (home) => ({ tipo: 'listo', home }),
    (error) => ({
      tipo: 'error',
      mensaje: error instanceof Error ? error.message : 'Error desconocido',
    }),
  );
}

export function useHome() {
  const [estado, setEstado] = useState<Estado>({ tipo: 'cargando' });

  useEffect(() => {
    let vigente = true;
    aEstado(obtenerHome()).then((nuevo) => vigente && setEstado(nuevo));
    return () => {
      vigente = false;
    };
  }, []);

  const recargar = useCallback(() => {
    setEstado({ tipo: 'cargando' });
    aEstado(obtenerHome()).then(setEstado);
  }, []);

  return { estado, recargar };
}
