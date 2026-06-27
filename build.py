#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Générateur statique zéro-dépendance du site Nicolas Courtier.
Source unique de vérité : _src/ (partials header/footer, templates, contenu ci-dessous).
Sortie : index.html, expertises/<slug>/index.html, sitemap.xml, robots.txt (100 % statique, Netlify).
Usage : python3 build.py   (à relancer après toute modif d'un partial/template/contenu)
"""
import os, datetime

# ⚠️⚠️ SITE — À CONFIRMER. Le domaine final n'est PAS tranché (refonte WordPress en cours,
# nom de domaine de CE site à décider avec le client). Placeholder = URL de preview Netlify.
# Au déploiement définitif : remplacer par le vrai domaine puis relancer `python3 build.py`.
SITE = "https://courtier-site.netlify.app"  # ← À CONFIRMER (preview Netlify provisoire)
OG_IMAGE = SITE + "/assets/img/portrait-nicolas-courtier.jpg"
TODAY = datetime.date.today().isoformat()

ROOT = os.path.dirname(os.path.abspath(__file__))
def rd(p): return open(os.path.join(ROOT, p), encoding="utf-8").read()
def wr(p, c):
    fp = os.path.join(ROOT, p)
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    open(fp, "w", encoding="utf-8").write(c)

def esc(s):   # texte -> HTML
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
def att(s):   # texte -> valeur d'attribut
    return esc(s).replace('"', "&quot;")

base   = rd("_src/template/base.html")
header = rd("_src/partials/header.html")
footer = rd("_src/partials/footer.html")
home_body = rd("_src/template/home.html")
expt   = rd("_src/template/expertise.html")

def render(repl, tpl):
    for k, v in repl.items():
        tpl = tpl.replace(k, v)
    return tpl

BANNER = ("<!-- FICHIER GÉNÉRÉ PAR build.py — NE PAS ÉDITER À LA MAIN. "
          "Modifier _src/ puis relancer python3 build.py -->")

def page(title, desc, canonical, jsonld, body, home_prefix):
    h = header.replace("{{HOME}}", home_prefix)
    f = footer.replace("{{HOME}}", home_prefix)
    out = render({
        "{{TITLE}}": att(title), "{{OG_TITLE}}": att(title),
        "{{DESC}}": att(desc), "{{CANONICAL}}": att(canonical),
        "{{OG_IMAGE}}": att(OG_IMAGE), "{{JSONLD}}": jsonld,
        "{{HEADER}}": h, "{{BODY}}": body, "{{FOOTER}}": f,
    }, base)
    # Bandeau anti-édition, juste après le doctype (n'affecte pas le mode de rendu)
    return out.replace("<!DOCTYPE html>", "<!DOCTYPE html>\n" + BANNER, 1)

# ───────────────────────── CONTENU DES 4 EXPERTISES (intégré tel quel) ─────────────────────────
DOMAINS = [
  {
    "slug": "propriete-intellectuelle", "domain": "Propriété intellectuelle",
    "title": "Propriété intellectuelle — Nicolas Courtier, avocat à Marseille",
    "desc": "Dépôt et défense de marques, dessins & modèles, droit d'auteur, noms de domaine, contrefaçon. Nicolas Courtier, avocat à Marseille, protège vos créations.",
    "promise": "Donner une forme juridique à ce que vous avez créé — et le défendre.",
    "problem": "Une marque, un logo, un produit, un contenu ont de la valeur tant qu'on peut prouver qu'ils sont à vous. Sans dépôt ni cadre, cette valeur est exposée.",
    "prestations": [
        ("Dépôt et surveillance de marques (INPI, EUIPO)", "Je sécurise votre marque du dépôt à la surveillance, en France et en Europe, et j'agis dès qu'une marque tierce empiète sur la vôtre."),
        ("Protection des dessins & modèles", "Je protège l'apparence de vos produits (formes, motifs, packaging) pour empêcher les copies."),
        ("Droit d'auteur et cession de droits", "Je cadre la titularité de vos créations et rédige les cessions, pour que vos droits soient clairs et opposables."),
        ("Contrats de licence", "Je structure l'exploitation de vos actifs (licences, redevances, exclusivités) en protégeant vos intérêts."),
        ("Gestion des noms de domaine", "Je récupère et défends vos noms de domaine face au cybersquatting et aux usages abusifs."),
        ("Actions en contrefaçon", "J'engage et conduis les actions quand vos droits sont copiés ou exploités sans autorisation."),
    ],
    "audience": "créateurs, studios, marques, startups, PME qui déposent ou défendent un actif.",
  },
  {
    "slug": "droit-du-numerique", "domain": "Droit du numérique",
    "title": "Droit du numérique — Nicolas Courtier, avocat à Marseille",
    "desc": "Contrats IT/SaaS, CGV/CGU, conformité NIS2 et cadrage IA Act. Nicolas Courtier, avocat à Marseille, sécurise vos outils numériques de l'idée à l'exploitation.",
    "promise": "Sécuriser vos contrats et vos outils numériques, de l'idée à l'exploitation.",
    "problem": "Sites, apps, SaaS, IA reposent sur des contrats et des obligations (NIS2, IA Act) souvent signés trop vite ou absents.",
    "prestations": [
        ("Contrats IT et SaaS", "Je rédige et négocie vos contrats de prestation, d'abonnement et de niveau de service pour éviter les angles morts."),
        ("CGV, CGU et mentions légales", "Je mets vos conditions et obligations légales en conformité avec vos usages réels."),
        ("Conformité NIS2", "J'accompagne votre mise en conformité aux obligations de cybersécurité issues de la directive NIS2."),
        ("Cadrage juridique des projets IA (IA Act)", "J'évalue vos usages de l'IA au regard du règlement européen et sécurise leur déploiement."),
        ("Contrats d'hébergement et de prestation", "Je verrouille la responsabilité, la réversibilité et la protection des données dans vos contrats techniques."),
    ],
    "audience": "éditeurs de logiciels, agences, e-commerçants, porteurs de projets tech.",
  },
  {
    "slug": "donnees-personnelles", "domain": "Données personnelles",
    "title": "Données personnelles & RGPD — Nicolas Courtier, Marseille",
    "desc": "Audit RGPD, DPO externalisé, registre, transferts hors UE, contrôles CNIL. Nicolas Courtier, avocat à Marseille, fait de la conformité un réflexe.",
    "promise": "La conformité comme un réflexe, pas une contrainte.",
    "problem": "Le RGPD n'est pas un document qu'on classe — c'est un pilotage continu, sous peine de sanctions CNIL.",
    "prestations": [
        ("Audit et mise en conformité RGPD", "Je cartographie vos traitements et établis un plan de conformité priorisé, pas un classeur qui dort."),
        ("DPO externalisé", "J'assure la fonction de délégué à la protection des données, en relais permanent de vos équipes."),
        ("Registre des traitements", "Je construis et tiens à jour le registre exigé par la CNIL."),
        ("Transferts hors UE", "Je sécurise vos flux de données internationaux (clauses types, garanties)."),
        ("Contrôle ou violation de données", "Je vous accompagne en cas de contrôle CNIL ou de fuite de données, de la réaction à la notification."),
    ],
    "audience": "entreprises traitant des données clients, e-commerce, santé, RH, secteur public.",
  },
  {
    "slug": "contentieux", "domain": "Contentieux",
    "title": "Contentieux — Nicolas Courtier, avocat à Marseille",
    "desc": "Contrefaçon, concurrence déloyale, e-réputation, saisies-contrefaçon. Nicolas Courtier, avocat à Marseille, défend vos droits devant toutes juridictions.",
    "promise": "Quand le dialogue ne suffit plus, défendre vos droits — partout.",
    "problem": "Contrefaçon, concurrence déloyale, atteinte à la réputation : il faut agir vite et au bon endroit.",
    "prestations": [
        ("Contrefaçon et concurrence déloyale", "Je conduis les actions pour faire cesser l'atteinte et obtenir réparation."),
        ("E-réputation et retrait de contenus", "J'obtiens le retrait de contenus illicites et la protection de votre image en ligne."),
        ("Saisies-contrefaçon", "Je fais constater et saisir les preuves avant d'agir au fond."),
        ("Négociation et transaction", "Je privilégie la résolution amiable quand elle sert mieux vos intérêts qu'un procès."),
        ("Représentation devant les juridictions", "Je vous représente devant les tribunaux civils et commerciaux compétents."),
    ],
    "audience": "toute entreprise ou créateur dont un droit immatériel est attaqué.",
  },
]

def prestations_html(items):
    # Numéro PST + titre PST + phrase descriptive (David Extra Light, muted), toujours visible.
    out = []
    for i, (title, desc) in enumerate(items, 1):
        out.append('      <div class="it"><span class="pn serif">%02d</span>'
                   '<div class="pt"><h3>%s</h3><p>%s</p></div></div>' % (i, esc(title), esc(desc)))
    return "\n".join(out)

def others_html(current_slug):
    out = []
    for d in DOMAINS:
        if d["slug"] == current_slug:
            continue
        out.append('      <a href="/expertises/%s/"><span class="k">Expertise</span><h3>%s</h3></a>'
                   % (d["slug"], esc(d["domain"])))
    return "\n".join(out)

# ───────────────────────── JSON-LD ─────────────────────────
HOME_JSONLD = '''<!-- JSON-LD (accueil) — données factuelles uniquement, aucun avis/note/récompense (YMYL).
     À CONFIRMER PAR LE CLIENT, puis réintégrer dans le bloc ci-dessous :
       "telephone": "+33 ..."   (n° du cabinet — à fournir)
       "email": "contact@courtier-avocats.com"   (à confirmer)
       "address": { "@type": "PostalAddress", "streetAddress": "2 rue Odette Jasse",
                    "postalCode": "13015", "addressLocality": "Marseille", "addressCountry": "FR" }   (à confirmer)
       n° de toque / barreau si fourni
-->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": ["LegalService", "Attorney"],
  "@id": "%(site)s/#cabinet",
  "name": "Nicolas Courtier — Avocat",
  "description": "Avocat au barreau de Marseille depuis 1991. Propriété intellectuelle, droit du numérique, données personnelles (RGPD) et contentieux — du conseil à la défense.",
  "url": "%(site)s/",
  "image": "%(img)s",
  "areaServed": { "@type": "City", "name": "Marseille" },
  "foundingDate": "1991",
  "knowsAbout": ["Propriété intellectuelle", "Droit du numérique", "Données personnelles et RGPD", "Contentieux"],
  "founder": {
    "@type": "Person",
    "name": "Nicolas Courtier",
    "jobTitle": "Avocat",
    "memberOf": { "@type": "Organization", "name": "Barreau de Marseille" }
  }
}
</script>''' % {"site": SITE, "img": OG_IMAGE}

def service_jsonld(d):
    return ('<script type="application/ld+json">\n'
            '{\n'
            '  "@context": "https://schema.org",\n'
            '  "@type": "Service",\n'
            '  "name": "%(name)s",\n'
            '  "serviceType": "%(name)s",\n'
            '  "description": "%(promise)s",\n'
            '  "url": "%(site)s/expertises/%(slug)s/",\n'
            '  "areaServed": { "@type": "City", "name": "Marseille" },\n'
            '  "provider": {\n'
            '    "@type": ["LegalService", "Attorney"],\n'
            '    "name": "Nicolas Courtier — Avocat",\n'
            '    "url": "%(site)s/"\n'
            '  }\n'
            '}\n'
            '</script>') % {"name": d["domain"], "promise": d["promise"].replace('"', '\\"'),
                            "site": SITE, "slug": d["slug"]}

# ───────────────────────── BUILD ─────────────────────────
HOME_TITLE = "Nicolas Courtier — Avocat en PI & numérique à Marseille"
HOME_DESC  = "Avocat au barreau de Marseille depuis 1991. Propriété intellectuelle, droit du numérique, RGPD et contentieux — du conseil à la défense, un seul interlocuteur."

def build():
    # Accueil
    wr("index.html", page(HOME_TITLE, HOME_DESC, SITE + "/", HOME_JSONLD, home_body, ""))

    # Pages d'expertise
    for d in DOMAINS:
        body = render({
            "{{CRUMB}}": esc(d["domain"]),
            "{{DOMAIN}}": esc(d["domain"]),
            "{{H1}}": esc(d["domain"]),
            "{{PROMISE}}": esc(d["promise"]),
            "{{PROBLEM}}": esc(d["problem"]),
            "{{AUDIENCE}}": esc(d["audience"]),
            "{{PRESTATIONS}}": prestations_html(d["prestations"]),
            "{{OTHERS}}": others_html(d["slug"]),
        }, expt)
        canonical = "%s/expertises/%s/" % (SITE, d["slug"])
        wr("expertises/%s/index.html" % d["slug"],
           page(d["title"], d["desc"], canonical, service_jsonld(d), body, "/"))

    # sitemap.xml
    urls = [(SITE + "/", "1.0")] + [("%s/expertises/%s/" % (SITE, d["slug"]), "0.8") for d in DOMAINS]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, prio in urls:
        sm += ['  <url>', '    <loc>%s</loc>' % loc, '    <lastmod>%s</lastmod>' % TODAY,
               '    <changefreq>monthly</changefreq>', '    <priority>%s</priority>' % prio, '  </url>']
    sm.append('</urlset>\n')
    wr("sitemap.xml", "\n".join(sm))

    # robots.txt
    wr("robots.txt", "User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % SITE)

    print("Build OK :")
    print("  - index.html")
    for d in DOMAINS:
        print("  - expertises/%s/index.html" % d["slug"])
    print("  - sitemap.xml, robots.txt")

if __name__ == "__main__":
    build()
