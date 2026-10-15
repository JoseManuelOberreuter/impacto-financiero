import { Platform, useWindowDimensions } from 'react-native';

/** Ancho desde el que la web muestra la barra de navegación arriba en vez de abajo. */
export const ANCHO_ESCRITORIO = 768;

export function useDiseno() {
  const { width } = useWindowDimensions();
  const esWeb = Platform.OS === 'web';
  const esEscritorio = esWeb && width >= ANCHO_ESCRITORIO;
  return {
    esWeb,
    esEscritorio,
    // Espacio para la barra de navegación web (arriba en escritorio, abajo en celular).
    espacioArriba: esEscritorio ? 88 : 0,
    espacioAbajo: esWeb && !esEscritorio ? 96 : 0,
  };
}
