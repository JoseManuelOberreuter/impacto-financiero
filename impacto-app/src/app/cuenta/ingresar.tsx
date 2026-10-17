import { Link, router } from 'expo-router';
import { useState } from 'react';
import { StyleSheet, View } from 'react-native';

import { Encabezado } from '@/components/encabezado';
import { Aviso, Boton, CampoTexto } from '@/components/formulario';
import { Pagina } from '@/components/pagina';
import { ThemedText } from '@/components/themed-text';
import { Vidrio } from '@/components/vidrio';
import { Spacing } from '@/constants/theme';
import { useSesion } from '@/hooks/use-sesion';
import { correoValido, mensajeDeError } from '@/utils/clave';

export default function IngresarScreen() {
  const { ingresar } = useSesion();
  const [correo, setCorreo] = useState('');
  const [clave, setClave] = useState('');
  const [enviando, setEnviando] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const enviar = async () => {
    setEnviando(true);
    setError(null);
    const resultado = await ingresar(correo, clave);
    setEnviando(false);
    if (!resultado.ok) {
      setError(mensajeDeError(resultado.error));
      return;
    }
    router.replace('/cuenta');
  };

  return (
    <Pagina>
      <Encabezado titulo="Iniciar sesión" volverA="/cuenta" />
      <Vidrio style={styles.tarjeta}>
        <CampoTexto
          etiqueta="Correo"
          valor={correo}
          onCambiar={setCorreo}
          placeholder="nombre@correo.cl"
          keyboardType="email-address"
          autoComplete="email"
          textContentType="emailAddress"
        />
        <CampoTexto
          etiqueta="Contraseña"
          valor={clave}
          onCambiar={setClave}
          clave
          autoComplete="current-password"
          textContentType="password"
          onSubmitEditing={enviar}
        />
        <Link href="/cuenta/recuperar" style={styles.olvide}>
          <ThemedText type="smallBold" themeColor="accent">
            ¿Olvidaste tu contraseña?
          </ThemedText>
        </Link>
        {error && <Aviso texto={error} />}
        <Boton
          texto="Iniciar sesión"
          onPress={enviar}
          deshabilitado={!correoValido(correo) || !clave}
          cargando={enviando}
        />
      </Vidrio>

      <View style={styles.pie}>
        <ThemedText type="small" themeColor="textSecondary">
          ¿No tienes cuenta?
        </ThemedText>
        <Link href="/cuenta/crear" replace>
          <ThemedText type="smallBold" themeColor="accent">
            Crear cuenta
          </ThemedText>
        </Link>
      </View>
    </Pagina>
  );
}

const styles = StyleSheet.create({
  tarjeta: {
    padding: Spacing.four,
    gap: Spacing.three,
  },
  olvide: {
    alignSelf: 'flex-end',
  },
  pie: {
    flexDirection: 'row',
    justifyContent: 'center',
    gap: Spacing.one,
  },
});
