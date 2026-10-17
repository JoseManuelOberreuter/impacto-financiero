import { Link, router } from 'expo-router';
import { useState } from 'react';
import { StyleSheet } from 'react-native';

import { Encabezado } from '@/components/encabezado';
import { Aviso, Boton, CampoTexto, ReglasClave } from '@/components/formulario';
import { Pagina } from '@/components/pagina';
import { ThemedText } from '@/components/themed-text';
import { Vidrio } from '@/components/vidrio';
import { Spacing } from '@/constants/theme';
import { useSesion } from '@/hooks/use-sesion';
import { claveValida, mensajeDeError } from '@/utils/clave';

/** Se abre desde el enlace del correo de recuperación, o desde Mi cuenta para cambiarla. */
export default function NuevaClaveScreen() {
  const { sesion, cargando, cambiarClave } = useSesion();
  const [clave, setClave] = useState('');
  const [repetir, setRepetir] = useState('');
  const [enviando, setEnviando] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const guardar = async () => {
    setEnviando(true);
    setError(null);
    const resultado = await cambiarClave(clave);
    setEnviando(false);
    if (!resultado.ok) {
      setError(mensajeDeError(resultado.error));
      return;
    }
    router.replace({ pathname: '/cuenta', params: { aviso: 'clave' } });
  };

  return (
    <Pagina>
      <Encabezado titulo="Nueva contraseña" volverA="/cuenta" />
      <Vidrio style={styles.tarjeta}>
        {!sesion && !cargando ? (
          <>
            <Aviso texto="El enlace venció o ya se usó. Pide uno nuevo para cambiar tu contraseña." />
            <Link href="/cuenta/recuperar" replace style={styles.enlace}>
              <ThemedText type="smallBold" themeColor="accent">
                Pedir un enlace nuevo
              </ThemedText>
            </Link>
          </>
        ) : (
          <>
            <CampoTexto
              etiqueta="Nueva contraseña"
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
              error={repetir && repetir !== clave ? 'Las contraseñas no coinciden.' : null}
            />
            {error && <Aviso texto={error} />}
            <Boton
              texto="Guardar contraseña"
              onPress={guardar}
              deshabilitado={!claveValida(clave) || repetir !== clave}
              cargando={enviando}
            />
          </>
        )}
      </Vidrio>
    </Pagina>
  );
}

const styles = StyleSheet.create({
  tarjeta: {
    padding: Spacing.four,
    gap: Spacing.three,
  },
  enlace: {
    alignSelf: 'center',
  },
});
