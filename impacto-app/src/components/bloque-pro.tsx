import { Lock } from 'lucide-react-native';
import { StyleSheet, View } from 'react-native';

import type { Plan } from '@/api/tipos';
import { ThemedText } from '@/components/themed-text';
import { Vidrio } from '@/components/vidrio';
import { Spacing } from '@/constants/theme';
import { useTheme } from '@/hooks/use-theme';

const NOMBRE_PLAN: Record<Plan, string> = { gratis: 'Gratis', pro: 'Pro', empresas: 'Empresas' };

/** Lo que se muestra en lugar de una función que el plan del usuario no incluye. */
export function BloquePro({ plan, descripcion }: { plan: Plan; descripcion?: string }) {
  const theme = useTheme();

  return (
    <Vidrio style={styles.tarjeta}>
      <View style={[styles.icono, { backgroundColor: theme.backgroundSelected }]}>
        <Lock size={18} color={theme.accent} strokeWidth={2} />
      </View>
      <View style={styles.texto}>
        <ThemedText type="smallBold">Disponible en {NOMBRE_PLAN[plan]}</ThemedText>
        {descripcion && (
          <ThemedText type="small" themeColor="textSecondary">
            {descripcion}
          </ThemedText>
        )}
      </View>
    </Vidrio>
  );
}

/** Etiqueta pequeña "Pro" para el modo vista previa. */
export function EtiquetaPlan({ plan }: { plan: Plan }) {
  const theme = useTheme();

  return (
    <View style={[styles.etiqueta, { backgroundColor: theme.backgroundSelected }]}>
      <ThemedText type="small" style={[styles.textoEtiqueta, { color: theme.accent }]}>
        {NOMBRE_PLAN[plan]}
      </ThemedText>
    </View>
  );
}

const styles = StyleSheet.create({
  tarjeta: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: Spacing.three,
    padding: Spacing.four,
  },
  icono: {
    width: 36,
    height: 36,
    borderRadius: 18,
    alignItems: 'center',
    justifyContent: 'center',
  },
  texto: {
    flex: 1,
    gap: Spacing.half,
  },
  etiqueta: {
    alignSelf: 'flex-start',
    paddingHorizontal: Spacing.two,
    paddingVertical: Spacing.half,
    borderRadius: Spacing.two,
  },
  textoEtiqueta: {
    fontSize: 12,
    lineHeight: 16,
  },
});
