import { Link } from 'expo-router';
import { Pressable, StyleSheet, View } from 'react-native';

import type { Canasta } from '@/api/tipos';
import { MiniGrafico } from '@/components/mini-grafico';
import { ThemedText } from '@/components/themed-text';
import { Vidrio } from '@/components/vidrio';
import { Spacing } from '@/constants/theme';
import { useTheme } from '@/hooks/use-theme';
import { pesos, porcentaje } from '@/utils/numeros';

/** Canasta semanal en una línea: total y variación a la izquierda, tendencia a la derecha. */
export function CanastaCompacta({ canasta }: { canasta: Canasta }) {
  const theme = useTheme();
  const color = canasta.variacion_semanal > 0 ? 'presionAlta' : 'presionBaja';

  return (
    <Link href="/precios" asChild>
      <Pressable>
        <Vidrio style={styles.card}>
          <View style={styles.textos}>
            <ThemedText type="small" themeColor="textSecondary">
              Canasta semanal
            </ThemedText>
            <ThemedText style={styles.total}>{pesos(canasta.total)}</ThemedText>
            <ThemedText type="smallBold" themeColor={color}>
              {porcentaje(canasta.variacion_semanal)}
            </ThemedText>
          </View>
          <View style={styles.grafico}>
            <MiniGrafico valores={canasta.serie.map((p) => p.precio)} color={theme.accent} alto={44} />
          </View>
        </Vidrio>
      </Pressable>
    </Link>
  );
}

const styles = StyleSheet.create({
  card: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: Spacing.three,
    padding: Spacing.four,
  },
  textos: {
    flex: 1,
    gap: Spacing.half,
  },
  total: {
    fontSize: 30,
    lineHeight: 36,
    fontWeight: 700,
    letterSpacing: -0.8,
  },
  grafico: {
    width: 120,
  },
});
