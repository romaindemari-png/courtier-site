# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  CONTENU CLIENT — tout ce qui change d'un cabinet à l'autre.                    ║
║  Le GABARIT (build.py, _src/partials, _src/template, assets/css/main.css,       ║
║  assets/js/main.js) ne contient AUCUNE donnée d'ici en dur.                     ║
║                                                                                 ║
║  Nouveau cabinet : dupliquer le site, remplacer CE fichier, `python3 build.py`. ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

# ── Déploiement ────────────────────────────────────────────────────────────────
SITE = "https://courtier-site.netlify.app"   # URL de production Netlify

# ── Identité ───────────────────────────────────────────────────────────────────
BRAND     = "Nicolas Courtier"
MONOGRAM  = "NC"
ROLE      = "Avocat"
SITE_NAME = "Nicolas Courtier — Avocat"        # og:site_name + name JSON-LD
LOCATION  = "Marseille"
CREDIT    = "LeStud"                            # crédit studio (pied de page)
COPYRIGHT = "© 2026 Nicolas Courtier · Avocat au barreau de Marseille"

# ── Couleurs / tokens (éditables) → génèrent assets/css/tokens.css ──────────────
COLORS = {
    "cream":    "#ECE7DB",
    "cream2":   "#E4DCCC",
    "ink":      "#16140F",
    "dark":     "#1A1815",
    "onDark":   "#EDE8DD",
    "accent":   "#2E2BF5",
    "muted":    "#675F50",                      # gris-brun chaud, contraste 5,1:1 sur crème (WCAG AA)
    "mutedDk":  "rgba(237,232,221,.55)",
    "line":     "rgba(22,20,15,.18)",
    "lineDk":   "rgba(237,232,221,.16)",
    "gradFrom": "#2E2BF5",                      # --grad = linear-gradient(120deg, gradFrom, gradTo)
    "gradTo":   "#7B4DFF",
}

# ── Coordonnées (⚠ à confirmer client — voir aussi le commentaire JSON-LD) ──────
CONTACT = {
    "email":         "contact@courtier-avocats.com",
    "street":        "2 rue Odette Jasse",
    "postal":        "13015",
    "city":          "Marseille",
    "barreau":       "Marseille — depuis 1991",
    "founding_year": "1991",
}

# ── Navigation (header + menu mobile + footer) ──────────────────────────────────
NAV = [
    {"href": "#cabinet",    "label": "Le cabinet"},
    {"href": "#expertises", "label": "Expertises"},
    {"href": "#approche",   "label": "L'approche"},
]
NAV_CONTACT = {"href": "/contact/", "label": "Contact"}              # menu mobile + footer
NAV_CTA     = {"href": "/contact/", "label": "Prendre rendez-vous"}  # CTA header → page /contact/

# ── SEO accueil ─────────────────────────────────────────────────────────────────
HOME_TITLE = "Nicolas Courtier — Avocat en PI & numérique à Marseille"
HOME_DESC  = ("Avocat au barreau de Marseille depuis 1991. Propriété intellectuelle, "
              "droit du numérique, RGPD et contentieux — du conseil à la défense, un seul interlocuteur.")
# JSON-LD (accueil)
LD_DESCRIPTION = ("Avocat au barreau de Marseille depuis 1991. Propriété intellectuelle, "
                  "droit du numérique, données personnelles (RGPD) et contentieux — du conseil à la défense.")
KNOWS_ABOUT = ["Propriété intellectuelle", "Droit du numérique", "Données personnelles et RGPD", "Contentieux"]
PERSON = {"name": "Nicolas Courtier", "jobTitle": "Avocat", "barreau": "Barreau de Marseille"}

# ── Images ──────────────────────────────────────────────────────────────────────
PORTRAIT = {"webp": "/assets/img/portrait-nicolas-courtier.webp",
            "jpg":  "/assets/img/portrait-nicolas-courtier.jpg",
            "alt":  "Nicolas Courtier, avocat au barreau de Marseille", "w": 803, "h": 1000}
APPROCHE_IMG = {"webp": "/assets/img/approche-gratte-ciels.webp",
                "jpg":  "/assets/img/approche-gratte-ciels.jpg",
                "alt":  "Tours d'un quartier d'affaires, traitées en duotone", "w": 750, "h": 1000}

# Hero : mot qui tourne → photo affichée au survol (clés = mots ; aussi data-img des cards)
HERO_WORDS = ["forme", "prix", "frontière", "contour"]
HERO_IMAGES = {
    "forme":     "/assets/img/forme.webp",
    "prix":      "/assets/img/prix.webp",
    "frontière": "/assets/img/approche-gratte-ciels.webp",
    "contour":   "/assets/img/contour.webp",
}

# ── Contenu de l'accueil ────────────────────────────────────────────────────────
HERO = {
    "baseline": "Trente-cinq ans de barreau au service de votre patrimoine immatériel — marques, créations, données, contrats.",
    "title_before": "Protéger ce qui",
    "title_after_prefix": "n'a pas de ",       # précède le mot qui tourne
    "first_word": "forme",                      # = HERO_WORDS[0]
    "title_after_suffix": ".",
}
CABINET = {
    "eyebrow": "Le cabinet",
    "title_html": "Défendre l'invisible, depuis <span class=\"ac\">1991</span>.",
    "body": ("Avocat au barreau de Marseille, DPO externalisé et maître de conférences à "
             "Aix-Marseille. Un seul interlocuteur pour la propriété intellectuelle, les données "
             "et le droit du numérique — du conseil au contentieux."),
    "stats": [("35", "ans de barreau"), ("3", "métiers réunis"), ("1", "interlocuteur")],
}
EXPERTISES = {"eyebrow": "Expertises", "title": "Ce que je défends."}
APPROCHE = {
    "eyebrow": "L'approche", "title": "Le droit et la technique, ensemble.",
    "items": [
        ("Là où les autres s'arrêtent",
         "Je relie votre système d'information au cadre juridique — pas l'un sans l'autre. La technique et le droit avancent ensemble, jamais en silos."),
        ("La conformité se pilote",
         "Du RGPD à l'IA Act, un copilotage continu et lisible — jamais un audit qui dort sur une étagère. La conformité devient un réflexe, pas une contrainte."),
        ("Une relation qui dure",
         "Un interlocuteur unique, qui connaît votre dossier et le suit dans le temps. Pas de relais, pas de perte d'information."),
    ],
}
MANIFESTO = {
    "quote_html": "La conformité ne se décrète pas, elle se <span class=\"ac grad\">pilote</span>.",
    "sup": "Entre votre système d'information et le cadre juridique, j'assure le copilotage — sans jargon, sans zone grise.",
}
CONTACT_SECTION = {
    "eyebrow": "Contact",
    "title_html": "Parlons de votre <span class=\"ac grad\">projet</span>.",
    "cta_label": "Écrire au cabinet",
    "secondary_label": "Prendre rendez-vous",
    "meta": [
        ("Cabinet", "2 rue Odette Jasse<br>13015 Marseille"),
        ("Écrire", "contact@courtier-avocats.com"),
        ("Barreau", "Marseille — depuis 1991"),
    ],
}

# ── Page /contact/ (formulaire Netlify Forms) ──────────────────────────────────
CONTACT_PAGE = {
    "title":   "Contact — Nicolas Courtier, avocat à Marseille",
    "desc":    "Contactez le cabinet de Nicolas Courtier, avocat à Marseille : propriété intellectuelle, droit du numérique, RGPD, contentieux. Décrivez votre projet en quelques lignes.",
    "eyebrow": "Contact",
    "h1_html": "Parlons de votre <span class=\"ac grad\">projet</span>.",
    "intro":   "Décrivez votre besoin en quelques lignes — je vous réponds rapidement. Les champs suivis d'un astérisque sont obligatoires.",
}

# ── Page /merci/ (confirmation d'envoi) ─────────────────────────────────────────
MERCI_PAGE = {
    "title":   "Message envoyé — Nicolas Courtier, avocat à Marseille",
    "desc":    "Votre message a bien été transmis au cabinet de Nicolas Courtier, avocat à Marseille.",
    "eyebrow": "Contact",
    "h1_html": "Message bien <span class=\"ac grad\">envoyé</span>.",
    "body":    "Merci, votre message est arrivé. Je vous réponds dans les meilleurs délais — généralement sous 48 heures ouvrées.",
}

# ── Page /mentions-legales/ (réglementée — placeholders [À COMPLÉTER] dans le template) ──
LEGAL_PAGE = {
    "title":   "Mentions légales — Nicolas Courtier, avocat à Marseille",
    "desc":    "Mentions légales du site de Nicolas Courtier, avocat au barreau de Marseille.",
    "eyebrow": "Informations légales",
    "h1":      "Mentions légales",
    "intro":   "Informations légales relatives au présent site et à son éditeur, conformément à la loi n° 2004-575 du 21 juin 2004 pour la confiance dans l'économie numérique (LCEN).",
}

# ── Module Actualités (lecture seule — Netlify Blobs) ───────────────────────────
# Couleurs de pastille = uniquement des valeurs de la palette gelée (accent, violet du
# dégradé, ink, muted) → aucune nouvelle couleur introduite.
ACTUS = {
    "home_eyebrow": "Le fil",
    "home_title":   "Actualités",
    "see_all":      "Toutes les actualités",
    "page_title":   "Actualités — Nicolas Courtier, avocat à Marseille",
    "page_desc":    "Actualités du cabinet de Nicolas Courtier, avocat à Marseille : interventions, publications, médias et décisions.",
    "page_eyebrow": "Le fil",
    "page_h1":      "Actualités",
    "page_intro":   "Interventions, publications, apparitions médias et décisions marquantes du cabinet.",
    "filter_all":   "Tout",
    "link_label":   "En savoir plus",
    "loading":      "Chargement des actualités…",
    "empty":        "Aucune actualité pour le moment.",
    "error":        "Les actualités sont momentanément indisponibles.",
    # ordre = ordre d'affichage des filtres ; color ∈ palette gelée
    "types": [
        {"key": "intervention", "label": "Intervention", "color": "#2E2BF5"},  # accent
        {"key": "publication",  "label": "Publication",  "color": "#7B4DFF"},  # violet du dégradé
        {"key": "media",        "label": "Média",        "color": "#16140F"},  # ink
        {"key": "decision",     "label": "Décision",     "color": "#675F50"},  # muted
    ],
}

# ── Admin Actualités (outil privé — Identity) ──────────────────────────────────
ADMIN = {
    "title":           "Admin · Actualités — Nicolas Courtier",
    "h1":              "Espace administration",
    "intro":           "Connectez-vous pour gérer les actualités du cabinet.",
    "login":           "Se connecter",
    "logout":          "Se déconnecter",
    "dash_title":      "Actualités",
    "loading":         "Chargement…",
    "empty":           "Aucune brève enregistrée.",
    "error":           "Impossible de charger les brèves (session expirée ?).",
    "draft_label":     "Brouillon",
    "published_label": "Publié",
    "pinned_label":    "Épinglé",
}

# ── Étapes communes "Comment ça se passe" (provisoire, à valider) ───────────────
STEPS = [
    ("Diagnostic", "On fait le point sur votre situation, vos actifs et vos risques — un état des lieux clair, sans jargon."),
    ("Action",     "Je mets en place la protection ou la stratégie adaptée : dépôts, contrats, mise en conformité ou procédure."),
    ("Suivi",      "Un interlocuteur unique qui suit votre dossier dans le temps et anticipe les évolutions."),
]

# ── Icônes SVG des cards (décoratives, par expertise) ───────────────────────────
_IC_PI   = '<svg width="38" height="38" viewBox="0 0 40 40" fill="none" stroke="currentColor" stroke-width="1" aria-hidden="true" focusable="false"><circle cx="20" cy="20" r="13"/><path d="M20 12.5v15M13.5 16.25l13 7.5M26.5 16.25l-13 7.5"/></svg>'
_IC_NUM  = '<svg width="38" height="38" viewBox="0 0 40 40" fill="none" stroke="currentColor" stroke-width="1" aria-hidden="true" focusable="false"><path d="M15 13l-7 7 7 7M25 13l7 7-7 7M22 11l-4 18"/></svg>'
_IC_RGPD = '<svg width="38" height="38" viewBox="0 0 40 40" fill="none" stroke="currentColor" stroke-width="1" aria-hidden="true" focusable="false"><ellipse cx="20" cy="12" rx="11" ry="4"/><path d="M9 12v8c0 2.2 4.9 4 11 4s11-1.8 11-4v-8"/><path d="M9 20c0 2.2 4.9 4 11 4s11-1.8 11-4"/></svg>'
_IC_CONT = '<svg width="38" height="38" viewBox="0 0 40 40" fill="none" stroke="currentColor" stroke-width="1" aria-hidden="true" focusable="false"><path d="M20 9v22M12 31h16M11 15l18-5"/><path d="M11 15l-4 8h8l-4-8zM29 10l-4 8h8l-4-8z"/></svg>'

# ── Expertises (nombre LIBRE : le build boucle, pas de 4 codé en dur) ───────────
# Chaque entrée = 1 page /expertises/<slug>/ + 1 card sur l'accueil + maillage + sitemap.
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
    "card": {"label": "Propriété intellectuelle", "title": "Marques & créations",
             "desc": "Droit d'auteur, dessins & modèles, noms de domaine, contrefaçon.",
             "img": "forme", "icon": _IC_PI},
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
    "card": {"label": "Droit du numérique", "title": "Contrats & plateformes",
             "desc": "Contrats IT, NIS2, intelligence artificielle, IA Act.",
             "img": "contour", "icon": _IC_NUM},
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
    "card": {"label": "Données personnelles", "title": "RGPD & mission DPO",
             "desc": "Mise en conformité, transferts, contrôles et sanctions CNIL.",
             "img": "prix", "icon": _IC_RGPD},
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
    "card": {"label": "Contentieux", "title": "Défense & litige",
             "desc": "Concurrence déloyale, e-réputation, devant toutes juridictions.",
             "img": "frontière", "icon": _IC_CONT},
  },
]
