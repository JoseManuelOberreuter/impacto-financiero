import { StyleSheet, View } from 'react-native';

import type { Precios, Producto } from '@/api/tipos';
import { Barra } from '@/components/barra';
import { Encabezado } from '@/components/encabezado';
import { Fila } from '@/components/fila';
import { MiniGrafico } from '@/components/mini-grafico';
import { ContenidoApi, Pagina } from '@/components/pagina';
import { ThemedText } from '@/components/themed-text';
import { Vidrio } from '@/components/vidrio';
import { Spacing } from '@/constants/theme';
import { useApi } from '@/hooks/use-api';
import { useTheme } from '@/hooks/use-theme';
import { fechaCorta } from '@/utils/fechas';
import { pesos, porcentaje, proporcion } from '@/utils/numeros';

export default function PreciosScreen() {
  const { estado, recargar } = useApi<Precios>('/precios');

  return (
    <Pagina>
      <Encabezado
        titulo="Precios"
        bajada="Lo que cuesta el día a día en Santiago, semana a semana."
      />
      <ContenidoApi estado={estado} recargar={recargar}>
        {(precios) => <Contenido precios={precios} />}
      </ContenidoApi>
    </Pagina>
  );
}

function Contenido({ precios }: { precios: Precios }) {
  const theme = useTheme();
  const { canasta } = precios;
  const mayorCosto = Math.max(...canasta.composicion.map((c) => c.costo));

  const categorias = new Map<string, Producto[]>();
  for (const producto of precios.productos) {
    categorias.set(producto.categoria, [...(categorias.get(producto.categoria) ?? []), producto]);
  }

  return (
    <>
      <Vidrio style={styles.tarjeta}>
        <ThemedText type="small" themeColor="textSecondary">
          Canasta semanal
        </ThemedText>
        <View style={styles.filaTotal}>
          <ThemedText style={styles.total}>{pesos(canasta.total)}</ThemedText>
          <ThemedText type="smallBold">{porcentaje(canasta.variacion_semanal)} esta semana</ThemedText>
        </View>
        <MiniGrafico valores={canasta.serie.map((p) => p.precio)} color={theme.accent} alto={64} />
        <ThemedText type="small" themeColor="textSecondary">
          En qué se va la canasta
        </ThemedText>
        <View style={styles.barras}>
          {canasta.composicion.map((item) => (
            <Barra
              key={item.nombre}
              etiqueta={`${item.nombre} · ${proporcion(item.porcentaje)}`}
              valor={pesos(item.costo)}
              proporcion={item.costo / mayorCosto}
            />
          ))}
        </View>
        <ThemedText type="small" themeColor="textSecondary" style={styles.nota}>
          {canasta.nota} Semana al {fechaCorta(canasta.dato_al)}.
        </ThemedText>
      </Vidrio>

      {[...categorias.entries()].map(([categoria, productos]) => (
        <View key={categoria} style={styles.seccion}>
          <ThemedText type="small" themeColor="textSecondary">
            {categoria}
          </ThemedText>
          <Vidrio style={styles.lista}>
            {productos.map((p, i) => (
              <Fila
                key={p.id}
                titulo={p.nombre}
                subtitulo={p.unidad}
                valor={pesos(p.precio)}
                subvalor={`${porcentaje(p.variacion_semanal)} semana`}
                href={`/precios/${p.id}`}
                ultima={i === productos.length - 1}
              />
            ))}
          </Vidrio>
        </View>
      ))}

      <View style={styles.seccion}>
        <ThemedText type="small" themeColor="textSecondary">
          Energía y transporte
        </ThemedText>
        <Vidrio style={styles.lista}>
          {precios.energia_y_transporte.map((r, i) => (
            <Fila
              key={r.id}
              titulo={r.nombre}
              subtitulo={`${r.unidad} · ${r.fuente}${r.de_ejemplo ? ' · ejemplo' : ''}`}
              valor={pesos(r.precio)}
              ultima={i === precios.energia_y_transporte.length - 1}
            />
          ))}
        </Vidrio>
      </View>

      <ThemedText type="small" themeColor="textSecondary" style={styles.nota}>
        Alimentos: mediana de panaderías, supermercados, ferias y carnicerías de la Región
        Metropolitana según ODEPA.
      </ThemedText>
    </>
  );
}

const styles = StyleSheet.create({
  tarjeta: {
    padding: Spacing.four,
    gap: Spacing.three,
  },
  filaTotal: {
    flexDirection: 'row',
    alignItems: 'flex-end',
    justifyContent: 'space-between',
    flexWrap: 'wrap',
    gap: Spacing.two,
  },
  total: {
    fontSize: 40,
    lineHeight: 46,
    fontWeight: 700,
    letterSpacing: -1.2,
  },
  barras: {
    gap: Spacing.three,
  },
  seccion: {
    gap: Spacing.three,
  },
  lista: {
    paddingHorizontal: Spacing.four,
  },
  nota: {
    fontSize: 12,
    lineHeight: 18,
  },
});
