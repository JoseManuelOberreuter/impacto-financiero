import { DarkTheme, DefaultTheme, ThemeProvider } from 'expo-router';
import { StyleSheet, View } from 'react-native';

import AppTabs from '@/components/app-tabs';
import { AvisoEjemplo } from '@/components/aviso-ejemplo';
import { useColorScheme } from '@/hooks/use-color-scheme';
import { ProveedorTema } from '@/hooks/use-preferencia-tema';

export default function RootLayout() {
  return (
    <ProveedorTema>
      <Navegacion />
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
      </View>
    </ThemeProvider>
  );
}

const styles = StyleSheet.create({
  contenedor: {
    flex: 1,
  },
});
