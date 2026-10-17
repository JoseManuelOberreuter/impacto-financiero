import { Link } from 'expo-router';
import { ChevronRight } from 'lucide-react-native';
import { Pressable, StyleSheet, View } from 'react-native';

import type { ImpactoFinanciero } from '@/api/tipos';
import { Barra } from '@/components/barra';
import { ThemedText } from '@/components/themed-text';
import { Vidrio } from '@/components/vidrio';
import { Spacing } from '@/constants/theme';
import { useTheme } from '@/hooks/use-theme';
import { mesLargo } from '@/utils/fechas';
import { pesos, porcentaje } from '@/utils/numeros';

function conSigno(valor: number): string {
  const signo = valor > 0 ? '+' : valor < 0 ? '−' : '';
  return `${signo}${pesos(Math.abs(valor))}`;
}

/** Protagonista del Inicio: solo la cifra. Lleva al termómetro con el detalle. */
export function TarjetaImpacto({ impacto }: { impacto: ImpactoFinanciero }) {
  const sube = impacto.diferencia_anual >= 0;

  return (
    <Link href="/termometros/impacto" asChild>
      <Pressable>
        <Vidrio style={styles.tarjeta}>
          <ThemedText type="small" themeColor="textSecondary">
            Impacto Financiero · {mesLargo(impacto.periodo)}
          </ThemedText>
          <View style={styles.cifra}>
            <ThemedText style={styles.total} themeColor={sube ? 'presionAlta' : 'presionBaja'}>
              {conSigno(impacto.diferencia_anual)}
            </ThemedText>
            <ThemedText type="smallBold" themeColor="textSecondary">
              al mes
            </ThemedText>
          </View>
          <ThemedText type="small">
            {sube ? 'Más' : 'Menos'} que hace un año para {impacto.hogar} (
            {porcentaje(impacto.variacion_anual)}). Frente al mes anterior:{' '}
            {conSigno(impacto.diferencia_mensual)}.
          </ThemedText>
        </Vidrio>
      </Pressable>
    </Link>
  );
}

/** Detalle del termómetro: en qué rubros se va la diferencia y el enlace a Mi impacto. */
export function DetalleImpacto({ impacto }: { impacto: ImpactoFinanciero }) {
  const theme = useTheme();
  const maximo = Math.max(...impacto.rubros.map((r) => Math.abs(r.diferencia_anual)), 1);

  return (
    <Vidrio style={styles.tarjeta}>
      <View style={styles.rubros}>
        {impacto.rubros.map((r) => (
          <Barra
            key={r.id}
            etiqueta={`${r.nombre} · ${porcentaje(r.variacion_anual)}`}
            valor={conSigno(r.diferencia_anual)}
            proporcion={Math.abs(r.diferencia_anual) / maximo}
            destacada={r.id !== 'otros'}
          />
        ))}
      </View>

      <ThemedText type="small" themeColor="textSecondary" style={styles.nota}>
        Gasto de {pesos(impacto.gasto_mes)} al mes a precios de hoy. Fuente: {impacto.fuente}.
      </ThemedText>

      <Link href="/herramientas" asChild>
        {/* Con Link asChild, el Pressable lleva un estilo estático y el color va en el View de adentro. */}
        <Pressable style={styles.boton}>
          <View style={[styles.botonContenido, { borderTopColor: theme.border }]}>
            <ThemedText type="smallBold" themeColor="accent">
              Calcular el mío en Mi impacto
            </ThemedText>
            <ChevronRight size={16} color={theme.accent} strokeWidth={2} />
          </View>
        </Pressable>
      </Link>
    </Vidrio>
  );
}

const styles = StyleSheet.create({
  tarjeta: {
    padding: Spacing.four,
    gap: Spacing.two,
  },
  cifra: {
    flexDirection: 'row',
    alignItems: 'baseline',
    gap: Spacing.two,
  },
  total: {
    fontSize: 34,
    lineHeight: 40,
    fontWeight: 700,
    letterSpacing: -0.8,
  },
  rubros: {
    gap: Spacing.three,
  },
  nota: {
    fontSize: 12,
    lineHeight: 18,
    marginTop: Spacing.one,
  },
  boton: {
    marginTop: Spacing.one,
  },
  botonContenido: {
    borderTopWidth: StyleSheet.hairlineWidth,
    paddingTop: Spacing.three,
    flexDirection: 'row',
    alignItems: 'center',
    gap: Spacing.one,
  },
});
