# 21 : LOT R0 : relevé de l'existant du CRM (01/11/2026)

**But.** Avant d'écrire la moindre ligne de code du plan 20, savoir **ce qui marche déjà**, **qui s'en sert**, et **quel lot risque de le casser**. Ce fichier sert de base au filet de non-régression (fichier 22).

**Comment ce relevé a été fait.** Lecture seule du dépôt du CRM (dernière version de `main`, fusion #386). **Rien n'a été exécuté** : aucun serveur touché, aucune commande lancée, aucun e-mail envoyé. Ce qui n'a pas pu être vérifié en lisant est listé au § 10.

**Règles du dépôt public respectées.** Aucun secret, aucune adresse de serveur, aucun mot de passe, aucune donnée de personne réelle. Les points de sécurité sont donnés **par catégorie** seulement.

**Lecture des colonnes.**
- **Lot à risque** : le lot du plan 20 (§ 3) qui risque de toucher l'élément.
- **Risque** : **faible** (rien ne change pour l'utilisateur si ça casse, ou le lot n'y touche presque pas), **moyen** (une fonction visible peut s'arrêter, mais on le voit vite), **élevé** (perte de données, envoi non voulu, obligation légale manquée, ou panne silencieuse).

---

## 1. En bref (12 lignes)

1. Le CRM a déjà **beaucoup de choses qui tournent seules** : **44 tâches planifiées** et 1 battement par minute.
2. **31 workflows GitHub**, dont **25 se connectent au serveur de production ou de préproduction** (déploiement, collecte, enrichissement, diagnostic, surveillance).
3. Le **déploiement part tout seul** à chaque fusion sur `main`, après la CI.
4. Beaucoup de fonctions sont **éteintes par un drapeau** (synchro avec le site, purges RGPD, ingestion, envoi vers le site) : ces drapeaux sont lus sur le serveur, **leur état réel n'est pas connu** en lisant le dépôt.
5. Les **simulateurs** (`MOCK_*`) sont déjà **refusés en production** (avec alerte), mais le démarrage n'est pas bloqué.
6. **10 tables d'ébauche** demandées : 9 sont des coquilles vides d'une ancienne ébauche (mai 2026), jamais utilisées par le code ; `opt_out` et `email_suppressions` sont, elles, **le cœur de l'opposition** et servent partout.
7. La **chaîne d'envoi faite à la main** existe : une commande prépare la liste des destinataires (fichier), une autre enregistre les retours (désinscription, plainte, rebonds). Le CRM **n'envoie rien lui-même**.
8. **Deux canaux signés** avec le site : la synchro du site (fermée par drapeau) et le socle « Partners » (fermé par défaut). Un troisième sens, CRM → site (« outbound »), est fermé aussi.
9. **122 migrations**, toutes ont une fonction de retour, mais **9 ont un retour vide** et **14 refusent le retour** (volontairement).
10. **54 écrans** dans le frontend ; plusieurs routes serveur prêtes **n'ont pas d'écran** (vues sauvegardées, modification et retrait d'un contact, action de masse CRM).
11. Le mot « **campagnes** » désigne aujourd'hui les **campagnes de collecte** (scraping), pas des campagnes d'e-mails : conflit direct avec le lot C1.
12. **391 fichiers de tests** existent déjà, et la CI est **bloquante** : le filet R0 doit **s'appuyer dessus**, pas repartir de zéro.

---

## 2. Tâches planifiées (`backend/routes/console.php`)

Le planificateur tourne dans un conteneur dédié. Il est **recréé à chaque déploiement**. Les verrous anti-chevauchement ont une durée bornée (6 h au plus) et sont libérés au redémarrage. Un battement chaque minute permet de voir si le planificateur s'est arrêté.

### 2.1 Socle, audit, sécurité

| Tâche | Quand | Ce que ça fait | Qui l'utilise | Lot à risque | Risque |
|---|---|---|---|---|---|
| `coverage:refresh-matrix` | chaque heure | Recalcule la matrice de couverture (carte des zones collectées) | écran « Couverture » | S7 (RLS, rôle de production) | moyen (a déjà cassé sans bruit en août) |
| `blacklists:check` | chaque heure | Vérifie les listes noires | exploitation | E8 (surveillance des listes noires) | moyen : risque de **doublon** avec E8 |
| `audit:verify-chain` | 03:00 | Vérifie que le journal d'audit n'a pas été modifié | sécurité | S7, S9 | élevé (alerte critique si rompu) |
| `db:partman-maintenir` | 01:30 | Crée les partitions du journal d'audit, applique la rétention 24 mois | base de données | S7 (tables migrées), S9 | élevé (sans elle, le journal d'audit ne peut plus écrire après la dernière partition) |
| `anomaly:detect` | toutes les 15 min | Détecte des anomalies | exploitation | S9 (alertes) | faible |
| `signals:nightly-scan` | 02:00 | Balayage nocturne des signaux | prospection | S7 | faible |
| battement du planificateur | chaque minute | Pose un horodatage ; la surveillance alerte s'il a plus de 15 min | surveillance des canaux | S9 (battement externe) | moyen |

### 2.2 RGPD et purges

| Tâche | Quand | Ce que ça fait | Qui l'utilise | Lot à risque | Risque |
|---|---|---|---|---|---|
| `retention:purge --all-workspaces` | 04:00 | Applique les durées de conservation (supprime) | conformité | S7, P2, J1, **décision « pas de purge »** | **élevé** |
| `rgpd:anonymize-ips` | 04:30 | Anonymise les adresses IP anciennes | conformité | S7 | moyen |
| `rgpd:verifications-en-attente` | 07:10 | Relance les demandes RGPD en attente | demandes RGPD | S7 (RGPD par espace), U11 | moyen |
| `rgpd:purge-vivier` | le 2 du mois | Purge candidats (2 ans) | conformité | S7, J3 | **élevé** — **sautée** tant que `CRM_PURGE_ENABLED` est éteint (saut écrit au journal) |
| `rgpd:purge-business-prospects` | le 2 du mois | Purge prospects (3 ans) | conformité | S7, P2, **décision « pas de purge »** | **élevé** — sautée, même drapeau |
| `rgpd:purge-personnes` | le 2 du mois | Purge personnes de la lettre et du guide inactives | conformité | S7, C6 | **élevé** — sautée, même drapeau |
| `retention:prune-scraper-runs --days=90` | 04:20 | Supprime l'historique des passages de collecte | exploitation | faible | faible |

### 2.3 Sondes et synchro

| Tâche | Quand | Ce que ça fait | Qui l'utilise | Lot à risque | Risque |
|---|---|---|---|---|---|
| sonde « clé de personne » | 06:10 | Contrôle la cohérence des clés de personnes ; alerte si échec | données | S7, Q1 | moyen |
| sonde « non diffusibles » | 06:20 | Contrôle que les fiches Sirene non diffusibles sont bien marquées | conformité (C3) | C3, S7 | **élevé** (garde légale) |
| sonde « personnes » | 06:30 | Alerte si des inscriptions du site arrivent sans créer de personne | synchro du site | S7, P2, ADR consoles (§ 11.2) | moyen |
| `crm:flush-outbound` | toutes les 5 min | Envoie au site les oppositions nées dans le CRM | site ↔ CRM | P4, ADR consoles, S7 | **élevé** — **sautée** tant que `CRM_OUTBOUND_ENABLED` est éteint |

### 2.4 Campagnes et listes

| Tâche | Quand | Ce que ça fait | Qui l'utilise | Lot à risque | Risque |
|---|---|---|---|---|---|
| `campaigns:start-scheduled` | chaque minute | Démarre les **campagnes de collecte** programmées (pas des e-mails) | écran « Campagnes » | **C1** (même mot), S7 | **élevé** (collision de nom avec le moteur de campagnes) |
| `audiences:full-refresh` | 04:00 | Recalcule les audiences | écran « Audiences » | C1 (ciblage), S7 | moyen |
| `crm:emails:verifier` | dimanche 05:00 | Vérifie les adresses e-mail (le domaine reçoit-il du courrier ?) | préparation des destinataires | **E4** (vérification des adresses) | moyen — **sautée** tant que `CRM_EMAILS_VERIFICATION_PLANIFIEE` est éteint ; à **étendre**, pas réécrire |
| `prospection:score-email-confidence` | 04:45 | Note la confiance des adresses | prospection | E4 | faible |

### 2.5 Collecte et enrichissement (prospection, presse, secteur public)

| Tâche | Quand | Ce que ça fait | Lot à risque | Risque |
|---|---|---|---|---|
| `companies:rescrape-archives`, `companies:retry-google-places` | le 1er du mois | Relance la collecte sur des fiches archivées ou incomplètes | S7, P2 | faible |
| 13 tâches `media:*` (extraction, synchro, liens, import CPPAP/SPEL/agences, Wikidata, Arcom, blogs, périodicité, confiance, nettoyage, enrichissement toutes les 3 h) | quotidien ou hebdo | Base presse | S6 (segment presse fermé par défaut), S7 | moyen |
| `journalists:scrape-ours` | 05:40 | Lit les ours des journaux | S6, S7 | moyen |
| `crm:insee:mise-a-jour-mensuelle` (+ reprise) | le 4 du mois, reprise ensuite | Met à jour les fiches depuis l'INSEE (fermées, non diffusibles) | **C3**, S7 | **élevé** (alimente la garde Sirene) |
| `crm:public:annuaire-officiel` | à partir du 6, 15:00 | Complète les fiches du secteur public | S7 | moyen |
| `crm:federations:trouver-sites` | le 3 du mois | Cherche le site des fédérations | S7 | faible — **sautée** tant que `CRM_BRAVE_FEDERATIONS_PLANIFIEE` est éteint |

**Point d'attention commun : S7.** Le lot S7 arme la barrière d'isolation (RLS) par défaut. **Toutes** ces tâches tournent en dehors d'une requête web : si elles n'ont pas le bon contexte d'espace, elles **ne verront plus rien** (zéro ligne, sans erreur). C'est le premier risque du plan.

---

## 3. Workflows GitHub (`.github/workflows`)

**Seuls 6 workflows ne touchent aucun serveur.** Les 25 autres se connectent au serveur par une clé d'accès gardée dans GitHub (catégorie : « clé de serveur dans le dépôt public », déjà prévue au retrait par S11).

### 3.1 Sans connexion à un serveur (contrôles, gratuits sur un dépôt public)

| Workflow | Déclencheur | Ce que ça fait | Risque |
|---|---|---|---|
| `ci.yml` | chaque PR, et appelé par le déploiement | Contrôle de la config de prod, Caddy, scripts exécutables, données personnelles, backend (PHPStan, Pint, **tests Pest sur un vrai Postgres**), frontend, workers. **Bloquant.** | — (c'est la porte du filet) |
| `e2e.yml` | push sur `main` et PR | 11 suites e2e Playwright sur le build. **Bloquant.** | — |
| `a11y.yml` | push et PR | Accessibilité (axe, Lighthouse) | — |
| `security.yml` | push, PR, chaque lundi | Secrets, analyse statique, images, dépendances, ZAP | — |
| `build-postgres-image.yml` | push, à la main | Construit l'image Postgres (PostGIS, pgvector, partman) | faible |
| `release-tracking.yml` | version, push | Suivi des versions (suivi d'erreurs) | faible |

### 3.2 Avec connexion au serveur

| Workflow | Déclencheur | Ce que ça fait | Lot à risque | Risque |
|---|---|---|---|---|
| `deploy-direct-ssh.yml` | **chaque push sur `main`** (sauf docs), après la CI | Déploie la **production** : image, `migrate`, vide le cache, recrée le planificateur | S5, S7, S11, toute migration | **élevé** |
| `deploy-staging.yml` | **chaque push sur `main`** | Déploie la **préproduction**, `migrate` | S7 (rejeu en préproduction) | **élevé** |
| `surveillance-canaux.yml` | chaque heure (minute 17) | Lance `crm:canaux:etat` (état des canaux, battement du planificateur) | S9, S11 | moyen |
| `surveillance-sauvegarde.yml` | chaque jour 05:00 | Vérifie que la sauvegarde de la nuit existe | S9, S11 | **élevé** (la sauvegarde a déjà été cassée sans bruit) |
| `crm-doublons.yml`, `crm-presse.yml` | à la main | Détecte et fusionne les doublons ; harmonise la presse | S7 | moyen |
| `prospection-collect*.yml` (3), `prospection-enrich`, `prospection-find-websites*` (2), `prospection-stats`, `prospection-reclassify` | à la main | Collecte et enrichissement. **`prospection-reclassify` et `prospection-collect-region` lancent des purges d'entreprises** | S7, **décision « pas de purge »**, S9 | **élevé** pour les deux qui purgent, moyen pour les autres |
| `pharmacies-*.yml` (6), `finess-sante-enrichir.yml` | à la main | Import, enrichissement, téléphones, sites, écart des pharmacies fermées (premier client de la console) | S7, K12 (base sectorielle) | moyen |
| `diag-pharmacies*.yml` (3) | à la main | Diagnostics en lecture seule | S7 | faible |
| `diag-website-status.yml` | à la main | Workflow ancien de **récupération** (juillet), avec des gestes d'administration du serveur | S11 | **élevé** (à revoir ou retirer en premier par S11) |

**Règle à tenir (plan 20, § 11.4)** : on ne retire la clé de serveur d'un workflow **qu'après** avoir remplacé ce workflow (tirage d'image, commande programmée, etc.).

---

## 4. Interrupteurs (drapeaux)

### 4.1 Simulateurs `MOCK_*`

| Drapeau | Ce qu'il simule | Défaut |
|---|---|---|
| `MOCK_MODE` | maître de tous les autres | vrai en local et en test, **faux** en production et en préproduction |
| `MOCK_LLM`, `MOCK_PROXIES`, `MOCK_CAPTCHA`, `MOCK_SMTP`, `MOCK_INSEE`, `MOCK_ANNUAIRE_ENTREPRISES`, `MOCK_BODACC`, `MOCK_BAN`, `MOCK_FRANCE_TRAVAIL`, `MOCK_SCRAPERS` | services externes | suit `MOCK_MODE` |
| `MOCK_MAIL`, `MOCK_IGN`, `MOCK_RPPS` | courrier, cartes, annuaire santé | lus ailleurs (fichiers de config), à vérifier qu'ils passent par la même garde |

**Déjà en place** : en production, un simulateur demandé est **refusé** et une alerte critique est écrite (test `AucunSimulacreEnProductionTest`). **Ce qui manque** (plan 20, § 11.5) : refuser **le démarrage** et couvrir `MOCK_MAIL`, `MOCK_IGN`, `MOCK_RPPS`. Lot à risque : **S2, P1, E1** (le simulateur du serveur d'envoi sera un nouveau simulateur). Risque : **élevé** (un faux envoi « réussi » en production serait invisible).

### 4.2 Drapeaux du CRM (tous **éteints par défaut** dans le code)

| Drapeau | Ce qu'il ouvre | Lot à risque | Risque |
|---|---|---|---|
| `CRM_INGEST_ENABLED` | Réception de la synchro du site (sinon 503) | ADR consoles, P4, S7 | **élevé** |
| `CRM_INGEST_DOSSIER_ENABLED`, `CRM_INGEST_PERSONNES_ENABLED`, `CRM_INGEST_CANDIDATES_ENABLED` | Sous-parties de la synchro (dossier client, personnes, candidats) | ADR consoles, S7 | **élevé** |
| `CRM_SYNC_DOSSIER_CLIENT_STAGE` | Étape de la synchro du dossier client | ADR consoles (synchro dans les deux sens) | **élevé** |
| `CRM_OUTBOUND_ENABLED` | Envoi des oppositions CRM → site | ADR consoles, P4 | **élevé** |
| `CRM_PURGE_ENABLED` | Purges RGPD mensuelles | J3, décision « pas de purge » | **élevé** |
| `CRM_DB_APP_ROLE_ENABLED` | Rôle de base « applicatif » qui porte la barrière RLS | **S7** | **élevé** |
| `CRM_SEGMENTS_OUVERTS` (liste, vide par défaut) | Segments ouverts aux campagnes | **S6** (segments fermés par défaut, par espace) | **élevé** |
| `CRM_PARTNERS_MODE` (`off` par défaut) | Canal Partners | P4, ADR consoles | moyen |
| `CRM_EMAILS_VERIFICATION_PLANIFIEE` | Vérification hebdo des adresses | E4 | moyen |
| `CRM_BRAVE_FEDERATIONS_PLANIFIEE` | Recherche mensuelle des sites de fédérations | — | faible |
| `CRM_BACKFILL_ENABLED`, `CRM_PROVENANCE_TIERS_ENABLED`, `CRM_SCRAPE_FUNNEL_ENABLED` | Rattrapages, provenance des données tierces, entonnoir de collecte | Q1 (provenance), S7 | moyen |

**Important** : aucun de ces drapeaux n'est écrit dans les fichiers Compose du dépôt. Leur valeur réelle est dans la configuration du serveur, **que ce relevé n'a pas lue** (voir § 10).

---

## 5. Tables d'ébauche

| Table | Créée par | Utilisée par le code ? | Ce qu'elle devient dans le plan 20 | Lot à risque | Risque |
|---|---|---|---|---|---|
| `opt_out` | migration du socle (mai), complétée en août (empreinte seule, sans adresse en clair) | **Oui, partout** : ingestion du site, presse, candidats, déduplication, effacement et export RGPD, éligibilité de campagne | à **réutiliser** ; reçoit `workspace_id` | **P2**, S7, C1 | **élevé** (c'est l'opposition des personnes) |
| `email_suppressions` | août 2026 | **Oui** : rebonds, plaintes, webhook du courrier transactionnel, éligibilité | à **réutiliser** ; reçoit `workspace_id` | **P2**, E5 | **élevé** |
| `unsubscribes` | ébauche de mai | Non (cité seulement par l'export RGPD et la barrière d'isolation) | doublon d'`opt_out` : à **retirer** (ou figer), avec test « l'export contient tout ce qu'il contenait » | P2, E6 | moyen |
| `email_inboxes` | ébauche de mai | Non | à **remplacer** par le registre des boîtes de E3, ou réutiliser | E3 | faible |
| `email_threads` | ébauche de mai | Non (couverte par la barrière d'isolation) | candidate pour les fils de réponse de RP1 | RP1, C1 | faible |
| `email_warmup_pools` | ébauche de mai | Non | remplacée par la chauffe de E7 | E7 | faible |
| `crm_pipelines` | ébauche de mai | Non | candidate pour les étapes de Will (Q1b) et le Kanban (Q2) | Q1b, Q2 | faible |
| `deals` | ébauche de mai | Presque pas (citée par la fusion de doublons et un index) | candidate pour « Affaires » (Q2) | Q2, **ADR consoles** (qui possède les affaires ?) | moyen |
| `crm_notes` | ébauche de mai | Non | candidate pour les notes (Q2) | Q2, ADR consoles | faible |
| `crm_tasks` | ébauche de mai | Non | candidate pour « Mes tâches » (Q1b) | Q1b, ADR consoles | faible |

**Contradiction trouvée** : un commentaire du code dit que `unsubscribes` et `dnc_entries` « n'ont jamais existé », alors que l'ébauche de mai les crée. À vérifier sur la base réelle (§ 10).

L'ébauche de mai contient aussi d'autres tables jamais utilisées (LinkedIn, analytique, `dnc_lists`). Elles sortent du périmètre de R0 mais doivent être **arbitrées une seule fois** (réutiliser ou retirer) dans P1.

---

## 6. Chaîne d'envoi faite à la main (`crm:campagne:*`)

Aujourd'hui, **le CRM n'envoie aucun e-mail commercial**. Il prépare, un outil externe envoie, puis le CRM enregistre les retours.

| Étape | Commande | Ce que ça fait | Lot à risque | Risque |
|---|---|---|---|---|
| 1. Vérifier | `crm:emails:verifier` | Marque les adresses valides (le domaine reçoit du courrier) | E4 | moyen |
| 2. Préparer | `crm:campagne:destinataires {segment} {fichier}` | Écrit un fichier des **adresses autorisées**. Écarte : non diffusibles, entreprises fermées, entrepreneurs individuels, adresses invalides ou non vérifiées, adresses grand public, opposition ou suppression, adresses de cabinet partagées. N'écrit rien en base. Segments en **liste fermée**. | **C1** (une seule porte d'envoi), C3, S6, P2 | **élevé** (toutes les gardes légales actuelles sont ici) |
| 3. Envoyer | outil externe | — | E1, C2 (« envoi fait à la main ») | — |
| 4. Retours | `crm:campagne:retours {fichier} [--dry-run]` | Lit les retours : `envoye` (pose la date de premier message, art. 14), `desinscription`/`plainte` (opposition définitive), `rebond_dur`, `rebond_mou` (seuil 3). Ne fait que **retirer**, jamais ajouter. | **E5** (devient une simple source d'import), J1 | **élevé** |

**Règle d'éligibilité centrale** : `EligibiliteCampagne::peutRecevoir` (opposition + suppression). Une garde existante (`AucunEnvoiSansEligibiliteTest`) impose de passer par elle. Le moteur C1 **doit** l'appeler, pas la recopier.

**Attention** : le compteur des rebonds mous vit en cache, hors transaction. Rejouer un fichier de retours le recompte.

---

## 7. Canaux signés avec le site et les partenaires

| Canal | Sens | Protection (catégorie) | État | Lot à risque | Risque |
|---|---|---|---|---|---|
| `POST /api/internal/site-sync` | site → CRM | signature HMAC avec horodatage dans le corps, secret vide = porte fermée, limiteur | **503 tant que `CRM_INGEST_ENABLED` est éteint** | ADR consoles, P4 (canal unique), S7 | **élevé** |
| `POST /api/internal/site-sync/gdpr` | site → CRM | même signature | même drapeau | S7 (RGPD par espace), P4 | **élevé** (droits d'accès et d'effacement sur les deux systèmes) |
| `crm:flush-outbound` (table `crm_outbound_events`) | CRM → site | — | sautée tant que `CRM_OUTBOUND_ENABLED` est éteint | ADR consoles | **élevé** |
| `POST /api/internal/partners/v1/ping` | partenaires → CRM | signature v2, anti-rejeu, idempotence, corps borné | **404 tant que `CRM_PARTNERS_MODE=off`** ; une seule route technique | P4 (à fusionner en un seul canal) | moyen |
| `POST /api/internal/email/zeptomail` | courrier transactionnel → CRM | jeton partagé | 503 sans jeton | S2, E5 | moyen |
| `POST /api/internal/scraper-result` | collecteurs → CRM | même classe de signature | actif | S7 | moyen |

Types d'événements reçus du site : formulaires, inscription et désinscription à la lettre, demande du guide, consentements. La classe de signature `HmacSignature` est **le patron à réutiliser** pour P4 (le code le dit lui-même).

---

## 8. Migrations (`backend/database/migrations`)

- **122 migrations**, de mai à fin octobre 2026.
- **Toutes** ont une fonction de retour.
- **9 ont un retour vide** (correctifs de données ou de contraintes) : retour arrière impossible sans restauration.
- **14 refusent volontairement le retour** (isolation, empreintes d'opposition, presse, fédérations, INSEE, etc.) : c'est voulu (on ne remet pas des adresses en clair), mais il faut le savoir.
- La migration d'ébauche de mai crée ses tables en SQL brut (pas en schéma Laravel).
- Le déploiement de production lance `migrate` **à chaque fusion**.

**Lots à risque** : P2 (ajout de `workspace_id` sur l'opposition), S7 (tables sans `workspace_id`, RLS), S8 (horodatages), E3, C1, Q1. **Risque : élevé** : une migration ratée part en production toute seule.

**Règle du plan 20 (§ 11.1)** : toute nouvelle migration doit être **réversible**, et testée dans les deux sens.

---

## 9. Routes API et écrans (`frontend/src/app/routeTree.tsx`)

**54 routes d'écran** dans le frontend. Côté serveur, ≈ 190 routes sous `/api/v1` (dont le groupe `/v1/crm/*` réservé à la console CRM), plus 6 routes internes signées.

### 9.1 Écrans qui ont leur serveur (ce qui marche)

Entreprises (liste, fiche), contacts (liste), fédérations, événements, doublons, listes manuelles, presse (médias, journalistes, envois presse), couverture, passages de collecte, routeur et fournisseurs du modèle de langage, demandes RGPD, AI Act, journal d'audit, utilisateurs, réglages, **campagnes de collecte** (`/campaigns`), étiquettes, audiences, observabilité, console (contacts, vivier, arbitrage, propositions, personnes, lettre et guide), connexion, 2FA, lien magique, mot de passe oublié.

### 9.2 Routes serveur prêtes **sans écran**

| Route serveur | Ce qui manque | Lot qui doit la brancher |
|---|---|---|
| `saved-views` (vues sauvegardées) | aucun écran ne l'appelle | U0 (contrat d'API), Q2 |
| `PUT` et `DELETE /contacts/{id}` | l'écran Contacts ne fait que lister | U0, **Q1** |
| `POST /v1/crm/bulk` (action de masse) | non appelée | U0, Q1b |
| `/v1/crm/candidates` | à peine appelée | à vérifier |

### 9.3 Écrans « vides » ou d'attente

`/cold-email`, `/linkedin`, `/crm`, `/analytics`, `/pas-encore-livre` : pages d'attente ; côté serveur, `/cold-email` et `/linkedin` répondent par un contrôleur d'attente. Lots à risque : C1, U2-U9 (les remplacer sans laisser de lien mort).

### 9.4 Le conflit du mot « campagnes »

`/campaigns`, `/campaigns/new`, `/campaigns/$campaignId` et l'API `/v1/campaigns` = **campagnes de collecte** (table `scraping_campaigns`). Le lot **C1** crée des campagnes d'**e-mails**. Il faut **renommer d'abord** (ex. « Collectes »), avec redirection de l'ancienne adresse et test de route (plan 20, § 11.5). **Risque : élevé.**

### 9.5 Pas de contrat d'API

Les types du frontend sont écrits à la main. Aucun test ne vérifie qu'un champ renvoyé par le serveur est celui qu'attend l'écran. Lot qui le pose : **U0** (§ 11.3 du plan 20).

---

## 10. Vérités à vérifier en exécution (par un agent, plus tard)

Ce relevé n'a rien exécuté. Les points suivants **doivent être mesurés** avant ou pendant R0, sur une copie locale ou en préproduction, **jamais en écrivant en production**.

1. **Liste réelle des tâches planifiées** : `php artisan schedule:list` (attendu : 44 tâches + le battement).
2. **Valeur réelle de chaque drapeau** (`MOCK_*`, `CRM_*`) en production et en préproduction (lecture de la config chargée, sans afficher les secrets).
3. **Le rôle applicatif et la RLS** sont-ils armés en production (`CRM_DB_APP_ROLE_ENABLED`) ? Quelles tables ont la barrière active ?
4. **Tâches planifiées sous RLS** : chacune rend-elle le même nombre de lignes sous le rôle de production que sans ? (rejeu en préproduction).
5. **Tables d'ébauche** : existent-elles vraiment dans la base de production (`unsubscribes`, `dnc_entries`…) ? Contiennent-elles des lignes ?
6. **Contenu réel de l'export RGPD** d'une personne factice : liste des tables qu'il lit (pour le test « rien ne disparaît »).
7. **Liste réelle des routes** : `php artisan route:list --json`, puis comparaison automatique avec les appels du frontend.
8. **Les 9 migrations au retour vide et les 14 qui refusent** : liste confirmée par un `migrate:rollback` sur une base jetable.
9. **La suite de tests passe-t-elle aujourd'hui** sur `main` (Pest, Vitest, e2e) ? Combien de tests en quarantaine (`QUARANTAINE.md`) ?
10. **Protection de la branche `main`** sur GitHub : quels contrôles sont « obligatoires » pour fusionner ? (impossible à lire depuis le code).
11. **Le décalage de 2 h** (S8) : où naît-il ? (le fuseau par défaut est Paris dans la config ; le décalage vient sans doute d'une colonne sans fuseau ou du frontend).
12. **Les workflows qui purgent** (`prospection-reclassify`, `prospection-collect-region`) : ont-ils tourné récemment ? Combien de fiches ont-ils supprimées ?
13. **Les canaux signés** : le site envoie-t-il déjà des événements (503 reçus ?), et le canal Partners est-il bien à `off` ?
14. **`MOCK_MAIL`, `MOCK_IGN`, `MOCK_RPPS`** passent-ils par la même garde de production que les autres simulateurs ?
15. **La 2FA actuelle** (code TOTP) : quels comptes l'utilisent ? (pour le test de connexion de bout en bout qui doit rester vert jusqu'à S12).
16. **La copie locale du CRM** utilisée par les agents est-elle à jour (fusions #384 à #386 et suivantes) ?

---

## 11. Synthèse des risques élevés (renvoi vers le fichier 22)

| N° | Élément | Lot qui le menace |
|---|---|---|
| R1 | Tâches planifiées muettes sous RLS | S7 |
| R2 | Garde Sirene / non diffusibles / INSEE | C3, S7 |
| R3 | Opposition et suppression (`opt_out`, `email_suppressions`) | P2, C1, E5 |
| R4 | Gardes de la préparation des destinataires | C1, S6 |
| R5 | Retours de campagne (désinscription, plainte, rebonds) | E5 |
| R6 | Canaux signés avec le site (signature, drapeaux, RGPD) | P4, ADR consoles |
| R7 | Synchro CRM → site et dossier client | ADR consoles |
| R8 | Purges (drapeau éteint, décision « pas de purge ») | S9, J3, workflows de collecte |
| R9 | Simulateurs en production | S2, P1, E1 |
| R10 | Migrations automatiques en production | P2, S7, S8, toutes |
| R11 | Déploiement et sauvegarde | S9, S11 |
| R12 | Collision « campagnes » | C1 |
| R13 | Export RGPD complet | P2, S7 |
| R14 | Connexion et 2FA actuelles | S1, S3 |
| R15 | Journal d'audit et partitions | S7, S9 |
| R16 | Segments fermés par défaut | S6 |
