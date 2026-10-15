import { StyleSheet, View } from 'react-native';

import { ThemedText } from '@/components/themed-text';
import { Spacing } from '@/constants/theme';
import { useTheme } from '@/hooks/use-theme';

type Props = {
  etiqueta: string;
  valor: string;
  /** Proporción de 0 a 1 respecto del máximo de la lista. */
  proporcion: number;
  destacada?: boolean;
};

/** Barra horizontal simple para comparar valores (regiones, composición de la canasta). */
export function Barra({ etiqueta, valor, proporcion, destacada }: Props) {
  const theme = useTheme();

  return (
    <View style={styles.contenedor}>
      <View style={styles.textos}>
        <ThemedText type={destacada ? 'smallBold' : 'small'}>{etiqueta}</ThemedText>
        <ThemedText type="smallBold">{valor}</ThemedText>
      </View>
      <View style={[styles.pista, { backgroundColor: theme.backgroundSelected }]}>
        <View
          style={[
            styles.relleno,
            {
              width: `${Math.max(Math.min(proporcion, 1), 0.02) * 100}%`,
              backgroundColor: theme.accent,
              opacity: destacada ? 1 : 0.55,
            },
          ]}
        />
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  contenedor: {
    gap: Spacing.one,
  },
  textos: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  pista: {
    height: 6,
    borderRadius: 3,
    overflow: 'hidden',
  },
  relleno: {
    height: '100%',
    borderRadius: 3,
  },
});
