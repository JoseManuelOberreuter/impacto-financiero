import type { ReactNode } from 'react';
import { ActivityIndicator, Pressable, ScrollView, StyleSheet, View } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';

import { FondoAmbiente } from '@/components/fondo-ambiente';
import { ThemedText } from '@/components/themed-text';
import { MaxContentWidth, Spacing } from '@/constants/theme';
import type { EstadoCarga } from '@/hooks/use-api';
import { useDiseno } from '@/hooks/use-diseno';
import { useTheme } from '@/hooks/use-theme';

/** Estructura común de todas las pantallas: fondo con luces, scroll y columna centrada. */
export function Pagina({ children }: { children: ReactNode }) {
  const { espacioArriba, espacioAbajo } = useDiseno();

  return (
    <View style={styles.contenedor}>
      <FondoAmbiente />
      <SafeAreaView style={styles.contenedor} edges={['top', 'left', 'right']}>
        <ScrollView
          contentInsetAdjustmentBehavior="automatic"
          contentContainerStyle={[
            styles.scroll,
            { paddingTop: Spacing.three + espacioArriba, paddingBottom: Spacing.six + espacioAbajo },
          ]}>
          <View style={styles.columna}>{children}</View>
        </ScrollView>
      </SafeAreaView>
    </View>
  );
}

type PropsContenido<T> = {
  estado: EstadoCarga<T>;
  recargar: () => void;
  children: (datos: T) => ReactNode;
};

/** Muestra el indicador de carga, el error con "Reintentar" o el contenido. */
export function ContenidoApi<T>({ estado, recargar, children }: PropsContenido<T>) {
  const theme = useTheme();

  if (estado.tipo === 'cargando') {
    return <ActivityIndicator style={styles.centro} />;
  }
  if (estado.tipo === 'error') {
    return (
      <View style={styles.centro}>
        <ThemedText type="smallBold">No pudimos cargar los datos</ThemedText>
        <ThemedText type="small" themeColor="textSecondary" style={styles.textoCentro}>
          {estado.mensaje}. ¿Está corriendo impacto-api?
        </ThemedText>
        <Pressable
          onPress={recargar}
          accessibilityRole="button"
          style={({ pressed }) => [
            styles.reintentar,
            { backgroundColor: theme.accent },
            pressed && styles.presionado,
          ]}>
          <ThemedText type="smallBold" themeColor="onAccent">
            Reintentar
          </ThemedText>
        </Pressable>
      </View>
    );
  }
  return <>{children(estado.datos)}</>;
}

const styles = StyleSheet.create({
  contenedor: {
    flex: 1,
  },
  scroll: {
    flexGrow: 1,
    alignItems: 'center',
    // Margen lateral de 20 px, igual que los diseños de Figma.
    paddingHorizontal: Spacing.three + Spacing.one,
  },
  columna: {
    width: '100%',
    maxWidth: MaxContentWidth,
    gap: Spacing.four,
  },
  centro: {
    alignItems: 'center',
    gap: Spacing.two,
    marginTop: Spacing.six,
  },
  textoCentro: {
    textAlign: 'center',
  },
  reintentar: {
    paddingHorizontal: Spacing.four,
    paddingVertical: Spacing.two,
    borderRadius: Spacing.four,
  },
  presionado: {
    opacity: 0.7,
  },
});
