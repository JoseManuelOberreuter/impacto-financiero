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

type Orden = 'movimiento' | 'subio' | 'bajo';

// Siempre se ven todos los datos: cada opción solo cambia el orden.
const ORDENES: { id: Orden; etiqueta: string }[] = [
  { id: 'movimiento', etiqueta: 'Lo que más se movió' },
  { id: 'subio', etiqueta: 'Lo que más subió' },
  { id: 'bajo', etiqueta: 'Lo que más bajó' },
];

const PRIMERO: Record<'subio' | 'bajo', CambioSemana['direccion'][]> = {
  subio: ['sube', 'estable', 'baja'],
  bajo: ['baja', 'estable', 'sube'],
};

/** Dentro de cada grupo, lo que más se movió va primero. */
function ordenar(datos: CambioSemana[], orden: Orden): CambioSemana[] {
  const porMovimiento = [...datos].sort((a, b) => b.movimiento - a.movimiento);
  if (orden === 'movimiento') return porMovimiento;
  const prioridad = PRIMERO[orden];
  return porMovimiento.sort((a, b) => prioridad.indexOf(a.direccion) - prioridad.indexOf(b.direccion));
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
  const [orden, setOrden] = useState<Orden>('movimiento');
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
