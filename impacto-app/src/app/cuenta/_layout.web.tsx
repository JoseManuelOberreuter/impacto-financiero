import { Slot } from 'expo-router';
import { StyleSheet, View } from 'react-native';

import { MenuSuelto } from '@/components/menu-web';

/** En web, Mi cuenta muestra el mismo menú que las secciones, aunque esté fuera de ellas. */
export default function Layout() {
  return (
    <View style={styles.contenedor}>
      <Slot />
      <MenuSuelto />
    </View>
  );
}

const styles = StyleSheet.create({
  contenedor: {
    flex: 1,
  },
});
