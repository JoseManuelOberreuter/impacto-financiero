import { useCallback, useEffect, useState } from 'react';

import { obtener } from '@/api/cliente';

export type EstadoCarga<T> =
  | { tipo: 'cargando' }
  | { tipo: 'error'; mensaje: string }
  | { tipo: 'listo'; datos: T };

function aEstado<T>(promesa: Promise<T>): Promise<EstadoCarga<T>> {
  return promesa.then(
    (datos) => ({ tipo: 'listo', datos }),
    (error) => ({
      tipo: 'error',
      mensaje: error instanceof Error ? error.message : 'Error desconocido',
    }),
  );
}

/** Carga una ruta de la API y expone su estado (cargando, error o listo). */
export function useApi<T>(ruta: string) {
  const [estado, setEstado] = useState<EstadoCarga<T>>({ tipo: 'cargando' });

  useEffect(() => {
    let vigente = true;
    aEstado(obtener<T>(ruta)).then((nuevo) => vigente && setEstado(nuevo));
    return () => {
      vigente = false;
    };
  }, [ruta]);

  const recargar = useCallback(() => {
    setEstado({ tipo: 'cargando' });
    aEstado(obtener<T>(ruta)).then(setEstado);
  }, [ruta]);

  return { estado, recargar };
}
