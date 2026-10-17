import { Link, router } from 'expo-router';
import { useState } from 'react';
import { StyleSheet, View } from 'react-native';

import { Encabezado } from '@/components/encabezado';
import { Aviso, Boton, CampoTexto, Casilla, ReglasClave } from '@/components/formulario';
import { Pagina } from '@/components/pagina';
import { ThemedText } from '@/components/themed-text';
import { Vidrio } from '@/components/vidrio';
import { Spacing } from '@/constants/theme';
import { useSesion } from '@/hooks/use-sesion';
import { claveValida, correoValido, mensajeDeError } from '@/utils/clave';

export default function CrearCuentaScreen() {
  const { crearCuenta } = useSesion();
  const [nombre, setNombre] = useState('');
  const [correo, setCorreo] = useState('');
  const [clave, setClave] = useState('');
  const [repetir, setRepetir] = useState('');
  const [acepta, setAcepta] = useState(false);
  const [enviando, setEnviando] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const errorCorreo = correo && !correoValido(correo) ? 'Revisa el correo.' : null;
  const errorRepetir = repetir && repetir !== clave ? 'Las contraseñas no coinciden.' : null;
  const listo = correoValido(correo) && claveValida(clave) && repetir === clave && acepta;

  const enviar = async () => {
    setEnviando(true);
    setError(null);
    const resultado = await crearCuenta(nombre, correo, clave);
    setEnviando(false);
    if (!resultado.ok) {
      setError(mensajeDeError(resultado.error));
      return;
    }
    router.replace({ pathname: '/cuenta/verificar', params: { correo: correo.trim() } });
  };

  return (
    <Pagina>
      <Encabezado
        titulo="Crear cuenta"
        bajada="Es opcional: sirve para guardar tus datos anclados y usarlos en todos tus dispositivos."
        volverA="/cuenta"
      />
      <Vidrio style={styles.tarjeta}>
        <CampoTexto
          etiqueta="Nombre (opcional)"
          valor={nombre}
          onCambiar={setNombre}
          placeholder="Ana"
          autoComplete="given-name"
          textContentType="givenName"
        />
        <CampoTexto
          etiqueta="Correo"
          valor={correo}
          onCambiar={setCorreo}
          placeholder="nombre@correo.cl"
          keyboardType="email-address"
          autoComplete="email"
          textContentType="emailAddress"
          error={errorCorreo}
        />
        <CampoTexto
          etiqueta="Contraseña"
          valor={clave}
          onCambiar={setClave}
          clave
          autoComplete="new-password"
          textContentType="newPassword"
        />
        <ReglasClave clave={clave} />
        <CampoTexto
          etiqueta="Repite la contraseña"
          valor={repetir}
          onCambiar={setRepetir}
          clave
          autoComplete="new-password"
          textContentType="newPassword"
          error={errorRepetir}
        />

        <Casilla
          marcada={acepta}
          onCambiar={setAcepta}
          texto={
            <>
              Acepto los{' '}
              <Link href="/legal/terminos" style={styles.enlace}>
                términos de uso
              </Link>{' '}
              (incluido el{' '}
              <Link href="/legal/aviso" style={styles.enlace}>
                aviso legal
              </Link>
              : la app no es asesoría financiera) y la{' '}
              <Link href="/legal/privacidad" style={styles.enlace}>
                política de privacidad
              </Link>
              .
            </>
          }
        />

        {error && <Aviso texto={error} />}
        <Boton texto="Crear cuenta" onPress={enviar} deshabilitado={!listo} cargando={enviando} />
      </Vidrio>

      <View style={styles.pie}>
        <ThemedText type="small" themeColor="textSecondary">
          ¿Ya tienes cuenta?
        </ThemedText>
        <Link href="/cuenta/ingresar" replace>
          <ThemedText type="smallBold" themeColor="accent">
            Iniciar sesión
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
  enlace: {
    textDecorationLine: 'underline',
  },
  pie: {
    flexDirection: 'row',
    justifyContent: 'center',
    gap: Spacing.one,
  },
});
