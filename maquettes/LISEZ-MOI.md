# Maquettes cliquables : Axion CRM Pro et Axion Envoi (lot M1)

Deux produits distincts, facturés à part, **avant tout codage**. Données factices uniquement (aucun vrai nom, domaines en `.example`, adresses IP de documentation). Rien n'est relié à un serveur.

## Comment ouvrir

1. Téléchargez ou clonez le dépôt `axion-crm-pro-plans`.
2. Ouvrez `maquettes/index.html` (Tableau de bord du CRM) en double-cliquant dessus (Chrome, Edge ou Firefox récent). Aucune installation.
3. **Changer de produit** : en haut du menu, le sélecteur **CRM Pro** (bleu) | **Envoi** (bleu-vert).
4. **Toutes les pages d'un coup** : « Toutes les maquettes » en bas du menu (`plan-des-pages.html`).
5. **Téléphone** : touche F12, icône téléphone, largeur **360 px**.

## Ce qui est à savoir

- **Deux produits, deux couleurs.** CRM Pro = bleu `#2448e5`. Envoi = bleu-vert `#0a6e78`. On voit le produit partout : liseré du menu, sélecteur en haut du menu, badge et bande colorée dans l'en-tête, bouton principal de la couleur du produit. Les couleurs de sens ne changent pas (vert = fait, terracotta = à faire, ambre = attention, bleu = en cours, violet = nouveau, rouge = arrêté).
- **Menu du CRM = menu réel de Will, à l'identique** (Tableau de bord, À traiter, Ma base, Presse, Réseaux, Ciblage, Alimenter la base, Réglages, Technique), en accordéon comme aujourd'hui. **Envoi** a son propre menu (Campagnes, Réponses, Boîtes d'envoi, Domaines, Serveurs et adresses IP, Chauffe, Santé des envois, Désinscriptions, Alertes d'envoi, Réglages d'envoi).
- **Le cadre violet pointillé « Maquette », sous l'en-tête, n'est pas dans le produit.** Il dit si la page est **« Reprise de : <composant réel> »** ou **« Nouvelle »**, et permet de voir les 4 états : Normal, Vide, Erreur, Chargement.
- **La cloche** affiche 6 notifications des deux produits (pastille CRM ou Envoi).
- **Ctrl K** : aller partout, chercher un envoi par adresse, ajouter une adresse IP, lancer une campagne vers une étiquette.
- **Tout arrêter** (dans Envoi, bouton rouge en haut) marche dans la maquette : un bandeau rouge reste affiché jusqu'à « Reprendre les envois ».
- Les boutons qui feraient un vrai travail affichent un petit message en bas à gauche.
- Contrôle automatique (`python3 _fabrique/controle.py --toutes`) : toutes les pages, 4 états, chaque onglet et chaque étape, à 1440, 1024, 768 et 360 px. Résultat dans `plan/23-MAQUETTES-INDEX.md` et ci-dessous.

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

1. La teinte d'**Envoi** (bleu-vert `#0a6e78`) lui convient-elle ? Assez distincte du bleu du CRM ?
2. **Tout arrêter** et le feu des envois : seulement dans Envoi (choix de ces maquettes) ou aussi dans l'en-tête du CRM ?
3. Mes tâches et Affaires en **onglets du Tableau de bord** (menu inchangé) : d'accord ?

## Fichiers

- `index.html` : Tableau de bord du CRM (reprise de `DashboardPage.tsx`).
- `campagnes.html` : accueil du produit Envoi.
- `GUIDE-STYLE.md` : composants du style, couleurs des deux produits.
- `captures/` : captures légères des pages clés (1440, 1024, 768, 360 px).
- `style.css`, `app.js` : style et comportements (code maison, aucune bibliothèque).
- `_fabrique/` : scripts Python qui produisent toutes les pages et le fichier `plan/23-MAQUETTES-INDEX.md`. Pour changer une page : modifier le script, puis `python3 maquettes/_fabrique/fabrique.py`.
