import { useId } from 'react';
import { StyleSheet } from 'react-native';
import Svg, { Defs, RadialGradient, Rect, Stop } from 'react-native-svg';

import { useTheme } from '@/hooks/use-theme';

// Luces difusas de un mismo tono detrás del contenido: le dan algo que "refractar" al vidrio.
const LUCES = [
  { id: 'luz1', cx: '15%', cy: '8%', r: '55%', color: 'ambiente1', opacidad: 0.55 },
  { id: 'luz2', cx: '95%', cy: '30%', r: '50%', color: 'ambiente2', opacidad: 0.35 },
  { id: 'luz3', cx: '30%', cy: '85%', r: '60%', color: 'ambiente3', opacidad: 0.45 },
] as const;

export function FondoAmbiente() {
  const theme = useTheme();
  // En web las pestañas quedan montadas a la vez: cada fondo necesita ids propios
  // o el navegador usa los degradados de una pestaña oculta y no se ve nada.
  const prefijo = useId().replace(/:/g, '');

  return (
    <Svg width="100%" height="100%" style={StyleSheet.absoluteFill} pointerEvents="none">
      <Defs>
        {LUCES.map((luz) => (
          <RadialGradient
            key={luz.id}
            id={`${prefijo}-${luz.id}`}
            cx={luz.cx}
            cy={luz.cy}
            r={luz.r}>
            <Stop offset="0" stopColor={theme[luz.color]} stopOpacity={luz.opacidad} />
            <Stop offset="1" stopColor={theme[luz.color]} stopOpacity={0} />
          </RadialGradient>
        ))}
      </Defs>
      <Rect width="100%" height="100%" fill={theme.background} />
      {LUCES.map((luz) => (
        <Rect key={luz.id} width="100%" height="100%" fill={`url(#${prefijo}-${luz.id})`} />
      ))}
    </Svg>
  );
}
