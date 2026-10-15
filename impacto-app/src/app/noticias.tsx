import { Link } from 'expo-router';
import { Pressable, StyleSheet, View } from 'react-native';

import type { Noticias } from '@/api/tipos';
import { Encabezado } from '@/components/encabezado';
import { Fila } from '@/components/fila';
import { MiniGrafico } from '@/components/mini-grafico';
import { NivelPresion } from '@/components/nivel-presion';
import { ContenidoApi, Pagina } from '@/components/pagina';
import { Seccion } from '@/components/seccion';
import { ThemedText } from '@/components/themed-text';
import { Vidrio } from '@/components/vidrio';
import { PRESION } from '@/constants/presion';
import { Spacing } from '@/constants/theme';
import { useApi } from '@/hooks/use-api';
import { useTheme } from '@/hooks/use-theme';
import { fechaCorta } from '@/utils/fechas';
import { conSigno, proporcion } from '@/utils/numeros';

export default function NoticiasScreen() {
  const { estado, recargar } = useApi<Noticias>('/noticias');

  return (
    <Pagina>
      <Encabezado titulo="Noticias" bajada="El ánimo de la prensa económica y los temas de la semana." />
      <ContenidoApi estado={estado} recargar={recargar}>
        {(noticias) => <Contenido noticias={noticias} />}
      </ContenidoApi>
    </Pagina>
  );
}

function textoTono(tono: number): string {
  if (tono <= -0.5) return 'Negativo';
  if (tono >= 0.5) return 'Positivo';
  return 'Neutro';
}

function Contenido({ noticias: n }: { noticias: Noticias }) {
  const theme = useTheme();

  return (
    <>
      <Vidrio style={styles.tarjeta}>
        <ThemedText type="small" themeColor="textSecondary">
          Ánimo de la semana
        </ThemedText>
        <NivelPresion presion={n.presion} tendencia={n.tendencia} etiqueta={n.etiqueta} />
        <View style={styles.indicadores}>
          <Dato valor={conSigno(n.tono_semana)} etiqueta="Tono (−100 a +100)" />
          <Dato valor={proporcion(n.incertidumbre)} etiqueta="Habla de incertidumbre" />
          <Dato valor={String(n.total_titulares)} etiqueta={`Titulares de ${n.medios} medios`} />
        </View>
        <MiniGrafico
          valores={n.serie_tono.map((p) => p.valor)}
          color={theme[PRESION[n.presion].color]}
          alto={64}
        />
        <ThemedText type="small" themeColor="textSecondary" style={styles.nota}>
          Últimos 7 días, al {fechaCorta(n.dato_al)}.
        </ThemedText>
      </Vidrio>

      <Seccion titulo="Temas que dominan">
        {n.temas.map((tema) => (
          <Vidrio key={tema.nombre} style={styles.tarjeta}>
            <View style={styles.encabezadoTema}>
              <ThemedText type="smallBold" style={styles.nombreTema}>
                {tema.nombre}
              </ThemedText>
              <ThemedText type="small" themeColor="textSecondary">
                {tema.cantidad} titulares · {textoTono(tema.tono)}
              </ThemedText>
            </View>
            {tema.titulares.map((titular) => (
              <View key={titular.titulo} style={styles.titular}>
                <ThemedText type="small">{titular.titulo}</ThemedText>
                <ThemedText type="small" themeColor="textSecondary" style={styles.nota}>
                  {titular.medio} · {fechaCorta(titular.fecha)}
                </ThemedText>
              </View>
            ))}
            <Link href={`/termometros/${tema.termometro}`} asChild>
              <Pressable>
                <ThemedText type="smallBold" themeColor="accent">
                  Ver termómetro relacionado
                </ThemedText>
              </Pressable>
            </Link>
          </Vidrio>
        ))}
      </Seccion>

      <Seccion titulo="Hechos esenciales (CMF)">
        <Vidrio style={styles.lista}>
          {n.hechos_esenciales.map((h, i) => (
            <Fila
              key={`${h.entidad}-${h.titulo}`}
              titulo={h.titulo}
              subtitulo={`${h.entidad} · ${fechaCorta(h.fecha)}\n${h.resumen}`}
              ultima={i === n.hechos_esenciales.length - 1}
            />
          ))}
        </Vidrio>
      </Seccion>

      <ThemedText type="small" themeColor="textSecondary" style={styles.nota}>
        {n.nota}
      </ThemedText>
    </>
  );
}

function Dato({ valor, etiqueta }: { valor: string; etiqueta: string }) {
  return (
    <View style={styles.dato}>
      <ThemedText style={styles.valor}>{valor}</ThemedText>
      <ThemedText type="small" themeColor="textSecondary" style={styles.nota}>
        {etiqueta}
      </ThemedText>
    </View>
  );
}

const styles = StyleSheet.create({
  tarjeta: {
    padding: Spacing.four,
    gap: Spacing.three,
  },
  indicadores: {
    flexDirection: 'row',
    gap: Spacing.three,
  },
  dato: {
    flex: 1,
    gap: Spacing.half,
  },
  valor: {
    fontSize: 24,
    lineHeight: 30,
    fontWeight: 700,
  },
  encabezadoTema: {
    gap: Spacing.half,
  },
  nombreTema: {
    fontSize: 17,
  },
  titular: {
    gap: Spacing.half,
  },
  lista: {
    paddingHorizontal: Spacing.four,
  },
  nota: {
    fontSize: 12,
    lineHeight: 18,
  },
});
