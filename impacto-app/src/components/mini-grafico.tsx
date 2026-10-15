import { useId, useState } from 'react';
import { View } from 'react-native';
import Svg, { Circle, Defs, LinearGradient, Path, Rect, Stop } from 'react-native-svg';

type Props = {
  valores: number[];
  color: string;
  alto?: number;
  /** Rango habitual del indicador: se dibuja como una franja de fondo. */
  banda?: { min: number; max: number } | null;
  colorBanda?: string;
};

const MARGEN = 4;

/** Línea de tendencia sin ejes, con relleno suave y, opcionalmente, la banda de "lo normal". */
export function MiniGrafico({ valores, color, alto = 56, banda, colorBanda }: Props) {
  const [ancho, setAncho] = useState(0);
  const idRelleno = `relleno-${useId().replace(/:/g, '')}`;

  if (valores.length < 2) {
    return null;
  }

  // Escala mínima de ±4 % del promedio: así variaciones pequeñas no parecen saltos.
  const extremos = banda ? [...valores, banda.min, banda.max] : valores;
  const promedio = valores.reduce((a, v) => a + v, 0) / valores.length;
  const rangoReal = Math.max(...extremos) - Math.min(...extremos);
  const holgura = Math.max(0, (Math.abs(promedio) * 0.08 - rangoReal) / 2);
  const min = Math.min(...extremos) - holgura;
  const max = Math.max(...extremos) + holgura;
  const rango = max - min || 1;
  const y = (v: number) => MARGEN + (1 - (v - min) / rango) * (alto - MARGEN * 2);

  const puntos = valores.map((v, i) => ({
    x: MARGEN + (i / (valores.length - 1)) * (ancho - MARGEN * 2),
    y: y(v),
  }));
  const linea = puntos.map((p, i) => `${i === 0 ? 'M' : 'L'}${p.x},${p.y}`).join(' ');
  const ultimo = puntos[puntos.length - 1];

  return (
    <View style={{ height: alto }} onLayout={(e) => setAncho(e.nativeEvent.layout.width)}>
      {ancho > 0 && (
        <Svg width={ancho} height={alto}>
          <Defs>
            <LinearGradient id={idRelleno} x1="0" y1="0" x2="0" y2="1">
              <Stop offset="0" stopColor={color} stopOpacity={0.25} />
              <Stop offset="1" stopColor={color} stopOpacity={0} />
            </LinearGradient>
          </Defs>
          {banda && (
            <Rect
              x={0}
              y={y(banda.max)}
              width={ancho}
              height={Math.max(y(banda.min) - y(banda.max), 1)}
              fill={colorBanda ?? color}
              opacity={0.12}
              rx={6}
            />
          )}
          <Path
            d={`${linea} L${ultimo.x},${alto} L${puntos[0].x},${alto} Z`}
            fill={`url(#${idRelleno})`}
          />
          <Path d={linea} stroke={color} strokeWidth={2} fill="none" strokeLinejoin="round" />
          <Circle cx={ultimo.x} cy={ultimo.y} r={3.5} fill={color} />
        </Svg>
      )}
    </View>
  );
}
