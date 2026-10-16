import type { ReactNode } from 'react';
import { StyleSheet, View } from 'react-native';

import { BloquePro, EtiquetaPlan } from '@/components/bloque-pro';
import { Spacing } from '@/constants/theme';
import { useCapacidades } from '@/hooks/use-capacidades';

type Props = {
  /** Id de la capacidad (docs/planes.md), por ejemplo "mi_impacto". */
  id: string;
  /** Qué ofrece, para el BloquePro cuando el plan no la incluye. */
  descripcion?: string;
  children: ReactNode;
};

/**
 * Muestra su contenido si el usuario tiene la capacidad; si no, el BloquePro.
 * En modo vista previa agrega la etiqueta del plan sobre el contenido.
 */
export function Capacidad({ id, descripcion, children }: Props) {
  const { modo, puede, planMinimo } = useCapacidades();
  const plan = planMinimo(id);

  if (!puede(id)) {
    return <BloquePro plan={plan} descripcion={descripcion} />;
  }
  if (modo === 'vista_previa' && plan !== 'gratis') {
    return (
      <View style={styles.conEtiqueta}>
        <EtiquetaPlan plan={plan} />
        {children}
      </View>
    );
  }
  return <>{children}</>;
}

const styles = StyleSheet.create({
  conEtiqueta: {
    gap: Spacing.two,
  },
});
