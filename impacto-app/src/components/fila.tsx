import { Link, type Href } from 'expo-router';
import { ChevronRight } from 'lucide-react-native';
import type { ReactNode } from 'react';
import { Pressable, StyleSheet, View } from 'react-native';

import { ThemedText } from '@/components/themed-text';
import { Spacing } from '@/constants/theme';
import { useTheme } from '@/hooks/use-theme';

type Props = {
  titulo: string;
  subtitulo?: string;
  valor?: string;
  subvalor?: string;
  izquierda?: ReactNode;
  href?: Href;
  ultima?: boolean;
};

/** Fila de lista dentro de una tarjeta de vidrio. Si tiene `href`, navega. */
export function Fila({ titulo, subtitulo, valor, subvalor, izquierda, href, ultima }: Props) {
  const theme = useTheme();

  const contenido = (
    <View
      style={[
        styles.fila,
        !ultima && { borderBottomColor: theme.border, borderBottomWidth: StyleSheet.hairlineWidth },
      ]}>
      {izquierda}
      <View style={styles.textos}>
        <ThemedText type="smallBold" style={styles.titulo}>
          {titulo}
        </ThemedText>
        {subtitulo && (
          <ThemedText type="small" themeColor="textSecondary">
            {subtitulo}
          </ThemedText>
        )}
      </View>
      {(valor || subvalor) && (
        <View style={styles.valores}>
          {valor && (
            <ThemedText type="smallBold" style={styles.titulo}>
              {valor}
            </ThemedText>
          )}
          {subvalor && (
            <ThemedText type="small" themeColor="textSecondary">
              {subvalor}
            </ThemedText>
          )}
        </View>
      )}
      {href && <ChevronRight size={18} color={theme.textSecondary} />}
    </View>
  );

  if (!href) {
    return contenido;
  }
  // Con Link asChild el estilo debe ser fijo: en web no acepta estilos en función de `pressed`.
  return (
    <Link href={href} asChild>
      <Pressable>{contenido}</Pressable>
    </Link>
  );
}

const styles = StyleSheet.create({
  fila: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: Spacing.three,
    paddingVertical: Spacing.three,
  },
  textos: {
    flex: 1,
    gap: Spacing.half,
  },
  titulo: {
    fontSize: 15,
  },
  valores: {
    alignItems: 'flex-end',
    gap: Spacing.half,
  },
});
