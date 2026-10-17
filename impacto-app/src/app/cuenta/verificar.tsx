import { Link, useLocalSearchParams } from 'expo-router';
import { MailCheck } from 'lucide-react-native';
import { useEffect, useState } from 'react';
import { StyleSheet, View } from 'react-native';

import { Encabezado } from '@/components/encabezado';
import { Aviso, Boton } from '@/components/formulario';
import { Pagina } from '@/components/pagina';
import { ThemedText } from '@/components/themed-text';
import { Vidrio } from '@/components/vidrio';
import { Spacing } from '@/constants/theme';
import { useSesion } from '@/hooks/use-sesion';
import { useTheme } from '@/hooks/use-theme';
import { mensajeDeError } from '@/utils/clave';

const ESPERA_SEGUNDOS = 60;

export default function VerificarScreen() {
  const theme = useTheme();
  const { correo } = useLocalSearchParams<{ correo?: string }>();
  const { reenviarVerificacion } = useSesion();
  const [espera, setEspera] = useState(ESPERA_SEGUNDOS);
  const [aviso, setAviso] = useState<{ texto: string; tipo: 'error' | 'exito' } | null>(null);

  // Cuenta regresiva para no reenviar el correo muchas veces seguidas.
  useEffect(() => {
    if (espera <= 0) return;
    const reloj = setTimeout(() => setEspera((s) => s - 1), 1000);
    return () => clearTimeout(reloj);
  }, [espera]);

  const reenviar = async () => {
    if (!correo) return;
    const resultado = await reenviarVerificacion(correo);
    setAviso(
      resultado.ok
        ? { texto: 'Te enviamos otro enlace.', tipo: 'exito' }
        : { texto: mensajeDeError(resultado.error), tipo: 'error' },
    );
    setEspera(ESPERA_SEGUNDOS);
  };

  return (
    <Pagina>
      <Encabezado titulo="Revisa tu correo" volverA="/cuenta" />
      <Vidrio style={styles.tarjeta}>
        <View style={[styles.icono, { backgroundColor: theme.backgroundSelected }]}>
          <MailCheck size={26} color={theme.accent} />
        </View>
        <ThemedText>
          Te enviamos un enlace para confirmar tu cuenta{correo ? ` a ${correo}` : ''}. Ábrelo para
          activarla.
        </ThemedText>
        <ThemedText type="small" themeColor="textSecondary">
          Si no lo ves en unos minutos, revisa la carpeta de spam.
        </ThemedText>
        {aviso && <Aviso texto={aviso.texto} tipo={aviso.tipo} />}
        <Boton
          texto={espera > 0 ? `Reenviar el correo (${espera} s)` : 'Reenviar el correo'}
          onPress={reenviar}
          deshabilitado={espera > 0 || !correo}
          tipo="secundario"
        />
        <Link href="/cuenta/ingresar" replace style={styles.enlace}>
          <ThemedText type="smallBold" themeColor="accent">
            Ya la confirmé: iniciar sesión
          </ThemedText>
        </Link>
      </Vidrio>
    </Pagina>
  );
}

const styles = StyleSheet.create({
  tarjeta: {
    padding: Spacing.four,
    gap: Spacing.three,
  },
  icono: {
    width: 52,
    height: 52,
    borderRadius: 26,
    alignItems: 'center',
    justifyContent: 'center',
  },
  enlace: {
    alignSelf: 'center',
  },
});
