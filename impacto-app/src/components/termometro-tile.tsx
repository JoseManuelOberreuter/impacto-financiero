import { Link } from 'expo-router';
import { Pressable, StyleSheet, View } from 'react-native';

import type { Termometro } from '@/api/tipos';
import { IconoTermometro } from '@/components/icono-termometro';
import { ThemedText } from '@/components/themed-text';
import { Vidrio } from '@/components/vidrio';
import { COLOR_DIRECCION, TENDENCIA } from '@/constants/presion';
import { Spacing } from '@/constants/theme';
import { useTheme } from '@/hooks/use-theme';

/** Versión compacta del termómetro para el home: ícono, nombre, flecha y dato clave. */
export function TermometroTile({ termometro }: { termometro: Termometro }) {
  const theme = useTheme();
  const tendencia = TENDENCIA[termometro.tendencia];
  const IconoTendencia = tendencia.icono;

  return (
    <Link href={`/termometros/${termometro.id}`} asChild>
      <Pressable
        style={styles.enlace}
        accessibilityLabel={`${termometro.nombre}: ${termometro.dato_clave}, ${tendencia.texto}`}>
        <Vidrio style={styles.tile}>
          <View style={[styles.icono, { backgroundColor: theme.backgroundSelected }]}>
            <IconoTermometro
              id={termometro.id}
              size={18}
              color={theme.accent}
              strokeWidth={2}
            />
          </View>
          <ThemedText type="smallBold" numberOfLines={2} style={styles.nombre}>
            {termometro.nombre}
          </ThemedText>
          <View style={styles.nivel}>
            <IconoTendencia size={14} color={theme[COLOR_DIRECCION[termometro.tendencia]]} strokeWidth={2.5} />
            <ThemedText type="small" themeColor="textSecondary" numberOfLines={2} style={styles.estado}>
              {termometro.dato_clave}
            </ThemedText>
          </View>
        </Vidrio>
      </Pressable>
    </Link>
  );
}

const styles = StyleSheet.create({
  enlace: {
    flexGrow: 1,
    flexBasis: '40%',
  },
  tile: {
    padding: Spacing.three,
    gap: Spacing.two,
  },
  icono: {
    width: 34,
    height: 34,
    borderRadius: 17,
    alignItems: 'center',
    justifyContent: 'center',
  },
  nombre: {
    minHeight: 40,
  },
  nivel: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    gap: Spacing.one,
  },
  estado: {
    flex: 1,
    fontSize: 13,
    lineHeight: 17,
  },
});
