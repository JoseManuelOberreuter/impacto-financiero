import { Slot } from 'expo-router';
import { StyleSheet, View } from 'react-native';

import { MenuSuelto } from '@/components/menu-web';

/** En web, los textos legales muestran el mismo menú que las secciones, aunque estén fuera de ellas. */
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
