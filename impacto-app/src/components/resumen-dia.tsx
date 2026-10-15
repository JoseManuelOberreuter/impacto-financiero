import { StyleSheet } from 'react-native';

import { ThemedText } from '@/components/themed-text';
import { ThemedView } from '@/components/themed-view';
import { Spacing } from '@/constants/theme';
import { useTheme } from '@/hooks/use-theme';

export function ResumenDia({ titulo, texto }: { titulo: string; texto: string }) {
  const theme = useTheme();

  return (
    <ThemedView type="backgroundElement" style={[styles.card, { borderLeftColor: theme.accent }]}>
      <ThemedText type="smallBold" themeColor="accent">
        {titulo}
      </ThemedText>
      <ThemedText style={styles.texto}>{texto}</ThemedText>
    </ThemedView>
  );
}

const styles = StyleSheet.create({
  card: {
    borderLeftWidth: 4,
    borderRadius: Spacing.three,
    padding: Spacing.three,
    gap: Spacing.one,
  },
  texto: {
    fontSize: 17,
    lineHeight: 26,
  },
});
