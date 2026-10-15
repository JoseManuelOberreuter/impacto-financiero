import { useSyncExternalStore } from 'react';
import { useColorScheme as useRNColorScheme } from 'react-native';

import { resolverEsquema, usePreferenciaTema } from '@/hooks/use-preferencia-tema';

const sinSuscripcion = () => () => {};

/**
 * To support static rendering, this value needs to be re-calculated on the client side for web
 */
export function useColorScheme() {
  // false durante el render estático en el servidor, true en el navegador.
  const hasHydrated = useSyncExternalStore(
    sinSuscripcion,
    () => true,
    () => false,
  );

  const colorScheme = useRNColorScheme();
  const { preferencia } = usePreferenciaTema();

  if (hasHydrated) {
    return resolverEsquema(preferencia, colorScheme);
  }

  return 'light';
}
