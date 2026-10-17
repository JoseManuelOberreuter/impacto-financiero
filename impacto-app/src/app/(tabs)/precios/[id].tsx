import { useLocalSearchParams } from 'expo-router';
import { StyleSheet, View } from 'react-native';

import type { Producto } from '@/api/tipos';
import { Barra } from '@/components/barra';
import { Encabezado } from '@/components/encabezado';
import { MiniGrafico } from '@/components/mini-grafico';
import { ContenidoApi, Pagina } from '@/components/pagina';
import { Seccion } from '@/components/seccion';
import { ThemedText } from '@/components/themed-text';
import { Vidrio } from '@/components/vidrio';
import { Spacing } from '@/constants/theme';
import { useApi } from '@/hooks/use-api';
import { useTheme } from '@/hooks/use-theme';
import { fechaCorta } from '@/utils/fechas';
import { pesos, porcentaje } from '@/utils/numeros';

export default function ProductoScreen() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const { estado, recargar } = useApi<Producto>(`/precios/${id}`);

  return (
    <Pagina>
      <ContenidoApi estado={estado} recargar={recargar}>
        {(producto) => <Detalle producto={producto} />}
      </ContenidoApi>
    </Pagina>
  );
}

function Detalle({ producto: p }: { producto: Producto }) {
  const theme = useTheme();
  const maxRegion = Math.max(...p.por_region.map((r) => r.precio));
  const maxTipo = Math.max(...p.por_tipo_local.map((t) => t.precio));
  const primera = p.serie[0];

  return (
    <>
      <Encabezado titulo={p.nombre} bajada={`Precio por ${p.unidad} en Santiago`} volverA="/precios" />

      <Vidrio style={styles.tarjeta}>
        <View style={styles.filaPrecio}>
          <ThemedText style={styles.precio}>{pesos(p.precio)}</ThemedText>
          <View style={styles.variaciones}>
            <ThemedText type="smallBold">{porcentaje(p.variacion_semanal)} semana</ThemedText>
            <ThemedText type="small" themeColor="textSecondary">
              {porcentaje(p.variacion_anual)} en el año
            </ThemedText>
          </View>
        </View>
        <MiniGrafico valores={p.serie.map((s) => s.precio)} color={theme.accent} alto={96} />
        {primera && (
          <ThemedText type="small" themeColor="textSecondary" style={styles.nota}>
            Últimas {p.serie.length} semanas, desde el {fechaCorta(primera.semana)}.
          </ThemedText>
        )}
      </Vidrio>

      {p.por_tipo_local.length > 1 && (
        <Seccion titulo="Dónde se compra">
          <Vidrio style={[styles.tarjeta, styles.barras]}>
            {p.por_tipo_local.map((t) => (
              <Barra key={t.tipo} etiqueta={t.tipo} valor={pesos(t.precio)} proporcion={t.precio / maxTipo} />
            ))}
          </Vidrio>
        </Seccion>
      )}

      <Seccion titulo="Por región">
        <Vidrio style={[styles.tarjeta, styles.barras]}>
          {p.por_region.map((r) => (
            <Barra
              key={r.region}
              etiqueta={r.region}
              valor={pesos(r.precio)}
              proporcion={r.precio / maxRegion}
              destacada={r.region === 'Metropolitana'}
            />
          ))}
        </Vidrio>
      </Seccion>

      <ThemedText type="small" themeColor="textSecondary" style={styles.nota}>
        Fuente: {p.fuente}. Mediana de {p.puntos_de_venta} puntos de venta de la Región
        Metropolitana, semana al {fechaCorta(p.dato_al)}.
      </ThemedText>
    </>
  );
}


const styles = StyleSheet.create({
  tarjeta: {
    padding: Spacing.four,
    gap: Spacing.three,
  },
  filaPrecio: {
    flexDirection: 'row',
    alignItems: 'flex-end',
    justifyContent: 'space-between',
    flexWrap: 'wrap',
    gap: Spacing.two,
  },
  precio: {
    fontSize: 52,
    lineHeight: 58,
    fontWeight: 700,
    letterSpacing: -1.5,
  },
  variaciones: {
    alignItems: 'flex-end',
    paddingBottom: Spacing.two,
  },
  barras: {
    gap: Spacing.three,
  },
  nota: {
    fontSize: 12,
    lineHeight: 18,
  },
});
