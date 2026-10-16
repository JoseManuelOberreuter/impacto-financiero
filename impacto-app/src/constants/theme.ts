/**
 * Below are the colors that are used in the app. The colors are defined in the light and dark mode.
 * There are many other ways to style your app. For example, [Nativewind](https://www.nativewind.dev/), [Tamagui](https://tamagui.dev/), [unistyles](https://reactnativeunistyles.vercel.app), etc.
 */

import '@/global.css';

import { Platform } from 'react-native';

// Colores que no cambian entre paletas de fondo.
const COMUN_CLARO = {
  backgroundElement: '#FFFFFF',
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
  // Vidrio (fallback de Liquid Glass).
  vidrio: 'rgba(255,255,255,0.55)',
  vidrioSolido: 'rgba(255,255,255,0.88)',
  vidrioBorde: 'rgba(255,255,255,0.9)',
} as const;

const COMUN_OSCURO = {
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
  vidrioBorde: 'rgba(255,255,255,0.12)',
} as const;

// Paletas de fondo, cada una con su versión clara y oscura.
const PALETAS = {
  // Mezcla la confianza del azul con el crecimiento del verde.
  verdeAzulado: {
    light: {
      ...COMUN_CLARO,
      text: '#0E1B18',
      background: '#DCEBE7',
      backgroundSelected: '#D2E3DE',
      textSecondary: '#55635F',
      border: '#D5E2DE',
      // Más marcado: sobre el fondo verde azulado un verde pálido se pierde.
      presionBajaFondo: '#C4E8D5',
      ambiente1: '#8CC3B3',
      ambiente2: '#5FA894',
      ambiente3: '#A9D3C6',
    },
    dark: {
      ...COMUN_OSCURO,
      text: '#EEF4F2',
      background: '#05110E',
      backgroundElement: '#10201C',
      backgroundSelected: '#1A3530',
      textSecondary: '#A2B5AF',
      border: '#22392F',
      presionBajaFondo: '#1B4A3A',
      vidrioSolido: 'rgba(16,34,30,0.92)',
      ambiente1: '#0F6B57',
      ambiente2: '#0B4F42',
      ambiente3: '#1B7D68',
    },
  },
  // Gris piedra con un toque frío y verdoso: sobrio, sin la calidez "de libro".
  piedraFresca: {
    light: {
      ...COMUN_CLARO,
      text: '#15181A',
      // Base un poco más clara y luces más marcadas para que el fondo tenga profundidad.
      background: '#EEEFEA',
      backgroundSelected: '#DCDED8',
      textSecondary: '#5B6061',
      border: '#D9DBD4',
      presionBajaFondo: '#D5EEDF',
      ambiente1: '#7F927E',
      ambiente2: '#5F7463',
      ambiente3: '#8BA29B',
    },
    dark: {
      ...COMUN_OSCURO,
      text: '#F0F2EF',
      background: '#0C0E0D',
      backgroundElement: '#181B19',
      backgroundSelected: '#252925',
      textSecondary: '#ABB0AB',
      border: '#2B2F2B',
      presionBajaFondo: '#16342B',
      vidrioSolido: 'rgba(26,29,27,0.92)',
      ambiente1: '#3B4239',
      ambiente2: '#2D332C',
      ambiente3: '#4A5246',
    },
  },
  // Gris crema cálido (la piedra original), con manchas tan marcadas como piedra fresca.
  piedraCalida: {
    light: {
      ...COMUN_CLARO,
      text: '#1A1712',
      background: '#EFEBE4',
      backgroundSelected: '#E4DED4',
      textSecondary: '#625D55',
      border: '#E2DCD2',
      ambiente1: '#8E7858',
      ambiente2: '#6E5A3F',
      ambiente3: '#A08A6B',
    },
    dark: {
      ...COMUN_OSCURO,
      text: '#F2EFEA',
      background: '#0E0D0B',
      backgroundElement: '#1B1916',
      backgroundSelected: '#29261F',
      textSecondary: '#B0AAA0',
      border: '#2E2B25',
      presionBajaFondo: '#16342B',
      vidrioSolido: 'rgba(29,26,22,0.92)',
      ambiente1: '#6E5A40',
      ambiente2: '#56462F',
      ambiente3: '#806A4B',
    },
  },
  // Azul grisáceo: serio y financiero, sin el azul típico de banco.
  pizarra: {
    light: {
      ...COMUN_CLARO,
      text: '#111723',
      background: '#E8ECF2',
      backgroundSelected: '#DAE0EA',
      textSecondary: '#56607A',
      border: '#D7DDE8',
      ambiente1: '#7D8FB0',
      ambiente2: '#5D7096',
      ambiente3: '#98A8C4',
    },
    dark: {
      ...COMUN_OSCURO,
      text: '#EEF1F6',
      background: '#0A0E16',
      backgroundElement: '#151B27',
      backgroundSelected: '#212A3B',
      textSecondary: '#A3ADC2',
      border: '#263045',
      presionBajaFondo: '#16342B',
      vidrioSolido: 'rgba(21,27,39,0.92)',
      ambiente1: '#22355A',
      ambiente2: '#1A2946',
      ambiente3: '#2E4470',
    },
  },
} as const;

// Paleta activa: cambiar aquí para comparar fondos.
export const Colors = PALETAS.pizarra;

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
