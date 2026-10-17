// En el celular físico o emulador Android, "localhost" no apunta a tu PC:
// define EXPO_PUBLIC_API_URL con la IP local (ej. http://192.168.1.10:8000).
const API_URL = process.env.EXPO_PUBLIC_API_URL ?? 'http://localhost:8000';

function cabeceras(token?: string | null, conCuerpo = false): Record<string, string> {
  return {
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
    ...(conCuerpo ? { 'Content-Type': 'application/json' } : {}),
  };
}

async function leer<T>(respuesta: Response): Promise<T> {
  if (respuesta.status === 404) {
    throw new Error('No encontramos lo que buscabas');
  }
  if (respuesta.status === 401) {
    throw new Error('Tu sesión venció. Vuelve a iniciar sesión.');
  }
  if (!respuesta.ok) {
    throw new Error(`La API respondió ${respuesta.status}`);
  }
  return respuesta.status === 204 ? (undefined as T) : respuesta.json();
}

/** GET a la API. `ruta` sin el prefijo de versión, por ejemplo "/home". Con `token`, como el usuario. */
export async function obtener<T>(ruta: string, token?: string | null): Promise<T> {
  return leer<T>(await fetch(`${API_URL}/v1${ruta}`, { headers: cabeceras(token) }));
}

/** PUT o DELETE a la API como el usuario con sesión. */
export async function enviar<T>(
  ruta: string,
  metodo: 'PUT' | 'DELETE',
  token: string,
  cuerpo?: unknown,
): Promise<T> {
  return leer<T>(
    await fetch(`${API_URL}/v1${ruta}`, {
      method: metodo,
      headers: cabeceras(token, cuerpo !== undefined),
      body: cuerpo !== undefined ? JSON.stringify(cuerpo) : undefined,
    }),
  );
}
