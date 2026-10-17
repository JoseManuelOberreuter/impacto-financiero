import { router, type Href } from 'expo-router';
import type { TabListProps, TabTriggerSlotProps } from 'expo-router/ui';
import {
  House,
  Newspaper,
  ShoppingCart,
  Thermometer,
  Wrench,
  type LucideIcon,
} from 'lucide-react-native';
import { useState } from 'react';
import { Pressable, StyleSheet, View } from 'react-native';

import { ThemedText } from '@/components/themed-text';
import { Vidrio } from '@/components/vidrio';
import { MaxContentWidth, Spacing } from '@/constants/theme';
import { useDiseno } from '@/hooks/use-diseno';
import { useTheme } from '@/hooks/use-theme';

// Piezas del menú web, compartidas por las pestañas (app-tabs.web.tsx) y por las pantallas de
// Mi cuenta, que se abren fuera de las pestañas pero en web deben mostrar el mismo menú.

export const SECCIONES: { name: string; href: Href; titulo: string; icono: LucideIcon }[] = [
  { name: 'index', href: '/', titulo: 'Inicio', icono: House },
  { name: 'termometros', href: '/termometros', titulo: 'Termómetros', icono: Thermometer },
  { name: 'precios', href: '/precios', titulo: 'Precios', icono: ShoppingCart },
  { name: 'noticias', href: '/noticias', titulo: 'Noticias', icono: Newspaper },
  { name: 'herramientas', href: '/herramientas', titulo: 'Herramientas', icono: Wrench },
];

/** Con el menú arriba, la marca va fija arriba a la izquierda (como la bandera a la derecha). */
export function Marca() {
  return (
    <View pointerEvents="none" style={styles.marca}>
      <ThemedText type="smallBold" style={styles.textoMarca}>
        Impacto Financiero
      </ThemedText>
    </View>
  );
}

/**
 * Ancho de la barra de desplazamiento del navegador (15 px en Windows, 0 en Mac).
 * El contenido se centra en el espacio que deja la barra; el menú debe hacer lo mismo.
 */
function anchoScrollbar(): number {
  if (typeof document === 'undefined') return 0;
  const prueba = document.createElement('div');
  prueba.style.cssText = 'position:absolute;top:-9999px;width:100px;height:100px;overflow:scroll';
  document.body.appendChild(prueba);
  const ancho = prueba.offsetWidth - prueba.clientWidth;
  prueba.remove();
  return ancho;
}

export function BarraNavegacion({
  esEscritorio,
  children,
  style,
  ...props
}: TabListProps & { esEscritorio: boolean }) {
  const [scrollbar] = useState(anchoScrollbar);

  return (
    <View
      {...props}
      style={[
        style,
        styles.contenedorBarra,
        esEscritorio ? styles.arriba : styles.abajo,
        { right: scrollbar },
      ]}>
      {/* Mismo ancho que el contenido: los bordes calzan con las tarjetas y las secciones quedan al centro. */}
      <Vidrio style={[styles.barra, esEscritorio ? styles.barraAncha : styles.barraCompacta]}>
        {children}
      </Vidrio>
    </View>
  );
}

type PropsBoton = TabTriggerSlotProps & { titulo: string; icono: LucideIcon; compacto: boolean };

export function BotonSeccion({ titulo, icono: Icono, compacto, isFocused, ...props }: PropsBoton) {
  const theme = useTheme();
  const color = isFocused ? theme.accent : theme.textSecondary;

  return (
    <Pressable
      {...props}
      accessibilityLabel={titulo}
      style={({ pressed }) => [
        styles.boton,
        compacto ? styles.botonCompacto : styles.botonAncho,
        isFocused && !compacto && { backgroundColor: theme.backgroundSelected },
        pressed && styles.presionado,
      ]}>
      <Icono size={compacto ? 22 : 16} color={color} strokeWidth={isFocused ? 2.25 : 1.75} />
      <ThemedText
        type="smallBold"
        style={[styles.texto, compacto && styles.textoCompacto, { color }]}
        numberOfLines={1}>
        {titulo}
      </ThemedText>
    </Pressable>
  );
}

/** El mismo menú, fuera de las pestañas: ninguna sección marcada y cada botón navega. */
export function MenuSuelto() {
  const { esEscritorio } = useDiseno();

  return (
    <>
      {esEscritorio && <Marca />}
      <BarraNavegacion esEscritorio={esEscritorio}>
        {SECCIONES.map((seccion) => (
          <BotonSeccion
            key={seccion.name}
            titulo={seccion.titulo}
            icono={seccion.icono}
            compacto={!esEscritorio}
            accessibilityRole="link"
            onPress={() => router.navigate(seccion.href)}
          />
        ))}
      </BarraNavegacion>
    </>
  );
}

const styles = StyleSheet.create({
  contenedorBarra: {
    flexDirection: 'column',
    position: 'absolute',
    left: 0,
    right: 0,
    paddingHorizontal: Spacing.three,
    alignItems: 'center',
  },
  arriba: {
    top: Spacing.three,
  },
  abajo: {
    bottom: Spacing.three,
    paddingHorizontal: Spacing.two,
  },
  barra: {
    flexDirection: 'row',
    alignItems: 'center',
    width: '100%',
    // Mismo ancho que la columna de contenido, para que los bordes calcen con las tarjetas.
    maxWidth: MaxContentWidth,
    borderRadius: Spacing.five,
    paddingHorizontal: Spacing.two,
    paddingVertical: Spacing.two,
    gap: Spacing.one,
  },
  barraAncha: {
    justifyContent: 'center',
  },
  barraCompacta: {
    justifyContent: 'space-around',
    paddingHorizontal: Spacing.one,
    gap: 0,
  },
  marca: {
    position: 'absolute',
    top: Spacing.three,
    left: Spacing.three,
    paddingVertical: Spacing.one,
  },
  textoMarca: {
    fontSize: 15,
  },
  boton: {
    alignItems: 'center',
    borderRadius: Spacing.four,
  },
  botonAncho: {
    flexDirection: 'row',
    gap: Spacing.two,
    paddingHorizontal: Spacing.three,
    paddingVertical: Spacing.two,
  },
  botonCompacto: {
    flex: 1,
    gap: Spacing.half,
    paddingVertical: Spacing.one,
  },
  texto: {
    fontSize: 14,
  },
  textoCompacto: {
    fontSize: 10,
    lineHeight: 14,
    fontWeight: 500,
    letterSpacing: -0.2,
  },
  presionado: {
    opacity: 0.7,
  },
});
