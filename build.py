#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GABARIT — générateur statique zéro-dépendance, réutilisable tel quel.
Ne contient AUCUNE donnée client : tout vient de _src/data.py.
Sortie 100 % statique (Netlify, sans build command) :
  index.html, expertises/<slug>/index.html, sitemap.xml, robots.txt, assets/css/tokens.css
Usage : python3 build.py
"""
import os, sys, json, datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "_src"))
import data as D

TODAY = datetime.date.today().isoformat()
OG_IMAGE = D.SITE + D.PORTRAIT["jpg"]
BANNER = ("<!-- FICHIER GÉNÉRÉ PAR build.py — NE PAS ÉDITER À LA MAIN. "
          "Modifier _src/ puis relancer python3 build.py -->")

def rd(p): return open(os.path.join(ROOT, p), encoding="utf-8").read()
def wr(p, c):
    fp = os.path.join(ROOT, p)
    os.makedirs(os.path.dirname(fp) or ".", exist_ok=True)
    open(fp, "w", encoding="utf-8").write(c)
def esc(s): return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
def att(s): return esc(s).replace('"', "&quot;")
def render(tpl, repl):
    for k, v in repl.items():
        tpl = tpl.replace(k, v)
    return tpl

base      = rd("_src/template/base.html")
header    = rd("_src/partials/header.html")
footer    = rd("_src/partials/footer.html")
home_t    = rd("_src/template/home.html")
expt_t    = rd("_src/template/expertise.html")
contact_t = rd("_src/template/contact.html")
merci_t   = rd("_src/template/merci.html")
legal_t   = rd("_src/template/mentions-legales.html")
actus_t   = rd("_src/template/actualites.html")

# ─────────────────────────── Fragments réutilisables ───────────────────────────
def picture(img, eager=False):
    # eager=True pour l'image prioritaire : pas de lazy + fetchpriority="high" (le reste reste lazy).
    prio = ' fetchpriority="high"' if eager else ' loading="lazy"'
    return ('<picture><source srcset="%s" type="image/webp">'
            '<img src="%s" alt="%s" width="%d" height="%d"%s></picture>'
            % (img["webp"], img["jpg"], att(img["alt"]), img["w"], img["h"], prio))

def tokens_css():
    c = D.COLORS
    root = ("--cream:%s;--cream2:%s;--ink:%s;--dark:%s;--onDark:%s;--accent:%s;"
            "--grad:linear-gradient(120deg,%s,%s);--muted:%s;--mutedDk:%s;--line:%s;--lineDk:%s"
            % (c["cream"], c["cream2"], c["ink"], c["dark"], c["onDark"], c["accent"],
               c["gradFrom"], c["gradTo"], c["muted"], c["mutedDk"], c["line"], c["lineDk"]))
    return "/* GÉNÉRÉ PAR build.py depuis _src/data.py (COLORS) — NE PAS ÉDITER À LA MAIN */\n:root{%s}\n" % root

# ─────────────────────────── Chrome (header / footer) ──────────────────────────
def _href(prefix, h):
    # Lien absolu (page, ex. /contact/) tel quel ; ancre (#cabinet) préfixée selon la page.
    return h if h.startswith("/") else prefix + h

def _nav(prefix, items, cls=""):
    a = ' class="%s"' % cls if cls else ""
    return "".join('<a%s href="%s">%s</a>' % (a, _href(prefix, n["href"]), esc(n["label"])) for n in items)

def chrome(prefix):
    mm_items = D.NAV + [D.NAV_CONTACT]
    mm = "\n  ".join(
        '<a href="%s">%s</a>' % (_href(prefix, n["href"]), esc(n["label"])) for n in mm_items)
    h = render(header, {
        "{{HOME}}": prefix, "{{BRAND}}": esc(D.BRAND), "{{MONOGRAM}}": esc(D.MONOGRAM),
        "{{NAV_LINKS}}": _nav(prefix, D.NAV, "lnk"),
        "{{NAV_CTA_HREF}}": _href(prefix, D.NAV_CTA["href"]), "{{NAV_CTA_LABEL}}": esc(D.NAV_CTA["label"]),
        "{{MM_LINKS}}": mm,
    })
    f = render(footer, {
        "{{HOME}}": prefix, "{{MONOGRAM}}": esc(D.MONOGRAM),
        "{{FOOTER_NAV}}": _nav(prefix, mm_items),
        "{{COPYRIGHT}}": esc(D.COPYRIGHT), "{{CREDIT}}": esc(D.CREDIT),
    })
    return h, f

def page(title, desc, canonical, jsonld, body, prefix, robots="index,follow"):
    h, f = chrome(prefix)
    out = render(base, {
        "{{TITLE}}": att(title), "{{OG_TITLE}}": att(title), "{{DESC}}": att(desc),
        "{{SITE_NAME}}": att(D.SITE_NAME), "{{CANONICAL}}": att(canonical), "{{ROBOTS}}": robots,
        "{{OG_IMAGE}}": att(OG_IMAGE), "{{JSONLD}}": jsonld,
        "{{HEADER}}": h, "{{BODY}}": body, "{{FOOTER}}": f,
    })
    return out.replace("<!DOCTYPE html>", "<!DOCTYPE html>\n" + BANNER, 1)

# ─────────────────────────── JSON-LD ───────────────────────────────────────────
def ld(obj):
    return '<script type="application/ld+json">\n%s\n</script>' % json.dumps(obj, ensure_ascii=False, indent=2)

def home_jsonld():
    comment = (
        "<!-- JSON-LD (accueil) — données factuelles uniquement, aucun avis/note/récompense (YMYL).\n"
        "     À CONFIRMER PAR LE CLIENT, puis réintégrer dans le bloc ci-dessous :\n"
        '       "telephone": "+33 ..."   (n° du cabinet — à fournir)\n'
        '       "email": "%s"   (à confirmer)\n'
        '       "address": { "@type": "PostalAddress", "streetAddress": "%s",\n'
        '                    "postalCode": "%s", "addressLocality": "%s", "addressCountry": "FR" }   (à confirmer)\n'
        "       n° de toque / barreau si fourni\n"
        "-->" % (D.CONTACT["email"], D.CONTACT["street"], D.CONTACT["postal"], D.CONTACT["city"]))
    obj = {
        "@context": "https://schema.org",
        "@type": ["LegalService", "Attorney"],
        "@id": D.SITE + "/#cabinet",
        "name": D.SITE_NAME,
        "description": D.LD_DESCRIPTION,
        "url": D.SITE + "/",
        "image": OG_IMAGE,
        "areaServed": {"@type": "City", "name": D.LOCATION},
        "foundingDate": D.CONTACT["founding_year"],
        "knowsAbout": D.KNOWS_ABOUT,
        "founder": {"@type": "Person", "name": D.PERSON["name"], "jobTitle": D.PERSON["jobTitle"],
                    "memberOf": {"@type": "Organization", "name": D.PERSON["barreau"]}},
    }
    return comment + "\n" + ld(obj)

def service_jsonld(d):
    return ld({
        "@context": "https://schema.org",
        "@type": "Service",
        "name": d["domain"],
        "serviceType": d["domain"],
        "description": d["promise"],
        "url": "%s/expertises/%s/" % (D.SITE, d["slug"]),
        "areaServed": {"@type": "City", "name": D.LOCATION},
        "provider": {"@type": ["LegalService", "Attorney"], "name": D.SITE_NAME, "url": D.SITE + "/"},
    })

def breadcrumb_jsonld(items):  # items = [(nom, url), …] dans l'ordre du fil d'ariane
    return ld({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": name, "item": url}
            for i, (name, url) in enumerate(items)
        ],
    })

# ─────────────────────────── Corps accueil ─────────────────────────────────────
def meta_html():  # coordonnées (accueil + page contact) — valeurs brutes (peuvent contenir <br>)
    return "\n".join('      <div><div class="k">%s</div><p>%s</p></div>' % (esc(k), v)
                     for k, v in D.CONTACT_SECTION["meta"])

def home_body():
    config = '<script type="application/json" id="hero-data">%s</script>' % json.dumps(
        {"words": D.HERO_WORDS, "images": D.HERO_IMAGES}, ensure_ascii=False)
    stats = "\n".join('          <div><div class="n serif">%s</div><div class="k">%s</div></div>'
                      % (esc(n), esc(k)) for n, k in D.CABINET["stats"])
    cards = []
    for i, d in enumerate(D.DOMAINS, 1):
        c = d["card"]
        cards.append(
            '      <a class="card" href="/expertises/%s/" data-img="%s"><span class="num serif">%02d</span>'
            '<div class="mid"><span class="lab">%s</span><h3>%s</h3><p>%s</p></div>'
            '<span class="ico">%s</span></a>'
            % (d["slug"], c["img"], i, esc(c["label"]), esc(c["title"]), esc(c["desc"]), c["icon"]))
    items = []
    for j, (h3, body) in enumerate(D.APPROCHE["items"]):
        items.append('        <div class="acc-item%s"><div class="acc-head"><h3>%s</h3>'
                     '<span class="pm"></span></div><div class="acc-body"><p>%s</p></div></div>'
                     % (" open" if j == 0 else "", esc(h3), esc(body)))
    return render(home_t, {
        "{{HERO_CONFIG}}": config,
        "{{HERO_BASELINE}}": esc(D.HERO["baseline"]),
        "{{HERO_TITLE_BEFORE}}": esc(D.HERO["title_before"]),
        "{{HERO_TITLE_AFTER_PREFIX}}": esc(D.HERO["title_after_prefix"]),
        "{{HERO_FIRST_WORD}}": esc(D.HERO["first_word"]),
        "{{HERO_TITLE_AFTER_SUFFIX}}": esc(D.HERO["title_after_suffix"]),
        "{{PORTRAIT}}": picture(D.PORTRAIT, eager=True),
        "{{CABINET_EYEBROW}}": esc(D.CABINET["eyebrow"]),
        "{{CABINET_TITLE}}": D.CABINET["title_html"],
        "{{CABINET_BODY}}": esc(D.CABINET["body"]),
        "{{CABINET_STATS}}": stats,
        "{{EXPERTISES_EYEBROW}}": esc(D.EXPERTISES["eyebrow"]),
        "{{EXPERTISES_TITLE}}": esc(D.EXPERTISES["title"]),
        "{{CARDS}}": "\n".join(cards),
        "{{APPROCHE_EYEBROW}}": esc(D.APPROCHE["eyebrow"]),
        "{{APPROCHE_TITLE}}": esc(D.APPROCHE["title"]),
        "{{APPROCHE_ITEMS}}": "\n".join(items),
        "{{APPROCHE_IMG}}": picture(D.APPROCHE_IMG),
        "{{ACTUS_CONFIG}}": actus_config(),
        "{{ACTUS_HOME_EYEBROW}}": esc(D.ACTUS["home_eyebrow"]),
        "{{ACTUS_HOME_TITLE}}": esc(D.ACTUS["home_title"]),
        "{{ACTUS_SEE_ALL}}": esc(D.ACTUS["see_all"]),
        "{{ACTUS_LOADING}}": esc(D.ACTUS["loading"]),
        "{{MANIFESTO_QUOTE}}": D.MANIFESTO["quote_html"],
        "{{MANIFESTO_SUP}}": esc(D.MANIFESTO["sup"]),
        "{{CONTACT_EYEBROW}}": esc(D.CONTACT_SECTION["eyebrow"]),
        "{{CONTACT_TITLE}}": D.CONTACT_SECTION["title_html"],
        "{{CONTACT_CTA}}": esc(D.CONTACT_SECTION["cta_label"]),
        "{{CONTACT_SECONDARY}}": esc(D.CONTACT_SECTION["secondary_label"]),
        "{{CONTACT_META}}": meta_html(),
    })

# ─────────────────────────── Corps contact / merci ─────────────────────────────
def contact_options():  # <select> peuplé depuis DOMAINS
    return "\n".join('            <option value="%s">%s</option>' % (att(d["domain"]), esc(d["domain"]))
                     for d in D.DOMAINS)

def contact_body():
    return render(contact_t, {
        "{{EYEBROW}}": esc(D.CONTACT_PAGE["eyebrow"]),
        "{{H1}}": D.CONTACT_PAGE["h1_html"],
        "{{INTRO}}": esc(D.CONTACT_PAGE["intro"]),
        "{{SUJET_OPTIONS}}": contact_options(),
        "{{CONTACT_META}}": meta_html(),
    })

def merci_body():
    return render(merci_t, {
        "{{EYEBROW}}": esc(D.MERCI_PAGE["eyebrow"]),
        "{{H1}}": D.MERCI_PAGE["h1_html"],
        "{{BODY}}": esc(D.MERCI_PAGE["body"]),
    })

def legal_body():  # valeurs connues injectées ; le reste = [À COMPLÉTER] dans le template
    return render(legal_t, {
        "{{EYEBROW}}": esc(D.LEGAL_PAGE["eyebrow"]),
        "{{H1}}": esc(D.LEGAL_PAGE["h1"]),
        "{{INTRO}}": esc(D.LEGAL_PAGE["intro"]),
        "{{BRAND}}": esc(D.BRAND),
        "{{LOCATION}}": esc(D.LOCATION),
    })

# ─────────────────────────── Module Actualités (lecture seule) ──────────────────
def actus_config():  # config (libellés/couleurs/états) en JSON non exécutable → lu par actus.js
    cfg = {"types": D.ACTUS["types"], "empty": D.ACTUS["empty"], "error": D.ACTUS["error"]}
    return '<script type="application/json" id="actus-config">%s</script>' % json.dumps(cfg, ensure_ascii=False)

def actus_filters():
    return "\n".join(
        '      <button type="button" class="actus-f" data-filter="%s" aria-pressed="false">%s</button>'
        % (t["key"], esc(t["label"])) for t in D.ACTUS["types"])

def actualites_body():
    return render(actus_t, {
        "{{ACTUS_CONFIG}}": actus_config(),
        "{{ACTUS_PAGE_EYEBROW}}": esc(D.ACTUS["page_eyebrow"]),
        "{{ACTUS_PAGE_H1}}": esc(D.ACTUS["page_h1"]),
        "{{ACTUS_PAGE_INTRO}}": esc(D.ACTUS["page_intro"]),
        "{{ACTUS_FILTER_ALL}}": esc(D.ACTUS["filter_all"]),
        "{{ACTUS_FILTERS}}": actus_filters(),
        "{{ACTUS_LOADING}}": esc(D.ACTUS["loading"]),
    })

# ─────────────────────────── Corps expertise ───────────────────────────────────
def steps_html():
    return "\n".join('      <div class="step"><div class="sn serif">%02d</div><h3>%s</h3><p>%s</p></div>'
                     % (i, esc(h3), esc(body)) for i, (h3, body) in enumerate(D.STEPS, 1))

def prestations_html(items):
    return "\n".join('      <div class="it"><span class="pn serif">%02d</span>'
                     '<div class="pt"><h3>%s</h3><p>%s</p></div></div>'
                     % (i, esc(t), esc(desc)) for i, (t, desc) in enumerate(items, 1))

def others_html(slug):
    return "\n".join('      <a href="/expertises/%s/"><span class="k">Expertise</span><h3>%s</h3></a>'
                     % (d["slug"], esc(d["domain"])) for d in D.DOMAINS if d["slug"] != slug)

def expertise_body(d):
    return render(expt_t, {
        "{{CRUMB}}": esc(d["domain"]), "{{DOMAIN}}": esc(d["domain"]),
        "{{H1}}": esc(d["domain"]), "{{PROMISE}}": esc(d["promise"]),
        "{{PROBLEM}}": esc(d["problem"]), "{{AUDIENCE}}": esc(d["audience"]),
        "{{PRESTATIONS}}": prestations_html(d["prestations"]),
        "{{STEPS}}": steps_html(), "{{OTHERS}}": others_html(d["slug"]),
    })

# ─────────────────────────── Build ─────────────────────────────────────────────
def build():
    wr("assets/css/tokens.css", tokens_css())
    wr("index.html", page(D.HOME_TITLE, D.HOME_DESC, D.SITE + "/", home_jsonld(), home_body(), ""))

    for d in D.DOMAINS:
        canonical = "%s/expertises/%s/" % (D.SITE, d["slug"])
        crumbs = breadcrumb_jsonld([("Accueil", D.SITE + "/"),
                                    ("Expertises", D.SITE + "/#expertises"),
                                    (d["domain"], canonical)])
        wr("expertises/%s/index.html" % d["slug"],
           page(d["title"], d["desc"], canonical, service_jsonld(d) + "\n" + crumbs, expertise_body(d), "/"))

    # Page contact (formulaire Netlify) + confirmation (noindex, hors sitemap)
    contact_crumbs = breadcrumb_jsonld([("Accueil", D.SITE + "/"), ("Contact", D.SITE + "/contact/")])
    wr("contact/index.html",
       page(D.CONTACT_PAGE["title"], D.CONTACT_PAGE["desc"], D.SITE + "/contact/", contact_crumbs, contact_body(), "/"))
    wr("merci/index.html",
       page(D.MERCI_PAGE["title"], D.MERCI_PAGE["desc"], D.SITE + "/merci/", "", merci_body(), "/", robots="noindex,follow"))
    # Mentions légales — accessible via le footer ; noindex tant que des [À COMPLÉTER] subsistent
    wr("mentions-legales/index.html",
       page(D.LEGAL_PAGE["title"], D.LEGAL_PAGE["desc"], D.SITE + "/mentions-legales/", "", legal_body(), "/", robots="noindex,follow"))
    # Actualités (lecture seule — contenu injecté par actus.js depuis la Function)
    actus_crumbs = breadcrumb_jsonld([("Accueil", D.SITE + "/"), ("Actualités", D.SITE + "/actualites/")])
    wr("actualites/index.html",
       page(D.ACTUS["page_title"], D.ACTUS["page_desc"], D.SITE + "/actualites/", actus_crumbs, actualites_body(), "/"))

    urls = ([(D.SITE + "/", "1.0")]
            + [("%s/expertises/%s/" % (D.SITE, d["slug"]), "0.8") for d in D.DOMAINS]
            + [(D.SITE + "/contact/", "0.7"), (D.SITE + "/actualites/", "0.6")])
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, prio in urls:
        sm += ['  <url>', '    <loc>%s</loc>' % loc, '    <lastmod>%s</lastmod>' % TODAY,
               '    <changefreq>monthly</changefreq>', '    <priority>%s</priority>' % prio, '  </url>']
    sm.append('</urlset>\n')
    wr("sitemap.xml", "\n".join(sm))
    wr("robots.txt", "User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % D.SITE)

    print("Build OK — %d page(s) d'expertise + contact/merci :" % len(D.DOMAINS))
    print("  - index.html  + assets/css/tokens.css")
    for d in D.DOMAINS:
        print("  - expertises/%s/index.html" % d["slug"])
    print("  - contact/index.html, merci/index.html, mentions-legales/index.html")
    print("  - actualites/index.html")
    print("  - sitemap.xml, robots.txt")

if __name__ == "__main__":
    build()
