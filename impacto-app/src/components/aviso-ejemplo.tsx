import { StyleSheet, View } from 'react-native';

import { ThemedText } from '@/components/themed-text';
import { Spacing } from '@/constants/theme';
import { useDiseno } from '@/hooks/use-diseno';

/**
 * Aviso temporal de "datos de ejemplo", fijo y discreto en la esquina inferior izquierda.
 * Para quitarlo: borrar este archivo y su línea en src/app/_layout.tsx.
 */
export function AvisoEjemplo() {
  const { esWeb, esEscritorio } = useDiseno();
  // Sobre la barra de pestañas cuando está abajo (celular y web angosta).
  const abajo = esEscritorio ? Spacing.three : esWeb ? 100 : 96;

  return (
    <View pointerEvents="none" style={[styles.aviso, { bottom: abajo }]}>
      <ThemedText type="small" themeColor="textSecondary" style={styles.texto}>
        Datos de ejemplo
      </ThemedText>
    </View>
  );
}

const styles = StyleSheet.create({
  aviso: {
    position: 'absolute',
    left: Spacing.three,
    opacity: 0.5,
  },
  texto: {
    fontSize: 10,
    lineHeight: 14,
  },
});
