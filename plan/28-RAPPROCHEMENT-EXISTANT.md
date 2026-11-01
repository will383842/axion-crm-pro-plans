# 28 : LOT V2 : rapprochement du plan avec l'existant du CRM (01/11/2026)

**But.** Ne **rien recréer** qui existe déjà dans le CRM Pro. Pour chaque lot du plan 20 et pour chaque page du plan 23, dire ce que le code fait déjà, avec le fichier et la ligne.

**Comment.** Lecture seule du dépôt `axion-crm-pro` (`main` à la fusion #387). Rien n'a été exécuté. Aucun serveur touché. Aucun secret, aucune adresse de serveur, aucune donnée de personne recopiés ici.

**Décision de Will (rappel).** On **garde le menu actuel** (Tableau de bord, À traiter, Ma base, Presse, Réseaux, Ciblage, Alimenter la base, Réglages, Technique). On ajoute **seulement deux entrées : Campagnes et Envois**.

**Verdicts.**
- **EXISTE** : à réutiliser tel quel.
- **PARTIEL** : la base existe, à étendre (on dit quoi).
- **ABSENT** : à créer.
- **CONFLIT** : même nom, autre sens (ou contraire à une décision de Will).

Chemins : `B/` = `backend/`, `F/` = `frontend/src/`. Les numéros de ligne sont ceux de `main` au 01/11.

---

## 0. En bref (12 lignes)

1. Le CRM a **déjà** beaucoup de briques que le plan 20 recompte : préparation des destinataires, éligibilité, opposition, suppressions, vérification des adresses, tâches, étapes, actions de masse, journal, rôles, sauvegarde chiffrée et exercice de restauration.
2. Il n'a **pas** de moteur d'envoi, pas de chauffe, pas de page publique de désinscription, pas de 2FA par e-mail, pas de « Tout arrêter ».
3. **4 conflits** à régler avant de coder : le mot « campagnes » (collectes), la **table `campaigns` d'ébauche** déjà créée, le **canal d'alerte Telegram** déjà codé, les **segments ouverts par défaut**.
4. Le relevé 21 se trompe ou se tait sur 12 points (§ 1.3) : il manque ≈ 25 tables d'ébauche, les segments sont **ouverts** (pas fermés), le décalage de 2 h est **déjà corrigé** dans le code, la vérification des listes noires est **une coquille vide**.
5. Les tâches existent déjà (table `activities`, type `task`) : **ne pas** créer `crm_tasks`.
6. Les étapes commerciales existent déjà (`nouveau → perdu`) : **étendre** la liste, ne pas créer un second champ.
7. La sauvegarde existe (copie chiffrée, copie hors site, vérification, exercice de restauration) : S9 devient surtout « alertes par e-mail ».
8. Le centre d'alertes a déjà sa table et sa cloche (`notifications`), mais **personne n'y écrit**.
9. Les maquettes (plan 23) utilisent un **autre menu** (Travailler, Prospecter, Envois, Mesurer) : il faut les **ranger dans le menu de Will** (§ 4).
10. Toutes les pages du plan 23 trouvent leur place dans le menu actuel + Campagnes + Envois.
11. Charge du plan 20 : **≈ 650 j → ≈ 589 j** (− 64 j économisés, + 3 j de rapprochement), détail au § 5.
12. 10 vérités à mesurer sur le serveur réel, sans rien écrire (§ 6).

---

## 1. Ce que le code a déjà : vérification du relevé 21

### 1.1 Les briques qui existent (carte rapide)

| Thème | Ce qui existe | Où (fichier:ligne) |
|---|---|---|
| Éligibilité « peut-on lui écrire ? » | une seule définition : opposition + suppression | `B/app/Support/EligibiliteCampagne.php:48`, `peutRecevoir` l. 150 |
| Motifs d'exclusion d'une adresse | non diffusible, fermée, entrepreneur individuel, site non vérifié, tiers mal informé, invalide, OSM, non vérifiée, personnelle (webmail), déjà informée, opposition | `B/app/Crm/Campagnes/EligibiliteAdresse.php:18-97`, `motif` l. 155 |
| Segments de campagne | organisateurs, fédérations, presse ; réglage `crm.segments_ouverts` | `B/app/Crm/Campagnes/Segments.php:53-66` ; `B/config/crm.php:507` |
| Gardes presse et console | la presse n'entre que par son segment ; un client de la console n'est jamais destinataire | `B/app/Crm/Campagnes/GardePresse.php:47`, `AdressePresseFiable.php:54`, `GardeConsoleClient.php:31` |
| Adresses partagées (cabinets) | exclues par paquet | `B/app/Crm/Doublons/AdressesPartagees.php` |
| Préparer la liste d'envoi | fichier des adresses autorisées, segment en liste fermée | `B/app/Console/Commands/CrmCampagneDestinataires.php:99` |
| Enregistrer les retours | envoyé (pose `first_info_at`), désinscription, plainte, rebond dur, rebond mou | `B/app/Console/Commands/CrmCampagneRetours.php:40`, `first_info_at` l. 216 |
| Liste de suppression | inscrire, rebond temporaire, raison la plus grave, téléphone sous toutes ses formes | `B/app/Support/ListeSuppression.php:14`, l. 63, 96, 157 |
| Opposition | table `opt_out` (e-mail, téléphone, source) | `B/database/migrations/2026_05_16_000005_create_referentials_geo_naf_schema.php:138` ; `B/database/migrations/2026_08_15_000004_email_suppressions.php` |
| Vérification des adresses | MX, A, MX nul, jetable, webmail marqué ; commande hebdo ; sondes SMTP ; Hunter ; score de confiance | `B/app/Crm/Emails/VerificationEmail.php:64` ; `B/app/Console/Commands/CrmEmailsVerifier.php:77` ; `B/app/Services/Smtp/RealSmtpProber.php:19` ; `B/app/Services/Email/HunterEmailVerifier.php:39` ; `EmailConfidenceService.php` |
| Résolveur DNS maison | requêtes DNS en UDP, garde anti-SSRF | `B/app/Crm/Emails/Dns/ResolveurDnsUdp.php:30` |
| Joignabilité | état « joignable » calculé par fiche et par personne | `B/app/Crm/Joignabilite/Joignabilite.php` ; commande `CrmJoignabiliteCalculer.php` |
| Audiences (listes dynamiques) | critères ET / OU / SAUF (`all`, `any`, `not`), aperçu, destinataires | `B/app/Services/Audiences/AudienceBuilderService.php:26`, l. 589, 820-836 ; `F/features/audiences/*` |
| Listes manuelles | créer, membres, retirer, restaurer, **import par rapprochement** | `B/app/Crm/Listes/ListesManuelles.php:53` ; `B/app/Crm/Listes/ImportListe.php` ; `B/routes/api.php:406-425` |
| Étiquettes | gestion, étiquettes de masse, étiquetage automatique | `B/routes/api.php:354-367` ; `B/app/Services/Tags/AutoTaggerService.php:45` |
| Doublons | détection, fusion à blanc, fusion, refus, écran | `B/app/Crm/Doublons/FusionFiches.php:86` ; `B/app/Services/Dedup/DeduplicationService.php:23` ; `F/features/doublons/DoublonsPage.tsx` |
| Tâches | tâches par entreprise et par personne (`activities`, type `task`, `due_at`, `done_at`), carte sur la fiche | `B/app/Http/Controllers/Api/CompanyTachesController.php:24` ; `B/app/Http/Controllers/Api/Crm/PersonnesController.php:254` ; `F/features/companies/components/TachesCrmCard.tsx:26` |
| Étapes commerciales | `nouveau, qualifie, opportunite, client, dormant, perdu` ; saisie à la main tracée | `B/app/Crm/Taxonomy.php:239` ; `B/app/Http/Controllers/Api/CompanyRelationController.php` |
| Activités et motifs d'échange | tables `crm_motifs` et activités (appel avec motif), extensibles sans code | `B/app/Crm/ActivitesEtMotifs.php:56, 99` ; `B/database/migrations/2026_08_19_000002_crm_activites_et_motifs.php:75` |
| Historique d'une personne | frise | `B/app/Http/Controllers/Api/Crm/PersonTimelineController.php` ; `F/features/crm-console/PersonTimelinePage.tsx` |
| Actions de masse | route `/crm/bulk`, « on ne recule jamais », refus listés | `B/app/Http/Controllers/Api/Crm/BulkController.php` ; `B/routes/api.php:582` |
| Vues sauvegardées | serveur prêt, **aucun écran** | `B/app/Http/Controllers/Api/SavedViewsController.php:41` ; `B/routes/api.php:373` |
| Modifier / retirer un contact | serveur prêt, **aucun écran** | `B/app/Http/Controllers/Api/ContactsController.php:167, 185` |
| Exports | entreprises, médias, journalistes, personnes (permission `data.export`, délai borné) | `B/routes/api.php:169, 264, 281, 548` |
| Journal d'audit | journal chaîné, vérification nocturne, partitions | `B/app/Support/AuditLogger.php:28` ; `B/app/Services/Audit/AuditHashChain.php` ; `F/features/rgpd/AuditLogsPage.tsx` |
| Rôles | `owner, admin, operator, viewer` (spatie) ; invitation par lien ; accès révoqué (`revoked_at`), compte en suppression douce | `B/app/Http/Controllers/Api/UsersController.php:79, 120, 406` ; `B/database/seeders/PermissionsAndRolesSeeder.php:47` |
| Espaces (multi-client) | `workspaces`, contexte d'espace, tâches de fond sous espace, RLS sur ≈ 29 tables, rôle applicatif (éteint) | `B/app/Support/WorkspaceContext.php:31` ; `B/app/Jobs/Concerns/RunsInWorkspace.php` ; `B/database/migrations/2026_05_16_000008_enable_rls_policies.php` ; `B/config/crm.php:36, 53` |
| Connexion | mot de passe (contrôle HIBP), **2FA par code TOTP** avec codes de secours hachés, lien magique 15 min à usage unique, mot de passe oublié | `B/app/Services/Auth/TwoFactorService.php:34` ; `B/app/Services/Auth/MagicLinkService.php:70` ; `F/features/auth/*` |
| Courrier d'authentification séparé | réglage `mail.auth_mailer` utilisé par lien magique, invitation, réinitialisation | `B/config/mail.php:26` |
| Limiteur de connexion | 5/min **par adresse IP** | `B/app/Providers/RouteServiceProvider.php:28` |
| Canaux signés | signature HMAC réutilisable, canal Partners (anti-rejeu, idempotence) | `B/app/Support/HmacSignature.php:34` ; `B/app/Http/Middleware/VerificateurCanalPartners.php` |
| Sauvegarde | copie quotidienne chiffrée, copie hors site, vérifications, exercice de restauration programmable, restauration | `infra/scripts/backup-postgres.sh`, `backup-b2.sh`, `verifier-sauvegarde-b2.sh`, `dr-drill.sh`, `run-dr-drill.sh`, `restore-postgres.sh` ; `.github/workflows/surveillance-sauvegarde.yml` |
| Surveillance | battement du planificateur, état des canaux, détection d'anomalies | `B/app/Support/BattementPlanificateur.php` ; `B/app/Console/Commands/CrmCanauxEtat.php:73` ; `AnomalyDetect.php` |
| Notifications dans l'écran | table `notifications`, lecture, « tout lu », cloche | `B/app/Http/Controllers/Api/NotificationsController.php:44` ; `F/components/layout/NotificationsBell.tsx` |
| Recherche globale Ctrl K | existe | `F/components/ui/GlobalSearch.tsx:36` |
| Garde Sirene | diffusion partielle (`P`) et refus (`N`), sonde quotidienne | `B/app/Crm/Insee/MiseAJourMensuelle.php:597-623` ; `B/app/Console/Commands/CrmSondeNonDiffusibles.php` |
| Base légale | mesure (compte, n'écrit rien) | `B/app/Crm/Ingest/MesureBaseLegale.php` |
| Données santé (base pharmacies) | import FINESS, téléphones, enrichissement, RPPS | `B/app/Crm/Pharmacies/*` ; `B/app/Console/Commands/CrmPharmaciesImportFiness.php` ; `ImportRpps.php` |
| Moteurs d'IA | routeur multi-fournisseurs | `B/app/Services/LLM/LLMRouterService.php:20` |
| Système de design | ≈ 30 composants (carte, tuile, pastille, onglets, fenêtre, état vide, erreur) | `F/components/ui/*` |
| Description de l'API | annotations OpenAPI (l5-swagger) sur les contrôleurs | `B/app/Http/Controllers/Api/ApiController.php` ; `B/config/l5-swagger.php` |

### 1.2 Ce qui n'existe pas du tout

Moteur d'envoi (KumoMTA ou autre), contrat « serveur d'envoi », registres domaines/IP/boîtes, configuration du serveur depuis la base, chauffe, disjoncteurs, « Tout arrêter », frein humain, page publique de désinscription et en-tête de désinscription en un clic, retours par webhook signé et relève IMAP, réponses (tri, file), boîtes témoins, test du matin, rapports DMARC, contrôleur de contenu, gabarits versionnés et séquences (il n'y a que des tables vides), 2FA par code e-mail, appareil de confiance, alertes par e-mail, écran de sauvegarde, « Mes tâches » (page globale), Kanban « Affaires », bloc d'information art. 14 par espace, arrêt d'envoi par client.

### 1.3 Corrections du relevé 21 (lu dans le code)

| # | Le relevé 21 dit | Le code dit | Où |
|---|---|---|---|
| 1 | « 10 tables d'ébauche » | **≈ 35 tables d'ébauche** dans la migration du socle de mai, dont **`campaigns`, `email_templates`, `email_sequences`, `email_sends`, `email_events`, `email_messages`, `pipeline_stages`, `deals`, `deal_history`, `crm_lost_reasons`**, `dnc_lists`, `dnc_entries`, `linkedin_*`, `analytics_*`. Aucune n'est lue par le code (seul un commentaire les cite). | `B/database/migrations/2026_05_16_000007_create_phase2_scaffold_schema.php:18-128` ; `B/app/Console/Commands/CrmDoublonsPersonnes.php:48` |
| 2 | `CRM_SEGMENTS_OUVERTS` « vide par défaut » = fermé | **Vide = les 3 segments OUVERTS** (organisateurs, fédérations, presse). Seul `aucun` ferme tout. | `B/app/Crm/Campagnes/Segments.php:66, 79-93` ; `B/config/crm.php:507` |
| 3 | Décalage de 2 h : « où naît-il ? » (§ 10.11) | **Cause trouvée et corrigée dans le code** : fuseau posé sur la connexion Postgres ; commande de reprise `horodatages:corriger` (UPDATE seuls, comptes vérifiés). Reste à savoir si elle a tourné. | `B/config/database.php:72-122` ; `B/app/Console/Commands/CorrigerHorodatages.php:61` |
| 4 | `blacklists:check` « vérifie les listes noires » (risque de doublon avec E8) | **Coquille vide** : en production, elle écrit seulement « implémentation prévue » et rend « succès », chaque heure. | `B/app/Console/Commands/BlacklistsCheck.php:16-24` ; `B/routes/console.php:102` |
| 5 | Le mot « campagnes » est à renommer | **Le menu dit déjà « Collectes »** ; restent la route `/campaigns`, l'API `/v1/campaigns`, la commande `campaigns:start-scheduled` et le dossier `features/campaigns`. | `F/components/layout/Sidebar.tsx:196` ; `F/app/routeTree.tsx:165-167` ; `B/routes/api.php` (groupe `/campaigns`) |
| 6 | (non cité) | **Un canal d'alerte Telegram est codé et branché** sur 3 commandes (anomalies, sondes). C'est contraire à la décision « alertes console + e-mail ». | `B/app/Services/Alertes/AlerteTelegram.php:52` ; `B/config/alertes.php:37` ; `AnomalyDetect.php:111`, `CrmSondePersonnes.php:104`, `CrmSondeNonDiffusibles.php:146` |
| 7 | Tables `crm_tasks`, `crm_notes` « candidates » pour Q1b et Q2 | Les tâches vivent **déjà** dans `activities` (type `task`) avec écran sur la fiche entreprise. `crm_tasks` serait un **second stockage**. | `B/app/Http/Controllers/Api/CompanyTachesController.php:12-24` |
| 8 | (non cité) | La table `notifications` et la cloche existent, mais **aucun code n'y écrit** : la cloche est toujours vide. | `B/app/Http/Controllers/Api/NotificationsController.php:23` (aucun `insert` ailleurs) |
| 9 | 44 tâches planifiées + battement | **47 lignes `Schedule::`** dans `routes/console.php` (à recompter avec `schedule:list`). | `B/routes/console.php` |
| 10 | 54 écrans | **53 `createRoute`** (dont la racine et la coquille, soit ≈ 51 écrans). | `F/app/routeTree.tsx` |
| 11 | 391 fichiers de tests | **382** fichiers `*Test.php` côté serveur **+ 124** côté écran (Vitest, Playwright). | `B/tests`, `frontend/` |
| 12 | « opposition par téléphone » à créer (Q3) | `opt_out.phone` existe, avec comparaison de toutes les formes françaises du numéro. | `B/app/Support/ListeSuppression.php:55-63` |

---

## 2. Lot par lot : verdicts (plan 20, § 3)

Colonne « j plan » = jours du plan 20. Colonne « j corrigé » = jours une fois l'existant réutilisé.

### 2.1 V0 : Sécurité et socle

| Lot | Verdict | Ce qui existe (où) | Ce qu'il reste à faire | j plan | j corrigé |
|---|---|---|---|---|---|
| S1 | PARTIEL | limiteur de connexion par IP (`RouteServiceProvider.php:28`), limiteur 2FA (`routes/api.php:75`) | ajouter le limiteur **par compte** et l'anti-rejeu | 1 | 0,5 |
| S2 | PARTIEL | courrier d'authentification séparé `mail.auth_mailer` (`config/mail.php:26`), déjà utilisé par 3 envois | refuser le démarrage s'il retombe sur le courrier par défaut ; ne jamais journaliser le contenu | 1,5 | 1 |
| S3 | PARTIEL / CONFLIT | 2FA **TOTP** + codes de secours hachés consommés (`TwoFactorService.php:34-125`), middleware `EnsureTwoFactorPassed`, page `/2fa`, lien magique 15 min | ajouter le **code par e-mail**, l'appareil de confiance, le code redemandé ; **garder** la table des codes de secours et le middleware. « 2FA » change de sens : TOTP aujourd'hui, e-mail demain (S12 retire le TOTP) | 6 | 5 |
| S4 | PARTIEL | pages connexion, 2FA, lien magique, mot de passe oublié (`F/features/auth/*`), changement de mot de passe (`F/features/settings/ChangerMotDePasse.tsx`) | les **reprendre** dans le nouveau style + écran « Sécurité du compte » | 3 | 2 |
| S5 | (retiré du dépôt public) | — | — | — | — |
| S6 | PARTIEL / CONFLIT | 4 rôles, permissions sur les routes (`permission:*`) ; segments réglables (`Segments.php`) | un admin **peut aujourd'hui nommer un owner** (`UsersController.php:334-380`, aucun refus) : à fermer ; segments **ouverts par défaut** : passer à « fermé par défaut, réglé par espace » ; vérifier la permission de `/crm/bulk` | 3 | 3 |
| S7 | PARTIEL | RLS sur ≈ 29 tables, `WorkspaceContext`, `RunsInWorkspace` pour les tâches de fond, rôle applicatif et mode strict **éteints** (`config/crm.php:36, 53`), script de droits `infra/scripts/droits-role-applicatif.sql` | armer, rejouer les tâches sous le rôle, RGPD **par espace** (l'effacement est aujourd'hui **tous espaces** : `GdprErasureService.php:327`), suite à deux clients | 14,5 | 12,5 |
| S8 | **EXISTE** | cause corrigée (`config/database.php:72-122`) + `horodatages:corriger` | **supprimer le lot** ; garder un test « heure de Paris » et vérifier sur le serveur que la reprise a tourné | 1 | 0,5 |
| S9 | PARTIEL / CONFLIT | sauvegarde chiffrée, copie hors site, vérifications, exercice de restauration, battement, état des canaux (§ 1.1) | **remplacer Telegram par l'e-mail** (même interface `envoyer(titre, corps)`), écrire dans `notifications` (centre d'alertes), bouton « alerte de test », battement **externe**, seconde adresse ; chronométrer `dr-drill.sh` | 9 | 5 |

### 2.2 V0 : Préparation multi-client

| Lot | Verdict | Ce qui existe | Ce qu'il reste | j plan | j corrigé |
|---|---|---|---|---|---|
| P1 | PARTIEL | drapeaux éteints par défaut (`config/crm.php`), `FeaturesController`, garde des données personnelles (`infra/scripts/garde-donnees-personnelles.sh`) | ADR ; **arbitrer une fois les ≈ 35 tables d'ébauche** (§ 3 des doublons) | 6 | 5,5 |
| P2 | PARTIEL | `opt_out` et `email_suppressions` avec `scope` (`business`/`vivier`), **sans** `workspace_id` | ajouter `workspace_id` ; identité légale et quotas par espace | 4 | 4 |
| P3 | PARTIEL | l'espace Axion est un `workspace` | retirer les valeurs en dur : espace par défaut `axion-ia` (`config/crm.php:159`), user-agents à l'adresse Axion (`CrmEntreprisesVerifierSites.php:79` et 3 autres) | 5 | 5 |
| P4 | **EXISTE** (patron) | `HmacSignature` (`Support/HmacSignature.php:34`), canal Partners signé v2 + anti-rejeu + idempotence (`VerificateurCanalPartners.php`) | brancher la console dessus ; **ne pas écrire un nouveau signataire** | 2 | 1 |
| P5 | ABSENT | — | arrêt d'envoi par client + arrêt général | 3 | 3 |

### 2.3 V0 : Envoi

| Lot | Verdict | Ce qui existe | Ce qu'il reste | j plan | j corrigé |
|---|---|---|---|---|---|
| E1 | PARTIEL | patron des simulateurs `MOCK_*` + refus en production (`config/crm.php:75-112`), `MockSmtpProber` | contrat « serveur d'envoi », simulateur, banc | 10,5 | 10,5 |
| E2 | ABSENT | — | KumoMTA complet | 20,5 | 20,5 |
| E3 | PARTIEL | résolveur DNS maison (`Crm/Emails/Dns/ResolveurDnsUdp.php:30`) pour le contrôle DNS ; table vide `email_inboxes` | registres domaines/IP/boîtes, PTR, contrôle DNS quotidien (sur le résolveur existant) | 5 | 4,5 |
| E3b | ABSENT | — | configuration tirée depuis la base | 10 | 10 |
| E4 | PARTIEL | `VerificationEmail` + `crm:emails:verifier` hebdo (éteint) + sondes SMTP + Hunter + score de confiance + tables `email_validations`, `email_verification_logs` | **étendre** : cascade de fournisseurs, pré-vol de 30 jours, coût affiché ; écrire aux **mêmes clés** (`VerificationEmail.php:1-40`) | 6 | 3,5 |
| E5 | PARTIEL | `ListeSuppression` (rebond dur, mou, plainte, raison la plus grave), `crm:campagne:retours`, webhook du courrier transactionnel (jeton) | webhook signé + anti-rejeu, VERP, relève IMAP, plaintes toutes sources ; `crm:campagne:retours` devient **une source d'import** ; compteur des rebonds mous en base (il est en cache) | 17 | 14 |
| E6 | PARTIEL | `opt_out` + `EligibiliteCampagne` | page publique, en-tête un clic (RFC 8058) | 6 | 5,5 |
| E7 | ABSENT | table vide `email_warmup_pools` | chauffe, disjoncteurs, frein, « Tout arrêter » | 15,5 | 15,5 |
| E8 | PARTIEL / CONFLIT | `blacklists:check` planifié chaque heure, **mais vide** | **remplacer le corps** de `blacklists:check` (même nom, même horaire), pas de seconde commande ; boîtes témoins, DMARC | 8,5 | 8 |

### 2.4 V0 : Campagnes, réponses, mesure

| Lot | Verdict | Ce qui existe | Ce qu'il reste | j plan | j corrigé |
|---|---|---|---|---|---|
| C1 | PARTIEL / CONFLIT | **ciblage ET/OU/SAUF** (audiences), listes, segments, `EligibiliteCampagne`, `EligibiliteAdresse`, `ResolveurDestinataires`, gardes presse/console/adresses partagées, liste figée sous forme de fichier ; tables vides `campaigns`, `email_templates`, `email_sequences`, `email_sends` | moteur, gabarits versionnés, séquences, validation, contrôleur de contenu. **Appeler** `ResolveurDestinataires` + `EligibiliteCampagne` (garde `AucunEnvoiSansEligibiliteTest`), ne pas les recopier. Conflit de nom : voir § 3, n° 1 et 2 | 25,5 | 21 |
| C2 | PARTIEL | « envoi fait à la main » = `crm:campagne:destinataires` + `crm:campagne:retours` | volume envoyable, lien de RDV, envoi unitaire, « m'envoyer un test » ; mettre un écran sur la chaîne manuelle existante | 7 | 6 |
| C3 | PARTIEL (gros) | non diffusible `P`/`N`, entreprise fermée, entrepreneur individuel, webmail refusé (motif `personnelle`), sonde quotidienne | ajouter : hors France refusé, questionnaire jamais automatique, aucun lien vers le site d'Axion, STOP élargi | 4,5 | 2 |
| C4 | ABSENT | — | textes | 3 | 3 |
| RP1 | PARTIEL | tables vides `email_threads`, `email_messages` ; **patron « à rattacher »** (`ArbitrageController` attach/dismiss, `ArbitragePage.tsx`) | tri, file ; réutiliser le patron d'arbitrage pour « réponses à rattacher » | 10 | 9 |
| RP2 | ABSENT | étape `opportunite` existe | RDV rattaché, arrêt de séquence | 3,5 | 3,5 |
| RP3 | ABSENT | statistiques du tableau de bord (`DashboardController`) | résultats par campagne | 8 | 8 |

### 2.5 V0 : Interface, CRM du quotidien, conformité, essai

| Lot | Verdict | Ce qui existe | Ce qu'il reste | j plan | j corrigé |
|---|---|---|---|---|---|
| U0 | PARTIEL | ≈ 30 composants (`F/components/ui`), annotations OpenAPI | adapter les composants au guide (U1bis) ; générer les types depuis l'OpenAPI existant | 5 | 4 |
| U1 | FAIT (maquettes) | plan 23, 45 pages | **ranger les maquettes dans le menu de Will** (§ 4) : + 1 j (compté au § 5) | 6 | 6 |
| U2-U9 | PARTIEL | Tableau de bord, Entreprises, Contacts, fiches, Réseaux, Listes, Audiences, Doublons, Presse, Carte de France | **reprendre** les écrans existants (nouveau style), créer seulement les écrans de campagne et d'envoi ; pas de nouvelle barre latérale | 22 | 19 |
| U10 | — | tests d'accessibilité déjà en CI (`a11y.yml`) | passe finale | 2 | 2 |
| U11 | PARTIEL | cloche + table `notifications` (centre d'alertes), `RgpdRequestsPage`, `ArbitragePage` (patron) | alertes, serveurs, IP, boîtes, prudence, configuration, identité, frein, page publique | 12 | 10 |
| U12 | PARTIEL | Journal (`AuditLogsPage`), Équipe (`UsersPage`), Étiquettes, réglages techniques (`ReglagesTechniques.tsx`), scripts de sauvegarde | écrans neufs : messages types, sauvegardes, DMARC, mise en route, listes noires, lien de RDV ; **reprendre** journal et équipe | 12 | 9 |
| Q1 | PARTIEL | `PUT`/`DELETE` contact (serveur), import **par rapprochement**, provenance (`ProvenanceTiers`, `OriginesDesChamps`), synchro sortante `crm:flush-outbound` (éteinte) | écrans modifier/retirer ; import **avec création** ; ajout rapide ; mode d'emploi | 10,5 | 7 |
| Q1b | PARTIEL / CONFLIT | tâches par fiche (`activities` type `task`), étapes `nouveau → perdu`, actions de masse, routeur d'IA | page « Mes tâches » + rappel du matin ; **renommer/étendre** les étapes vers celles de Will (§ 3, n° 5) ; aperçu et annulation des actions de masse | 10,5 | 7 |
| J1 | PARTIEL | `first_info_at` (date du premier message, art. 14), `contacts.legal_basis`, `MesureBaseLegale` | bloc art. 14 par espace, alerte J+21, refus J+30 | 6 | 5 |
| J2 | (retiré du dépôt public) | — | — | — | — |
| J3, D0 | ABSENT (textes) | — | — | 2 + 1 | 2 + 1 |
| T1 | ABSENT | 11 suites e2e en CI (`e2e.yml`) | scénarios d'envoi, feu vert | 6 | 6 |

### 2.6 V1 et V2

| Lot | Verdict | Ce qui existe | Ce qu'il reste | j plan | j corrigé |
|---|---|---|---|---|---|
| Q2 | PARTIEL | vues sauvegardées (serveur), exports, historique, activités avec contenu (notes), motifs d'appel ; tables vides `deals`, `pipeline_stages`, `deal_history` | écrans vues et notes ; Kanban « Affaires » sur l'étape existante | 27,5 | 22 |
| Q3 | PARTIEL | `opt_out.phone` + toutes les formes du numéro, motifs d'appel, liens `tel:` (`ContactsListPage.tsx`) | campagne multicanal, file d'appels, script | 9 | 7,5 |
| C5 | PARTIEL | segment presse + gardes + registre des envois presse (`PresseEnvoisController`, dans `activities`) | A/B, messages déclenchés, récurrentes, score anti-spam | 15 | 13,5 |
| C6 | PARTIEL | personnes de la lettre et abonnements (`Crm/Personnes/Abonnements.php`, `PersonnesPage.tsx`) | double inscription, envoi | 7 | 6,5 |
| RP4, E9, J4, K2, K6, K7, K11 | ABSENT | — | — | 15,5 + 16 + 15,5 + 7 + 6 + 2 + 3 | inchangé |
| K1 | PARTIEL | rôles par espace (`user_workspaces.role_slug`), invitation par lien, `revoked_at`, table `invitations` | accès support tracé, transfert | 9,5 | 6,5 |
| K3 | PARTIEL | `WorkspaceController` (lire, modifier) | création d'un client | 8 | 7,5 |
| K5 | PARTIEL | sauvegarde globale chiffrée | sauvegarde par client | 5 | 4,5 |
| K8 | PARTIEL | `ObservabilityController`, `crm:canaux:etat` | diagnostic par client | 6 | 5 |
| K9 | PARTIEL | jetons d'API (Sanctum, `personal_access_tokens`), exports, plafond d'export (`Support/PlafondExport.php`) | clés à portée limitée, champs personnalisés | 11 | 9,5 |
| K10 | PARTIEL | routeur d'IA | propriétaire de fiche, accroche figée | 9 | 8,5 |
| K12 | PARTIEL | données pharmacies (FINESS, RPPS, téléphones) | modèle « fiche de référence + surcouche » | 12 | 11 |
| S11 | PARTIEL | `security.yml` (secrets, ZAP), masquage (`MasquageCoordonnees`, `EmpreinteIp`) | en-têtes, déploiement sans clé SSH | 8,5 | 7,5 |
| U13 | PARTIEL | boutons d'export, observabilité | écrans V1 | 19,5 | 18 |
| X3 (V2) | PARTIEL | file sortante signée `crm_outbound_events` + `crm:flush-outbound` (patron) | webhooks par client | 3 | 2,5 |
| S12 (V2) | — | code TOTP à retirer | inchangé | 0,5 | 0,5 |

---

## 3. Doublons à éviter (réutiliser, renommer, étendre)

| # | Ce que le plan ou les maquettes recréent | Ce qui existe | Réutiliser | Renommer | Étendre |
|---|---|---|---|---|---|
| 1 | **Écran et API « Campagnes »** (C1, maquettes `campagnes.html`) | `/campaigns` = **collectes** (`routeTree.tsx:165-167`, `ScrapingCampaignsController`, table `scraping_campaigns`, `campaigns:start-scheduled`) | — | route `/campaigns` → **`/collectes`** (+ redirection et test de route) ; dossier `features/campaigns` → `features/collectes` ; garder la table `scraping_campaigns` | les campagnes d'e-mails prennent **`/campagnes`** (route et API en français), jamais `/campaigns` |
| 2 | **Table des campagnes d'e-mails** (C1) | table vide **`campaigns`** (canal `cold_email`, statuts `draft…archived`) + `email_templates`, `email_sequences`, `email_sends` | **réutiliser** `campaigns` si elle est vide en production (vérité n° 1) | modèle Eloquent `Campaign` (libre : le modèle des collectes s'appelle `ScrapingCampaign`) | migration réversible : versions de gabarit, étapes 1-4, liste figée. **Retirer** de `email_sends` les colonnes `opened_at`/`clicked_at` (règle « aucun pixel ») |
| 3 | **Service d'éligibilité** (C1, C3, E6) | `EligibiliteCampagne`, `EligibiliteAdresse`, `ResolveurDestinataires`, gardes | **appeler** ces classes, une seule porte | — | ajouter les motifs manquants (hors France, lien vers le site d'Axion) **dans** `EligibiliteAdresse::motif` |
| 4 | **Désinscription / opposition** (E6, maquette « Désinscriptions ») | `opt_out`, `email_suppressions`, `ListeSuppression`, `EligibiliteCampagne::peutRecevoir` | ces tables et classes | — | `workspace_id` (P2) ; page publique ; écran « Puis-je écrire à… ? » = `peutRecevoir` + `EligibiliteAdresse::motif` + joignabilité |
| 5 | Tables `unsubscribes`, `dnc_lists`, `dnc_entries` (ébauche) | doublons d'`opt_out` | **non** | — | les **retirer** (migration réversible) avec le test « l'export RGPD contient tout ce qu'il contenait » |
| 6 | **Vérification d'adresse** (E4) | `VerificationEmail`, `crm:emails:verifier`, sondes SMTP, Hunter, confiance | la commande et les **mêmes clés** de résultat | — | cascade, pré-vol, coût |
| 7 | **Import** (Q1, maquette « Importer ») | import **par rapprochement** dans une liste (`ImportListe`, `/listes-manuelles/{id}/import`), `ScrapingIngestFile` | le lecteur de fichier et le rapprochement | — | mode « créer les fiches inconnues », avec provenance |
| 8 | **Listes et listes dynamiques** (maquette `listes.html`) | `ListesManuelles` + audiences (ET/OU/SAUF) | tout | « Audiences » peut garder son nom (menu actuel) | rien côté serveur |
| 9 | **Étiquettes** | `TagsController`, étiquettes de masse, étiquetage automatique | tout | — | — |
| 10 | **Doublons** | détection, fusion à blanc, fusion, refus, écran | tout | — | rien (ne pas refaire `doublons.html` côté serveur) |
| 11 | **Tâches** (Q1b, maquette `taches.html`) | `activities` type `task` (entreprise et personne) | `activities` | — | page « Mes tâches » qui **lit** ces activités ; **ne pas** utiliser la table vide `crm_tasks` (à retirer) |
| 12 | **Notes** (Q2) | `activities.content` + frise | `activities` (type `note`) | — | **ne pas** utiliser `crm_notes` (à retirer) |
| 13 | **Étapes commerciales** (Q1b : à contacter, contacté, répondu, RDV, devis, gagné, perdu) | `lifecycle_stage` : nouveau, qualifie, opportunite, client, dormant, perdu (`Taxonomy.php:239`, contrainte SQL) | le champ et sa trace `stage_changed` | **libellés** à l'écran : nouveau → « À contacter », client → « Gagné » | ajouter `contacte`, `repondu`, `rdv`, `devis` dans `Taxonomy` + contrainte (migration réversible), garder « on ne recule jamais » pour les automatismes |
| 14 | **Affaires / Kanban** (Q2) | tables vides `deals`, `pipeline_stages`, `crm_pipelines`, `deal_history` ; étape de la fiche | d'abord **l'étape de la fiche** | — | une seule de ces tables, choisie dans l'ADR (P1) ; retirer les autres |
| 15 | **Journal** (U12, maquette `journal.html`) | `audit_logs` chaîné + `AuditLogsPage` | tout | — | export avec code e-mail |
| 16 | **Rôles et équipe** (K1, U12, maquette `equipe.html`) | 4 rôles, invitation, révocation, suppression douce, écran Utilisateurs | tout | garder le libellé **« Utilisateurs »** du menu | refuser qu'un admin nomme un owner (S6), transfert |
| 17 | **2FA** (S3) | TOTP + codes de secours + middleware + page `/2fa` | codes de secours, middleware, page | — | code par e-mail ; TOTP gardé jusqu'à S12 |
| 18 | **Sauvegarde** (S9, U12, maquette `sauvegardes.html`) | scripts de sauvegarde, copie hors site, vérification, exercice, restauration | tous les scripts | — | un écran qui **lit** leur résultat ; alerte par e-mail |
| 19 | **Alertes** (S9, U11, maquettes `alertes.html`, `reglages-alertes.html`) | `AlerteTelegram` (**contraire à la décision**), table `notifications`, cloche, `anomaly:detect`, `crm:canaux:etat` | la cloche et la table `notifications` ; l'interface `envoyer(titre, corps, contexte)` | `AlerteTelegram` → **`Alerte`** (canaux : console + e-mail) ; retirer `config/alertes.php` « telegram » | règles type × canal, alerte de test |
| 20 | **Listes noires** (E8) | `blacklists:check` (vide) | le nom et l'horaire | — | écrire le vrai contrôle dedans |
| 21 | **Signature console** (P4) | `HmacSignature`, canal Partners | tout | — | — |
| 22 | **Statistiques** (maquette `statistiques.html`, groupe « Mesurer ») | tableau de bord, Carte de France (`/coverage`), `DashboardController` | les deux écrans | — | résultats de campagne dans **Campagnes** |
| 23 | **Recherche Ctrl K, cloche** (en-tête des maquettes) | `GlobalSearch.tsx`, `NotificationsBell.tsx` | tout | — | ajouter le feu des envois et « Tout arrêter » |
| 24 | **Boîtes d'envoi** (E3) | table vide `email_inboxes`, `email_warmup_pools` | non (schéma trop pauvre) | — | nouveau registre dans E3 ; retirer les deux tables vides |

**Règle.** Toute table d'ébauche non reprise est **retirée** dans P1, par migration réversible, après la vérité n° 1 (aucune ligne en production).

---

## 4. Cartographie du menu (menu actuel de Will + Campagnes + Envois)

**Lecture.** « Entrée » = ligne du menu. Une page sans entrée s'ouvre par un bouton, une carte ou une fiche. Les seules **nouvelles sections** sont **Campagnes** et **Envois**. Dans les sections existantes, j'ajoute au plus **3 lignes** (signalées « nouvelle ligne ») : **à valider par Will**. Sinon, ces pages passent en cartes.

Ordre proposé : Tableau de bord, À traiter, Ma base, **Campagnes**, **Envois**, Presse, Réseaux, Ciblage, Alimenter la base, Réglages, Technique. (Campagnes et Envois se placent juste après Ma base, car c'est le travail du jour.)

| Section du menu | Entrées (route actuelle) | Pages du plan 23 qui s'y rangent | Ce qui change |
|---|---|---|---|
| **Tableau de bord** | Tableau de bord (`/`) | Aujourd'hui (`index.html`) ; **Mise en route** (bandeau sur le tableau de bord, pas une entrée) ; résumé « Statistiques » (carte) | le tableau de bord actuel (`DashboardPage.tsx`, `AFaire.tsx`) est **repris**, pas refait |
| **À traiter** (pastille 326) | Doublons à vérifier (`/doublons`), Personnes à rattacher (`/console/arbitrage`), Propositions à valider (`/console/propositions`) | Doublons ; À valider (venu du site) ; **Réponses** (nouvelle ligne) ; **Réponses à rattacher** (onglet de Réponses) ; **Mes tâches** (nouvelle ligne) | la pastille additionne aussi les réponses à traiter et les tâches en retard (`F/features/a-traiter/compteurs.ts`) |
| **Ma base** | Entreprises, Contacts, Newsletter et guide, Candidats | Entreprises, Fiche entreprise, Contacts, Fiche contact, À valider (partie « lettre et guide ») ; **Affaires** (V1, nouvelle ligne) | rien ne bouge |
| **Campagnes** (NOUVELLE) | Campagnes (`/campagnes`), Messages types (`/campagnes/messages`), Résultats (`/campagnes/resultats`) | Campagnes (liste) ; Création en 5 étapes (bouton « Nouvelle campagne ») ; Suivi (page d'une campagne) ; Messages types ; Éditeur de message (page d'un message) ; Statistiques (partie résultats) | nouvelle section ; le `data-tour="nav-campaigns"` reste sur **Collectes**, la nouvelle entrée prend `nav-campagnes` |
| **Envois** (NOUVELLE) | Santé des envois, Boîtes d'envoi, Domaines, Serveurs, Montée en douceur, Alertes, Ne plus écrire | Santé ; Boîtes ; Domaines ; Serveurs et test du matin ; Montée en douceur ; Alertes (centre) ; Désinscriptions (« Puis-je écrire à… ? ») | nouvelle section ; la cloche de l'en-tête mène à Envois › Alertes |
| **Presse** | Médias, Journalistes, Communiqués envoyés | Presse | rien ne bouge |
| **Réseaux** | Fédérations et ordres, Événements | Réseaux (fédérations, événements) | la maquette y met « International » : **non**, « Entreprises en Roumanie » reste dans Technique (comme aujourd'hui) |
| **Ciblage** | Audiences, Listes | Listes, listes dynamiques | la maquette y met les étiquettes : **non**, Étiquettes reste dans Réglages |
| **Alimenter la base** | Collectes (`/campaigns` → **`/collectes`**), Carte de France (`/coverage`) | Collectes de données ; Statistiques (partie carte) | **seul changement réel** : l'adresse `/campaigns` devient `/collectes` (le libellé est déjà « Collectes »). La maquette range Collectes dans Réglages : **non** |
| **Réglages** | Paramètres (`/settings`), Utilisateurs (`/users`), Étiquettes (`/tags`), Demandes RGPD (`/rgpd/requests`) | Réglages (accueil) ; Mon compte et sécurité ; Alertes et avis ; Règles de prudence, horaires, automatismes ; Identité de l'expéditeur ; Équipe et rôles (= Utilisateurs) ; Demandes RGPD | les pages neuves sont des **cartes** de Paramètres, pas des lignes du menu ; le libellé « Utilisateurs » reste |
| **Technique** (repliée) | Entreprises en Roumanie, Historique des collectes, Santé du système, Moteurs d'IA, Serveurs relais, Rotation des accès, Registre de l'IA, Journal des actions | Outils techniques ; Journal ; Registre de l'IA ; **Sauvegardes** (carte de Santé du système) ; **Configuration technique** (E3b, carte de Santé du système) | la maquette met Journal et Registre de l'IA dans Réglages : **non**, ils restent dans Technique |
| Hors menu | `/login`, `/2fa`, `/magic-link`, `/magic-link/verify`, `/password-reset`, page introuvable | Connexion et code ; Page introuvable ; **Page publique de désinscription** (servie sous le domaine d'envoi) | `/cold-email`, `/linkedin`, `/crm`, `/analytics`, `/pas-encore-livre` restent des redirections |

**Ce qui change pour les maquettes (plan 23).** Les groupes « Travailler », « Prospecter », « Mesurer » et la barre à 18 entrées sont **abandonnés**. Les 45 pages gardent leur contenu ; seule la barre latérale de `index.html` (et du socle `_fabrique`) est refaite avec le menu ci-dessus. Écarts assumés n° 1 et n° 5 du plan 23 : **annulés**.

**Ce qui change dans le code du CRM (plus tard, par le lot qui code).** `F/components/layout/Sidebar.tsx:166-224` : insérer deux sections après « Ma base » ; `F/app/routeTree.tsx:165-167` : renommer `/campaigns` en `/collectes` avec redirection ; mettre à jour la garde `tests/components/navigation-cible.test.tsx` et le fil d'Ariane (`AutoBreadcrumbs.tsx`).

---

## 5. Corrections à apporter au plan 20

### 5.1 Lots à supprimer
- **S8** : déjà corrigé dans le code. Remplacé par une vérification dans R0 (0,5 j gardé).

### 5.2 Lots à requalifier en « extension » (avec le fichier à étendre)
S1, S2, S3 (`TwoFactorService`), S9 (scripts `infra/scripts`, `AlerteTelegram` → `Alerte`), P4 (`HmacSignature`), E4 (`VerificationEmail`), E5 (`ListeSuppression`, `crm:campagne:retours`), E8 (`blacklists:check`), C1 (`ResolveurDestinataires`, table `campaigns`), C3 (`EligibiliteAdresse`), Q1 (`ContactsController`, `ImportListe`), Q1b (`activities`, `Taxonomy`), Q2 (`SavedViewsController`, `activities`), K1 (`UsersController`).

### 5.3 Lots à corriger (fait faux dans le plan)
- **S6** : écrire « segments **ouverts** par défaut aujourd'hui, à fermer » (et non « déjà fermés »). Ajouter « un admin peut nommer un owner : à fermer ».
- **S9** : ajouter « retirer le canal Telegram codé » (décision de Will).
- **C1** : ajouter « routes `/campagnes`, jamais `/campaigns` ; réutiliser ou retirer la table `campaigns` d'ébauche ».
- **P1** : la liste des tables d'ébauche à arbitrer passe de 10 à ≈ 35.
- **U1** : ajouter « maquettes rangées dans le menu de Will » (U1ter, 1 j).
- **§ 11.5 du plan 20** : « renommer les campagnes de collecte » : le libellé est **déjà fait** ; il reste la route et l'API.

### 5.4 Jours économisés

| Phase | Plan 20 | Économisé | Ajouté | Nouveau |
|---|---|---|---|---|
| V0 | 323 | − 44 (S1 0,5 ; S2 0,5 ; S3 1 ; S4 1 ; S7 2 ; S8 0,5 ; S9 4 ; P1 0,5 ; P4 1 ; E3 0,5 ; E4 2,5 ; E5 3 ; E6 0,5 ; E8 0,5 ; C1 4,5 ; C2 1 ; C3 2,5 ; RP1 1 ; U0 1 ; U2-U9 3 ; U11 2 ; U12 3 ; Q1 3,5 ; Q1b 3,5 ; J1 1) | + 3 (U1ter maquettes 1 ; renommage `/collectes` + redirection + tests 0,5 ; Telegram → e-mail 0,5 ; retrait des tables d'ébauche 1) | **≈ 282** |
| V1 | 212 | − 19,5 (Q2 5,5 ; Q3 1,5 ; C5 1,5 ; C6 0,5 ; K1 3 ; K3 0,5 ; K5 0,5 ; K8 1 ; K9 1,5 ; K10 0,5 ; K12 1 ; S11 1 ; U13 1,5) | 0 | **≈ 192,5** |
| V2 | 115 | − 0,5 (X3) | 0 | **≈ 114,5** |
| **Total** | **≈ 650** | **− 64** | **+ 3** | **≈ 589 j** |

Avec relectures (+ 15 %) : **≈ 677 j** (au lieu de 747). Fourchette ± 30 % : 412 à 766 j.

**Hors de ce total, comme dans le plan 20 :** les ≈ 15 à 20 j du § 11 (R0, ADR consoles, contrat d'API, filet de non-régression). Une partie est **déjà faite** (relevé 21, filet 22) ; le contrat d'API part des annotations OpenAPI existantes.

**Effet sur les dates.** − 41 j en V0 ≈ **− 1,5 semaine** de calendrier avec 6 routines. Mais le premier envoi reste tenu par les **délais incompressibles** (âge des domaines, port 25) : la date du premier envoi ne bouge presque pas ; la marge grandit.

---

## 6. Les 10 vérités à vérifier sur le serveur réel (lecture seule, sans rien écrire)

| # | Question | Comment la lire (sans écrire) | Pourquoi |
|---|---|---|---|
| 1 | Les tables d'ébauche `campaigns`, `email_templates`, `email_sequences`, `email_sends`, `crm_tasks`, `crm_notes`, `deals`, `unsubscribes`, `dnc_entries` sont-elles **vides** ? | `SELECT count(*)` sur chacune, en lecture | réutiliser ou retirer sans perte (§ 3, n° 2, 5, 11, 12, 14) |
| 2 | Quelle est la valeur réelle de `CRM_SEGMENTS_OUVERTS` ? | `php artisan tinker` en lecture : `config('crm.segments_ouverts')` | vide = 3 segments ouverts (S6) |
| 3 | Le canal Telegram est-il configuré et actif ? | présence (oui/non) des variables, sans afficher leur valeur ; journal `alerte` des 7 derniers jours | à retirer (décision de Will) ; savoir si quelqu'un le lit encore |
| 4 | La reprise `horodatages:corriger` a-t-elle tourné ? | journal d'audit ou de déploiement ; comparer un `created_at` récent à l'heure de Paris | supprimer S8 sans risque |
| 5 | Date de la **dernière copie** locale et hors site, et du **dernier exercice de restauration réussi** | sortie de `verifier-sauvegarde.sh`, `verifier-sauvegarde-b2.sh`, journal de `run-dr-drill.sh` | réduire S9 à l'alerte par e-mail |
| 6 | Le rôle applicatif et le mode strict sont-ils armés ? Combien de tables ont la RLS active ? | `config('crm.db_app_role')`, `config('crm.strict_workspace_scope')` ; `SELECT relname FROM pg_class WHERE relrowsecurity` | point de départ réel de S7 |
| 7 | La table `notifications` contient-elle des lignes ? | `SELECT count(*) FROM notifications` | confirmer que la cloche est vide (centre d'alertes) |
| 8 | Quelle part des adresses est vérifiée `valide`, et la vérification planifiée est-elle allumée ? | `config('crm.emails_verification.planifiee')` ; `crm:emails:verifier --dry-run` (n'écrit rien) | taille réelle du travail de E4 |
| 9 | Combien de comptes ont le TOTP actif, et `MAIL_MAILER_AUTH` est-il distinct du courrier par défaut ? | `SELECT count(*) FROM users WHERE totp_enabled_at IS NOT NULL` ; `config('mail.auth_mailer')` | test de connexion à garder vert jusqu'à S12 ; S2 |
| 10 | De quoi est fait le **326** d'« À traiter », et `CRM_CONSOLE_V2_ENABLED` est-il vrai ? | `GET /api/v1/crm/a-traiter/compteurs` (lecture) ; `config('crm.console_v2')` | la pastille recevra réponses et tâches ; le menu dépend de ce drapeau |

---

## Résumé (15 lignes)

1. Le CRM a déjà l'éligibilité, l'opposition, les suppressions, la vérification d'adresses, les audiences ET/OU/SAUF, les listes, les étiquettes, les doublons, les tâches, les étapes, le journal, les rôles, la sauvegarde.
2. Il n'a pas de moteur d'envoi, de chauffe, de désinscription publique, de 2FA par e-mail, de « Tout arrêter ».
3. Conflit 1 : `/campaigns` = collectes. Les campagnes d'e-mails prennent `/campagnes` ; `/campaigns` devient `/collectes`.
4. Conflit 2 : une table vide `campaigns` existe déjà : la réutiliser si elle est vide en production.
5. Conflit 3 : un canal d'alerte **Telegram** est codé : le remplacer par console + e-mail.
6. Conflit 4 : les segments sont **ouverts** par défaut (le relevé 21 disait fermés).
7. Le décalage de 2 h est déjà corrigé : lot S8 supprimé.
8. `blacklists:check` est vide : E8 remplit cette commande, n'en crée pas une autre.
9. Tâches et notes : dans `activities`, jamais dans `crm_tasks` ou `crm_notes`.
10. Étapes : étendre `lifecycle_stage` vers les étapes de Will, pas de second champ.
11. ≈ 35 tables d'ébauche à arbitrer une fois (P1), après comptage en production.
12. Menu : celui de Will + **Campagnes** + **Envois** ; aucune autre section ; les maquettes changent de barre latérale.
13. Seul vrai déplacement : l'adresse `/campaigns` → `/collectes` ; Journal, Roumanie, Étiquettes, Collectes restent où ils sont.
14. Charge : ≈ 650 j → **≈ 589 j** (− 64 j, + 3 j) ; avec relectures ≈ 677 j.
15. 10 vérités à mesurer en lecture seule sur le serveur avant de coder (§ 6).
