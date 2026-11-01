# 12 : Vérification de l'interface écran par écran (01/11/2026)

Rédigé par le responsable Interface de l'équipe, **en lecture seule**. Aucun code applicatif n'a été écrit, aucun e-mail envoyé, aucun serveur touché, aucun secret recopié. Rien n'a été rejoué dans un navigateur : ce sont des constats sur les plans et sur le code lu.

**Sources lues**
- `07-ux-ui-2027.md` **en entier** (876 lignes) : 12 principes, menu à 7 entrées, 13 écrans, système de design, 5 parcours, critères, questions Q1 à Q12.
- Par recherche ciblée : `10` (liste complète), `11` (inventaire SOS-Expat, § 2, 3, 5, 6, 14, 15, 16, 18), `02` (fonctions A1 à M13), `03` (§ 2, 3, 4, 5, 7, 8, 10, 13), `08` (blocs A, B, C, F). Survol de `00`, `04`, `05`, `06`, `REPRENDRE`.
- Code actuel `axion-crm-pro` (lecture) : `frontend/src/app/routeTree.tsx` (57 routes), `features/` (24 dossiers), `components/ui/` (32 composants), `features/users/UsersPage.tsx`, `features/settings/SettingsPage.tsx`, `features/rgpd/AuditLogsPage.tsx`, `components/layout/NotificationsBell.tsx`.

**Décisions de Will appliquées dans tout ce document** : fonctions complètes (seuls les volumes démarrent petit) ; campagnes au cœur ; KumoMTA ; alertes **dans la console et par e-mail seulement**, jamais téléphone ni Telegram ; **pas de mode sombre** ; aucun lien avec systeme.io ; **ne sont pas proposés** : constructeur visuel d'automatisations, modèles clients, agenda par client, connecteur systeme.io, serveur MCP, marque blanche ; interface organisée, moderne, peu de texte, boutons clairs, blocs colorés validés.

**Légende des tableaux**
- **OUI** : un écran de 07 pilote la fonction, avec son bouton.
- **PARTIEL** : la fonction est citée (onglet, phrase, bouton) mais sans maquette, sans états ou sans le bouton qui la pilote.
- **TROU** (= « AUCUN ÉCRAN ») : aucun écran. La fonction n'est pilotable que par une commande ou par le code.
- Les identifiants **UI-xx** renvoient aux corrections du § 5 ; **C-xx** aux corrections des écrans existants de 07 (§ 3).

---

## 0. Verdict en une phrase

**Non, l'interface de 07 ne couvre pas 100 % des fonctions du plan** : sur **128 fonctions** recensées, **51 sont pilotées par un écran (40 %)**, **36 le sont en partie (28 %)** et **41 n'ont aucun écran (32 %)**. Les 13 écrans de 07 sont solides pour le travail quotidien (Aujourd'hui, fiche, pipeline, campagne, réponses, santé, opposition), mais **l'exploitation de l'envoi** (IP, serveurs, configuration, règles de prudence, alertes, DMARC, sauvegardes) et **l'administration** (équipe, journal, exports, usage des clients) sont des trous. Avec les **71 corrections du § 5** (≈ 42 jours-agent en V0, ≈ 34,5 en V1, ≈ 5,5 en V2), la couverture atteint 100 %.

---

## 1. Matrice FONCTION → ÉCRAN → BOUTON

Le chemin d'écran suit le menu de 07 § 2.1 corrigé par C-09 et C-17 (voir § 3). Le bouton cité est le **bouton qui pilote la fonction** (principal plein s'il est marqué ■).

### 1.1 Accès, sécurité, équipe

| # | Fonction (source) | Écran qui la pilote | Bouton | État | Correction |
|---|---|---|---|---|---|
| 1 | Connexion et code à 6 chiffres par e-mail (02 I1, 04) | Connexion (07 § 3.13) | ■ Valider | OUI | C-04 (états) |
| 2 | Codes de secours : affichage unique, régénération (04) | Réglages › Mon compte | Régénérer les codes | PARTIEL (cité, pas de maquette) | UI-12 |
| 3 | Appareils connectés, déconnexion à distance (02 I9) | Réglages › Mon compte | Déconnecter cet appareil | PARTIEL | UI-12 |
| 4 | Code redemandé pour export et gestes sensibles (07 § 4.3) | Fenêtre de confirmation | ■ Confirmer | OUI | — |
| 5 | Inviter, désactiver un utilisateur (existe : `/users`) | Réglages › Équipe | ■ Inviter une personne | PARTIEL (écran existant, non maquetté dans 07) | UI-11 |
| 6 | Rôles : propriétaire, membre, membre « envois », lecteur ; rôles fins en V1 (02 I8, M2) | Réglages › Équipe | Changer le rôle | PARTIEL | UI-11 |
| 7 | Accès support d'Axion limité dans le temps et tracé (02 M2) | Bandeau violet seulement | — | PARTIEL (aucun écran pour accorder, retirer, relire) | UI-32 |
| 8 | Journal d'audit (existe : `/audit-logs`) | Réglages › Journal | Filtrer · Exporter | PARTIEL (rangé dans « Technique », sans maquette) | UI-10 |
| 9 | Journal des lectures de fiches nominatives (02 I7) | Réglages › Journal | Filtre « Lectures » | PARTIEL | UI-10 |
| 10 | Bascule de client (07 § 3.12) | Barre latérale | Basculer vers… | OUI | — |

### 1.2 Contacts, listes, étiquettes

| # | Fonction | Écran | Bouton | État | Correction |
|---|---|---|---|---|---|
| 11 | Fiche entreprise / personne (02 A1, A2) | Contacts › fiche (07 § 3.2) | ■ Marquer comme faite (prochaine action) | OUI | — |
| 12 | Ajout rapide d'une personne ou entreprise, dédoublonnage à la saisie (02 A4) | Palette « Ajouter une entreprise » | — | PARTIEL (pas de formulaire) | UI-55 |
| 13 | Modifier, mettre en corbeille un contact (02 A3) | Fiche › ⋯ | — | PARTIEL (non montré) | UI-55 |
| 14 | Notes, appels, rencontres (02 A5) | Fiche › barre d'ajout rapide | Note · Appel · Tâche | OUI | — |
| 15 | Chronologie unifiée (02 A6) | Fiche › Activité | filtres en puces | OUI | — |
| 16 | Badges d'envoi : vérifiée, informée, opposition (02 A7) | Fiche › bloc vert « Joignable » | — | OUI | — |
| 17 | Personne partie ou remplacée (02 A11, F5) | Fiche personne | Proposer la remplaçante | OUI | — |
| 18 | Champs personnalisés par espace (02 A12, 08 F7) | — | — | TROU | UI-35 |
| 19 | Responsable de fiche, réaffectation (02 A13, D9) | Filtre « Responsable » du pipeline | — | PARTIEL | UI-56 |
| 20 | Doublons : fusion réversible (existe) | Contacts › Doublons | Fusionner | OUI (existant) | — |
| 21 | Recherche globale (existe) | En-tête, Ctrl+K | — | OUI | — |
| 22 | Import de fichier par l'interface (02 B4) | Contacts › Listes › Importer (assistant 4 étapes, 07 § 3.4) | ■ Importer | OUI | — |
| 23 | Export de la sélection ou d'une liste, journalisé (02 B1, B5) | Barre d'action collante | Exporter | OUI | — |
| 24 | Export complet d'un espace, réversibilité (02 B7) | — | — | TROU | UI-20 |
| 25 | Déclarer des envois faits à la main (02 B6) | — | — | TROU | UI-34 |
| 26 | Import planifié depuis un fichier ou une URL (02 B8) | — | — | TROU | UI-57 |
| 27 | Étiquettes : création, pose en masse (02 C1) | Contacts › Étiquettes ; barre collante | Étiqueter | OUI | — |
| 28 | Règles automatiques d'étiquettes (existe : `/tags`) | Contacts › Étiquettes | — | PARTIEL (onglet cité, non maquetté) | UI-27 (même lot de maquettes Réglages) |
| 29 | Listes fixes (02 C2) | Contacts › Listes (07 § 3.4) | ■ Nouvelle liste | OUI | — |
| 30 | Listes dynamiques, constructeur en phrases (02 C3) | Contacts › Listes dynamiques | ■ Nouvelle liste | OUI | — |
| 31 | Vues sauvegardées (02 C4) | — | — | TROU | UI-36 |
| 32 | Joignables : volume réellement envoyable (02 C10, H6) | Colonne « Joignables » | — | OUI | — |

### 1.3 Pipeline, tâches, rendez-vous

| # | Fonction | Écran | Bouton | État | Correction |
|---|---|---|---|---|---|
| 33 | Kanban par étape, alternative clavier (02 D2) | Pipeline (07 § 3.3) | ■ Ajouter une opportunité | OUI | C-09 (libellé) |
| 34 | Montant informatif, raison de perte (02 D3) | Pipeline | Déplacer vers… | OUI | — |
| 35 | Mes tâches (02 D5) | Pipeline › Mes tâches | ■ Ajouter une tâche | OUI | — |
| 36 | Récapitulatif du matin par e-mail (02 D6) | Dispositif transverse | — | PARTIEL (heure et contenu non réglables) | UI-02 |
| 37 | Tâches automatiques : sans réponse, RDV non honoré (02 D7) | — | — | TROU | UI-44 |
| 38 | Suggestions de recontact (02 D8) | — | — | TROU | UI-63 |
| 39 | Attribution d'un RDV à sa campagne (02 G3) | Statistiques, suivi de campagne | — | OUI | — |
| 40 | RDV pris → étape « opportunité » (02 G4) | Pipeline (automatique, visible) | — | OUI | — |
| 41 | Lien vers le dossier client de la console (02 G6) | Fiche › bloc gris | Ouvrir dans la console | OUI | — |

### 1.4 Campagnes (le cœur)

| # | Fonction | Écran | Bouton | État | Correction |
|---|---|---|---|---|---|
| 42 | Liste des campagnes, statuts, filtres (02 E1 ; 03 § 7.3) | Campagnes › Campagnes | ■ Nouvelle campagne | PARTIEL (07 n'a ni maquette de liste ni de suivi) | UI-58 |
| 43 | Assistant en 5 étapes (02 E2) | Campagnes › Nouvelle (07 § 3.5) | ■ Continuer : <étape> | OUI | C-07 |
| 44 | Ciblage ET / OU / SAUF, exclusions par historique (03 § 2.2) | Assistant › ① Cible | — | OUI | — |
| 45 | Exclusions manuelles par campagne : adresse, organisation, domaine (03 § 2.2, remontée V1) | — | — | TROU | UI-25 |
| 46 | Liste figée au départ, instantané tracé (02 C8) | Assistant › ⑤ (« Version a3f9 ») | — | PARTIEL (l'instantané n'est pas nommé) | UI-25 |
| 47 | Séquence de 1 à 4 étapes, étapes manuelles (02 E3, E4) | Assistant › ③ Séquence | + Ajouter une étape | OUI | — |
| 48 | Planification : fenêtres, jours fériés (02 E9) | Assistant › ③ (repliée) | — | OUI | — |
| 49 | Pression commerciale par personne et par entreprise (02 E10) | — | — | TROU (aucun réglage, seulement l'exclusion) | UI-26 |
| 50 | Feu vert : 31 contrôles avec bouton correcteur (03 § 2.6) | Assistant › ④ Vérification | Corriger le lien… | OUI | — |
| 51 | Aperçu de 20 messages tels qu'ils partiront (02 E8) | Assistant › ④ | Voir 20 messages | OUI | — |
| 52 | « M'envoyer un test » par message et par campagne (11 § 18 n° 1) | Assistant › ④ ; éditeur | M'envoyer un test | PARTIEL (bouton présent, ni destinataires, ni résultat, ni hors chauffe) | UI-06 |
| 53 | Validation par Will attachée à la version, refus motivé (02 E8) | Assistant › ⑤ | ■ Valider et programmer | OUI | — |
| 54 | 5 minutes pour annuler au-delà de 500 destinataires | Toast collant | Annuler le départ | OUI | C-06 |
| 55 | Pause, reprise, annulation d'une campagne (02 E11) | Suivi de campagne (prose) | Mettre en pause · Reprendre | PARTIEL (pas de maquette, pas d'états) | UI-58 |
| 56 | Suivi d'une campagne : frise, tuiles, journal des décisions (02 E17) | Suivi de campagne (prose) | — | PARTIEL | UI-58 |
| 57 | Variantes et test A/B : création (02 E12 ; 03 § 2.7) | — (résultat seulement dans Statistiques) | — | TROU | UI-23 |
| 58 | Messages types : liste, versions, « utilisé par » (02 E5) | Campagnes › Messages types (onglet cité) | — | PARTIEL (seul l'éditeur est maquetté) | UI-08 |
| 59 | Éditeur de message, relecture automatique, champs (02 E5, E7) | Éditeur (07 § 3.6) | ■ Enregistrer et continuer | OUI | C-05 |
| 60 | Historique des versions | Éditeur › ⋯ | Historique des versions | OUI | — |
| 61 | Bloc d'information art. 14 et pied légal : textes du client (02 E6, J5) | Inséré d'office ; texte réglé nulle part | — | PARTIEL | UI-13 |
| 62 | Lien de prise de RDV personnalisé (02 E14, P0) | — | — | TROU | UI-59 |
| 63 | Campagnes presse : communiqué par lien, relances J+5 / J+10 (02 E15 ; 03 § 7.4) | Campagnes › Presse (onglet cité) | — | PARTIEL (aucune maquette dans 07) | UI-24 |
| 64 | Messages déclenchés par un événement (02 E19 ; 08 F10) | — | — | TROU | UI-37 |
| 65 | Lettre d'information : abonnés consentants, double inscription, formulaires (08 F8, F9) | — | — | TROU | UI-38 |
| 66 | Centre de préférences, version web, éditeur par blocs (08 F16 à F18) | — | — | TROU | UI-38 |
| 67 | Campagnes récurrentes (02 E18) | — | — | TROU | UI-38 |
| 68 | Variations de texte par IA, chaque version validée (02 E13) | — | — | TROU | UI-52 |
| 69 | Écrire un message à une personne depuis sa fiche (02 E16) | — | — | TROU | UI-33 |
| 70 | Règles de passage entre campagnes (03 § 2.4, V1) | — | — | TROU | UI-44 |

### 1.5 Réponses

| # | Fonction | Écran | Bouton | État | Correction |
|---|---|---|---|---|---|
| 71 | File des réponses, classement en un geste (02 F6) | Réponses (07 § 3.7) | ■ action suggérée | OUI | — |
| 72 | STOP clair appliqué, STOP ambigu à confirmer, opposition par domaine (02 F3) | Réponses › STOP à confirmer | Confirmer l'opposition | OUI | — |
| 73 | Demande RGPD reçue par réponse (02 F4) | Réponses | Demande RGPD | OUI | — |
| 74 | « Écrivez plutôt à… » (02 F5) | Réponses | Mauvaise personne | OUI | — |
| 75 | Réponses à rattacher (sans jeton) | Réponses › À rattacher (onglet cité) | — | PARTIEL | UI-61 |
| 76 | Répondre depuis la console (02 F7, V1) | Réponses | Répondre ▾ | PARTIEL (pas de composeur) | UI-60 |
| 77 | Alerte si une réponse « intéressé » attend plus de 24 h (02 F8) | Cloche | — | PARTIEL | UI-02 |
| 78 | Avis immédiat d'une réponse « intéressé » (11 § 18 n° 2) | — (pas d'e-mail prévu) | — | TROU | UI-03 |
| 79 | Frein quand les réponses s'accumulent (06 C7) | — | — | TROU | UI-45 |

### 1.6 Santé des envois, serveurs, délivrabilité

| # | Fonction | Écran | Bouton | État | Correction |
|---|---|---|---|---|---|
| 80 | Feux par domaine et par boîte (03 § 3.3) | Santé des envois (07 § 3.8) | Pourquoi | OUI | C-01 |
| 81 | Montée en douceur : palier, courbe (03 § 3.1) | Santé › Montée en douceur | — | OUI (lecture) | C-08 |
| 82 | Réglage de la courbe de montée (03 § 3.1 « réglable ») | — | — | TROU | UI-07 |
| 83 | Règles d'arrêt et de ralentissement, seuils (03 § 3.2, `emailing_seuils`) | — (seul le tiroir « Pourquoi » les cite) | — | TROU | UI-07 |
| 84 | Tout arrêter et reprendre, par portée (03 § 3.3) | En-tête, toutes pages | Tout arrêter | OUI | C-12 |
| 85 | Pause d'une boîte | Santé › Domaines et boîtes | Pause | OUI | — |
| 86 | Ajouter un domaine : assistant DNS (03 § 7.2) | Santé › Expéditeurs (07 § 3.9) | ■ Vérifier maintenant | OUI | C-05 |
| 87 | Ajouter, modifier une boîte, test de connexion (03 lot E4 ; 11 n° 61) | Assistant domaine › ④ seulement | — | PARTIEL | UI-14 |
| 88 | Adresses IP d'envoi : PTR, groupe, palier (03 § 7.2 onglet IP) | — | — | TROU | UI-05 |
| 89 | Santé des serveurs : services, file, disque, homme mort (03 § 7.6) | Santé › Serveurs (onglet cité) | — | PARTIEL (pas de maquette dans 07) | UI-04 |
| 90 | Ajouter un serveur d'envoi (11 n° 56, INF-041) | — | — | TROU | UI-16 |
| 91 | Appliquer la configuration du serveur depuis la base (03 § 10, `appliquerConfiguration`) | — | — | TROU | UI-15 |
| 92 | Files d'attente par client, fournisseur, campagne (08 F6) | — | — | TROU | UI-39 |
| 93 | Listes noires : détail par IP et domaine, revérifier (03 § 7.1) | Santé › bloc gris « Listes noires » | — | PARTIEL | UI-50 |
| 94 | Boîtes témoins et test de fumée de 06:45 (03 § 7.6) | — | — | TROU | UI-04 |
| 95 | Rapports DMARC agrégés (11 n° 37, 81) | — | — | TROU | UI-17 |
| 96 | Expiration des domaines et certificats (11 § 18 n° 4) | — | — | TROU | UI-18 |
| 97 | Sources de mesure, Postmaster, SNDS (11 n° 161) | — | — | TROU | UI-40 |
| 98 | Vérification des adresses : verdicts, fraîcheur 30 j, coût, crédits (03 § 4) | — | — | TROU | UI-21 |
| 99 | Centre d'alertes : règles, gravité, action déjà prise (03 § 7.7) | Santé › Alertes (onglet cité) | — | PARTIEL | UI-01 |
| 100 | Réglages des alertes : types, canaux console / e-mail, destinataires, alerte de test (02 L4) | — | — | TROU | UI-02 |
| 101 | Rapports du matin, hebdomadaire, archivés (02 H7 ; 11 n° 135, 136) | E-mail seulement | — | PARTIEL | UI-43 |
| 102 | Ne plus écrire : « Puis-je écrire à… ? » (02 J2) | Santé › Ne plus écrire (07 § 3.10) | Vérifier | OUI | C-02 |
| 103 | Réautoriser une erreur technique, avec motif | Ne plus écrire | Réautoriser (motif) | OUI | — |
| 104 | Page publique de désinscription et « pourquoi ce message » (03 § 5) | — (page publique non dessinée) | — | PARTIEL | UI-62 |

### 1.7 Statistiques

| # | Fonction | Écran | Bouton | État | Correction |
|---|---|---|---|---|---|
| 105 | Résultats, entonnoir, activité (02 H3 à H5) | Statistiques (07 § 3.11) | Exporter ▾ | OUI | C-03 |
| 106 | Carte de couverture (existe) | Statistiques › Couverture | — | OUI | — |
| 107 | Coût mensuel, information seulement (02 H8) | Statistiques | — | OUI | — |
| 108 | Export d'un rapport de campagne pour un client (08 F12) | Statistiques › Exporter ▾ | — | PARTIEL | UI-43 |

### 1.8 Conformité

| # | Fonction | Écran | Bouton | État | Correction |
|---|---|---|---|---|---|
| 109 | Demandes RGPD (existe : `/rgpd/requests`) | Réglages › Conformité | — | PARTIEL (déplacée, non maquettée) | UI-28 |
| 110 | Écran Conformité : registre, sous-traitants, versions des textes (02 J12) | Réglages › Conformité (onglet cité) | — | PARTIEL | UI-27 |
| 111 | Ouvrir une famille fermée (presse, santé, syndicats), case tracée (03 G4) | Assistant (grisée, « Fermée par réglage ») | — | TROU (aucun écran pour ouvrir) | UI-26 |
| 112 | Registre « informé le » par adresse (02 J5) | Fiche › bloc vert | — | OUI | — |

### 1.9 Clients et plateforme

| # | Fonction | Écran | Bouton | État | Correction |
|---|---|---|---|---|---|
| 113 | Créer un client (02 M13 ; 05) | Réglages › Clients (07 § 3.12) | ■ Créer l'espace du client | OUI | C-11, C-15 |
| 114 | Supervision de tous les clients (02 M11) | Vue « Tous les clients » (citée) | — | PARTIEL | UI-32 |
| 115 | Usage, forfait, quotas, remise à zéro à la date anniversaire (02 M5) | — | — | TROU | UI-31 |
| 116 | Diagnostic par client, demande de support (02 M10) | — | — | TROU | UI-32 |
| 117 | Sauvegarde et restauration d'un seul client (02 M7) | — | — | TROU | UI-09 |
| 118 | Mises à jour par vagues, version par client (02 M9) | — | — | TROU | UI-41 |
| 119 | Clés d'API par espace (08 F11) | — | — | TROU | UI-42 |
| 120 | Webhooks sortants signés (08 F19) | — | — | TROU | UI-42 |

### 1.10 Exploitation et transverse

| # | Fonction | Écran | Bouton | État | Correction |
|---|---|---|---|---|---|
| 121 | État des sauvegardes : dernière, hors site, plafond 9 Go, exercice de restauration (02 L1, L2) | — | — | TROU | UI-09 |
| 122 | Interrupteurs des automatisations (11 n° 143, CON-009) | — | — | TROU | UI-30 |
| 123 | Santé de la synchro console (02 K4) | Réglages › Synchro console (onglet cité) | — | PARTIEL | UI-29 |
| 124 | Collectes et enrichissement (existe : `/campaigns`) | Réglages › Technique › Collectes | — | OUI (déplacé) | — |
| 125 | Moteurs d'IA, journal technique, registre IA (existe) | Réglages › Technique | — | OUI (existant) | — |
| 126 | Mise en route en 5 jalons (07 § 1) | Aujourd'hui › bloc violet | Commencer | PARTIEL (jalons sans écrans détaillés) | UI-19 |
| 127 | Aide courte par module (02 L10) | « ? » et page Aide | — | PARTIEL | UI-46 |
| 128 | Cloche, bandeau rouge, palette d'actions (07 § 1) | En-tête | — | OUI | — |

**Décompte** : 128 fonctions ; **OUI 51** ; **PARTIEL 36** ; **TROU 41**.

---

## 2. Parcours « ajouter sans coder »

Question posée pour chacun : **peut-on le faire avec l'interface seule ?** Pour chaque parcours : l'écran, les étapes, ce que le système fait ensuite, ce qui reste manuel en V0, et comment le rendre faisable dès la V0 sans risque.

Règle commune proposée pour tous les ajouts techniques : **l'interface décrit, le serveur tire**. Le CRM écrit une **version de configuration** en base ; le serveur d'envoi la **tire** par le tunnel privé, la valide à blanc (`validerConfiguration`), l'applique, puis le test de fumée confirme. **Aucune clé SSH dans le CRM, aucun secret affiché, aucun shell lancé depuis l'interface.** Retour arrière automatique à la version précédente si le test échoue. C'est l'objet de **UI-15**.

### 2.1 Ajouter un domaine d'envoi

| | |
|---|---|
| **Écran** | Santé des envois › Expéditeurs › ■ Ajouter un domaine (assistant 07 § 3.9) |
| **Étapes** | ① saisir le domaine (contrôle de nommage, refus de `axion-ia.com` et du domaine principal, âge affiché) → ② copier les lignes DNS → ③ vérification toutes les 2 min → ④ ajouter les boîtes |
| **Le système ensuite** | Génère la clé de signature **côté serveur** (seule la clé publique est affichée), contrôle DNS quotidien à 06:30, compte à rebours des 21 jours d'âge, inscrit le domaine au registre, prépare `go.<domaine>` (désinscription) et `bounce.<domaine>`, l'intègre à la courbe au palier P1 le jour où il est prêt |
| **Manuel en V0** | (1) Acheter le domaine (Will). (2) Poser les lignes DNS chez l'hébergeur DNS (Cloudflare par API seulement en V1). (3) **Charger le domaine et sa clé dans la configuration du serveur d'envoi** : en V0, le plan 03 § 13 range « configuration depuis la base » en V1, donc c'est **une intervention à la main**. (4) Certificat de `go.<domaine>`. (5) Adresse de réception des rapports DMARC. |
| **Faisable dès la V0 sans risque** | Avancer **UI-15** en V0 (configuration générée et tirée par le serveur) : le domaine passe de « DNS vérifié » à « Prêt sur le serveur (configuration v8) » sans intervention. Certificat de `go.` émis automatiquement par le serveur web à la première requête **pour les seuls domaines inscrits au registre** (liste blanche lue en base). Adresse DMARC `dmarc@bounce.<domaine>` incluse d'office dans la ligne n° 3. Les étapes manuelles restantes (achat, DNS) sont affichées comme **jalons hors outil** avec leur état, jamais cachées. |

### 2.2 Ajouter une boîte d'envoi

| | |
|---|---|
| **Écran** | Assistant domaine › ④ **et** (manque) Santé › Expéditeurs › ligne du domaine › ⋯ › Ajouter une boîte (**UI-14**) |
| **Étapes** | Prénom, nom de la personne réelle, adresse, signature sans téléphone, case « accord écrit de la personne », identifiants de relève (champ **en écriture seule**), [Tester la connexion], ■ Commencer la montée en douceur |
| **Le système ensuite** | Teste la connexion de relève et d'envoi, inscrit la boîte au registre, la place au palier P1, lance la relève des réponses toutes les 5 min, l'ajoute à l'affectation collante |
| **Manuel en V0** | Créer la boîte chez l'hébergeur de boîtes (connecteur hébergeur prévu en V2, hors périmètre ici). Obtenir l'accord écrit de la personne. |
| **Faisable dès la V0 sans risque** | Le mot de passe de relève est saisi une fois, chiffré en base, **jamais réaffiché** (bouton « Remplacer » seulement), jamais dans le journal. Le test de connexion dit le résultat en clair (« Connexion refusée : mot de passe incorrect »). Une boîte qui échoue 3 fois passe en « Pause technique », visible dans les feux. |

### 2.3 Ajouter une adresse IP d'envoi

| | |
|---|---|
| **Écran** | **AUCUN** dans 07. Proposé : Santé › Expéditeurs › onglet « Adresses IP » › ■ Ajouter une adresse IP (**UI-05**) |
| **Étapes** | Saisir l'IP fournie par l'hébergeur → l'écran affiche le **nom inverse attendu** (PTR) à poser chez l'hébergeur → [Vérifier] (PTR, listes noires, ports) → choisir le client et le groupe (une IP par client en froid) → ■ Mettre en service |
| **Le système ensuite** | Vérifie le PTR et les listes noires, ajoute l'IP à la configuration (UI-15), la place à P1, la surveille toutes les 5 min |
| **Manuel en V0** | Commander l'IP, poser le PTR dans le panneau de l'hébergeur, **configurer l'IP sur la machine** (réseau du système), demander l'ouverture du port 25. |
| **Faisable dès la V0 sans risque** | L'interface ne touche pas au réseau de la machine. Elle **attend** que l'IP réponde (contrôle par la sonde externe) et l'affiche « En attente de la machine » avec la fiche d'intervention en 3 lignes. Refus automatique d'une IP déjà affectée à un autre client (garde « une réputation par IP »). |

### 2.4 Ajouter un serveur d'envoi

| | |
|---|---|
| **Écran** | **AUCUN**. Proposé : Santé › Technique › Serveurs › ■ Ajouter un serveur (**UI-16**, V1) |
| **Étapes** | Installer l'image publique sur la machine (runbook) → la machine **demande à rejoindre** et s'affiche avec son empreinte → l'owner compare l'empreinte et clique [Accepter ce serveur] (code e-mail redemandé) → le serveur tire sa configuration |
| **Le système ensuite** | Arme l'homme mort, le battement, le test de fumée, la sonde anti-relais ; répartit les IP et le plafond par client |
| **Manuel en V0** | **Tout** : V0 = un seul serveur, installé par runbook. |
| **Faisable dès la V0 sans risque** | En V0, l'écran **Serveurs** (UI-04) suffit : il montre le serveur installé à la main et son état. L'enrôlement par empreinte arrive en V1 ; **aucun secret n'est jamais copié de l'interface vers la machine** (c'est la machine qui présente son empreinte). |

### 2.5 Ajouter un client

| | |
|---|---|
| **Écran** | Bascule de client › + Ajouter un client, ou Réglages › Clients (07 § 3.12) |
| **Étapes** | Identité (raison sociale, SIREN, contact RGPD, page d'information) → Premier responsable → Récapitulatif (case « contrat de sous-traitance signé ») → ■ Créer l'espace du client |
| **Le système ensuite** | Crée l'espace, sa configuration par défaut (familles fermées, seuils par défaut, liste d'opposition vide et propre), envoie le lien d'activation ; la « Mise en route » du client démarre |
| **Manuel en V0** | En **instance dédiée** (modèle recommandé par 02 et 05) : créer la machine, la base, les secrets et le domaine du CRM du client (02 M8, **pas d'écran**, commande d'installation). En instance mutualisée : interdit tant que l'étanchéité n'est pas prouvée. |
| **Faisable dès la V0 sans risque** | Séparer les deux gestes : (a) **installer l'instance** reste une commande (V0) ; (b) **créer l'espace et son premier responsable** se fait par l'écran **dans l'instance du client**. L'écran 07 § 3.12 doit le dire (C-15). Pas d'étape « Marque » (C-11). |

### 2.6 Ajouter un utilisateur

| | |
|---|---|
| **Écran** | Réglages › Équipe › ■ Inviter une personne (existe : `UsersPage`, à aligner, **UI-11**) |
| **Étapes** | E-mail, rôle (Propriétaire, Membre, Membre « envois », Lecteur), [Envoyer l'invitation] |
| **Le système ensuite** | Lien d'activation à durée limitée, code par e-mail obligatoire dès la première connexion, accueil selon le rôle (07 § 2.3), ligne au journal |
| **Manuel en V0** | Rien. |
| **Faisable dès la V0** | Déjà presque faisable. Ajouter : « Désactiver » (jamais « Supprimer »), « Renvoyer l'invitation », dernière connexion, et **interdiction pour un admin de nommer un propriétaire** (02 § 1). |

### 2.7 Ajouter un gabarit (message type)

| | |
|---|---|
| **Écran** | Campagnes › Messages types › ■ Nouveau message type (**UI-08** pour la liste) → éditeur 07 § 3.6 |
| **Étapes** | Objet, texte, champs insérés par menu, relecture automatique, [M'envoyer un test], ■ Enregistrer |
| **Le système ensuite** | Version 1 enregistrée, statut « Brouillon » puis « À valider » ; toute campagne qui l'utilise repasse « À valider » si le texte change |
| **Manuel en V0** | Rien. |
| **Faisable dès la V0** | Oui, si la liste UI-08 est faite. |

### 2.8 Ajouter une règle de ralentissement

| | |
|---|---|
| **Écran** | **AUCUN**. Proposé : Réglages › Envois › Règles de prudence (**UI-07**) |
| **Étapes** | Les 7 règles de 03 § 3.2 affichées **en phrases** (« Si plus de **2 %** d'adresses refusées sur 7 jours, redescendre d'un palier ») → [Rendre plus prudent] → valeur nouvelle → motif → code e-mail → ■ Enregistrer la règle |
| **Le système ensuite** | Nouvelle version de `emailing_seuils`, effet à la prochaine évaluation (5 min), ligne au journal, mention « règle modifiée le … par … » dans les tiroirs « Pourquoi » |
| **Manuel en V0** | Les règles par fournisseur (ralentir vers un fournisseur sur réponse « trop de messages ») sont générées dans la configuration du serveur (08 F3) : **lecture seule** en V0. |
| **Faisable dès la V0 sans risque** | **Durcir seulement** en V0 : chaque champ a une borne fixée par la doctrine (rebonds ≤ 2 %, plaintes ≤ 0,1 %, paliers ≤ courbe de 03 § 3.1). Assouplir au-delà est **refusé par le serveur**, pas seulement caché. Ajouter une règle par fournisseur, ou assouplir, passe en V1 avec la validation de l'owner. Les règles par fournisseur sont listées en lecture (« Vers Microsoft : ralentir à 1 message par minute après 3 refus »). |

---

## 3. Vérification des 13 écrans de 07

Critères : **un seul bouton principal** ; **4 états** (vide, chargement, erreur, succès) ; **vocabulaire** sans jargon ni mot banni ; **WCAG 2.2 AA**.

| Écran (07) | Bouton principal unique | Vide | Charg. | Erreur | Succès | Vocabulaire | WCAG 2.2 AA | Correction |
|---|---|---|---|---|---|---|---|---|
| § 3.1 Aujourd'hui | OUI (change en cas d'alerte rouge) | OUI | OUI | OUI | OUI | OUI | Courbe « ▁▂▃ » sans texte équivalent (1.1.1) | C-08 |
| § 3.2 Fiche | OUI | OUI | OUI | OUI | OUI | OUI | Frise d'étapes sans `aria-current` écrit | C-08 |
| § 3.3 Pipeline, Mes tâches | OUI | OUI | OUI | OUI | OUI | **« Pipeline », « Kanban »** : anglicismes | Alternative au glisser-déposer : OUI (2.5.7) | C-09 |
| § 3.4 Listes | OUI | OUI | OUI | OUI (par onglet, trop vague) | OUI | OUI | Barre collante du bas peut masquer le focus (2.4.11) : `scroll-padding-bottom` manquant | C-08 |
| § 3.5 Assistant de campagne | OUI | OUI | OUI | OUI | OUI | OUI | Bouton « désactivé avec raison » : préciser `aria-disabled` + focusable + `aria-describedby` ; récapitulatif collant et focus (2.4.11) | C-07 |
| § 3.6 Éditeur | OUI | OUI | **NON** | OUI | OUI | OUI | Puces de champs dans le texte : nom accessible ; `iframe` d'aperçu sans titre ; ◀ ▶ sans libellé | C-05, C-08 |
| § 3.7 Réponses | OUI (action suggérée) | OUI | OUI | OUI | OUI | « STOP » gardé (mot des gens) | Raccourcis à une lettre désactivables : OUI (2.1.4) ; boutons au pouce : OUI | — |
| § 3.8 Santé des envois | **AMBIGU** : aucun bouton plein en état normal, et 6 onglets sans bouton défini | OUI | OUI (jamais vert par défaut) | OUI (échec fermé) | OUI | « Palier » à expliquer par « ? » | Courbe ASCII sans tableau équivalent ; pulsation du feu : OK | C-01, C-08 |
| § 3.9 Assistant DNS | OUI | OUI | **NON** (pas d'état « vérification en cours ») | OUI (ambre) | OUI | Sigles DNS autorisés ici (P7) | Boutons [Copier] identiques sans nom distinct (2.4.6, 4.1.2) ; relance auto toutes les 2 min ne doit pas déplacer le focus | C-05, C-08 |
| § 3.10 Ne plus écrire | **À revoir** : la question de l'écran est « Puis-je écrire à… ? » (P1), le principal devrait être [Vérifier] | OUI | **NON** | OUI | OUI | OUI | Résultat OUI/NON à annoncer en `aria-live` | C-02, C-05 |
| § 3.11 Statistiques | **AUCUN** bouton principal (seulement [Exporter ▾]) | OUI | **NON** | OUI | **NON** | « Test A/B » : jargon | Tableau équivalent : OUI | C-03, C-09 |
| § 3.12 Clients | OUI | OUI | OUI | OUI | OUI | OUI | Contrôle de contraste de la couleur : OUI | C-11, C-15 |
| § 3.13 Connexion | OUI | sans objet | **NON** (« Envoi du code… ») | OUI | OUI | OUI | 3.3.8 OK ; décompte « 0:42 » à ne pas annoncer chaque seconde | C-04 |

**Problèmes transverses relevés dans 07**
- **Toast « Annuler » de 8 s** (P6 b) : seul moyen d'annuler → échec possible du critère 2.2.1 (temps limité). Il faut un second chemin sans limite de temps (C-06).
- **Mode sombre** : P9 et Q1 laissent la porte ouverte. Will a décidé : **clair seul**. Le code le confirme (`lib/theme.ts`, réglage « Affichage » limité à la densité), mais des classes `dark:` restent dans les composants (C-10).
- **Marque blanche** : Q12 annonce « la marque blanche complète passe en V2 (M4) » et l'assistant client a une étape « Marque » (logo, couleur). **Contraire à la décision de Will** (C-11).
- **« Arrêter tous les envois de Axion-IA ? »** : élision fautive ; le gabarit doit gérer « d'Axion-IA » (C-12).
- **Parcours 1** commence à l'étape 2 (C-13).
- **Santé des envois a 6 onglets**, et il en faudrait 8 avec IP et Vérification : trop pour P1 (C-17).
- **13 écrans annoncés** (10 § 9) alors qu'il en faut au moins **31** pour piloter tout le plan (§ 4).

---

## 4. Écrans MANQUANTS à ajouter

Rangés par entrée de menu. Chaque écran respecte P1 à P12 : phrase d'état, au plus 4 tuiles, **un** bouton principal, 4 états, blocs colorés à sens unique.

| Écran manquant | Place dans le menu | Bouton principal | Réf. |
|---|---|---|---|
| Centre d'alertes | Santé des envois › Alertes (et « Voir toutes les alertes » dans la cloche) | ■ Voir ce qui s'est passé (alerte la plus grave) | UI-01 |
| Réglages des alertes et des avis | Réglages › Mon compte › Alertes | ■ Enregistrer · [M'envoyer une alerte de test] | UI-02 |
| Avis de réponse intéressée | Cloche + e-mail regroupé | (aucun écran propre : réglé dans UI-02) | UI-03 |
| Santé du serveur et test du matin | Santé des envois › Technique › Serveurs | ■ Relancer le test du matin | UI-04 |
| Adresses IP | Santé des envois › Expéditeurs › Adresses IP | ■ Ajouter une adresse IP | UI-05 |
| « M'envoyer un test » (fenêtre de résultat) | Éditeur, assistant ④, Messages types | ■ Envoyer le test | UI-06 |
| Règles de prudence | Réglages › Envois › Règles de prudence | ■ Enregistrer la règle | UI-07 |
| Liste des messages types | Campagnes › Messages types | ■ Nouveau message type | UI-08 |
| État des sauvegardes | Réglages › Technique › Sauvegardes | (aucun bouton plein : lecture) · [Voir le dernier exercice] | UI-09 |
| Journal d'audit | Réglages › Journal | (lecture) · [Exporter le journal] | UI-10 |
| Équipe et rôles | Réglages › Équipe | ■ Inviter une personne | UI-11 |
| Sécurité du compte | Réglages › Mon compte | ■ Régénérer les codes de secours | UI-12 |
| Identité de l'expéditeur et textes légaux | Réglages › Client › Identité | ■ Enregistrer l'identité | UI-13 |
| Ajouter une boîte (hors assistant) | Santé › Expéditeurs › ⋯ | ■ Tester et ajouter | UI-14 |
| Configuration du serveur | Santé › Technique › Configuration | ■ Appliquer la version 8 | UI-15 |
| Ajouter un serveur | Santé › Technique › Serveurs | ■ Accepter ce serveur | UI-16 |
| Rapports DMARC | Santé › Expéditeurs › tiroir du domaine « Qui envoie en votre nom ? » | (lecture) · [Voir les sources inconnues] | UI-17 |
| Expiration des domaines | Colonne « Expire le » + alerte 30 j | — | UI-18 |
| Mise en route détaillée | Aujourd'hui › bloc violet › page « Mise en route » | ■ <jalon suivant> | UI-19 |
| Exports | Réglages › Exports | ■ Préparer l'export | UI-20 |
| Vérification des adresses | Contacts › Listes › colonne « Joignables » › tiroir, et Santé › Technique › Vérification | ■ Vérifier les adresses de la liste | UI-21 |
| Réglages d'envoi | Réglages › Envois › Horaires et pression · Familles | ■ Enregistrer | UI-26 |
| Conformité | Réglages › Conformité | ■ Traiter la demande suivante | UI-27, UI-28 |
| Synchro console | Réglages › Synchro console | ■ Rejouer les envois bloqués | UI-29 |
| Interrupteurs des automatisations | Réglages › Envois › Automatismes | (interrupteurs, pas de bouton plein) | UI-30 |
| Usage et forfait | Réglages › Client › Usage | (lecture) | UI-31 |
| Tous les clients, diagnostic, accès support | Réglages › Clients | ■ Ajouter un client | UI-32 |
| Files d'attente | Santé › Technique › Files | (lecture) · [Retirer…] | UI-39 |
| Sources de mesure | Santé › Technique › Sources | (lecture) | UI-40 |
| Mises à jour | Réglages › Technique › Mises à jour | ■ Mettre à jour (vague suivante) | UI-41 |
| Lettre d'information | Campagnes › Lettre | ■ Nouvelle lettre | UI-38 |

---

## 5. Corrections : texte exact, effort, priorité

Efforts en **jours-agent** pour l'écran **et** sa liaison à l'API (les moteurs eux-mêmes sont déjà comptés dans les lots E0 à E14 de 03 et les lots de 02 ; seul **UI-15** ajoute du travail serveur nouveau, signalé). Les textes ci-dessous sont **à coller dans 07** (ou dans le plan corrigé) tels quels.

### 5.1 Corrections des écrans existants de 07 (C-xx)

| Réf. | Où dans 07 | Texte exact de la correction | Effort | Prio |
|---|---|---|---|---|
| C-01 | § 3.8, après la maquette | « **Bouton principal par onglet.** Vue d'ensemble : aucun bouton plein quand tout est vert ; ■ Voir ce qui s'est passé dès qu'un feu est ambre ou rouge. Expéditeurs : ■ Ajouter un domaine. Montée en douceur : aucun (lecture). Ne plus écrire : ■ Vérifier. Alertes : ■ Voir ce qui s'est passé. Technique : ■ Relancer le test du matin. » | 0,25 | V0 |
| C-02 | § 3.10 | « Le bouton principal est **■ Vérifier** (la question de l'écran). [Ajouter une opposition] devient secondaire. » | 0,1 | V0 |
| C-03 | § 1 P3 et § 3.11 | P3 : « **Au plus un** bouton principal par écran ; un écran de lecture peut n'en avoir aucun. » § 3.11 : ajouter « **Chargement** : tuiles et entonnoir en squelette, la phrase d'état en dernier. **Succès** (export) : toast « Export prêt · Télécharger », lien valable 24 h, ligne au journal. » | 0,2 | V0 |
| C-04 | § 3.13 | « **Chargement** : après « Se connecter », le bouton affiche « Envoi du code… » ; la page du code s'ouvre quand l'e-mail est parti. Le décompte de renvoi n'est annoncé aux lecteurs d'écran qu'à 0 (« Vous pouvez demander un nouveau code »). » | 0,1 | V0 |
| C-05 | § 3.6, 3.9, 3.10 | 3.6 : « **Chargement** : texte et aperçu en squelette ; l'éditeur reste en lecture tant que la version n'est pas chargée. » 3.9 : « **Chargement** : chaque ligne affiche « Vérification… » avec une roue, une ligne à la fois. » 3.10 : « **Chargement** : « Vérification… » sous le champ ; jamais de réponse OUI par défaut. » | 0,2 | V0 |
| C-06 | § 1 P6 (b) | « Le toast « Annuler » reste affiché tant qu'il a le **focus ou le survol**. Tout geste annulable l'est aussi **sans limite de temps** depuis la ligne concernée (« Annuler le classement ») ou depuis le journal de la fiche (WCAG 2.2.1). » | 0,5 | V0 |
| C-07 | § 3.5 ④ et § 4.2 | « Un bouton principal indisponible garde le focus : `aria-disabled="true"`, `aria-describedby` vers la raison (« 2 contrôles à corriger »). Jamais l'attribut `disabled` seul. » | 0,1 | V0 |
| C-08 | § 1 P8 | Ajouter : « Toute courbe ou mini-courbe a un **texte équivalent** (« Hausse de 20 à 120 messages par jour en 21 jours ») et un lien « Voir en tableau ». Les frises ont `aria-current="step"`. Les boutons répétés ont un nom distinct (« Copier la valeur de la ligne 2 »). Les barres collantes en haut **et en bas** sont compensées par `scroll-padding-top` et `scroll-padding-bottom`. Les mises à jour automatiques ne déplacent jamais le focus. » | 0,3 | V0 |
| C-09 | § 2.1, § 3.3, § 3.11 | « Menu « Pipeline » → « **Affaires** » ; onglet « Tableau (Kanban) » → « **Tableau** » ; bloc « Test A/B » → « **Comparaison de versions** ». Ajouter « Pipeline », « Kanban », « A/B », « onboarding » à la garde de vocabulaire. » (À confirmer par Will : il emploie peut-être déjà « pipeline ».) | 0,2 | V0 |
| C-10 | § 1 P9, Q1 | P9 : « **Clair seul, décision de Will.** Pas de mode sombre ni de bascule. » Q1 : « Tranchée : pas de mode sombre. » Garde : « aucune classe `dark:` dans les nouveaux écrans ». | 0,1 | V0 |
| C-11 | § 3.12 étape 2, Q12 | Retirer l'étape « Marque » ; l'assistant passe à **3 étapes** (Identité, Premier responsable, Récapitulatif). Remplacer par : « **Repère de l'espace** : une couleur choisie dans 6 teintes prédéfinies et le nom de l'espace, affichés en liseré et dans les boutons sensibles. Ce n'est pas une personnalisation de l'interface. » Q12 : « Tranchée : pas de marque blanche. » | 0,2 | V0 |
| C-12 | § 3.8, fenêtre « Tout arrêter » | « Titre : « **Tout arrêter · {nom du client}** ? » (évite l'élision « de Axion-IA »). » | 0,05 | V0 |
| C-13 | § 5 Parcours 1 | Renuméroter les étapes à partir de 1. | 0,05 | V0 |
| C-15 | § 3.12 | Ajouter : « **Installation dédiée** : l'instance du client est installée par une commande (02 M8). Cet assistant crée ensuite l'espace et son premier responsable **dans** cette instance. Mutualisé : bouton masqué tant que l'étanchéité n'est pas prouvée (02 I5). » | 0,1 | V0 |
| C-17 | § 2.1 | « Santé des envois, onglets : **Vue d'ensemble · Expéditeurs** (domaines, boîtes, adresses IP) **· Montée en douceur · Ne plus écrire · Alertes · Technique** (serveurs, configuration, files, vérification des adresses, sources de mesure ; propriétaire seulement). » | 0,1 | V0 |
| | | **Sous-total C-xx** | **≈ 2,65** | |

### 5.2 Écrans et fonctions à ajouter (UI-xx)

| Réf. | Texte exact de la correction (à ajouter à 07) | Effort | Prio |
|---|---|---|---|
| UI-01 | « **§ 3.14 Centre d'alertes** (Santé › Alertes). Phrase : « 1 alerte en cours, 0 non lue. » Liste par gravité (■ rouge, ▲ ambre, ○ info) ; chaque ligne : la règle franchie en une phrase, **ce que le système a déjà fait**, la reprise prévue, [Voir ce qui s'est passé]. Alertes regroupées par cause (1 par 15 min). Fermeture automatique quand la cause disparaît, avec la mention « Résolue toute seule à 10:42 ». Vide : bloc vert « Aucune alerte. Dernier contrôle il y a 3 min. » Erreur : « Lecture impossible : par prudence, les envois sont retenus. » » | 2 | V0 |
| UI-02 | « **Réglages › Mon compte › Alertes et avis.** Tableau type × canal : lignes Alerte rouge, Alerte ambre, Réponse intéressée, Réponse en attente > 24 h, Campagne à valider, Sauvegarde, Synchro ; colonnes **Console** et **E-mail**. Pas d'autre canal (ni téléphone, ni messagerie instantanée). Alerte rouge : console + e-mail **toujours actifs** (non décochables). Heure du récapitulatif du matin (08:00 par défaut). Adresse de réception. [M'envoyer une alerte de test] : envoie une alerte fictive par chaque canal coché et affiche « Reçue ? Oui / Non ». » | 1,5 | V0 |
| UI-03 | « **Avis de réponse intéressée** : dès qu'une réponse est classée « Intéressé », pastille dans la cloche et e-mail **regroupé** (au plus un toutes les 15 min) : « 2 réponses intéressées vous attendent » + lien vers Réponses. **Aucun nom ni adresse dans l'objet ou le corps.** » | 1 | V0 |
| UI-04 | « **§ 3.15 Technique › Serveurs.** Phrase : « Serveur d'envoi sain. Dernier envoi 11:42. Test du matin réussi. » Une carte par machine : état (feu + mot), service d'envoi, liaison privée, disque, mémoire, file (nombre, âge du plus ancien), plafond restant du jour **par client**, version de configuration et empreinte, battement de l'homme mort. Bloc « Test du matin (06:45) » : arrivé en boîte de réception chez chaque boîte témoin, autorisation / signature / politique : réussies. Le logiciel du serveur n'est jamais nommé. ■ Relancer le test du matin. Vide : « Aucun serveur d'envoi. » + lien vers le guide d'installation. Erreur : feu gris « État inconnu, envois retenus par prudence ». » | 2 | V0 |
| UI-05 | « **Expéditeurs › Adresses IP.** Colonnes : Adresse, Client, Nom inverse (PTR) ✓/✗, Listes noires, Palier, Aujourd'hui / plafond, État. ■ Ajouter une adresse IP : ① adresse → ② nom inverse attendu [Copier] → ③ [Vérifier] → ④ client (une IP n'appartient qu'à un client) → ■ Mettre en service. Une IP qui ne répond pas encore reste « En attente de la machine ». » | 2 | V0 |
| UI-06 | « **M'envoyer un test.** Fenêtre : destinataires cochés par défaut = moi + boîtes témoins ; destinataire d'exemple (pour les champs) ; [Envoyer le test]. Le test passe par la même porte qu'un vrai envoi, **ne compte pas dans la montée en douceur** et est marqué « TEST » dans le journal. Résultat en 2 min : « Reçu en boîte de réception (3/4), en indésirables (1/4 : Outlook). Signature : réussie. » » | 1 | V0 |
| UI-07 | « **§ 3.16 Réglages › Envois › Règles de prudence.** Les règles en phrases, valeur en gras, modifiables seulement **vers plus de prudence** en V0 (bornes : refusées ≤ 2 %, plaintes ≤ 0,1 %, paliers ≤ courbe de référence). Chaque modification : motif obligatoire, code e-mail, nouvelle version, journal. Onglet « Courbe » : les 13 paliers en tableau, abaissables. Bloc « Vers chaque fournisseur » : règles de ralentissement générées, en lecture seule (modifiables en V1 par l'owner). ■ Enregistrer la règle. Erreur : « Valeur refusée : plus souple que la règle de base (2 %). » » | 2,5 | V0 |
| UI-08 | « **Campagnes › Messages types.** Colonnes : Nom, Version, Statut (Brouillon / À valider / Validé / Archivé), Utilisé par, Modifié le. Actions de ligne : Ouvrir, Dupliquer, Archiver (jamais Supprimer sauf brouillon jamais envoyé). ■ Nouveau message type. Vide : « Pas encore de message type. Écrivez-en un, il servira à toutes vos campagnes. » » | 1 | V0 |
| UI-09 | « **Réglages › Technique › Sauvegardes.** Phrase : « Dernière sauvegarde cette nuit à 03:00. Copie hors site : faite. » Tuiles : Dernière sauvegarde, Copie hors site, Place utilisée / plafond (9 Go), Dernier exercice de restauration (date, durée, résultat). Par client en mode multi-client. **Aucun bouton « Restaurer »** : la restauration suit le guide écrit, avec deux personnes. Alerte ambre si la copie a plus de 26 h, rouge à 48 h. » | 1,5 | V0 |
| UI-10 | « **Réglages › Journal.** Reprend `AuditLogsPage` existante dans la coquille 2027. Filtres en puces : Qui, Quoi (Envois, Campagnes, Oppositions, Accès, Lectures, Réglages), Client, Période. Les gestes de pilotage (Tout arrêter, Reprendre, règle modifiée, réautorisation) sont en tête. Aucune adresse en clair. [Exporter le journal] (code e-mail). » | 1 | V0 |
| UI-11 | « **Réglages › Équipe.** Colonnes : Personne, Rôle, Dernière connexion, Code par e-mail (actif), État. ■ Inviter une personne (e-mail + rôle). Actions : Changer le rôle, Renvoyer l'invitation, **Désactiver** (jamais Supprimer). Un administrateur ne peut pas nommer un propriétaire (refus serveur). Aide « ? » par rôle : 1 phrase. » | 1,5 | V0 |
| UI-12 | « **Réglages › Mon compte › Sécurité.** Codes de secours : « 7 restants » + ■ Régénérer les codes (code e-mail). Appareils de confiance : liste (appareil, ville approximative, dernière utilisation) + [Ne plus faire confiance]. » | 1 | V0 |
| UI-13 | « **Réglages › Client › Identité.** Raison sociale, forme, SIREN, adresse, contact RGPD, page « prospection », durée de conservation annoncée ; **texte du bloc d'information** (avec aperçu tel qu'il partira) et **pied de message**. Bloquant : aucune campagne vers un non-informé tant que ces champs sont vides (l'assistant ④ affiche « Identité incomplète [Compléter] »). ■ Enregistrer l'identité. » | 1 | V0 |
| UI-14 | « **Ajouter une boîte** (depuis la ligne d'un domaine). Prénom, nom, adresse, signature sans téléphone, case « accord écrit de la personne », identifiants de relève **en écriture seule** (jamais réaffichés, bouton « Remplacer »). [Tester la connexion] → ■ Commencer la montée en douceur. 3 échecs de relève → « Pause technique » visible dans les feux. » | 1,5 | V0 |
| UI-15 | « **Technique › Configuration.** Phrase : « Configuration v8 prête : 1 domaine ajouté. » Différences en clair (« + domaine <domaine-3> », « + adresse IP … »). ■ Appliquer la version 8 (propriétaire, code e-mail) : le serveur **tire** la version par la liaison privée, la valide à blanc, l'applique, le test de fumée confirme ; échec → retour automatique à v7 et alerte. Aucune clé ni secret affiché. » **Travail serveur nouveau** (passage de V1 à V0 de « configuration depuis la base ») : 4 j + écran 1 j. | 5 | V0 |
| UI-16 | « **Ajouter un serveur** : la machine installée demande à rejoindre ; l'écran montre son empreinte ; l'owner la compare au guide et clique ■ Accepter ce serveur (code e-mail). Rien n'est copié de l'interface vers la machine. » | 3 | V1 |
| UI-17 | « **Tiroir « Qui envoie en votre nom ? »** (par domaine) : depuis les rapports DMARC reçus, sources autorisées (vert) et **sources inconnues** (ambre, « 12 messages depuis une adresse inconnue »), taux de signature réussie. Préalable : politique `p=none` avec adresse de rapports dès la création du domaine. » Ingestion 2 j (11 n° 7) + écran 1 j. | 3 | V0 (conseillé par 11) |
| UI-18 | « **Colonne « Expire le »** dans Expéditeurs (domaines et certificats de `go.` et `mta-sts.`), ambre à 30 j, rouge à 7 j, alerte dans le centre d'alertes et par e-mail. » | 1 | V1 |
| UI-19 | « **Mise en route** (page dédiée, ouverte depuis le bloc violet) : 5 jalons, chacun avec son état, son temps (« ≈ 5 min » ou « attente : 12 jours »), son bouton, et les **actions hors outil** listées comme cases (acheter les domaines, poser le DNS, créer les boîtes chez l'hébergeur) que l'utilisateur coche lui-même. ■ = jalon suivant. » | 1 | V0 |
| UI-20 | « **Réglages › Exports.** Liste des exports faits (qui, quoi, quand, nombre de lignes). ■ Préparer l'export : choix (sélection, liste, résultats de campagne, **espace complet** pour la réversibilité). Code e-mail + motif ; lien valable 24 h ; journal. L'export complet est réservé au propriétaire. » | 2 | V1 (sélection : V0, existe) |
| UI-21 | « **Vérification des adresses.** Dans Listes, le tiroir de la colonne « Joignables » détaille : vérifiées < 30 j, à revérifier, invalides, inconnues. ■ Vérifier les adresses de la liste : estimation du coût affichée **à titre d'information** (« ≈ 1,20 € ») puis lancement. Technique › Vérification : crédits restants du prestataire, coût du mois, dernière erreur. » | 1,5 | V0 |
| UI-23 | « **Assistant ② Message** : [+ Ajouter une version de l'objet] (2 à 4). L'écran dit : « Gagnante choisie sur les **réponses positives**, après 300 envois par version. » Résultat dans le suivi de campagne, onglet « Comparaison ». » | 1 | V1 |
| UI-24 | « **Campagnes › Presse** (maquette de 03 § 7.4 passée au système 2027) : phrase d'état, colonnes Média, Rubrique, Angle, Provenance (✓ fiable / ▲ à revoir), Statut, Mise à jour ; ■ Nouveau communiqué ; validation **message par message** ; communiqué par lien seulement. » | 1,5 | V1 |
| UI-25 | « **Assistant ① Cible** : [Exclure une adresse, une organisation ou un domaine] (champ unique, empreinte). **⑤ Lancement** : « Liste figée le 18/01 à 07:10 : 312 personnes » + [Voir la liste figée]. » | 0,5 | V1 |
| UI-26 | « **Réglages › Envois › Horaires et pression** : fenêtre d'envoi par défaut (09:00-17:00, jours ouvrés, fériés exclus), pression commerciale en phrases (« Au plus 1 message tous les 5 jours ouvrés par personne »), durcissable seulement. **Familles** : liste des familles avec cadenas ; [Ouvrir cette famille] réservé au propriétaire, motif + code e-mail, trace au journal. » | 1,5 | V0 |
| UI-27 | « **Réglages › Conformité** : registre des traitements, sous-traitants (avec contrat oui/non), analyses d'intérêt légitime, versions des textes d'information (date, campagnes concernées). Règles automatiques d'étiquettes maquettées dans Contacts › Étiquettes avec le même gabarit. » | 1,5 | V1 |
| UI-28 | « **Réglages › Conformité › Demandes** : la page existante `/rgpd/requests` dans la coquille 2027, délai restant en tête (« à traiter avant le 14/02 »), ■ Traiter la demande suivante. » | 0,5 | V0 |
| UI-29 | « **Réglages › Synchro console** : en attente, abandonnés, dernier passage, ■ Rejouer les envois bloqués. » | 1 | V1 |
| UI-30 | « **Réglages › Envois › Automatismes** : un interrupteur par automatisme (relève des boîtes, construction des vagues, vérification planifiée, rapports), avec l'état et l'heure du dernier passage. Couper un automatisme affiche un bandeau ambre sur les pages concernées. » (Simple liste d'interrupteurs, **pas** de constructeur d'automatisations.) | 1 | V0 |
| UI-31 | « **Réglages › Client › Usage** : envois, vérifications, IA, utilisateurs du mois, plafond **informatif** (ambre au-delà, rien ne se bloque), remise à zéro le <date anniversaire>. » | 1,5 | V1 |
| UI-32 | « **Réglages › Clients** (opérateur) : tableau Client, Version, Santé, Alertes, Usage ; tiroir **Diagnostic** (version, drapeaux, files, dernières erreurs) ; [Demander un accès support] → durée (1 h à 8 h) + motif, accordé par le propriétaire du client, bandeau violet, journal consultable par le client. » | 3 | V1 |
| UI-33 | « **Fiche › [Écrire un message]** : message unique à une personne, même éditeur, même porte (opposition, pression, bloc d'information), tracé dans la chronologie. » | 1 | V1 |
| UI-34 | « **Fiche › ⋯ › Déclarer un envoi fait à la main** : date, objet, boîte ; compte dans la pression et dans l'information art. 14. » | 1 | V1 |
| UI-35 | « **Réglages › Client › Champs** : ajouter un champ (texte, liste, date), utilisable en ciblage et comme champ de message (avec valeur de repli). » | 1,5 | V1 |
| UI-36 | « **Vues sauvegardées** : dans chaque tableau, [Enregistrer cette vue] et liste déroulante des vues. » | 0,5 | V1 |
| UI-37 | « **Campagnes › Messages déclenchés** : formulaire en une phrase « **Quand** [événement ▾ : formulaire du site, RDV annulé, inscription Tour France IA] **envoyer** [message type ▾] **après** [délai] ». Liste des règles avec interrupteur. Chaque règle passe par la validation de l'owner. **Pas de schéma ni de constructeur visuel.** » | 1,5 | V1 |
| UI-38 | « **Campagnes › Lettre** : abonnés consentants (séparés de la prospection), journal de consentement, formulaire d'inscription intégrable à double confirmation, pages « merci / confirmez / désinscrit » au nom de l'expéditeur ; envois récurrents. V2 : centre de préférences, version web sans suivi, éditeur par blocs. » | 3 (V1) + 2 (V2) | V1 / V2 |
| UI-39 | « **Technique › Files** : messages en attente par client, fournisseur, campagne, âge ; [Retirer…] avec motif. » | 1,5 | V1 |
| UI-40 | « **Technique › Sources** : chaque source de mesure (serveur, rapports DMARC, Postmaster, SNDS, vérificateur, listes noires) avec état et âge. » | 1 | V1 |
| UI-41 | « **Réglages › Technique › Mises à jour** : version actuelle, version disponible, notes en 3 lignes, vagues (Axion, pilote, tous), ■ Mettre à jour (vague suivante), retour arrière. » | 1 | V1 |
| UI-42 | « **Réglages › Technique › Accès API** : clés par espace (nom, droits, dernière utilisation), [Créer une clé] affichée **une seule fois**, [Révoquer]. V2 : **Webhooks sortants** (adresse, événements, signature, rejeu). » | 1,5 (V1) + 1 (V2) | V1 / V2 |
| UI-43 | « **Statistiques › Rapports** : rapports du matin, hebdomadaires et mensuels **figés et archivés**, [Télécharger (PDF)] ; rapport de campagne exportable pour un client. » | 1,5 | V1 |
| UI-44 | « **Réglages › Envois › Tâches automatiques** : liste en phrases (« Si pas de réponse 3 jours après le dernier message, créer une tâche « Appeler » »), interrupteur par règle ; **Règles de passage** entre campagnes au même format (« Quand une campagne se termine sans réponse, proposer la campagne X »). Pas de constructeur visuel. » | 1 | V1 |
| UI-45 | « **Frein** : quand plus de 20 réponses attendent depuis plus de 24 h, Aujourd'hui affiche un bloc terracotta « Les nouveaux premiers messages sont ralentis tant que les réponses attendent » et la construction des vagues ne programme que les relances. » | 0,5 | V0 |
| UI-46 | « **Aide** : une page courte par entrée de menu (1 écran, 5 questions), ouverte par « ? » au même endroit sur chaque page ; aide des raccourcis par la touche « ? ». » | 1 | V1 |
| UI-50 | « **Tiroir « Listes noires »** : par IP et par domaine, chaque liste avec ✓/✗ et heure du contrôle ; [Revérifier maintenant] ; si listé, le guide de sortie en 3 étapes. » | 0,5 | V0 |
| UI-52 | « **Éditeur › [Proposer une variante]** (IA, fournisseur UE ou sous contrat) : la variante s'affiche à côté, **jamais envoyée sans validation**, aucun fait inventé. » | 1 | V2 |
| UI-55 | « **Ajout rapide** (palette ou bouton « + » de Contacts) : un écran, dédoublonnage pendant la saisie, provenance obligatoire. **Fiche › ⋯** : Modifier · Mettre en corbeille (restaurable). » | 1 | V0 |
| UI-56 | « **Responsable** d'une fiche affiché dans l'en-tête, [Changer] ; filtre « Moi » partout. » | 0,5 | V1 |
| UI-57 | « **Import planifié** : dans l'assistant d'import, [Répéter chaque semaine depuis cette adresse]. » | 1 | V2 |
| UI-58 | « **§ 3.5 bis Liste et suivi des campagnes.** Liste : colonnes Campagne, Nature, Statut (7 badges), Étape, Joignables, Envoyés, Réponses (dont positives), Désinscriptions, Fin prévue ; filtres en puces. Suivi : frise des étapes avec nombres, 5 tuiles, « exclus du jour par motif » et « journal des décisions » repliés ; boutons [Mettre en pause] (secondaire) / ■ Reprendre (si en pause) / ⋯ Annuler la campagne (motif). États : vide (bloc violet existant), chargement (squelette de tableau), erreur (« Lecture impossible »), succès (toast « Campagne en pause. Rien ne partira. Annuler »). » | 1,5 | V0 |
| UI-59 | « **Champ « Lien de rendez-vous »** dans « Insérer un champ ▾ » ; l'adresse se règle dans Réglages › Client › Identité ; le lien porte la campagne pour l'attribution. » | 0,5 | V0 |
| UI-60 | « **Réponses › Répondre** : composeur sous le fil, signature de la boîte, envoi par la même boîte et la même porte, ■ Envoyer la réponse. » | 1 | V1 |
| UI-61 | « **Réponses › À rattacher** : la réponse et 3 fiches proposées ; ■ Rattacher à <fiche> ; [Créer la personne]. » | 0,5 | V0 |
| UI-62 | « **Page publique de désinscription** (`go.<domaine>`) : une phrase « Vous ne recevrez plus de messages de <Entité>. », case facultative « Pour toute mon organisation », lien « Pourquoi ai-je reçu ce message ? ». Clair, sans suivi, AA, téléphone d'abord. » | 1 | V0 |
| UI-63 | « **Aujourd'hui › bloc gris « À recontacter »** : personnes écrites il y a plus de N mois, sans réponse, toujours joignables. » | 0,5 | V2 |

### 5.3 Totaux

| Priorité | Corrections | Jours-agent |
|---|---|---|
| **V0** | C-01 à C-17 + UI-01 à 15, 17, 19, 21, 26, 28, 30, 45, 50, 55, 58, 59, 61, 62 | **≈ 42** (dont 4 j de travail serveur nouveau pour UI-15) |
| **V1** | UI-16, 18, 20, 23 à 25, 27, 29, 31 à 44 (parts V1), 46, 56, 60 | **≈ 34,5** |
| **V2** | UI-38 (part V2), 42 (webhooks), 52, 57, 63 | **≈ 5,5** |
| **Total** | 71 corrections (15 C + 56 UI) | **≈ 82** (+ 15 % de relecture ≈ 94) |

Attention au **double compte** dans le plan corrigé : une partie de ces écrans est déjà incluse dans le lot E12 « Console V0 » de 03 (≈ Accueil, Campagnes, Modèles, Réponses, Délivrabilité, Oppositions, Alertes, Santé serveur) et dans les lots 2 à 5 de 02. Le consolidateur doit retirer de E12 ce qui est chiffré ici (estimation : 12 à 15 j de recouvrement).

---

## 6. Points à faire trancher par Will (courts, avec recommandation)

| # | Question | Recommandation |
|---|---|---|
| W1 | « Pipeline » devient « Affaires » dans le menu ? | **Oui**, sauf s'il tient au mot. |
| W2 | Configuration du serveur appliquée depuis l'interface **dès la V0** (UI-15, +4 j) ? | **Oui** : sinon chaque domaine, boîte ou IP ajouté demande une intervention technique. |
| W3 | Règles de prudence : **durcir seulement** en V0, assouplir en V1 avec validation ? | **Oui.** |
| W4 | Rapports DMARC en V0 (11 n° 7) ? | **Oui**, la politique `p=none` avec rapports doit exister dès la création des domaines. |
| W5 | Assistant client sans étape « Marque », remplacée par un **repère couleur** de l'espace ? | **Oui** (cohérent avec « pas de marque blanche »). |
| W6 | Avis par e-mail regroupé pour chaque réponse intéressée ? | **Oui**, sans nom dans l'e-mail. |

---

## Résumé (20 lignes)

1. Lecture : 07 en entier ; 02, 03, 08, 10, 11 par recherche ; code `axion-crm-pro` (routes, pages Utilisateurs, Réglages, Journal). Rien n'a été codé ni envoyé.
2. Matrice : **128 fonctions** → **51 pilotées (40 %)**, **36 partielles (28 %)**, **41 sans écran (32 %)**.
3. Verdict : **l'UI de 07 ne couvre pas 100 % des fonctions**. Le quotidien est bien couvert ; l'exploitation de l'envoi et l'administration ne le sont pas.
4. Trous majeurs V0 : centre d'alertes, réglages d'alertes (console + e-mail seulement), serveurs et test du matin, adresses IP, règles de prudence, sauvegardes, journal, équipe, identité légale.
5. Trou bloquant « sans coder » : la configuration du serveur d'envoi n'est appliquée depuis la base qu'en V1 → en V0, chaque domaine, boîte ou IP demande une intervention à la main.
6. Proposition : UI-15 en V0, « l'interface décrit, le serveur tire », validation à blanc, retour arrière automatique, aucun secret affiché (+5 j).
7. Parcours « ajouter sans coder » : domaine, boîte, gabarit, utilisateur, règle (durcir seulement) faisables en V0 avec les corrections ; IP en partie ; serveur et installation d'un client restent des commandes en V0.
8. Campagnes (le cœur) : assistant excellent, mais il manque la liste et le suivi maquettés, la liste des messages types, la création des versions à comparer, la presse, les exclusions manuelles et le lien de RDV.
9. « M'envoyer un test » existe comme bouton mais sans destinataires ni résultat : spécifié (UI-06).
10. Avis immédiat de réponse intéressée : absent, ajouté (console + e-mail regroupé, sans donnée personnelle).
11. Rapports DMARC et expiration des domaines : absents, ajoutés (V0 et V1).
12. 13 écrans vérifiés : 4 sans état « chargement », Statistiques sans bouton principal, Santé et Ne plus écrire au bouton principal ambigu.
13. WCAG 2.2 AA : toast de 8 s seul moyen d'annuler (2.2.1), courbes sans texte équivalent, boutons [Copier] sans nom distinct, focus sous les barres collantes, bouton désactivé muet.
14. Vocabulaire : « Pipeline », « Kanban », « Test A/B » à remplacer ; aucun mot banni trouvé à l'écran.
15. Contradictions avec Will : Q1 laisse le mode sombre ouvert, Q12 et l'étape « Marque » annoncent la marque blanche : corrigées (C-10, C-11).
16. Rien de proposé hors périmètre : pas de constructeur visuel (règles « Quand… alors… » en phrases), pas de systeme.io, pas de MCP, pas d'agenda ni de modèles clients, pas de téléphone.
17. 71 corrections avec texte exact : **V0 ≈ 42 j**, **V1 ≈ 34,5 j**, **V2 ≈ 5,5 j**, total ≈ 82 j-agent (≈ 94 avec relecture).
18. Double compte probable avec le lot E12 de 03 (12 à 15 j) : à retirer lors de la consolidation.
19. 6 questions courtes pour Will (W1 à W6), chacune avec recommandation.
20. Prochaine étape : intégrer ces corrections dans le plan corrigé unique avec les fichiers 13 à 17, puis test de 45 min sur maquettes cliquables.
