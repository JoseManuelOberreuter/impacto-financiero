import { Check, Circle, Eye, EyeOff } from 'lucide-react-native';
import { useEffect, useState, type ReactNode } from 'react';
import {
  ActivityIndicator,
  Platform,
  Pressable,
  StyleSheet,
  TextInput,
  View,
  type TextInputProps,
} from 'react-native';

import { ThemedText } from '@/components/themed-text';
import { Vidrio } from '@/components/vidrio';
import { Spacing } from '@/constants/theme';
import { useTheme } from '@/hooks/use-theme';
import { REGLAS_CLAVE } from '@/utils/clave';

type PropsCampo = Omit<TextInputProps, 'style' | 'onChangeText' | 'value'> & {
  etiqueta: string;
  valor: string;
  onCambiar: (texto: string) => void;
  /** Campo de contraseña: oculto, con botón para mostrarlo. */
  clave?: boolean;
  error?: string | null;
};

/**
 * En web, el autocompletado del navegador pinta el campo con su propio fondo claro y rectangular.
 * Esta regla lo tapa con el color de la caja y el texto del tema, que cambian con la apariencia.
 */
function useAutocompletarConTema(fondo: string, texto: string) {
  useEffect(() => {
    if (Platform.OS !== 'web' || typeof document === 'undefined') return;
    const id = 'estilo-autocompletar';
    const etiqueta = document.getElementById(id) ?? document.head.appendChild(document.createElement('style'));
    etiqueta.id = id;
    etiqueta.textContent = `
      input:-webkit-autofill,
      input:-webkit-autofill:hover,
      input:-webkit-autofill:focus {
        -webkit-box-shadow: 0 0 0 1000px ${fondo} inset !important;
        box-shadow: 0 0 0 1000px ${fondo} inset !important;
        -webkit-text-fill-color: ${texto} !important;
        caret-color: ${texto};
      }`;
  }, [fondo, texto]);
}

/** Campo de texto con etiqueta, estilo de la app y, si es contraseña, "Mostrar". */
export function CampoTexto({ etiqueta, valor, onCambiar, clave, error, ...props }: PropsCampo) {
  const theme = useTheme();
  const [visible, setVisible] = useState(false);
  useAutocompletarConTema(theme.backgroundSelected, theme.text);

  return (
    <View style={styles.campo}>
      <ThemedText type="smallBold">{etiqueta}</ThemedText>
      <View
        style={[
          styles.caja,
          {
            backgroundColor: theme.backgroundSelected,
            borderColor: error ? theme.presionAlta : theme.border,
          },
        ]}>
        <TextInput
          value={valor}
          onChangeText={onCambiar}
          secureTextEntry={clave && !visible}
          autoCapitalize={clave || props.keyboardType === 'email-address' ? 'none' : props.autoCapitalize}
          autoCorrect={false}
          placeholderTextColor={theme.textSecondary}
          accessibilityLabel={etiqueta}
          style={[styles.entrada, { color: theme.text }]}
          {...props}
        />
        {clave && (
          <Pressable
            onPress={() => setVisible((v) => !v)}
            accessibilityRole="button"
            accessibilityLabel={visible ? 'Ocultar contraseña' : 'Mostrar contraseña'}
            hitSlop={8}>
            {visible ? (
              <EyeOff size={18} color={theme.textSecondary} />
            ) : (
              <Eye size={18} color={theme.textSecondary} />
            )}
          </Pressable>
        )}
      </View>
      {error && (
        <ThemedText type="small" style={{ color: theme.presionAlta }}>
          {error}
        </ThemedText>
      )}
    </View>
  );
}

/** Requisitos de la contraseña que se van marcando mientras se escribe. */
export function ReglasClave({ clave }: { clave: string }) {
  const theme = useTheme();

  return (
    <View style={styles.reglas} accessibilityLabel="Requisitos de la contraseña">
      {REGLAS_CLAVE.map((regla) => {
        const cumple = regla.cumple(clave);
        return (
          <View key={regla.texto} style={styles.regla}>
            {cumple ? (
              <Check size={14} color={theme.presionBaja} strokeWidth={2.5} />
            ) : (
              <Circle size={12} color={theme.textSecondary} />
            )}
            <ThemedText type="small" style={{ color: cumple ? theme.presionBaja : theme.textSecondary }}>
              {regla.texto}
            </ThemedText>
          </View>
        );
      })}
    </View>
  );
}

type PropsBoton = {
  texto: string;
  onPress: () => void;
  deshabilitado?: boolean;
  cargando?: boolean;
  /** "secundario" para acciones menos importantes; "peligro" para borrar. */
  tipo?: 'principal' | 'secundario' | 'peligro';
};

export function Boton({ texto, onPress, deshabilitado, cargando, tipo = 'principal' }: PropsBoton) {
  const theme = useTheme();
  const inactivo = deshabilitado || cargando;
  const color = tipo === 'principal' ? theme.onAccent : tipo === 'peligro' ? theme.presionAlta : theme.text;
  const contenido = cargando ? (
    <ActivityIndicator color={color} />
  ) : (
    <ThemedText type="smallBold" style={{ color }}>
      {texto}
    </ThemedText>
  );

  return (
    <Pressable
      onPress={onPress}
      disabled={inactivo}
      accessibilityRole="button"
      accessibilityState={{ disabled: inactivo, busy: cargando }}
      style={({ pressed }) => ({ opacity: inactivo ? 0.5 : pressed ? 0.8 : 1 })}>
      {/* El secundario es de vidrio, como las tarjetas; los demás tienen fondo de color. */}
      {tipo === 'secundario' ? (
        <Vidrio style={styles.boton}>{contenido}</Vidrio>
      ) : (
        <View
          style={[
            styles.boton,
            { backgroundColor: tipo === 'principal' ? theme.accent : theme.presionAltaFondo },
          ]}>
          {contenido}
        </View>
      )}
    </Pressable>
  );
}

/** Casilla para aceptar algo (términos, o que se entiende una acción sin vuelta atrás). */
export function Casilla({
  marcada,
  onCambiar,
  texto,
}: {
  marcada: boolean;
  onCambiar: (marcada: boolean) => void;
  /** Texto o contenido con enlaces (por ejemplo, a los términos). */
  texto: ReactNode;
}) {
  const theme = useTheme();

  return (
    <Pressable
      onPress={() => onCambiar(!marcada)}
      accessibilityRole="checkbox"
      accessibilityState={{ checked: marcada }}
      style={styles.casillaFila}>
      <View
        style={[
          styles.casilla,
          { borderColor: marcada ? theme.accent : theme.textSecondary, backgroundColor: marcada ? theme.accent : 'transparent' },
        ]}>
        {marcada && <Check size={14} color={theme.onAccent} strokeWidth={3} />}
      </View>
      <ThemedText type="small" style={styles.casillaTexto}>
        {texto}
      </ThemedText>
    </Pressable>
  );
}

/** Mensaje de error o de éxito bajo un formulario. */
export function Aviso({ texto, tipo = 'error' }: { texto: string; tipo?: 'error' | 'exito' | 'info' }) {
  const theme = useTheme();
  const fondo = tipo === 'error' ? theme.presionAltaFondo : tipo === 'exito' ? theme.presionBajaFondo : theme.avisoFondo;
  const color = tipo === 'error' ? theme.presionAlta : tipo === 'exito' ? theme.presionBaja : theme.avisoTexto;

  return (
    <View style={[styles.aviso, { backgroundColor: fondo }]} accessibilityRole="alert">
      <ThemedText type="small" style={{ color }}>
        {texto}
      </ThemedText>
    </View>
  );
}

const styles = StyleSheet.create({
  campo: {
    gap: Spacing.two,
  },
  caja: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: Spacing.two,
    borderWidth: StyleSheet.hairlineWidth,
    borderRadius: Spacing.three,
    paddingHorizontal: Spacing.three,
  },
  entrada: {
    flex: 1,
    paddingVertical: Spacing.two + Spacing.half,
    fontSize: 16,
  },
  reglas: {
    gap: Spacing.one,
  },
  regla: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: Spacing.two,
  },
  boton: {
    alignItems: 'center',
    justifyContent: 'center',
    minHeight: 46,
    borderRadius: Spacing.three,
    paddingHorizontal: Spacing.four,
  },
  casillaFila: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    gap: Spacing.two,
  },
  casilla: {
    width: 20,
    height: 20,
    borderRadius: 5,
    borderWidth: 1.5,
    alignItems: 'center',
    justifyContent: 'center',
    marginTop: 1,
  },
  casillaTexto: {
    flex: 1,
  },
  aviso: {
    padding: Spacing.three,
    borderRadius: Spacing.three,
  },
});
