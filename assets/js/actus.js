/* Module Actualités — injection (lecture seule). Vanilla, défensif, CSP-friendly.
   Config (libellés/couleurs/états) lue depuis un bloc JSON #actus-config (issu de data.py).
   Données via la Function /.netlify/functions/get-actus (déjà filtrées/triées côté serveur). */
(function () {
  var containers = document.querySelectorAll('[data-actus]');
  if (!containers.length) return;                 // page sans module actus

  var ENDPOINT = '/.netlify/functions/get-actus';
  var CFG = {};
  try { var c = document.getElementById('actus-config'); if (c) CFG = JSON.parse(c.textContent); } catch (e) {}
  var TYPES = {};
  (CFG.types || []).forEach(function (t) { TYPES[t.key] = t; });

  function state(el, msg) {
    el.textContent = '';
    var p = document.createElement('p');
    p.className = 'actus-state';
    p.textContent = msg;
    el.appendChild(p);
  }

  function fmtDate(iso) {
    var d = new Date((iso || '') + 'T00:00:00');
    if (isNaN(d.getTime())) return iso || '';
    try { return d.toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' }); }
    catch (e) { return iso; }
  }

  function render(item) {
    var t = TYPES[item.type] || { label: item.type || '', color: '#675F50' };
    var art = document.createElement('article');
    art.className = 'actu';
    art.setAttribute('data-type', item.type || '');

    var head = document.createElement('div'); head.className = 'actu-head';
    var dot = document.createElement('span'); dot.className = 'actu-dot'; dot.style.background = t.color; dot.setAttribute('aria-hidden', 'true');
    var type = document.createElement('span'); type.className = 'actu-type'; type.textContent = t.label;
    head.appendChild(dot); head.appendChild(type);
    if (item.epingle) {
      var pin = document.createElement('span'); pin.className = 'actu-pin'; pin.title = 'Épinglé';
      pin.setAttribute('aria-label', 'Épinglé'); pin.textContent = '★';
      head.appendChild(pin);
    }
    var time = document.createElement('time'); time.className = 'actu-date';
    if (item.date) { time.setAttribute('datetime', item.date); time.textContent = fmtDate(item.date); }
    head.appendChild(time);
    art.appendChild(head);

    var h = document.createElement('h3'); h.className = 'actu-titre'; h.textContent = item.titre || '';
    art.appendChild(h);

    if (item.corps) { var p = document.createElement('p'); p.className = 'actu-corps'; p.textContent = item.corps; art.appendChild(p); }

    // Lien externe optionnel — seulement http(s) (pas de javascript: …)
    if (item.lien && /^https?:\/\//i.test(item.lien)) {
      var a = document.createElement('a'); a.className = 'actu-lien';
      a.href = item.lien; a.target = '_blank'; a.rel = 'noopener';
      a.textContent = 'En savoir plus';
      var arr = document.createElement('span'); arr.setAttribute('aria-hidden', 'true'); arr.textContent = ' ↗';
      a.appendChild(arr);
      art.appendChild(a);
    }
    return art;
  }

  function paint(container, items) {
    container.textContent = '';
    if (!items.length) { state(container, CFG.empty || 'Aucune actualité.'); return; }
    var frag = document.createDocumentFragment();
    items.forEach(function (it) { frag.appendChild(render(it)); });
    container.appendChild(frag);
  }

  function initFilters(listEl, all) {
    var bar = document.querySelector('.actus-filters');
    if (!bar) return;
    bar.addEventListener('click', function (e) {
      var btn = e.target.closest ? e.target.closest('.actus-f') : null;
      if (!btn) return;
      var f = btn.getAttribute('data-filter');
      bar.querySelectorAll('.actus-f').forEach(function (b) {
        var on = b === btn;
        b.classList.toggle('is-on', on);
        b.setAttribute('aria-pressed', on ? 'true' : 'false');
      });
      paint(listEl, f === 'all' ? all : all.filter(function (it) { return it.type === f; }));
    });
  }

  fetch(ENDPOINT, { headers: { Accept: 'application/json' } })
    .then(function (r) { if (!r.ok) throw new Error('HTTP ' + r.status); return r.json(); })
    .then(function (all) {
      if (!Array.isArray(all)) all = [];
      containers.forEach(function (c) {
        if (c.getAttribute('data-actus') === 'home') {
          paint(c, all.slice(0, 3));
        } else {
          paint(c, all);
          initFilters(c, all);
        }
      });
    })
    .catch(function () {
      containers.forEach(function (c) { state(c, CFG.error || 'Indisponible.'); });
    });
})();
