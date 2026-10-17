import { Check, ChevronDown } from 'lucide-react-native';
import { useState } from 'react';
import { Pressable, StyleSheet, View } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import Svg, { Polygon, Rect } from 'react-native-svg';

import { BotonCuenta } from '@/components/boton-cuenta';
import { ThemedText } from '@/components/themed-text';
import { Vidrio } from '@/components/vidrio';
import { Spacing } from '@/constants/theme';
import { useDiseno } from '@/hooks/use-diseno';
import { useTheme } from '@/hooks/use-theme';

/** Bandera de Chile dibujada (no emoji): franja blanca y roja, cuadro azul con estrella. */
export function BanderaChile({ ancho = 22 }: { ancho?: number }) {
  const alto = (ancho * 2) / 3;
  return (
    <Svg width={ancho} height={alto} viewBox="0 0 30 20" accessibilityLabel="Bandera de Chile">
      <Rect x={0} y={0} width={30} height={10} fill="#FFFFFF" />
      <Rect x={0} y={10} width={30} height={10} fill="#D52B1E" />
      <Rect x={0} y={0} width={10} height={10} fill="#0039A6" />
      <Polygon
        points="5,1.8 5.9,4.3 8.6,4.4 6.5,6 7.2,8.6 5,7.1 2.8,8.6 3.5,6 1.4,4.4 4.1,4.3"
        fill="#FFFFFF"
      />
      <Rect x={0} y={0} width={30} height={20} fill="none" stroke="rgba(0,0,0,0.15)" strokeWidth={0.6} />
    </Svg>
  );
}

/**
 * Selector de país fijo en la esquina superior derecha, con la burbuja de cuenta a su izquierda,, como el aviso de "datos de ejemplo":
 * por ahora solo Chile, con aviso de que vendrán más. Va en src/app/_layout.tsx.
 */
export function SelectorPais() {
  const theme = useTheme();
  const { esWeb } = useDiseno();
  const { top } = useSafeAreaInsets();
  const [abierto, setAbierto] = useState(false);

  return (
    <View style={[styles.contenedor, { top: esWeb ? Spacing.three : top + Spacing.two }]}>
      <View style={styles.fila}>
        <BotonCuenta />
        <Pressable
          onPress={() => setAbierto((a) => !a)}
          accessibilityRole="button"
          accessibilityLabel="País: Chile"
          accessibilityState={{ expanded: abierto }}
          style={styles.boton}>
          <BanderaChile />
          <ChevronDown size={14} color={theme.textSecondary} strokeWidth={2} />
        </Pressable>
      </View>

      {abierto && (
        <Vidrio style={[styles.menu, { backgroundColor: theme.backgroundElement }]}>
          <View style={styles.opcion}>
            <BanderaChile ancho={20} />
            <ThemedText type="smallBold" style={styles.nombre}>
              Chile
            </ThemedText>
            <Check size={16} color={theme.accent} strokeWidth={2.25} />
          </View>
          <ThemedText type="small" themeColor="textSecondary" style={styles.pronto}>
            Próximamente más países
          </ThemedText>
        </Vidrio>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  contenedor: {
    position: 'absolute',
    right: Spacing.three,
    zIndex: 20,
    alignItems: 'flex-end',
  },
  fila: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: Spacing.two,
  },
  boton: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: Spacing.one,
    paddingVertical: Spacing.one,
    paddingHorizontal: Spacing.one,
  },
  menu: {
    marginTop: Spacing.one,
    minWidth: 210,
    padding: Spacing.three,
    gap: Spacing.two,
  },
  opcion: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: Spacing.two,
  },
  nombre: {
    flex: 1,
  },
  pronto: {
    fontSize: 12,
    lineHeight: 16,
  },
});
