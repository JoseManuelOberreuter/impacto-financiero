/**
 * Below are the colors that are used in the app. The colors are defined in the light and dark mode.
 * There are many other ways to style your app. For example, [Nativewind](https://www.nativewind.dev/), [Tamagui](https://tamagui.dev/), [unistyles](https://reactnativeunistyles.vercel.app), etc.
 */

import '@/global.css';

import { Platform } from 'react-native';

export const Colors = {
  light: {
    text: '#0B1220',
    // Fondo de un solo tono azul, un poco más oscuro (propuesta G).
    background: '#D9E3F2',
    backgroundElement: '#FFFFFF',
    backgroundSelected: '#E6ECF2',
    textSecondary: '#5B636E',
    border: '#E2E6EB',
    accent: '#1F5FAD',
    onAccent: '#FFFFFF',
    // Estado de presión: siempre acompañado de texto, nunca solo color.
    presionBaja: '#1B7A5A',
    presionBajaFondo: '#E3F4EC',
    presionMedia: '#9A6200',
    presionMediaFondo: '#FDF1DC',
    presionAlta: '#B23A1E',
    presionAltaFondo: '#FBE7E1',
    avisoFondo: '#FFF8E1',
    avisoTexto: '#6B4E00',
    // Vidrio (fallback de Liquid Glass) y luces de fondo.
    vidrio: 'rgba(255,255,255,0.55)',
    vidrioSolido: 'rgba(255,255,255,0.88)',
    vidrioBorde: 'rgba(255,255,255,0.9)',
    ambiente1: '#5B8FE0',
    ambiente2: '#3F78D6',
    ambiente3: '#7FA6E8',
  },
  dark: {
    text: '#F2F4F7',
    background: '#06080C',
    backgroundElement: '#181C20',
    backgroundSelected: '#243039',
    textSecondary: '#A3ABB5',
    border: '#2A3036',
    accent: '#7EB2F0',
    onAccent: '#0E1114',
    presionBaja: '#5FCB9F',
    presionBajaFondo: '#14302A',
    presionMedia: '#F0B95C',
    presionMediaFondo: '#3A2C12',
    presionAlta: '#F08E73',
    presionAltaFondo: '#3D1E17',
    avisoFondo: '#2E2712',
    avisoTexto: '#F2D58A',
    vidrio: 'rgba(255,255,255,0.06)',
    vidrioSolido: 'rgba(28,32,40,0.92)',
    vidrioBorde: 'rgba(255,255,255,0.12)',
    ambiente1: '#1D4FA8',
    ambiente2: '#163E86',
    ambiente3: '#2A5DB8',
  },
} as const;

export type ThemeColor = keyof typeof Colors.light & keyof typeof Colors.dark;

export const Fonts = Platform.select({
  ios: {
    /** iOS `UIFontDescriptorSystemDesignDefault` */
    sans: 'system-ui',
    /** iOS `UIFontDescriptorSystemDesignSerif` */
    serif: 'ui-serif',
    /** iOS `UIFontDescriptorSystemDesignRounded` */
    rounded: 'ui-rounded',
    /** iOS `UIFontDescriptorSystemDesignMonospaced` */
    mono: 'ui-monospace',
  },
  default: {
    sans: 'normal',
    serif: 'serif',
    rounded: 'normal',
    mono: 'monospace',
  },
  web: {
    sans: 'var(--font-display)',
    serif: 'var(--font-serif)',
    rounded: 'var(--font-rounded)',
    mono: 'var(--font-mono)',
  },
});

export const Spacing = {
  half: 2,
  one: 4,
  two: 8,
  three: 16,
  four: 24,
  five: 32,
  six: 64,
} as const;

export const MaxContentWidth = 640;
