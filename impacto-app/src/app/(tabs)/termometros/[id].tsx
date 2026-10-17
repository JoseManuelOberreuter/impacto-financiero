import { useLocalSearchParams } from 'expo-router';
import { StyleSheet, View } from 'react-native';

import type { Indicador, TermometroDetalle } from '@/api/tipos';
import { Encabezado } from '@/components/encabezado';
import { Fila } from '@/components/fila';
import { DetalleImpacto } from '@/components/impacto-financiero';
import { MiniGrafico } from '@/components/mini-grafico';
import { ContenidoApi, Pagina } from '@/components/pagina';
import { Seccion } from '@/components/seccion';
import { ThemedText } from '@/components/themed-text';
import { Vidrio } from '@/components/vidrio';
import { COLOR_DIRECCION } from '@/constants/presion';
import { Spacing } from '@/constants/theme';
import { useApi } from '@/hooks/use-api';
import { useTheme } from '@/hooks/use-theme';
import { fechaCorta } from '@/utils/fechas';

export default function TermometroDetalleScreen() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const { estado, recargar } = useApi<TermometroDetalle>(`/termometros/${id}`);

  return (
    <Pagina>
      <ContenidoApi estado={estado} recargar={recargar}>
        {(t) => <Detalle termometro={t} />}
      </ContenidoApi>
    </Pagina>
  );
}

function Detalle({ termometro: t }: { termometro: TermometroDetalle }) {
  return (
    <>
      <Encabezado
        titulo={t.nombre}
        bajada={t.pregunta}
        volverA="/termometros"
      />

      <View style={styles.bloque}>
        <ThemedText style={styles.dato}>{t.dato_clave}</ThemedText>
        <ThemedText style={styles.explicacion}>{t.explicacion}</ThemedText>
      </View>

      {t.impacto && (
        <Seccion titulo="En qué se va la diferencia">
          <DetalleImpacto impacto={t.impacto} />
        </Seccion>
      )}

      <Seccion titulo="Indicadores">
        {t.indicadores.map((indicador) => (
          <TarjetaIndicador key={indicador.id} indicador={indicador} />
        ))}
      </Seccion>

      {t.percepcion && (
        <Seccion titulo="Lo que siente la gente">
          <Vidrio style={styles.tarjeta}>
            <ThemedText type="small" themeColor="textSecondary">
              {t.percepcion.nombre}
            </ThemedText>
            <ThemedText style={styles.valorIndicador}>{t.percepcion.valor}</ThemedText>
            <ThemedText type="small">{t.percepcion.descripcion}</ThemedText>
            <ThemedText type="small" themeColor="textSecondary" style={styles.fuente}>
              Fuente: {t.percepcion.fuente}
            </ThemedText>
          </Vidrio>
        </Seccion>
      )}

      {t.proximas_publicaciones.length > 0 && (
        <Seccion titulo="Próximas actualizaciones">
          <Vidrio style={styles.lista}>
            {t.proximas_publicaciones.map((p, i) => (
              <Fila
                key={`${p.fecha}-${p.nombre}`}
                titulo={p.nombre}
                subtitulo={p.fuente}
                valor={fechaCorta(p.fecha)}
                ultima={i === t.proximas_publicaciones.length - 1}
              />
            ))}
          </Vidrio>
        </Seccion>
      )}

      {t.herramienta_relacionada && (
        <Seccion titulo="Herramienta relacionada">
          <Vidrio style={styles.lista}>
            <Fila titulo={t.herramienta_relacionada} href="/herramientas" ultima />
          </Vidrio>
        </Seccion>
      )}

      <Seccion titulo="Cómo se calcula">
        <ThemedText type="small" themeColor="textSecondary" style={styles.metodologia}>
          {t.metodologia} Fuentes: {t.fuentes.join(', ')}.
        </ThemedText>
      </Seccion>
    </>
  );
}

function TarjetaIndicador({ indicador }: { indicador: Indicador }) {
  const theme = useTheme();
  // Verde si el último dato subió, rojo si bajó, gris si no cambió (como en el resto de la app).
  const [anterior, ultimo] = indicador.serie.slice(-2).map((p) => p.valor);
  const direccion = ultimo > anterior ? 'sube' : ultimo < anterior ? 'baja' : 'estable';
  const color = theme[COLOR_DIRECCION[direccion]];

  return (
    <Vidrio style={styles.tarjeta}>
      <View style={styles.filaIndicador}>
        <ThemedText type="smallBold" style={styles.nombreIndicador}>
          {indicador.nombre}
        </ThemedText>
      </View>
      <View style={styles.filaValor}>
        <ThemedText style={styles.valorIndicador}>{indicador.valor}</ThemedText>
        {indicador.variacion && (
          <ThemedText type="small" themeColor="textSecondary">
            {indicador.variacion}
          </ThemedText>
        )}
      </View>
      <MiniGrafico
        valores={indicador.serie.map((p) => p.valor)}
        color={color}
        banda={indicador.banda_normal}
        colorBanda={theme.textSecondary}
        alto={72}
      />
      {indicador.banda_normal && indicador.serie.length > 1 && (
        <ThemedText type="small" themeColor="textSecondary" style={styles.fuente}>
          La franja gris es el rango habitual.
        </ThemedText>
      )}
      <ThemedText type="small">{indicador.descripcion}</ThemedText>
      <ThemedText type="small" themeColor="textSecondary" style={styles.fuente}>
        {indicador.fuente} · dato al {fechaCorta(indicador.dato_al)}
      </ThemedText>
    </Vidrio>
  );
}


const styles = StyleSheet.create({
  bloque: {
    gap: Spacing.two,
  },
  dato: {
    fontSize: 24,
    lineHeight: 32,
    fontWeight: 700,
    letterSpacing: -0.4,
  },
  explicacion: {
    fontSize: 17,
    lineHeight: 26,
  },
  tarjeta: {
    padding: Spacing.four,
    gap: Spacing.two,
  },
  lista: {
    paddingHorizontal: Spacing.four,
  },
  filaIndicador: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    gap: Spacing.two,
  },
  nombreIndicador: {
    flex: 1,
    fontSize: 16,
  },
  filaValor: {
    flexDirection: 'row',
    alignItems: 'baseline',
    gap: Spacing.two,
    flexWrap: 'wrap',
  },
  valorIndicador: {
    fontSize: 28,
    lineHeight: 34,
    fontWeight: 700,
    letterSpacing: -0.6,
  },
  fuente: {
    fontSize: 12,
  },
  metodologia: {
    lineHeight: 20,
  },
});
