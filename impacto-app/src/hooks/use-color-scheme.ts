import { useColorScheme as useRNColorScheme } from 'react-native';

import { resolverEsquema, usePreferenciaTema } from '@/hooks/use-preferencia-tema';

/** Modo claro u oscuro: la preferencia del usuario o, si es "automático", la del sistema. */
export function useColorScheme() {
  const { preferencia } = usePreferenciaTema();
  return resolverEsquema(preferencia, useRNColorScheme());
}
