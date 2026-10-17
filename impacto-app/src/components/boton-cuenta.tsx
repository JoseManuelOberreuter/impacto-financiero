import { router } from 'expo-router';
import { User } from 'lucide-react-native';
import { Pressable, StyleSheet } from 'react-native';

import { ThemedText } from '@/components/themed-text';
import { useSesion } from '@/hooks/use-sesion';
import { useTheme } from '@/hooks/use-theme';

/**
 * Burbuja de cuenta junto a la bandera, arriba a la derecha. Sin sesión muestra un ícono;
 * con sesión, la inicial del nombre o del correo. Abre Mi cuenta.
 */
export function BotonCuenta() {
  const theme = useTheme();
  const { disponible, sesion } = useSesion();
  if (!disponible) return null;

  const nombre = (sesion?.user.user_metadata?.nombre as string | undefined) ?? sesion?.user.email ?? '';
  const inicial = nombre.trim().charAt(0).toUpperCase();

  return (
    <Pressable
      onPress={() => router.push('/cuenta')}
      accessibilityRole="button"
      accessibilityLabel={sesion ? 'Mi cuenta' : 'Crear cuenta o iniciar sesión'}
      hitSlop={6}
      style={({ pressed }) => [
        styles.burbuja,
        {
          backgroundColor: sesion ? theme.accent : theme.backgroundSelected,
          borderColor: theme.border,
          opacity: pressed ? 0.8 : 1,
        },
      ]}>
      {sesion && inicial ? (
        <ThemedText type="smallBold" style={{ color: theme.onAccent }}>
          {inicial}
        </ThemedText>
      ) : (
        <User size={16} color={theme.text} strokeWidth={2} />
      )}
    </Pressable>
  );
}

const styles = StyleSheet.create({
  burbuja: {
    width: 30,
    height: 30,
    borderRadius: 15,
    borderWidth: StyleSheet.hairlineWidth,
    alignItems: 'center',
    justifyContent: 'center',
  },
});
