# Maquettes cliquables : Axion CRM Pro et Axion Envoi (lots M1 et M2)

Deux produits distincts, facturés à part, **avant tout codage**. Données factices uniquement (aucun vrai nom, domaines en `.example`, adresses IP de documentation). Rien n'est relié à un serveur.

## Comment ouvrir

1. Téléchargez ou clonez le dépôt `axion-crm-pro-plans`.
2. Ouvrez `maquettes/index.html` (Tableau de bord du CRM) en double-cliquant dessus (Chrome, Edge ou Firefox récent). Aucune installation.
3. **Changer de produit** : en haut du menu, le sélecteur **CRM Pro** (bleu de marque du CRM) | **Envoi** (turquoise pétrole).
4. **Toutes les pages d'un coup** : « Toutes les maquettes » en bas du menu (`plan-des-pages.html`).
5. **Téléphone** : touche F12, icône téléphone, largeur **360 px**.

## Ce qui est à savoir

- **Deux produits, deux couleurs, un seul style.** CRM Pro = bleu de marque du vrai CRM `#0051bd` (`brand-600`). Envoi = turquoise pétrole `#0b7285` (ADR-13). Même échelle, mêmes composants, même barre latérale bleu profond. On voit le produit partout : liseré du menu, sélecteur en haut du menu, badge et bande colorée dans l'en-tête, bouton principal de la couleur du produit. Les couleurs de sens ne changent pas (vert = fait, terracotta = à faire, ambre = attention, bleu = en cours, violet = nouveau, rouge = arrêté).
- **Menu du CRM = menu réel de Will, à l'identique** (Tableau de bord, À traiter, Ma base, Presse, Réseaux, Ciblage, Alimenter la base, Réglages, Technique), en accordéon comme aujourd'hui. **Envoi** a son propre menu (Campagnes, Réponses, Boîtes d'envoi, Domaines, Serveurs et adresses IP, Chauffe, Santé des envois, Désinscriptions, Alertes d'envoi, Réglages d'envoi).
- **Le cadre violet pointillé « Maquette », sous l'en-tête, n'est pas dans le produit.** Il dit si la page est **« Reprise de : <composant réel> »** ou **« Nouvelle »**, et permet de voir les 4 états : Normal, Vide, Erreur, Chargement.
- **La cloche** affiche 6 notifications des deux produits (pastille CRM ou Envoi).
- **Ctrl K** : aller partout, chercher un envoi par adresse, ajouter une adresse IP, lancer une campagne vers une étiquette.
- **Tout arrêter** (dans Envoi, bouton rouge en haut) marche dans la maquette : un bandeau rouge reste affiché jusqu'à « Reprendre les envois ».
- Les boutons qui feraient un vrai travail affichent un petit message en bas à gauche.
- Contrôle automatique (`python3 _fabrique/controle.py --toutes`) : toutes les pages, 4 états, chaque onglet et chaque étape, à 1440, 1024, 768 et 360 px. Résultat du 01/11 (lot M2) : **73 pages, 1 300 vues, 0 chevauchement, 0 débordement, 0 contraste insuffisant (7:1 pour le texte courant), 0 texte sous 12 px, 0 taille hors échelle du CRM, 1 seul bouton plein par écran, 0 zone tactile sous 44 px au téléphone, 0 erreur JavaScript.**

## Test de 45 minutes avec Will : 7 tâches

Déroulé : Will pense à voix haute ; l'animateur ne l'aide pas et note le temps, les clics et les hésitations de plus de 5 s. Départ : `index.html` (Tableau de bord du CRM), sauf mention.

| # | Produit | Tâche donnée à Will (sans dire où cliquer) | Réussie si | Temps |
|---|---|---|---|---|
| T1 | CRM Pro | « Retrouvez la Boulangerie des Tilleuls, ajoutez-lui l'étiquette salon-artisans-2026, puis exportez votre sélection. » | Ma base › Entreprises, case cochée, étiquette posée, export lancé ; ≤ 3 min. Will reconnaît son écran actuel. | 6 min |
| T2 | CRM Pro | « Traitez les doublons : fusionnez une paire, écartez-en une autre. Puis validez une proposition. » | À traiter trouvé sans aide ; fusion et refus faits ; ≤ 3 min. | 6 min |
| T3 | CRM Pro | « Quels journalistes du Courrier du Rhône pouvez-vous contacter ? Consignez une relance. » | Presse › Médias › fiche ; journaliste opposé repéré ; échange consigné ; ≤ 3 min. | 6 min |
| T4 | Envoi | « Lancez une campagne vers l'étiquette salon-artisans-2026, en testant deux objets, demain à 9 h. » | ≤ 3 clics pour démarrer (Étiquettes › Campagne vers cette étiquette) ; A/B et date trouvés ; ≤ 5 min. | 8 min |
| T5 | Envoi | « La campagne Organisateurs : mettez-la en pause depuis la liste, changez la date, puis retrouvez ce qui est arrivé à Yves Roche. » | Pause en 3 clics ; date changée ; refus « Adresse inexistante » trouvé (Chercher un envoi ou onglet Destinataires) ; ≤ 4 min. | 7 min |
| T6 | Envoi | « Un domaine va mal : lequel, depuis quand ? Ajoutez ensuite une adresse IP et appliquez-la. » | Santé › feu › fiche domaine (2 clics) ; IP ajoutée en ≤ 3 clics (Ctrl K ou Serveurs) ; ≤ 4 min. | 6 min |
| T7 | Les deux | (téléphone, 360 px) « Passez du CRM à Envoi, répondez à Paul Morin depuis l'outil, puis revenez au CRM. » | Produit reconnu à la couleur sans hésiter ; réponse envoyée ; retour au CRM ; sans zoom. | 6 min |

**À la fin, 5 notes sur 10** : moderne, clair, peu de texte, boutons évidents, « je reconnais mon CRM ».

**Règle de décision** : toute tâche ratée ou plus lente que 1,5 fois la cible donne une correction de maquette **avant** le codage. Second passage de 15 min sur les tâches corrigées. Ensuite : **validation écrite de Will**.

## Les 10 parcours du plan 27 (3 clics au plus pour démarrer)

| # | Parcours | Chemin dans les maquettes | Clics |
|---|---|---|---|
| P1 | Campagne vers une étiquette | CRM › Étiquettes › « Campagne vers cette étiquette » (ou Ctrl K) | 2 pour démarrer |
| P2 | La programmer demain 9 h / la reprogrammer | Envoi › Campagnes › « Changer la date » › « Demain 9:00 » | 3 |
| P3 | Suivi d'une campagne | Envoi › Campagnes › ligne | 2 |
| P4 | Voir qu'un domaine chauffe mal | Envoi › Santé des envois › feu du domaine (fiche 30 jours) | 2 |
| P5 | Ajouter une adresse IP | Ctrl K › « Ajouter une adresse IP » › « Ajouter et appliquer » | 3 |
| P6 | Traiter une réponse intéressée | Envoi › Réponses › « Appliquer la suggestion » | 2 |
| P7 | Pause d'une campagne | Envoi › Campagnes › « Pause » › confirmer | 3 |
| P8 | Puis-je écrire à… ? | Ctrl K › « Puis-je écrire à… ? » › Vérifier | 3 |
| P9 | Résultats d'une boîte | Envoi › Boîtes d'envoi › tuile de la boîte | 2 |
| P10 | Ce qui est arrivé au message d'une personne | Ctrl K › « Chercher un envoi » (adresse) | 2 |

(Depuis le CRM, passer à Envoi ajoute 1 clic sur le sélecteur de produit ; Ctrl K marche partout.)

## Points à trancher par Will pendant le test

1. La teinte d'**Envoi** (turquoise pétrole `#0b7285`) lui convient-elle ? Assez distincte du bleu du CRM ?
2. **Tout arrêter** et le feu des envois : seulement dans Envoi (choix de ces maquettes) ou aussi dans l'en-tête du CRM ?
3. Mes tâches et Affaires en **onglets du Tableau de bord** (menu inchangé) : d'accord ?

## Fichiers

- `index.html` : Tableau de bord du CRM (reprise de `DashboardPage.tsx`).
- `campagnes.html` : accueil du produit Envoi.
- `GUIDE-STYLE.md` : composants du style, couleurs des deux produits.
- `captures/` : captures légères des pages clés (1440, 1024, 768, 360 px) et **2 comparaisons réel / maquette** (`comparaison-tableau-de-bord.png`, `comparaison-entreprises.png`).
- `style.css`, `app.js` : style et comportements (code maison, aucune bibliothèque).
- `_fabrique/` : scripts Python qui produisent toutes les pages et le fichier `plan/23-MAQUETTES-INDEX.md`. Pour changer une page : modifier le script, puis `python3 maquettes/_fabrique/fabrique.py`.

## Lot M2 : fidélité au vrai CRM (01/11/2026)

**Comment la comparaison a été faite.** Le vrai CRM (`axion-crm-pro/frontend`, version du dépôt, lecture seule) a été **lancé pour de vrai** (Vite, hors dépôt) avec une API simulée (données factices, comme ses tests e2e), puis photographié à 1440 px. Rien n'a été reconstitué à la main. Comparer côte à côte :

- `captures/comparaison-tableau-de-bord.png` : `DashboardPage.tsx` réel / `index.html`
- `captures/comparaison-entreprises.png` : `CompaniesListPage.tsx` réel / `entreprises.html`

| | Vrai CRM | Maquettes M1 (avant) | Maquettes M2 (maintenant) |
|---|---|---|---|
| Police | Inter | police système | Inter |
| Corps du texte | 14 px (`text-sm`) | 16 px | **14 px** |
| Détails, pastilles | 12 px (`text-xs`) | 14 à 16 px | **12 px** |
| Titre de page | 24 px, 30 px dès 768 px (36 px sur l'accueil) | 28 px | **24 px** |
| Titre de section | 18 px gras | 20 px | **18 px gras** |
| Chiffres des tuiles | 24 px (30 à 36 px sur l'accueil) | 36 à 44 px | **24 px** |
| Boutons | 36 px, 14 px, rayon 8 px | 44 à 48 px, 16 à 17 px, rayon 12 px | **36 px, 14 px, rayon 8 px** (44 px au téléphone) |
| Couleur de marque | `brand-600` `oklch(0.45 0.20 250)` = `#0051bd` | `#2448e5` | **`#0051bd`** |
| Barre latérale | bleu profond `#04203a`, 260 px, texte `#d4dfeb` | blanche, 264 px | **`#04203a`, 260 px, texte `#d4dfeb`** |
| En-tête | même bleu profond | blanc | **même bleu profond** |
| Cartes | blanches, rayon 16 px, ombre douce | rayon 16 px, cadre foncé | rayon 16 px, ombre du CRM, cadre `slate-300` |

### Résumé (15 lignes)

1. Le socle `style.css` est réécrit d'après le code réel du CRM : Inter, 14 px pour le texte, 12 px pour les détails.
2. Titres : 24 px (page), 18 px gras (section), 16 px (carte) ; chiffres des tuiles 24 px.
3. Boutons et champs 36 px, rayon 8 px ; cartes rayon 16 px, ombres `--shadow-*` du CRM.
4. Barre latérale et en-tête bleu profond `#04203a` (jetons `--color-sidebar-*`), 260 px, rail de 64 px.
5. CRM Pro prend la vraie couleur de marque `#0051bd` ; Envoi le turquoise pétrole `#0b7285` de l'ADR-13.
6. Les deux produits partagent la même feuille : seule la couleur d'identité change (liseré, sélecteur, badge, bouton plein).
7. Couleurs de sens accordées à la palette du CRM (orange, sky, emerald, amber, violet, rose) ; pastilles au style `StatusPill`.
8. Gardé : un seul bouton plein par écran, contraste ≥ 4,5:1 partout et ≥ 7:1 pour le texte courant.
9. Zones tactiles de 44 px au téléphone seulement ; sur ordinateur, tailles du vrai CRM.
10. `controle.py` : minimum 12 px, contrôle de fidélité (12, 14, 16, 18, 20, 24 px), zones tactiles.
11. Résultat : 73 pages, 1 300 vues, 0 problème aux 4 largeurs ; aucune page supprimée.
12. Écart 1 : le vrai CRM met ses titres de page à 30 px dès 768 px et les chiffres de l'accueil à 30-36 px ; ici 24 px au plus (consigne).
13. Écart 2 : le bouton principal du CRM est ardoise `slate-900` ; ici il prend la couleur du produit (ADR-13).
14. Écart 3 : texte secondaire `slate-600` (7,6:1) au lieu de `slate-500` (4,8:1) ; cadres un cran plus nets ; titres de groupe du menu 12 px au lieu de 13 px ; titres de carte 16 px au lieu de 14 px.
15. Écart 4 : les tuiles du CRM (KpiCard) ont un libellé en pastille colorée ; ici une icône pâle + libellé ; le cadre « Maquette » et la bande produit de l'en-tête n'existent pas dans le CRM.
