import { Minus, TrendingDown, TrendingUp, type LucideIcon } from 'lucide-react-native';

import type { Presion, Tendencia } from '@/api/tipos';
import type { ThemeColor } from '@/constants/theme';

// El nivel siempre se escribe además del color (accesibilidad).
export const PRESION: Record<Presion, { texto: string; color: ThemeColor; fondo: ThemeColor }> = {
  baja: { texto: 'Baja', color: 'presionBaja', fondo: 'presionBajaFondo' },
  media: { texto: 'Media', color: 'presionMedia', fondo: 'presionMediaFondo' },
  alta: { texto: 'Alta', color: 'presionAlta', fondo: 'presionAltaFondo' },
};

export const TENDENCIA: Record<Tendencia, { icono: LucideIcon; texto: string }> = {
  sube: { icono: TrendingUp, texto: 'sube' },
  baja: { icono: TrendingDown, texto: 'baja' },
  estable: { icono: Minus, texto: 'estable' },
};
