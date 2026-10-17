import { useState } from 'react';
import { StyleSheet } from 'react-native';

import { Encabezado } from '@/components/encabezado';
import { Aviso, Boton, CampoTexto } from '@/components/formulario';
import { Pagina } from '@/components/pagina';
import { Vidrio } from '@/components/vidrio';
import { Spacing } from '@/constants/theme';
import { useSesion } from '@/hooks/use-sesion';
import { correoValido, mensajeDeError } from '@/utils/clave';

export default function RecuperarScreen() {
  const { recuperar } = useSesion();
  const [correo, setCorreo] = useState('');
  const [enviando, setEnviando] = useState(false);
  const [aviso, setAviso] = useState<{ texto: string; tipo: 'error' | 'exito' } | null>(null);

  const enviar = async () => {
    setEnviando(true);
    const resultado = await recuperar(correo);
    setEnviando(false);
    // Mismo mensaje exista o no la cuenta: no revelamos qué correos están registrados.
    // Solo mostramos el error cuando es por demasiados intentos.
    const limite = !resultado.ok && /rate|too many|security/i.test(resultado.error.message ?? '');
    setAviso(
      limite
        ? { texto: mensajeDeError(resultado.error), tipo: 'error' }
        : {
            texto: 'Si existe una cuenta con ese correo, te enviamos un enlace para elegir una nueva contraseña.',
            tipo: 'exito',
          },
    );
  };

  return (
    <Pagina>
      <Encabezado
        titulo="Recuperar contraseña"
        bajada="Escribe tu correo y te enviaremos un enlace para elegir una nueva contraseña."
        volverA="/cuenta"
      />
      <Vidrio style={styles.tarjeta}>
        <CampoTexto
          etiqueta="Correo"
          valor={correo}
          onCambiar={setCorreo}
          placeholder="nombre@correo.cl"
          keyboardType="email-address"
          autoComplete="email"
          textContentType="emailAddress"
          onSubmitEditing={enviar}
        />
        {aviso && <Aviso texto={aviso.texto} tipo={aviso.tipo} />}
        <Boton texto="Enviar enlace" onPress={enviar} deshabilitado={!correoValido(correo)} cargando={enviando} />
      </Vidrio>
    </Pagina>
  );
}

const styles = StyleSheet.create({
  tarjeta: {
    padding: Spacing.four,
    gap: Spacing.three,
  },
});
