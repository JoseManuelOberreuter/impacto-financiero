// Formato chileno a mano: punto de miles, coma decimal.
// El espacio antes de "%" es no separable para que no quede solo en otra línea.

/** 2165 → "$2.165" */
export function pesos(valor: number): string {
  const entero = Math.round(valor).toString();
  return `$${entero.replace(/\B(?=(\d{3})+(?!\d))/g, '.')}`;
}

/** 0.7 → "+0,7 %", -1.25 → "−1,3 %", 0 → "0,0 %" */
export function porcentaje(valor: number): string {
  const signo = valor > 0 ? '+' : valor < 0 ? '−' : '';
  return `${signo}${Math.abs(valor).toFixed(1).replace('.', ',')}\u00a0%`;
}

/** 7 → "7,0 %" (sin signo, para participaciones y proporciones) */
export function proporcion(valor: number): string {
  return `${valor.toFixed(1).replace('.', ',')}\u00a0%`;
}

/** −18 → "−18", 5 → "+5" (con el signo menos tipográfico) */
export function conSigno(valor: number): string {
  return valor > 0 ? `+${valor}` : valor < 0 ? `−${Math.abs(valor)}` : '0';
}
