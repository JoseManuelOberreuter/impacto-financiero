import { NativeTabs } from 'expo-router/unstable-native-tabs';

import { useTheme } from '@/hooks/use-theme';

/**
 * Menú en iPhone y Android: barra de pestañas nativa. En iOS 26 usa Liquid Glass.
 * Los íconos son SF Symbols (iOS) y Material Symbols (Android).
 */
export default function AppTabs() {
  const theme = useTheme();

  return (
    <NativeTabs tintColor={theme.accent}>
      <NativeTabs.Trigger name="index">
        <NativeTabs.Trigger.Label>Inicio</NativeTabs.Trigger.Label>
        <NativeTabs.Trigger.Icon sf="house" md="home" />
      </NativeTabs.Trigger>
      <NativeTabs.Trigger name="termometros">
        <NativeTabs.Trigger.Label>Termómetros</NativeTabs.Trigger.Label>
        <NativeTabs.Trigger.Icon sf="thermometer.medium" md="thermostat" />
      </NativeTabs.Trigger>
      <NativeTabs.Trigger name="precios">
        <NativeTabs.Trigger.Label>Precios</NativeTabs.Trigger.Label>
        <NativeTabs.Trigger.Icon sf="cart" md="shopping_cart" />
      </NativeTabs.Trigger>
      <NativeTabs.Trigger name="noticias">
        <NativeTabs.Trigger.Label>Noticias</NativeTabs.Trigger.Label>
        <NativeTabs.Trigger.Icon sf="newspaper" md="newspaper" />
      </NativeTabs.Trigger>
      <NativeTabs.Trigger name="herramientas">
        <NativeTabs.Trigger.Label>Herramientas</NativeTabs.Trigger.Label>
        <NativeTabs.Trigger.Icon sf="wrench.and.screwdriver" md="build" />
      </NativeTabs.Trigger>
    </NativeTabs>
  );
}
