import type { ReactNode } from 'react';
import { StyleSheet, View } from 'react-native';

import { ThemedText } from '@/components/themed-text';
import { Spacing } from '@/constants/theme';

/** Bloque con un título pequeño en gris y su contenido debajo. */
export function Seccion({ titulo, children }: { titulo: string; children: ReactNode }) {
  return (
    <View style={styles.seccion}>
      <ThemedText type="small" themeColor="textSecondary">
        {titulo}
      </ThemedText>
      {children}
    </View>
  );
}

const styles = StyleSheet.create({
  seccion: {
    gap: Spacing.three,
  },
});
