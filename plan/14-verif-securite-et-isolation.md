# 14 : Vérification sécurité et isolation du plan « CRM Pro complet » (01/11/2026)

Rapport du responsable sécurité et isolation. Lecture seule : aucun code applicatif écrit, rien envoyé, aucun serveur touché. Le code relu est celui de `axion-crm-pro` au commit de tête du 01/11/2026.

**Règle de publication (dépôt public).** Ce fichier ne contient aucune valeur de secret, aucun numéro de ligne et aucune recette d'exploitation. Les failles non corrigées sont décrites par catégorie et par nom de fichier. Le détail technique (lignes, enchaînements) est dans le rapport privé du responsable, hors dépôt, à transmettre à l'équipe de correction par un canal privé.

Certitude :
- **[C]** : vu dans le code ou la configuration du dépôt.
- **[S]** : supposé, à vérifier sur le serveur (état réel des variables de production).

---

## 0. Verdict en une phrase

**Aucun client ne peut être accueilli aujourd'hui**, ni en mode mutualisé, ni même en instance dédiée sans les correctifs V0 du § 6.

Six points bloquent :
1. La barrière d'isolation Postgres (RLS) est écrite et testée, mais **inactive par défaut** : l'application se connecte avec un rôle qui la contourne.
2. Les traitements RGPD (export et effacement) **traversent les espaces**.
3. La 2FA est **contournable avec le seul mot de passe**.
4. Un admin peut **se nommer owner**.
5. L'action de masse de la console CRM n'a **aucune permission**.
6. Les courriels d'authentification sont configurés de façon à pouvoir **finir dans les journaux**.

---

## 1. Failles déjà signalées : état au 01/11

| # | Faille signalée | État | Fichiers concernés | Catégorie |
|---|---|---|---|---|
| F1 | 2FA contournable avec le seul mot de passe | **[C] TOUJOURS OUVERTE** | `EnsureTwoFactorPassed.php`, `TwoFactorController.php`, `TwoFactorService.php` | Authentification : le flux d'enrôlement n'est pas protégé par la 2FA déjà active. Pas d'anti-rejeu TOTP. Limiteur par IP seulement, pas par compte. |
| F2 | Modification en masse sans permission | **[C] OUVERTE** | `routes/api.php` (groupe console CRM), `Crm/BulkController.php` | Autorisation par route absente. Contrôle insuffisant des étiquettes protégées. `CompanyTagsBulkController` est, lui, correctement protégé. |
| F3 | Un admin peut nommer un owner | **[C] OUVERTE** | `UsersController.php`, `PermissionsAndRolesSeeder.php` | Élévation de privilège horizontale : aucune hiérarchie de rôles, pas de refus de l'auto-modification, un owner peut être rétrogradé ou fermé par un admin. |
| F4 | Segments sensibles ouverts quand la configuration est vide | **[C] OUVERTE (par choix documenté)** | `Segments.php`, `config/crm.php`, `.env.example` | Ouverture par défaut (« fail-open ») : une variable vide ou perdue rouvre tous les segments, presse comprise. Aucun segment « santé » dans la liste ; la donnée santé est marquée ailleurs (`app/Crm/Sante/*`) [S]. |
| F5 | Courriels d'authentification mal configurés | **[C] OUVERTE, aggravée** | `infra/scripts/configure-prod-env.sh`, `config/mail.php`, `MagicLinkService.php`, `PasswordResetController.php` | Configuration du transport d'authentification incohérente avec son commentaire ; risque de données d'authentification dans les journaux centralisés. Valeur réelle sur le serveur : [S]. |
| F6 | Secrets dans le dépôt | **[C] Aucun secret actif trouvé** | divers | Clone partiel : à rejouer sur l'historique complet. Constats : `.env.example` seulement, une clé de test factice, une mention documentaire de PEM. En revanche, **l'IP publique du serveur de production est commitée** dans plusieurs scripts et un README de `infra/scripts/`. Ce n'est pas un secret, mais c'est contraire à la règle « aucune IP dans le dépôt ». |

## 2. Autres failles trouvées

| # | Gravité | Catégorie | Fichiers | État |
|---|---|---|---|---|
| A1 | **Critique** | Fuite entre espaces par les droits RGPD : export et effacement cherchent la personne par e-mail **dans tous les espaces**, sous un rôle qui contourne la RLS. | `Services/Rgpd/GdprPortabilityService.php`, `GdprErasureService.php`, `RgpdRequestsController.php` | [C] |
| A2 | **Haute** | Lien magique non atomique (course entre lecture et consommation) ; même motif, plus bénin, pour la réinitialisation. | `MagicLinkService.php`, `PasswordResetController.php` | [C] |
| A3 | **Haute** | Clé SSH de production stockée en secret de **dépôt** et lue par environ 25 workflows sans environnement protégé ; utilisateur root ; hôte non épinglé ; secrets passés en arguments de commande distante. | `.github/workflows/*` (dont `deploy-direct-ssh.yml`) | [C] |
| A4 | Moyenne | Pas de CSP sur le domaine de production (seulement en local et dans une config nginx non déployée). | `infra/caddy/Caddyfile`, `frontend/Caddyfile.app` | [C] |
| A5 | Moyenne | Webhook ZeptoMail : jeton accepté dans l'URL. Comparaison et refus sur secret vide corrects. | `ZeptoMailWebhookController.php` | [C] |
| A6 | Moyenne | Canaux internes signés : pas de limiteur sur l'un, pas d'anti-rejeu par nonce, signature du corps sans horodatage sur l'un. HMAC à temps constant correct. | `Internal/ScraperResultController.php`, `SiteSyncController.php` | [C] |
| A7 | Moyenne | Données personnelles (e-mails en clair) dans les journaux, dont l'énumération d'adresses inconnues ; niveau `debug` signalé en production sans rotation. | `MagicLinkService.php`, `HunterEmailVerifier.php`, `UsersController.php`, `EmailFinderService.php`, `MentionsLegalesScraperService.php`, `docker-compose.prod.yml` | [C] |
| A8 | Moyenne | Le contexte d'espace fait confiance à `current_workspace_id` sans contrôler l'appartenance (ni la révocation) dans `user_workspaces` ; même chose pour l'autorisation des canaux temps réel. | `SetCurrentWorkspace.php`, `routes/channels.php` | [C] |
| A9 | Moyenne | Telescope, s'il est allumé, s'ouvre au owner de **n'importe quel** espace, alors qu'il voit tout. Horizon idem. | `TelescopeServiceProvider.php`, `HorizonServiceProvider.php` | [C] |
| A10 | Moyenne | CI : Semgrep tourne mais **ne bloque pas** sur découverte ; Trivy ne tourne pas sur PR ; `security.yml` n'est pas une condition du déploiement ; **aucune action épinglée par SHA** (dont celle qui reçoit la clé SSH). | `.github/workflows/security.yml`, `ci.yml`, `deploy-direct-ssh.yml` | [C] |
| A11 | Basse | SSRF : la garde existe (`SsrfGuard`) mais un service de lecture de pages ne fige pas l'IP vérifiée (rebinding DNS possible) ; activation lue par `env()`. | `MentionsLegalesScraperService.php`, `SsrfGuard.php` | [C/S] |
| A12 | Basse | Documentation d'API (Swagger) servie sans authentification en production. | `config/l5-swagger.php`, Caddyfile | [C] |
| A13 | Basse | `env()` lu hors config (ignoré sous `config:cache`) dans le fournisseur de routes et ses limiteurs. | `RouteServiceProvider.php` | [C] |
| A14 | Basse | Gardes d'espace des contrôleurs laxistes quand `workspace_id` est NULL ; `current_workspace_id` assignable en masse ; cookie `secure` faux par défaut (forcé en prod) ; invalidation des autres sessions non prouvée sous Redis. | `ApiController.php`, `User.php`, `config/session.php` | [C/S] |
| A15 | Basse | Sauvegardes chiffrées (AES-256-CBC, PBKDF2) mais **sans authentification** du chiffré (pas d'AEAD), avec une seule phrase secrète pour tout. | `infra/scripts/backup-postgres.sh` | [C] |

**Infirmé ou correct.**
- Injection SQL : les fragments bruts n'utilisent que des constantes ou des listes blanches.
- XSS : aucun HTML injecté côté React.
- CORS : origine explicite.
- CSRF : aucune route exclue.
- `APP_DEBUG=false` en production.
- Imports CSV bornés et non stockés ; exports protégés contre l'injection de formules.
- Toutes les routes destructrices et d'export portent une permission, sauf F2.
- Aucun `pull_request_target`.
- Gitleaks bloquant sur PR et sur push.
- Session : régénération de l'identifiant au login, cookie chiffré et `http_only`.

---

## 3. Isolation multi-client

### 3.1 Ce qui est prouvé [C]

- **Politique RLS stricte et fermée par défaut.** La migration de durcissement d'août pose ENABLE + FORCE et une politique unique par table portant `workspace_id`. Si la variable de session est vide, aucune ligne n'est visible. Les tables créées depuis ont chacune leur bloc strict.
- **Rôle applicatif prévu.** Il n'est ni superutilisateur, ni BYPASSRLS, ni propriétaire des tables.
- **Tâches de fond.** Un trait des jobs sérialise l'espace cible et refuse de tourner sans lui. Le contexte est purgé entre deux jobs et en fin de requête.
- **Caches.** Les caches métier incluent l'espace dans leur clé. Seules deux clés du routeur LLM n'ont pas d'espace (gravité faible).
- **Fichiers.** Un seul écrit sur disque : l'export RGPD, chiffré, sous un nom aléatoire.
- **Tests.** `RlsTest`, `EtancheiteParTableTest` et environ 17 tests `*SousRlsTest` tournent sous le rôle non privilégié, avec deux espaces.

### 3.2 Ce qui ne l'est pas

1. **[C] La RLS ne s'applique pas en fonctionnement normal.**
   - Le drapeau `CRM_DB_APP_ROLE_ENABLED` vaut `false` par défaut (`config/database.php`, `config/crm.php`, `.env.example`). La connexion par défaut utilise alors un rôle qui contourne la RLS.
   - Un test (`RolePorteurDeLaRlsTest`) **verrouille** cet état, et le service d'effacement RGPD en dépend.
   - Aucune garde au démarrage ne refuse la production sans RLS.
   - Valeur réelle en production [S] : les commentaires du code se contredisent. À mesurer avec une requête sur le rôle courant.
2. **[C] Environ 45 commandes console** n'ont pas de contexte d'espace. Si le drapeau passe à `true`, elles ne verront plus rien : panne silencieuse, pas de fuite. Une jointure presse/entreprises ne compare pas les espaces.
3. **[C] L'ingestion du scraping écrit dans un espace fixe** (celui d'Axion). La conception est mono-locataire.
4. **[C] Tables sans `workspace_id` :**
   - **globales par choix** : `opt_out`, `email_suppressions` (adresses en clair), `crm_outbound_events` ;
   - **enfants sans colonne** (relevé heuristique, à confirmer table par table) : `email_messages`, `email_sequences`, `dnc_entries`, `deal_history`, `linkedin_sequence_runs`, `email_validations`, `prompt_templates` et `prompt_template_versions`, `magic_links` ;
   - **techniques** : `job_batches`, `partners_idempotence` ;
   - **exclues de la RLS** : `audit_logs`, partitionnée et filtrée seulement en PHP.
5. **[C]** La liste des politiques n'est vérifiée que **par nom**. Une politique permissive orpheline portant un autre nom s'ajouterait par OU. C'est déjà arrivé une fois.
6. **[S] Redis et les files sont partagés** entre espaces. C'est acceptable si chaque charge utile porte l'espace, ce qui est le cas des jobs relus. Dans une instance mutualisée, Redis doit avoir un préfixe par instance, et un mot de passe.

### 3.3 Migration des tables sans `workspace_id` (proposition, V0)

Pour chaque table : ajouter la colonne en nullable, remplir, puis la rendre NOT NULL, puis poser la RLS.

1. `opt_out`, `email_suppressions`, `dnc_entries` :
   - Ajouter `workspace_id uuid NULL`.
   - Remplir avec l'espace Axion (seul locataire actuel).
   - Passer en `NOT NULL` avec une clé étrangère.
   - Remplacer l'unicité `(email)` par `(workspace_id, email_empreinte)`.
   - Poser ENABLE + FORCE et la politique stricte.
   - Créer une **table séparée `suppressions_plateforme`** sans espace, pour les pièges et les adresses invalides (liste technique commune, D-C4), en lecture seule pour le rôle applicatif.
   - Ne plus stocker l'adresse en clair : empreinte, plus le chiffré si besoin de restitution.
2. Tables enfants (`email_messages`, `email_sequences`, `deal_history`, `linkedin_sequence_runs`, `email_validations`, `prompt_template*`) :
   - colonne dénormalisée remplie depuis le parent ;
   - déclencheur `BEFORE INSERT` qui recopie l'espace du parent et refuse un écart ;
   - RLS stricte.
3. `magic_links` : espace non pertinent (rattaché à l'utilisateur). Le garder hors RLS mais le **révoquer** pour toute lecture autre que la fonction de consommation atomique.
4. `audit_logs` :
   - RLS sur la table mère partitionnée (Postgres l'applique aux requêtes passant par la mère) ;
   - lecture du support Axion par une fonction `SECURITY DEFINER` journalisée.
5. `crm_outbound_events`, `job_batches`, `partners_idempotence` : ajouter l'espace si la charge contient des données d'un client ; sinon, documenter leur caractère technique dans l'inventaire de `EtancheiteParTableTest`.
6. Garde de CI : **toute table nouvelle** sans `workspace_id` ni mention dans l'inventaire « global assumé » fait échouer la suite. L'inventaire existe déjà ; il faut le rendre exhaustif.

### 3.4 Suite de tests « deux clients factices » (plan)

Elle s'appuie sur deux espaces, **Alpha** et **Bêta**, créés par la commande de création de client. Chacun reçoit :
- un owner, un admin, un viewer ;
- 50 entreprises, 50 contacts, une liste, une campagne brouillon ;
- 3 oppositions, dont **une même adresse dans les deux espaces** ;
- une demande RGPD.

La suite tourne **entièrement sous le rôle applicatif** (drapeau à `true`), y compris en HTTP.

1. **Base** : pour chaque table de l'inventaire calculé, contexte Alpha, alors 0 ligne de Bêta (lecture, mise à jour, suppression). Sans contexte, 0 ligne. Contexte forgé vers un espace inexistant, 0 ligne. Aucune politique permissive hors convention de nom (requête sur `pg_policies`).
2. **HTTP, IDOR** : pour chaque route `GET/PUT/PATCH/DELETE {id}` de `routes/api.php` (liste générée), un utilisateur d'Alpha qui vise un identifiant de Bêta reçoit 404, jamais 200 ni 403. Test généré depuis la table des routes, pour que toute route nouvelle soit couverte.
3. **Appartenance** : un utilisateur dont `current_workspace_id` pointe vers Bêta sans appartenance (ou avec une appartenance révoquée) reçoit un refus. Même chose sur les canaux temps réel.
4. **Rôles** : un admin d'Alpha ne peut ni nommer, ni rétrograder, ni fermer un owner. Un viewer ne peut pas faire d'action de masse.
5. **RGPD** : une demande dans Alpha pour l'adresse commune n'exporte et n'efface **que** les données d'Alpha. Les données et le compte de Bêta restent intacts.
6. **Opposition** : une désinscription chez Alpha ne bloque pas Bêta (sauf liste plateforme). Un envoi Bêta vers une adresse opposée chez Bêta est refusé.
7. **Jobs et commandes** : chaque job dispatché depuis Alpha n'écrit que dans Alpha. Chaque commande planifiée est rejouée sous le rôle applicatif : elle doit soit poser un contexte explicite, soit échouer bruyamment, jamais rendre « 0 traité » en silence.
8. **Caches** : même requête de tableau de bord pour Alpha puis Bêta, réponses distinctes. Garde statique : toute clé `Cache::` sans espace est refusée, sauf liste blanche.
9. **Journaux et exports** : aucun e-mail en clair dans les journaux produits par la suite (analyse du fichier de journal à la fin). Les exports d'Alpha ne contiennent aucun identifiant de Bêta.
10. **Retours d'envoi** (dès que le module existe) : un événement signé avec l'identité SMTP de Bêta est appliqué à Bêta, même si un en-tête prétend Alpha.

Effort : 4 jours-agent, plus 1 de garde CI. Condition de sortie : vert en CI, sous rôle applicatif, bloquant sur `main`.

### 3.5 À faire AVANT d'accueillir un client (même en instance dédiée)

1. Passer le drapeau du rôle applicatif à `true` par défaut. Inverser le test qui verrouille l'état superutilisateur. Ajouter une garde au démarrage qui refuse `APP_ENV=production` si le rôle courant a BYPASSRLS, est superutilisateur ou possède les tables.
2. Porter les commandes console sous contexte d'espace explicite (`--workspace=` ou boucle sur les espaces avec contexte posé). Donner une connexion privilégiée nommée aux seules migrations et à la maintenance partman.
3. Réécrire export et effacement RGPD **par espace** (et la fermeture de compte utilisateur seulement pour un membre du seul espace demandeur).
4. Faire la migration § 3.3, puis la suite § 3.4 au vert.
5. Contrôler l'appartenance dans `SetCurrentWorkspace` et dans les canaux.
6. Faire les correctifs F1, F2, F3, F5, A2 et A3.

---

## 4. Sécurité du module d'envoi (rien n'est codé : exigences pour le plan 03)

| Sujet | Exigence | Garde |
|---|---|---|
| Clés DKIM | Générées **sur le serveur d'envoi**. La clé privée ne le quitte jamais (INF-027). 2048 bits RSA, ou Ed25519 en double signature. Rotation semestrielle par deux sélecteurs (RES-015). Seule la clé publique remonte au CRM. | Garde CI : motif PEM interdit dans tout le dépôt (gitleaks par défaut, plus une règle maison pour `BEGIN .*PRIVATE KEY` sans liste blanche). |
| Identifiants SMTP | Un identifiant **par locataire et par groupe d'envoi** (INF-083), généré à la création du client, stocké chiffré en base (cast `encrypted`, clé applicative par instance). Jamais dans un fichier versionné. | Test : création de deux clients, alors deux identifiants distincts ; l'un ne peut pas injecter dans le groupe de l'autre. |
| **Tenant imposé par l'identité SMTP** | Le serveur d'envoi déduit le locataire, le pool et l'IP **de l'identifiant authentifié**, jamais d'un en-tête (`X-Tenant` ou autre). Il **supprime** tout en-tête de routage reçu. | Test de banc : identifiant Bêta plus en-tête Alpha, alors l'envoi part par le pool Bêta et l'en-tête est retiré. |
| Relais ouvert | Écoute sur l'IP privée WireGuard seulement. AUTH obligatoire. `MAIL FROM` limité aux domaines **vérifiés du locataire authentifié**. Aucun port 25 entrant public sur le serveur d'envoi. Test anti-relais en 4 couches en boîte noire depuis l'extérieur, chaque jour (sonde externe). | Sonde quotidienne ; alerte si un port inattendu répond (IPv4 et IPv6). |
| Webhook d'événements | HMAC-SHA256 du corps brut **plus horodatage** dans l'en-tête, écart de 5 minutes au plus, **nonce mémorisé 72 h** (anti-rejeu), refus si secret absent, comparaison à temps constant, un secret par locataire et par serveur, écoute privée seulement, limiteur. **Jamais de jeton dans l'URL** (corriger aussi A5). | Tests : signature fausse, horodatage périmé, rejeu, secret vide : tous refusés. |
| Signature HMAC « API signée » vers la console | Même schéma ; clé par instance ; rotation sans coupure (deux clés acceptées pendant la bascule). | Idem. |
| Déploiement sans clé dans le dépôt public | Chaque instance **tire** son image publique (GHCR) ; aucune clé SSH de client dans GitHub. Les secrets d'instance sont générés sur place par la commande d'installation (`/opt/<instance>/.env`, droits 600) et sauvegardés chiffrés hors dépôt. Le registre des clients vit **dans la base** (X3 du 06), jamais dans un dépôt. | Garde CI : aucun nom de client, aucune IP, aucun domaine client dans le dépôt (liste de motifs ; l'IP déjà commitée est à retirer, F6). |
| Gardes de CI | Gitleaks (bloquant, déjà), **Semgrep bloquant** (cliquet : base de découvertes figée, toute nouvelle découverte bloque), motif PEM, motif IPv4/IPv6 publique (hors plages Cloudflare et documentation RFC 5737), garde données personnelles existante, actions épinglées par SHA, Dependabot pour `github-actions`. | Les 3 premières exigées sur `main` ; `security.yml` en `needs` du déploiement. |
| Protection de `main` | PR obligatoire, contrôles exigés (CI et Gitleaks, plus Semgrep une fois le cliquet posé), pas de push forcé, pas de suppression, historique linéaire. Administrateurs inclus si possible. Secret SSH dans un **environnement protégé** limité à `main`. | Relu le 30/10 : 4 contrôles exigés, Gitleaks et Semgrep non exigés. Non relu aujourd'hui (pas d'accès à l'API de protection dans cette session). |
| Sauvegardes chiffrées | Une archive **par client** et une phrase secrète par client. Passer à un chiffrement authentifié (`age` ou `openssl` en AEAD, ou un HMAC du chiffré). Restauration testée chaque mois (le script d'exercice existe). Clés B2 limitées à un seul bucket et à l'écriture. | Exercice mensuel journalisé dans l'audit. |
| Journal d'audit | La chaîne de hachage existe (`AuditHashChain`). L'étendre à : changements de rôle, 2FA (activation, secours, réinitialisation), lancement et arrêt de campagne, changement de domaine ou d'IP, accès du support Axion (temporisé, motif obligatoire), exports. Ajouter une vérification quotidienne de la chaîne, avec alerte. | Test : chaque action sensible écrit une entrée chaînée. |
| Secours de la 2FA par e-mail | Codes de secours hachés, à usage unique, consommés de façon **atomique**. Commande `crm:2fa:reinitialiser` lancée sur le serveur seulement, journalisée, qui **notifie l'utilisateur** et révoque ses sessions. Le changement d'adresse e-mail du compte exige un code envoyé à **l'ancienne** adresse. Le lien magique ne doit pas franchir la 2FA (décision 1 du 04 : l'éteindre). Mailer d'authentification séparé et **non journalisant**. | Tests du lot PR-D. |

---

## 5. Menaces propres à un outil d'envoi vendu à des clients

| Menace | Parade |
|---|---|
| **Abus par un client** (spam, fichiers achetés, volume brutal) | Politique d'usage acceptable au contrat ; case « base légale » obligatoire à l'import ; vérification des listes avant envoi ; plafonds journaliers par locataire **appliqués au serveur d'envoi** (pas seulement au CRM) ; chauffe imposée ; coupure automatique si les rebonds dépassent 5 % ou les plaintes 0,1 % ; arrêt d'urgence par client et arrêt général Axion. |
| **Phishing via la plateforme** (compte client compromis, ou client malveillant) | Domaines d'expédition vérifiés (DNS) et rattachés au locataire ; interdiction d'expéditeurs imitant des marques connues (liste et distance d'édition) ; analyse des liens (domaines récents, raccourcisseurs, URL de connexion) ; première campagne de chaque client validée par un humain Axion ; 2FA obligatoire pour tout compte qui peut envoyer ; alerte sur un changement de domaine ou d'IP suivi d'un envoi dans les 24 h. |
| **Fuite entre clients** | §§ 3.3 à 3.5 ; instance dédiée par défaut tant que la suite à deux clients n'est pas verte en production ; support Axion temporisé et journalisé. |
| **Réputation partagée** (un client fait lister l'IP ou le domaine d'un autre) | Au moins une IP dédiée par client ; domaines jamais partagés ; groupes d'envoi séparés ; serveur d'envoi sur le compte d'hébergement du client si possible (D-C6) ; surveillance des listes noires par IP et par domaine ; aucun domaine `axion-ia.com` en envoi de masse. |
| **Compte d'hébergement d'Axion fermé après plainte** | Serveur d'envoi du client sur son compte ; adresse d'abus traitée sous 24 h ; boucles de rétroaction (JMRP, SNDS, Postmaster) inscrites dès V0. |
| **Exfiltration de la base de prospection d'Axion** | Données Axion dans l'espace Axion seulement, jamais dans une instance client (D-C3) ; ingestion du scraping rendue « par espace » (§ 3.2, point 3). |
| **Désinscription qui casse après le départ d'un client** | Page de désinscription maintenue N années, domaine renouvelé automatiquement (critique M1 du 06). |

---

## 6. Plan 04 : est-il correct et complet ?

**Non.** Il est juste sur la 2FA, mais incomplet.

1. Quatre sections sont vides : « URGENT », « Constats », « Solution » et « Pièges ». Le retrait était volontaire, mais il manque alors les renvois vers ce fichier.
2. La synthèse 00 annonce « 7 petites PR » ; le 04 en liste 5.
3. Les décisions sautent le n° 5.
4. La durée de la 2FA (12 h ou 30 jours, X8 du 06) n'est pas tranchée.
5. **Exiger Semgrep sur `main` ne sert à rien tant que Semgrep sort en succès sur découverte.**
6. Il manque les failles F2, F3, F4, F5 (configuration réelle), A1, A2, A3, A8 et la garde RLS au démarrage.

### Plan 04 corrigé (remplace la liste de PR du 04)

| PR | Contenu | Tests d'abord | Effort (j-agent) | Priorité |
|---|---|---|---|---|
| **PR-0** | Fermer F1 : enrôlement refusé si la 2FA est active (409) ; les routes d'enrôlement sortent de la liste blanche (enrôlement autorisé seulement pour un compte sans 2FA, ou après franchissement) ; anti-rejeu TOTP (dernier pas mémorisé) ; limiteur **par compte** sur la vérification, avec verrou. | 6 | 1 | **V0** |
| **PR-1** | F5 : mailer d'authentification réel (transactionnel dédié, pas le compte commercial) ; démarrage **refusé** en production si ce mailer est `log`, `array` ou un repli vers `log` ; retrait du lien de tout journal (y compris mode simulation) ; purge des journaux existants et invalidation des jetons en cours. Correction du script de configuration de production. | 4 | 1 | **V0** |
| **PR-2** | F2 : permission `companies.update` sur l'action de masse CRM ; refus des étiquettes verrouillées (ajout et retrait). | 4 | 0,5 | **V0** |
| **PR-3** | F3 : hiérarchie des rôles (seul un owner touche au rôle owner ou à un compte owner) ; refus de l'auto-modification de rôle ; au moins un owner par espace ; révocation des sessions de la cible ; entrée d'audit. | 6 | 1 | **V0** |
| **PR-4** | A2 : consommation atomique (mise à jour conditionnelle avec retour de ligne) du lien magique, de la réinitialisation et des codes de secours. | 3 | 0,5 | **V0** |
| **PR-5** | A1 : export et effacement RGPD filtrés par espace ; fermeture de compte limitée aux membres du seul espace ; test à deux espaces. | 4 | 1,5 | **V0** |
| **PR-6** | RLS armée : drapeau à `true` par défaut ; garde au démarrage (rôle sans BYPASSRLS ni superutilisateur ni propriétaire) ; inversion du test verrou ; connexion privilégiée nommée pour migrations et maintenance ; contexte explicite pour les ~45 commandes ; contrôle d'appartenance dans le middleware et les canaux. | 10 | 5 | **V0** |
| **PR-7** | Migration des tables sans `workspace_id` (§ 3.3) et inventaire exhaustif. | 6 | 3 | **V0** (avant tout client) |
| **PR-8** | Suite « deux clients factices » (§ 3.4) bloquante. | — | 5 | **V0** |
| **PR-9** | A3 et A10 : clé SSH dans un environnement protégé, utilisateur non root avec commande restreinte, clé d'hôte épinglée, secrets passés par l'entrée standard ; actions épinglées par SHA et Dependabot ; Semgrep en cliquet bloquant ; `security.yml` en condition du déploiement ; règles PEM et IP ; retrait de l'IP commitée. | — | 2 | **V0** |
| **PR-10** | F4 : segments sensibles fermés si la configuration est vide ; liste explicite en production. | 3 | 0,5 | **V0** |
| **PR-C** (inchangée) | Mailer `auth` isolé (variables `MAIL_AUTH_*`) et garde anti-dérive commerciale. Fusionnable avec PR-1. | — | (dans PR-1) | V0 |
| **PR-D** (inchangée, plus les compléments) | 2FA e-mail backend, plus : codes de secours atomiques, changement d'adresse validé par l'ancienne, réinitialisation qui notifie et révoque, journal d'audit. | 16 | 3 | **V0** |
| **PR-E** (inchangée) | Front de la 2FA e-mail. | — | 2 | V0 |
| **PR-11** | A4, A5, A6 : CSP, Permissions-Policy et COOP en production ; webhook ZeptoMail par en-tête seulement ; limiteur et nonce sur les canaux internes. | 5 | 1,5 | V1 |
| **PR-12** | A7, A9, A12, A13 : e-mails remplacés par empreinte ou identifiant dans les journaux, niveau `info` et rotation en prod ; Telescope et Horizon réservés à un rôle plateforme (pas au owner d'un espace) ; Swagger fermé en prod ; `env()` remplacé par `config()`. | 3 | 1,5 | V1 |
| **PR-13** | A11, A14, A15 : IP figée dans toutes les lectures de pages ; gardes NULL strictes ; `current_workspace_id` retiré du fillable ; `secure` vrai par défaut ; test d'invalidation des sessions sous Redis ; sauvegarde par client en chiffrement authentifié. | 4 | 2 | V1 |
| **PR-F** (inchangée) | Retrait du TOTP. | — | 0,5 | V2 |
| Module d'envoi (§ 4) | Exigences à intégrer aux lots E0, E1, E3 et E6 du plan 03 (pas de PR séparée). | — | +3 répartis | V0 pour E1/E3/E6 |

**Total V0 : environ 27 jours-agent** (dont 13 pour l'isolation, PR-6 à PR-8), plus 15 % de relecture. V1 : environ 5 jours-agent.

**Ordre** : PR-0, PR-1, PR-2, PR-3, PR-4 (moins de 4 jours, à faire immédiatement, même sans client), puis PR-9, PR-5, PR-6, PR-7, PR-8, PR-10, puis la 2FA e-mail.

### Décisions ajoutées pour Will
- **D-S1** : Mesurer **sur le serveur** l'état du drapeau RLS, du mode simulation et du mailer d'authentification, puis lancer PR-0 et PR-1 immédiatement (recommandé).
- **D-S2** : Durée de la 2FA (12 h ou 30 jours), à trancher une fois (X8).
- **D-S3** : Segments sensibles fermés par défaut (recommandé), contre la décision du 01/10 qui les ouvre quand la configuration est vide.
- **D-S4** : Première campagne de chaque client validée par un humain Axion (recommandé).

---

## 7. Ce qui bloque l'accueil d'un premier client

1. RLS armée et prouvée en production (PR-6), avec garde au démarrage.
2. RGPD par espace (PR-5).
3. Tables d'opposition et de suppression par espace (PR-7).
4. Suite « deux clients factices » verte sous le rôle applicatif (PR-8).
5. 2FA réellement obligatoire (PR-0, puis PR-D et PR-E) ; mailer d'authentification sain (PR-1).
6. Rôles et action de masse (PR-2, PR-3) ; liens à usage unique atomiques (PR-4).
7. Clé SSH de production isolée et CI bloquante (PR-9).
8. Côté envoi : tenant imposé par l'identité SMTP, anti-relais testé, webhook HMAC avec anti-rejeu, plafonds au serveur d'envoi (§ 4).

Même en **instance dédiée**, les points 2, 5, 6 et 7 restent bloquants. La RLS (1, 3, 4) l'est pour le mutualisé, et fortement recommandée pour le dédié : l'instance contient aussi l'espace de démonstration ou de support.
