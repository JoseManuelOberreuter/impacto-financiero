import { GlassView, isLiquidGlassAvailable } from 'expo-glass-effect';
import { Platform, StyleSheet, View, type ViewProps, type ViewStyle } from 'react-native';

import { Spacing } from '@/constants/theme';
import { useTheme } from '@/hooks/use-theme';

// En web se imita el vidrio con desenfoque del fondo (CSS backdrop-filter).
const DESENFOQUE_WEB =
  Platform.OS === 'web'
    ? ({ backdropFilter: 'blur(28px) saturate(170%)' } as ViewStyle)
    : null;

/**
 * Superficie de vidrio: Liquid Glass nativo en iOS 26+, y un equivalente
 * translúcido en web y en el resto de las plataformas.
 */
export function Vidrio({ style, children, ...props }: ViewProps) {
  const theme = useTheme();

  if (isLiquidGlassAvailable()) {
    return (
      <GlassView glassEffectStyle="regular" style={[styles.base, style]} {...props}>
        {children}
      </GlassView>
    );
  }

  return (
    <View
      style={[
        styles.base,
        {
          backgroundColor: Platform.OS === 'web' ? theme.vidrio : theme.vidrioSolido,
          borderColor: theme.vidrioBorde,
        },
        styles.borde,
        DESENFOQUE_WEB,
        style,
      ]}
      {...props}>
      {children}
    </View>
  );
}

const styles = StyleSheet.create({
  base: {
    borderRadius: Spacing.four,
    overflow: 'hidden',
  },
  borde: {
    borderWidth: StyleSheet.hairlineWidth,
  },
});
