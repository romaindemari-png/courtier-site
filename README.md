# Nicolas Courtier — site vitrine (base `lestud-template-cabinet`)

Site statique pur (HTML/CSS/JS), généré depuis une **source unique** par un petit
script Python sans dépendance. Aucun CMS, aucun framework, aucune build command sur
l'hébergeur : Netlify sert le HTML tel quel.

Le site est construit **« template-ready »** : le **gabarit** (réutilisable) est
strictement séparé du **contenu client** (un seul fichier). Le jour où un 2ᵉ cabinet
arrive, on duplique, on remplace le fichier de données, et le template s'extrait
proprement — sans toucher au gabarit. (On ne templatise pas encore : règle LeStud,
on extrait un template seulement au 2ᵉ site du même type.)

## ⚠️ Règle n°1 — ne jamais éditer le HTML généré

Produits par `build.py` et écrasés à chaque build (chacun porte un bandeau
`<!-- FICHIER GÉNÉRÉ PAR build.py — NE PAS ÉDITER À LA MAIN -->`) :

- `index.html`
- `expertises/*/index.html`
- `contact/index.html`, `merci/index.html`, `mentions-legales/index.html`
- `assets/css/tokens.css`
- `sitemap.xml`, `robots.txt`

Toute modification se fait dans `_src/` (ou `assets/css/main.css` / `assets/js/main.js`),
**puis** on régénère.

## Gabarit (réutilisable) vs Contenu client (à remplacer)

| | Fichier(s) | Rôle |
|---|---|---|
| **CONTENU CLIENT** | **`_src/data.py`** | **Tout** ce qui change d'un cabinet à l'autre : identité, couleurs, coordonnées, navigation, textes de l'accueil, images, et la liste `DOMAINS` (expertises + prestations). **Le seul fichier à remplacer pour un nouveau cabinet.** |
| GABARIT | `build.py` | Logique de génération. Aucune donnée client. |
| GABARIT | `_src/partials/header.html`, `footer.html` | Header + footer, à placeholders. |
| GABARIT | `_src/template/base.html` | Squelette `<head>` (SEO, OG, fonts, CSS/JS). |
| GABARIT | `_src/template/home.html` | Mise en page de l'accueil, à placeholders. |
| GABARIT | `_src/template/expertise.html` | Gabarit verrouillé d'une page d'expertise. |
| GABARIT | `assets/css/main.css` | Styles. Les **couleurs** sont des `var(--token)` ; les valeurs viennent de `data.py`. |
| GABARIT | `assets/js/main.js` | Interactions. Les données hero arrivent via `window.HERO` (injecté). |

> Un contrôle automatique : `grep` des données client (nom, ville, etc.) dans les
> fichiers du gabarit doit renvoyer **vide**. Tout est dans `_src/data.py`.

### Détails « template-ready »

- **Tokens couleur centralisés.** `COLORS` dans `data.py` → `build.py` génère
  `assets/css/tokens.css` (`:root{--cream…}`). Changer la palette = éditer `COLORS`.
- **Nombre de pages piloté par les données.** `build.py` **boucle** sur `DOMAINS` :
  un cabinet peut en avoir 3, 4 ou 6 — pages, cards d'accueil, maillage interne et
  `sitemap.xml` s'adaptent tout seuls.
- **Header/footer = source unique.** Liens construits avec un préfixe `{{HOME}}` :
  vide sur l'accueil (`#cabinet`), `/` sur les sous-pages (`/#cabinet`).

## Structure

```
_src/
  data.py                  ← CONTENU CLIENT (le seul fichier à remplacer)
  partials/header.html     ← header + menu mobile + grain + filtre SVG #duo
  partials/footer.html     ← footer
  template/base.html       ← <head> + emplacements
  template/home.html       ← accueil
  template/expertise.html  ← gabarit d'une page d'expertise
build.py                   ← générateur (gabarit)
assets/                    ← css/ (main.css + tokens.css généré) js/ fonts/ img/ favicon.svg
index.html, expertises/*/  ← SORTIE GÉNÉRÉE (ne pas éditer)
sitemap.xml, robots.txt    ← SORTIE GÉNÉRÉE
```

## Construire le site

```bash
python3 build.py
```

Régénère toutes les pages + `tokens.css` + `sitemap.xml` + `robots.txt`. À lancer après
**toute** modif d'un partial, template, du CSS/JS ou de `data.py`. Aperçu local :

```bash
python3 -m http.server 8765   # puis http://127.0.0.1:8765
```

## Modifier le contenu

Presque tout passe par **`_src/data.py`**, puis `python3 build.py` :

- **Identité, couleurs, coordonnées, navigation, crédit** → en haut de `data.py`.
- **Textes de l'accueil** (hero, cabinet, approche, manifeste, contact) → blocs `HERO`,
  `CABINET`, `APPROCHE`, `MANIFESTO`, `CONTACT_SECTION`.
- **Images** → `PORTRAIT`, `APPROCHE_IMG`, `HERO_IMAGES`.
- **Mise en page** (rare) → `_src/template/` ; **styles** → `assets/css/main.css`.

### Ajouter ou modifier une page d'expertise

Tout est dans la liste `DOMAINS` de **`_src/data.py`**. Chaque entrée :

```python
{
  "slug": "nouveau-domaine",          # → URL /expertises/nouveau-domaine/
  "domain": "Nom du domaine",         # fil d'ariane + H1 + eyebrows
  "title": "… — Nicolas Courtier, avocat à Marseille",  # <title> (~55-60 c.)
  "desc": "…",                        # meta description (150-160 c.)
  "promise": "…",                     # hero
  "problem": "…",                     # « Le problème »
  "prestations": [("Titre", "Phrase descriptive."), …],   # « Ce que je fais »
  "audience": "…",                    # « Pour qui »
  "card": {"label": "…", "title": "…", "desc": "…",       # card sur l'accueil
           "img": "forme", "icon": "<svg…>"},             # img = clé de HERO_IMAGES
}
```

Ajoute (ou édite) l'entrée, puis `python3 build.py`. La page, la **card d'accueil**, le
maillage interne (liens vers les autres expertises), le `sitemap.xml` et le JSON-LD sont
régénérés automatiquement. Rien d'autre à toucher.

## Déploiement (Netlify)

Hébergement **statique brut**, aucune build command : Netlify publie la racine du repo.
On commite donc le HTML généré avec les sources. `build.py` tourne **en local**.

> ⚠️ **Domaine à confirmer.** `SITE` dans `_src/data.py` vaut un placeholder de preview
> Netlify. Au déploiement définitif : remplacer par le vrai domaine, relancer
> `python3 build.py`, committer.

## Pour un nouveau cabinet (futur)

1. Dupliquer le repo.
2. Remplacer **`_src/data.py`** (identité, couleurs, textes, `DOMAINS`) + les images
   dans `assets/img/`.
3. `python3 build.py`. Le gabarit reste inchangé.

## Formulaire de contact (Netlify Forms)

La page `/contact/` (template `_src/template/contact.html`) contient un formulaire
**Netlify Forms** : `data-netlify="true"`, champ caché `form-name`, honeypot `bot-field`,
et `action="/merci/"` (page de confirmation, en `noindex`). Le `<select>` « Domaine
concerné » est peuplé depuis `DOMAINS`. Tous les CTA du site pointent vers `/contact/`.

> ⚠️ **Netlify Forms ne fonctionne qu'une fois déployé sur Netlify** (détection du
> formulaire à la mise en ligne) — **pas testable en local**. Après branchement Netlify :
> vérifier la réception dans *Site settings → Forms*, et configurer une notification
> email (les soumissions n'arrivent nulle part tant que ce n'est pas fait).

## À valider par le client

- Textes des pages d'expertise + de la page contact (problème, prestations, étapes,
  pour qui, intro) : **standard métier provisoire**, à relire.
- JSON-LD + bloc coordonnées : téléphone, email, adresse, n° de toque/barreau en
  **« À CONFIRMER »** — aucune donnée inventée (ni avis, ni note, ni récompense).
- Notification email des soumissions du formulaire à configurer côté Netlify.
- **Mentions légales** (`/mentions-legales/`, en `noindex`) : page réglementée, tous les
  champs `[À COMPLÉTER PAR LE CLIENT]` (adresse, SIREN, téléphone, email, toque, structure,
  assurance RC, médiateur…) à renseigner avant mise en ligne, puis repasser en `index`.
