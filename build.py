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

base    = rd("_src/template/base.html")
header  = rd("_src/partials/header.html")
footer  = rd("_src/partials/footer.html")
home_t  = rd("_src/template/home.html")
expt_t  = rd("_src/template/expertise.html")

# ─────────────────────────── Fragments réutilisables ───────────────────────────
def picture(img):
    return ('<picture><source srcset="%s" type="image/webp">'
            '<img src="%s" alt="%s" width="%d" height="%d" loading="lazy"></picture>'
            % (img["webp"], img["jpg"], att(img["alt"]), img["w"], img["h"]))

def tokens_css():
    c = D.COLORS
    root = ("--cream:%s;--cream2:%s;--ink:%s;--dark:%s;--onDark:%s;--accent:%s;"
            "--grad:linear-gradient(120deg,%s,%s);--muted:%s;--mutedDk:%s;--line:%s;--lineDk:%s"
            % (c["cream"], c["cream2"], c["ink"], c["dark"], c["onDark"], c["accent"],
               c["gradFrom"], c["gradTo"], c["muted"], c["mutedDk"], c["line"], c["lineDk"]))
    return "/* GÉNÉRÉ PAR build.py depuis _src/data.py (COLORS) — NE PAS ÉDITER À LA MAIN */\n:root{%s}\n" % root

# ─────────────────────────── Chrome (header / footer) ──────────────────────────
def _nav(prefix, items, cls=""):
    a = ' class="%s"' % cls if cls else ""
    return "".join('<a%s href="%s%s">%s</a>' % (a, prefix, n["href"], esc(n["label"])) for n in items)

def chrome(prefix):
    mm_items = D.NAV + [{"href": "#contact", "label": "Contact"}]
    mm = "\n  ".join(
        '<a href="%s%s" onclick="document.getElementById(\'mm\').classList.remove(\'open\')">%s</a>'
        % (prefix, n["href"], esc(n["label"])) for n in mm_items)
    h = render(header, {
        "{{HOME}}": prefix, "{{BRAND}}": esc(D.BRAND), "{{MONOGRAM}}": esc(D.MONOGRAM),
        "{{NAV_LINKS}}": _nav(prefix, D.NAV, "lnk"),
        "{{NAV_CTA_HREF}}": prefix + D.NAV_CTA["href"], "{{NAV_CTA_LABEL}}": esc(D.NAV_CTA["label"]),
        "{{MM_LINKS}}": mm,
    })
    f = render(footer, {
        "{{HOME}}": prefix, "{{MONOGRAM}}": esc(D.MONOGRAM),
        "{{FOOTER_NAV}}": _nav(prefix, mm_items),
        "{{COPYRIGHT}}": esc(D.COPYRIGHT), "{{CREDIT}}": esc(D.CREDIT),
    })
    return h, f

def page(title, desc, canonical, jsonld, body, prefix):
    h, f = chrome(prefix)
    out = render(base, {
        "{{TITLE}}": att(title), "{{OG_TITLE}}": att(title), "{{DESC}}": att(desc),
        "{{SITE_NAME}}": att(D.SITE_NAME), "{{CANONICAL}}": att(canonical),
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

# ─────────────────────────── Corps accueil ─────────────────────────────────────
def home_body():
    config = "<script>window.HERO={words:%s,images:%s};</script>" % (
        json.dumps(D.HERO_WORDS, ensure_ascii=False), json.dumps(D.HERO_IMAGES, ensure_ascii=False))
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
    meta = "\n".join('      <div><div class="k">%s</div><p>%s</p></div>' % (esc(k), v)
                     for k, v in D.CONTACT_SECTION["meta"])
    return render(home_t, {
        "{{HERO_CONFIG}}": config,
        "{{HERO_BASELINE}}": esc(D.HERO["baseline"]),
        "{{HERO_TITLE_BEFORE}}": esc(D.HERO["title_before"]),
        "{{HERO_TITLE_AFTER_PREFIX}}": esc(D.HERO["title_after_prefix"]),
        "{{HERO_FIRST_WORD}}": esc(D.HERO["first_word"]),
        "{{HERO_TITLE_AFTER_SUFFIX}}": esc(D.HERO["title_after_suffix"]),
        "{{PORTRAIT}}": picture(D.PORTRAIT),
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
        "{{MANIFESTO_QUOTE}}": D.MANIFESTO["quote_html"],
        "{{MANIFESTO_SUP}}": esc(D.MANIFESTO["sup"]),
        "{{CONTACT_EYEBROW}}": esc(D.CONTACT_SECTION["eyebrow"]),
        "{{CONTACT_TITLE}}": D.CONTACT_SECTION["title_html"],
        "{{CONTACT_CTA}}": esc(D.CONTACT_SECTION["cta_label"]),
        "{{CONTACT_SECONDARY}}": esc(D.CONTACT_SECTION["secondary_label"]),
        "{{CONTACT_META}}": meta,
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
        wr("expertises/%s/index.html" % d["slug"],
           page(d["title"], d["desc"], canonical, service_jsonld(d), expertise_body(d), "/"))

    urls = [(D.SITE + "/", "1.0")] + [("%s/expertises/%s/" % (D.SITE, d["slug"]), "0.8") for d in D.DOMAINS]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, prio in urls:
        sm += ['  <url>', '    <loc>%s</loc>' % loc, '    <lastmod>%s</lastmod>' % TODAY,
               '    <changefreq>monthly</changefreq>', '    <priority>%s</priority>' % prio, '  </url>']
    sm.append('</urlset>\n')
    wr("sitemap.xml", "\n".join(sm))
    wr("robots.txt", "User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % D.SITE)

    print("Build OK — %d page(s) d'expertise :" % len(D.DOMAINS))
    print("  - index.html  + assets/css/tokens.css")
    for d in D.DOMAINS:
        print("  - expertises/%s/index.html" % d["slug"])
    print("  - sitemap.xml, robots.txt")

if __name__ == "__main__":
    build()
