import { Stack } from 'expo-router';

/** Los textos legales se abren encima de las pestañas (en web, _layout.web.tsx les agrega el menú). */
export default function Layout() {
  return <Stack screenOptions={{ headerShown: false }} />;
}
