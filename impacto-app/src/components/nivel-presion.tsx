import { StyleSheet, View } from 'react-native';

import type { Presion, Tendencia } from '@/api/tipos';
import { ThemedText } from '@/components/themed-text';
import { PRESION, TENDENCIA } from '@/constants/presion';
import { Spacing } from '@/constants/theme';
import { useTheme } from '@/hooks/use-theme';

type Props = {
  presion: Presion;
  tendencia?: Tendencia;
  /** Texto a mostrar; por defecto "Presión baja/media/alta". */
  etiqueta?: string;
  conFondo?: boolean;
};

/** Nivel de presión escrito, con su color y la flecha de tendencia. */
export function NivelPresion({ presion, tendencia, etiqueta, conFondo = true }: Props) {
  const theme = useTheme();
  const nivel = PRESION[presion];
  const IconoTendencia = tendencia ? TENDENCIA[tendencia].icono : null;

  return (
    <View style={[styles.chip, conFondo && { backgroundColor: theme[nivel.fondo] }, conFondo && styles.conFondo]}>
      {IconoTendencia && <IconoTendencia size={14} color={theme[nivel.color]} strokeWidth={2.5} />}
      <ThemedText type="smallBold" themeColor={nivel.color}>
        {etiqueta ?? `Presión ${nivel.texto.toLowerCase()}`}
      </ThemedText>
    </View>
  );
}

const styles = StyleSheet.create({
  chip: {
    flexDirection: 'row',
    alignItems: 'center',
    alignSelf: 'flex-start',
    gap: Spacing.one,
  },
  conFondo: {
    paddingHorizontal: Spacing.two,
    paddingVertical: Spacing.half,
    borderRadius: Spacing.two,
  },
});
