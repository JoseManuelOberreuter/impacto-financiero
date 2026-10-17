import { ScrollViewStyleReset } from 'expo-router/html';
import type { PropsWithChildren } from 'react';

import { Colors } from '@/constants/theme';

/**
 * Plantilla del HTML de la web estática (solo se usa al generar la web, nunca en el celular).
 *
 * La web se genera sin saber si el sistema del visitante está en modo oscuro, así que el HTML
 * sale claro hasta que carga la app. Este script corre antes de la primera pintada: lee la
 * apariencia guardada ("impacto:preferencia-tema") o la del sistema, pinta el fondo correcto y,
 * si toca oscuro, oculta el contenido claro hasta que la app lo vuelve a dibujar en oscuro
 * (src/app/_layout.tsx quita la clase "tema-pendiente"). Si la app no carga, se muestra igual a los 3 s.
 */
const TEMA_ANTES_DE_PINTAR = `(function () {
  try {
    var guardada = localStorage.getItem('impacto:preferencia-tema');
    var oscuro = guardada === 'oscuro' || (guardada !== 'claro' && window.matchMedia('(prefers-color-scheme: dark)').matches);
    var html = document.documentElement;
    html.style.backgroundColor = oscuro ? '${Colors.dark.background}' : '${Colors.light.background}';
    html.style.colorScheme = oscuro ? 'dark' : 'light';
    if (oscuro) html.classList.add('tema-pendiente');
  } catch (e) {}
})();`;

const ESTILOS = `
html { background-color: ${Colors.light.background}; }
@media (prefers-color-scheme: dark) { html { background-color: ${Colors.dark.background}; } }
html.tema-pendiente #root { visibility: hidden; animation: mostrar-igual 0s 3s forwards; }
@keyframes mostrar-igual { to { visibility: visible; } }
`;

export default function Root({ children }: PropsWithChildren) {
  return (
    <html lang="es">
      <head>
        <meta charSet="utf-8" />
        <meta httpEquiv="X-UA-Compatible" content="IE=edge" />
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no" />
        <meta name="color-scheme" content="light dark" />
        <script dangerouslySetInnerHTML={{ __html: TEMA_ANTES_DE_PINTAR }} />
        <ScrollViewStyleReset />
        <style dangerouslySetInnerHTML={{ __html: ESTILOS }} />
      </head>
      <body>{children}</body>
    </html>
  );
}
