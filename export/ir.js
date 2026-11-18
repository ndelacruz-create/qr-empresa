/* Página de salida: registra la visita en Vercel Web Analytics y sigue al destino fijo. */
(function () {
  'use strict';
  var me = document.currentScript, to = me && me.getAttribute('data-to');
  if (!to || !/^https:\/\//.test(to)) return;
  var done = false;
  function go() { if (!done) { done = true; location.replace(to); } }
  var va = document.querySelector('script[src*="/_vercel/insights/"]');
  if (va) {
    va.addEventListener('load', function () { setTimeout(go, 450); });
    va.addEventListener('error', go);
  }
  setTimeout(go, 1500);
})();
