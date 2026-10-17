import { StyleSheet, View } from 'react-native';

import { Encabezado } from '@/components/encabezado';
import { Pagina } from '@/components/pagina';
import { ThemedText } from '@/components/themed-text';
import { Vidrio } from '@/components/vidrio';
import { Spacing } from '@/constants/theme';
import type { DocumentoLegal } from '@/constants/legal';

/** Página de un texto legal (aviso, términos o privacidad): una tarjeta por sección. */
export function PaginaLegal({ documento }: { documento: DocumentoLegal }) {
  return (
    <Pagina>
      <Encabezado titulo={documento.titulo} bajada={documento.bajada} volverA="/" />
      {documento.secciones.map((seccion) => (
        <Vidrio key={seccion.titulo} style={styles.tarjeta}>
          <ThemedText type="smallBold">{seccion.titulo}</ThemedText>
          <View style={styles.parrafos}>
            {seccion.parrafos.map((parrafo) => (
              <ThemedText key={parrafo} type="small" themeColor="textSecondary" style={styles.parrafo}>
                {parrafo}
              </ThemedText>
            ))}
          </View>
        </Vidrio>
      ))}
    </Pagina>
  );
}

const styles = StyleSheet.create({
  tarjeta: {
    padding: Spacing.four,
    gap: Spacing.two,
  },
  parrafos: {
    gap: Spacing.two,
  },
  parrafo: {
    lineHeight: 21,
  },
});
