import { StyleSheet, View } from 'react-native';

import type { Presion, Tendencia, Termometro } from '@/api/tipos';
import { ThemedText } from '@/components/themed-text';
import { ThemedView } from '@/components/themed-view';
import { Spacing, type ThemeColor } from '@/constants/theme';
import { useTheme } from '@/hooks/use-theme';
import { fechaCorta } from '@/utils/fechas';

const COLOR_PRESION: Record<Presion, { texto: ThemeColor; fondo: ThemeColor }> = {
  baja: { texto: 'presionBaja', fondo: 'presionBajaFondo' },
  media: { texto: 'presionMedia', fondo: 'presionMediaFondo' },
  alta: { texto: 'presionAlta', fondo: 'presionAltaFondo' },
};

const TENDENCIA: Record<Tendencia, { simbolo: string; texto: string }> = {
  sube: { simbolo: '▲', texto: 'sube' },
  baja: { simbolo: '▼', texto: 'baja' },
  estable: { simbolo: '●', texto: 'estable' },
};

export function TermometroCard({ termometro }: { termometro: Termometro }) {
  const theme = useTheme();
  const colores = COLOR_PRESION[termometro.presion];
  const tendencia = TENDENCIA[termometro.tendencia];

  return (
    <ThemedView
      type="backgroundElement"
      style={[styles.card, { borderColor: theme.border }]}
      accessibilityLabel={`${termometro.nombre}: ${termometro.etiqueta_presion}, tendencia ${tendencia.texto}. ${termometro.dato_clave}. ${termometro.frase}`}>
      <View style={styles.encabezado}>
        <ThemedText type="smallBold" style={styles.nombre}>
          {termometro.icono} {termometro.nombre}
        </ThemedText>
        <View style={[styles.estado, { backgroundColor: theme[colores.fondo] }]}>
          <ThemedText type="smallBold" themeColor={colores.texto}>
            {termometro.etiqueta_presion} {tendencia.simbolo}
          </ThemedText>
        </View>
      </View>

      <ThemedText type="small" themeColor="textSecondary">
        {termometro.pregunta}
      </ThemedText>

      <ThemedText style={styles.dato}>{termometro.dato_clave}</ThemedText>
      <ThemedText type="small">“{termometro.frase}”</ThemedText>

      <ThemedText type="small" themeColor="textSecondary" style={styles.pie}>
        Dato al {fechaCorta(termometro.dato_al)}
        {termometro.proxima_actualizacion &&
          ` · próxima actualización ${fechaCorta(termometro.proxima_actualizacion)}`}
        {'\n'}Fuente: {termometro.fuentes.join(', ')}
      </ThemedText>
    </ThemedView>
  );
}

const styles = StyleSheet.create({
  card: {
    borderWidth: 1,
    borderRadius: Spacing.three,
    padding: Spacing.three,
    gap: Spacing.one,
  },
  encabezado: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    flexWrap: 'wrap',
    gap: Spacing.two,
  },
  nombre: {
    fontSize: 16,
  },
  estado: {
    paddingHorizontal: Spacing.two,
    paddingVertical: Spacing.half,
    borderRadius: Spacing.two,
  },
  dato: {
    fontSize: 20,
    lineHeight: 28,
    fontWeight: 700,
    marginTop: Spacing.one,
  },
  pie: {
    marginTop: Spacing.two,
    fontSize: 12,
    lineHeight: 18,
  },
});
