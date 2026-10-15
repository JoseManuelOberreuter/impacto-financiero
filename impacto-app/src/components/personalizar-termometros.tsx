import { Pressable, StyleSheet, View } from 'react-native';

import type { Termometro } from '@/api/tipos';
import { ThemedText } from '@/components/themed-text';
import { ThemedView } from '@/components/themed-view';
import { Spacing } from '@/constants/theme';
import { useTheme } from '@/hooks/use-theme';

type Props = {
  termometros: Termometro[];
  seleccionados: string[];
  maximo: number;
  onCambiar: (ids: string[]) => void;
  onCerrar: () => void;
};

// El orden de selección define el orden en el home.
export function PersonalizarTermometros({
  termometros,
  seleccionados,
  maximo,
  onCambiar,
  onCerrar,
}: Props) {
  const theme = useTheme();

  function alternar(id: string) {
    if (seleccionados.includes(id)) {
      onCambiar(seleccionados.filter((s) => s !== id));
    } else if (seleccionados.length < maximo) {
      onCambiar([...seleccionados, id]);
    }
  }

  return (
    <ThemedView
      type="backgroundElement"
      style={[styles.panel, { borderColor: theme.border }]}>
      <ThemedText type="smallBold">
        Elige hasta {maximo} termómetros ({seleccionados.length}/{maximo})
      </ThemedText>
      <ThemedText type="small" themeColor="textSecondary">
        Aparecen en el orden en que los elijas.
      </ThemedText>

      <View style={styles.lista}>
        {termometros.map((t) => {
          const posicion = seleccionados.indexOf(t.id);
          const activo = posicion >= 0;
          const bloqueado = !activo && seleccionados.length >= maximo;
          return (
            <Pressable
              key={t.id}
              onPress={() => alternar(t.id)}
              disabled={bloqueado}
              role="checkbox"
              aria-checked={activo}
              aria-disabled={bloqueado}
              style={({ pressed }) => [pressed && styles.presionado, bloqueado && styles.bloqueado]}>
              <ThemedView
                type={activo ? 'backgroundSelected' : 'background'}
                style={[styles.opcion, { borderColor: activo ? theme.accent : theme.border }]}>
                <ThemedText type="smallBold" themeColor={activo ? 'accent' : 'textSecondary'}>
                  {activo ? posicion + 1 : '○'}
                </ThemedText>
                <View style={styles.textoOpcion}>
                  <ThemedText type="smallBold">
                    {t.icono} {t.nombre}
                  </ThemedText>
                  <ThemedText type="small" themeColor="textSecondary">
                    {t.pregunta}
                  </ThemedText>
                </View>
              </ThemedView>
            </Pressable>
          );
        })}
      </View>

      <Pressable
        onPress={onCerrar}
        accessibilityRole="button"
        style={({ pressed }) => [
          styles.listo,
          { backgroundColor: theme.accent },
          pressed && styles.presionado,
        ]}>
        <ThemedText type="smallBold" themeColor="onAccent">
          Listo
        </ThemedText>
      </Pressable>
      <ThemedText type="small" themeColor="textSecondary" style={styles.nota}>
        Por ahora tu elección no se guarda al recargar.
      </ThemedText>
    </ThemedView>
  );
}

const styles = StyleSheet.create({
  panel: {
    borderWidth: 1,
    borderRadius: Spacing.three,
    padding: Spacing.three,
    gap: Spacing.two,
  },
  lista: {
    gap: Spacing.two,
    marginTop: Spacing.one,
  },
  opcion: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: Spacing.three,
    borderWidth: 1,
    borderRadius: Spacing.two,
    paddingHorizontal: Spacing.three,
    paddingVertical: Spacing.two,
  },
  textoOpcion: {
    flex: 1,
  },
  listo: {
    alignItems: 'center',
    paddingVertical: Spacing.two,
    borderRadius: Spacing.four,
    marginTop: Spacing.one,
  },
  nota: {
    fontSize: 12,
    textAlign: 'center',
  },
  presionado: {
    opacity: 0.7,
  },
  bloqueado: {
    opacity: 0.45,
  },
});
