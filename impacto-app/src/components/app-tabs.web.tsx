import type { Href } from 'expo-router';
import {
  TabList,
  TabSlot,
  TabTrigger,
  Tabs,
  type TabListProps,
  type TabTriggerSlotProps,
} from 'expo-router/ui';
import {
  House,
  Newspaper,
  ShoppingCart,
  Thermometer,
  Wrench,
  type LucideIcon,
} from 'lucide-react-native';
import { Pressable, StyleSheet, View } from 'react-native';

import { ThemedText } from '@/components/themed-text';
import { Vidrio } from '@/components/vidrio';
import { MaxContentWidth, Spacing } from '@/constants/theme';
import { useDiseno } from '@/hooks/use-diseno';
import { useTheme } from '@/hooks/use-theme';

const SECCIONES: { name: string; href: Href; titulo: string; icono: LucideIcon }[] = [
  { name: 'index', href: '/', titulo: 'Inicio', icono: House },
  { name: 'termometros', href: '/termometros', titulo: 'Termómetros', icono: Thermometer },
  { name: 'precios', href: '/precios', titulo: 'Precios', icono: ShoppingCart },
  { name: 'noticias', href: '/noticias', titulo: 'Noticias', icono: Newspaper },
  { name: 'herramientas', href: '/herramientas', titulo: 'Herramientas', icono: Wrench },
];

/**
 * Menú en web: barra de vidrio arriba en escritorio y abajo en pantallas angostas,
 * para que se sienta como la app en el celular.
 */
export default function AppTabs() {
  const { esEscritorio } = useDiseno();

  // Los TabTrigger deben ser hijos directos de TabList: así define las rutas del menú.
  return (
    <Tabs>
      <TabSlot style={styles.slot} />
      <TabList asChild>
        <BarraNavegacion esEscritorio={esEscritorio}>
          {SECCIONES.map((seccion) => (
            <TabTrigger key={seccion.name} name={seccion.name} href={seccion.href} asChild>
              <BotonSeccion titulo={seccion.titulo} icono={seccion.icono} compacto={!esEscritorio} />
            </TabTrigger>
          ))}
        </BarraNavegacion>
      </TabList>
    </Tabs>
  );
}

function BarraNavegacion({
  esEscritorio,
  children,
  style,
  ...props
}: TabListProps & { esEscritorio: boolean }) {
  return (
    <View
      {...props}
      style={[style, styles.contenedorBarra, esEscritorio ? styles.arriba : styles.abajo]}>
      <Vidrio style={[styles.barra, !esEscritorio && styles.barraCompacta]}>
        {esEscritorio && (
          <ThemedText type="smallBold" style={styles.marca}>
            Impacto
          </ThemedText>
        )}
        {children}
      </Vidrio>
    </View>
  );
}

type PropsBoton = TabTriggerSlotProps & { titulo: string; icono: LucideIcon; compacto: boolean };

function BotonSeccion({ titulo, icono: Icono, compacto, isFocused, ...props }: PropsBoton) {
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

const styles = StyleSheet.create({
  slot: {
    height: '100%',
  },
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
    maxWidth: MaxContentWidth + Spacing.six,
    borderRadius: Spacing.five,
    paddingHorizontal: Spacing.two,
    paddingVertical: Spacing.two,
    gap: Spacing.one,
  },
  barraCompacta: {
    justifyContent: 'space-around',
    paddingHorizontal: Spacing.one,
    gap: 0,
  },
  marca: {
    marginLeft: Spacing.three,
    marginRight: 'auto',
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
