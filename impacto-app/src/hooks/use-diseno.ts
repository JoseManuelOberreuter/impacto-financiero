import { Platform, useWindowDimensions } from 'react-native';

/** Ancho desde el que la web muestra la barra de navegación arriba en vez de abajo. */
export const ANCHO_ESCRITORIO = 768;
/** Ancho desde el que la marca cabe fija a la izquierda sin chocar con el menú centrado. */
export const ANCHO_MARCA_FUERA = 1100;

export function useDiseno() {
  const { width } = useWindowDimensions();
  const esWeb = Platform.OS === 'web';
  const esEscritorio = esWeb && width >= ANCHO_ESCRITORIO;
  return {
    esWeb,
    esEscritorio,
    // En pantallas anchas la marca va fija arriba a la izquierda; si no, dentro del menú.
    marcaFuera: esWeb && width >= ANCHO_MARCA_FUERA,
    // Espacio para la barra de navegación web (arriba en escritorio, abajo en celular).
    espacioArriba: esEscritorio ? 88 : 0,
    espacioAbajo: esWeb && !esEscritorio ? 96 : 0,
  };
}
