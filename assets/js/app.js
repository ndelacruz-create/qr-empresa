/* AC Hotel Punta Cana · landing
   Fechas en hora de República Dominicana e interactividad.
   La página trae dos versiones (.v-m celular, .v-d computadora); cada una funciona por separado.
   Sin innerHTML ni eval: solo textContent, atributos y estilos. */
(function () {
  'use strict';

  var rd = {};
  try {
    new Intl.DateTimeFormat('en-CA', { timeZone: 'America/Santo_Domingo', year: 'numeric', month: 'numeric', day: 'numeric' })
      .formatToParts(new Date())
      .forEach(function (p) { rd[p.type] = Number(p.value); });
  } catch (e) {
    var d0 = new Date(Date.now() - 4 * 3600000);
    rd = { year: d0.getUTCFullYear(), month: d0.getUTCMonth() + 1, day: d0.getUTCDate() };
  }
  var today = Date.UTC(rd.year, rd.month - 1, rd.day);

  function parse(iso) { var p = iso.split('-'); return { y: +p[0], m: +p[1], d: +p[2] }; }
  function left(iso) { var f = parse(iso); return Math.round((Date.UTC(f.y, f.m - 1, f.d) - today) / 86400000); }
  var dias = ['domingo', 'lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado'];
  var meses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'];
  function fecha(iso) {
    var k = left(iso); if (k === 0) return 'hoy'; if (k === 1) return 'mañana';
    var f = parse(iso), t = new Date(Date.UTC(f.y, f.m - 1, f.d));
    return dias[t.getUTCDay()] + ' ' + f.d + ' de ' + meses[f.m - 1];
  }
  function cuenta(iso) { var k = left(iso); return k < 0 ? '' : k > 1 ? 'faltan ' + k + ' días' : k === 1 ? 'es mañana' : 'es hoy'; }
  function $all(sel, root) { return Array.prototype.slice.call(root.querySelectorAll(sel)); }

  var agendaAll = [
    { f: '2026-11-21', name: 'Feria Artesanal', href: 'temporada', feria: true },
    { f: '2026-11-26', name: 'Cena de Thanksgiving', href: 'temporada' },
    { f: '2026-12-24', name: 'Cena de Nochebuena', href: 'temporada' },
    { f: '2026-12-27', name: 'San Silvestre del Caribe', href: 'comunidad' },
    { f: '2026-12-31', name: 'Gran Cena de Fin de Año', href: 'temporada' },
    { f: '2027-01-01', name: 'Brunch de Bienvenida 2027', href: 'temporada' }
  ].filter(function (e) { return left(e.f) >= 0; });

  function ultimoDomingo(y, m0) { var t = new Date(Date.UTC(y, m0 + 1, 0)); t.setUTCDate(t.getUTCDate() - t.getUTCDay()); return t; }
  var ls = ultimoDomingo(rd.year, rd.month - 1);
  if (ls.getTime() < today) ls = ultimoDomingo(rd.year, rd.month);
  var lsIso = ls.getUTCFullYear() + '-' + (ls.getUTCMonth() + 1) + '-' + ls.getUTCDate();

  function setup(root) {
    var pfx = root.getAttribute('data-pfx') || '';
    function byId(id) { return document.getElementById(pfx + id); }

    // Eventos con fecha: se ocultan al día siguiente
    $all('[data-until]', root).forEach(function (el) { if (left(el.getAttribute('data-until')) < 0) el.style.display = 'none'; });
    var temporada = byId('temporada');
    if (temporada) {
      var quedan = $all('[data-until]', temporada).filter(function (el) { return el.style.display !== 'none'; });
      var vacio = temporada.querySelector('[data-noseason]');
      if (vacio && quedan.length === 0) vacio.hidden = false;
    }
    $all('[data-countdown]', root).forEach(function (el) { el.textContent = cuenta(el.getAttribute('data-countdown')); });
    $all('[data-lastsunday]', root).forEach(function (el) {
      el.textContent = (left(lsIso) === 0 ? 'hoy, ' : '') + 'domingo ' + ls.getUTCDate() + ' de ' + meses[ls.getUTCMonth()];
    });

    // Próximo en la agenda (portada)
    var wrap = root.querySelector('[data-agenda-wrap]');
    var link = root.querySelector('[data-agenda-link]');
    if (!agendaAll.length) {
      if (wrap) wrap.style.display = 'none';
    } else if (link) {
      var nx = agendaAll[0];
      link.setAttribute('href', '#' + pfx + nx.href);
      var w = link.querySelector('[data-agenda="when"]'); if (w) w.textContent = fecha(nx.f);
      if (!nx.feria) {
        var n1 = link.querySelector('[data-agenda="name1"]'); if (n1) n1.textContent = nx.name;
        var n2 = link.querySelector('[data-agenda="name2"]'); if (n2) n2.textContent = '';
        $all('[data-feria]', link).forEach(function (f) { f.style.display = 'none'; });
        link.style.background = '#FBF8F4'; link.style.color = '#1C1C1C'; link.style.border = '0';
        link.style.paddingTop = '18px'; link.style.paddingBottom = '16px';
        var eb = link.querySelector('[data-agenda-eyebrow]'); if (eb) eb.style.color = '#80694C';
      }
    }

    // Day Pass: una opción abierta a la vez
    function setTier(id) {
      $all('[data-tier-box]', root).forEach(function (box) {
        var tid = box.getAttribute('data-tier-box'), on = tid === id;
        var btn = box.querySelector('[data-tier]');
        if (btn) {
          btn.setAttribute('aria-expanded', on ? 'true' : 'false');
          var spans = btn.querySelectorAll('span');
          for (var i = 0; i < spans.length; i++) { if (spans[i].style.fontStyle) spans[i].style.fontStyle = on ? 'italic' : 'normal'; }
          var svg = btn.querySelector('svg'); if (svg) svg.style.transform = 'rotate(' + (on ? 45 : 0) + 'deg)';
        }
        var panel = byId('tier-' + tid); if (panel) panel.hidden = !on;
      });
    }
    $all('[data-tier]', root).forEach(function (b) { b.addEventListener('click', function () { setTier(b.getAttribute('data-tier')); }); });

    // Tarjetas que giran
    var giradas = {};
    function flip(n) {
      giradas[n] = !giradas[n];
      var on = giradas[n];
      var card = root.querySelector('[data-flip-card="' + n + '"]'); if (!card) return;
      card.style.transform = 'rotateY(' + (on ? 180 : 0) + 'deg)';
      var front = card.children[0], back = card.children[1];
      if (front) { front.style.visibility = on ? 'hidden' : 'visible'; front.setAttribute('aria-hidden', on ? 'true' : 'false'); }
      if (back) { back.style.visibility = on ? 'visible' : 'hidden'; back.setAttribute('aria-hidden', on ? 'false' : 'true'); }
      $all('[data-flip="' + n + '"][aria-expanded]', root).forEach(function (b) { b.setAttribute('aria-expanded', on ? 'true' : 'false'); });
      var target = on ? back && back.querySelector('a, button') : front && front.querySelector('[data-flip]');
      if (target) setTimeout(function () { target.focus({ preventScroll: true }); }, 520);
    }
    $all('[data-flip]', root).forEach(function (b) { b.addEventListener('click', function () { flip(b.getAttribute('data-flip')); }); });

    // Alrededores: pestañas y lugares desplegables
    var abierto = '';
    function setPlace(pid) {
      $all('[data-place]', root).forEach(function (b) {
        var id = b.getAttribute('data-place'), on = id === pid;
        b.setAttribute('aria-expanded', on ? 'true' : 'false');
        var spans = b.querySelectorAll('span');
        for (var i = 0; i < spans.length; i++) { if (spans[i].style.fontStyle && spans[i].style.fontSize === '23px') spans[i].style.fontStyle = on ? 'italic' : 'normal'; }
        var svg = b.querySelector('svg'); if (svg) svg.style.transform = 'rotate(' + (on ? 45 : 0) + 'deg)';
        var panel = byId('place-' + id); if (panel) panel.hidden = !on;
      });
    }
    $all('[data-place]', root).forEach(function (b) {
      b.addEventListener('click', function () { var id = b.getAttribute('data-place'); abierto = abierto === id ? '' : id; setPlace(abierto); });
    });
    $all('[data-zona-tab]', root).forEach(function (t) {
      t.addEventListener('click', function () {
        var z = t.getAttribute('data-zona-tab');
        $all('[data-zona-tab]', root).forEach(function (o) {
          var on = o === t;
          o.setAttribute('aria-pressed', on ? 'true' : 'false');
          o.style.background = on ? '#1C1C1C' : 'transparent';
          o.style.color = on ? '#FFFFFF' : '#1C1C1C';
        });
        $all('[data-zona-panel]', root).forEach(function (p) { p.hidden = p.getAttribute('data-zona-panel') !== z; });
        abierto = ''; setPlace('');
      });
    });
  }

  Array.prototype.forEach.call(document.querySelectorAll('.v-m, .v-d'), setup);
})();
