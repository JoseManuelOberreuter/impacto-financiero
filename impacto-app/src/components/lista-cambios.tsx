import { Link, type Href } from 'expo-router';
import { ArrowDownRight, ArrowUpRight, Minus, type LucideIcon } from 'lucide-react-native';
import { Pressable, StyleSheet, View } from 'react-native';

import type { CambioSemana, Tendencia } from '@/api/tipos';
import { MiniGrafico } from '@/components/mini-grafico';
import { ThemedText } from '@/components/themed-text';
import { Vidrio } from '@/components/vidrio';
import { PRESION } from '@/constants/presion';
import { Spacing } from '@/constants/theme';
import { useTheme } from '@/hooks/use-theme';

const FLECHA: Record<Tendencia, LucideIcon> = {
  sube: ArrowUpRight,
  baja: ArrowDownRight,
  estable: Minus,
};

/** "Lo que cambió esta semana": flecha, nombre, detalle y mini gráfico por fila. */
export function ListaCambios({ cambios }: { cambios: CambioSemana[] }) {
  const theme = useTheme();

  return (
    <Vidrio style={styles.lista}>
      {cambios.map((cambio, i) => (
        <FilaCambio
          key={cambio.id}
          cambio={cambio}
          divisor={i < cambios.length - 1 ? theme.border : undefined}
        />
      ))}
    </Vidrio>
  );
}

function FilaCambio({ cambio, divisor }: { cambio: CambioSemana; divisor?: string }) {
  const theme = useTheme();
  const nivel = PRESION[cambio.presion];
  const Flecha = FLECHA[cambio.direccion];

  return (
    // Link asChild exige un estilo plano en el Pressable: el diseño va en la vista interior.
    <Link href={cambio.enlace as Href} asChild>
      <Pressable accessibilityLabel={`${cambio.nombre}: ${cambio.detalle}`}>
        <View
          style={[
            styles.fila,
            divisor && {
              borderBottomColor: divisor,
              borderBottomWidth: StyleSheet.hairlineWidth,
            },
          ]}>
          <View style={[styles.icono, { backgroundColor: theme[nivel.fondo] }]}>
            <Flecha size={17} color={theme[nivel.color]} strokeWidth={2.25} />
          </View>
          <View style={styles.textos}>
            <ThemedText type="smallBold" style={styles.nombre}>
              {cambio.nombre}
            </ThemedText>
            <ThemedText type="small" themeColor="textSecondary" style={styles.detalle}>
              {cambio.detalle}
            </ThemedText>
          </View>
          <View style={styles.grafico}>
            <MiniGrafico valores={cambio.serie} color={theme[nivel.color]} alto={30} />
          </View>
        </View>
      </Pressable>
    </Link>
  );
}

const styles = StyleSheet.create({
  lista: {
    paddingHorizontal: Spacing.three,
    paddingVertical: Spacing.one,
  },
  fila: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: Spacing.three,
    paddingVertical: Spacing.three,
  },
  icono: {
    width: 34,
    height: 34,
    borderRadius: 17,
    alignItems: 'center',
    justifyContent: 'center',
  },
  textos: {
    flex: 1,
    gap: Spacing.half,
  },
  nombre: {
    fontSize: 15,
  },
  detalle: {
    fontSize: 13,
    lineHeight: 18,
  },
  grafico: {
    width: 72,
  },
});
