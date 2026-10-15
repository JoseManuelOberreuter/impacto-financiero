import { StyleSheet } from 'react-native';

import { ThemedText } from '@/components/themed-text';
import { ThemedView } from '@/components/themed-view';
import { Spacing } from '@/constants/theme';
import { useTheme } from '@/hooks/use-theme';

// Se muestra mientras el usuario no haya configurado su AFP (ver docs/termometros.md).
export function MiAfpInvitacion() {
  const theme = useTheme();

  return (
    <ThemedView
      type="backgroundElement"
      style={[styles.card, { borderColor: theme.border }]}>
      <ThemedText type="smallBold" style={styles.titulo}>
        💼 Mi AFP
      </ThemedText>
      <ThemedText type="small" themeColor="textSecondary">
        Elige tu AFP y tu fondo para ver cada día cómo le va a tu ahorro previsional. Sin crear
        cuenta.
      </ThemedText>
      <ThemedView type="backgroundSelected" style={styles.boton}>
        <ThemedText type="smallBold" themeColor="textSecondary">
          Configurar (próximamente)
        </ThemedText>
      </ThemedView>
    </ThemedView>
  );
}

const styles = StyleSheet.create({
  card: {
    borderWidth: 1,
    borderStyle: 'dashed',
    borderRadius: Spacing.three,
    padding: Spacing.three,
    gap: Spacing.two,
  },
  titulo: {
    fontSize: 16,
  },
  boton: {
    alignSelf: 'flex-start',
    paddingHorizontal: Spacing.three,
    paddingVertical: Spacing.two,
    borderRadius: Spacing.four,
  },
});
