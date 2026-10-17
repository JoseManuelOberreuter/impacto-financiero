// Reglas de la contraseña (docs/cuentas.md). Supabase las valida también en el servidor.
export const REGLAS_CLAVE: { texto: string; cumple: (clave: string) => boolean }[] = [
  { texto: 'Al menos 10 caracteres', cumple: (c) => c.length >= 10 },
  { texto: 'Una letra minúscula', cumple: (c) => /[a-záéíóúñ]/.test(c) },
  { texto: 'Una letra mayúscula', cumple: (c) => /[A-ZÁÉÍÓÚÑ]/.test(c) },
  { texto: 'Un número', cumple: (c) => /\d/.test(c) },
];

export function claveValida(clave: string): boolean {
  return REGLAS_CLAVE.every((regla) => regla.cumple(clave));
}

export function correoValido(correo: string): boolean {
  return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(correo.trim());
}

/** Traduce los errores de Supabase Auth a mensajes claros, sin revelar si un correo existe. */
export function mensajeDeError(error: { message?: string; code?: string } | null | undefined): string {
  const texto = `${error?.code ?? ''} ${error?.message ?? ''}`.toLowerCase();
  if (texto.includes('invalid_credentials') || texto.includes('invalid login')) {
    return 'El correo o la contraseña no son correctos.';
  }
  if (texto.includes('email_not_confirmed') || texto.includes('not confirmed')) {
    return 'Primero confirma tu correo: revisa tu bandeja de entrada.';
  }
  if (texto.includes('weak_password') || texto.includes('password should')) {
    return 'La contraseña no cumple los requisitos.';
  }
  if (texto.includes('same_password') || texto.includes('different from the old')) {
    return 'La nueva contraseña debe ser distinta de la anterior.';
  }
  if (texto.includes('rate') || texto.includes('too many') || texto.includes('security purposes')) {
    return 'Demasiados intentos. Espera un momento y vuelve a intentarlo.';
  }
  if (texto.includes('network') || texto.includes('fetch')) {
    return 'No pudimos conectarnos. Revisa tu conexión.';
  }
  return 'Algo salió mal. Inténtalo de nuevo.';
}
