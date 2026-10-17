import { DarkTheme, DefaultTheme, ThemeProvider } from 'expo-router';
import { StyleSheet, View } from 'react-native';

import AppTabs from '@/components/app-tabs';
import { AvisoEjemplo } from '@/components/aviso-ejemplo';
import { SelectorPais } from '@/components/selector-pais';
import { ProveedorCapacidades } from '@/hooks/use-capacidades';
import { useColorScheme } from '@/hooks/use-color-scheme';
import { ProveedorTema } from '@/hooks/use-preferencia-tema';

export default function RootLayout() {
  return (
    <ProveedorTema>
      <ProveedorCapacidades>
        <Navegacion />
      </ProveedorCapacidades>
    </ProveedorTema>
  );
}

function Navegacion() {
  const colorScheme = useColorScheme();
  return (
    <ThemeProvider value={colorScheme === 'dark' ? DarkTheme : DefaultTheme}>
      <View style={styles.contenedor}>
        <AppTabs />
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
