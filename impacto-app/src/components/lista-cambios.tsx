import { Link, type Href } from 'expo-router';
import { ArrowDownRight, ArrowUpRight, Minus, Pin, type LucideIcon } from 'lucide-react-native';
import { Pressable, StyleSheet, View } from 'react-native';

import type { CambioSemana, Tendencia } from '@/api/tipos';
import { MiniGrafico } from '@/components/mini-grafico';
import { ThemedText } from '@/components/themed-text';
import { Vidrio } from '@/components/vidrio';
import { COLOR_DIRECCION, FONDO_DIRECCION } from '@/constants/presion';
import { Spacing } from '@/constants/theme';
import { useAnclados } from '@/hooks/use-anclados';
import { useTheme } from '@/hooks/use-theme';

const FLECHA: Record<Tendencia, LucideIcon> = {
  sube: ArrowUpRight,
  baja: ArrowDownRight,
  estable: Minus,
};

type Props = {
  cambios: CambioSemana[];
  /** Muestra el botón para anclar o desanclar cada dato ("Todos los datos"). */
  anclable?: boolean;
  /** Se llama cuando no se pudo anclar por el límite del plan. */
  onLimite?: () => void;
};

/** Lista de datos: flecha, nombre, detalle, mini gráfico y si está sobre o bajo lo normal. */
export function ListaCambios({ cambios, anclable, onLimite }: Props) {
  const theme = useTheme();

  return (
    <Vidrio style={styles.lista}>
      {cambios.map((cambio, i) => (
        <FilaCambio
          key={cambio.id}
          cambio={cambio}
          anclable={anclable}
          onLimite={onLimite}
          divisor={i < cambios.length - 1 ? theme.border : undefined}
        />
      ))}
    </Vidrio>
  );
}

function FilaCambio({
  cambio,
  divisor,
  anclable,
  onLimite,
}: {
  cambio: CambioSemana;
  divisor?: string;
  anclable?: boolean;
  onLimite?: () => void;
}) {
  const theme = useTheme();
  const { estaAnclado, alternar } = useAnclados();
  const anclado = estaAnclado(cambio.id);
  // Flecha y gráfico como en cualquier app de activos: sube verde, baja rojo, sin cambio gris.
  const color = COLOR_DIRECCION[cambio.direccion];
  const fondo = FONDO_DIRECCION[cambio.direccion];
  const Flecha = FLECHA[cambio.direccion];

  return (
    <View
      style={[
        styles.fila,
        divisor && { borderBottomColor: divisor, borderBottomWidth: StyleSheet.hairlineWidth },
      ]}>
      {/* Link asChild exige un estilo plano en el Pressable: el diseño va en la vista interior. */}
      <Link href={cambio.enlace as Href} asChild>
        <Pressable accessibilityLabel={`${cambio.nombre}: ${cambio.detalle}`} style={styles.enlace}>
          <View style={styles.contenido}>
            <View style={[styles.icono, { backgroundColor: theme[fondo] }]}>
              <Flecha size={17} color={theme[color]} strokeWidth={2.25} />
            </View>
            <View style={styles.textos}>
              <View style={styles.titulo}>
                <ThemedText type="smallBold" style={styles.nombre}>
                  {cambio.nombre}
                </ThemedText>
                {anclado && !anclable && (
                  <Pin size={12} color={theme.textSecondary} strokeWidth={2} accessibilityLabel="Anclado" />
                )}
              </View>
              <ThemedText type="small" themeColor="textSecondary" style={styles.detalle}>
                {cambio.detalle}
              </ThemedText>
            </View>
            <View style={styles.derecha}>
              {/* El gráfico toma el ancho de su contenedor: con alignItems flex-end quedaría en 0. */}
              <View style={styles.grafico}>
                <MiniGrafico valores={cambio.serie} color={theme[color]} alto={26} />
              </View>
              {/* Comparado con los últimos 5 años, en palabras ("Más cara que lo normal"). */}
              <ThemedText type="small" themeColor="textSecondary" style={styles.presion} numberOfLines={2}>
                {cambio.estado}
              </ThemedText>
            </View>
          </View>
        </Pressable>
      </Link>
      {anclable && (
        <Pressable
          onPress={() => {
            if (!alternar(cambio.id)) onLimite?.();
          }}
          accessibilityRole="button"
          accessibilityLabel={anclado ? `Desanclar ${cambio.nombre}` : `Anclar ${cambio.nombre} en el Inicio`}
          accessibilityState={{ selected: anclado }}
          hitSlop={8}
          style={styles.pin}>
          <Pin
            size={18}
            color={anclado ? theme.accent : theme.textSecondary}
            fill={anclado ? theme.accent : 'transparent'}
            strokeWidth={2}
          />
        </Pressable>
      )}
    </View>
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
    gap: Spacing.two,
  },
  enlace: {
    flex: 1,
  },
  contenido: {
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
  titulo: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: Spacing.one,
  },
  nombre: {
    fontSize: 15,
  },
  detalle: {
    fontSize: 13,
    lineHeight: 18,
  },
  derecha: {
    width: 96,
    alignItems: 'flex-end',
    gap: Spacing.half,
  },
  grafico: {
    alignSelf: 'stretch',
  },
  presion: {
    fontSize: 11,
    lineHeight: 14,
    textAlign: 'right',
  },
  pin: {
    padding: Spacing.one,
  },
});
