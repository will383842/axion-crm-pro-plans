# 08 : Matrice de parité PowerMTA + MailWizz → KumoMTA + CRM Pro (30/10/2026)

Question de Will : « pour remplacer PowerMTA et MailWizz, comment va-t-on faire pour que notre outil soit tout aussi complet ? »

Travail en LECTURE SEULE : aucun e-mail, aucun accès serveur, rien exécuté, aucun secret recopié. RIEN N'EST CODÉ. Constats d'agent, non recoupés par un second relecteur.

**Sources lues**
- Ce que les anciens outils de Will utilisaient : `_AUDIT-SOS-EXPAT-REPRISE-2026-10-30\` (00, A, B, C, E), dont la config PowerMTA de SOS-Expat telle que décrite par les audits (`pmta/config`, `bounce-classifications`, `routing-domains`, `blocking-errors`).
- Cahier : `_PLAN-ENVOI-EMAILING-CRM-PRO-2026-09-28\04-final\` (`CAHIER-DES-CHARGES…md`, `REGISTRE-REQ.csv` : 502 REQ, dont CAM 83, CHA 69, CON 78, INF 83, RES 67, RET 48, SEC 41, VER 33) et `06-verification\V1-parite-sos-expat.md` (146 fonctions SOS-Expat recensées, 118 couvertes).
- Plan : `_PLAN-CRM-PRO-COMPLET-2026-10-30\` 00, 01, 02, 03, 05.
- Existant : `C:\Users\willi\Documents\Projets\Axion-CRM-Pro` (commit `1f7b0caa` du 29/10 : pas de dossier `backend/app/Emailing`, aucune trace de KumoMTA ; briques `Crm/Campagnes`, `Crm/Listes`, `Crm/Emails`).
- Documentation publique (30/10) : docs.kumomta.com (gestion des files, shaping et Traffic Shaping Automation, classifieur de rebonds, `log_arf` / `log_oob`, log hooks) ; mailwizz.com/features.
- **Limite** : la doc de PowerMTA (Bird) n'est pas publique. Les fonctions PowerMTA ci-dessous viennent de la configuration de SOS-Expat (lue par les audits A et C) et de connaissances générales sur le produit. Certitude moyenne sur les noms exacts des directives.

**Légende de parité** : IDENTIQUE (même fonction, même niveau) · ÉQUIVALENT (même résultat, autre forme) · PARTIEL (des briques existent, il faut écrire le reste) · ABSENT (il faut tout écrire, ou on y renonce exprès).
**État dans le CRM Pro** : EXISTE (code présent) · PRÉVU (au plan 02/03/05, avec sa référence) · ABSENT (dans aucun plan) · EXCLU (refusé exprès par une règle de Will ou du cahier).
**Effort** : jours-agent (j), tests compris, hors relectures (+15 %). **Priorité** : étape du module d'envoi, V0 (premier envoi sûr, 20 à 300/j), V1 (1 000 à 2 000/j, tout le quotidien), V2 (jusqu'à 5 000/j, confort).

---

## A. Fonctions du MTA : PowerMTA → KumoMTA

| # | Fonction PowerMTA (ce que SOS-Expat en utilisait) | Équivalent KumoMTA | Parité | Comment on comble l'écart | Effort | Prio |
|---|---|---|---|---|---|---|
| A1 | **Virtual MTA et pools** (5 VMTA, 1 IP = 1 domaine, choix par en-tête ou `MAIL FROM`) | `egress_source` (IP source, EHLO) + `egress_pool` pondéré, via le helper `sources.toml` ; pool choisi par locataire (`tenant`) dans `queues.toml` | ÉQUIVALENT | Générer `sources.toml` et `queues.toml` depuis le registre des IP et domaines (REQ-INF-010/037). **Piège** : le locataire doit être imposé par l'identité SMTP AUTH, jamais lu dans l'en-tête `X-Tenant` (fichier 05). | inclus E3 + 1 j (garde « tenant par AUTH ») | V0 |
| A4 | **Classification des rebonds** (`bounce-category-patterns`, 2 785 motifs en 18 catégories) | Classifieur intégré (`kumo.configure_bounce_classifier`), règles regex en TOML, fichier par défaut `iana.toml`, fichiers perso placés avant ; classe écrite dans chaque journal (`bounce_classification`) | ÉQUIVALENT | Convertir la table de SOS-Expat en TOML **après vérification de son origine** (licence inconnue, R7), la tester sur un corpus réel du banc ; table `smtp_response_patterns` côté CRM pour la décision dur/mou/plainte (CHA-025). Pas de validateur de fichier fourni : en écrire un en CI. | 2 j (prévu E6) + 0,5 j validateur | V0 |
| A5 | **Mode « backoff »** (`smtp-pattern-list` « too many », RBL, Spamhaus → ralentir à 1 msg/min puis revenir après succès) | **Traffic Shaping Automation** : démon séparé (`tsa-daemon`) ; règles regex sur les réponses distantes, actions `Suspend` (durée) et `SetConfig` (surcharge temporaire, ex. baisser le débit) | ÉQUIVALENT (plus général, mais à écrire) | Traduire la liste `blocking-errors` de SOS-Expat en règles TSA ; brancher les mêmes réponses sur les disjoncteurs du CRM (CHA-016 : pause d'une IP vers un fournisseur). Tester chaque règle avec des réponses simulées au banc. | 2 j | V0 |
| A7 | **Rebonds asynchrones (OOB / DSN)** | `log_oob = "LogThenDrop"` sur `bounce.<domaine>` → enregistrement `OOB` | ÉQUIVALENT | VERP `rb-<jeton>@bounce.<domaine>` (RET-009) ; ne jamais mettre `true` (boucle de relais possible selon la FAQ KumoMTA). | prévu E6 | V0 |
| A8 | **DKIM** (`domain-key` par domaine) | Helper `dkim_sign` (RSA, Ed25519, plusieurs signatures, clé sur disque ou coffre) | IDENTIQUE | Seul signataire = serveur d'envoi (INF-027). Rotation à deux sélecteurs (RES-015) : à écrire nous-mêmes, comme avec PowerMTA. | 1 j rotation | V1 |
| A9 | **Gestion de la file** (`pmta show queue`, pause/reprise/suppression d'une file, « jobs » `x-job` annulables) | Files planifiées `campagne:locataire@domaine` + files prêtes par source ; `kcli` (résumé des files, suspendre, rebondir/retirer, réaffecter) et API d'admin HTTP (suspend, bounce, rebind, inspection de message) | ÉQUIVALENT (en ligne de commande) / PARTIEL (pas d'écran) | Opérations `pause`, `reprise`, `retirer` du contrat `ServeurEnvoi` (plan 03 § 10) branchées sur l'API d'admin ; **écran « Files d'attente » à ajouter** dans la console (par locataire, par fournisseur, âge du plus ancien, suspendre, retirer par campagne). | 3 j écran | V1 |
| A10 | **Comptabilité** (fichiers `acct-*.csv` : livré, rebond, report, plainte ; pipe `bounce-pipe.sh` vers l'API) | Journaux JSON compressés (zstd) par segments, un enregistrement par événement (Reception, Delivery, TransientFailure, Bounce, Expiration, Feedback, OOB, AdminBounce…) ; **log hooks** natifs vers webhook (par lots), Kafka ou AMQP | ÉQUIVALENT (meilleur : poussée native, idempotence possible) | Log hook → webhook HMAC sur la liaison privée (plan 03 § 6), + tirage nocturne de réconciliation. Prévoir une règle de shaping pour la file du hook (sinon accumulation, doc KumoMTA). | prévu E6 | V0 |
| A11 | **Réessais et expiration** (`retry-after`, `bounce-after` 24 h, nouvel essai à 10 min) | `retry_interval`, `max_retry_interval` (montée exponentielle), `max_age`, par locataire ou domaine | IDENTIQUE | Valeurs dans la config générée ; `max_age` court (24 h) pour la prospection. | 0,25 j | V0 |
| A12 | **TLS** (`use-starttls`, `require-starttls` ; SOS-Expat l'imposait partout, à tort) | `enable_tls` (opportuniste, requis, avec ou sans vérification), **MTA-STS** et **DANE** natifs | ÉQUIVALENT / MIEUX | Opportuniste par défaut, MTA-STS activé ; ne pas reprendre le `require-starttls` global (bug 7 de l'audit A). | 0,25 j | V0 |
| A13 | **Routage** (route vers relais, `smtp-source-host`, VMTA par en-tête) | `routing_domain`, relais par file, `kumo-proxy` (SOCKS5) pour sortir par un autre hôte | ÉQUIVALENT | Aucun proxy sur le chemin d'envoi (garde G6) : on n'utilise pas `kumo-proxy`. | 0 | — |
| A14 | **Tampons et spool** (spool disque, mémoire) | Spool persistant sur disque (RocksDB), limite mémoire « souple », **backpressure** : refus temporaire 4xx à la réception quand la mémoire ou le spool saturent | ÉQUIVALENT | Le CRM traite un 4xx d'injection comme « report », jamais comme échec (CHA-030). Alerte disque du spool. | 0,5 j | V0 |
| A15 | **Supervision** (moniteur web PowerMTA, SNMP ; console de gestion PMC vendue à part) | Métriques **Prometheus** (`/metrics`), `kcli top` ; **aucune interface graphique native** | PARTIEL | Grafana + règles Alertmanager (on reprend les 7 alertes de SOS-Expat : serveur arrêté, rebonds, liste noire, disque, file, moteur, mémoire) + écran « Santé serveur » de la console (plan 03 § 7.6). | 2 j Grafana/alertes (E11) | V0 |
| A16 | **Injection** (SMTP, éventuellement authentifié) | SMTP avec AUTH (choix du cahier) ; API HTTP d'injection avec gabarits (gardée fermée, repli documenté) | IDENTIQUE | Écouteur 2525 sur WireGuard seulement, anti-relais 4 couches (INF-020). | prévu E3 | V0 |
| A17 | **Plafond journalier par IP** (400/j à froid dans la config SOS-Expat) | Débits par file (`max_message_rate`), par portée (`overall_max_message_rate`), throttles Lua ; **pas de « budget du jour » natif** | PARTIEL | Plafond dur local par locataire et global (INF-023) écrit en Lua (throttle à la journée) ; la chauffe fine reste décidée par le CRM (CHA-004). | prévu E3 (+1 j tests de bornes) | V0 |
| A18 | **Chauffe d'IP** (PowerMTA n'en a pas ; SOS-Expat la faisait par scripts et quotas MailWizz) | Pas de planificateur de chauffe ; seulement les débits par source | ABSENT des deux côtés | C'est le CRM qui décide (plan 03 § 3 : paliers en jours effectifs, recul automatique) et pousse les débits. | prévu E8 | V0 |
| A19 | **Homme mort, refus de `MAIL FROM` hors registre** (absents de PowerMTA aussi) | Rien de natif ; possible en Lua (événement de réception) + minuterie | ABSENT → à écrire | Invariants du contrat (INF-021, INF-025). | prévu E3 | V0 |
| A20 | **Licence et support** | PowerMTA : licence payante (Bird), support éditeur. KumoMTA : Apache-2.0, gratuit ; support payant facultatif (Silver dès 5 000 $/an, Gold dès 10 000 $/an, fichier 05) | — | Version figée par empreinte, copie des binaires, contrat `ServeurEnvoi`, repli Postfix + rspamd (fichier 05). | 8-15 j (repli Postfix, déjà au plan 05 M2) | V1-V2 |

**Bilan bloc A** : sur 19 fonctions techniques, 5 IDENTIQUES, 10 ÉQUIVALENTES (dont la gestion des files, faisable mais sans écran), 2 PARTIELLES (supervision sans écran, plafond du jour), 2 ABSENTES des deux produits (chauffe, homme mort) que le plan fait déjà porter par le CRM. **Aucune fonction de PowerMTA utilisée par SOS-Expat n'est sans équivalent.** Ce qui manque à KumoMTA, c'est l'écran, pas la mécanique.

---

## B. Fonctions de MailWizz → où elles vivent dans le CRM Pro

| # | Fonction MailWizz | CRM Pro | Référence | Ce qu'il faut ajouter | Effort | Prio |
|---|---|---|---|---|---|---|
| B1 | **Listes et abonnés** | EXISTE : listes manuelles, membres, corbeille ; import par rapprochement (5 Mo, 20 000 lignes) | 02 C2, B3 ; `Crm/Listes/ListesManuelles.php`, `ImportListe.php` | Import de fichier par l'interface (correspondance de colonnes, rapport ligne à ligne) : PRÉVU 02 B4 | prévu (4 j) | V0 |
| B3 | **Champs personnalisés** | ABSENT en pratique (seul `signals` JSONB) ; PRÉVU en P2 | 02 A12 | **Remonter en V1** : indispensable pour un client (MailWizz l'offrait par liste) et pour les variables de gabarit | 3 j | V1 |
| B4 | **Campagnes régulières** | ABSENT dans le code (`/cold-email` répond 501) ; PRÉVU en entier : objet campagne, assistant 6 étapes, validation versionnée, vagues, pause/annulation | 02 E1-E11 ; 03 § 2 ; lot E9 | — | prévu (22 j E9) | V0 |
| B5 | **Autorépondeurs / séquences** | PRÉVU : séquences 1 à 4 étapes en jours ouvrés, arrêt sur réponse, RDV, opposition, rebond ; absence = pause | 02 E3 ; CAM-035 à 038 | Étapes manuelles (appel, courrier) PRÉVU 02 E4 | prévu | V0 |
| B6 | **Campagnes récurrentes, RSS, déclenchées par un événement** | PRÉVU en P2 seulement | 02 E18, E19 | Remonter E19 (formulaire du site, RDV annulé, inscription Tour France IA) en V1 ; RSS : sans objet | 4 j | V1 |
| B7 | **Modèles et éditeur** (glisser-déposer GrapesJS/Stripo, galerie de modèles, pages d'atterrissage) | PRÉVU : gabarits versionnés, texte brut obligatoire, HTML minimal, aperçu fidèle, variables en liste blanche, contrôleur de contenu | 02 E5, E7 ; CAM-023, 024, 027, 034 | **Pas d'éditeur visuel** : voulu pour la prospection (texte d'abord). Pour la lettre d'information : éditeur HTML par blocs simple (ex. GrapesJS, licence BSD) + modèles responsive repris des squelettes SOS-Expat (audit C) | 6 j | V2 (lettre) |
| B8 | **Suivi ouvertures / clics** (pixel, liens réécrits, géolocalisation) | EXCLU exprès : aucun pixel, aucun lien réécrit, aucun identifiant personnel dans une URL | SEC-016 ; garde G5 | Remplacé par : livrés, réponses classées, RDV attribués, oppositions. Option « clics agrégés sans identifiant » laissée en « plus tard » : **décision de Will** | 0 (2 j si oui) | V2 |
| B9 | **Désinscription** (lien, page de liste) | PRÉVU : RFC 8058 un clic sur `go.<domaine d'envoi>`, `mailto:`, STOP par réponse, opposition par domaine | 03 § 5 ; RET-010, 020-026 | **Centre de préférences** (choisir ses thèmes) : ABSENT, utile seulement pour la lettre | 2 j | V2 |
| B10 | **Rebonds et plaintes** (serveurs de rebonds POP3/IMAP, serveurs FBL, webhooks des fournisseurs) | PRÉVU : webhook idempotent, `AppliquerRetour`, 3e mou = suppression, plainte = opposition, ARF par IMAP | 03 § 6 ; RET-001 à 018 | — | prévu (14 j E6) | V0 |
| B11 | **Liste noire globale et par client, listes de suppression par campagne, moniteurs de listes noires** | EXISTE : opposition globale + suppression + `peutRecevoir` ; PRÉVU : `workspace_id` (par client), exclusions par campagne, surveillance DNSBL | 02 J1, J3, M1 ; 03 § 5, E11 ; CAM-012 | — | prévu | V0 |
| B12 | **Double inscription (double opt-in)** | ABSENT | 05 § C (manque pour « complet ») | Confirmation par lien signé, journal de consentement (date, IP en empreinte, texte accepté), relance unique, jamais de confirmation forcée (leçon MailWizz n° 1 de l'audit C) | 3 j | V1 (lettre) |
| B13 | **Formulaires d'inscription et pages de liste** | ABSENT dans le CRM ; le site axionia a ses formulaires et pousse `newsletter_optin` | 02 E18 ; `SiteSyncEvent.php:44` | Formulaire intégrable (script ou iframe) par espace, anti-robot, pages « merci / confirmez / désinscrit » à la marque du client | 4 j | V1 (si clients) / V2 |
| B14 | **Rapports** (tableau de bord, stats de campagne, export) | PRÉVU : indicateurs uniques, deux lectures (date d'envoi / d'événement), entrepôt horaire sans donnée personnelle, rapports hebdo par e-mail, export | 02 H4, H7 ; 03 § 2.10 | Export PDF/CSV d'un rapport de campagne pour un client | 1 j | V1 |
| B15 | **API** (clés API, signature des requêtes, liste blanche d'IP) | PARTIEL : API v1 Sanctum pour la console seulement (173 routes) | `routes/api.php` | **API publique par espace** (clés révocables, portée par droit, signature, limites de débit) : contacts, listes, opposition, lancer une campagne déjà validée, lire les stats | 5 j | V1 (si clients) |
| B16 | **Webhooks sortants** (événements de campagne vers une appli externe) | ABSENT | — | Webhooks signés par espace : réponse reçue, opposition, rebond dur, RDV, fin de campagne ; rejeu, journal | 3 j | V2 |
| B17 | **Multi-clients et groupes de clients** | PARTIEL : espaces (`workspaces`), RLS écrite mais non prouvée ; PRÉVU : installation par client d'abord, puis mutualisé | 02 M0-M13 ; 05 § B | — | prévu (≈ 60 j lot 5) | V1 |
| B18 | **Quotas par client** (compteurs, limites par groupe, plans tarifaires) | PARTIEL : `cost_cap_eur` ; PRÉVU : plafonds journaliers, vérification, IA, compteurs remis à zéro à la date anniversaire, Stripe ; un dépassement informe, ne bloque pas la facturation | 02 M5 ; 03 § 1.2 | Le plafond **technique** d'envoi (réputation) reste dur ; seul le plafond commercial informe | prévu (4 j) | V1 |
| B19 | **Délégation de droits** (utilisateurs et groupes, permissions fines) | PARTIEL : 4 rôles, 16 permissions figés ; PRÉVU : rôles par client, accès support tracé, rôles personnalisés | 02 I8, M2 | — | prévu (6 j) | V1 |
| B20 | **Passerelles de livraison** (SMTP, PowerMTA, SES, Mailgun, SendGrid… ; quotas horaires/jour/mois par serveur ; plans de chauffe) | PRÉVU : contrat `ServeurEnvoi` agnostique (9 opérations, kit de conformité, mode simulation) ; une réalisation KumoMTA + Postfix de secours | 03 § 10 ; 05 M2 | Relais SES/Brevo/Mailgun EXCLUS pour le froid (contraire à leurs règles, compte suspendu, fichier 01). Une réalisation « relais SMTP tiers » pour la **lettre** seulement si Will le veut | 3 j (optionnel) | V2 |
| B21 | **Domaines d'envoi (DKIM) et domaines de suivi** | PRÉVU : registre des domaines, plan DNS généré, contrôle quotidien SPF/DKIM/DMARC/PTR/MTA-STS, Cloudflare par API en V1 | 03 § 7.2 ; RES-* | Domaines de suivi : sans objet (pas de suivi) ; `go.<domaine>` sert à la désinscription | prévu | V0 |
| B22 | **Moniteurs de boîtes** (actions selon le contenu des réponses) | PRÉVU : relève IMAP toutes les 5 min, rattachement, tri par règles puis IA, STOP | 02 F1-F9 ; 03 § 2.8 | — | prévu | V0 |
| B23 | **A/B** (objet) | PRÉVU en V1 : 2 à 4 variantes d'un élément, métrique = réponses positives, échantillon minimal 300 livrés | 02 E12 ; CAM-031 | — | prévu | V1 |
| B24 | **Contrôle anti-spam du contenu** (mots interdits objet/corps) | PRÉVU : contrôleur unique (bloque / avertit), formulations interdites de Will | 02 E7 ; CAM-027 | Score SpamAssassin/rspamd du message rendu avant validation (complément) | 1 j | V1 |
| B25 | **Envoi selon le fuseau, fenêtres d'envoi** | PRÉVU : fenêtres nommées heure de Paris, jours ouvrés, fériés ; outre-mer en V1 | CHA-027 ; 02 E9 | — | prévu | V0 |
| B26 | **Version web du message, partage de campagne** | ABSENT | — | Page « voir dans le navigateur » (jeton opaque, sans suivi) pour la lettre seulement | 1 j | V2 |
| B27 | **Sondages, pages d'atterrissage** | ABSENT | — | Hors périmètre : le site axionia et la console font déjà les questionnaires | 0 | — |
| B28 | **Actions sur abonnés après ouverture/clic** (copier, déplacer) | EXCLU (pas de pixel) | — | Remplacé par des actions sur **réponse** et **RDV** (arrêt de séquence, étape « opportunité », tâche) : PRÉVU 02 F9, G4, D7 | prévu | V0-V1 |
| B29 | **Courriels transactionnels** | Hors module, volontairement : ZeptoMail reste le canal du site, intouchable (garde G2) | 03 § 8 | — | 0 | — |

**Bilan bloc B** : pour la **prospection**, le plan couvre tout ce que MailWizz faisait pour SOS-Expat, et mieux (validation par version, pression commerciale, gardes). Ce qui manque est le volet **lettre d'information / marketing à des abonnés consentants** (B7, B9, B12, B13, B26) et le volet **plateforme pour clients** (B3, B15, B16), que MailWizz offrait d'origine. Ces trous étaient signalés par le fichier 05 (§ C) et le lot M10, sans estimation : ils sont chiffrés au § F.

---

## C. Pilotage qu'ajoutaient Backlink Engine et Mission Control

| # | Fonction | Où c'était | CRM Pro | Écart | Effort | Prio |
|---|---|---|---|---|---|---|
| C1 | **Chauffe** par boîte et par domaine (5 → 500/j ; Mission Control : 5-15-30-50/j) | `warmupScheduler.ts`, `pressWarmup.ts`, `WarmupState.php` | PRÉVU, plus strict : paliers en jours effectifs, budget = min(IP, domaine, boîte), recul automatique, inactivité (03 § 3.1) | Aucun ; Mailflow (faux trafic) EXCLU (CHA-035) | prévu (E8) | V0 |
| C2 | **Listes noires** de nos IP et domaines (Spamhaus, Barracuda, SpamCop, SORBS via Quad9) | `mailbox.ts`, `blacklist_checker.py` | PRÉVU : résolveur local ou clé DQS, SORBS retiré (RES-053) | Correction des deux défauts (Spamhaus faux via résolveur public, SORBS mort) | prévu (E11) | V0 |
| C3 | **Santé par domaine et par boîte** (rebonds, plaintes 7 j, pause auto) | `Deliverability.tsx`, `domainHealthMonitor.ts`, `MailboxMonitor.tsx` | PRÉVU : écrans Délivrabilité › Domaines / IP / Boîtes / Chauffe (03 § 7.1-7.2), seuils 2 % / 0,1 % au lieu de 5 % / 1 % | Échec fermé au lieu d'ouvert | prévu (E11-E12) | V0 |
| C4 | **Alertes** (Telegram, pause d'une boîte presse malade, pause totale si 3 boîtes malades) | `pressHealthMonitor.ts`, `telegramService.ts` | PRÉVU : console + e-mail à Will ; Telegram éteint (plus de push depuis le 24/10) | Décision 03 § 15.2 à confirmer | prévu | V0 |
| C5 | **Santé du serveur** (services, files PMTA/Postfix, disque, RAM) | `VpsHealth.tsx` | PRÉVU : « Santé serveur » par l'API de métriques, sans shell | — | prévu | V0 |
| C6 | **Rapports quotidien et hebdo** | `dailyBroadcastReport.ts`, `weeklyReport.ts` | PRÉVU (02 H7, rapport du matin E11) | — | prévu | V0-V1 |
| C7 | **Rotation des domaines** (round-robin, saute les malades) | `domainRotator.ts` | PRÉVU sous forme honnête : affectation pondérée et **collante** (CHA-033) ; jamais de domaines ajoutés pour contourner un listage | — | prévu | V0 |
| C8 | **Mode auto / revue** (revue par défaut) | `outreachMode.ts` | PRÉVU (CAM-042, validation par l'owner) | — | prévu | V0 |
| C9 | **Classement IA des réponses**, variations de texte IA | `replyCategorizer.ts`, `generateBroadcastVariations.ts` | PRÉVU : règles en V0, IA en V1/V2, chaque variante validée | — | prévu | V1-V2 |
| C10 | **Campagnes presse** (5 boîtes presse@, J+5, J+10) | `PressCampaign.tsx` | PRÉVU (03 § 2.9, 7.4) avec pool à part | Corriger le registre (presse ouverte le 01/10) | prévu | V1 |
| C11 | **Synchro** avec un autre outil (Mission Control) | `MissionControlSync.tsx` | PRÉVU sous la forme synchro console ⇄ CRM (02 K1-K6) | — | prévu | V0-V1 |
| C12 | **Boîtes témoins, test de fumée, Postmaster, SNDS** | absents chez SOS-Expat | PRÉVU : témoins 06:45 en V0, Postmaster/SNDS par API en V1 | — | prévu | V0-V1 |

**Bilan bloc C** : tout le pilotage de Backlink Engine est repris (7 écrans au plan 03 § 7), sans ses défauts (seuils laxistes, échec ouvert, faux trafic, pixel, bouton « supprimer »).

---

## D. Ce que MailWizz + PowerMTA ne font PAS et que notre intégration apporte

1. **Ciblage par les données du CRM** : entreprise (secteur, taille, région, étape), fonction de la personne, événement à venir, historique de contact, en ET/OU/SAUF imbriqués, recalculé à chaque vague (CAM-007, 008, 010, 080). MailWizz ne voyait qu'une liste plate et ses champs.
2. **Une seule porte d'opposition** (`peutRecevoir`) appelée à la vague **et** moins de 15 min avant l'injection, avec retrait des messages déjà en file en moins de 5 min (CAM-003, 048). Chez SOS-Expat, la liste vivait dans MailWizz, hors de l'outil métier.
3. **Pression commerciale unique, toutes campagnes confondues** : 1 message / 5 jours ouvrés, 4 / 60 jours, 2 adresses par organisation et par vague (CAM-014, 067).
4. **Arrêt des séquences à la réponse humaine, au RDV pris, au passage client**, pause sur absence du bureau (CAM-036 à 038, 02 G4) ; MailWizz ne savait rien des RDV Calendly ni de la relation commerciale.
5. **Garde-fous de conformité codés et testés** : jamais `axion-ia.com` comme expéditeur, bloc art. 14 exigé pour un non-informé, segments sensibles fermés par défaut, pas de pixel, pas de proxy, pas de simulacre en production (gardes G1 à G12).
6. **Validation attachée à une version** : toute retouche après validation fait repasser la campagne « à valider » ; feu vert de 31 cases recalculé à chaque reprise (CAM-042, SEC-019).
7. **Isolation par client de bout en bout** : IP, domaines, boîtes, chauffe, seuils, opposition, journal et arrêt d'urgence par locataire ; le locataire imposé par l'identité de connexion au MTA ; textes légaux au nom du client (03 § 1).
8. **Chauffe pilotée par les résultats réels**, en jours effectifs, avec recul immédiat et hausse le lendemain seulement, au niveau le plus bas de IP / domaine / boîte (CHA-004, 005, 060). PowerMTA n'a pas de chauffe ; MailWizz n'appliquait pas vraiment ses quotas (audit A).
9. **Vérification d'adresse fraîche exigée à l'injection** (verdict valide de moins de 30 jours, pré-vol par tranche), sans sonde SMTP depuis nos IP (VER-001, 020).
10. **Statistiques honnêtes sans pixel** : livrés, réponses classées, RDV attribués à la campagne, à la variante et au segment, deux lectures temporelles (CON-055, 02 G3). Les ouvertures de MailWizz sont faussées par Apple MPP.
11. **Disjoncteurs à plusieurs portées** (global, locataire, IP, IP × fournisseur, domaine, boîte, campagne, variante) et **arrêt d'urgence prouvé par son effet** (CHA-017, 019).
12. **Serveur d'envoi remplaçable** derrière un contrat testé (kit de conformité, mode simulation, essai à blanc en production sans SMTP) : changer de MTA ne touche ni le CRM ni la réputation (03 § 10, 05 § A).

---

## E. Honnêteté sur les RISQUES

| # | Risque | Gravité | Ce qu'on fait |
|---|---|---|---|
| E1 | **Maturité moindre de KumoMTA** : produit plus jeune que PowerMTA (20 ans de production chez les grands routeurs), communauté d'environ 568 étoiles (fichier 05), moins de retours d'expérience publics, docs parfois contradictoires (ex. `log_oob = true` montré en exemple alors que la FAQ le déconseille). Les auteurs viennent pourtant de l'équipe de Momentum (connaissance générale, non vérifiée ici). | Moyen | Version figée par empreinte, banc jetable, kit de conformité, mise à jour seulement après passage du kit ; lecture du journal des changements à chaque version. |
| E2 | **Aucune interface native** : PowerMTA avait un moniteur web, MailWizz une interface complète. Avec KumoMTA, tout écran est à construire (Santé serveur, Files, Délivrabilité, Campagnes…). | Majeur (charge) | Déjà chiffré au plan (E12 Console V0 : 18 j) ; écran « Files d'attente » ajouté (§ F). Grafana en dépannage. |
| E3 | **Configuration en Lua** (plus TOML pour les helpers) : puissante mais c'est du code ; une erreur peut ouvrir un relais ou laisser passer un `MAIL FROM` hors registre. | Majeur | Configuration **générée** depuis la base, validée à blanc avant application, retour arrière automatique (INF-037/038) ; tests anti-relais en boîte noire ; relecture Opus sécurité de tout Lua. |
| E4 | **Support communautaire** par défaut (forum, Discord, GitHub) ; support payant cher pour notre taille (5 000 $/an et plus). | Moyen | Runbooks écrits par nous ; on achète du support seulement si le volume le justifie (V2). |
| E5 | **Fonctions à écrire nous-mêmes** (KumoMTA ne les a pas) : webhook récepteur côté CRM, homme mort, refus de `MAIL FROM` hors registre, plafond journalier par locataire, chauffe, règles TSA, classement dur/mou côté CRM, écrans. MailWizz donnait l'équivalent « clé en main », même mal appliqué. | Majeur (charge) | Presque tout est déjà dans les lots E3, E6, E8, E11, E12 (≈ 63 j). Le § F ajoute ce qui manquait. |
| E6 | **Changement de licence futur de KumoMTA** | Faible à moyen | Les versions publiées restent Apache-2.0 ; repli Postfix + rspamd 8-15 j sans nouvelle chauffe (fichier 05). |
| E7 | **Règles de backoff et de rebonds sans base éprouvée** : la table de 2 785 motifs n'a jamais été validée sur de vrais journaux et son origine est inconnue ; un faux « rebond dur » écarte un vrai prospect. | Moyen | Corpus du banc, mode « observation » d'abord (on classe sans appliquer), revue des 50 premiers rebonds durs par Will ou un agent. |
| E8 | **Volume de démarrage trop faible pour des taux significatifs** (20-50/j) | Moyen | Règles absolues sous l'échantillon (CHA-014) + boîtes témoins chaque jour. |
| E9 | **Volet lettre d'information plus pauvre que MailWizz** tant que § F n° 7 à 11 ne sont pas faits | Moyen | Les inscrire au plan, ou garder la lettre sur l'outil du site tant que V1 n'est pas atteinte. |
| E10 | **Charge totale** : V0 ≈ 138 j, V1 ≈ 115-135 j, V2 ≈ 70-90 j, plus CRM hors envoi ≈ 185 j, plus le § F ≈ 45 j. MailWizz s'installait en une journée. | Majeur (délai) | Démarrer petit en volumes, pas en fonctions (règle de Will) ; agents en parallèle ; horloges hors code (domaines de 21 jours, port 25) lancées tout de suite. |

---

## F. Écarts restants : effort et priorité

Seuls les écarts **absents du plan** ou **mal placés** sont listés ; ce qui est déjà chiffré dans les fichiers 02 et 03 ne l'est pas une seconde fois.

| # | Écart | Bloc | Effort (j-agent) | Prio | Où l'ajouter |
|---|---|---|---|---|---|
| F1 | Garde « locataire imposé par l'identité SMTP AUTH », test de falsification `X-Tenant` | A1 | 1 | V0 | lot E3 |
| F2 | Fichier de shaping : base communautaire + surcharges prudentes + groupes fournisseurs (conversion `routing-domains`), test de chargement en CI | A2, A3 | 1,5 | V0 | lot E3 |
| F3 | Règles TSA (backoff) depuis `blocking-errors`, testées par réponses simulées, reliées aux disjoncteurs du CRM | A5 | 2 | V0 | lot E8 |
| F4 | Validateur des fichiers du classifieur de rebonds en CI + mode « observation » avant application | A4, E7 | 1 | V0 | lot E6 |
| F5 | Plafond journalier dur par locataire en Lua : tests aux bornes, redémarrage, changement de jour | A17 | 1 | V0 | lot E3 |
| F6 | Écran « Files d'attente » (par locataire, fournisseur, campagne ; suspendre, retirer, âge) sur l'API d'admin | A9 | 3 | V1 | lot E12/V1 |
| F7 | Champs personnalisés par espace (remontée de P2) | B3 | 3 | V1 | lot 5 du fichier 02 → V1 |
| F8 | Double inscription + journal de consentement | B12 | 3 | V1 | lot M10 (fichier 05) |
| F9 | Formulaires intégrables + pages « merci / confirmez / désinscrit » à la marque du client | B13 | 4 | V1 | lot M10 |
| F10 | Campagnes déclenchées par un événement (remontée de P2) | B6 | 4 | V1 | lot E9-V1 |
| F11 | API publique par espace (clés, portées, signature, débit) | B15 | 5 | V1 (dès le 1er client) | lot 5 du fichier 02 |
| F12 | Export de rapport de campagne (PDF/CSV) pour un client | B14 | 1 | V1 | lot 4 du fichier 02 |
| F13 | Score SpamAssassin/rspamd du message rendu avant validation | B24 | 1 | V1 | lot E9 |
| F14 | Rotation DKIM à deux sélecteurs (déjà REQ-RES-015, remontée en V1 par l'audit, non chiffrée) | A8 | 1 | V1 | lot V1 |
| F15 | Inscriptions FBL (Microsoft JMRP/SNDS, Yahoo CFL) : runbook et suivi | A6 | 0,5 | V1 | lot E11 |
| F16 | Éditeur HTML par blocs + modèles responsive pour la lettre | B7 | 6 | V2 | lot M10 |
| F17 | Centre de préférences (thèmes) | B9 | 2 | V2 | lot M10 |
| F18 | Version web du message (jeton opaque, sans suivi) | B26 | 1 | V2 | lot M10 |
| F19 | Webhooks sortants signés par espace | B16 | 3 | V2 | lot 5 du fichier 02 |
| F20 | Réalisation `ServeurEnvoi` « relais SMTP tiers », pour la lettre seulement (si Will le veut) | B20 | 3 | V2 | fichier 05 M2 |
| F21 | Clics agrégés sans identifiant personnel (si Will le décide) | B8 | 2 | V2 | décision de Will |
| | **Total des ajouts** | | **≈ 49 j** (V0 ≈ 6,5 j ; V1 ≈ 25,5 j ; V2 ≈ 17 j, dont 5 j optionnels) | | |

Avec les relectures (+15 %) : environ 56 jours-agent, soit environ 15 % du chantier d'envoi complet (V0 + V1 + V2 ≈ 323 à 363 j).

---

## Verdict

**Oui, l'outil sera aussi complet pour ce que Will faisait réellement avec PowerMTA et MailWizz (la prospection et la presse), à condition d'ajouter au plan les écarts du § F.**

- **Côté MTA, parité atteinte** : toutes les fonctions de PowerMTA utilisées par SOS-Expat ont un équivalent dans KumoMTA (pools, débits par domaine et fournisseur, regroupement MX, rebonds, FBL, OOB, DKIM, files, réessais, TLS, routage, spool, injection). KumoMTA fait **mieux** sur MTA-STS et DANE natifs, journaux JSON poussés en continu (webhook, Kafka) au lieu de fichiers CSV, automatisation du ralentissement par règles, coût de licence nul. Il fait **moins bien** sur l'interface (aucune), la maturité, le support et la doc parfois contradictoire.
- **Côté MailWizz, parité atteinte pour la prospection**, et nettement dépassée : ciblage par les données du CRM, opposition unique revérifiée avant l'injection, pression commerciale, arrêt sur réponse ou RDV, validation par version, isolation par client, chauffe pilotée par les résultats, statistiques sans pixel.
- **Moins complet aujourd'hui** sur trois volets que MailWizz offrait d'origine :
  - **la lettre d'information à des abonnés consentants** : double inscription, formulaires, éditeur visuel, centre de préférences, version web ;
  - **la plateforme pour clients** : champs personnalisés, API publique, webhooks sortants ;
  - **le suivi des ouvertures et des clics**, refusé exprès. Ce n'est pas un manque à combler, c'est une règle.
- **À ajouter au plan** :
  - les 5 ajouts V0 (F1 à F5, ≈ 6,5 j), intégrés aux lots E3, E6 et E8 ;
  - les ajouts V1 (F6 à F15, ≈ 25,5 j), dont l'écran « Files d'attente », les champs personnalisés et l'API publique avant le premier client ;
  - le lot M10 « lettre d'information », jusqu'ici non chiffré (F8, F9, F16 à F18, ≈ 16 j) ;
  - deux décisions de Will : clics agrégés (F21) et relais tiers pour la lettre (F20).

**Décisions attendues de Will** : (1) suivi des clics agrégés sans identifiant, oui ou non ; (2) la lettre d'information passe-t-elle en V1 ou en V2 (et par le moteur du CRM, comme proposé en D-C7) ; (3) API publique dès le premier client, ou plus tard.

---

## Sources web consultées (30/10/2026)
- [KumoMTA : gestion des files (files `campagne:locataire@domaine`, `queues.toml`, pool par locataire, réessais, débits)](https://docs.kumomta.com/userguide/configuration/queuemanagement/)
- [KumoMTA : Traffic Shaping (chapitre, fichiers de shaping, MX rollup et provider blocks)](https://docs.kumomta.com/userguide/trafficshaping/)
- [KumoMTA : Traffic Shaping Automation (démon TSA, actions Suspend et SetConfig)](https://docs.kumomta.com/userguide/trafficshaping/automation/)
- [KumoMTA : `configure_bounce_classifier`](https://docs.kumomta.com/reference/kumo/configure_bounce_classifier) · [personnaliser la classification](https://docs.kumomta.com/faq/customize_bounce_classification/)
- [KumoMTA : traitement des FBL](https://docs.kumomta.com/userguide/configuration/fbl/) · [`log_arf`](https://docs.kumomta.com/reference/kumo/make_listener_domain/log_arf/) · [`log_oob`](https://docs.kumomta.com/reference/kumo/make_listener_domain/log_oob/) · [réception de courrier (FAQ)](https://docs.kumomta.com/faq/receiving_inbound_mail/)
- [KumoMTA : log hooks](https://docs.kumomta.com/reference/kumo/configure_log_hook/) · [webhooks](https://docs.kumomta.com/userguide/operation/webhooks/) · [expédier les journaux (FAQ)](https://docs.kumomta.com/faq/shipping_logs/)
- [MailWizz : liste des fonctions](https://www.mailwizz.com/features/)
- Non vérifiés en ligne ici (connaissance générale de l'agent) : API HTTP d'injection et d'administration de KumoMTA, `kcli`, `/metrics` Prometheus, spool RocksDB et backpressure, DKIM Ed25519 ; directives exactes de PowerMTA (doc non publique).
