# Guide du style visuel : maquettes Axion CRM Pro (lot U1bis)

Ce guide sert à **régénérer les 40 autres pages sans rien inventer**. Chaque composant existe déjà dans `maquettes/_fabrique/socle.py` (fonction Python) et dans `maquettes/style.css` (classe). Les 5 pages repères dans `_fabrique/pages_reperes.py` montrent chaque composant en vrai.

Pages repères : `index.html` (Aujourd'hui), `contacts.html`, `campagne-nouvelle.html`, `sante.html`, `reponses.html`. Captures : `maquettes/captures/` (1440, 1024, 768, 360 px).

## 1. Les 8 règles

1. **Tout se voit en arrivant.** En haut de page : une rangée de tuiles chiffres (KPI). Pas de paragraphe.
2. **Phrases de 6 mots au plus.** Un chiffre, une jauge ou une pastille remplace une phrase.
3. **Cartes blanches à cadre net** : bordure 1 px foncée à 20 %, ombre, rayon 16 px.
4. **Couleur = sens** (jamais décorative) : voir § 2.
5. **Un seul bouton plein par écran et par état** : bleu marque, 48 px, ombre, icône. Les autres boutons : contour foncé 2 px.
6. **Texte 16 px minimum** (pastilles et étiquettes en capitales : 14 px gras au plus petit). Titre de page 28 px, titre de bloc 20 px.
7. **Contraste AA renforcé** : texte noir bleuté `#0d1830` sur blanc (17:1), texte secondaire `#34405a` (10:1). Jamais de gris clair pour du texte utile.
8. **Zéro chevauchement** : mise en page en `grid` / `flex` avec `gap`. Aucune position absolue pour du contenu. Seul l'en-tête est collant (`sticky`). Le cadre « Maquette » est dans le flux, sous l'en-tête.

## 2. Couleurs et sens

| Teinte | Sens | Plein (pastilles, icônes) | Fond pâle | Texte sur pâle |
|---|---|---|---|---|
| `terracotta` | À faire | `#b4441a` (5,6:1 avec blanc) | `#fdf0e9` | `#7a2c0e` |
| `bleu` | En cours | `#1d4ed8` (6,7:1) | `#eaf1ff` | `#1e3a8a` |
| `vert` | Fait, sain | `#15803d` (5,0:1) | `#e8f7ee` | `#14532d` |
| `ambre` | Attention | `#a14a07` (6,0:1) | `#fff4dc` | `#78350f` |
| `violet` | Nouveau, suggestion | `#6d28d9` (7,1:1) | `#f2edff` | `#4c1d95` |
| `rouge` | Arrêté, STOP, danger | `#b91c1c` (6,5:1) | `#fdecec` | `#7f1212` |
| `gris` | Neutre | `#475569` (7,6:1) | `#f1f3f7` | `#1f2937` |

Marque (bouton plein, liens, onglet actif) : `#2448e5` (6,7:1 avec blanc). Fond de page : `#eef1f6`.

## 3. Coquille

| Composant | Usage | Exemple (Python) |
|---|---|---|
| Page dans la coquille | Toute page de l'application | `page('contacts', 'Contacts', '<strong>1 248 personnes</strong>, 1 102 joignables.', normal, vide, actions=…, onglets_haut=…)` |
| Barre latérale | 264 px dès 1024 px ; **rail d'icônes** de 76 px entre 768 et 1023 px (dans la grille, ne recouvre rien) ; masquée sous 768 px, ouverte en tiroir par le bouton menu | automatique |
| En-tête collant | Fil d'Ariane, recherche Ctrl K, feu des envois (pastille pleine), cloche, « Tout arrêter », compte | automatique |
| Cadre « Maquette » | Choisir l'état : Normal, Vide, Erreur, Chargement. **Sous l'en-tête, dans le flux** | automatique |
| Titre de page | `h1` 28 px + phrase d'état courte (18 px) + actions à droite | arguments `titre`, `phrase`, `actions` de `page()` |
| Onglets de section | Liens entre pages sœurs, avec nombre | `onglets_nav('Sections de Contacts', [('contacts.html', 'Personnes', '1 248'), …], 'contacts.html')` |
| Onglets dans la page | Panneaux (role=tab), libellé avec `<span class="nb">7</span>` | `onglets('Réponses', [('a-traiter', 'À traiter <span class="nb">7</span>', contenu), …])` |

## 4. Composants

| Nom | Usage | Exemple |
|---|---|---|
| **Bouton plein** | L'action principale, une seule par écran | `btn('Ajouter un contact', 'plein', icone='ajout-personne', attrs='data-ouvre="fen-ajout"')` |
| Bouton contour | Actions secondaires (contour foncé 2 px) | `btn('Importer', 'contour', icone='collecte')` ; petit : `btn('Voir la santé', 'petit', 'sante.html', 'fleche')` |
| Bouton discret | Lien d'action dans une ligne de tableau | `btn('Ouvrir', 'petit-discret', 'contact.html')` |
| Bouton danger | Arrêter, STOP (contour rouge) ; plein rouge seulement dans une fenêtre de confirmation | `<button class="btn btn-danger">` / `btn-danger-plein` |
| **Tuile chiffre (KPI)** | Rangée du haut de chaque page : grosse icône, libellé, chiffre 44 px, détail court, mini-graphique. Cliquable si `href` | `kpis(kpi('Réponses à traiter', '7', 'reponses', 'terracotta', badge('vert', '2 intéressées'), 'reponses.html'), …)` |
| **Bloc coloré** | Carte blanche, bande haute 6 px de la teinte, icône carrée pleine 48 px, mot-pastille à droite | `bloc('Mes tâches du jour', contenu, 'bleu', 'taches', mot='5 aujourd’hui', pied=btn(…))` |
| Bloc neutre | Graphiques, récapitulatifs | `bloc('Envoyés cette semaine', barres(…), icone='stats')` |
| **Pastille de statut** | Pleine, texte blanc gras, symbole en tête (●, ▲, ■, ✓, ▶, ○) | `badge('vert', 'Intéressée', '●')`, `feu('ambre', 'Ralenti')` |
| Grande ligne cliquable | Listes courtes (≥ 68 px) : initiales, titre + détail, pastille, chevron | `lignes(ligne('Claire Durand', '« Rappelez-moi jeudi. »', initiales('Claire Durand', 'terracotta'), badge('vert', 'Intéressée'), 'reponses.html'))` |
| Ligne à cocher | Tâches (case 24 px) | voir `_case_tache()` dans `pages_reperes.py` |
| Initiales | Personne sans photo | `initiales('Paul Martin', 'bleu')` ; grand : classe `initiales grand` |
| **Jauge** | Part d'un total, quota, seuil (role=meter) | `jauge('Quota', 96, 120, 'vert', '96 / 120')` |
| **Anneau** | Score « X sur N » (contrôles, jalons) | `anneau(7, 7, 'vert', '7/7', 'Contrôles au vert', 'Fédérations T1')` |
| **Barres** | Volume par jour ou par catégorie | `barres([('Lun', 84), ('Mar', 102)], 'bleu', 'Envoyés par jour')` |
| **Courbe** | Évolution sur 14 ou 30 jours | `courbe([1, 0, 2, 5, 7], ['19 oct.', '1er nov.'], 'vert', 'Réponses par jour')` |
| Série de points | Historique court (7 derniers matins, boîtes) | `points_serie([('Lun', '', 'coche'), ('Mer', 'ambre', 'alerte')])` |
| Mini-chiffres | 2 à 4 chiffres dans un bloc | `chiffres([('07:05', 'heure'), ('4/4', 'témoins')])` |
| **Grande tuile de feu** | État par domaine, boîte, serveur : fond teinté, rond plein 56 px | `tuile_feu('prospection-b.example', 'ambre', '1 boîte', chiffres(…) + jauge(…), 'domaines.html')` |
| Verdict global | Bandeau d'état en haut d'une page de surveillance | `verdict_global('Envois normaux', '4 boîtes prêtes · 1 ralentie', 'vert', 'coche')` |
| **Stepper** | Parcours à étapes : ronds numérotés reliés, coche verte quand fait | `frise(['Cible', 'Message', 'Envoi', 'Vérification', 'Lancement'], 1)` dans `<div data-assistant>` ; panneaux `data-etape="n"`, boutons `data-aller="n"` |
| Choix en cartes | Choisir une liste, un message (radio dans une carte, gros chiffre) | `<div class="choix">` + `<label>` ; voir `carte_liste()` |
| Séquence | Messages d'une campagne (Jour 0, +4, +11) | `<ol class="sequence">` |
| Contrôles | Liste de vérifications réussies (tuiles vertes cochées) | `<ul class="controles">` |
| **Tableau** | Zébré, survol bleu pâle, ligne entière cliquable ; cartes empilées sous 768 px | `tableau('Personnes', colonnes, lignes, liens=['contact.html', …], secondaires=(1, 4, 5))` |
| Colonnes secondaires | Masquées entre 768 et 1180 px pour éviter tout défilement | argument `secondaires` de `tableau()` |
| Cellule personne | Case + initiales + nom + entreprise | classe `cellule-personne` (voir `_contacts()`) |
| Barre d'outils | Recherche + puces de filtre avec nombres | `<div class="barre-outils">` + `champ-recherche` + `filtres([…])` |
| Barre de sélection | Actions de masse (fond foncé, dans le flux) | `<div class="barre-selection">` |
| Mini-titre | Sous-partie en capitales avec filet | `mini_titre('Feux par domaine')` |
| Suggestion | Proposition de l'assistant (violet) + effets en tuiles + bouton plein | classes `suggestion`, `effets` (voir `_reponses()`) |
| Gestes | Boutons de classement avec touche clavier | `<button class="btn btn-contour"><span class="touche">1</span>Pas intéressé</button>` |
| **État vide** | Grande icône dans un rond 112 px, titre, 1 phrase, bouton plein | `etat_vide('personnes', 'Aucun contact pour l’instant', 'Importez un fichier pour commencer.', btn(…, 'plein'))` |
| État d'erreur | Rond rouge plein, « Réessayer » | `etat_erreur('Chiffres illisibles. Par prudence, pas de vert.', 'État des envois inconnu')` |
| Chargement | Squelette (tuiles + bloc) | automatique |
| Fenêtre / tiroir | Confirmation, ajout, import (dialog natif) | `fenetre('fen-stop', titre, corps, pied)`, `tiroir(…)` |

## 5. Recette pour régénérer une page

1. Déplacer sa fonction dans `pages_reperes.py` (ou réécrire sur place) avec les briques ci-dessus.
2. Haut de page : `kpis(…)` (3 à 5 tuiles, teintes selon le sens).
3. Corps : `grille deux` ou `grille trois` de `bloc(…)` colorés ; graphiques plutôt que phrases.
4. Un seul `btn(…, 'plein')` visible par état (les fenêtres fermées ne comptent pas).
5. `python3 maquettes/_fabrique/fabrique.py` puis `python3 maquettes/_fabrique/controle.py nom.html` : **doit sortir sans erreur**.

## 6. Contrôle automatique

`maquettes/_fabrique/controle.py` (Playwright + Chromium) ouvre les pages à 1440, 1024, 768 et 360 px, dans les 4 états, chaque onglet et chaque étape, et cherche : chevauchements entre éléments frères, débordements horizontaux (page, élément, contenu), contrastes sous 4,5:1 (3:1 pour le gros texte), texte sous 16 px hors pastilles, plus d'un bouton plein visible, bouton plein sous 48 px, erreurs JavaScript.

- `python3 maquettes/_fabrique/controle.py` : 5 pages repères + captures dans `maquettes/captures/`.
- `python3 maquettes/_fabrique/controle.py --toutes` : les 45 pages.

Compatibilité : les anciennes classes (`tuiles`, `bloc`, `liste`, `frise`, `choix`, `colonnes`, `fiche`…) restent dans `style.css`. Les 40 pages non régénérées s'ouvrent avec le nouveau style (pastilles pleines, cadres, boutons) et passent le contrôle, mais restent **textuelles** tant qu'elles ne sont pas refaites.
