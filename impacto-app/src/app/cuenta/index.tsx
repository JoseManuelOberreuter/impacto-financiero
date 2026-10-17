import { Link, router, useLocalSearchParams } from 'expo-router';
import { Cloud, Pin, Smartphone } from 'lucide-react-native';
import { useEffect, useState, type ReactNode } from 'react';
import { ActivityIndicator, StyleSheet, View } from 'react-native';

import { obtener } from '@/api/cliente';
import { Encabezado } from '@/components/encabezado';
import { Fila } from '@/components/fila';
import { Aviso, Boton } from '@/components/formulario';
import { Pagina } from '@/components/pagina';
import { Seccion } from '@/components/seccion';
import { SelectorSegmentado } from '@/components/selector-segmentado';
import { ThemedText } from '@/components/themed-text';
import { Vidrio } from '@/components/vidrio';
import { Spacing } from '@/constants/theme';
import { usePreferenciaTema, type PreferenciaTema } from '@/hooks/use-preferencia-tema';
import { useSesion } from '@/hooks/use-sesion';
import { useTheme } from '@/hooks/use-theme';

type Yo = {
  id: string;
  correo: string;
  verificado: boolean;
  nombre: string | null;
  plan: string;
};

const OPCIONES_TEMA: { valor: PreferenciaTema; etiqueta: string }[] = [
  { valor: 'automatico', etiqueta: 'Automático' },
  { valor: 'claro', etiqueta: 'Claro' },
  { valor: 'oscuro', etiqueta: 'Oscuro' },
];

/** Claro, oscuro o automático. Se guarda en este dispositivo, con o sin cuenta. */
function Apariencia() {
  const { preferencia, cambiarPreferencia } = usePreferenciaTema();

  return (
    <Seccion titulo="Apariencia">
      <Vidrio style={styles.tarjeta}>
        <ThemedText type="small" themeColor="textSecondary">
          Automático usa el modo claro u oscuro de tu dispositivo.
        </ThemedText>
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

const NOMBRE_PLAN: Record<string, string> = { gratis: 'Gratis', pro: 'Pro', empresas: 'Empresas' };

export default function CuentaScreen() {
  const { disponible, cargando, sesion } = useSesion();

  return (
    <Pagina>
      <Encabezado titulo="Mi cuenta" volverA="/" />
      {!disponible ? (
        <>
          <Vidrio style={styles.tarjeta}>
            <ThemedText type="small" themeColor="textSecondary">
              Las cuentas todavía no están disponibles. La app funciona igual sin cuenta.
            </ThemedText>
          </Vidrio>
          <Apariencia />
        </>
      ) : cargando ? (
        <ActivityIndicator style={styles.cargando} />
      ) : sesion ? (
        <ConSesion />
      ) : (
        <SinSesion />
      )}
    </Pagina>
  );
}

function Beneficio({ icono, titulo, texto }: { icono: ReactNode; titulo: string; texto: string }) {
  const theme = useTheme();
  return (
    <View style={styles.beneficio}>
      <View style={[styles.icono, { backgroundColor: theme.backgroundSelected }]}>{icono}</View>
      <View style={styles.textos}>
        <ThemedText type="smallBold">{titulo}</ThemedText>
        <ThemedText type="small" themeColor="textSecondary">
          {texto}
        </ThemedText>
      </View>
    </View>
  );
}

function SinSesion() {
  const theme = useTheme();
  const { aviso } = useLocalSearchParams<{ aviso?: string }>();
  return (
    <>
      {aviso === 'borrada' && <Aviso texto="Tu cuenta quedó borrada." tipo="exito" />}
      <Vidrio style={styles.tarjeta}>
        <ThemedText>La cuenta es opcional. Sin ella, la app funciona igual en este dispositivo.</ThemedText>
        <Beneficio
          icono={<Pin size={18} color={theme.accent} />}
          titulo="Tus datos anclados, a salvo"
          texto="Se guardan en tu cuenta y no se pierden si cambias de teléfono."
        />
        <Beneficio
          icono={<Smartphone size={18} color={theme.accent} />}
          titulo="En todos tus dispositivos"
          texto="Lo mismo en el teléfono y en la web."
        />
        <Beneficio
          icono={<Cloud size={18} color={theme.accent} />}
          titulo="Lo que viene"
          texto="Alertas y el plan Pro necesitan una cuenta."
        />
      </Vidrio>
      <Boton texto="Crear cuenta" onPress={() => router.push('/cuenta/crear')} />
      <Boton texto="Iniciar sesión" tipo="secundario" onPress={() => router.push('/cuenta/ingresar')} />
      <Apariencia />
    </>
  );
}

function ConSesion() {
  const { sesion, token, salir } = useSesion();
  const { aviso } = useLocalSearchParams<{ aviso?: string }>();
  const [yo, setYo] = useState<Yo | null>(null);
  const [ocupado, setOcupado] = useState<'salir' | 'todos' | null>(null);

  useEffect(() => {
    if (!token) return;
    obtener<Yo>('/yo', token)
      .then(setYo)
      .catch(() => setYo(null));
  }, [token]);

  const nombre = yo?.nombre ?? (sesion?.user.user_metadata?.nombre as string | undefined) ?? null;
  const correo = yo?.correo ?? sesion?.user.email ?? '';

  const cerrar = async (todos: boolean) => {
    setOcupado(todos ? 'todos' : 'salir');
    await salir(todos);
    setOcupado(null);
  };

  return (
    <>
      {aviso === 'clave' && <Aviso texto="Tu contraseña quedó actualizada." tipo="exito" />}

      <Vidrio style={styles.lista}>
        <Fila titulo="Nombre" valor={nombre ?? 'Sin nombre'} />
        <Fila titulo="Correo" subtitulo={correo} />
        <Fila titulo="Plan" valor={yo ? (NOMBRE_PLAN[yo.plan] ?? yo.plan) : '...'} ultima />
      </Vidrio>

      <Apariencia />

      <Seccion titulo="Seguridad">
        <Vidrio style={styles.lista}>
          <Fila titulo="Cambiar contraseña" href="/cuenta/nueva-clave" ultima />
        </Vidrio>
      </Seccion>

      <Seccion titulo="Sesión">
        <View style={styles.botones}>
          <Boton texto="Cerrar sesión" tipo="secundario" onPress={() => cerrar(false)} cargando={ocupado === 'salir'} />
          <Boton
            texto="Cerrar sesión en todos los dispositivos"
            tipo="secundario"
            onPress={() => cerrar(true)}
            cargando={ocupado === 'todos'}
          />
        </View>
      </Seccion>

      {/* Discreto a propósito: borrar la cuenta tiene su propia pantalla con varios pasos. */}
      <Link href="/cuenta/borrar" style={styles.borrar}>
        <ThemedText type="small" themeColor="textSecondary">
          Borrar cuenta
        </ThemedText>
      </Link>
    </>
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
  cargando: {
    marginTop: Spacing.five,
  },
  beneficio: {
    flexDirection: 'row',
    gap: Spacing.three,
    alignItems: 'center',
  },
  icono: {
    width: 36,
    height: 36,
    borderRadius: 18,
    alignItems: 'center',
    justifyContent: 'center',
  },
  textos: {
    flex: 1,
    gap: Spacing.half,
  },
  borrar: {
    alignSelf: 'center',
    marginTop: Spacing.four,
  },
  botones: {
    gap: Spacing.two,
  },
});
