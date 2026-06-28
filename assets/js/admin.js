/* Admin Actualités — login Identity + CRUD (palier 2b).
   Source de vérité = le store : toute action POST le tableau complet à save-actus,
   puis re-fetch actus-admin. Widget vendorisé. Config/libellés via #admin-config (data.py). */
(function () {
  var I = window.netlifyIdentity;
  var $ = function (id) { return document.getElementById(id); };
  var signin = $('signin'), dash = $('dash'), boot = $('admin-boot'),
      loginBtn = $('login'), logoutBtn = $('logout'), userEl = $('admin-user'),
      listEl = $('admin-list'),
      form = $('actu-form'), fId = $('f-id'), fDate = $('f-date'), fType = $('f-type'),
      fTitre = $('f-titre'), fCorps = $('f-corps'), fLien = $('f-lien'),
      fEpingle = $('f-epingle'), fPublie = $('f-publie'),
      fSave = $('f-save'), fCancel = $('f-cancel'), fMsg = $('f-msg');

  var CFG = {};
  try { var c = $('admin-config'); if (c) CFG = JSON.parse(c.textContent); } catch (e) {}
  var TYPES = {}; (CFG.types || []).forEach(function (t) { TYPES[t.key] = t; });

  var actus = [];        // miroir mémoire de l'état serveur
  var editingId = null;  // id en cours d'édition (null = création)
  var busy = false;      // verrou pendant un POST

  if (!I) { if (boot) boot.textContent = 'Module de connexion indisponible.'; return; }

  if (loginBtn) loginBtn.addEventListener('click', function () { I.open('login'); });
  if (logoutBtn) logoutBtn.addEventListener('click', function () { I.logout(); });

  I.on('init', function (user) { if (boot) boot.hidden = true; user ? showDash(user) : showSignin(); });
  I.on('login', function (user) { I.close(); showDash(user); });
  I.on('logout', function () { showSignin(); });
  I.init(); // traite aussi invite_token / recovery_token de l'URL (#…)

  function showSignin() { dash.hidden = true; logoutBtn.hidden = true; signin.hidden = false; }
  function showDash(user) {
    signin.hidden = true; logoutBtn.hidden = false; dash.hidden = false;
    if (userEl) userEl.textContent = (user && user.email) || '';
    resetForm();
    loadActus();
  }

  // ---------- helpers ----------
  function authed(url, opts) {
    var u = I.currentUser();
    if (!u) return Promise.reject(new Error('no-user'));
    return u.jwt().then(function (token) {
      opts = opts || {}; opts.headers = opts.headers || {};
      opts.headers.Authorization = 'Bearer ' + token;
      return fetch(url, opts);
    });
  }
  function state(msg) { listEl.textContent = ''; var p = document.createElement('p'); p.className = 'admin-state'; p.textContent = msg; listEl.appendChild(p); }
  function msg(text, isErr) { fMsg.textContent = text || ''; fMsg.className = 'admin-formmsg' + (isErr ? ' is-err' : (text ? ' is-ok' : '')); }
  function fmtDate(iso) { var d = new Date((iso || '') + 'T00:00:00'); if (isNaN(d.getTime())) return iso || ''; try { return d.toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' }); } catch (e) { return iso; } }
  function todayISO() { var d = new Date(); var m = ('0' + (d.getMonth() + 1)).slice(-2), j = ('0' + d.getDate()).slice(-2); return d.getFullYear() + '-' + m + '-' + j; }
  function setBusy(on) {
    busy = on;
    [fSave, fCancel, logoutBtn].forEach(function (b) { if (b) b.disabled = on; });
    listEl.querySelectorAll('button').forEach(function (b) { b.disabled = on; });
  }

  // ---------- chargement ----------
  function loadActus() {
    state(CFG.loading || 'Chargement…');
    authed('/.netlify/functions/actus-admin').then(function (r) {
      if (r.status === 401) { I.logout(); throw new Error('401'); }
      if (!r.ok) throw new Error('HTTP ' + r.status);
      return r.json();
    }).then(function (all) {
      actus = Array.isArray(all) ? all : [];
      renderList();
    }).catch(function () { state(CFG.error || 'Erreur de chargement.'); });
  }

  function sorted() {
    return actus.slice().sort(function (a, b) {
      var pa = a.epingle ? 1 : 0, pb = b.epingle ? 1 : 0;
      if (pa !== pb) return pb - pa;
      return String(b.date || '').localeCompare(String(a.date || ''));
    });
  }

  function badge(cls, text) { var s = document.createElement('span'); s.className = 'admin-badge ' + cls; s.textContent = text; return s; }

  function renderList() {
    listEl.textContent = '';
    var items = sorted();
    if (!items.length) { state(CFG.empty || 'Aucune brève enregistrée.'); return; }
    var frag = document.createDocumentFragment();
    items.forEach(function (it) { frag.appendChild(renderItem(it)); });
    listEl.appendChild(frag);
  }

  function renderItem(it) {
    var t = TYPES[it.type] || { label: it.type || '', color: '#675F50' };
    var item = document.createElement('article'); item.className = 'admin-item'; item.setAttribute('data-id', it.id);

    var row = document.createElement('div'); row.className = 'admin-row';
    var dot = document.createElement('span'); dot.className = 'admin-dot'; dot.style.background = t.color; dot.setAttribute('aria-hidden', 'true');
    var type = document.createElement('span'); type.className = 'admin-type'; type.textContent = t.label;
    row.appendChild(dot); row.appendChild(type);
    row.appendChild(it.publie ? badge('admin-badge--pub', CFG.published_label || 'Publié') : badge('admin-badge--draft', CFG.draft_label || 'Brouillon'));
    if (it.epingle) row.appendChild(badge('admin-badge--pin', CFG.pinned_label || 'Épinglé'));
    var date = document.createElement('span'); date.className = 'admin-date'; if (it.date) date.textContent = fmtDate(it.date);
    row.appendChild(date);
    item.appendChild(row);

    var h = document.createElement('h3'); h.className = 'admin-it-titre'; h.textContent = it.titre || ''; item.appendChild(h);
    if (it.corps) { var p = document.createElement('p'); p.className = 'admin-it-corps'; p.textContent = it.corps; item.appendChild(p); }

    var acts = document.createElement('div'); acts.className = 'admin-actions';
    acts.appendChild(actBtn('edit', CFG.act_edit || 'Éditer'));
    acts.appendChild(actBtn('toggle', it.publie ? (CFG.act_unpublish || 'Dépublier') : (CFG.act_publish || 'Publier')));
    acts.appendChild(actBtn('del', CFG.act_delete || 'Supprimer', true));
    item.appendChild(acts);
    return item;
  }
  function actBtn(act, label, danger) {
    var b = document.createElement('button'); b.type = 'button';
    b.className = 'abtn abtn--sm' + (danger ? ' abtn--danger' : '');
    b.setAttribute('data-act', act); b.textContent = label;
    return b;
  }

  // ---------- actions liste (délégation) ----------
  listEl.addEventListener('click', function (e) {
    if (busy) return;
    var btn = e.target.closest ? e.target.closest('button[data-act]') : null;
    if (!btn) return;
    var art = btn.closest('.admin-item'); if (!art) return;
    var id = art.getAttribute('data-id');
    var item = actus.filter(function (b) { return String(b.id) === String(id); })[0];
    if (!item) return;
    var act = btn.getAttribute('data-act');

    if (act === 'edit') { fillForm(item); window.scrollTo({ top: 0, behavior: 'smooth' }); }
    else if (act === 'toggle') {
      var next = actus.map(function (b) { return String(b.id) === String(id) ? Object.assign({}, b, { publie: !b.publie }) : b; });
      save(next, CFG.saved_publish || 'Statut mis à jour.');
    }
    else if (act === 'del') {
      if (!window.confirm(CFG.confirm_delete || 'Supprimer cette brève ?')) return;
      var rest = actus.filter(function (b) { return String(b.id) !== String(id); });
      save(rest, CFG.saved_delete || 'Brève supprimée.');
    }
  });

  // ---------- formulaire ----------
  function resetForm() {
    editingId = null; if (fId) fId.value = '';
    if (form) form.reset();
    if (fDate) fDate.value = todayISO();
    if (fCancel) fCancel.hidden = true;
    msg('');
  }

  function fillForm(it) {
    editingId = it.id; if (fId) fId.value = it.id;
    fDate.value = it.date || todayISO();
    fType.value = it.type || (CFG.types && CFG.types[0] && CFG.types[0].key) || '';
    fTitre.value = it.titre || '';
    fCorps.value = it.corps || '';
    fLien.value = it.lien || '';
    fEpingle.checked = !!it.epingle;
    fPublie.checked = !!it.publie;
    if (fCancel) fCancel.hidden = false;
    msg('');
  }

  if (fCancel) fCancel.addEventListener('click', function () { resetForm(); });

  if (form) form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (busy) return;
    var titre = fTitre.value.trim();
    if (!titre) return msg(CFG.need_title || 'Titre obligatoire.', true);
    if (!fType.value) return msg(CFG.need_type || 'Choisissez un type.', true);
    if (!fDate.value) return msg(CFG.need_date || 'Date obligatoire.', true);
    var lien = fLien.value.trim();
    if (lien && !/^https?:\/\//i.test(lien)) return msg(CFG.bad_link || 'Lien invalide.', true);

    var brave = {
      id: editingId || undefined,
      date: fDate.value, type: fType.value, titre: titre,
      corps: fCorps.value.trim(), lien: lien,
      epingle: fEpingle.checked, publie: fPublie.checked
    };
    var next;
    if (editingId) next = actus.map(function (b) { return String(b.id) === String(editingId) ? Object.assign({ id: editingId }, brave) : b; });
    else next = actus.concat([brave]);
    save(next, editingId ? (CFG.saved_update || 'Mis à jour.') : (CFG.saved_create || 'Créé.'));
  });

  // ---------- écriture ----------
  function save(next, okMsg) {
    if (busy) return;
    setBusy(true); msg(CFG.saving || 'Enregistrement…');
    authed('/.netlify/functions/save-actus', {
      method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(next)
    }).then(function (r) {
      return r.json().catch(function () { return {}; }).then(function (j) { return { ok: r.ok, status: r.status, j: j }; });
    }).then(function (x) {
      if (x.status === 401) { I.logout(); throw new Error('401'); }
      if (!x.ok) throw new Error((x.j && x.j.error) || ('HTTP ' + x.status));
      resetForm(); msg(okMsg || 'Enregistré.', false);
      return loadActus();             // re-synchronise depuis le serveur (source de vérité)
    }).catch(function (err) {
      msg((CFG.save_error || 'Échec') + ' ' + (err && err.message ? '(' + err.message + ')' : ''), true);
    }).then(function () { setBusy(false); });
  }

  // init date du jour au démarrage
  if (fDate) fDate.value = todayISO();
})();
