/* Gabarit — JS partagé (toutes pages).
   Chaque bloc est défensif : il ne s'exécute que si ses éléments existent,
   pour qu'un seul fichier serve l'accueil ET les pages d'expertise. */
(function () {
  var HERO = window.HERO || {};
  var P = HERO.images || {};
  var canHover = window.matchMedia('(hover:hover) and (pointer:fine)').matches;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var HEADER_H = 74;

  // Chorégraphie active uniquement si : mouvement autorisé ET les 3 libs présentes.
  var gsap = window.gsap, ST = window.ScrollTrigger;
  var animate = !reduce && !!window.Lenis && !!gsap && !!ST;
  var lenis = null;

  /* ---------- Smooth scroll (Lenis) + synchro GSAP ticker ---------- */
  if (animate) {
    document.documentElement.classList.add('js-anim');
    gsap.registerPlugin(ST);

    // lerp doux ; smoothWheel seulement → le tactile (iOS) reste 100 % natif.
    lenis = new Lenis({ lerp: 0.09, smoothWheel: true });
    lenis.on('scroll', ST.update);
    gsap.ticker.add(function (t) { lenis.raf(t * 1000); });
    gsap.ticker.lagSmoothing(0);

    // Menu mobile ouvert → stop Lenis (sinon scroll bloqué) ; fermé → start.
    var mmEl = document.getElementById('mm');
    if (mmEl) new MutationObserver(function () {
      if (mmEl.classList.contains('open')) lenis.stop(); else lenis.start();
    }).observe(mmEl, { attributes: true, attributeFilter: ['class'] });

    // Ancres internes (#section) via lenis.scrollTo — préserve le smooth.
    // (Les liens inter-pages "/#section" commencent par "/" → navigation normale.)
    document.querySelectorAll('a[href^="#"]').forEach(function (a) {
      a.addEventListener('click', function (e) {
        var id = a.getAttribute('href');
        if (id.length < 2) return;                 // ignore href="#"
        var target = document.querySelector(id);
        if (!target) return;
        e.preventDefault();
        lenis.start();                             // au cas où le menu l'a stoppé
        lenis.scrollTo(target, { offset: -HEADER_H });
      });
    });
  }

  /* ---------- Hero — mot qui tourne en cut sec + photo au survol (accueil) ---------- */
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

  /* ---------- Accordéon de l'approche (accueil) ---------- */
  document.querySelectorAll('.acc-head').forEach(function (h) {
    h.addEventListener('click', function () {
      var item = h.parentElement, open = item.classList.contains('open');
      item.parentElement.querySelectorAll('.acc-item').forEach(function (x) { x.classList.remove('open'); });
      if (!open) item.classList.add('open');
      // la hauteur change → recalage des positions ScrollTrigger après la transition
      if (animate) setTimeout(function () { ST.refresh(); }, 560);
    });
  });

  /* ---------- Image qui suit le curseur sur les cards (accueil) — indépendant de Lenis ---------- */
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

  /* ---------- Révélations chorégraphiées + parallaxe (GSAP) ; sinon fallback ---------- */
  if (animate) {
    // fade + montée
    gsap.utils.toArray('.rv').forEach(function (el) {
      gsap.to(el, { opacity: 1, y: 0, duration: 1, ease: 'power3.out',
        scrollTrigger: { trigger: el, start: 'top 88%', once: true } });
    });
    // groupes avec léger stagger
    gsap.utils.toArray('.stg').forEach(function (grp) {
      gsap.to(grp.children, { opacity: 1, y: 0, duration: 0.9, ease: 'power3.out', stagger: 0.09,
        scrollTrigger: { trigger: grp, start: 'top 86%', once: true } });
    });
    // parallaxe douce sur les visuels (image légèrement zoomée pour ne pas révéler les bords)
    gsap.utils.toArray('.cab .pf, .appr .vis').forEach(function (boxEl) {
      var im = boxEl.querySelector('img');
      if (!im) return;
      gsap.set(im, { scale: 1.12, transformOrigin: '50% 50%' });
      gsap.fromTo(im, { yPercent: -5 }, { yPercent: 5, ease: 'none',
        scrollTrigger: { trigger: boxEl, start: 'top bottom', end: 'bottom top', scrub: true } });
    });
  } else if (!reduce) {
    // Fallback (libs absentes / iOS récalcitrant) : reveals via IntersectionObserver, scroll natif.
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { threshold: .12 });
    document.querySelectorAll('.rv,.stg').forEach(function (el) { io.observe(el); });
  }
  // (reduced-motion : le CSS rend déjà tout visible — aucune init.)
})();
