import { TabList, TabSlot, TabTrigger, Tabs } from 'expo-router/ui';
import { StyleSheet } from 'react-native';

import { BarraNavegacion, BotonSeccion, Marca, SECCIONES } from '@/components/menu-web';
import { useDiseno } from '@/hooks/use-diseno';

/**
 * Menú en web: barra de vidrio arriba en escritorio y abajo en pantallas angostas,
 * para que se sienta como la app en el celular. Las piezas están en menu-web.tsx.
 */
export default function AppTabs() {
  const { esEscritorio } = useDiseno();

  // Los TabTrigger deben ser hijos directos de TabList: así define las rutas del menú.
  return (
    <Tabs>
      <TabSlot style={styles.slot} />
      {esEscritorio && <Marca />}
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

const styles = StyleSheet.create({
  slot: {
    height: '100%',
  },
});
