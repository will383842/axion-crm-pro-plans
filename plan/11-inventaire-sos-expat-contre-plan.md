# 11 : Inventaire ligne à ligne des anciens outils SOS-Expat, comparé au plan « CRM Pro complet » (30/10/2026)

Question de Will : « est-ce que tout ce qui était dans SOS-Expat (suivi de chauffe, alertes, surveillance des domaines, serveurs, etc.) est bien prévu ? »


## Sources et abréviations

| Abréviation | Source | Comment elle a été lue |
|---|---|---|
| **BE** | Backlink Engine, copie locale `C:\Users\willi\Documents\Projets\VS_CODE\Sauvegardes\Sauv_backlink_engine\2026-10-17_03-00-02\code\` | Lue directement : 28 fichiers de routes (`src/api/routes/`), 63 services (`src/services/`), 10 workers et le planificateur `src/jobs/schedulers/cronScheduler.ts` (16 tâches), 44 modèles Prisma (`prisma/schema.prisma`), 28 pages (`frontend/src/pages/`), ~45 scripts (`scripts/`) |
| **CEE** | `cold_email-engine` (GitHub public, moteur PowerMTA + MailWizz) | Pas de copie locale ; d'après l'audit `_AUDIT-SOS-EXPAT-REPRISE-2026-10-30\A-cold_email-engine.md` |
| **SEP** | `sos-expat-project` / `Outil-sos-expat` (copie identique), GitHub public | Pas de copie locale (recherche disque faite) ; d'après l'audit `F-recherche-sos-expat-project.md` |
| **MC** | Mission Control, `C:\Users\willi\Documents\Projets\VS_CODE\Outils_communication\Mission_control_sos-expat\` | D'après les audits `B-…md` et `I-…md` |
| **TR** | `C:\Users\willi\Documents\Projets\VS_CODE\email_sos-expat_transactionnel\` | Lu sur place : `cron/root-crontab`, `scripts/`, `docs/` (noms seulement), et audit `C-…md` |
| **P02 / P03 / P07 / P08** | Fichiers 02, 03, 07, 08 de ce dossier | § ou numéro de ligne de leurs tableaux |
| **REQ-…** | `_PLAN-ENVOI-EMAILING-CRM-PRO-2026-09-28\04-final\REGISTRE-REQ.csv` (502 REQ) | [V0]/[V1]/[V2] = priorité du registre ; P03 § 12 dit lesquelles passent en V0 du module |

Verdicts : **REPRIS** (avec référence) · **PARTIEL** (prévu en partie ou trop tard) · **ABSENT** (nulle part dans le plan ni le registre) · **ÉCARTÉ** (exprès, avec la raison).

---

## 1. Chauffe (montée progressive)

| # | Élément ancien | Source | Ce que ça faisait | Verdict | Référence plan |
|---|---|---|---|---|---|
| 1 | Chauffe par campagne, échelle 5→500/j, avance si envoi la veille | BE `src/services/broadcast/warmupScheduler.ts` ; tâche `advance-warmup` 00:05 | Plafond quotidien par campagne qui monte chaque jour | REPRIS (en mieux : par IP, domaine et boîte, jours effectifs) | P03 § 3.1 ; CHA-002, 004, 005 ; P08 C1 |
| 2 | Chauffe presse 13 paliers (5→250/j), 50/boîte | BE `src/services/press/pressWarmup.ts`, route `/api/press/warmup`, `/warmup/advance` | Courbe dédiée aux 5 boîtes presse@ | REPRIS (pool presse séparé, même courbe CRM) | P03 § 2.9, § 3.1 |
| 3 | Chauffe par adresse 5-15-30-50/j, report au lendemain 8 h | MC `app/Models/WarmupState.php` | Quota par adresse d'envoi | REPRIS (plafond par boîte, CHA-037) | P03 § 3.1 |
| 4 | Moteur de chauffe par IP sur 70 jours, envoi étalé sur 16 h | CEE `app/services/warmup_engine.py` | Plan par IP + seuils de pause | REPRIS (courbe tronquée au palier de Will) | P03 § 3.1-3.2 ; CHA-028 |
| 5 | Ajustement horaire du débit PMTA selon un planning | SEP `warmup-hourly-adjust.py` | Change le débit chaque heure | REPRIS (répartition par poids horaires) | CHA-028, CHA-029 |
| 6 | Mise en pause des files quand le quota du jour est atteint | SEP `warmup-quota-enforcer.sh` ; BE modèle `SendingQuota` | Plafond dur du jour | REPRIS (plafond local dur sur le serveur + budget CRM) | INF-023 ; CHA-004 ; P08 A17, F5 |
| 7 | Arrêt d'urgence de la chauffe (pause PMTA, débit 1/h) + reprise | SEP `warmup-killswitch.sh`, `warmup-resume.sh` | Coupure d'urgence manuelle | REPRIS (« Tout arrêter » en 2 clics, levée par `approve`) | CHA-019, CHA-048 ; P03 § 3.3 |
| 8 | Pause 72 h si rebonds > 2 %, 96 h si plaintes > 0,03 %, arrêt si > 5 % / 0,1 % | CEE `app/config.py`, `warmup_engine.py` | Seuils automatiques | REPRIS (2 % rebonds, 0,1 % plaintes, règles absolues sous échantillon) | P03 § 3.2 ; CHA-013, 014, 021 |
| 9 | Retour au palier précédent si rebond > 2 %, arrêt 48 h si plainte > 0,1 %, engagement mini 5 % | `VS_CODE\SYSTEME-ENVOI-MASSIF-PROFESSIONNEL.md` (audit C) | Doctrine de chauffe | REPRIS ; « 5 % d'engagement » à redéfinir (pas de pixel) : décision de Will | P03 § 3.2 |
| 10 | Rapport quotidien de chauffe | SEP `warmup-daily-report.sh` (Telegram) | Bilan du jour | REPRIS (rapport du matin console + e-mail) | CON-062 ; P03 lot E11 |
| 11 | Courbe et chronologie de chauffe par boîte | BE `/mailbox/warmup-stats`, `/warmup-timeline`, `MailboxMonitor.tsx` | Graphique de progression | REPRIS | P03 § 7.1 ; CON-051 (onglet Historique) |
| 12 | Machine d'états des IP (actif, retrait, repos, chauffe, quarantaine) | CEE `app/services/ip_manager.py` | Cycle de vie des IP | REPRIS (6 états, chaque état a une sortie : corrige le bug « quarantaine sans sortie ») | RES-001, 002 ; P03 § 3.3 |
| 13 | IP de réserve, bascule si une IP est listée | CEE `scripts/ip-recovery.sh`, audit C | Bascule automatique | REPRIS (redistribution bornée, V1) | CHA-046 |
| 14 | Rotation mensuelle des IP « pour user la réputation » | CEE `monthly_rotation()`, `scripts/ip-rotation.sh` | Changer d'IP chaque mois | ÉCARTÉ (contournement, bug qui retirait toutes les IP) | P03 § 3.1 (« jamais pour contourner ») |
| 15 | Chauffe par faux trafic (Mailflow.io) sur les boîtes presse@ | SEP `infra/mail-server/README.md` | Échanges simulés | ÉCARTÉ (faux trafic, interface « qui ment ») | CHA-035 ; P08 C1 |
| 16 | Jours de chauffe comptés même sans envoi (MC) ou par lignes de stats (CEE) | MC `WarmupState.php`, CEE bug 3 | Défaut de calcul | ÉCARTÉ (corrigé : jours effectifs) | CHA-005 |
| 17 | Inactivité : rien de prévu | — | — | REPRIS en plus (recul après 7/30/90 jours) | CHA-006 |

## 2. Alertes (canaux et seuils)

| # | Élément ancien | Source | Ce que ça faisait | Verdict | Référence plan |
|---|---|---|---|---|---|
| 18 | Alertes Telegram (envoi générique, test, réponse reçue, prospect gagné, backlink perdu/vérifié, rapport hebdo, rapport diffusion, alerte diffusion) | BE `src/services/notifications/telegramService.ts` ; route `/settings/telegram` | Push au téléphone | ÉCARTÉ (décision de Will du 24/10 : plus de push) ; remplacé par console + e-mail ; connecteur Telegram facultatif éteint (V1) | P03 § 7.8 ; P02 L4 ; CON-025 remplacée en V0 |
| 19 | Service Telegram Laravel (plusieurs robots, boutons) | MC `app/Services/Social/TelegramAlertService.php` | Idem | ÉCARTÉ (même raison) ; réutilisable en 0,3 j si Will rallume | P03 § 7.8 |
| 20 | Alertes Telegram du moteur (chauffe, liste noire, santé) | CEE `app/services/telegram_alerter.py` | Idem | ÉCARTÉ (même raison) | — |
| 21 | Réponses reçues transférées sur Telegram | SEP `forward-replies-telegram.py` | Prévenir Will d'une réponse | PARTIEL : écran Réponses + alerte si une réponse « intéressé » attend > 24 h ; **pas d'avis immédiat par e-mail** | P02 F6, F8 ; voir ABSENT n° 2 |
| 22 | Analyse des journaux PMTA toutes les 4 h, problèmes envoyés sur Telegram | SEP `problem-emails-tracker.sh` | Détection des envois en échec | REPRIS (évaluation toutes les 5 min, signaux faibles) | CHA-018 ; CON-064 |
| 23 | 7 alertes Alertmanager (PMTA arrêté, rebonds élevés, IP listée, disque, file, moteur arrêté, mémoire) | CEE `monitoring/alert-rules.yml` | Alertes techniques | REPRIS | P08 A15 ; INF-046 ; P02 L4, L7 |
| 24 | Bandeau d'alertes : rebond > 5 % / > 10 %, domaine listé, > 10 échecs en 24 h | MC `OutreachController::alerts` | Alertes en tête d'écran (squelette : seule « échecs 24 h » réelle) | REPRIS (règles fermées, écran Alertes, cloche) | CON-023, 024, 048 ; P03 § 7.7 |
| 25 | Seuils santé presse 3 % rebonds / 0,1 % plaintes, échantillon mini 5 | BE `pressHealthMonitor.ts` | Pause d'une boîte malade | REPRIS (table unique des seuils) | CHA-013 ; P03 § 3.2 |
| 26 | Regroupement / dédoublonnage des alertes | absent chez SOS-Expat | — | REPRIS en plus (regroupées par cause, 1 message / 15 min) | CON-048 |
| 27 | Bouton « alerte de test » | BE `sendTestNotification` | Vérifier le canal | REPRIS | P02 L4 |

## 3. Surveillance des domaines (DNS, authentification, expiration, réputation)

| # | Élément ancien | Source | Ce que ça faisait | Verdict | Référence plan |
|---|---|---|---|---|---|
| 28 | Contrôle SPF / DKIM / DMARC des domaines d'envoi (résolveur Quad9) | BE `settings.ts` route `/sending-domains/dns-check` | Vérifie 3 TXT par domaine | REPRIS (chaque jour 06:30 + à la demande, plus PTR, MX, MTA-STS, TLS-RPT, DNSSEC) | RES-023 ; P03 § 7.2 |
| 29 | Contrôle SPF/DKIM/DMARC/PTR/MX | CEE `app/services/dns_validator.py` | Idem côté moteur | REPRIS | RES-023 |
| 30 | Gabarits d'enregistrements DNS à poser | CEE `deploy/dns-helper.sh`, `dns/dns-templates.md` | Texte des enregistrements | REPRIS (plan DNS généré, assistant) | RES-011, RES-006 |
| 31 | Génération des clés DKIM | CEE `scripts/generate-dkim.sh` ; OpenDKIM (SEP) | Clés par domaine | REPRIS (un seul signataire, clés générées sur le serveur d'envoi) | INF-027 ; P08 A8 |
| 32 | DKIM sur un seul sélecteur, sans rotation | CEE | Défaut | REPRIS en mieux (rotation 2 sélecteurs, V1) | RES-015 ; P08 F14 |
| 33 | MTA-STS sur les 5 domaines | SEP `infra/mail-server/` | Politique TLS | REPRIS (contrôlé V1, servi V2) | RES-018, RES-023 |
| 34 | Santé par domaine d'envoi (rebonds 5 %, plaintes 1 %, 7 j, échantillon 20) | BE `outreach/domainHealthMonitor.ts`, route `/sent-emails/domain-health`, `Deliverability.tsx` | Tableau par domaine + exclusion des domaines malades | REPRIS (seuils durcis 2 % / 0,1 %) | P03 § 7.2 ; RES-056 ; P08 C3 |
| 35 | Table `domain_health` (squelette jamais remplie) | MC | — | ÉCARTÉ (vide) ; remplacé par le n° 34 | — |
| 36 | Expiration des domaines | absent chez SOS-Expat (aucun code trouvé) | — | PARTIEL : prévu mais en V2 (RDAP + certificats) | RES-024 [V2] ; voir ABSENT n° 4 (à remonter) |
| 37 | Rapports DMARC agrégés (lecture `rua`) | SEP `dmarc-parser.py` | Analyse des rapports DMARC | REPRIS, mais **contradiction** : RES-017 listée en V0 (P03 § 12) et « ingestion DMARC » dans la V1 (P03 § 13) | RES-016, RES-017 ; voir n° 157 |
| 38 | Passé et âge d'un domaine avant usage | absent chez SOS-Expat | — | REPRIS en plus (âge ≥ 21 j en V0, DBL/SURBL au passé en V2) | RES-008, RES-009 |
| 39 | Réputation Google Postmaster / Microsoft SNDS / JMRP | absents chez SOS-Expat | — | REPRIS en plus (V1) | RES-055, RES-036, RES-066 |
| 40 | Cloudflare (seulement une mention « Email Routing ») | CEE `deploy/dns-helper.sh` | Aucune intégration | REPRIS en plus (poussée DNS par API, V1) | RES-063 |
| 41 | `axion-ia.com` jamais expéditeur | — | — | REPRIS en plus (garde G1, DMARC p=reject vérifié) | P03 § 8 G1 |

## 4. Listes noires

| # | Élément ancien | Source | Ce que ça faisait | Verdict | Référence plan |
|---|---|---|---|---|---|
| 42 | 7 listes DNS sur l'IP (Spamhaus ZEN, Barracuda, SpamCop, SORBS, PSBL, CBL, UBL) via Quad9 | BE `src/api/routes/mailbox.ts` route `/blacklists` ; section « Blacklists · IP » de `MailboxMonitor.tsx` | Contrôle à la demande | REPRIS (résolveur local ou clé DQS, SORBS retiré, chaque heure) | RES-053 ; P03 § 7.1 ; P08 C2 |
| 43 | 9 listes interrogées toutes les 4 h, passage en attente | CEE `app/services/blacklist_checker.py`, `scripts/check-blacklists.sh`, `blacklist-protection.sh` | Surveillance + pause | REPRIS (listage = pause de la ressource + runbook) | RES-053 ; P03 § 3.2 ; SEC-021 |
| 44 | Listes noires des domaines d'envoi et des domaines des liens | absent chez SOS-Expat | — | REPRIS en plus (DBL, SURBL, URIBL chaque heure) | RES-054 |
| 45 | Domaine destinataire : Spamhaus DBL + Google Safe Browsing | BE `src/services/safety/domainChecker.ts` | Écarte les destinataires douteux | PARTIEL : DBL/SURBL destinataire en V2 ; Safe Browsing non repris (peu utile en B2B) | VER-033 [V2] |
| 46 | Refus SMTP pour réputation → ralentir (liste `blocking-errors`) | TR `pmta/config` | Repli automatique | REPRIS (règles TSA + disjoncteur IP × fournisseur) | P08 A5, F3 ; CHA-016, CHA-069 |

## 5. Santé des serveurs (CPU, disque, files, ports)

| # | Élément ancien | Source | Ce que ça faisait | Verdict | Référence plan |
|---|---|---|---|---|---|
| 47 | Charge CPU, RAM, disque, temps de marche | BE `src/api/routes/vpsHealth.ts`, `VpsHealth.tsx` | Écran Santé du VPS (seuils disque 80/90 %, RAM 85/95 %) | REPRIS (toutes les 5 min, par l'agent, sans shell) | INF-045, INF-046 ; P03 § 7.6 |
| 48 | Services actifs (postfix, dovecot, pmta, nginx, opendkim, docker) par systemctl et sonde TCP | BE `vpsHealth.ts` | État des services | REPRIS (services attendus par rôle) | INF-045 |
| 49 | Taille des files PMTA et Postfix, dernière activité PMTA | BE `vpsHealth.ts` | File d'attente, dernier envoi | REPRIS (taille et âge des files, dernier envoi) ; écran « Files d'attente » détaillé en V1 | INF-045 ; P08 A9, F6 |
| 50 | Contrôle PMTA, disque, mémoire, file | CEE `app/services/health_monitor.py`, `scripts/health-check.sh` | Idem côté moteur | REPRIS | INF-045 |
| 51 | Métriques Prometheus (13) + tableau Grafana (9 panneaux) | CEE `app/api/routes/metrics.py`, `monitoring/grafana/dashboards/email-engine.json` | Supervision technique | REPRIS (métriques KumoMTA + Grafana en dépannage) | P08 A15 |
| 52 | Incident « relais ouvert » PMTA listé Spamhaus (10/04/2026) | SEP `docs/audits/AUDIT-EMAIL-INFRASTRUCTURE-COMPLET.md` | Aucune sonde ne l'avait vu | REPRIS en mieux : anti-relais 4 couches, sonde externe M4, balayage des ports IPv4/IPv6, coupure automatique | INF-020, 047, 048 ; CHA-020, 048 |
| 53 | Homme mort (le serveur s'arrête si le CRM se tait) | absent chez SOS-Expat | — | REPRIS en plus | INF-025 ; P08 A19 |
| 54 | Contrôle de cohérence base ↔ configuration réelle du MTA, pause si écart | CEE `deploy/validate-coherence.sh`, `scripts/check-sender-coherence.sh` | Détecte une configuration qui a dérivé | PARTIEL : dérive surveillée seulement en V2 ; en V0 le serveur est réglé par runbook | INF-040 [V2], INF-024 ; voir ABSENT n° 3 |
| 55 | Réparation de déploiement du moteur | SEP `FIX-EMAIL-ENGINE-DEPLOYMENT.sh` | Script de dépannage | ÉCARTÉ (propre à FastAPI/Celery) | — |
| 56 | Déploiement multi-VPS (6 serveurs PMTA) | CEE `deploy/deploy-all.sh`, `deploy/vps2…6-pmta/` | Installation des serveurs | REPRIS sous forme d'assistant « Ajouter un serveur » (V1) ; multi-serveurs V2 | INF-041, INF-066 |
| 57 | Mises à jour, redémarrages de services | absents (à la main) | — | REPRIS en plus (écran Mises à jour, redémarrage en fenêtre) | INF-073, INF-074 |
| 58 | Battement externe (qui surveille le surveillant ?) | absent chez SOS-Expat | — | PARTIEL : prévu en V2 | INF-049 [V2] ; critique 06 n° 8 |

## 6. Surveillance des boîtes (connexion, quota, préparation)

| # | Élément ancien | Source | Ce que ça faisait | Verdict | Référence plan |
|---|---|---|---|---|---|
| 59 | Score de préparation 0-100 par boîte (chauffe, stats froides, listes noires) | BE `mailbox.ts` route `/readiness`, `computeReadiness()` | « Prête pour campagne » | REPRIS (score 0-100 pondéré par ressource, V1) | RES-052 ; P03 § 7.1 |
| 60 | Statistiques par boîte (envoyés, livrés, rebonds durs, plaintes, ouverts, cliqués) lues dans les CSV PMTA | BE `mailbox.ts` routes `/stats`, `/timeline` | Activité par boîte | REPRIS sans ouvertures ni clics | RES-056 ; P03 § 7.1 |
| 61 | Vérification de connexion des 5 boîtes presse@ | BE `press/sender.ts` `verifyPressInboxes()`, route `/api/press/verify-inboxes` | Teste l'accès SMTP/IMAP | REPRIS (3 échecs IMAP → pause technique ; identification refusée → alerte) | CHA-051 |
| 62 | Boîte pleine (quota) | absent chez SOS-Expat | — | REPRIS en plus (boîte pleine → pause technique) | CHA-051 |
| 63 | Pause / reprise d'une boîte presse, pause globale si 3 boîtes malades sur 5 | BE `pressHealthMonitor.ts`, routes `/api/press/pause`, `/resume`, `/inboxes/:inbox/resume` ; tâche `press-health-check` chaque heure | Disjoncteur boîte + global | REPRIS (disjoncteurs par boîte, pool, global) | CHA-017 ; P03 § 3.3, § 7.4 |
| 64 | Lecture des boîtes (liste, message, supprimer, restaurer) | BE `src/api/routes/mailboxes.ts`, `mailbox/maildirReader.ts`, `Mailboxes.tsx` | Webmail intégré | PARTIEL : lecture en fil dans Réponses ; suppression de messages ÉCARTÉE | P03 § 7.0 ; CAM-053 |
| 65 | Boîtes témoins et test de placement | absent chez SOS-Expat | — | REPRIS en plus (test de fumée 06:45) | RES-057 ; INF-050 |
| 66 | Hébergement des boîtes presse@ sur le serveur d'envoi lui-même (Postfix + Dovecot) | SEP `infra/mail-server/README.md` | Tout sur une machine | REPRIS en mieux (boîtes dans un compte distinct) | RES-021 |

## 7. Rebonds, plaintes, FBL, DMARC

| # | Élément ancien | Source | Ce que ça faisait | Verdict | Référence plan |
|---|---|---|---|---|---|
| 67 | Table de 2 785 motifs de rebonds (18 catégories) | TR / CEE `pmta/bounce-classifications` | Classement dur / mou | REPRIS après vérification de l'origine + test sur vrais journaux, mode observation d'abord | P08 A4, F4 ; CHA-025 |
| 69 | Traitement des rebonds (script) | SEP `bounce-processor.py` | Applique les rebonds | REPRIS (service unique `AppliquerRetour`) | P03 § 6 ; RET-002 |
| 70 | Pipe de comptabilité PMTA vers l'API, renvoi HMAC | CEE `scripts/bounce-pipe.sh`, `delivery-pipe.sh` | Remontée des événements | REPRIS sous forme KumoMTA (log hook → webhook privé + tirage nocturne) | P03 § 6 ; P08 A10 |
| 71 | Webhook MailWizz (rebond, plainte, ouverture, clic, désinscription) | BE `webhooks.ts` route `/mailwizz`, `outreach/webhookHandler.ts` | Réception d'événements | REPRIS pour le fond (machine d'états) ; MailWizz ÉCARTÉ | P03 § 6 |
| 72 | Webhook « email-engine » | BE `webhooks.ts` route `/email-engine` | Idem pour le moteur | ÉCARTÉ (moteur abandonné) | — |
| 73 | Webhook rebond PMTA (route publique) | MC `OutreachController::pmtaBounce` | Idem | REPRIS en mieux (liaison privée, HMAC fermé) | P03 § 6 |
| 74 | HMAC des webhooks ouvert si secret vide | CEE `app/api/routes/webhooks.py` (bug 4) | Faille | ÉCARTÉ (secret absent = refus) | P03 § 6 |
| 75 | File de reprise des webhooks (JSONL) | CEE `app/services/retry_queue.py` | Rejeu | REPRIS (rejeu 72 h, idempotence par clé unique) | P03 § 6 |
| 76 | Rebond mou compté jusqu'à 3 puis traité comme dur | BE `webhooks.ts` l. 785-806 | Règle de suppression | REPRIS (compteur en base) | RET-013 ; P03 § 5 |
| 77 | Plaintes FBL (tâche MailWizz `feedback-loop-handler` toutes les 5 min) | TR `cron/root-crontab` | Lecture des plaintes | REPRIS (ARF RFC 5965 par IMAP, inscriptions FBL guidées) | RET-016, 017 ; P08 A6, F15 |
| 78 | Rebonds asynchrones (tâche MailWizz `bounce-handler`) | TR `cron/root-crontab` | Lecture des DSN | REPRIS (VERP sur `bounce.`) | RET-009 ; P08 A7 |
| 79 | Journal de livraison (tâche `process-delivery-and-bounce-log`) | TR `cron/root-crontab` | Import des journaux | REPRIS (log hook + réconciliation) | INF-055 ; RET-046 |
| 80 | Santé des canaux de retour | absent chez SOS-Expat | — | REPRIS en plus (aucun événement depuis 2 h → arrêt) | RET-035 ; CHA-048 |
| 81 | Rapports DMARC | SEP `dmarc-parser.py` | voir n° 37 | REPRIS (contradiction V0/V1 à trancher) | RES-017 |

## 8. Traitement des réponses

| # | Élément ancien | Source | Ce que ça faisait | Verdict | Référence plan |
|---|---|---|---|---|---|
| 82 | Relève IMAP toutes les 5 min | BE `outreach/imapMonitor.ts` ; tâche `imap-check` ; worker `replyWorker.ts` | Récupère les réponses | REPRIS | RES-041 ; P02 F1 |
| 83 | Classement IA des réponses (intéressé, pas intéressé…) | BE `replyCategorizer.ts`, `llm/prompts/categorizeReply.ts` | Tri automatique | REPRIS (règles en V0, IA en V1/V2) | P02 F2 ; P03 § 2.8 ; P08 C9 |
| 84 | Écran Réponses + réponses par campagne | BE `routes/replies.ts`, `Replies.tsx`, `broadcast.ts` `/:id/replies` | Liste des réponses | REPRIS | CAM-053 ; P02 F6 |
| 85 | Arrêt de la séquence à la réponse | BE `sequenceAdvancer.ts` | Stop relances | REPRIS (réponse, RDV, passage client, absence = pause) | CAM-036-038 ; P02 F9 |
| 86 | Avis immédiat « un prospect a répondu » | BE `notifyProspectReplied()` ; SEP `forward-replies-telegram.py` | Push instantané | PARTIEL (voir n° 21) | P02 F8 ; ABSENT n° 2 |
| 87 | Répondre depuis l'outil | absent (MC renvoyait au webmail) | — | REPRIS en plus (V1) | CAM-054 ; P02 F7 |

## 9. Suppression, désinscription

| # | Élément ancien | Source | Ce que ça faisait | Verdict | Référence plan |
|---|---|---|---|---|---|
| 88 | Liste de suppression (adresse normalisée, motif, source) + vérification en lot | BE `suppression/suppressionManager.ts`, `routes/suppression.ts`, `Suppression.tsx` | Liste unique | REPRIS (une seule porte `peutRecevoir()`, empreintes) | RET-028 ; P03 § 5, § 7.5 |
| 89 | Bouton « retirer » une suppression sans motif | BE `Suppression.tsx`, `DELETE /suppression/:id` | Levée libre | ÉCARTÉ (levée motivée, jamais pour plainte ou opposition) | RET-031 |
| 90 | Désinscription GET/POST, jeton signé, pied de page par langue | BE `routes/unsubscribe.ts`, `press/unsubscribeToken.ts`, `press/unsubscribeFooter.ts` | Lien de désinscription | REPRIS (RFC 8058 un clic, `mailto:`, page à l'entité) | RET-010, 020-027 ; P03 § 5 |
| 92 | Domaines bloqués | MC `BlockedDomainService.php` | Exclusion d'un domaine | REPRIS (opposition par domaine entier) | RET-026 ; P02 F3 |
| 93 | Opposition par réponse « STOP » | absente | — | REPRIS en plus | RET-025 |

## 10. Étiquettes, contacts, vérification d'adresses

| # | Élément ancien | Source | Ce que ça faisait | Verdict | Référence plan |
|---|---|---|---|---|---|
| 94 | Étiquettes par catégorie (CRUD, sur prospects, campagnes, modèles) | BE `routes/tags.ts`, modèles `Tag`, `ProspectTag`, `CampaignTag`, `TemplateTag` | Ciblage par tags (jamais codé côté envoi) | REPRIS (étiquettes CRM existantes, ciblage ET/OU/SAUF) | CAM-008 ; P02 C2-C3 ; P03 § 2.2 |
| 95 | Détection automatique des étiquettes | BE `tags/tagDetector.ts` | Pose des tags à l'import | PARTIEL (familles/segments automatiques ; pas de détecteur de tags dédié) | P02 C ; Segments |
| 96 | Correspondance type de contact → catégorie | BE `contactTypeMappings.ts`, `prospects/contactTypeMapper.ts` | Classement des contacts | REPRIS (familles de segments) | CAM-006 |
| 97 | Import CSV en masse avec doublons, ajout rapide | BE `ingestion/csvParser.ts`, `dedup/deduplicator.ts`, `BulkImport.tsx`, `QuickAdd.tsx` | Alimentation | REPRIS | P02 B3-B4, A (ajout rapide), doublons |
| 98 | Vérification d'adresses (syntaxe, MX, jetables, rôles, fautes de frappe) | BE `email/emailValidator.ts`, `outreach/emailValidator.ts` ; CEE `email_validator.py` ; MC `EmailVerificationService.php` | Avant envoi | REPRIS (cascade locale + fournisseur, verdict < 30 j exigé) | P03 § 4 ; VER-* |
| 99 | Audit qualité des contacts presse avant campagne (valide / risqué / invalide) | BE `press/emailAudit.ts` ; scripts `press-contacts-audit.ts`, `contacts-full-audit.ts` | Réduire les rebonds | REPRIS (pré-vol, écran Vérification) | VER-020, VER-029 |
| 100 | Suggestions de recontact | BE `prospects.ts` `/recontact-suggestions`, `RecontactSuggestions.tsx` | Relancer d'anciens contacts | REPRIS (P2) | P02 D8 |
| 101 | Fiche prospect détaillée | BE `ProspectDetail.tsx` | Vue 360° | REPRIS | CAM-057 |

## 11. Campagnes, séquences, modèles, tests A/B

| # | Élément ancien | Source | Ce que ça faisait | Verdict | Référence plan |
|---|---|---|---|---|---|
| 102 | Campagnes (créer, inscrire, stats, supprimer) | BE `routes/campaigns.ts`, `Campaigns.tsx`, `CampaignsHub.tsx` | Prospection | REPRIS | P03 § 2 ; lot E9 |
| 103 | Diffusion en masse : créer, aperçu, démarrer, pause, contacts éligibles, stats, destinataires | BE `routes/broadcast.ts` (22 routes), `broadcastManager.ts`, `Broadcast.tsx` | Campagne de masse | REPRIS (assistant 6 étapes, feu vert, pause/annulation) | P03 § 2.5-2.6, § 7.3 ; CON-013 |
| 104 | Exclusions et destinataires manuels par campagne | BE `broadcast.ts` `/exclusions`, `/manual-recipients` | Ajuster la cible | REPRIS (V1) | CAM-012 |
| 105 | **Envoi d'un test** d'une campagne à une adresse | BE `broadcast.ts` `POST /:id/test-send` | Voir le message réel avant lancement | PARTIEL : mode « recette » global (liste blanche) et « s'envoyer un test » dans la mise en route ; **pas de bouton par campagne/modèle** | INF-060 ; P07 l. 761 ; ABSENT n° 1 |
| 106 | Santé de campagne (pause si mauvaise) | BE `checkCampaignHealth()` | Disjoncteur campagne | REPRIS | CHA-017 (portée campagne) |
| 107 | Séquences de relance (toutes les 10 min) | BE `sequenceAdvancer.ts`, `broadcastSequenceAdvancer.ts`, workers `sequenceWorker`, tâches `advance-sequence`, `advance-broadcast-sequence` ; MC `ProcessSequencesJob` | Étapes et délais | REPRIS (1 à 4 étapes, jours ouvrés) | CAM-035 ; P03 § 2.4 |
| 108 | Traitement des campagnes actives toutes les 10 min | BE tâche `process-broadcast`, `broadcastWorker.ts` | Moteur d'envoi | REPRIS (vagues, tranches, file Horizon) | CHA-029 ; CAM-075 |
| 109 | Nouvel essai des appels MailWizz échoués chaque heure | BE tâche `retry-failed-outreach` | Reprise | REPRIS (échec fermé, report sur 4xx) | CAM-075 ; CHA-030 |
| 110 | File atomique (verrou, lots de 20) | MC `ProcessEmailQueueJob.php` | Évite le double envoi | REPRIS (une tâche par message, idempotence) | CAM-075 |
| 111 | Mode « auto / revue » (revue par défaut), brouillons, approuver / refuser / tout approuver | BE `outreachMode.ts`, `sentEmails.ts` `/drafts`, `/approve`, `/reject`, `/approve-all` ; MC `reviewQueue`, `approveBatch` | Validation par Will | REPRIS (validation attachée à une version ; message par message en V1 pour la presse) | CAM-042, CAM-044 ; P03 § 2.6 |
| 112 | Inscription automatique des nouveaux prospects toutes les 10 min | BE `autoEnrollmentWorker.ts`, `autoEnrollment/campaignSelector.ts` | Ajoute seul des contacts aux campagnes | PARTIEL / ÉCARTÉ en partie : cible recalculée à chaque vague mais validée ; messages déclenchés par événement en V1 | CAM-008, CAM-039 ; P02 E19 ; P08 F10 |
| 113 | Modèles de messages par langue, traduction IA | BE `routes/messageTemplates.ts` (`/:id/translate`), `templates.ts`, `MessageTemplates.tsx` | Modèles multilingues | PARTIEL : modèles versionnés FR ; traduction écartée (FR canonique) | CAM-023, 024 ; P03 § 2.3 |
| 114 | Choix automatique du modèle selon type, langue, étiquette | BE `messageTemplateSelector.ts`, `templateSelector.ts` | Sélection | PARTIEL (modèle choisi par étape de séquence, pas par règle automatique) | P03 § 2.3-2.4 |
| 115 | Variables et rendu de modèle | BE `messaging/templateRenderer.ts` ; CEE Jinja2 sans bac à sable | Personnalisation | REPRIS (variables en liste blanche, aperçu) ; Jinja libre ÉCARTÉ | CAM-024 |
| 116 | Rédaction et personnalisation par IA, coût en jetons | BE `llm/prompts/generateOutreachEmail.ts`, `personalizeEmail.ts` ; MC `AiEmailGenerationService.php` | E-mail écrit par l'IA | PARTIEL : V2 (chaque texte validé) ; plafond de coût IA par espace existe | CAM-026, 028, 030 [V2] ; P02 E13 ; critique 06 l. 49 |
| 117 | Variations IA d'un même texte (cache) | BE `generateBroadcastVariations.ts`, `variationCache.ts`, routes `/variations` | Éviter un texte identique | PARTIEL (V1/V2, chaque variante validée) | P02 E13 ; P08 C9 |
| 118 | Tests A/B et résultats | BE `sentEmails.ts` `/ab-stats`, `AbTestResults.tsx` | Comparer des variantes (sur ouvertures) | REPRIS (V1, métrique = réponses positives) | CAM-031 ; P08 B23 |
| 119 | Plafond quotidien par type de contact | MC `OutreachConfig` | Limite par famille | REPRIS (budget par campagne et pression par personne) | P03 § 2.5 ; CAM-014, 067 |
| 120 | Cadence des séquences chatter (J0, J2, J5, J10) | TR `templates/campaign/` | Modèle de cadence | REPRIS (principe) ; textes SOS ÉCARTÉS (promesses de gains) | P03 § 2.4 |
| 121 | Squelettes HTML et lettre d'information (blog, promo, récap) | TR `templates/transactional/`, `templates/newsletter/` | Mise en forme | PARTIEL : texte brut d'abord ; éditeur par blocs pour la lettre en V2 | P08 B7, F16 |
| 122 | Ouvertures et clics (pixel, redirection) | BE `routes/tracking.ts` ; MC `/track/open`, `/track/click` | Suivi | ÉCARTÉ (règle : aucun pixel, faussé par Apple MPP) | G5 ; SEC-016 ; P08 B8 |
| 123 | Prospection par formulaire de contact (file des sites sans e-mail, message généré, contact manuel noté) | BE `FormOutreach.tsx`, `scraping/contactFormDetector.ts`, route `generate-form-message` | Contacter par le formulaire du site | ABSENT (seules les étapes manuelles « appel, courrier » sont prévues) | P02 E4 ; ABSENT n° 5 |

## 12. Presse

| # | Élément ancien | Source | Ce que ça faisait | Verdict | Référence plan |
|---|---|---|---|---|---|
| 124 | Campagne presse : 5 boîtes presse@ en rotation, relances J+5 / J+10, lancer, pause, reprise | BE `PressCampaign.tsx`, `press/sender.ts`, `pressOutreachWorker.ts`, `routes/press.ts` | Envoi aux journalistes | REPRIS (pool presse à part, validation, jamais en masse) | P03 § 2.9, § 7.4 ; P08 C10 |
| 125 | Modèles de pitch par angle et langue | BE `press/pitchRenderer.ts`, `press/templates/pitches.ts`, `PressTemplates.tsx`, `scripts/seed-media-templates.ts` | Textes presse | REPRIS (angle, communiqué par lien) ; langues ÉCARTÉES | P03 § 2.9 |
| 126 | Statistiques presse, santé presse | BE `/api/press/stats`, `/api/press/health`, `/health/check-now` | Suivi | REPRIS | P03 § 7.4 |
| 127 | Résumé presse quotidien 20:00 | BE `press/pressDailyDigest.ts`, `/digest/send-now` | Bilan du jour | REPRIS (dans le rapport quotidien ; pas de résumé presse séparé) | CON-062 |
| 128 | Rattrapage d'inscription presse | BE `scripts/press-enqueue-rattrapage.ts` | Remettre en file | REPRIS (reprise idempotente) | CAM-075 |
| 129 | Scraping de journalistes, communiqués en PDF/Word | MC `JournalistController`, `PressController` | Sourcing et documents | ÉCARTÉ (scraping) ; communiqué hors CRM, joint par lien | P03 § 2.9 |

## 13. Statistiques, tableaux de bord, rapports

| # | Élément ancien | Source | Ce que ça faisait | Verdict | Référence plan |
|---|---|---|---|---|---|
| 130 | Tableau de bord (aujourd'hui, stats, entonnoir, vue outreach, campagnes) | BE `routes/dashboard.ts` (6 routes), `Dashboard.tsx` | Accueil | REPRIS (« que dois-je faire aujourd'hui ? ») | CON-010 ; P03 § 7.7 ; P07 |
| 131 | Vue délivrabilité globale | BE `sentEmails.ts` `/deliverability-overview`, `Deliverability.tsx` | Santé d'ensemble | REPRIS | CON-017 ; P03 § 7.2 |
| 132 | Liste des e-mails envoyés (détail, par prospect) | BE `sentEmails.ts`, `SentEmails.tsx` | Suivi par e-mail | REPRIS (fiche 360°, suivi de campagne) | CAM-057 ; P02 E17 |
| 133 | Statistiques de campagne (par statut, étape, type) | MC `OutreachController::stats` ; BE `/campaigns/:id/stats` | Agrégats | REPRIS (indicateurs uniques, deux lectures) | CON-028, 054, 055 ; P03 § 2.10 |
| 134 | Statistiques du jour à 23:59 | BE tâche `daily-stats` | Figer le jour | REPRIS (entrepôt horaire sans donnée personnelle) | CON-054 |
| 135 | Rapport quotidien de diffusion 21:00 | BE `reporting/dailyBroadcastReport.ts`, tâche `daily-broadcast-report` | Bilan | REPRIS | CON-062 ; lot E11 |
| 136 | Rapport hebdomadaire dimanche 20:00, archivé | BE `reporting/weeklyReport.ts` (`storeWeeklyReport`), `Reports.tsx`, `routes/reports.ts` | Bilan hebdo | REPRIS (quotidien, hebdo, mensuel figés et archivés) | CON-062 |
| 137 | Export d'un rapport pour un client | absent | — | REPRIS en plus (V1) | P08 F12 |

## 14. Sauvegardes, tâches planifiées, journaux

| # | Élément ancien | Source | Ce que ça faisait | Verdict | Référence plan |
|---|---|---|---|---|---|
| 138 | Sauvegarde hebdomadaire automatique avec alerte, contrôle d'état | TR `scripts/backup-auto-telegram.ps1`, `check-backup-status.ps1`, `TaskScheduler-BackupHebdo.xml`, `docs/GUIDE-BACKUP-AUTOMATIQUE-HEBDOMADAIRE.md` | Sauvegarde du serveur d'envoi | REPRIS (sauvegarde chiffrée du serveur d'envoi à chaque config + chaque semaine ; écran Sauvegardes) | INF-054, INF-077 ; P02 L1-L2 |
| 139 | Sauvegardes quotidiennes de tout | CEE `scripts/backup-all.sh`, `backup-*.ps1` | Idem | REPRIS (CRM : quotidien chiffré + Backblaze, hors site quotidien à ajouter) | P02 L1, L2 |
| 140 | Guides de récupération production | TR `docs/GUIDE-RECUPERATION-PRODUCTION-HETZNER.md`, `RECUPERATION-RAPIDE.md` | Remise en état | REPRIS (resynchro obligatoire après restauration, runbooks) | INF-057, INF-058, SEC-023 |
| 141 | 8 tâches cron MailWizz (envoi, file, transactionnel, rebonds, FBL, journaux, horaire, quotidien) | TR `cron/root-crontab` | Moteur MailWizz | ÉCARTÉ (MailWizz) ; fonctions reprises par les files Horizon et le battement du moteur | INF-032 retirée → CAM-075 ; INF-043 |
| 142 | 16 tâches répétées BullMQ (enrichissement 2 min, inscription 10 min, nouvel essai 1 h, IMAP 5 min, backlinks dim. 02:00, perte de liens dim. 03:00, stats 23:59, séquences 10 min, crawl 02:00, hebdo dim. 20:00, diffusion 10 min, séquence diffusion 10 min, chauffe 00:05, santé presse :15, résumé presse 20:00, rapport diffusion 21:00) | BE `src/jobs/schedulers/cronScheduler.ts` | Planificateur | REPRIS pour les 11 liées à l'envoi (voir lignes ci-dessus) ; 5 ÉCARTÉES (backlinks, perte de liens, crawl, enrichissement SEO, score) | CHA-012, 018 ; CON-062 ; RES-041 |
| 143 | Interrupteurs par tâche automatique (10 workers activables un par un) | BE `automation/automationToggles.ts`, route `/settings/automation/workers` | Couper une automatisation | REPRIS (interrupteurs en Réglages, pause visible partout) | CON-009, CON-027 |
| 144 | 13 tâches cron de `/opt/mail-security/*.sh` sur le serveur SOS-Expat | SEP `docs/audits/AUDIT-EMAIL-INFRASTRUCTURE-COMPLET.md` l. 534-555 (GitHub public) | Inconnu en détail | **NON VÉRIFIÉ** : pas de copie locale ; probablement les scripts de SEP déjà listés (chauffe, rebonds, DMARC, listes noires) | voir ABSENT n° 6 |
| 145 | Journal d'audit, journal d'activité | CEE `app/services/audit.py` ; MC « Journal » | Traçabilité | REPRIS (`audit_logs` + journal des gestes de pilotage) | CON-032 ; P02 I7 |
| 146 | Journaux applicatifs | BE `utils/logger.ts` | Logs | REPRIS (sans adresse en clair) | G9 ; SEC-008 |

## 15. Rôles, accès, sécurité

| # | Élément ancien | Source | Ce que ça faisait | Verdict | Référence plan |
|---|---|---|---|---|---|
| 147 | Connexion, inscription, rôles `ops` / `admin` | BE `routes/auth.ts`, `middleware/auth.ts`, enum `UserRole` | Accès | REPRIS (4 rôles, 16 permissions, rôles fins V1, 2FA e-mail) | P02 I1-I8 ; P04 |
| 148 | JWT, multi-locataire | CEE `app/services/auth.py`, migrations 002-005 | Accès | REPRIS (Laravel, RLS prouvée) | P02 I5 ; G10 |
| 149 | Rôle « chercheur », équipe et objectifs | MC `Layout.tsx` l. 310-326 | Travail en équipe | PARTIEL (rôles prévus ; objectifs d'équipe non prévus, inutiles en solo) | P02 I8 |
| 150 | Secrets en clair dans les dépôts publics | CEE, SEP, MC, VS_CODE (audits A, C, F) | Fuite | ÉCARTÉ et corrigé (gardes CI G8, Gitleaks) ; jetons à révoquer côté SOS-Expat | G8 ; P02 I6 ; synthèse 00 |
| 151 | Analyse Bandit/Safety qui ne bloquait jamais | CEE `.github/workflows/ci.yml` | CI | REPRIS en mieux (Gitleaks + Semgrep exigés) | P02 I6 |

## 16. Intégrations et webhooks

| # | Élément ancien | Source | Ce que ça faisait | Verdict | Référence plan |
|---|---|---|---|---|---|
| 152 | PowerMTA (VMTA, débits par FAI, files, TLS, comptabilité) | CEE `powermta/`, TR `pmta/config` ; BE `smtpSender.ts` | Serveur d'envoi | ÉCARTÉ (décision de Will) ; toutes les fonctions ont un équivalent KumoMTA | P08 bloc A |
| 154 | Rotation des domaines d'envoi en sautant les malades | BE `outreach/domainRotator.ts` | Répartition | REPRIS (affectation pondérée et collante) | CHA-033 ; P08 C7 |
| 155 | MailWizz (campagnes, listes, quotas, base MySQL écrite en direct) | BE `outreach/mailwizzClient.ts`, `config/mailwizz.ts` ; CEE `mailwizz_db.py` | Orchestrateur | ÉCARTÉ (décision de Will) ; fonctions reprises par le CRM | P08 bloc B |
| 156 | Synchro Mission Control → Backlink Engine (webhook signé, rattrapage horaire `backlink:resync`) + écran de suivi | MC `BacklinkEngineWebhookService.php`, `ResyncBacklinkEngine.php` ; BE `webhooks.ts` `/mission-control/contact-created`, `MissionControlSync.tsx` | Synchro entre outils | REPRIS (synchro console ⇄ CRM, écran « Santé de la synchro ») | P02 K1-K4 ; P08 C11 |
| 157 | Webhook « utilisateur inscrit sur le site » | BE `webhooks.ts` `/sos-expat/user-registered` | Événement du site | REPRIS (outbox site → CRM, événements `form_submission`, `calendly_*`) | P02 E19 ; RET-029 |
| 158 | API d'ingestion de prospects | BE `routes/ingest.ts` | Entrée externe | PARTIEL (API publique par espace en V1) | P08 B15, F11 |
| 159 | Webhooks sortants signés vers un autre outil | CEE (vers « scraper-pro ») | Push d'événements | PARTIEL (V2) | P08 B16, F19 |
| 160 | Automatisations MailWizz du site (cycle de vie, Trustpilot) | SEP `sos/firebase/functions/src/emailMarketing/` | Messages déclenchés | PARTIEL (déclenchés par événement en V1, lettre en V1/V2) | P08 F10, M10 |
| 161 | Santé des API externes | MC `CheckApiHealthCommand.php` | Surveiller les services tiers | REPRIS (écran « Sources de mesure » : état et âge de chaque source ; crédits du vérificateur) | RES-067 ; VER-029 |

## 17. Hors sujet (prospection de liens SEO, contenu) : écarté exprès

| # | Élément ancien | Source | Verdict |
|---|---|---|---|
| 162 | Crawl de blogs, SerpAPI, concurrents, « write for us » | BE `services/crawling/*`, `routes/crawling.ts` | ÉCARTÉ (hors envoi) |
| 163 | Vérification de backlinks, perte de liens | BE `services/verification/*`, `routes/backlinks.ts`, `Backlinks.tsx` | ÉCARTÉ |
| 164 | Score SEO du prospect, enrichissement de page d'accueil, voisinage de liens | BE `services/enrichment/*` | ÉCARTÉ |
| 165 | Ressources, pages cibles, ancres, négociations, partenaires, conversions, tâches SEO | BE `routes/assets.ts`, `targetPages.ts`, modèles `Negotiation`, `Partner*`, `TaskAssignment` | ÉCARTÉ (les tâches CRM « Mes tâches » sont prévues à part, P02) |
| 166 | Détection de langue, pays, thématique, opportunité par IA | BE `llm/prompts/detectLanguage.ts`, `classifyThematic.ts`, `detectOpportunity.ts`, `enrichment/countryDetector.ts` | ÉCARTÉ (FR seul ; familles du CRM) |
| 167 | Moteur de contenu, scrapers d'annuaires, réseaux sociaux | MC `Services/Content/*`, `Scraping/*`, `Social/*` | ÉCARTÉ |
| 168 | Scripts d'essai manuels de bout en bout | BE `scripts/test-bounce-e2e.ts`, `test-smtp-e2e.ts`, `prod-readiness-audit.ts` | REPRIS en mieux (banc, kit de conformité, essai à blanc, P03 § 9) |

---

## 18. Ce qui est ABSENT ou mal placé : à ajouter au plan

| n° | Ajout | Vient de | Effort (j-agent) | Priorité | Où |
|---|---|---|---|---|---|
| 1 | Bouton « Envoyer un test à moi » par modèle et par campagne (message réel, en-têtes, signature DKIM visible), hors comptage de chauffe | BE `broadcast.ts` `/:id/test-send` | 0,5 | **V0** | lot E9 / E12 |
| 2 | Avis immédiat par e-mail et dans la console quand une réponse classée « intéressé » arrive (regroupé, sans donnée personnelle dans l'objet) ; aujourd'hui seule l'alerte « attend > 24 h » est prévue | BE `notifyProspectReplied`, SEP `forward-replies-telegram.py` | 0,5 | **V0** | lot E10 ; P02 F8 |
| 3 | Contrôle de dérive « configuration en base ↔ configuration chargée du serveur d'envoi », avec pause si écart : **remonter INF-040 de V2 en V1**, et en V0 comparer l'empreinte de configuration au test de fumée de 06:45 | CEE `validate-coherence.sh`, `check-sender-coherence.sh` | 1 | V0 (empreinte) / V1 (complet) | lots E3, E11 |
| 4 | Expiration des domaines et certificats (`go.`, `mta-sts.`) avec alerte 30 j avant : **remonter RES-024 de V2 en V1** (les 2 domaines achetés expirent dans un an) | absent chez SOS-Expat, mais trou réel | 0,5 | V1 | lot E4-V1 |
| 5 | « Contact par formulaire du site » comme étape manuelle de séquence (message préparé, lien vers le formulaire, contact noté à la main), **ou** décision explicite de l'écarter | BE `FormOutreach.tsx` | 1 | V1 (ou ÉCARTÉ par Will) | P02 E4 |
| 6 | Lire la section « 13 tâches cron » de l'audit SOS-Expat (dépôt GitHub public `sos-expat-project`, `docs/audits/AUDIT-EMAIL-INFRASTRUCTURE-COMPLET.md` l. 534-555) pour confirmer qu'aucune surveillance n'a été oubliée | SEP | 0,25 | V0 (lecture) | ce fichier |
| 7 | Trancher la contradiction sur les rapports DMARC : RES-017 est dans la liste V0 (P03 § 12) mais « ingestion DMARC » est rangée en V1 (P03 § 13) | SEP `dmarc-parser.py` | 0 (correction du plan) ; 2 j si V0 | V0 conseillé (p=none avec `rua` dès la création) | P03 § 12-13 |
| 8 | Battement externe « qui surveille le surveillant » (INF-049) : remonter de V2 en V1 | critique 06 n° 8 (SOS-Expat ne l'avait pas non plus) | 0,5 | V1 | lot E11-V1 |

**Total : environ 4,25 jours-agent** (V0 ≈ 2,25 j ; V1 ≈ 2 j), plus 2 j si l'ingestion DMARC passe en V0. Les relectures ajoutent environ 15 %.

Décisions de Will liées : Telegram reste-t-il éteint (oui selon le 24/10 ; P03 § 7.8) ; formulaire de contact (n° 5) repris ou écarté ; « engagement 5 % » redéfini en réponses humaines.

---

## 19. Verdict honnête

**Oui pour l'essentiel, non à 100 %.**

- **Tout ce qui surveillait vraiment l'envoi chez SOS-Expat est prévu**, souvent en mieux : chauffe (par IP, domaine et boîte, jours effectifs, recul automatique), alertes (console + e-mail, seuils durcis à 2 % / 0,1 %), surveillance DNS SPF/DKIM/DMARC/PTR/MX chaque jour, listes noires des IP (corrigées : résolveur local, SORBS retiré) et en plus des domaines, santé des serveurs (CPU, RAM, disque, services, files), boîtes (connexion, boîte pleine, score de préparation), rebonds, plaintes FBL, désinscription un clic, suppression, étiquettes, campagnes, presse, A/B, modèles, rapports, sauvegardes, interrupteurs. Sur 168 lignes : environ 123 REPRIS, 19 PARTIEL, 1 ABSENT, 24 ÉCARTÉ exprès (dont le volet SEO), 1 non vérifié.
- **Le plan ajoute ce que SOS-Expat n'avait pas** : sonde externe des ports et du relais (l'incident Spamhaus du 10/04 venait de là), homme mort, boîtes témoins, Postmaster, SNDS, santé des canaux de retour, âge des domaines, opposition par réponse STOP.
- **Ce qui manque** : un bouton d'envoi de test par campagne, un avis immédiat quand un prospect intéressé répond, le contrôle de dérive de configuration (prévu trop tard, V2), l'expiration des domaines (V2), le contact par formulaire (absent), et une contradiction sur DMARC. Environ 4 jours-agent.
- **Écartés exprès** : Telegram et toute notification au téléphone (décision du 24/10), pixel d'ouverture et clics, MailWizz, PowerMTA, rotation d'IP pour contourner, faux trafic Mailflow, traduction multilingue, tout le volet SEO/backlinks et contenu.
- **Réserves** : (1) beaucoup de surveillances arrivent en V1 et non en V0 (agent SSH, score 0-100, Postmaster, SNDS, écran Files d'attente) : au premier envoi, la surveillance V0 couvre listes noires, DNS, santé serveur, chauffe, rebonds, plaintes et alertes, ce qui égale déjà ce que SOS-Expat avait ; (2) l'ancien système n'a jamais été prouvé de bout en bout (aucun test, pont MailWizz-PowerMTA à 0 %) : « reprendre » veut dire reprendre des idées et des valeurs, pas un outil qui marchait ; (3) les 13 tâches cron du serveur SOS-Expat n'ont pas pu être lues en détail (pas de copie locale).
