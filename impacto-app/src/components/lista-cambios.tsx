import { Link, type Href } from 'expo-router';
import { ArrowDownRight, ArrowUpRight, Minus, Pin, type LucideIcon } from 'lucide-react-native';
import { Pressable, StyleSheet, View } from 'react-native';

import type { CambioSemana, Tendencia } from '@/api/tipos';
import { MiniGrafico } from '@/components/mini-grafico';
import { ThemedText } from '@/components/themed-text';
import { Vidrio } from '@/components/vidrio';
import { PRESION } from '@/constants/presion';
import { Spacing, type ThemeColor } from '@/constants/theme';
import { useAnclados } from '@/hooks/use-anclados';
import { useTheme } from '@/hooks/use-theme';

const FLECHA: Record<Tendencia, LucideIcon> = {
  sube: ArrowUpRight,
  baja: ArrowDownRight,
  estable: Minus,
};

// La flecha dice si el movimiento conviene al bolsillo (verde), no conviene (rojo) o depende (gris).
// La presión va aparte, escrita: "bajó, pero sigue cara" se lee como ↘ verde + "Presión alta".
const TONO: Record<CambioSemana['tono'], { color: ThemeColor; fondo: ThemeColor }> = {
  favorable: { color: 'presionBaja', fondo: 'presionBajaFondo' },
  desfavorable: { color: 'presionAlta', fondo: 'presionAltaFondo' },
  neutral: { color: 'textSecondary', fondo: 'backgroundSelected' },
};

type Props = {
  cambios: CambioSemana[];
  /** Muestra el botón para anclar o desanclar cada dato y la presión escrita ("Todos los datos"). */
  anclable?: boolean;
  /** Se llama cuando no se pudo anclar por el límite del plan. */
  onLimite?: () => void;
};

/** Lista de datos: flecha, nombre, detalle y mini gráfico por fila (y la presión en la lista completa). */
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
  const tono = TONO[cambio.tono];
  const presion = PRESION[cambio.presion];
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
            <View style={[styles.icono, { backgroundColor: theme[tono.fondo] }]}>
              <Flecha size={17} color={theme[tono.color]} strokeWidth={2.25} />
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
                <MiniGrafico valores={cambio.serie} color={theme.accent} alto={26} />
              </View>
              {/* En el Inicio casi todos tienen presión alta: la etiqueta solo aporta en la lista completa. */}
              {anclable && (
                <ThemedText type="small" style={[styles.presion, { color: theme[presion.color] }]}>
                  Presión {presion.texto.toLowerCase()}
                </ThemedText>
              )}
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
    width: 76,
    alignItems: 'flex-end',
    gap: Spacing.half,
  },
  grafico: {
    alignSelf: 'stretch',
  },
  presion: {
    fontSize: 11,
    lineHeight: 14,
  },
  pin: {
    padding: Spacing.one,
  },
});
