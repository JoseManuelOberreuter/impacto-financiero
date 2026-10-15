import { useState } from 'react';
import { ActivityIndicator, Pressable, ScrollView, StyleSheet, View } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';

import type { Home } from '@/api/tipos';
import { MiAfpInvitacion } from '@/components/mi-afp-invitacion';
import { PersonalizarTermometros } from '@/components/personalizar-termometros';
import { ResumenDia } from '@/components/resumen-dia';
import { TermometroCard } from '@/components/termometro-card';
import { ThemedText } from '@/components/themed-text';
import { ThemedView } from '@/components/themed-view';
import { MaxContentWidth, Spacing } from '@/constants/theme';
import { useHome } from '@/hooks/use-home';
import { useTheme } from '@/hooks/use-theme';
import { fechaLarga } from '@/utils/fechas';

export default function HomeScreen() {
  const { estado, recargar } = useHome();

  return (
    <ThemedView style={styles.contenedor}>
      <SafeAreaView style={styles.safeArea}>
        <ScrollView contentContainerStyle={styles.scroll}>
          <View style={styles.columna}>
            {estado.tipo === 'cargando' && <ActivityIndicator style={styles.centro} />}
            {estado.tipo === 'error' && (
              <ErrorCarga mensaje={estado.mensaje} onReintentar={recargar} />
            )}
            {estado.tipo === 'listo' && <Contenido home={estado.home} />}
          </View>
        </ScrollView>
      </SafeAreaView>
    </ThemedView>
  );
}

function Contenido({ home }: { home: Home }) {
  const theme = useTheme();
  const [seleccionados, setSeleccionados] = useState(home.termometros_por_defecto);
  const [personalizando, setPersonalizando] = useState(false);

  const visibles = seleccionados
    .map((id) => home.termometros.find((t) => t.id === id))
    .filter((t) => t !== undefined);

  return (
    <>
      <View style={styles.encabezado}>
        <ThemedText type="smallBold" themeColor="accent">
          IMPACTO FINANCIERO
        </ThemedText>
        <ThemedText type="subtitle" style={styles.fecha}>
          {fechaLarga(home.generado_el)}
        </ThemedText>
      </View>

      {home.datos_de_ejemplo && (
        <ThemedView type="avisoFondo" style={styles.aviso}>
          <ThemedText type="small" themeColor="avisoTexto">
            Datos de ejemplo: todavía no están conectadas las fuentes oficiales.
          </ThemedText>
        </ThemedView>
      )}

      <ResumenDia titulo={home.resumen.titulo} texto={home.resumen.texto} />

      <View style={styles.seccion}>
        <ThemedText type="smallBold" style={styles.tituloSeccion}>
          Tus termómetros
        </ThemedText>
        {!personalizando && (
          <Pressable
            onPress={() => setPersonalizando(true)}
            accessibilityRole="button"
            style={({ pressed }) => pressed && styles.presionado}>
            <ThemedText type="smallBold" themeColor="accent">
              Personalizar
            </ThemedText>
          </Pressable>
        )}
      </View>

      {personalizando && (
        <PersonalizarTermometros
          termometros={home.termometros}
          seleccionados={seleccionados}
          maximo={home.max_termometros_home}
          onCambiar={setSeleccionados}
          onCerrar={() => setPersonalizando(false)}
        />
      )}

      {visibles.length === 0 ? (
        <ThemedText type="small" themeColor="textSecondary">
          No elegiste termómetros. Toca “Personalizar” para agregar alguno.
        </ThemedText>
      ) : (
        visibles.map((t) => <TermometroCard key={t.id} termometro={t} />)
      )}

      <MiAfpInvitacion />

      <View style={[styles.pie, { borderTopColor: theme.border }]}>
        <ThemedText type="small" themeColor="textSecondary" style={styles.textoPie}>
          {home.aviso_legal}
        </ThemedText>
        <ThemedText type="small" themeColor="textSecondary" style={styles.textoPie}>
          “Presión” compara cada dato con lo habitual en los últimos años; no dice si algo es
          bueno o malo.
        </ThemedText>
      </View>
    </>
  );
}

function ErrorCarga({ mensaje, onReintentar }: { mensaje: string; onReintentar: () => void }) {
  const theme = useTheme();
  return (
    <View style={styles.centro}>
      <ThemedText type="smallBold">No pudimos cargar los datos</ThemedText>
      <ThemedText type="small" themeColor="textSecondary" style={styles.textoPie}>
        {mensaje}. ¿Está corriendo impacto-api?
      </ThemedText>
      <Pressable
        onPress={onReintentar}
        accessibilityRole="button"
        style={({ pressed }) => [
          styles.reintentar,
          { backgroundColor: theme.accent },
          pressed && styles.presionado,
        ]}>
        <ThemedText type="smallBold" themeColor="onAccent">
          Reintentar
        </ThemedText>
      </Pressable>
    </View>
  );
}

const styles = StyleSheet.create({
  contenedor: {
    flex: 1,
  },
  safeArea: {
    flex: 1,
  },
  scroll: {
    flexGrow: 1,
    alignItems: 'center',
    paddingHorizontal: Spacing.three,
    paddingVertical: Spacing.four,
  },
  columna: {
    width: '100%',
    maxWidth: MaxContentWidth,
    gap: Spacing.three,
  },
  encabezado: {
    gap: Spacing.one,
  },
  fecha: {
    fontSize: 26,
    lineHeight: 34,
  },
  aviso: {
    borderRadius: Spacing.two,
    paddingHorizontal: Spacing.three,
    paddingVertical: Spacing.two,
  },
  seccion: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginTop: Spacing.two,
  },
  tituloSeccion: {
    fontSize: 18,
  },
  pie: {
    borderTopWidth: 1,
    paddingTop: Spacing.three,
    marginTop: Spacing.two,
    gap: Spacing.two,
  },
  textoPie: {
    fontSize: 12,
    lineHeight: 18,
    textAlign: 'center',
  },
  centro: {
    alignItems: 'center',
    gap: Spacing.two,
    marginTop: Spacing.six,
  },
  reintentar: {
    paddingHorizontal: Spacing.four,
    paddingVertical: Spacing.two,
    borderRadius: Spacing.four,
  },
  presionado: {
    opacity: 0.7,
  },
});
