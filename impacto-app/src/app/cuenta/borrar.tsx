import { Link, router } from 'expo-router';
import { useEffect, useState } from 'react';
import { StyleSheet, View } from 'react-native';

import { Encabezado } from '@/components/encabezado';
import { Aviso, Boton, CampoTexto, Casilla } from '@/components/formulario';
import { Pagina } from '@/components/pagina';
import { ThemedText } from '@/components/themed-text';
import { Vidrio } from '@/components/vidrio';
import { Spacing } from '@/constants/theme';
import { useSesion } from '@/hooks/use-sesion';
import { useTheme } from '@/hooks/use-theme';
import { mensajeDeError } from '@/utils/clave';

const PALABRA = 'BORRAR';
const ESPERA_SEGUNDOS = 5;

const SE_PIERDE = [
  'Tu cuenta, tu correo y tu nombre.',
  'Los datos anclados y las preferencias guardadas en la cuenta.',
  'Tu plan y cualquier suscripción asociada.',
];

/**
 * Borrar la cuenta a propósito tiene varios pasos: entender qué se pierde, marcar que no se
 * puede deshacer, confirmar la contraseña, escribir BORRAR y esperar unos segundos.
 */
export default function BorrarCuentaScreen() {
  const theme = useTheme();
  const { sesion, cargando, ingresar, borrarCuenta } = useSesion();
  const [entiende, setEntiende] = useState(false);
  const [clave, setClave] = useState('');
  const [palabra, setPalabra] = useState('');
  const [borrando, setBorrando] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const listo = entiende && clave.length > 0 && palabra.trim() === PALABRA;

  if (!sesion) {
    return (
      <Pagina>
        <Encabezado titulo="Borrar cuenta" volverA="/cuenta" />
        {!cargando && <Aviso texto="Inicia sesión para borrar tu cuenta." tipo="info" />}
      </Pagina>
    );
  }

  const borrar = async () => {
    setBorrando(true);
    setError(null);
    // Confirmamos la contraseña antes de borrar: un teléfono desbloqueado no basta.
    const verificacion = await ingresar(sesion.user.email ?? '', clave);
    if (!verificacion.ok) {
      setBorrando(false);
      setError(mensajeDeError(verificacion.error));
      return;
    }
    const resultado = await borrarCuenta();
    setBorrando(false);
    if (!resultado.ok) {
      setError(mensajeDeError(resultado.error));
      return;
    }
    router.replace({ pathname: '/cuenta', params: { aviso: 'borrada' } });
  };

  return (
    <Pagina>
      <Encabezado
        titulo="Borrar cuenta"
        bajada="Esto es definitivo. Si solo quieres dejar de usarla en este dispositivo, cierra sesión."
        volverA="/cuenta"
      />

      <Vidrio style={styles.tarjeta}>
        <ThemedText type="smallBold">Se borra para siempre</ThemedText>
        <View style={styles.lista}>
          {SE_PIERDE.map((texto) => (
            <View key={texto} style={styles.punto}>
              <View style={[styles.vineta, { backgroundColor: theme.presionAlta }]} />
              <ThemedText type="small" style={styles.textoPunto}>
                {texto}
              </ThemedText>
            </View>
          ))}
        </View>
        <ThemedText type="small" themeColor="textSecondary">
          Los datos anclados en este dispositivo se mantienen. Puedes crear una cuenta nueva más
          adelante, pero empezará vacía.
        </ThemedText>
      </Vidrio>

      <Vidrio style={styles.tarjeta}>
        <Casilla
          marcada={entiende}
          onCambiar={setEntiende}
          texto="Entiendo que se borra mi cuenta y que no se puede deshacer."
        />
        <CampoTexto
          etiqueta="Tu contraseña"
          valor={clave}
          onCambiar={setClave}
          clave
          autoComplete="current-password"
          textContentType="password"
        />
        <CampoTexto
          etiqueta={`Escribe ${PALABRA} para confirmar`}
          valor={palabra}
          onCambiar={setPalabra}
          autoCapitalize="characters"
          placeholder={PALABRA}
        />
        {error && <Aviso texto={error} />}
        {listo ? (
          <BotonFinal onPress={borrar} cargando={borrando} />
        ) : (
          <Boton texto="Borrar mi cuenta para siempre" tipo="peligro" onPress={borrar} deshabilitado />
        )}
      </Vidrio>

      <Link href="/cuenta" replace style={styles.cancelar}>
        <ThemedText type="smallBold" themeColor="accent">
          No, mantener mi cuenta
        </ThemedText>
      </Link>
    </Pagina>
  );
}

/** Se monta al completar todo: el botón se habilita recién tras unos segundos de espera. */
function BotonFinal({ onPress, cargando }: { onPress: () => void; cargando: boolean }) {
  const [espera, setEspera] = useState(ESPERA_SEGUNDOS);

  useEffect(() => {
    if (espera <= 0) return;
    const reloj = setTimeout(() => setEspera((s) => s - 1), 1000);
    return () => clearTimeout(reloj);
  }, [espera]);

  return (
    <Boton
      texto={espera > 0 ? `Borrar mi cuenta (${espera} s)` : 'Borrar mi cuenta para siempre'}
      tipo="peligro"
      onPress={onPress}
      deshabilitado={espera > 0}
      cargando={cargando}
    />
  );
}

const styles = StyleSheet.create({
  tarjeta: {
    padding: Spacing.four,
    gap: Spacing.three,
  },
  lista: {
    gap: Spacing.two,
  },
  punto: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: Spacing.two,
  },
  vineta: {
    width: 6,
    height: 6,
    borderRadius: 3,
  },
  textoPunto: {
    flex: 1,
  },
  cancelar: {
    alignSelf: 'center',
  },
});
