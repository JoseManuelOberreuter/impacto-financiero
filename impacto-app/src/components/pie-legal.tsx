import { Link, type Href } from 'expo-router';
import { StyleSheet, View } from 'react-native';

import { ThemedText } from '@/components/themed-text';
import { Spacing } from '@/constants/theme';
import { useTheme } from '@/hooks/use-theme';

const ENLACES: { titulo: string; href: Href }[] = [
  { titulo: 'Aviso legal y fuentes', href: '/legal/aviso' },
  { titulo: 'Términos de uso', href: '/legal/terminos' },
  { titulo: 'Privacidad', href: '/legal/privacidad' },
];

/** Pie de todas las páginas: de dónde salen los datos, que no es asesoría y los textos legales. */
export function PieLegal() {
  const theme = useTheme();

  return (
    <View style={[styles.pie, { borderTopColor: theme.border }]}>
      <ThemedText type="small" themeColor="textSecondary" style={styles.texto}>
        Datos públicos del Banco Central, INE, CNE, CMF, ODEPA y la Superintendencia de Pensiones, con
        cálculos propios. Información referencial: no es asesoría financiera ni de inversión, y no nos
        hacemos responsables de las decisiones que tomes con ella.
      </ThemedText>
      <View style={styles.enlaces}>
        {ENLACES.map((enlace) => (
          <Link key={enlace.titulo} href={enlace.href}>
            <ThemedText type="small" themeColor="accent" style={styles.enlace}>
              {enlace.titulo}
            </ThemedText>
          </Link>
        ))}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  pie: {
    marginTop: Spacing.four,
    paddingTop: Spacing.four,
    borderTopWidth: StyleSheet.hairlineWidth,
    gap: Spacing.three,
    alignItems: 'center',
  },
  texto: {
    fontSize: 12,
    lineHeight: 18,
    textAlign: 'center',
  },
  enlaces: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'center',
    columnGap: Spacing.four,
    rowGap: Spacing.one,
  },
  enlace: {
    fontSize: 12,
    lineHeight: 18,
  },
});
