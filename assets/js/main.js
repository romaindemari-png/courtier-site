/* Gabarit — JS partagé (toutes pages).
   Chaque bloc est défensif : il ne s'exécute que si ses éléments existent,
   pour qu'un seul fichier serve l'accueil ET les pages d'expertise. */
(function () {
  // Données hero injectées par build.py (window.HERO = { words:[…], images:{…} }).
  // Le gabarit ne contient aucune donnée client : voir _src/data.py.
  var HERO = window.HERO || {};
  var P = HERO.images || {};
  var canHover = window.matchMedia('(hover:hover) and (pointer:fine)').matches;

  /* Hero — mot qui tourne en cut sec + photo au survol (accueil) */
  var rot = document.getElementById('rot'),
      box = document.getElementById('hphotoBox'),
      pim = document.getElementById('hphoto'),
      wcur = document.getElementById('wcur');
  if (rot && wcur && HERO.words && HERO.words.length) {
    var words = HERO.words, idx = 0, paused = false;
    setInterval(function () { if (paused) return; idx = (idx + 1) % words.length; wcur.textContent = words[idx]; }, 2000);
    if (canHover) {
      rot.addEventListener('mouseenter', function () { paused = true; if (pim) pim.src = P[words[idx]]; if (box) box.classList.add('show'); });
      rot.addEventListener('mouseleave', function () { paused = false; if (box) box.classList.remove('show'); });
    }
  }

  /* Révélations au scroll (toutes pages) */
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
  }, { threshold: .12 });
  document.querySelectorAll('.rv,.stg').forEach(function (el) { io.observe(el); });

  /* Accordéon de l'approche (accueil) */
  document.querySelectorAll('.acc-head').forEach(function (h) {
    h.addEventListener('click', function () {
      var item = h.parentElement, open = item.classList.contains('open');
      item.parentElement.querySelectorAll('.acc-item').forEach(function (x) { x.classList.remove('open'); });
      if (!open) item.classList.add('open');
    });
  });

  /* Image qui suit le curseur sur les cards (accueil) */
  var trail = document.getElementById('trail'), tim = document.getElementById('trailimg');
  if (trail && tim && canHover) {
    var tx = 0, ty = 0, cx = 0, cy = 0, raf = null;
    function loop() { cx += (tx - cx) * 0.2; cy += (ty - cy) * 0.2; trail.style.transform = 'translate(' + cx + 'px,' + cy + 'px) translate(-50%,-50%)'; raf = requestAnimationFrame(loop); }
    document.addEventListener('mousemove', function (e) { tx = e.clientX; ty = e.clientY; });
    document.querySelectorAll('.card[data-img]').forEach(function (c) {
      c.addEventListener('mouseenter', function () { tim.src = P[c.dataset.img]; cx = tx; cy = ty; trail.classList.add('show'); if (!raf) loop(); });
      c.addEventListener('mouseleave', function () { trail.classList.remove('show'); });
    });
  }
})();
