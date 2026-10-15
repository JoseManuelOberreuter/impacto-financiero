import { useState } from 'react';
import { StyleSheet, View } from 'react-native';

import type { Herramientas } from '@/api/tipos';
import { Encabezado } from '@/components/encabezado';
import { Fila } from '@/components/fila';
import { ContenidoApi, Pagina } from '@/components/pagina';
import { Seccion } from '@/components/seccion';
import { SelectorSegmentado } from '@/components/selector-segmentado';
import { ThemedText } from '@/components/themed-text';
import { Vidrio } from '@/components/vidrio';
import { Spacing } from '@/constants/theme';
import { useApi } from '@/hooks/use-api';
import { usePreferenciaTema, type PreferenciaTema } from '@/hooks/use-preferencia-tema';
import { useTheme } from '@/hooks/use-theme';
import { fechaCorta } from '@/utils/fechas';
import { porcentaje } from '@/utils/numeros';

export default function HerramientasScreen() {
  const { estado, recargar } = useApi<Herramientas>('/herramientas');

  return (
    <Pagina>
      <Encabezado titulo="Herramientas" bajada="Calculadoras, tu AFP, el calendario de datos y ajustes." />
      <ContenidoApi estado={estado} recargar={recargar}>
        {(h) => <Contenido herramientas={h} />}
      </ContenidoApi>
    </Pagina>
  );
}

function Contenido({ herramientas: h }: { herramientas: Herramientas }) {
  return (
    <>
      <MiAfp afp={h.mi_afp} />

      <Seccion titulo="Calculadoras">
        <Vidrio style={styles.lista}>
          {h.calculadoras.map((c, i) => (
            <Fila
              key={c.id}
              titulo={c.nombre}
              subtitulo={c.descripcion}
              subvalor={c.disponible ? undefined : 'Pronto'}
              ultima={i === h.calculadoras.length - 1}
            />
          ))}
        </Vidrio>
      </Seccion>

      <Seccion titulo="Calendario económico">
        <Vidrio style={styles.lista}>
          {h.calendario.map((e, i) => (
            <Fila
              key={`${e.fecha}-${e.nombre}`}
              titulo={e.nombre}
              subtitulo={e.fuente}
              valor={fechaCorta(e.fecha)}
              subvalor={e.estimada ? 'estimada' : undefined}
              href={e.termometro ? `/termometros/${e.termometro}` : undefined}
              ultima={i === h.calendario.length - 1}
            />
          ))}
        </Vidrio>
      </Seccion>

      <Seccion titulo="Cómo calculamos">
        <Vidrio style={styles.tarjeta}>
          {h.metodologia.map((m) => (
            <View key={m.titulo} style={styles.metodo}>
              <ThemedText type="smallBold">{m.titulo}</ThemedText>
              <ThemedText type="small" themeColor="textSecondary" style={styles.texto}>
                {m.texto}
              </ThemedText>
            </View>
          ))}
        </Vidrio>
      </Seccion>

      <Ajustes />
    </>
  );
}

const OPCIONES_TEMA: { valor: PreferenciaTema; etiqueta: string }[] = [
  { valor: 'automatico', etiqueta: 'Automático' },
  { valor: 'claro', etiqueta: 'Claro' },
  { valor: 'oscuro', etiqueta: 'Oscuro' },
];

function Ajustes() {
  const { preferencia, cambiarPreferencia } = usePreferenciaTema();

  return (
    <Seccion titulo="Ajustes">
      <Vidrio style={styles.tarjeta}>
        <View style={styles.metodo}>
          <ThemedText type="smallBold">Apariencia</ThemedText>
          <ThemedText type="small" themeColor="textSecondary">
            Automático usa el modo claro u oscuro de tu dispositivo.
          </ThemedText>
        </View>
        <SelectorSegmentado
          opciones={OPCIONES_TEMA}
          valor={preferencia}
          onCambiar={cambiarPreferencia}
          etiquetaAccesible="Apariencia"
        />
      </Vidrio>
    </Seccion>
  );
}

function MiAfp({ afp }: { afp: Herramientas['mi_afp'] }) {
  const theme = useTheme();
  const [fondo, setFondo] = useState('C');
  const seleccionado = afp.fondos.find((f) => f.fondo === fondo) ?? afp.fondos[0];
  const ordenadas = [...seleccionado.afps].sort((a, b) => b.anio - a.anio);

  return (
    <Seccion titulo="Mi AFP">
      <Vidrio style={styles.tarjeta}>
        <ThemedText type="small" themeColor="textSecondary">
          Rentabilidad nominal por AFP. Elige tu fondo:
        </ThemedText>
        <SelectorSegmentado
          opciones={afp.fondos.map((f) => ({ valor: f.fondo, etiqueta: f.fondo }))}
          valor={fondo}
          onCambiar={setFondo}
          etiquetaAccesible="Fondo"
        />
        <View>
          <View style={styles.cabeceraTabla}>
            <ThemedText type="small" themeColor="textSecondary" style={styles.columnaAfp}>
              AFP
            </ThemedText>
            <ThemedText type="small" themeColor="textSecondary" style={styles.columnaNumero}>
              Mes
            </ThemedText>
            <ThemedText type="small" themeColor="textSecondary" style={styles.columnaNumero}>
              Año
            </ThemedText>
          </View>
          {ordenadas.map((a) => (
            <View
              key={a.afp}
              style={[styles.filaTabla, { borderTopColor: theme.border }]}>
              <ThemedText type="smallBold" style={styles.columnaAfp}>
                {a.afp}
              </ThemedText>
              <ThemedText type="small" style={styles.columnaNumero}>
                {porcentaje(a.mes)}
              </ThemedText>
              <ThemedText type="smallBold" style={styles.columnaNumero}>
                {porcentaje(a.anio)}
              </ThemedText>
            </View>
          ))}
        </View>
        <ThemedText type="small" themeColor="textSecondary" style={styles.nota}>
          {afp.fuente}, al {fechaCorta(afp.dato_al)}
          {afp.provisional ? ' (datos provisionales)' : ''}. La rentabilidad pasada no garantiza
          la futura.
        </ThemedText>
      </Vidrio>
    </Seccion>
  );
}

const styles = StyleSheet.create({
  tarjeta: {
    padding: Spacing.four,
    gap: Spacing.three,
  },
  lista: {
    paddingHorizontal: Spacing.four,
  },
  cabeceraTabla: {
    flexDirection: 'row',
    paddingBottom: Spacing.two,
  },
  filaTabla: {
    flexDirection: 'row',
    paddingVertical: Spacing.two,
    borderTopWidth: StyleSheet.hairlineWidth,
  },
  columnaAfp: {
    flex: 2,
  },
  columnaNumero: {
    flex: 1,
    textAlign: 'right',
  },
  metodo: {
    gap: Spacing.one,
  },
  texto: {
    lineHeight: 20,
  },
  nota: {
    fontSize: 12,
    lineHeight: 18,
  },
});
