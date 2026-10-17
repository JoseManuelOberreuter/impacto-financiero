import { Platform, useWindowDimensions } from 'react-native';

/**
 * Ancho desde el que la web muestra la barra de navegación arriba en vez de abajo. Arriba solo
 * cabe cuando sobra espacio a los lados del menú para la marca (izquierda) y la burbuja de
 * cuenta con la bandera (derecha); más angosto, el menú va abajo como en el celular.
 */
export const ANCHO_ESCRITORIO = 1100;

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
