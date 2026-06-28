/* Admin Actualités — login Netlify Identity + lecture privée (palier 2a, LECTURE SEULE).
   Widget vendorisé (window.netlifyIdentity). Config/libellés via #admin-config (data.py). */
(function () {
  var I = window.netlifyIdentity;
  var signin = document.getElementById('signin'),
      dash = document.getElementById('dash'),
      boot = document.getElementById('admin-boot'),
      loginBtn = document.getElementById('login'),
      logoutBtn = document.getElementById('logout'),
      userEl = document.getElementById('admin-user'),
      listEl = document.getElementById('admin-list');

  var CFG = {};
  try { var c = document.getElementById('admin-config'); if (c) CFG = JSON.parse(c.textContent); } catch (e) {}
  var TYPES = {}; (CFG.types || []).forEach(function (t) { TYPES[t.key] = t; });

  if (!I) { if (boot) boot.textContent = 'Module de connexion indisponible.'; return; }

  if (loginBtn) loginBtn.addEventListener('click', function () { I.open('login'); });
  if (logoutBtn) logoutBtn.addEventListener('click', function () { I.logout(); });

  // init() traite aussi un invite_token / recovery_token présent dans l'URL (#…) :
  // le lien d'invitation qui atterrit sur /admin/ ouvre l'écran de création de mot de passe.
  I.on('init', function (user) { if (boot) boot.hidden = true; user ? showDash(user) : showSignin(); });
  I.on('login', function (user) { I.close(); showDash(user); });
  I.on('logout', function () { showSignin(); });
  I.init();

  function showSignin() { dash.hidden = true; logoutBtn.hidden = true; signin.hidden = false; }
  function showDash(user) {
    signin.hidden = true; logoutBtn.hidden = false; dash.hidden = false;
    if (userEl) userEl.textContent = (user && user.email) || '';
    loadActus(user);
  }

  function state(msg) {
    listEl.textContent = '';
    var p = document.createElement('p'); p.className = 'admin-state'; p.textContent = msg; listEl.appendChild(p);
  }
  function fmtDate(iso) {
    var d = new Date((iso || '') + 'T00:00:00');
    if (isNaN(d.getTime())) return iso || '';
    try { return d.toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' }); } catch (e) { return iso; }
  }

  function loadActus(user) {
    state(CFG.loading || 'Chargement…');
    user.jwt().then(function (token) {
      return fetch('/.netlify/functions/actus-admin', { headers: { Authorization: 'Bearer ' + token } });
    }).then(function (r) {
      if (r.status === 401) { I.logout(); throw new Error('401'); }
      if (!r.ok) throw new Error('HTTP ' + r.status);
      return r.json();
    }).then(function (all) {
      if (!Array.isArray(all)) all = [];
      all.sort(function (a, b) {
        var pa = a.epingle ? 1 : 0, pb = b.epingle ? 1 : 0;
        if (pa !== pb) return pb - pa;
        return String(b.date || '').localeCompare(String(a.date || ''));
      });
      paint(all);
    }).catch(function () { state(CFG.error || 'Erreur de chargement.'); });
  }

  function paint(items) {
    listEl.textContent = '';
    if (!items.length) { state(CFG.empty || 'Aucune brève.'); return; }
    var frag = document.createDocumentFragment();
    items.forEach(function (it) { frag.appendChild(renderItem(it)); });
    listEl.appendChild(frag);
  }

  function badge(cls, text) { var b = document.createElement('span'); b.className = 'admin-badge ' + cls; b.textContent = text; return b; }

  function renderItem(it) {
    var t = TYPES[it.type] || { label: it.type || '', color: '#675F50' };
    var item = document.createElement('article'); item.className = 'admin-item';

    var row = document.createElement('div'); row.className = 'admin-row';
    var dot = document.createElement('span'); dot.className = 'admin-dot'; dot.style.background = t.color; dot.setAttribute('aria-hidden', 'true');
    var type = document.createElement('span'); type.className = 'admin-type'; type.textContent = t.label;
    row.appendChild(dot); row.appendChild(type);
    row.appendChild(it.publie
      ? badge('admin-badge--pub', CFG.published_label || 'Publié')
      : badge('admin-badge--draft', CFG.draft_label || 'Brouillon'));
    if (it.epingle) row.appendChild(badge('admin-badge--pin', CFG.pinned_label || 'Épinglé'));
    var date = document.createElement('span'); date.className = 'admin-date'; if (it.date) date.textContent = fmtDate(it.date);
    row.appendChild(date);
    item.appendChild(row);

    var h = document.createElement('h2'); h.className = 'admin-it-titre'; h.textContent = it.titre || '';
    item.appendChild(h);
    if (it.corps) { var p = document.createElement('p'); p.className = 'admin-it-corps'; p.textContent = it.corps; item.appendChild(p); }
    return item;
  }
})();
