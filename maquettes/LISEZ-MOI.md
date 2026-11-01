# Maquettes cliquables : Axion CRM Pro 2027 (lots U0 + U1)

Toutes les pages du CRM et la barre latérale, **avant tout codage**. Données factices uniquement. Rien n'est relié à un serveur : aucun envoi, aucune donnée réelle.

## Comment ouvrir

1. Téléchargez ou clonez le dépôt `axion-crm-pro-plans`.
2. Ouvrez `maquettes/index.html` en double-cliquant dessus (Chrome, Edge ou Firefox récent). Aucune installation.
3. Pour voir **toutes les pages d'un coup** : menu « Toutes les maquettes » en bas de la barre latérale (`plan-des-pages.html`).
4. Pour voir le **téléphone** : touche F12, puis l'icône téléphone, puis largeur **360 px**.

## Ce qui est à savoir

- **Le cadre violet pointillé en bas à droite n'est pas dans le produit.** Il sert à voir chaque écran dans ses 4 états : **Normal, Vide, Erreur, Chargement**.
- **Ctrl K** (ou la barre « Rechercher ou agir… ») : aller partout et lancer une action.
- **Raccourcis** : `G` puis `A` (Aujourd'hui), `R` (Réponses), `C` (Campagnes), `F` (Affaires), `T` (Tâches), `S` (Santé des envois). Désactivables dans « Mon compte ».
- **Tout arrêter** (bouton rouge en haut) marche vraiment dans la maquette : un bandeau rouge apparaît sur toutes les pages jusqu'à « Reprendre les envois ».
- Les boutons qui feraient un vrai travail affichent un petit message en bas à gauche (avec « Annuler » quand c'est réversible).
- Règles tenues : clair seulement ; **un seul bouton plein par écran** ; peu de texte ; « Affaires » et non « Pipeline » ; alertes **console + e-mail** seulement ; aucune marque blanche ; aucun constructeur visuel d'automatisations.
- Contrôle automatique fait le 01/11 : 45 pages × 4 états × 2 largeurs (1 280 px et 360 px) : **0 erreur, 0 défilement horizontal, 0 page avec deux boutons pleins, 0 violation d'accessibilité** (axe-core, WCAG 2.2 AA).

## Test de 45 minutes avec Will : 7 tâches

Déroulé : Will pense à voix haute, l'animateur ne l'aide pas et note le temps, les clics et les hésitations de plus de 5 s. Commencer chaque tâche depuis `index.html`.

| # | Tâche donnée à Will (sans dire où cliquer) | Réussie si | Temps prévu |
|---|---|---|---|
| T1 | « Dites-moi ce que vous devez faire aujourd'hui. » | Il le dit en ≤ 10 s en lisant seulement « Aujourd'hui ». | 2 min |
| T2 | « Traitez la réponse de Claire Durand, puis enregistrez le STOP de Louis Bernard. » | Suggestion appliquée en 1 geste ; opposition enregistrée ; ≤ 3 min. | 6 min |
| T3 | « Une boîte a un problème : que s'est-il passé ? Puis arrêtez tous les envois et relancez-les. » | Il explique la cause en ≤ 30 s (Alertes → « Voir ce qui s'est passé ») ; « Tout arrêter » en 2 clics ; reprise trouvée. | 6 min |
| T4 | « Lancez une campagne vers les Organisateurs Rhône-Alpes avec le message type n° 1. » | ≤ 5 min et ≤ 15 clics, sans retour en arrière par confusion. | 8 min |
| T5 | « Peut-on écrire à paul@boulangerie-martin.example ? » | Réponse « Non » trouvée en ≤ 10 s (Désinscriptions ou Ctrl K « Puis-je écrire à… ? »). | 2 min |
| T6 | « Faites-vous prévenir par e-mail des réponses intéressées, puis envoyez-vous une alerte de test. » | Réglages › Alertes et avis trouvé, case cochée, test envoyé ; ≤ 2 min. | 5 min |
| T7 | (téléphone, 360 px) « Ouvrez le menu, allez dans Réponses et classez 2 réponses. » | Sans zoom, sans erreur de cible. | 6 min |

Reste du temps (≈ 10 min) : faire défiler `plan-des-pages.html` et noter les pages à revoir.

**À la fin, 5 notes sur 10** : moderne, clair, peu de texte, boutons évidents, confiance pour lancer un envoi.

**Règle de décision** : toute tâche ratée ou plus lente que 1,5 fois la cible donne une correction de maquette **avant** le codage. Second passage de 15 min sur les seules tâches corrigées. Ensuite : **validation écrite de Will** (condition de fin du lot U1).

## Points à trancher par Will pendant le test

1. Barre latérale à **18 entrées en 4 groupes repliables** (choix de ces maquettes) ou **7 entrées avec onglets** (plan 07) ?
2. Barre latérale **blanche** (choix de ces maquettes, pour rester « clair seulement ») ou bleu nuit ?
3. « **Montée en douceur** » ou « **Chauffe** » dans le menu ?

## Fichiers

- `index.html` : coquille (barre latérale, en-tête, recherche, centre d'alertes) + Aujourd'hui.
- `style.css` : jetons de design (couleurs, espacements, rayons, typographie système, états vide / chargement / erreur, contrastes AA mesurés).
- `app.js` : comportements (menu, onglets au clavier, fenêtres, Ctrl K, états, Tout arrêter). Code maison, aucune bibliothèque, aucune police externe.
- Une page HTML par écran (liste complète : `plan/23-MAQUETTES-INDEX.md`).
- `_fabrique/` : script Python qui produit toutes les pages HTML et le fichier 23. Pour changer une page : modifier le script, puis lancer `python3 maquettes/_fabrique/fabrique.py`.
