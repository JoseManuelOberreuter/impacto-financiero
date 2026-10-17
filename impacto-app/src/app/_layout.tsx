import { DarkTheme, DefaultTheme, Stack, ThemeProvider } from 'expo-router';
import { StyleSheet, View } from 'react-native';

import { AvisoEjemplo } from '@/components/aviso-ejemplo';
import { SelectorPais } from '@/components/selector-pais';
import { ProveedorAnclados } from '@/hooks/use-anclados';
import { ProveedorCapacidades } from '@/hooks/use-capacidades';
import { useColorScheme } from '@/hooks/use-color-scheme';
import { ProveedorTema } from '@/hooks/use-preferencia-tema';
import { ProveedorSesion } from '@/hooks/use-sesion';

export default function RootLayout() {
  return (
    <ProveedorTema>
      <ProveedorSesion>
        <ProveedorCapacidades>
          <ProveedorAnclados>
            <Navegacion />
          </ProveedorAnclados>
        </ProveedorCapacidades>
      </ProveedorSesion>
    </ProveedorTema>
  );
}

function Navegacion() {
  const colorScheme = useColorScheme();
  return (
    <ThemeProvider value={colorScheme === 'dark' ? DarkTheme : DefaultTheme}>
      <View style={styles.contenedor}>
        {/* Las pestañas van en (tabs); Mi cuenta (/cuenta) se abre encima, fuera de ellas. */}
        <Stack screenOptions={{ headerShown: false }} />
        <AvisoEjemplo />
        <SelectorPais />
      </View>
    </ThemeProvider>
  );
}

const styles = StyleSheet.create({
  contenedor: {
    flex: 1,
  },
});
