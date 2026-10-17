import { useState } from 'react';
import { Pressable, ScrollView, StyleSheet, View } from 'react-native';

import type { CambioSemana } from '@/api/tipos';
import { Encabezado } from '@/components/encabezado';
import { ListaCambios } from '@/components/lista-cambios';
import { ContenidoApi, Pagina } from '@/components/pagina';
import { ThemedText } from '@/components/themed-text';
import { Spacing } from '@/constants/theme';
import { useAnclados } from '@/hooks/use-anclados';
import { useApi } from '@/hooks/use-api';
import { useTheme } from '@/hooks/use-theme';

type Orden = 'mas' | 'menos' | 'convienen' | 'no_convienen';

// Siempre se ven todos los datos: cada opción solo cambia el orden.
const ORDENES: { id: Orden; etiqueta: string }[] = [
  { id: 'mas', etiqueta: 'Más presión' },
  { id: 'menos', etiqueta: 'Menos presión' },
  { id: 'convienen', etiqueta: 'Me convienen' },
  { id: 'no_convienen', etiqueta: 'No me convienen' },
];

const PRIMERO: Record<'convienen' | 'no_convienen', CambioSemana['tono'][]> = {
  convienen: ['favorable', 'neutral', 'desfavorable'],
  no_convienen: ['desfavorable', 'neutral', 'favorable'],
};

/** La API los entrega de más a menos presión; el orden es estable dentro de cada grupo. */
function ordenar(datos: CambioSemana[], orden: Orden): CambioSemana[] {
  if (orden === 'mas') return datos;
  if (orden === 'menos') return [...datos].reverse();
  const prioridad = PRIMERO[orden];
  return [...datos].sort((a, b) => prioridad.indexOf(a.tono) - prioridad.indexOf(b.tono));
}

export default function DatosScreen() {
  const { estado, recargar } = useApi<CambioSemana[]>('/datos');

  return (
    <Pagina>
      <Encabezado
        titulo="Todos los datos"
        bajada="Elige cómo ordenarlos. Ancla los que más te importan para verlos siempre primero en el Inicio."
        volverA="/termometros"
      />
      <ContenidoApi estado={estado} recargar={recargar}>
        {(datos) => <Contenido datos={datos} />}
      </ContenidoApi>
    </Pagina>
  );
}

function Contenido({ datos }: { datos: CambioSemana[] }) {
  const theme = useTheme();
  const { limite, anclados } = useAnclados();
  const [orden, setOrden] = useState<Orden>('mas');
  const [avisoLimite, setAvisoLimite] = useState(false);
  const visibles = ordenar(datos, orden);

  return (
    <View style={styles.contenido}>
      <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={styles.chips}>
        {ORDENES.map((f) => {
          const activo = f.id === orden;
          return (
            <Pressable
              key={f.id}
              onPress={() => setOrden(f.id)}
              accessibilityRole="button"
              accessibilityState={{ selected: activo }}
              style={[
                styles.chip,
                { backgroundColor: activo ? theme.accent : theme.backgroundSelected },
              ]}>
              <ThemedText type="smallBold" style={{ color: activo ? theme.onAccent : theme.textSecondary }}>
                {f.etiqueta}
              </ThemedText>
            </Pressable>
          );
        })}
      </ScrollView>

      <ThemedText type="small" themeColor="textSecondary">
        {visibles.length} {visibles.length === 1 ? 'dato' : 'datos'}
        {limite !== null ? ` · ${anclados.length} de ${limite} anclados` : ''}
      </ThemedText>

      {avisoLimite && (
        <View style={[styles.aviso, { backgroundColor: theme.avisoFondo }]}>
          <ThemedText type="small" style={{ color: theme.avisoTexto }}>
            En el plan gratis puedes anclar hasta {limite} datos. Desancla uno o pásate a Pro para
            anclar sin límite.
          </ThemedText>
        </View>
      )}

      <ListaCambios cambios={visibles} anclable onLimite={() => setAvisoLimite(true)} />
    </View>
  );
}

const styles = StyleSheet.create({
  contenido: {
    gap: Spacing.three,
  },
  chips: {
    gap: Spacing.two,
  },
  chip: {
    paddingHorizontal: Spacing.three,
    paddingVertical: Spacing.two,
    borderRadius: Spacing.four,
  },
  aviso: {
    padding: Spacing.three,
    borderRadius: Spacing.three,
  },
});
