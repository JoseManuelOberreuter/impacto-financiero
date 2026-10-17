import { router } from 'expo-router';
import { ChevronLeft } from 'lucide-react-native';
import type { ReactNode } from 'react';
import { Pressable, StyleSheet, View } from 'react-native';

import { ThemedText } from '@/components/themed-text';
import { Spacing } from '@/constants/theme';
import { useTheme } from '@/hooks/use-theme';

type Props = {
  titulo: string;
  bajada?: string;
  /** Ruta a la que vuelve si no hay historial (por ejemplo, al abrir el enlace directo). */
  volverA?: '/' | '/termometros' | '/precios' | '/herramientas' | '/cuenta';
  extra?: ReactNode;
};

export function Encabezado({ titulo, bajada, volverA, extra }: Props) {
  const theme = useTheme();

  return (
    <View style={styles.contenedor}>
      {volverA && (
        <Pressable
          onPress={() => (router.canGoBack() ? router.back() : router.replace(volverA))}
          accessibilityRole="button"
          accessibilityLabel="Volver"
          hitSlop={12}
          style={({ pressed }) => [styles.volver, pressed && styles.presionado]}>
          <ChevronLeft size={20} color={theme.accent} strokeWidth={2.25} />
          <ThemedText type="smallBold" themeColor="accent">
            Volver
          </ThemedText>
        </Pressable>
      )}
      <ThemedText style={styles.titulo}>{titulo}</ThemedText>
      {bajada && <ThemedText themeColor="textSecondary">{bajada}</ThemedText>}
      {extra}
    </View>
  );
}

const styles = StyleSheet.create({
  contenedor: {
    gap: Spacing.two,
  },
  volver: {
    flexDirection: 'row',
    alignItems: 'center',
    alignSelf: 'flex-start',
    marginLeft: -Spacing.one,
    marginBottom: Spacing.one,
  },
  titulo: {
    fontSize: 32,
    lineHeight: 38,
    fontWeight: 700,
    letterSpacing: -0.8,
  },
  presionado: {
    opacity: 0.6,
  },
});
