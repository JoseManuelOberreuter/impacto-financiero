import { Link } from 'expo-router';
import { Pressable, StyleSheet, View } from 'react-native';

import type { Termometro } from '@/api/tipos';
import { IconoTermometro } from '@/components/icono-termometro';
import { ThemedText } from '@/components/themed-text';
import { Vidrio } from '@/components/vidrio';
import { PRESION, TENDENCIA } from '@/constants/presion';
import { Spacing } from '@/constants/theme';
import { useTheme } from '@/hooks/use-theme';

/** Versión compacta del termómetro para el home: ícono, nombre y nivel de presión. */
export function TermometroTile({ termometro }: { termometro: Termometro }) {
  const theme = useTheme();
  const presion = PRESION[termometro.presion];
  const tendencia = TENDENCIA[termometro.tendencia];
  const IconoTendencia = tendencia.icono;

  return (
    <Link href={`/termometros/${termometro.id}`} asChild>
      <Pressable
        style={styles.enlace}
        accessibilityLabel={`${termometro.nombre}: ${termometro.etiqueta_presion}, tendencia ${tendencia.texto}`}>
        <Vidrio style={styles.tile}>
          <View style={[styles.icono, { backgroundColor: theme[presion.fondo] }]}>
            <IconoTermometro
              id={termometro.id}
              size={18}
              color={theme[presion.color]}
              strokeWidth={2}
            />
          </View>
          <ThemedText type="smallBold" numberOfLines={2} style={styles.nombre}>
            {termometro.nombre}
          </ThemedText>
          <View style={styles.nivel}>
            <ThemedText type="small" themeColor="textSecondary">
              Presión
            </ThemedText>
            <ThemedText type="smallBold" themeColor={presion.color}>
              {presion.texto}
            </ThemedText>
            <IconoTendencia size={14} color={theme[presion.color]} strokeWidth={2.5} />
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
    alignItems: 'center',
    gap: Spacing.one,
  },
});
