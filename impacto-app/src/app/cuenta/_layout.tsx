import { Stack } from 'expo-router';

/** Mi cuenta se abre encima de las pestañas (en web, _layout.web.tsx le agrega el menú). */
export default function Layout() {
  return <Stack screenOptions={{ headerShown: false }} />;
}
