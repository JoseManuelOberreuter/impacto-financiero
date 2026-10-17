const MESES = ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dic'];
const MESES_LARGOS = [
  'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
  'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre',
];
const DIAS = ['domingo', 'lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado'];

// Se parsea a mano para evitar corrimientos por zona horaria con fechas ISO sin hora.
function partes(iso: string) {
  const [anio, mes, dia] = iso.split('-').map(Number);
  return { anio, mes, dia };
}

/** "2026-10-09" → "9-oct" */
export function fechaCorta(iso: string): string {
  const { mes, dia } = partes(iso);
  return `${dia}-${MESES[mes - 1]}`;
}

/** "2026-10-15" → "Miércoles 15 de octubre" */
export function fechaLarga(iso: string): string {
  const { anio, mes, dia } = partes(iso);
  const diaSemana = DIAS[new Date(anio, mes - 1, dia).getDay()];
  return `${diaSemana[0].toUpperCase()}${diaSemana.slice(1)} ${dia} de ${MESES_LARGOS[mes - 1]}`;
}

/** "2025-10-01" → "octubre de 2025" */
export function mesYAnio(iso: string): string {
  const { anio, mes } = partes(iso);
  return `${MESES_LARGOS[mes - 1]} de ${anio}`;
}

/** "2026-09-01" → "septiembre" */
export function mesLargo(iso: string): string {
  return MESES_LARGOS[partes(iso).mes - 1];
}
