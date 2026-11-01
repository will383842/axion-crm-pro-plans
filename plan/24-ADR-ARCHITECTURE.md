# 24 : Décisions d'architecture (ADR) : isolation, envoi, consoles (01/11/2026)

**Lot P1.** Ce fichier fixe les choix d'architecture avant tout code. Il complète `20-PLAN-CORRIGE-UNIQUE.md` (§ 3, 9, 10, 11). **RIEN N'EST CODÉ.**

Rédigé en lecture seule. Sources : plans `01`, `02`, `03`, `05`, `16`, `20` ; relevé du code de `axion-crm-pro` (dernière fusion lue : #386). Aucun secret, aucune IP, aucune donnée de personne n'est recopié ici. Seuls des **noms** de variables et de fichiers sont cités.

**Décisions de Will déjà prises (non reposées)** : rien d'Axion en dur ; `workspace_id` sur toutes les tables d'envoi, opposition et suppressions comprises ; aucune suppression de données de personnes ; Axion est un client parmi d'autres ; pas de marque blanche ; entité d'envoi = SAS française ; KumoMTA, repli Postfix + rspamd ; facturation dans le Hub de la console.

**Format de chaque ADR** : contexte, options, **recommandation**, conséquences, retour arrière, question pour Will (si besoin).

**Vocabulaire figé** (pour tout le code et tous les plans) :
- **espace** = `workspace` = le client du CRM (Axion est un espace). Le mot « tenant » n'est **jamais** utilisé dans le CRM.
- **groupe d'envoi** = ce que KumoMTA appelle « tenant ». Il est imposé par l'identité de connexion SMTP, jamais lu dans un en-tête.
- **console du site** = la console d'administration du site Axion-IA (dossier client, devis, Hub de facturation).
- **console des automatisations** = la console qui vend et pilote les automatisations, dont le CRM Pro en V1.

---

## Ce qui existe déjà (relevé du code, à ne pas casser)

| Sujet | État réel | Fichiers |
|---|---|---|
| Isolation | RLS posée et forcée sur les tables à `workspace_id`, prédicat strict sur `app.current_workspace_id`. **Mais** l'application se connecte par défaut avec un rôle qui contourne la RLS. Le rôle applicatif ne sert que si `CRM_DB_APP_ROLE_ENABLED=true` (défaut `false`). | `2026_08_14_000001_harden_workspace_isolation.php` ; `config/database.php` ; `config/crm.php` |
| Contexte d'espace | Middleware `SetCurrentWorkspace`, `WorkspaceContext::run()` ; trait `RunsInWorkspace` pour les jobs ; scope Eloquent inerte tant que `CRM_STRICT_WORKSPACE_SCOPE=false`. | `app/Support/WorkspaceContext.php` ; `app/Jobs/Concerns/RunsInWorkspace.php` |
| Tâches planifiées | ≈ 45 entrées dans `routes/console.php`. **44 commandes sur 98** posent un contexte d'espace. Les autres ne marchent que parce que la RLS est contournée. | `routes/console.php` |
| Opposition et suppressions | `opt_out` et `email_suppressions` sont **globales** (pas de `workspace_id`, seulement un `scope`). | migrations `2026_05_16_000005`, `2026_08_14_000004`, `2026_08_15_000004` |
| Canal du site | `POST /internal/site-sync` (+ `/gdpr`) signé HMAC (`X-Site-*`), idempotence par `event_id`. Sens sortant : `crm:flush-outbound` (oppositions et effacements seulement). Tout fermé par drapeaux. | `SiteSyncController.php` ; `CanalSigneSite.php` ; `ConsentOutboundRecorder.php` |
| Canal Partners | `POST /internal/partners/v1/ping` seul, signé (`X-Partners-*`, clé identifiée, clé d'idempotence, anti-rejeu, secret par sens). Fermé (`CRM_PARTNERS_MODE=off`). | `VerificateurCanalPartners.php` |
| Identifiant client | `companies.console_client_ref` au format `site:client:<uuid>`, index unique. **`console_client_id` n'existe pas dans le CRM.** | `2026_10_25_000010_synchro_dossier_client.php` ; `DossierClientIngest.php` |
| Tâches, notes, affaires | Tâches = `activities` (`kind='task'`). Tables `deals`, `pipeline_stages`, `crm_tasks`, `crm_notes`, `crm_pipelines`… = ébauches sans modèle. | `Taxonomy.php` ; migrations « scaffold » |
| « Campagnes » | `/campaigns` = campagnes de **collecte** (scraping), table `scraping_campaigns`. Les envois passent par une commande qui produit un fichier pour un outil externe. | `ScrapingCampaign.php` ; `routeTree.tsx` ; `CrmCampagneDestinataires.php` |
| Contrat d'API | `l5-swagger` installé, annotations partielles, aucune description générée, aucun type TypeScript généré, aucun test de contrat. | `composer.json` ; `config/l5-swagger.php` |
| Drapeaux | Variables `CRM_*` dans `config/crm.php`, lues par le front via `FeaturesController`. Pas de Pennant. | `config/crm.php` |

---

## ADR-01 : Isolation entre clients (RLS, rôle de base, ordre de bascule)

**Contexte.** La barrière RLS est écrite mais pas armée : le rôle par défaut la contourne. Plus de la moitié des commandes planifiées ne posent pas de contexte d'espace. Si on arme la RLS d'un coup, ces commandes verront zéro ligne (ou échoueront en écriture) : la synchro du site, les purges gardées, l'INSEE, l'audit pourraient s'arrêter sans bruit.

**Options.**
- A. Armer la RLS en une fois (changer le rôle en production).
- B. Armer par étapes, avec un relevé et un rejeu sous le rôle de production en préproduction.
- C. Garder l'isolation seulement dans le code (scope Eloquent), sans RLS.

**RECOMMANDATION : B.** Deux barrières : RLS (base) **et** scope strict (code). Ordre de bascule :
1. **Relevé (R0)** : liste de toutes les commandes, jobs et entrées de synchro, avec leur besoin : « un espace », « tous les espaces », « plateforme (sans espace) ».
2. **Rôle plateforme dédié** pour les seules tâches transverses (audit, référentiels INSEE/FINESS, battement) : un rôle séparé, listé, journalisé. Jamais le superutilisateur.
3. **Mise en conformité** : chaque commande « un espace » passe par `WorkspaceContext::run()` ; chaque commande « tous les espaces » boucle espace par espace (`--all-workspaces`) ; une garde CI refuse une nouvelle commande sans déclaration.
4. **Préproduction sous le rôle applicatif** : rejouer toutes les tâches planifiées et des entrées de synchro réelles **anonymisées** ; comparer les compteurs avec la production.
5. **Suite « deux clients factices »** bloquante en CI, exécutée sous le rôle applicatif (aujourd'hui `RlsTest` ne peut pas).
6. **Production** : `CRM_DB_APP_ROLE_ENABLED=true`, puis 48 h plus tard `CRM_STRICT_WORKSPACE_SCOPE=true`.
7. **Démarrage refusé** en production si la RLS n'est pas armée (après l'étape 6 seulement).

**Conséquences.** ≈ 1 à 2 j de plus dans S7 pour le relevé et la mise en conformité des commandes. Les tests tournent sous le vrai rôle. Les tables globales (référentiels) gardent une policy de lecture explicite.

**Retour arrière.** Remettre `CRM_DB_APP_ROLE_ENABLED=false` (un redémarrage, aucune migration). Le scope strict a son propre drapeau. Aucune donnée n'est modifiée par la bascule.

**Question pour Will :** _aucune_ (décision technique ; Will a déjà demandé l'isolation complète).

---

## ADR-02 : Modèle de données multi-espace (envoi, opposition, base sectorielle)

**Contexte.** `opt_out` et `email_suppressions` sont globales. Or l'opposition d'un prospect au client A ne doit pas bloquer le client B, sauf cas de sécurité (piège à spam, adresse invalide, plainte). Il faut aussi la base sectorielle (ex. pharmacies) attribuée à un client sans la lui donner.

**Options pour l'opposition.**
- A. Tout global (aujourd'hui) : faux, un client bloque les autres.
- B. Tout par espace : une adresse piège blessera chaque client l'un après l'autre.
- C. **Par espace + une liste globale de sécurité** réduite.

**RECOMMANDATION : C.**
- **Toutes les tables d'envoi** portent `workspace_id NOT NULL` avec RLS : domaines, IP attribuées, boîtes, gabarits, campagnes, étapes, envois, événements, réponses, règles de contenu, quotas, identité légale.
- **`opt_out` et `email_suppressions`** reçoivent `workspace_id`. Migration **sans perte** : les lignes existantes vont dans l'espace Axion (elles viennent toutes d'Axion). L'empreinte (`email_hash`) reste la clé de comparaison.
- **Liste globale de sécurité** (`suppression_plateforme`, sans `workspace_id`, écrite par la plateforme seulement) : pièges connus, domaines invalides, rebonds durs « adresse inexistante », plaintes authentifiées. Elle bloque **tous** les espaces. Elle ne contient **jamais** une simple désinscription commerciale.
- **Règle d'éligibilité unique** : envoi permis seulement si l'adresse n'est ni dans l'opposition de l'espace, ni dans la liste de sécurité, ni dans l'opposition de la base sectorielle (si la fiche vient d'une base).
- **Base sectorielle** (lot K12) :
  - `fiches_reference` (plateforme, lecture seule pour les espaces) ;
  - `attributions_base` (secteur, espace, début, fin, motif, auteur) : un retrait coupe l'accès, ne supprime rien ;
  - `surcouche_fiche` par espace (étape, notes, étiquettes, champs, tâches) ;
  - **double opposition** : « ne plus être contacté par ce client » (opposition de l'espace) et « ne plus figurer dans la base d'Axion » (`opposition_reference`, respectée par tous les espaces attribués, la fiche reste gardée avec son empreinte, sans suppression).
- **Axion** est un espace ordinaire : aucune ligne spéciale, aucun identifiant en dur. Les réglages propres à Axion (presse ouverte, règles de Will) sont des **lignes de réglage** datées dans son espace.

**Conséquences.** P2 grossit un peu (migration des deux tables + liste de sécurité, ≈ +1 j). Les tests « l'opposition de A ne bloque pas B » et « un piège bloque tout le monde » deviennent bloquants.

**Retour arrière.** La migration ajoute des colonnes et une table ; la descente retire la colonne après recopie. Tant que le drapeau du module d'envoi est éteint, l'ancienne lecture globale reste la seule utilisée.

**Question pour Will (oui/non) :** une **plainte authentifiée** reçue par un client bloque-t-elle l'adresse **pour tous les clients** ? **Recommandation : oui** (elle protège les serveurs de tous).

---

## ADR-03 : Contrat unique `ServeurEnvoi`

**Contexte.** Le CRM ne doit jamais dépendre de KumoMTA. Le contrat est décrit dans `03 § 10` (9 opérations, un événement normalisé, des invariants). Aujourd'hui, le CRM produit un fichier pour un outil externe et relit les retours par une commande.

**Options.**
- A. Appeler KumoMTA directement.
- B. **Interface `App\Emailing\ServeurEnvoi` + kit de conformité**, plusieurs réalisations.

**RECOMMANDATION : B.**
- Réalisations : `Simulation` (CI, préproduction, essai à blanc), `KumoMta` (V0), `Postfix` (repli, lot E10), et éventuellement `RelaisTiers` (secours temporaire, décision 41).
- Le même **kit de conformité** (tests) passe sur chaque réalisation. Une réalisation qui échoue n'est pas branchée.
- Aucun écran, aucune table, aucun libellé ne nomme le moteur. Le choix est un réglage par **serveur** en base.
- Le groupe d'envoi est imposé par l'identifiant SMTP du serveur (un identifiant par espace et par groupe). Un en-tête de routage reçu est ignoré.
- Les retours arrivent tous par **un seul** service `AppliquerRetour`, avec l'événement normalisé. L'ancienne commande de retours devient une **source d'import** de ce service.
- ZeptoMail reste hors du contrat (codes et e-mails techniques seulement).

**Conséquences.** Changer de moteur = écrire une réalisation + passer le kit, sans toucher au CRM (8 à 15 j estimés pour Postfix).

**Retour arrière.** Chaque serveur a sa réalisation en base : revenir à `Simulation` coupe tout envoi réel en une ligne.

**Question pour Will :** _aucune_ (déjà décidé : KumoMTA, repli Postfix).

---

## ADR-04 : Accord avec les deux consoles

### 4.1 Nommer les deux consoles

| Nom figé | Ce qu'elle fait | Lien avec le CRM |
|---|---|---|
| **Console du site** (console d'administration du site Axion-IA) | formulaires, questionnaire, rendez-vous, **dossier client** (rencontre, projet, devis, suivi), **Hub** (factures, Stripe) | envoie des fiches et le dossier client ; reçoit oppositions, effacements et retouches de fiche |
| **Console des automatisations** | vend les automatisations, dont le CRM Pro en V1 ; crée les clients, active les options, porte l'abonnement | pilote les espaces ; reçoit usage, santé, version, alertes |

### 4.2 Un seul canal signé

**Contexte.** Deux canaux existent déjà : site-sync (HMAC sur `ts.body`, sans clé identifiée, un seul secret pour les deux sens) et Partners (clé identifiée, signature sur méthode + chemin + clé d'idempotence + corps, secret par sens, anti-rejeu). Le lot P4 en prévoyait un troisième.

**Options.** A. Garder trois canaux. B. **Un seul format de canal signé**, avec un émetteur par console.

**RECOMMANDATION : B.** Le format de Partners devient le **format unique** (« canal signé v2 ») :
- en-têtes : horodatage, identifiant de clé, clé d'idempotence, signature ;
- signature sur horodatage + méthode + chemin + clé d'idempotence + corps ;
- un secret **par émetteur et par sens**, rotation par identifiant de clé (deux clés valides pendant la rotation) ;
- anti-rejeu (fenêtre de 5 min + mémoire des clés d'idempotence en base) ;
- émetteurs déclarés : `console-site`, `console-automatisations`, `partners`.
- **Migration sans casse** : site-sync accepte les deux formats pendant une période, derrière un drapeau ; le site bascule ; puis l'ancien format est refusé. Le chemin `/internal/site-sync` reste, il change seulement de vérificateur.
- P4 devient « canal signé v2 » : il **fusionne** site-sync et Partners au lieu d'en créer un nouveau.

### 4.3 Un seul identifiant client

**Contexte.** Le CRM utilise `console_client_ref` (texte `site:client:<uuid>`, unique, déjà en production côté code). Le nom `console_client_id` vient d'ailleurs (probablement le cahier de la console) ; il n'existe pas dans le CRM.

**RECOMMANDATION : garder `console_client_ref`** comme seul nom dans le CRM. Format : `<console>:client:<uuid>` (`site:client:…` aujourd'hui ; `auto:client:…` si la console des automatisations a ses propres clients). Côté console, l'UUID reste la clé interne ; le texte complet est ce qui circule. Une seule table de correspondance si un jour deux formats coexistent. **Aucun nouvel identifiant.**

Distinction à ne pas mélanger : `console_client_ref` désigne **un client d'Axion dans la fiche entreprise**. L'espace (client du CRM en V1) porte, lui, `console_espace_ref` (posé par la console des automatisations à la création).

### 4.4 Qui possède quoi

| Donnée | Propriétaire | L'autre côté |
|---|---|---|
| Dossier client (rencontre, projet, devis, suivi) | **console du site** | le CRM affiche un résumé en lecture et un lien |
| Factures, abonnement, paiement | **Hub de la console** | le CRM reçoit l'état d'abonnement |
| Tâches, notes, appels, affaires **de prospection** | **CRM** | non envoyés à la console |
| Tâches et notes **d'un client signé** (après devis) | **console du site** | le CRM ne les recrée pas |
| Identité et coordonnées de la fiche | partagées | synchro dans les deux sens (§ 4.7) |
| Étape commerciale | **CRM** jusqu'à « gagné » ; la console pose « client » | « le plus récent gagne » |
| Opposition RGPD | **les deux** | l'opposition gagne partout |

### 4.5 Connexion d'un client en V1

**Options.** A. Comptes séparés dans le CRM (e-mail + code). B. Connexion unique depuis la console des automatisations.

**RECOMMANDATION : A en V1.** Le client reçoit une invitation du CRM, se connecte avec son e-mail et le code par e-mail (2FA déjà prévue). La console affiche seulement un lien « Ouvrir le CRM ». Aucune session partagée, aucun jeton de la console accepté pour se connecter. Plus simple et plus sûr ; la connexion unique pourra venir plus tard.

### 4.6 Fin de client

**RECOMMANDATION.** La console envoie un état : `actif`, `suspendu`, `resilie`. Effets :
- `suspendu` : envoi en pause, lecture gardée, rien supprimé ;
- `resilie` : l'espace passe en **dormant** (lecture seule, export disponible, envoi coupé) ; jamais supprimé ;
- côté fiche d'Axion : un client qui part passe à l'étape **perdu** ou **dormant**, jamais supprimé ;
- seule exception : suppression **sur ordre écrit du client** (art. 28, décision 31), exécutée par un humain d'Axion avec journal.

### 4.7 Synchro du dossier client dans les deux sens

**RECOMMANDATION.** Garde-fous (règles du 25/10) codés et testés :
1. **Le plus récent gagne**, champ par champ, par horodatage de la source ; l'ancienne valeur va à l'historique.
2. **Aucune suppression ne se propage** dans aucun sens.
3. **L'opposition RGPD gagne partout** : elle passe toujours, même si l'autre valeur est plus récente.
4. **Aucune purge** des fiches venues de la console (étiquette protégée `src:console-client`, déjà en place).
5. Jamais de montant, jamais le texte des réponses au questionnaire.
6. Chaque message est idempotent et rejouable ; écran « Santé de la synchro ».
7. Sens CRM → console ouvert derrière un drapeau, éteint par défaut, après un essai de bout en bout en préproduction.

**Retour arrière (ADR-04 en entier).** Chaque sens et chaque émetteur a son drapeau. Fermer un drapeau = les messages attendent dans la file, rien n'est perdu.

**Question pour Will (A/B) :** connexion d'un client en V1 : **A = compte propre dans le CRM (recommandé)**, B = connexion unique depuis la console.

---

## ADR-05 : Tables d'ébauche existantes

**Contexte.** ≈ 35 tables « phase 2 » créées sans modèle : `deals`, `pipeline_stages`, `crm_tasks`, `crm_notes`, `crm_pipelines`, `crm_lost_reasons`, `campaigns`, `email_templates`, `email_sequences`, `email_sends`, `unsubscribes`, `dnc_lists`/`dnc_entries`, `email_inboxes`/`threads`/`messages`, `linkedin_*`, `analytics_*`… Certaines sont **lues par l'export RGPD** (`unsubscribes`, `dnc_entries`, `email_messages`). Le code se contredit (`EligibiliteCampagne.php` dit que `dnc_entries` et `unsubscribes` n'existent pas).

**Options.** A. Tout réutiliser. B. Tout supprimer. C. **Arbitrer table par table.**

**RECOMMANDATION : C, sans jamais supprimer une table qui contient une ligne.**
- **Réutiliser** (les noms et colonnes sont adaptés par migration) : `deals` + `pipeline_stages` (affaires, Q2) ; `crm_lost_reasons` (motifs de perte).
- **Ne pas réutiliser, garder en lecture puis retirer** : `campaigns`, `email_templates`, `email_sequences`, `email_sends`, `email_inboxes/threads/messages` (le module d'envoi crée ses propres tables sous `Emailing`) ; `crm_tasks`, `crm_notes` (les tâches et notes restent dans `activities`) ; `unsubscribes`, `dnc_*` (remplacées par l'opposition par espace de l'ADR-02) ; `linkedin_*`, `analytics_*` (hors plan).
- **Méthode de retrait** : 1) compter les lignes en production ; 2) si non vide : copier dans la table cible, puis garder l'ancienne en lecture 90 jours ; 3) retirer la table de l'export RGPD **dans la même fusion** que son remplacement ; 4) retirer la table seulement après.
- **Test d'export RGPD obligatoire** : sur un jeu factice, l'export « avant » et « après » contient **les mêmes données** (mêmes personnes, mêmes champs, au besoin sous une autre clé). Le test échoue si une donnée disparaît de l'export.

**Conséquences.** ≈ 1 j dans R0 (comptes et liste) ; le reste suit chaque lot qui remplace une table.

**Retour arrière.** Rien n'est supprimé avant 90 jours ; la migration de descente remet l'export.

**Question pour Will :** _aucune_.

---

## ADR-06 : Contrat d'API entre écrans et serveur

**Contexte.** Le front et le serveur ne partagent aucun type. `l5-swagger` est installé mais partiel. Rien n'empêche un champ de diverger.

**Options.** A. Annotations `l5-swagger` complétées. B. **Description OpenAPI écrite à la main dans le dépôt**, source unique. C. Types écrits à la main côté front.

**RECOMMANDATION : B, avec l'outil déjà présent seulement pour l'affichage.**
- Fichier `backend/openapi/crm.yaml` versionné, une section par module.
- Types TypeScript **générés** dans le front (`api.generated.ts`) ; schémas `zod` générés pour valider les réponses en développement.
- **Test de contrat en CI** : chaque route décrite est appelée dans les tests serveur et sa réponse est validée contre la description ; la CI échoue si un champ manque ou change de type, ou si le fichier généré n'est pas à jour.
- Nouvelle route = description d'abord, puis code (garde CI : route sans description refusée, sauf liste d'exceptions qui ne fait que diminuer).
- Ordre : d'abord les routes déjà prêtes sans écran (contacts, vues sauvegardées, actions de masse), puis chaque nouveau lot.
- Les canaux internes (consoles) ont **leur propre** description, séparée.
- La documentation d'API n'est **pas** publiée en production (S11).

**Conséquences.** ≈ 5 j dans U0 (déjà prévu au § 11 du plan 20).

**Retour arrière.** Le test de contrat peut passer en « avertir » au lieu de « bloquer » par un réglage de CI, le temps d'une correction.

**Question pour Will :** _aucune_.

---

## ADR-07 : Renommer les campagnes de collecte avant les campagnes d'e-mails

**Contexte.** Le mot « campagnes » et l'adresse `/campaigns` désignent aujourd'hui la **collecte** (scraping). Le lot C1 crée les **campagnes d'e-mails**. Deux sens pour un mot = confusion et routes en collision.

**RECOMMANDATION.**
- Renommer côté écrans : « Collectes » ; adresses `/collectes`, `/collectes/new`, `/collectes/$id`.
- **Redirection** permanente de `/campaigns…` vers `/collectes…` pendant 6 mois, avec un test de route.
- Côté API : nouvelles routes `/collectes`, anciennes gardées comme alias puis retirées.
- Le nom de table `scraping_campaigns` **ne change pas** (pas de migration risquée).
- **Ordre** : ce renommage est fusionné **avant** la première route du lot C1. Les campagnes d'e-mails prennent ensuite « Campagnes » et `/campagnes`.

**Retour arrière.** Les redirections et alias suffisent ; aucune donnée touchée.

**Question pour Will (oui/non) :** le mot **« Collectes »** pour l'ancienne fonction vous va ? **Recommandation : oui.**

---

## ADR-08 : Drapeaux éteints par défaut et retour arrière par lot

**Contexte.** Les drapeaux existent déjà (`CRM_*` dans `config/crm.php`). Il manque une règle commune.

**RECOMMANDATION.**
- Toute nouveauté est derrière un drapeau, **éteint par défaut** (absence = éteint).
- Deux niveaux : **plateforme** (variable `CRM_*`, pour les bascules techniques) et **espace** (table `fonctions_espace`, pour les options d'un client : envoi, téléphone, base sectorielle…).
- Pas de nouvelle bibliothèque : on garde `config/crm.php` et `FeaturesController`.
- **Démarrage refusé en production** si un simulateur est allumé (`MOCK_MODE`, `MOCK_MAIL`) alors que l'envoi réel est actif.
- Chaque lot livre une **ligne de retour arrière** dans sa description : quel drapeau fermer, quelle migration descendre, combien de temps.
- Migrations **réversibles** et **compatibles avec la version précédente** (ajouter d'abord, retirer ensuite, jamais dans la même fusion).
- Suite **« ne doit pas régresser »** (lot R0) bloquante pour tous les lots.
- Un drapeau ouvert depuis 60 jours sans incident est retiré du code (dette suivie).

**Retour arrière.** Par construction : fermer le drapeau.

**Question pour Will :** _aucune_.

---

## Questions pour Will (résumé)

| # | Question | Recommandation |
|---|---|---|
| Q1 (ADR-02) | Une plainte authentifiée chez un client bloque l'adresse pour tous les clients ? | **Oui** |
| Q2 (ADR-04) | Connexion d'un client en V1 : A = compte propre dans le CRM, B = connexion unique depuis la console ? | **A** |
| Q3 (ADR-07) | Le mot « Collectes » pour les anciennes campagnes de collecte ? | **Oui** |

---

## Limites

- **Dépôt du site Axion-IA non lu** : il n'est pas dans l'accès de cette session. Je n'ai donc pas vu le cahier de la console, le nom `console_client_id`, ni le format réel des messages côté site. L'ADR-04 doit être relu contre ce dépôt avant le lot de synchro.
- **Console des automatisations non lue** : son cahier (canal signé prévu, création de client) n'est pas dans les dépôts accessibles.
- **Production non mesurée** : l'état réel de `CRM_DB_APP_ROLE_ENABLED`, des drapeaux de synchro et des simulateurs est inconnu (mesure prévue en S1/S2, décision 13).
- **Nombre de lignes des tables d'ébauche inconnu** : il faut le compter en production (R0) avant tout retrait.
- **Code lu, rien exécuté** : constats tirés d'une lecture par un agent ; les numéros de ligne peuvent bouger avec les prochaines fusions.
- Le CRM local lu s'arrête à la fusion #386.
