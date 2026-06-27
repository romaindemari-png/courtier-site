# Nicolas Courtier — site vitrine

Site statique pur (HTML/CSS/JS), généré depuis une **source unique** par un petit
script Python sans dépendance. Aucun CMS, aucun framework, aucune build command sur
l'hébergeur : Netlify sert le HTML tel quel.

## ⚠️ Règle n°1 — ne jamais éditer le HTML généré

Les fichiers suivants sont **produits par `build.py`** et écrasés à chaque build.
Chacun porte un bandeau `<!-- FICHIER GÉNÉRÉ PAR build.py — NE PAS ÉDITER À LA MAIN -->` :

- `index.html`
- `expertises/*/index.html`
- `sitemap.xml`, `robots.txt`

Toute modification se fait dans `_src/` (ou les données de `build.py`), **puis** on régénère.

## Structure

```
_src/
  partials/header.html     ← header + menu mobile + grain + filtre SVG #duo (source unique)
  partials/footer.html     ← footer (source unique)
  template/base.html       ← squelette <head> (SEO, OG, fonts, CSS/JS) + emplacements
  template/home.html       ← corps de l'accueil
  template/expertise.html  ← gabarit verrouillé d'une page d'expertise
build.py                   ← contenu des 4 expertises (DOMAINS) + générateur
assets/                    ← css/ js/ fonts/ img/ + favicon.svg (servis tels quels)
index.html, expertises/*/  ← SORTIE GÉNÉRÉE (ne pas éditer)
```

Le header et le footer n'existent **qu'une fois** (`_src/partials/`). Les liens y
utilisent `{{HOME}}` : vide sur l'accueil (`#cabinet`), `/` sur les sous-pages (`/#cabinet`).

## Construire le site

```bash
python3 build.py
```

Régénère les 5 pages + `sitemap.xml` + `robots.txt`. À lancer après **toute** modif
d'un partial, d'un template, du CSS/JS ou du contenu. Aperçu local :

```bash
python3 -m http.server 8765   # puis http://127.0.0.1:8765
```

## Modifier le contenu

- **Header / footer** → `_src/partials/`, puis `python3 build.py`.
- **Accueil** → `_src/template/home.html`.
- **Mise en page d'une expertise** (commune aux 4) → `_src/template/expertise.html`.
- **Styles / scripts** → `assets/css/main.css`, `assets/js/main.js`.

### Ajouter ou modifier une page d'expertise

Tout passe par la liste `DOMAINS` dans **`build.py`**. Chaque entrée :

```python
{
  "slug": "nouveau-domaine",          # → URL /expertises/nouveau-domaine/
  "domain": "Nom du domaine",         # fil d'ariane + H1 + eyebrows
  "title": "… — Nicolas Courtier, avocat à Marseille",   # <title> (~55-60 c.)
  "desc": "…",                        # meta description (150-160 c.)
  "promise": "…",                     # phrase de promesse (hero)
  "problem": "…",                     # section « Le problème »
  "prestations": [                    # section « Ce que je fais »
      ("Titre de la prestation", "Phrase descriptive."),
      # …
  ],
  "audience": "…",                    # section « Pour qui »
}
```

Ajoute (ou édite) l'entrée, puis `python3 build.py`. La page, le maillage interne
(liens vers les autres expertises), le `sitemap.xml` et le JSON-LD sont régénérés
automatiquement. Pour une nouvelle page, pense à l'ajouter aussi comme card sur
l'accueil dans `_src/template/home.html`.

## Déploiement (Netlify)

Hébergement **statique brut**, aucune build command : Netlify publie la racine du repo.
On commite donc le HTML généré avec les sources.

> ⚠️ **Domaine à confirmer.** `SITE` dans `build.py` vaut un placeholder de preview
> Netlify (`https://courtier-site.netlify.app`). Au déploiement définitif : remplacer
> par le vrai domaine, relancer `python3 build.py`, committer.

## À valider par le client

- Textes des 4 pages d'expertise (problème, prestations, étapes, pour qui) : **standard
  métier provisoire**, à relire.
- JSON-LD : téléphone, email, adresse, n° de toque/barreau sont en **commentaire
  « À CONFIRMER »** — aucune donnée inventée (ni avis, ni note, ni récompense).
- CTA contact (`href="#"`) : à brancher à l'étape Netlify Forms.
