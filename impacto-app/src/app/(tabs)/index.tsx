import { Link } from 'expo-router';
import { ChevronRight } from 'lucide-react-native';
import { Pressable, StyleSheet, View } from 'react-native';

import type { Home } from '@/api/tipos';
import { TarjetaImpacto } from '@/components/impacto-financiero';
import { ListaCambios } from '@/components/lista-cambios';
import { ContenidoApi, Pagina } from '@/components/pagina';
import { Seccion } from '@/components/seccion';
import { TermometroTile } from '@/components/termometro-tile';
import { ThemedText } from '@/components/themed-text';
import { Spacing } from '@/constants/theme';
import { useAnclados } from '@/hooks/use-anclados';
import { useApi } from '@/hooks/use-api';
import { useDiseno } from '@/hooks/use-diseno';
import { useTheme } from '@/hooks/use-theme';
import { fechaLarga } from '@/utils/fechas';

// Diseño: propuesta G en Figma ("Impacto Financiero — Inicio (propuestas)").
export default function InicioScreen() {
  // Los datos anclados van primero en "Lo que cambió esta semana".
  const { anclados } = useAnclados();
  const ruta = anclados.length ? `/home?anclados=${encodeURIComponent(anclados.join(','))}` : '/home';
  const { estado, recargar } = useApi<Home>(ruta);

  return (
    <Pagina>
      <ContenidoApi estado={estado} recargar={recargar}>
        {(home) => <Contenido home={home} />}
      </ContenidoApi>
    </Pagina>
  );
}

function Contenido({ home }: { home: Home }) {
  const theme = useTheme();
  const { esEscritorio } = useDiseno();
  // La personalización llegará cuando haya base de datos para guardarla.
  const termometros = home.termometros_por_defecto
    .map((id) => home.termometros.find((t) => t.id === id))
    .filter((t) => t !== undefined);

  return (
    <>
      <View style={styles.encabezado}>
        {/* En escritorio la marca ya está en la barra de navegación: "Hoy en Chile" sube a esta fila. */}
        {esEscritorio ? (
          <ThemedText type="small" themeColor="textSecondary">
            Hoy en Chile
          </ThemedText>
        ) : (
          <ThemedText type="smallBold">Impacto Financiero</ThemedText>
        )}
        {/* Fuera del escritorio, deja espacio al selector de país fijo en la esquina. */}
        <ThemedText
          type="small"
          themeColor="textSecondary"
          style={[styles.fecha, !esEscritorio && styles.fechaConBandera]}>
          {fechaLarga(home.generado_el)}
        </ThemedText>
      </View>

      <View style={styles.hero}>
        {!esEscritorio && (
          <ThemedText type="small" themeColor="textSecondary">
            Hoy en Chile
          </ThemedText>
        )}
        <ThemedText style={styles.titular}>{home.resumen.titulo}</ThemedText>
        <ThemedText themeColor="textSecondary">{home.resumen.texto}</ThemedText>
      </View>

      <TarjetaImpacto impacto={home.impacto} />

      <Seccion titulo="Lo que cambió esta semana">
        <ListaCambios cambios={home.cambios} />
        <Link href="/termometros/datos" asChild>
          <Pressable style={styles.verTodos}>
            <View style={styles.verTodosContenido}>
              <ThemedText type="smallBold" themeColor="accent">
                Ver todos los datos
              </ThemedText>
              <ChevronRight size={16} color={theme.accent} strokeWidth={2} />
            </View>
          </Pressable>
        </Link>
      </Seccion>

      <Seccion titulo="Termómetros">
        <View style={styles.grilla}>
          {termometros.map((t) => (
            <TermometroTile key={t.id} termometro={t} />
          ))}
        </View>
      </Seccion>

      <ThemedText type="small" themeColor="textSecondary" style={styles.pie}>
        {home.aviso_legal}
      </ThemedText>
    </>
  );
}

const styles = StyleSheet.create({
  encabezado: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  fecha: {
    marginLeft: 'auto',
  },
  fechaConBandera: {
    marginRight: 52,
  },
  hero: {
    gap: Spacing.two,
  },
  titular: {
    fontSize: 27,
    lineHeight: 33,
    fontWeight: 600,
    letterSpacing: -0.4,
  },
  verTodos: {
    alignSelf: 'flex-end',
  },
  verTodosContenido: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: Spacing.one,
  },
  grilla: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: Spacing.three,
  },
  pie: {
    fontSize: 12,
    lineHeight: 18,
    textAlign: 'center',
  },
});
