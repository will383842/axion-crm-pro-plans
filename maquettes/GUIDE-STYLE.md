# Guide du style visuel : maquettes Axion CRM Pro et Axion Envoi (lots U1bis, M1, M2)

Ce guide sert à **régénérer les 40 autres pages sans rien inventer**. Chaque composant existe déjà dans `maquettes/_fabrique/socle.py` (fonction Python) et dans `maquettes/style.css` (classe). Les 5 pages repères dans `_fabrique/pages_reperes.py` montrent chaque composant en vrai.

Pages repères : `index.html` (Aujourd'hui), `contacts.html`, `campagne-nouvelle.html`, `sante.html`, `reponses.html`. Captures : `maquettes/captures/` (1440, 1024, 768, 360 px).

## 0. Lot M2 : même échelle et mêmes couleurs que le vrai CRM

Le style est **relevé dans le code du CRM réel** (`axion-crm-pro/frontend/src` : `styles/index.css`, `components/ui/*`, `components/layout/Sidebar.tsx` et `Header.tsx`, `features/dashboard/DashboardPage.tsx`, `features/companies/CompaniesListPage.tsx` et `CompanyDetailPage.tsx`). Une seule feuille (`style.css`) pour les deux produits ; seule la couleur d'identité change.

| Élément | Vrai CRM (Tailwind) | Maquettes M2 |
|---|---|---|
| Police | Inter | Inter (repli : police système) |
| Texte courant | `text-sm` 14/20 px | 14/20 px |
| Détails, pastilles, en-têtes de tableau | `text-xs` 12/16 px | 12/16 px (jamais moins) |
| Titre de page | `text-2xl` 24 px (`md:text-3xl` 30 px) | 24/32 px, demi-gras |
| Titre de section | `text-lg font-bold` 18 px | 18/28 px gras |
| Titre de carte | `text-sm font-semibold` 14 px | 16/24 px demi-gras |
| Chiffre de tuile | `text-2xl` 24 px (KpiCard) ; 30 px sur l'accueil | 24/32 px gras |
| Bouton | `h-9 px-4 text-sm` (36 px) ; petit `h-8 text-xs` | 36 px / 32 px ; **44 px au téléphone** |
| Champ | `h-9 rounded-lg text-sm` | 36 px, rayon 8 px ; 44 px au téléphone |
| Rayons | boutons et champs `rounded-lg` 8 px ; cartes `rounded-2xl` 16 px | 8 px / 12 px / 16 px |
| Ombres | `--shadow-card`, `--shadow-popover` | mêmes valeurs |
| Barre latérale | 260 px, fond `oklch(0.24 0.06 250)` = `#04203a`, texte `#d4dfeb`, actif `#003969` | identique ; rail de 64 px entre 768 et 1023 px |
| En-tête | même bleu profond que la barre, collant | identique + bande de 4 px de la couleur du produit |
| Fond de page | `oklch(0.98 0.005 250)` = `#f6f9fc` | `#f6f9fc` |

**Échelle permise** (contrôle de fidélité) : **12, 14, 16, 18, 20, 24 px**. Toute autre taille fait échouer `controle.py`.

## 1. Les 8 règles

1. **Tout se voit en arrivant.** En haut de page : une rangée de tuiles chiffres (KPI). Pas de paragraphe.
2. **Phrases de 6 mots au plus.** Un chiffre, une jauge ou une pastille remplace une phrase.
3. **Cartes blanches à cadre net** : bordure 1 px `slate-300` (un cran plus net que le CRM), ombre `--shadow-card`, rayon 16 px.
4. **Couleur = sens** (jamais décorative) : voir § 2.
5. **Un seul bouton plein par écran et par état**, couleur du produit, 36 px (44 px au téléphone), ombre. Les autres : fond blanc, cadre `slate-400`.
6. **Texte courant 14 px, détails 12 px, jamais moins.** Titre de page 24 px, titre de section 18 px.
7. **Contraste** : ≥ 4,5:1 partout, **≥ 7:1 pour le texte courant**. Texte `#0f172b` (17,8:1), secondaire `#45556c` (7,6:1 ; le CRM met `slate-500`, 4,8:1).
8. **Zéro chevauchement** : `grid` / `flex` avec `gap`. Seul l'en-tête est collant. Le cadre « Maquette » est dans le flux.

## 2. Couleurs et sens (palette Tailwind du CRM : StatusPill, KpiCard)

| Teinte | Sens | Tailwind | Plein (texte blanc) | Vif (barres) | Fond pâle | Texte sur pâle (≥ 7:1) |
|---|---|---|---|---|---|---|
| `terracotta` | À faire | orange | `#ca3500` (5,2:1) | `#ff6900` | `#fff7ed` | `#7e2a0c` |
| `bleu` | En cours | sky | `#0069a8` (5,9:1) | `#00a6f4` | `#f0f9ff` | `#00598a` |
| `vert` | Fait, sain | emerald | `#007a55` (5,4:1) | `#00bc7d` | `#ecfdf5` | `#006045` |
| `ambre` | Attention | amber | `#bb4d00` (5,0:1) | `#fe9a00` | `#fffbeb` | `#7b3306` |
| `violet` | Nouveau, suggestion | violet | `#7008e7` (7,3:1) | `#8e51ff` | `#f5f3ff` | `#5d0ec0` |
| `rouge` | Arrêté, STOP | rose | `#c70036` (6,0:1) | `#ff2056` | `#fff1f2` | `#a50036` |
| `gris` | Neutre | slate | `#45556c` (7,6:1) | `#90a1b9` | `#f1f5f9` | `#314158` |

Pastilles (`badge`) : comme `StatusPill` du CRM : fond pâle, texte « plein » (700), symbole en tête, 12 px.

## 2 bis. Deux produits, une couleur d'identité chacun (ADR-13)

| Produit | Plein (texte blanc) | Foncé | Pâle | Vif (sur fond foncé) |
|---|---|---|---|---|
| **CRM Pro** | `#0051bd` = `brand-600` du CRM, `oklch(0.45 0.20 250)` (7,2:1) | `#003991` (`brand-700`) | `#ebf7ff` (`brand-50`) | `#1795fa` (`brand-400`) |
| **Envoi** | `#0b7285` turquoise pétrole (5,6:1) | `#085563` | `#e3f3f6` | `#22b8cf` |

- Où elle se voit : liseré de 4 px à gauche de la barre, sélecteur de produit, badge et bande haute de l'en-tête, barre de l'entrée de menu active, soulignement de l'onglet actif, **bouton plein**. Jamais sur une pastille, une jauge ou un feu.
- `<body data-produit="crm|envoi">` : `style.css` redéfinit `--marque*`. Rien d'autre ne change.
- Écart assumé : dans le vrai CRM, le bouton principal est **ardoise** (`slate-900`) et la marque ne sert qu'aux liens et accents ; ici, il prend la couleur du produit (ADR-13).
- Python : `page(..., reprise='frontend/src/features/…/X.tsx')` affiche « Reprise de : … » dans le cadre Maquette ; sans `reprise`, la page est « Nouvelle ». Le produit vient de l'entrée de menu (`NAV_CRM`, `NAV_ENVOI`) ou de l'argument `menu=`.
- Briques M1 : `filtres_champs()`, `pagination()`, `dl()`, `chrono()`, `barre_masse()`, `.bandeau`, `.paire`, `.critere` + `.operateur`, `.version-ab`, `.fil-message` + `.bulle`. M2 : tuile `kpi(..., 'sombre')` (tuile foncée « Entreprises » du tableau de bord).

## 3. Coquille

| Composant | Usage | Exemple (Python) |
|---|---|---|
| Page dans la coquille | Toute page de l'application | `page('contacts', 'Contacts', '<strong>1 248 personnes</strong>, 1 102 joignables.', normal, vide, actions=…, onglets_haut=…)` |
| Barre latérale | Bleu profond du CRM, sélecteur de produit en haut, liseré de 4 px de la couleur du produit ; 260 px dès 1024 px ; **rail d'icônes** de 64 px entre 768 et 1023 px (dans la grille) ; masquée sous 768 px, ouverte en tiroir | automatique |
| En-tête collant | Bleu profond comme le CRM : fil d'Ariane, recherche Ctrl K, feu des envois, cloche, « Tout arrêter » (Envoi), compte | automatique |
| Cadre « Maquette » | Choisir l'état : Normal, Vide, Erreur, Chargement. **Sous l'en-tête, dans le flux** | automatique |
| Titre de page | `h1` 24 px + phrase d'état courte (14 px) + actions à droite | arguments `titre`, `phrase`, `actions` de `page()` |
| Onglets de section | Liens entre pages sœurs, avec nombre | `onglets_nav('Sections de Contacts', [('contacts.html', 'Personnes', '1 248'), …], 'contacts.html')` |
| Onglets dans la page | Panneaux (role=tab), libellé avec `<span class="nb">7</span>` | `onglets('Réponses', [('a-traiter', 'À traiter <span class="nb">7</span>', contenu), …])` |

## 4. Composants

| Nom | Usage | Exemple |
|---|---|---|
| **Bouton plein** | L'action principale, une seule par écran (36 px, 44 au téléphone) | `btn('Ajouter un contact', 'plein', icone='ajout-personne', attrs='data-ouvre="fen-ajout"')` |
| Bouton contour | Actions secondaires (fond blanc, cadre 1 px `slate-400`) | `btn('Importer', 'contour', icone='collecte')` ; petit : `btn('Voir la santé', 'petit', 'sante.html', 'fleche')` |
| Bouton discret | Lien d'action dans une ligne de tableau | `btn('Ouvrir', 'petit-discret', 'contact.html')` |
| Bouton danger | Arrêter, STOP (contour rouge) ; plein rouge seulement dans une fenêtre de confirmation | `<button class="btn btn-danger">` / `btn-danger-plein` |
| **Tuile chiffre (KPI)** | Rangée du haut de chaque page : grosse icône, libellé, chiffre 24 px, détail court, mini-graphique. Cliquable si `href` | `kpis(kpi('Réponses à traiter', '7', 'reponses', 'terracotta', badge('vert', '2 intéressées'), 'reponses.html'), …)` |
| **Bloc coloré** | Carte blanche, filet haut de 3 px de la teinte, icône carrée pâle 36 px, mot-pastille à droite | `bloc('Mes tâches du jour', contenu, 'bleu', 'taches', mot='5 aujourd’hui', pied=btn(…))` |
| Bloc neutre | Graphiques, récapitulatifs | `bloc('Envoyés cette semaine', barres(…), icone='stats')` |
| **Pastille de statut** | Comme `StatusPill` : fond pâle, texte 700, symbole en tête (●, ▲, ■, ✓, ▶, ○), 12 px | `badge('vert', 'Intéressée', '●')`, `feu('ambre', 'Ralenti')` |
| Grande ligne cliquable | Listes courtes (≥ 52 px) : initiales, titre + détail, pastille, chevron | `lignes(ligne('Claire Durand', '« Rappelez-moi jeudi. »', initiales('Claire Durand', 'terracotta'), badge('vert', 'Intéressée'), 'reponses.html'))` |
| Ligne à cocher | Tâches (case 16 px, 20 au téléphone) | voir `_case_tache()` dans `pages_reperes.py` |
| Initiales | Personne sans photo | `initiales('Paul Martin', 'bleu')` ; grand : classe `initiales grand` |
| **Jauge** | Part d'un total, quota, seuil (role=meter) | `jauge('Quota', 96, 120, 'vert', '96 / 120')` |
| **Anneau** | Score « X sur N » (contrôles, jalons) | `anneau(7, 7, 'vert', '7/7', 'Contrôles au vert', 'Fédérations T1')` |
| **Barres** | Volume par jour ou par catégorie | `barres([('Lun', 84), ('Mar', 102)], 'bleu', 'Envoyés par jour')` |
| **Courbe** | Évolution sur 14 ou 30 jours | `courbe([1, 0, 2, 5, 7], ['19 oct.', '1er nov.'], 'vert', 'Réponses par jour')` |
| Série de points | Historique court (7 derniers matins, boîtes) | `points_serie([('Lun', '', 'coche'), ('Mer', 'ambre', 'alerte')])` |
| Mini-chiffres | 2 à 4 chiffres dans un bloc | `chiffres([('07:05', 'heure'), ('4/4', 'témoins')])` |
| **Grande tuile de feu** | État par domaine, boîte, serveur : carte blanche, filet gauche de la teinte, carré pâle 36 px | `tuile_feu('prospection-b.example', 'ambre', '1 boîte', chiffres(…) + jauge(…), 'domaines.html')` |
| Verdict global | Bandeau d'état en haut d'une page de surveillance | `verdict_global('Envois normaux', '4 boîtes prêtes · 1 ralentie', 'vert', 'coche')` |
| **Stepper** | Parcours à étapes : ronds numérotés reliés, coche verte quand fait | `frise(['Cible', 'Message', 'Envoi', 'Vérification', 'Lancement'], 1)` dans `<div data-assistant>` ; panneaux `data-etape="n"`, boutons `data-aller="n"` |
| Choix en cartes | Choisir une liste, un message (radio dans une carte, gros chiffre) | `<div class="choix">` + `<label>` ; voir `carte_liste()` |
| Séquence | Messages d'une campagne (Jour 0, +4, +11) | `<ol class="sequence">` |
| Contrôles | Liste de vérifications réussies (tuiles vertes cochées) | `<ul class="controles">` |
| **Tableau** | Comme `CompaniesListPage` : en-tête 12 px capitales sur `slate-50`, lignes 14 px, survol `slate-50`, ligne entière cliquable ; cartes empilées sous 768 px | `tableau('Personnes', colonnes, lignes, liens=['contact.html', …], secondaires=(1, 4, 5))` |
| Colonnes secondaires | Masquées entre 768 et 1520 px pour éviter tout défilement | argument `secondaires` de `tableau()` |
| Cellule personne | Case + initiales + nom + entreprise | classe `cellule-personne` (voir `_contacts()`) |
| Barre d'outils | Recherche + puces de filtre avec nombres | `<div class="barre-outils">` + `champ-recherche` + `filtres([…])` |
| Barre de sélection | Actions de masse (fond foncé, dans le flux) | `<div class="barre-selection">` |
| Mini-titre | Titre de section (18 px gras, comme « Ma base » du tableau de bord) | `mini_titre('Feux par domaine')` |
| Suggestion | Proposition de l'assistant (violet) + effets en tuiles + bouton plein | classes `suggestion`, `effets` (voir `_reponses()`) |
| Gestes | Boutons de classement avec touche clavier | `<button class="btn btn-contour"><span class="touche">1</span>Pas intéressé</button>` |
| **État vide** | Comme `EmptyState` : cadre pointillé, icône 40 px, titre 18 px, 1 phrase 14 px, bouton plein | `etat_vide('personnes', 'Aucun contact pour l’instant', 'Importez un fichier pour commencer.', btn(…, 'plein'))` |
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

`maquettes/_fabrique/controle.py` (Playwright + Chromium) ouvre les pages à 1440, 1024, 768 et 360 px, dans les 4 états, chaque onglet et chaque étape, et cherche : chevauchements entre éléments frères ; débordements horizontaux ; contrastes sous 4,5:1 (3:1 pour le gros texte) et **sous 7:1 pour le texte courant** (`p`, `td`, `dd`, `li`, `blockquote`) ; texte sous 12 px, ou texte courant sous 14 px hors détails ; **fidélité** : toute taille hors de l'échelle 12, 14, 16, 18, 20, 24 px (la liste des tailles de chaque page est imprimée) ; plus d'un bouton plein visible, bouton plein sous 36 px (44 px au téléphone) ; **zones tactiles** sous 44 px au téléphone (boutons, champs, onglets, menu) ; erreurs JavaScript.

- `python3 maquettes/_fabrique/controle.py` : 8 pages clés + captures légères dans `maquettes/captures/`.
- `python3 maquettes/_fabrique/controle.py --toutes` : toutes les pages ; `--largeur=360` pour une seule largeur.
- Prérequis : `pip install playwright pillow` (Chromium déjà présent dans `/opt/pw-browsers`).

Compatibilité : les anciennes classes (`tuiles`, `bloc`, `liste`, `frise`, `choix`, `colonnes`, `fiche`…) restent dans `style.css`. Les 40 pages non régénérées s'ouvrent avec le nouveau style (pastilles pleines, cadres, boutons) et passent le contrôle, mais restent **textuelles** tant qu'elles ne sont pas refaites.
