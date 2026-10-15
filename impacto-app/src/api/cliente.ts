import type { Home } from './tipos';

// En el celular físico o emulador Android, "localhost" no apunta a tu PC:
// define EXPO_PUBLIC_API_URL con la IP local (ej. http://192.168.1.10:8000).
const API_URL = process.env.EXPO_PUBLIC_API_URL ?? 'http://localhost:8000';

export async function obtenerHome(): Promise<Home> {
  const respuesta = await fetch(`${API_URL}/v1/home`);
  if (!respuesta.ok) {
    throw new Error(`La API respondió ${respuesta.status}`);
  }
  return respuesta.json();
}
