import { Link } from 'expo-router';
import { ChevronRight } from 'lucide-react-native';
import { Pressable, StyleSheet, View } from 'react-native';

import type { Termometro } from '@/api/tipos';
import { Encabezado } from '@/components/encabezado';
import { IconoTermometro } from '@/components/icono-termometro';
import { NivelPresion } from '@/components/nivel-presion';
import { ContenidoApi, Pagina } from '@/components/pagina';
import { ThemedText } from '@/components/themed-text';
import { Vidrio } from '@/components/vidrio';
import { PRESION } from '@/constants/presion';
import { Spacing } from '@/constants/theme';
import { useApi } from '@/hooks/use-api';
import { useTheme } from '@/hooks/use-theme';
import { fechaCorta } from '@/utils/fechas';

export default function TermometrosScreen() {
  const { estado, recargar } = useApi<Termometro[]>('/termometros');

  return (
    <Pagina>
      <Encabezado
        titulo="Termómetros"
        bajada="Cada uno resume varios indicadores y los compara con lo habitual de los últimos años."
      />
      <ContenidoApi estado={estado} recargar={recargar}>
        {(termometros) => (
          <View style={styles.lista}>
            {termometros.map((t) => (
              <TarjetaTermometro key={t.id} termometro={t} />
            ))}
          </View>
        )}
      </ContenidoApi>
    </Pagina>
  );
}

function TarjetaTermometro({ termometro }: { termometro: Termometro }) {
  const theme = useTheme();
  const presion = PRESION[termometro.presion];

  return (
    <Link href={`/termometros/${termometro.id}`} asChild>
      <Pressable>
        <Vidrio style={styles.tarjeta}>
          <View style={styles.encabezado}>
            <View style={[styles.icono, { backgroundColor: theme[presion.fondo] }]}>
              <IconoTermometro id={termometro.id} size={20} color={theme[presion.color]} />
            </View>
            <View style={styles.titulos}>
              <ThemedText type="smallBold" style={styles.nombre}>
                {termometro.nombre}
              </ThemedText>
              <ThemedText type="small" themeColor="textSecondary">
                {termometro.pregunta}
              </ThemedText>
            </View>
            <ChevronRight size={18} color={theme.textSecondary} />
          </View>
          <NivelPresion
            presion={termometro.presion}
            tendencia={termometro.tendencia}
            etiqueta={termometro.etiqueta_presion}
          />
          <ThemedText style={styles.dato}>{termometro.dato_clave}</ThemedText>
          <ThemedText type="small">{termometro.frase}</ThemedText>
          <ThemedText type="small" themeColor="textSecondary" style={styles.pie}>
            Dato al {fechaCorta(termometro.dato_al)} · {termometro.fuentes.join(', ')}
          </ThemedText>
        </Vidrio>
      </Pressable>
    </Link>
  );
}

const styles = StyleSheet.create({
  lista: {
    gap: Spacing.three,
  },
  tarjeta: {
    padding: Spacing.four,
    gap: Spacing.two,
  },
  encabezado: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: Spacing.three,
    marginBottom: Spacing.one,
  },
  icono: {
    width: 40,
    height: 40,
    borderRadius: 20,
    alignItems: 'center',
    justifyContent: 'center',
  },
  titulos: {
    flex: 1,
  },
  nombre: {
    fontSize: 17,
  },
  dato: {
    fontSize: 20,
    lineHeight: 28,
    fontWeight: 700,
  },
  pie: {
    fontSize: 12,
  },
});
