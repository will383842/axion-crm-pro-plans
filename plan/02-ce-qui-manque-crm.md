# 02 — Ce qui manque au CRM Pro pour être complet (30/10/2026)

Responsable : complétude fonctionnelle. Lecture seule : aucun code modifié, aucun accès au serveur, aucun e-mail.
Code lu : `C:\Users\willi\Documents\Projets\Axion-CRM-Pro` au commit `1f7b0caa` (29/10). Les chemins de code ci-dessous partent de ce dépôt.
Sources : `_AUDIT-CRM-PRO-ENVOI-MASSE-2026-10-30\` (zones 1, 2, 3, 5, 6, 7 et CRITIQUE-COMPLETUDE), `_AUDIT-SOS-EXPAT-REPRISE-2026-10-30\` (B, C, E, I), les pages de la sauvegarde backlink-engine (`VS_CODE\Sauvegardes\Sauv_backlink_engine\2026-10-17_03-00-02\code\frontend\src\pages\`), le cahier d'envoi `_PLAN-ENVOI-EMAILING-CRM-PRO-2026-09-28\04-final\` (§7, écrans E0 à E27), la mémoire (synchro console, dossier client, accès CRM).
Rien n'a été vérifié en production : tout état qui dépend d'un drapeau du serveur reste NON VÉRIFIÉ.

## Cadre fixé par Will (repris tel quel dans chaque ligne)

- **Complet, pas de version réduite.** « Démarrer petit » ne vaut que pour les **volumes d'envoi** (quelques centaines par jour, puis montée selon rebonds et plaintes). Toutes les fonctions sont listées et classées P0/P1/P2.
- Le CRM Pro sera aussi **déployé chez des clients** : domaine (m) ajouté.
- Les **campagnes d'e-mails sont centrales** : domaine (e) détaillé fonction par fonction.
- Aucune suppression de données clients, aucune purge, conservation illimitée ; corbeille douce seulement ; doublons = seule exception (fusion réversible).
- Opposition et liste de suppression partout ; information art. 14 ; cible TPE/PME ; segments presse et santé **fermés par défaut**.
- Jamais de validation manuelle de prix : un coût ou un montant **informe**, il ne bloque pas et ne demande pas de clic de validation.
- Synchro console ⇄ CRM **automatique dans les deux sens**, le plus récent gagne, ancienne valeur gardée à l'historique, aucune suppression propagée, jamais de montant en V1, jamais le texte des réponses du questionnaire, l'opposition gagne partout.
- 2FA **par e-mail** (code reçu par courriel), pas par application.
- Plus aucune notification push : les alertes passent par e-mail et par la console.
- Le dossier client après rendez-vous vit **dans la console du site** : le CRM ne le refait pas, il s'y relie.
- Contenu : jamais « Qualiopi » ni « certifié », jamais « Grenoble » (« partout en France »), jamais « Aucun gain garanti », jamais « faites-le vous-même », logos et avis clients éteints.

**Hors périmètre** (autre agent) : le **moteur d'envoi** lui-même (KumoMTA, serveurs M3/M4, domaines, DNS, chauffe, injection, désinscription en un clic côté message, relève des rebonds). Ici on liste ce que le CRM doit offrir **autour** : ciblage, contenu, validation, planification, réponses, statistiques. Les lignes qui en dépendent portent la dépendance « MOTEUR ».

**Légende.** État : EXISTE / PARTIEL / MANQUE. Effort en jours-agent : **S** ≤ 1 j, **M** 2 à 3 j, **L** 4 à 8 j (chiffre exact entre parenthèses). Priorité : **P0** = avant le premier envoi ou le premier client, **P1** = nécessaire pour un CRM complet au quotidien, **P2** = confort, échelle ou équipe.

---

## (a) Fiches et contacts

| # | Fonction | État | Preuve | Effort | Prio | Dépendances |
|---|---|---|---|---|---|---|
| A1 | Fiches entreprise : liste filtrée, détail, création, édition, corbeille douce, enrichissement, score | EXISTE | `backend/routes/api.php:167-205` ; `frontend/src/features/companies/` | — | — | — |
| A2 | Personnes : hub, fiche, chronologie, rattachement à une entreprise | EXISTE (lecture) | `api.php:521-560` ; `features/crm-console/PersonneDetailPage.tsx` | — | — | — |
| A3 | Modifier et retirer un contact (`PUT`/`DELETE /contacts/{id}`) en corbeille douce, avec journal et fiches protégées | PARTIEL : répond 501 | `ContactsController.php:174,192` | M (1,5) | P0 | `FichesProtegees`, liste de suppression |
| A4 | Ajout rapide d'une personne ou d'une entreprise en un écran, dédoublonnage pendant la saisie, provenance obligatoire (source réelle pour l'art. 14) | MANQUE : pas de création de personne/contact, seulement `POST /companies` et `/journalists` | `api.php:185,287` ; modèle : `QuickAdd.tsx` (backlink) | S (1) | P1 | A3, doublons |
| A5 | Notes libres, appels et rencontres sur une fiche entreprise ou personne | PARTIEL : activité `note` seulement pour médias et journalistes | `api.php:272,307` ; entreprises : tâches seulement (`CompanyTachesController.php`) | M (2) | P1 | — |
| A6 | Chronologie unifiée : e-mails envoyés et reçus, réponses, RDV, notes, étapes, oppositions, synchro | PARTIEL : chronologie sans e-mails ni réponses | `PersonTimelineController.php`, `EnrichmentTimeline.tsx` | M (2) | P1 | MOTEUR, (f) |
| A7 | Badges d'envoi sur la fiche : qualité de l'adresse, « informée le … », dernier message, en séquence, opposition | MANQUE (écran E27 du cahier, classé V2 à tort) | `CAHIER…md:4963` | M (1,5) | P1 | MOTEUR, J5 |
| A8 | Doublons : détection, fusion réversible, ignorer | EXISTE | `api.php:242-248` ; `app/Crm/Doublons/` | — | — | — |
| A9 | Recherche globale | EXISTE | `api.php:428` ; `tests/e2e/global-search.spec.ts` | — | — | — |
| A10 | Fonction et rôle de la personne normalisés (dirigeant, RH, DAF…), utilisables en ciblage | PARTIEL (métiers des audiences, non vérifié pour les personnes INSEE) | `features/audiences/metiers.ts` | M (2) | P1 | E2 |
| A11 | Personne « partie de l'entreprise » ou « remplacée par » : marquer, proposer la nouvelle personne, garder l'ancienne | MANQUE | cycle « fin de vie », CRITIQUE M1 | S (1) | P1 | F5 |
| A12 | Champs personnalisés par espace (texte, liste, date) | MANQUE (seul `signals` JSONB) | migration `2026_05_16_000003` | M (3) | P2 | M3 (config par client) |
| A13 | Propriétaire de fiche (portefeuille) et réaffectation | MANQUE (0 occurrence `owner_id`) | recherche dans `backend/app` | S (1) | P2 | I8 |

## (b) Import et export

| # | Fonction | État | Preuve | Effort | Prio | Dépendances |
|---|---|---|---|---|---|---|
| B1 | Exports CSV journalisés (entreprises, médias, journalistes, personnes), droit `data.export` | EXISTE | `api.php:169,264,281,548` ; `ExportPermissionTest.php` | — | — | — |
| B2 | Imports de référentiels (INSEE, FINESS, RPPS, presse, fédérations, événements) | EXISTE en ligne de commande seulement | `app/Console/Commands/Crm*Import*.php` | — | — | — |
| B3 | Import d'une liste par rapprochement (ne crée aucune fiche) | EXISTE | `app/Crm/Listes/ImportListe.php` (5 Mo, 20 000 lignes) | — | — | — |
| B4 | **Import de fichier par l'interface** : CSV/XLSX, correspondance des colonnes, aperçu, dédoublonnage, création ou mise à jour, provenance et date de collecte (art. 14), rapport ligne à ligne, annulation du lot en corbeille (jamais de purge) | MANQUE | Z3 M5 ; modèle : `BulkImport.tsx` (backlink), import CSV de partner-engine (rapport C) | L (4) | P1 | A4, J6 |
| B5 | Export de la sélection, d'une liste, d'une audience ou des résultats d'une campagne | PARTIEL (audiences : destinataires en API) | `api.php:398` ; Z3 m3 | S (1) | P1 | C5 |
| B6 | Déclarer des « envois faits à la main » (messages partis de la boîte de Will) pour tenir l'art. 14 et la pression | MANQUE (écran E25) | `CAHIER…md:4961` | M (2) | P1 | J5 |
| B7 | Export complet et réversibilité d'un espace client (toutes ses données, format ouvert) | PARTIEL (portabilité RGPD par personne seulement) | `GdprPortabilityService.php` | M (2) | P0 client | M1 |
| B8 | Import planifié depuis un fichier ou une URL (mise à jour régulière d'une source) | MANQUE | — | M (2) | P2 | B4 |

## (c) Listes, segments, étiquettes

| # | Fonction | État | Preuve | Effort | Prio | Dépendances |
|---|---|---|---|---|---|---|
| C1 | Étiquettes : CRUD, pose en masse, règles automatiques, référentiel gouverné | EXISTE | `api.php:354-368` | — | — | — |
| C2 | Listes manuelles (corbeille, restauration, membres) | EXISTE | `api.php:406-426` | — | — | — |
| C3 | Audiences dynamiques (constructeur, aperçu, destinataires) | EXISTE | `api.php:384-401` ; `features/audiences/` | — | — | — |
| C4 | Écran des vues sauvegardées (filtres réutilisables) | PARTIEL : API sans écran, routes déclarées trois fois | `api.php:373-381` | S (1) | P1 | — |
| C8 | Liste figée au départ d'une campagne (instantané : qui, quel texte, quand) | MANQUE | Z1 manque 11 | M (2) | P0 | E8 |
| C9 | Critères d'exclusion : « contacté depuis N jours », « déjà ciblé par la campagne X », « démarche en cours », « client », « RDV pris » | MANQUE (REQ-CAM-077 à 083) | `CAHIER…md:4938` | M (2) | P0 | A6 |
| C10 | Mesure du volume réellement envoyable par segment (adresse valide, hors exclusions), affichée dans le ciblage | MANQUE | Z1 M7 ; CRITIQUE B4 | S (1) | P0 | joignabilité planifiée (L8) |

## (d) Pipeline, Kanban, tâches et rappels

| # | Fonction | État | Preuve | Effort | Prio | Dépendances |
|---|---|---|---|---|---|---|
| D1 | Étape de relation (nouveau, qualifié, opportunité, client, dormant, perdu), jamais de recul automatique | EXISTE (un champ) | `Taxonomy.php:239-246` ; `RelationCard.tsx` | — | — | — |
| D2 | **Kanban** par étape (glisser-déposer, filtres, compteurs) | MANQUE (0 occurrence) | Z3 M3 | M (3) | P1 | D1 |
| D3 | Opportunité : montant **informatif**, probabilité, date de clôture prévue, raison de perte ; jamais de validation de prix, jamais synchronisé vers la console en V1 | MANQUE | Z3 §3 point 1 | M (2) | P1 | D2 |
| D4 | Tâches par fiche avec échéance | EXISTE | `CompanyTachesController.php:53-69` (`due_at`) ; `TachesCrmCard.tsx` | — | — | — |
| D5 | **Vue « Mes tâches »** : aujourd'hui, en retard, à venir, terminer, reporter | MANQUE (aucune route) | `routeTree.tsx` ; Z3 M3 | M (2) | P1 | D4 |
| D6 | Rappels : récapitulatif du matin **par e-mail** (pas de push) + pastille console | MANQUE | `AFaire.tsx` ne compte pas les tâches | S (1) | P1 | L3 (mailer) |
| D7 | Tâches automatiques : relancer sans réponse à J+x, RDV non honoré, après RDV, réponse « intéressé » non traitée | MANQUE | modèle : rappels Mission_control (rapport D) | M (2) | P1 | (f), (g) |
| D8 | Suggestions de recontact (« écrit il y a plus de N mois, pas de réponse, toujours éligible ») | MANQUE | modèle : `RecontactSuggestions.tsx` (backlink) | S (1) | P2 | C9 |
| D9 | Assignation des tâches et des fiches à un membre de l'équipe | MANQUE | Z3 m3 | S (1) | P2 | A13 |

## (e) Campagnes d'e-mails, séquences et relances (fonctions côté CRM)

Le CRM n'a aujourd'hui **aucune** campagne d'envoi : `/cold-email` répond 501 (`api.php:608-609`), pas de dossier `app/Emailing`. Les « campagnes » existantes sont des campagnes de **collecte** (`api.php:476-500`). Le CRM sait seulement produire un fichier de destinataires éligibles (`CrmCampagneDestinataires.php`) et importer des retours (`CrmCampagneRetours.php`). Tout ce qui suit est donc MANQUE, sauf mention.

| # | Fonction | État | Preuve / modèle | Effort | Prio | Dépendances |
|---|---|---|---|---|---|---|
| E1 | Objet campagne : objectif, statut (brouillon, à valider, planifiée, en cours, en pause, terminée, archivée), propriétaire, historique | MANQUE | écrans E2, E5 du cahier | M (2) | P0 | — |
| E2 | Assistant en 6 étapes (Objectif, Destinataires, Message, Expédition, Contrôle, Envoi) ; ciblage par étiquettes « toutes / au moins une / sauf », listes, audiences, famille, taille, fonction, géographie | MANQUE (les critères existent dans les audiences) | E3 ; `features/audiences/` | L (4) | P0 | C3, C9 |
| E3 | Séquences : étapes, délais en jours ouvrés, gabarit par étape, conditions d'arrêt (réponse, RDV, opposition, rebond, étape « client »), sortie propre | MANQUE | modèles : `sequenceAdvancer.ts`, `ProcessSequencesJob` (rapports B, C) | L (5) | P0 | MOTEUR, (f), (g) |
| E4 | Étapes manuelles dans une séquence (appel, message LinkedIn, courrier) qui créent une tâche | MANQUE (`/linkedin` en 501) | `api.php:609` | S (1) | P1 | D5 |
| E5 | Gabarits (messages types) : éditeur texte d'abord, champs personnalisés par menu, aperçu par destinataire, versions, « utilisé par » | MANQUE | E6 du cahier | L (4) | P0 | — |
| E6 | Blocs fixes obligatoires insérés d'office : identité de l'annonceur, adresse, lien d'opposition, bloc art. 14 au premier message | MANQUE | Z5 J4, J7 ; REQ-SEC-015 | M (2) | P0 | D-07 (entité), D-26 (texte) |
| E7 | Relecture automatique des textes : formulations interdites de Will, mots de spam, liens, poids, champ vide | MANQUE | CRITIQUE C2 | M (2) | P0 | E5 |
| E8 | **Validation par Will** de chaque campagne et de chaque nouvelle version de texte (aperçu de 20 messages, « ce qui va partir »), mode « revue » par défaut ; jamais de validation de prix | MANQUE | E4 du cahier ; `outreachMode.ts` (rapport B) | M (3) | P0 | E1, E5 |
| E9 | Planification : date de départ, heures et jours ouvrés, heure de Paris, jours fériés, fuseaux d'outre-mer, étalement sur la journée | MANQUE | REQ-CHA-027 ; Z6 m4 (horodatages décalés de 2 h à corriger avant) | M (2) | P0 | MOTEUR, L9 |
| E10 | Pression commerciale : au plus un message par personne et par entreprise sur N jours, toutes campagnes confondues | MANQUE | REQ-CAM (pression) | M (2) | P0 | C9 |
| E11 | Pause, reprise, arrêt d'une campagne et arrêt d'urgence global | MANQUE | P9 du cahier (2 clics) | S (1) | P0 | MOTEUR |
| E12 | Variantes (A/B) d'objet et de texte, répartition, règle de volume minimal avant de conclure (à 150/jour un test n'est pas significatif) | MANQUE | CRITIQUE M4 ; modèle `AbTestResults.tsx` | M (3) | P1 | E5, H4 |
| E13 | Variations de texte par IA, chaque version validée par Will, aucun fait inventé, fournisseur UE ou contrat | MANQUE | `generateBroadcastVariations.ts` (rapport B) ; CRITIQUE C2 | M (2) | P2 | E7, E8 |
| E14 | Lien de prise de RDV Calendly personnalisé dans le message (pré-rempli, marqué par campagne) | MANQUE | CAHIER « RDV : 90 jours » (`:361`) | S (1) | P0 | G3 |
| E15 | Campagnes presse et médias : communiqué, liste de rédactions, envoi personne par personne, registre « à qui, quoi, quand », relance d'un journaliste | PARTIEL : registre en lecture seulement | `features/media/EnvoisPressePage.tsx` ; `api.php:278` ; modèles `PressCampaign.tsx`, `PressTemplates.tsx` | M (3) | P1 | E1-E8, segment presse ouvert par réglage |
| E16 | Envoi unitaire depuis une fiche (un message à une personne, tracé) | MANQUE | — | S (1) | P1 | MOTEUR, E6 |
| E17 | Suivi d'une campagne : progression, remis, rebonds, réponses, RDV, oppositions, par messagerie ; chiffres « provisoires » | MANQUE | E5 du cahier | M (3) | P0 | MOTEUR, (f), (g) |
| E18 | Campagnes récurrentes (lettre d'information aux clients, relance trimestrielle) avec consentement distinct de la prospection | MANQUE | `newsletter_optin` reçu du site (`SiteSyncEvent.php:44`) | M (2) | P2 | J1 |
| E19 | Messages déclenchés par un événement (formulaire du site, RDV annulé, inscription Tour France IA) | MANQUE | événements `form_submission`, `calendly_*` (`SiteSyncEvent.php:39-43`) | M (2) | P2 | E3 |
| E20 | Aucun pixel d'ouverture ni clic par personne : garde automatique qui l'interdit | MANQUE (bon par absence) | Z5 D20 ; REQ-SEC-016 | S (0,5) | P0 | E5 |

## (f) Réponses et boîte de réception

| # | Fonction | État | Preuve / modèle | Effort | Prio | Dépendances |
|---|---|---|---|---|---|---|
| F1 | Relève automatique des boîtes d'envoi (IMAP) et rattachement de chaque réponse à la personne, l'entreprise, la campagne et l'étape | MANQUE (0 occurrence IMAP) | CRITIQUE B1 ; modèle `imapMonitor.ts` (rapport B) | L (4) | P0 | MOTEUR (boîtes), décision « quelle boîte reçoit » |
| F2 | Tri automatique : intéressé, pas intéressé, plus tard, absence ou réponse automatique, mauvaise personne, STOP, demande RGPD, hors sujet | MANQUE | modèle `replyCategorizer.ts` | M (3) | P0 | F1 |
| F3 | « STOP » : opposition automatique quand c'est clair, file « STOP à confirmer » sinon ; opposition par **domaine entier** (« plus personne chez nous ») | MANQUE | Z5 J9 ; REQ-RET-025 | M (2) | P0 | F2, J3 |
| F4 | Demande RGPD reçue par réponse → crée la demande dans le module existant, délai d'un mois suivi | PARTIEL (module RGPD existe) | `api.php:444-457` | S (1) | P0 | F2 |
| F5 | « Écrivez plutôt à … » : proposer la nouvelle personne, arrêter la séquence de l'ancienne | MANQUE | — | S (1) | P1 | A11 |
| F6 | Écran Réponses : à traiter, STOP à confirmer, à rattacher, toutes ; action suggérée en bouton principal ; réponse suivante ouverte seule | MANQUE | E7 du cahier ; `Replies.tsx` (backlink) | M (3) | P0 | F1, F2 |
| F7 | Répondre depuis la console (fil de conversation, signature, envoi par la même boîte) | MANQUE (V1 du cahier : lien vers le webmail) | `CAHIER…md:477` | M (3) | P1 | MOTEUR |
| F8 | Délai de traitement : alerte si une réponse « intéressé » attend plus de 24 h ouvrées | MANQUE | CRITIQUE B1 | S (0,5) | P1 | F6, D6 |
| F9 | Toute réponse arrête la séquence de la personne (et, au choix, de son entreprise) | MANQUE | rapports B, C | S (1) | P0 | E3, F1 |

## (g) Rendez-vous (Calendly) et dossier client

| # | Fonction | État | Preuve | Effort | Prio | Dépendances |
|---|---|---|---|---|---|---|
| G1 | Réception des RDV Calendly (pris, honoré, annulé, absent) depuis le site | EXISTE (derrière drapeau) | `SiteSyncEvent.php:40-43` ; `Taxonomy.php:300-302` | — | — | drapeau prod NON VÉRIFIÉ |
| G2 | Rattachement du RDV à la fiche ; sans SIREN → arbitrage, jamais de fusion seule | EXISTE | `DossierClientIngest.php:14-62` ; `ArbitragePage.tsx` | — | — | — |
| G3 | **Attribution** du RDV à la campagne, à la séquence, à la variante et au segment (fenêtre de 90 jours) | MANQUE | CRITIQUE B2 | M (2) | P0 | E14, E1 |
| G4 | RDV pris → arrêt de la séquence + passage à l'étape « opportunité » (jamais de recul) | MANQUE | `DossierClientIngest.php` (l'étape ne bouge pas, sauf « client ») | S (1) | P0 | décision de Will (étape automatique) |
| G5 | RDV non honoré ou annulé → tâche de relance automatique | MANQUE | — | S (0,5) | P1 | D7 |
| G6 | Lien direct fiche CRM ↔ dossier client de la console (`console_client_ref`), résumé en lecture : étape, projet, prochaine action | PARTIEL (référence stockée, pas de lien ni résumé) | `DossierClientIngest.php` | S (1) | P1 | K1 |
| G7 | Le dossier client lui-même (rencontre, projet, devis, suivi) | **Ne pas construire dans le CRM** : il vit dans la console du site | mémoire `prospects-rdv-dossier-client-console-existe-2026-10-24.md` | — | — | — |

## (h) Statistiques et tableaux de bord

| # | Fonction | État | Preuve | Effort | Prio | Dépendances |
|---|---|---|---|---|---|---|
| H1 | Tableau de bord : chiffres de collecte, « À faire », audiences, qualité | EXISTE | `DashboardController.php:112-276` ; `features/dashboard/` | — | — | — |
| H2 | Carte de couverture | EXISTE | `features/coverage/FranceCoverageMap.tsx` | — | — | — |
| H3 | Entonnoir commercial : contacté → répondu → intéressé → RDV → opportunité → client, par période | MANQUE | Z3 §3 point 11 | M (2) | P1 | G3, D1 |
| H4 | Résultats par campagne, séquence, étape, variante, segment, expéditeur : remis, rebonds, réponses, RDV, oppositions, plaintes (pas d'ouvertures) | MANQUE | E17 du cahier ; CRITIQUE M4 | L (4) | P0 | MOTEUR, (f), (g) |
| H5 | Activité : messages envoyés, réponses traitées, tâches faites, par jour et par personne | MANQUE | — | S (1) | P1 | D5, F6 |
| H6 | Volume envoyable par famille et fraîcheur des vérifications | MANQUE | Z1 manques 5-6 | S (1) | P0 | C10 |
| H7 | Rapport hebdomadaire par e-mail (envoyés, rebonds, plaintes, réponses, RDV) + rapports figés exportables | MANQUE | modèle `weeklyReport.ts` (rapport B) | M (2) | P1 | H4, L3 |
| H8 | Coût mensuel visible (vérification d'adresses, IA, serveurs) : information seulement, jamais de validation | MANQUE | CRITIQUE C1 | S (1) | P1 | M5 |

## (i) Sécurité, droits, 2FA par e-mail

| # | Fonction | État | Preuve | Effort | Prio | Dépendances |
|---|---|---|---|---|---|---|
| I1 | **2FA par e-mail** : code à 6 chiffres envoyé à l'adresse du compte, usage unique, 10 min, essais limités par compte, appareil de confiance (durée à trancher), code redemandé pour les exports et les gestes sensibles | MANQUE (TOTP par application seulement ; 2FA éteinte sur le compte de Will) | `TwoFactorController.php:17-56` ; mémoire `crm-prod-acces-mailer-telescope.md` | M (2) | P0 | L3 (mailer d'authentification) |
| I5 | Refus de démarrer en production sans le cloisonnement des espaces (RLS) actif + test IDOR en boîte noire | MANQUE | `config/database.php:37` ; Z7 §3 | M (2) | P0 | indispensable avant (m) |
| I6 | Gitleaks et contrôles de sécurité exigés pour fusionner ; mise à jour de `maplibre-gl` ; CSP en production | MANQUE | Z7 M4, M5, m1 | S (1) | P0 | — |
| I7 | Journal des **lectures** de fiches nominatives ; IP du journal en empreinte | MANQUE | `AuditHashChainLogger.php:93` | S (1) | P1 | — |
| I8 | Rôles personnalisés et permissions fines (par espace) | PARTIEL : 4 rôles et 16 permissions figés | `PermissionsAndRolesSeeder.php:13-70` | M (3) | P1 | M2 |
| I9 | Sessions et appareils connectés : liste, déconnexion à distance | MANQUE | — | S (1) | P2 | I1 |
| I10 | Lien magique atomique, codes 2FA non réutilisables, plus d'adresse en clair dans les journaux | MANQUE | Z7 m3, m4, m5 | S (1) | P1 | — |

## (j) Conformité

| # | Fonction | État | Preuve | Effort | Prio | Dépendances |
|---|---|---|---|---|---|---|
| J1 | Opposition globale (empreinte gardée), liste de suppression, recontrôle avant chaque envoi | EXISTE | `EligibiliteCampagne.php:108-242` ; `ListeSuppression.php` | — | — | — |
| J2 | Écran « Ne plus écrire » : « Puis-je écrire à … ? » (oui/non et pourquoi), ajouter, réautoriser une erreur technique | MANQUE | E16 du cahier | M (2) | P0 | J1 |
| J3 | Opposition par domaine destinataire | MANQUE | Z5 J9 | S (1) | P0 | J1 |
| J4 | Demandes RGPD (accès, effacement, portabilité), registre IA | EXISTE | `api.php:100,444-457` | — | — | — |
| J5 | Registre art. 14 par adresse : date, version du texte, campagne (au-delà de `first_info_at`) | PARTIEL | `CrmCampagneRetours.php:21-26` | M (2) | P0 | E6 |
| J6 | Provenance obligatoire de chaque fiche (source réelle et date) affichée dans le bloc art. 14 | PARTIEL (`provenance_tiers`) | migration `2026_10_03_000080` | S (1) | P0 | B4 |
| J7 | Textes : bloc art. 14 par flux, pied de message, page publique « prospection » sur le site, politique de conservation écrite (illimitée, motif) | MANQUE | Z5 J4, J6, J11 | M (2) rédaction | P0 | D-07, D-26 |
| J8 | AIPD révisée, analyses d'intérêt légitime par flux, ligne au registre art. 30, contrats de sous-traitance | MANQUE | Z5 J3, J12, J13, J14 ; `TODO.md` §3 | M (3) rédaction | P0 | décisions de Will |
| J9 | Désactiver les workflows qui suppriment encore des fiches (`purge-non-commercial`, `purge-non-diffusible`) | MANQUE | `.github/workflows/prospection-collect-region.yml:104-105` | S (0,5) | P0 | accord de Will (respect de « ne rien purger ») |
| J10 | Notification CNIL de la fuite du 19/08 (ou motif écrit de non-notification) | MANQUE | `TODO.md` §4 | — (décision) | P0 | Will |
| J11 | Retirer du dépôt public les données de journalistes | MANQUE | Z7 C2 | S (0,5) | P0 | Will |
| J12 | Écran Conformité : registre, sous-traitants, analyses, entité, versions des textes | MANQUE | E21 du cahier | M (2) | P1 | J7, J8 |

## (k) Synchro console ⇄ CRM

| # | Fonction | État | Preuve | Effort | Prio | Dépendances |
|---|---|---|---|---|---|---|
| K1 | Console → CRM : signature, idempotence, dossier client, « le plus récent gagne », aucune suppression propagée | EXISTE (drapeaux à ouvrir) | `SiteSyncController.php:37-84` ; `DossierClientIngest.php` | — | — | état prod NON VÉRIFIÉ |
| K2 | CRM → console : **retouches de fiche** (identité, coordonnées, étape), même règle « plus récent gagne », jamais de montant, jamais le texte du questionnaire | MANQUE (oppositions seulement) | `ConsentOutboundRecorder.php:7-30` ; plan `_PLAN-QUESTIONNAIRE-PREAUDIT-2026-10-24\PLAN-SYNCHRO-CONSOLE-CRM-PRO.md` | M (3) | P0 | côté site |
| K3 | Ouverture des 3 clés du sens sortant + runbook d'ouverture | MANQUE | `TODO.md` §1.2 | S (0,5) | P0 | session déployeuse |
| K4 | Écran « Santé de la synchro » : en attente, abandonnés, dernier passage, rejouer | MANQUE | modèle `MissionControlSync.tsx` | S (1) | P1 | K2 |
| K5 | Historique des valeurs remplacées visible sur la fiche | PARTIEL (gardé en chronologie) | `DossierClientIngest.php` (d) | S (0,5) | P1 | A6 |
| K6 | Test de bout en bout avec la console réelle (préproduction) | MANQUE | Z3 « Trous » | S (1) | P0 | K2 |

## (l) Exploitation

| # | Fonction | État | Preuve | Effort | Prio | Dépendances |
|---|---|---|---|---|---|---|
| L1 | Sauvegarde quotidienne chiffrée + copie Backblaze hebdomadaire + surveillance | EXISTE | `infra/scripts/backup-postgres.sh` ; `surveillance-sauvegarde.yml` | — | — | — |
| L2 | Copie hors site quotidienne, alerte avant le plafond de 9 Go, sauvegarde rapprochée des oppositions, exercice de restauration mensuel daté | MANQUE | Z1 M5 ; Z6 M1-M2 | M (2) | P0 | — |
| L4 | Alertes qui atteignent Will **par e-mail** (pas de push) : erreurs, file bloquée, disque, sauvegarde, synchro ; bouton « alerte de test » | MANQUE (récepteur Telegram absent) | `alertmanager.yml:30` ; Z6 C2 | M (2) | P0 | L3 |
| L5 | Inventaire unique « drapeau → valeur » de la production | MANQUE | CRITIQUE C5 | S (0,5) | P0 | session déployeuse |
| L6 | Pare-feu de l'hôte versionné, utilisateur de déploiement restreint, clé d'hôte épinglée | MANQUE | Z6 C1, M4 | M (2) | P0 | — |
| L7 | Limites mémoire, Redis des files sans éviction, alertes disque et RAM | MANQUE | Z6 M6 | S (1) | P1 | — |
| L8 | Calcul planifié de la joignabilité et de la vérification des adresses | MANQUE (commandes non planifiées) | Z1 M3 | S (0,5) | P0 | — |
| L9 | Correction du décalage de 2 h des horodatages | MANQUE | Z6 m4 | S (1) | P0 | avant E9 |
| L10 | Mode d'emploi d'une page pour Will + temps quotidien estimé | MANQUE | CRITIQUE M2 | S (0,5) | P1 | — |
| L11 | Ménage des documents périmés (`_REPORTS/PROGRESS.md`, ancien TODO, `backend;C`) | MANQUE | Z1 m4 ; Z3 m8 | S (0,5) | P2 | — |

## (m) Multi-locataire et déploiement chez des clients

Base existante : espaces de travail (`workspaces`, `user_workspaces`, `workspace_id` partout), RLS écrite mais non prouvée active (`2026_08_14_000001_harden_workspace_isolation.php`), plafond de coût IA par espace (`Workspace.php:45`, `cost_cap_eur`), permission `workspaces.manage` (`api.php:139`). Rien n'existe pour installer, configurer, facturer ou suivre un client.

| # | Fonction | État | Preuve | Effort | Prio | Dépendances |
|---|---|---|---|---|---|---|
| M0 | **Choix du modèle** : une instance par client (base et serveur séparés) ou des espaces dans une instance commune. Recommandation : instance dédiée par client tant que la RLS n'est pas prouvée (fuite du 19/08) | MANQUE (décision) | — | — | P0 | Will |
| M1 | Isolement des données prouvé : RLS armée, test IDOR, aucune donnée d'Axion (base INSEE, presse, oppositions d'Axion) visible chez un client | PARTIEL | I5 ; `opt_out` et `email_suppressions` sans `workspace_id` (Z1 M4) | L (4) | P0 | I5 |
| M2 | Rôles par client : owner du client, membres, lecteurs ; accès support d'Axion tracé et limité dans le temps | PARTIEL (rôles globaux) | `PermissionsAndRolesSeeder.php` | M (3) | P0 | I8 |
| M3 | Configuration par client : identité de l'annonceur, segments ouverts, référentiels, étapes du pipeline, champs personnalisés, gabarits, heures d'envoi, textes art. 14 au nom du client | MANQUE (`settings` libre) | `Workspace.php:45-50` | L (4) | P0 | A12, E6 |
| M4 | Marque blanche : logo, couleurs, nom, sous-domaine, adresse d'expédition des courriels de service | MANQUE | — | M (3) | P2 | M3 |
| M5 | Usage et facturation : compteurs (fiches, envois, vérifications, IA, utilisateurs), remise à zéro à la **date anniversaire** de l'abonnement, plafonds informatifs, lien Stripe ; aucun blocage par validation de prix | PARTIEL (plafond IA seul) | `cost_cap_eur` ; décisions console du 27/10 (Stripe, date anniversaire) | L (4) | P1 | console automatisations (facturation) |
| M6 | Expéditeurs, domaines et liste d'opposition **propres à chaque client** (réputation séparée) + liste d'opposition globale d'Axion pour ses propres envois | MANQUE | Z1 M4 | M (3) | P0 | MOTEUR |
| M7 | Sauvegardes par client et restauration d'un seul client sans toucher aux autres | MANQUE (sauvegarde de toute la base) | `backup-postgres.sh` | M (3) | P0 | M0 |
| M8 | Installation automatisée d'un client (serveur, base, secrets, domaine, premier compte) en une commande, sans copier de secret d'Axion | MANQUE (Terraform d'une ancienne spec) | `infra/terraform` ; Z6 C4 | L (5) | P0 | M0 |
| M9 | Mises à jour : version publiée, migrations sans coupure, mise à jour de tous les clients par vagues, retour arrière | MANQUE (déploiement SSH d'une seule prod) | `deploy-direct-ssh.yml` ; Z6 M4 | L (4) | P1 | M8 |
| M10 | Support : diagnostic par client (version, drapeaux, santé, erreurs, files), journal d'accès du support, demande de support depuis l'application | MANQUE | décision console « support avec diagnostic par client » (26/10) | M (3) | P1 | L4, M2 |
| M11 | Supervision de tous les clients depuis la console d'Axion (santé, version, usage, alertes) | MANQUE | — | M (3) | P1 | M5, M10 |
| M12 | Contrat : Axion sous-traitant du client (modèle de DPA, registre, sous-traitants ultérieurs), réversibilité (B7), aucune suppression en fin de contrat sans ordre écrit du client | MANQUE | `TODO.md` §3 ; décision « jamais de suppression en fin de client » (26/10) | M (2) rédaction | P0 | Will |
| M13 | Accueil d'un nouveau client : assistant « Mise en route » (import, identité, premier utilisateur, 2FA par e-mail, premier segment) | MANQUE | E23 du cahier (pour l'envoi) | M (3) | P1 | B4, M3 |

---

## Ordre de construction en 5 lots (tout est construit ; seuls les volumes démarrent petit)

Total estimé (milieu des fourchettes) : environ **185 jours-agent** côté CRM, hors moteur d'envoi et hors rédaction juridique faite par Will. En parallèle sur plusieurs agents, les lots 2 et 3 se chevauchent.

| Lot | Contenu | Lignes | Effort | Condition de sortie |
|---|---|---|---|---|
| **2. Travail quotidien** | Ajout rapide, notes et appels, Kanban, opportunités, Mes tâches, rappels du matin par e-mail, tâches automatiques, vues sauvegardées, actions de masse, import de fichier par l'interface, provenance, fonctions des personnes, synchro CRM → console et son écran de santé | A4, A5, A10, A11, D2-D7, C4, C5, B4, B5, J6, K2-K6, G6 | ≈ 38 j | Will travaille une journée entière dans le CRM sans tableur ni console à côté |
| **3. Campagnes** (avec le moteur) | Objet campagne, assistant, ciblage et exclusions, liste figée, volume envoyable, gabarits, blocs légaux, relecture des interdits, validation par Will, planification, pression, pause et arrêt, séquences avec étapes manuelles, lien Calendly, garde « aucun pixel », écran « Ne plus écrire », opposition par domaine, registre art. 14, déclarations manuelles | E1-E11, E14, E16, E20, C7-C10, J2, J3, J5, B6 | ≈ 50 j | Première campagne de 150 messages validée, partie, suivie |
| **4. Réponses, RDV et mesure** | Relève des boîtes, tri, STOP, demandes RGPD, écran Réponses, réponse dans la console, arrêt des séquences, attribution des RDV, étape « opportunité », relances après RDV, suivi de campagne, résultats, entonnoir, activité, rapports hebdomadaires, coûts, badges et chronologie complète, A/B, presse et médias | F1-F9, G3-G5, E12, E15, E17, H3-H8, A6, A7, J12 | ≈ 45 j | Chaque réponse est traitée sous 24 h ; chaque RDV est rattaché à sa campagne |
| **5. Déploiement chez des clients et échelle** | Modèle d'instance, isolement, rôles par client, configuration, marque blanche, usage et facturation, expéditeurs par client, sauvegardes et restauration par client, installation, mises à jour par vagues, support, supervision, contrats, mise en route ; puis champs personnalisés, propriétaires, assignation, recontact, campagnes récurrentes et déclenchées, variations IA, sessions, rôles fins | M0-M13, A12, A13, D8, D9, E13, E18, E19, I7-I10, B7, B8, L7, L10, L11 | ≈ 60 j (dont M1, M3, M7, M8, M12 en P0 avant le 1er client) | Un client pilote installé en une commande, isolé, sauvegardé à part, mis à jour sans coupure |

**Ce qui démarre petit : les volumes, pas les fonctions.** Premier envoi à 150 messages par jour sur les adresses les plus sûres (génériques d'organisateurs et de fédérations), une ou deux boîtes, puis montée seulement si les rebonds restent sous 2 % et les plaintes sous 0,1 % ; objectif 5 000 par jour durables, jamais en multipliant les domaines pour contourner un blocage.

## Décisions à demander à Will

1. Modèle client : une instance par client (recommandé) ou espaces partagés ?
2. RDV pris → étape « opportunité » posée automatiquement (jamais de recul) ?
3. Quelle boîte reçoit les réponses des campagnes (liée au choix de l'hébergeur des boîtes, D-70) ?
4. 2FA par e-mail : code à chaque connexion, ou appareil de confiance pendant 30 jours (recommandé), avec code toujours redemandé pour un export ?
5. Retouches CRM → console : identité, coordonnées et étape suffisent-ils (jamais de montant, jamais de réponse au questionnaire) ?
6. Montants d'opportunité dans le CRM, à titre d'information seulement ?
7. Date d'ouverture de la famille TPE/PME (INSEE) à la prospection ; presse rouverte par réglage explicite ?
8. Désactivation des deux workflows de purge ; courriels d'authentification autorisés à sortir (ZeptoMail) ?
9. Clients : leur facturer à l'usage (compteurs, date anniversaire) via Stripe, comme pour la console ?
