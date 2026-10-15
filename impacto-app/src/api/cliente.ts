// En el celular físico o emulador Android, "localhost" no apunta a tu PC:
// define EXPO_PUBLIC_API_URL con la IP local (ej. http://192.168.1.10:8000).
const API_URL = process.env.EXPO_PUBLIC_API_URL ?? 'http://localhost:8000';

/** GET a la API. `ruta` sin el prefijo de versión, por ejemplo "/home". */
export async function obtener<T>(ruta: string): Promise<T> {
  const respuesta = await fetch(`${API_URL}/v1${ruta}`);
  if (respuesta.status === 404) {
    throw new Error('No encontramos lo que buscabas');
  }
  if (!respuesta.ok) {
    throw new Error(`La API respondió ${respuesta.status}`);
  }
  return respuesta.json();
}
