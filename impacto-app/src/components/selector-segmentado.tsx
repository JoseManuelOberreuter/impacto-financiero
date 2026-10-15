import { Pressable, StyleSheet, View } from 'react-native';

import { ThemedText } from '@/components/themed-text';
import { Spacing } from '@/constants/theme';
import { useTheme } from '@/hooks/use-theme';

type Props<T extends string> = {
  opciones: { valor: T; etiqueta: string }[];
  valor: T;
  onCambiar: (valor: T) => void;
  etiquetaAccesible: string;
};

/** Control segmentado tipo iOS: una sola opción activa. */
export function SelectorSegmentado<T extends string>({
  opciones,
  valor,
  onCambiar,
  etiquetaAccesible,
}: Props<T>) {
  const theme = useTheme();

  return (
    <View
      role="tablist"
      aria-label={etiquetaAccesible}
      style={[styles.contenedor, { backgroundColor: theme.backgroundSelected }]}>
      {opciones.map((opcion) => {
        const activo = opcion.valor === valor;
        return (
          <Pressable
            key={opcion.valor}
            onPress={() => onCambiar(opcion.valor)}
            role="tab"
            aria-selected={activo}
            style={[styles.opcion, activo && { backgroundColor: theme.backgroundElement }]}>
            <ThemedText type="smallBold" themeColor={activo ? 'text' : 'textSecondary'}>
              {opcion.etiqueta}
            </ThemedText>
          </Pressable>
        );
      })}
    </View>
  );
}

const styles = StyleSheet.create({
  contenedor: {
    flexDirection: 'row',
    borderRadius: Spacing.three,
    padding: Spacing.half,
  },
  opcion: {
    flex: 1,
    alignItems: 'center',
    paddingVertical: Spacing.two,
    borderRadius: Spacing.two + Spacing.half,
  },
});
