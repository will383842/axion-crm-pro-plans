# 17 : Plan d'exécution cloud, plan chiffré unique et calendrier (01/11/2026)

Responsable exécution, en lecture seule. RIEN N'EST CODÉ. Aucun e-mail, aucun serveur, aucun secret. Matière lue : `plan/00` à `plan/11` et `REPRENDRE.md` (dépôt `axion-crm-pro-plans`) ; `.github/workflows/` du dépôt `axion-crm-pro` au commit `ce80ca9` (#386). Les chiffres de charge viennent des fichiers 02, 03, 04, 05, 06, 07, 08 et 11. Ce sont des estimations d'agents, incertaines à ± 30 %. Ils sont ici recomptés une seule fois.

**Unité** : 1 jour-agent (j) = une journée de travail d'un agent d'exécution, tests compris. Les relectures et audits Opus ajoutent + 15 %. Le calendrier suppose des routines qui tournent 5 jours sur 7.

---

## 0. Pourquoi un nouveau total

| Total ancien | D'où il vient | Problème |
|---|---|---|
| 223,5 j | cahier, option accélérée D-86 | inclut l'outillage, pas le CRM ni les clients |
| 315 j / 338 j | synthèse et critique de l'audit | même périmètre, deux comptes |
| 323 à 363 j | 03 : V0 138 + V1 115-135 + V2 70-90 | envoi seulement |
| « 185 j » | 02, CRM hors envoi | **la somme de ses 5 lots fait 215 j** (22 + 38 + 50 + 45 + 60), pas 185 |
| — | 02 lots 3-4 contre 03 E9, E10, E12 | ≈ 46 j comptés deux fois |
| non chiffrés | 04 (7 PR), 05 (M0-M11), 07 (13 écrans), 08 F1-F21 (49 j), 11 (8 ajouts, 4,25 j), manques de 06 | absents des totaux |

**Méthode** : chaque fonction est rangée dans **un seul** lot. Quand deux fichiers décrivent la même chose, le lot garde le chiffre le plus détaillé (règles citées dans la colonne « Contenu »). Retirés : les 5 ajouts N1-N5 et la marque blanche (refus de Will du 30/10, fichier 09) ; l'écran « Réglages › Clients » ne garde que le nom et le logo du client. Les options F20 (relais tiers) et F21 (clics agrégés) restent hors total, en attente d'une décision de Will.

**Règles de non-double compte** :
- E6 (retours) contient la relève IMAP et le STOP : les lignes F1-F3 de 02 ne sont pas recomptées.
- E9 (campagnes) contient l'objet campagne, l'assistant, les gabarits, la validation et les séquences de 02 (E1-E3, E5-E11, C8, C9).
- Les écrans de l'envoi de 03 E12 (18 j) sont remplacés par le lot Interface (U).
- La RLS est comptée dans S7 seulement, pas dans E1 ni dans 05 M4.
- Le battement externe (06 C6 = 11 n° 8) est compté une fois, dans S9.
- Les champs personnalisés (02 A12 = 08 F7) et les campagnes déclenchées (02 E19 = 08 F10) sont comptés une fois chacun.

---

## 1. Le plan chiffré unique

### 1.A Hors code (Will) : horloges à lancer en premier (0 j-agent, mais elles fixent le calendrier)

| ID | Action | Délai incompressible | Bloque | Quand |
|---|---|---|---|---|
| H1 | Acheter 2 domaines d'envoi, DNS chez Cloudflare « envoi », DMARC `p=none` avec `rua` dès la création | **21 jours d'âge** avant P1 | premier envoi réel | **S1 (3 nov)** → prêts le 24 nov |
| H2 | Ouvrir le compte Hetzner « envoi » ET un VPS OVH en plan B (06 M3 : une IP Hetzner du projet a déjà été listée par Spamhaus) | **≈ 1 mois + première facture** avant la demande de port 25 ; réponse au cas par cas | serveur réel (E2 en production) | **S1** → demande vers le 4 déc → réponse vers le 11 déc |
| H3 | Hébergeur des boîtes de réponse (D-70) et **personnes titulaires** des boîtes (06 B3) | 2 boîtes pour P1, 4 en P3, 14-16 en P13 | montée au-delà de ≈ 600/j | S1 pour 2-4 boîtes ; S16 pour la suite |
| H4 | Vérificateur d'adresses : compte et DPA | 1 à 2 semaines | E4 | S1-S2 |
| H5 | Entité expéditrice (D-07) et textes art. 14 (D-26), rédigés par l'IA puis relus par Will | relecture de Will | T1 | S1 (décision), S7 (relecture) |
| H6 | Notification CNIL de la fuite du 19/08 et organisateurs en retard art. 14 (D-01) | **déjà en retard** | légal, indépendant du code | **S1** |
| H7 | Troisième domaine (2e cohorte, P11) | 21 jours d'âge | 1 000/j | au plus tard le 15 mars 2027 |

### 1.B Tableau par lot

Légende : **Par.** = parallélisable avec d'autres lots (Oui / Non / Découpable en N agents). **Modèle** : « S » = Sonnet exécute ; « O » = Opus conçoit, relit ou audite. Chaque lot fini passe la relecture Opus et la critique de complétude (§ 5).

#### Phase 1 : V0, premier envoi réel d'Axion (complet en fonctions, petit en volume)

| ID | Contenu (sources) | Dépend de | j | Par. | Modèle | Preuve de réussite |
|---|---|---|---|---|---|---|
| **S1** | Fermer C1 : 409 sur setup/confirm si 2FA active, routes retirées de la liste blanche, anti-rejeu TOTP (04 PR-0) | — | 1 | Oui | S + audit O | tests Pest rouges puis verts ; test de rejeu refusé |
| **S2** | Mailer `auth` isolé, `MAIL_AUTH_*`, test « aucun envoi commercial par Mail:: » (04 PR-C) | — | 1 | Oui | S | test de dérive vert ; ZeptoMail transactionnel inchangé |
| **S3** | 2FA par code e-mail : migration additive, service, contrôleur, limiteurs, secours `crm:2fa:reinitialiser`, 16 tests (04 PR-D, 02 I1) | S2 | 4 | Oui | S + audit O sécurité | 16 tests verts ; 10 min, 5 essais, verrou 1 h vérifiés aux bornes |
| **S4** | Écran 13 « Connexion et 2FA » : saisie, renvoi, codes de secours affichés une fois (04 PR-E, 07 § 3.13) | S3, U0 | 2 | Oui | S | e2e connexion complète ; 0 violation axe |
| **S5** | Contrôles exigés sur `main` : + Gitleaks + Semgrep (déjà lancés sur chaque PR, donc sans délai de plus), garde données perso, `maplibre-gl`, CSP (02 I6, 04) | — | 1 | Oui | S | protection de branche relue : 6 contrôles exigés |
| **S6** | Permissions : modification en masse, un admin ne nomme pas un owner, segments sensibles fermés par défaut (10 § 1) | — | 2 | Oui | S + audit O | tests d'autorisation (IDOR) verts |
| **S7** | RLS armée par défaut, rôle applicatif Postgres, suite de tests sous ce rôle, refus de démarrer sans RLS, IDOR en boîte noire (02 M1, I5 ; 05 M4 ; règle 7) | — | 6 | Découpable 2 | S + audit O sécurité | test « deux clients factices » vert sous le rôle de production ; démarrage refusé si `CRM_DB_APP_ROLE_ENABLED=false` en prod |
| **S8** | Corriger le décalage de 2 h des horodatages (02 L9) | — | 1 | Non (touche beaucoup de fichiers : PR seule, fusionnée en premier) | S | test d'horodatage heure de Paris ; aucune régression |
| **S9** | Exploitation P0 : copie hors site quotidienne et restauration mensuelle (L2), alertes e-mail et bouton « alerte de test » (L4), inventaire des drapeaux (L5), pare-feu et déploiement (L6), joignabilité planifiée (L8), workflows de purge éteints (J9), journalistes retirés du dépôt (J11), battement externe « qui surveille le surveillant » (06 C6, 11 n° 8) | — | 9 | Découpable 2 | S + relecture O | alerte de test reçue ; battement coupé → e-mail reçu ; restauration chronométrée |
| **P1** | ADR envoi agnostique, licences, dictionnaire, convention « tenant », arbitrage des tables échafaudées, drapeau du module (éteint), 8 permissions, gardes CI G1-G9 dont « jamais axion-ia.com », clés PEM et IP publiques (03 E0, 05 M0, règles 3 et 5) | — | 6 | Non (tête de chaîne) | **O conçoit**, S code les gardes | ADR fusionné ; chaque garde a un test qui échoue sur un faux secret, une fausse IP, `axion-ia.com` |
| **P2** | `workspace_id` sur `opt_out` et `email_suppressions` (en citant le choix `scope` de la migration `2026_08_14_000004`, 06 X10), identité légale et quotas par espace (03 E1, règle 2) | P1 | 4 | Non | S + audit O | test : l'opposition de A ne bloque pas B ; l'opposition d'Axion gagne partout dans l'espace Axion |
| **P3** | Édition « produit » : rien d'Axion en dur (espaces figés, gardes « Axion »), l'espace Axion traité comme un client parmi d'autres (05 M3, règles 1 et 8) | P1 | 5 | Oui | S + relecture O | recherche « axion » dans `app/` : seulement la configuration ; test d'un espace « Client factice » complet |
| **P4** | Contrat d'API signée CRM ↔ console (usage, quotas), signature et rejeu refusé (règle 4) | P1 | 2 | Oui | O conçoit, S code | test de signature et d'anti-rejeu |
| **P5** | Gardes d'envoi « par entité » et arrêt général Axion (05 M5, règle 6) | P2 | 3 | Oui | S | test : l'arrêt de A n'arrête pas B ; l'arrêt général arrête tout |
| **P6** | Jeu de test réutilisable « deux clients factices » (règle 7) | S7 | 1 | Oui | S | utilisé par S7, P2, P5, T1 |
| **E1** | Contrat `ServeurEnvoi`, simulateur et puits SMTP, kit de conformité, banc jetable, REQ-INF-006 réintégrée (03 E2, 06 C8) | P1 | 6,5 | Non (chaîne critique) | O conçoit le contrat, S code | kit vert sur le simulateur |
| **E2** | KumoMTA : config Lua, DKIM, anti-relais en 4 couches, WireGuard, plafond local, homme mort, sonde externe, version figée par SHA-256 et copie des binaires (05 M1), tenant imposé par SMTP AUTH (08 F1), shaping (F2), plafond par locataire (F5), empreinte de config au test de fumée (11 n° 3) (03 E3) | E1 ; port 25 pour la production seulement | 17 | Découpable 2 | S + audit O sécurité | kit de conformité vert sur KumoMTA au banc ; test de relais ouvert en boîte noire refusé ; `X-Tenant` falsifié ignoré |
| **E3** | Registres domaines, IP, boîtes, personnes titulaires, règle « boîtes par personne réelle » (06 B3), plan DNS généré, contrôle DNS quotidien, PTR (03 E4) | P2 | 8 | Oui | S | DNS du banc contrôlé ; `axion-ia.com` refusé |
| **E4** | Vérification des adresses : fournisseur, cascade, porte qualité, pré-vol de 30 jours (03 E5) | P2, H4 | 6 | Oui | S | test sur 100 adresses factices ; coût estimé affiché (information, sans blocage tant que Will n'a pas tranché Q9) |
| **E5** | Retours : webhook HMAC idempotent, table d'événements, `AppliquerRetour`, rebonds mous en base, VERP, ARF, IMAP, STOP, réconciliation nocturne, validateur du classifieur (08 F4) (03 E6) | E1, E3 | 15 | Découpable 2 (webhook / IMAP) | S + audit O | retours rejoués : doublons, désordre, retard de 72 h, webhook falsifié refusé |
| **E6** | Désinscription RFC 8058 sous `go.<domaine>`, POST en un clic, opposition par domaine, page encore servie après la fin d'un domaine ou d'un client (06 M1) (03 E7) | E5 | 5,5 | Oui | S | désinscription effective en moins d'une minute |
| **E7** | Chauffe et protections : courbe en jours effectifs, budget = min(IP, domaine, boîte), décision de 07:00, seuils, disjoncteurs, arrêt d'urgence, TSA (08 F3), frein « réponses en attente » et mode absence (06 C7) (03 E8) | E3, E5 | 15 | Découpable 2 | S + audit O | tests aux bornes (1,99 % / 2,01 %) ; « Tout arrêter » coupe l'injection |
| **E8** | Surveillance : listes noires (résolveur local ou DQS), boîtes témoins, test de fumée, santé, alertes console et e-mail, rapport du matin, ingestion DMARC (11 n° 7), relecture des 13 tâches cron de SOS-Expat (11 n° 6) (03 E11) | E2, E5 | 9 | Oui | S | témoin rouge simulé → alerte reçue |
| **C1** | Moteur de campagnes : `EnvoiAutorise`, ciblage ET/OU/SAUF et exclusions, liste figée, pression, gabarits versionnés, variables, contrôleur des interdits, séquences 1-4 étapes en jours ouvrés, vagues, validation par version, pause et arrêt, composition, injection, bloc art. 14 (03 E9 ∪ 02 E1-E3, E5-E11, C8, C9) | E4, E6, E7 | 22 | Découpable 3 (ciblage / gabarits et validation / séquences et injection) | S + relecture O | campagne de banc validée, figée, injectée ; personne en opposition jamais injectée |
| **C2** | Volume envoyable par segment (C10, H6), lien Calendly (E14), envoi unitaire (E16), étapes manuelles (E4), envois faits à la main (B6), bouton « m'envoyer un test » (11 n° 1), garde « aucun pixel » (E20) | C1 | 7 | Oui | S | chaque fonction a son test ; le test d'envoi ne compte pas dans la chauffe |
| **C3** | Gardes ajoutées : destinataire hors France refusé (06 C1), aucun lien vers `axion-ia.com` dans un message à froid (C2), questionnaire jamais envoyé automatiquement (M9) | C1 | 2 | Oui | S | 3 tests rouges puis verts |
| **C4** | Rédaction des 2 premières séquences (organisateurs, fédérations) et de la page « pourquoi ce message » (06 B4) | J2 | 2 | Oui | **O rédige**, Will valide | textes validés par Will et passés au contrôleur des interdits |
| **RP1** | Réponses : rattachement, tri par règles, file, fiche 360°, demande RGPD (F4), « écrivez plutôt à » (F5), arrêt de séquence (F9), avis immédiat « intéressé » (11 n° 2) (03 E10) | E5 | 10 | Oui | S | 7 réponses factices triées ; STOP → opposition |
| **RP2** | RDV : attribution à la campagne (G3), arrêt de séquence et étape « opportunité » (G4), relance si RDV non honoré (G5) | RP1 | 3,5 | Oui | S | RDV factice rattaché à sa campagne |
| **RP3** | Mesure V0 : suivi de campagne (E17), résultats par campagne, étape, segment, expéditeur, sans ouvertures (H4) | C1, RP1 | 8 | Oui | S | chiffres du banc égaux au journal |
| **U0** | Système de design 2027 : jetons, composants, lexique sans jargon, 4 états, gardes « un seul bouton plein » et vocabulaire (07 § 1, § 4) | — | 5 | Non (fichiers partagés de l'interface) | **O conçoit**, S code | gardes automatiques vertes |
| **U1** | Maquettes cliquables des 13 écrans, test de 45 min avec Will (7 tâches), corrections (07 § 6) | — | 4 | Oui | **O** | 7 tâches réussies dans la cible |
| **U2-U9** | Écrans 1 Aujourd'hui (2), 5 Assistant de campagne (4), 6 Éditeur avec aperçu (3), 7 Réponses (3), 8 Santé des envois et « Tout arrêter » (3), 9 Domaines et boîtes (3), 10 Ne plus écrire (2), 11 Statistiques (2) : un écran par PR | U0, U1, API du lot servi | 22 | Découpable (un écran = une PR, 2 développeurs au plus) | S + relecture O | e2e par écran ; 0 violation axe ; campagne en 5 min et 15 clics |
| **U10** | Passe finale : clavier seul, 360 px, Lighthouse, NVDA sur 2 parcours | U2-U9 | 2 | Non | **O** relit | 6.1 du fichier 07 tenu sur les écrans de la V0 |
| **Q1** | CRM P0 : modifier et retirer un contact (A3), ajout rapide (A4), provenance (J6), import de fichier par l'interface (B4), sens sortant de la synchro (K3, K6), mode d'emploi pour Will (L10, passé en P0 par 06) | S7 | 10,5 | Oui | S | `PUT`/`DELETE` ne répondent plus 501 ; import de 100 lignes factices |
| **J1** | Conformité codée : base légale par flux, bloc art. 14 par espace, registre art. 14 par adresse (03 E13, 02 J5) | P2 | 6 | Oui | S + relecture O juriste | premier message sans bloc art. 14 refusé |
| **J2** | Textes : art. 14, pied de message, page « prospection », AIPD v2, LIA, registre art. 30 (02 J7, J8) ; méthode de Will du 27/10 (rédigés par l'IA, relus avec lui à la fin) | H5 | 4 | Oui | **O** juriste | textes relus par Will |
| **J3** | Règles écrites : effacement art. 17 et « aucune suppression » (06 M2), tableau des tiers et de leurs replis (M4), repli hébergeur avec critère d'abandon (M3) | — | 2 | Oui | **O** | 3 fiches au registre des décisions |
| **T1** | Bout en bout : scénarios du banc, essai à blanc en production (zéro SMTP), recette, premier message à Will, feu vert de 31 cases, J1 = 20 organisateurs (03 E14) | tout ce qui précède | 6 | Non | S + audit O final | 31 cases vertes ; spf/dkim/dmarc=pass chez les 4 témoins |
| | **Total phase 1 (V0)** | | **≈ 246 j** | | | **≈ 283 j avec relectures** |

#### Phase 2 : V1, CRM complet au quotidien et version pour la console des automatisations

| ID | Contenu (sources) | Dépend de | j | Par. | Modèle | Preuve de réussite |
|---|---|---|---|---|---|---|
| **Q2** | Travail quotidien (lot 2 de 02 sans ce qui est déjà dans Q1) : notes et appels, fonctions des personnes, Kanban, opportunités au montant informatif, Mes tâches, récapitulatif du matin par e-mail, tâches automatiques, vues sauvegardées, actions de masse, export, santé de la synchro, historique ; écrans 2 à 4 (fiche, pipeline et tâches, listes) recalés sur U0 | Q1, U0 | 32,5 | Découpable 2 (coordination avec le chantier « fiche client ») | S + relecture O | Will travaille une journée entière dans le CRM, sans tableur |
| **Q3** | Campagne d'appels : file, script validé, issue d'appel, opposition par téléphone (06 C5, pharmacies) | Q2 | 3 | Oui | S | appel noté « STOP » → `opt_out` |
| **Q4** | Étapes commerciales réglables, jeu par défaut de Will avec « devis » (06 M7) | K2 | 1,5 | Oui | S | test d'un jeu d'étapes par client |
| **C5** | Campagnes V1 : A/B (E12), presse complète (E15), déclenchées par un événement (E19 = F10), récurrentes (E18), score anti-spam (F13), formulaire de contact en étape manuelle (11 n° 5, ou rejet par Will) | C1 | 15 | Oui | S | chaque fonction a son test au banc |
| **C6** | Lettre d'information (si Will la confie au CRM, Q11) : double inscription (F8), formulaires et pages à la marque du client (F9) | C1, décision | 7 | Oui | S | inscription confirmée ; journal de consentement |
| **RP4** | Réponses et mesure V1 : répondre depuis la console (F7), alerte après 24 h (F8), entonnoir (H3), activité (H5), rapport hebdomadaire (H7), coûts visibles (H8), export de rapport (F12), chronologie (A6), badges (A7) | RP3 | 14 | Oui | S | rapport hebdomadaire reçu |
| **E9** | Envoi V1 : écran « Files d'attente » (F6), rotation DKIM (F14), FBL (F15), expiration des domaines et certificats (11 n° 4), Postmaster et SNDS, Cloudflare par API, configuration depuis la base et contrôle de dérive complet, 13 portées de disjoncteurs, capacité et projection | V0 en production | 19 | Découpable 2 | S + audit O | alerte d'expiration 30 jours avant, testée |
| **E10** | Repli Postfix + rspamd passé au même kit de conformité (05 M2) | E1 | 10 | Oui | S | kit de conformité vert sur Postfix |
| **J4** | Écran Conformité (J12) ; CGV, CGU, politique d'usage, DPA, annexe sécurité, niveau de service (06 C9) ; contrôle d'entrée d'un client et de son fichier (M8) ; cadre « base sectorielle mise à disposition » si Will le confirme (B1) | J2 | 11 | Oui | **O** juriste, S code | textes relus ; client factice refusé sans SIREN |
| **K1** | Rôles par client et accès du support tracé (02 M2), rôles fins (I8), sessions (I9), lien magique atomique (I10), journal des lectures (I7) | S7 | 9 | Oui | S + audit O | IDOR entre clients refusé |
| **K2** | Configuration par client avec héritage plateforme → secteur → client et droits par option (02 M3, 06 M5) | P3 | 6 | Oui | O conçoit, S code | faux 2e secteur ajouté sans toucher au code |
| **K3** | Création de client (commande et écran 12 « Réglages › Clients », nom et logo seulement) et assistant de mise en route (02 M13) | K2, U0 | 8 | Oui | S | « Garage Durand » créé en 8 min au test |
| **K4** | Installation en une commande, mise à jour par tirage de l'image publique version par version, vagues, retour arrière (02 M8, M9 ; 05 M7) | P3, S9 | 9 | Oui | S + audit O | installation d'un client factice depuis zéro, puis mise à jour et retour arrière |
| **K5** | Sauvegarde et restauration par client ; RPO et RTO alignés sur la console, plan de reprise chronométré (02 M7, 06 C10) | K4 | 5 | Oui | S | restauration d'un seul client chronométrée |
| **K6** | Usage et quotas remontés à la console par API signée, remise à zéro à la date anniversaire ; un dépassement informe, ne bloque pas (02 M5, 05 M9) | P4 | 4 | Oui | S | compteur remis à zéro au test de date |
| **K7** | Facturation : acompte, frais de mise en place, options, impayés, TVA, Tiime, et où elle vit (Hub de la console ?) (06 B6) | K6, décision Q15 | 6 | Oui | O conçoit (relecture « argent »), S code | facture de test produite, impayé simulé suspend l'envoi sans perte de données |
| **K8** | Diagnostic par client (02 M10), supervision depuis la console (M11) | K4 | 6 | Oui | S | page de diagnostic d'un client factice |
| **K9** | API publique par espace (08 F11), champs personnalisés (A12 = F7), export complet et réversibilité (B7) | K1 | 10 | Oui | S + audit O | export complet relu ; clé d'API à portée limitée |
| **K10** | Propriétaire de fiche, recontact, assignation (A13, D8, D9), limites mémoire (L7), ménage (L11), variations de texte par IA validées (E13) | Q2 | 6,5 | Oui | S | tests unitaires |
| **K11** | Client pilote de bout en bout : deux clients factices puis le pilote (05 M11) | K1-K9 | 3 | Non | S + audit O final | pilote isolé, sauvegardé à part, mis à jour sans coupure |
| | **Total phase 2 (V1 + version console)** | | **≈ 186 j** | | | **≈ 213 j avec relectures** |

#### Phase 3 : V2 (jusqu'à 5 000 par jour, confort)

| ID | Contenu | j | Modèle |
|---|---|---|---|
| X1 | V2 de 03 : plusieurs serveurs, 5 000/j, micro-variations, attribution du chiffre d'affaires, connecteurs, exercices, tests de charge, suggestions de tri des réponses par IA (07 Q6) | 70-90 | S + O |
| X2 | Lettre : éditeur par blocs (F16), centre de préférences (F17), version web (F18) | 9 | S |
| X3 | Webhooks sortants signés (F19) | 3 | S |
| — | Options F20 et F21 si Will le décide | (5) | — |
| | **Total phase 3** | **≈ 82-102 j** (≈ 106 avec relectures) | |

#### Récapitulatif unique

| Phase | j-agent | avec relectures (+ 15 %) | Fourchette ± 30 % |
|---|---|---|---|
| Phase 1 : V0, premier envoi réel | 246 | **283** | 200 à 370 |
| Phase 2 : V1 et version console | 186 | **213** | 150 à 280 |
| **Jusqu'à la version console** | **432** | **496** | **350 à 645** |
| Phase 3 : V2 | 92 | 106 | 75 à 140 |
| **Tout** | **524** | **602** | |

Le total est plus élevé que les anciens chiffres (223 à 363 j) parce qu'ils ne comptaient que l'envoi. Ce compte ajoute le socle, l'interface, la conformité, les clients, 04, 05, 08, 11 et les manques de 06, et retire les doubles.

---

## 2. Chaîne critique et parallélisme

### 2.1 Pistes sans collision de fichiers (une routine par piste)

| Piste | Lots | Fichiers possédés (personne d'autre n'y écrit) |
|---|---|---|
| A Sécurité et connexion | S1-S4, S6, puis K1 | `backend/app/Http/Controllers/Auth*`, services 2FA, `frontend/src/**/auth*` |
| B Données et isolation | S7, P2, P3, P5, P6, puis K2 | **toutes les migrations qui modifient des tables existantes**, `app/Policies`, `config/database.php` |
| C Exploitation et CI | S5, S8, S9, gardes de P1, puis K4, K5 | `.github/workflows/**`, `infra/` hors envoi, scripts de sauvegarde |
| D Envoi, cœur | E1, E5 (partie webhook), E6, E7 | `backend/app/Emailing/{Contrat,Retours,Desinscription,Chauffe}/**` |
| E Serveur d'envoi | E2, E3, E8, puis E9, E10 | `infra/envoi/**`, `backend/app/Emailing/{Registres,Surveillance}/**` |
| F Campagnes | C1, C2, C3, puis C5, C6 | `backend/app/Emailing/Campagnes/**` |
| G Vérification et réponses | E4, E5 (partie IMAP), RP1-RP4 | `backend/app/Emailing/{Verification,Reponses,Stats}/**` |
| H Interface | U0-U10, S4 (écran), puis K3 (écran) | `frontend/src/ui/**` (U0 seulement), `frontend/src/features/emailing/**` |
| I CRM au quotidien | Q1-Q4 | `backend/app/Crm/**` et `frontend/src/features/crm/**`, **après accord du chantier « fiche client »** |
| J Conformité et textes | J1-J4, C4 | `spec/`, `docs/legal/`, `backend/app/Emailing/Conformite/**` |
| K Clients et console | K6-K11 | `backend/app/Clients/**` (nouveau) |

**Fichiers chauds** (routes, `AppServiceProvider`, routeur et menu du front, seeder des permissions, `.env.example`) : P1 crée une fois `routes/emailing.php`, `EmailingServiceProvider`, `config/emailing.php` et un seeder de permissions du module. Ensuite, chaque piste n'écrit que dans ses fichiers. Le menu et le routeur du front ne sont touchés que par la piste H.

**Combien en parallèle** : **5 pistes Sonnet en même temps + 1 routine Opus**, soit 6 routines, sous le plafond de 6 à 8 partagé avec d'autres chantiers. Si le plafond descend à 4, la V0 glisse d'environ 5 semaines.

### 2.2 Chaîne critique de la V0

P1 (6) → P2 (4) → E1 (6,5) → E5 en 2 agents (8) → E7 en 2 agents (8) → C1 en 3 agents (10) → intégration des écrans 5 et 8 (4) → T1 (6).
**= 52,5 j-agent en série**, environ 60 avec les relectures, plus environ 4 jours d'attente de fusion, **soit environ 64 jours ouvrés, ou 13 semaines** à partir du 2 novembre. C'est cohérent avec le débit : 283 j répartis sur 5 pistes, environ 57 jours ouvrés.

Ce qui raccourcit la chaîne : les tests de T1 écrits dès la semaine 4 ; les écrans codés en parallèle sur des réponses d'API figées par contrat ; E3 et E4 faits en parallèle de E1.

### 2.3 Délais hors code à lancer en semaine 1

Domaines (21 j), Hetzner et OVH (≈ 1 mois + facture avant le port 25), boîtes, vérificateur, entité et textes, CNIL. **Aucun ne doit se trouver sur la chaîne critique** : lancés le 3 novembre, ils sont tous prêts avant la mi-décembre. La chauffe (6 à 9 semaines) ne commence qu'au premier envoi réel. C'est elle qui fixe la date des 2 000 par jour.

---

## 3. Exécution dans le cloud

### 3.1 Routines (une par sujet)

| Routine | Modèle | Rythme | Rôle |
|---|---|---|---|
| `crm-piste-<X>` (5 actives au plus) | **Sonnet** | 2 passages par jour ouvré | prend le prochain lot non bloqué de sa piste, l'exécute, pousse, ouvre la PR |
| `crm-controle` | **Opus** | 2 passages par jour (13:00 et 18:00) | relit les PR « prêtes » (revue de code, sécurité), critique de complétude en fin de lot, met à jour l'avancement, le REPRENDRE et la liste du train de fusion |
| Conception ponctuelle | **Opus** | à la demande | ADR (P1), maquettes (U0-U1), textes (J2, C4, J4), facturation (K7) |

Jamais Haiku. Routines **sans connecteurs**, avec seulement les deux dépôts. **Les consignes de chaque routine sont stockées dans le dépôt** (`chantier/routines/<piste>.md` de `axion-crm-pro-plans`). Si Will change de compte Claude, il recrée les routines en 5 minutes à partir de ces fichiers : rien ne vit dans la mémoire d'un compte ou d'un PC.

**Gabarit de consigne d'une piste** (à reprendre tel quel) :
1. Lire `chantier/REPRENDRE-CHANTIER.md`, `chantier/pistes/<X>.md` et `chantier/PROPRIETE-FICHIERS.md`.
2. Prendre le premier lot de la piste dont les dépendances sont fusionnées. Sinon, écrire « bloqué par … » et s'arrêter.
3. Créer la branche `p<X>/<lot>-<sujet>` depuis `origin/main`. Écrire les tests d'abord.
4. Faire un commit et un push toutes les 30 à 60 minutes, après `gitleaks protect --staged`. Sur un dépôt public, **pousser une branche, c'est publier**.
5. Ne lancer que les tests ciblés dans la session. Quand ils sont verts, ouvrir **une** PR, titrée `[<lot>] …`.
6. Mettre à jour `chantier/pistes/<X>.md`. Ne jamais fusionner. Ne jamais toucher un fichier possédé par une autre piste. Aucun secret, aucun serveur, aucun e-mail réel.

### 3.2 Ce qui se fait en local (PC de Will)

Lecture et édition seulement : relire un texte, corriger une ligne dans l'éditeur web de GitHub ou dans VS Code, puis pousser aussitôt. Aucun Docker, aucune suite de tests, aucun clone lourd (mémoire du PC). Rien n'est gardé en local.

### 3.3 Pousser par lots sans faire la queue

- **Pousser une branche ne déclenche aucune CI** : `ci.yml` ne part que sur une PR, et `security.yml`, `e2e.yml` et `a11y.yml` seulement sur une PR ou sur `main`. Les routines poussent donc en continu sans coût, et le travail est sur GitHub en cas de changement de compte.
- **Une PR par lot**, ouverte seulement quand le lot est prêt. La CI tourne une fois, avec la relance si un correctif est poussé (`cancel-in-progress` déjà actif sur les PR).
- **Branches courtes** : 3 jours au plus, environ 400 lignes hors tests. Un gros lot est découpé en sous-lots, chacun avec sa PR. Pas de PR empilées.
- **Train de fusion quotidien à 18:00** (heure de Paris) : `crm-controle` liste les PR vertes et relues. Will les fusionne d'un coup, ou délègue s'il le décide (décision W8). Les déploiements sur `main` ont `cancel-in-progress: false` avec un groupe de concurrence : GitHub garde au plus 1 déploiement en cours et 1 en attente. Un train de 6 fusions donne donc **2 déploiements au plus**, pas 6.
- **Un seul déploiement d'activation** : tout le module d'envoi reste derrière son drapeau éteint (P1). Les déploiements du train sont donc sans effet visible. Le module est allumé une seule fois, en S13 (essai à blanc puis premier envoi), par un déploiement groupé validé par Will.

### 3.4 CI : ce qui tourne, ce qui ne doit pas tourner

Constat (lecture des workflows) : une PR lance environ **14 tâches**. `ci.yml` en a 7 (config-prod, caddyfile, scripts, données personnelles, backend, frontend, workers), `security.yml` 4 (gitleaks, semgrep, composer-audit, pnpm-audit), `e2e.yml` 1 et `a11y.yml` 2. Chaque fusion sur `main` relance security, e2e, a11y et **deux** déploiements (staging et direct-ssh), qui rappellent chacun `ci.yml`. Une vingtaine de workflows de données planifiés (pharmacies, prospection, surveillance) partagent la même réserve de 20 tâches simultanées du compte gratuit. C'est la cause de la file de 30 à 80 minutes.

PR « économie de CI » (piste C, semaine 1, sans rien payer) :
1. Tâche « changements » en tête de `ci.yml` : une PR qui ne touche que le front saute le backend ; une PR de documentation saute tout. Les tâches sautées **répondent « réussi »**, pour que les contrôles exigés ne restent pas en attente.
2. `e2e.yml` et Lighthouse : seulement sur les PR marquées `ci:complet`, sur le train et chaque nuit sur `main`. axe reste sur toutes les PR.
3. Sur `main` après fusion : Gitleaks seulement. Semgrep, les audits, e2e et a11y passent la nuit (ils viennent de tourner sur la PR).
4. Workflows de données planifiés entre 00:00 et 06:00 UTC, en accord avec les chantiers pharmacies et prospection.
5. Contrôles exigés sur `main` : les 4 actuels, plus Gitleaks et Semgrep (S5). Ils tournent déjà sur chaque PR : les exiger n'ajoute aucune minute.
6. Pour `infra/envoi/**` seulement : validation de la config Lua de KumoMTA, vérification de l'empreinte SHA-256, kit de conformité joué contre le simulateur (sans réseau).

**Ne tourne jamais en CI** : envoi SMTP réel, port 25, DNS réel, connexion à un serveur, secret de production, base de production, Trivy et ZAP sur une PR (déjà exclus), tests de charge, workflows de données en journée, coureurs payants ou « larger runners ».

**Garde-fous sans frein** : Gitleaks local avant chaque commit (installé par le hook de démarrage de session) ; tests ciblés dans la session ; suite complète une fois par PR ; relecture Opus asynchrone. La relecture ne bloque que la fusion, jamais le travail de la piste suivante.

### 3.5 Coordination avec les autres sessions

`chantier/PROPRIETE-FICHIERS.md` contient une ligne par réservation (piste, fichiers, jusqu'à quand). Les autres chantiers du même dépôt (« fiche client » vague 2, synchro console, pharmacies FINESS) y sont inscrits avant le lancement. Une routine vérifie ce fichier avant de toucher un fichier. Si un fichier est réservé par un autre chantier, elle écrit « bloqué » et passe au lot suivant. Les migrations sont additives seulement. Seule la piste B modifie les tables existantes.

---

## 4. Calendrier semaine par semaine (S1 = semaine du 2 novembre 2026)

| Sem. | Dates | Pistes actives | Contenu | Jalon |
|---|---|---|---|---|
| S1 | 2-6 nov | A, B, C + O (P1, U1, J2) | S1, S2, S8, S5 et PR « économie de CI », S7 démarre, ADR | **Will : feu vert + décisions W1 ; achats H1-H4 ; CNIL H6** |
| S2 | 9-13 nov | A, B, C, D + O | S3, S7, S9, P2, E1 démarre, maquettes | ADR fusionné |
| S3 | 16-20 nov | A, B, C, D, E + O | S4, S6, P3, E1, E3, U0 | **Will : test des maquettes, 45 min** |
| S4 | 23-27 nov | B, D, E, G, H | P4-P6, E5, E2 (banc), E4, U0, écran 1 | domaines âgés de 21 jours (24 nov) |
| S5 | 30 nov-4 déc | D, E, F, G, H | E5, E2, C1 démarre, Q1 par la piste B libérée, écrans 9 et 10 | **Will : demande de port 25 (Hetzner et OVH)** |
| S6 | 7-11 déc | D, E, F, G, H | E6, E7, E8, C1, RP1, écran 5 | **BANC OK** : kit de conformité vert sur simulateur et KumoMTA, retours rejoués, désinscription en moins d'1 min |
| S7 | 14-18 déc | D, E, F, G, H | E7, E8, C1, RP1-RP2, écrans 6 et 7 | **Will : relire art. 14 et séquences (1 h)** |
| S8-S9 | 21 déc-1er janv | F, H, I (réduit) | lots sans décision de Will ; pas de train les jours fériés | semaines creuses (prévues) |
| S10 | 4-8 janv | D, E, F, G, H, J | fin de E7, C1, C2, C3, RP3, écrans 8 et 11, J1, J3 ; serveur réel si port 25 obtenu | port 25 obtenu (sinon plan B, § 6) |
| S11 | 11-15 janv | F, G, H, J, D→T1 | fin C2-C3, RP3, intégration, U10 | |
| S12 | 18-22 janv | T1, H + pistes V1 | scénarios complets sur le banc ; préproduction | **Will : second passage du test, 15 min** |
| S13 | 25-29 janv | T1 | déploiement d'activation groupé, essai à blanc en production (zéro SMTP), puis message à Will et à 4 témoins | **PREMIER ENVOI INTERNE (≈ 27 janv)** |
| S14 | 1-5 fév | T1 + V1 | feu vert de 31 cases, P1 = 20 organisateurs | **PREMIER ENVOI RÉEL LIMITÉ (≈ 2-3 fév 2027)** |
| S15-S21 | 8 fév-26 mars | 5 pistes V1 | Q2, C5, RP4, E9, K1-K6 ; montée P1 → P7 | **≈ 22 mars : 250/j (fin de la V0)** |
| S22-S23 | 29 mars-9 avril | V1 | K7-K11, J4, fin de V1 ; 500/j vers le 30 mars | client pilote sur le banc |
| S24 | 12-16 avril | V1 | client pilote installé, isolé, sauvegardé | **VERSION CONSOLE (≈ 15 avril 2027)** |
| S25-S27 | 19 avril-7 mai | V2 commence | 1 000/j vers le 13 avril (3e domaine acheté avant le 15 mars) ; **2 000/j vers le 4 mai** si 2e IP et 14-16 boîtes tenues | **MONTÉE DE VOLUME : 2 000/j** |
| S28-S32 | mai-juin | V2 | chauffe du client pilote (6-9 semaines) | client pilote à volume réel ≈ juin 2027 |

Montée : jours effectifs = jours d'envoi réels. Toute pause recule la date d'autant. Sans personnes titulaires des boîtes (06 B3), la courbe plafonne vers 600 par jour à partir de début avril.

### 4.1 Moments où Will doit agir ou valider (liste courte)

| # | Quand | Quoi | Temps |
|---|---|---|---|
| W1 | **S1** | Feu vert et décisions bloquantes : premier client et mutualisé (06 Q1-Q3), personnes des boîtes (Q4), 2FA 12 h ou 30 j (Q6), alertes (Q7), budget qui bloque ou informe (Q9), France seulement (Q10), entité D-07, hébergeur D-03, licence du code | 1 h |
| W2 | **S1** | Achats et comptes H1-H4 ; CNIL et art. 14 en retard (H6) ; rotation des clés | 2 h |
| W3 | S3 | Test des maquettes (45 min) | 45 min |
| W4 | S5 | Demande de port 25, chez les deux hébergeurs | 20 min |
| W5 | S7 | Relire les textes art. 14 et les 2 séquences | 1 h |
| W6 | S12 | Second passage du test en préproduction | 15 min |
| W7 | S13-S14 | Valider le premier message reçu, cocher le feu vert, autoriser le déploiement d'activation | 30 min |
| W8 | Chaque jour ouvré | Train de fusion de 18:00, sauf s'il le délègue (décision à prendre en S1) ; décisions inscrites au registre | 10 min |
| W9 | Dès S14 | Réponses et RDV (20 à 60 par jour à 2 000 envois ; le frein de E7 protège ses absences) | 30-60 min/j |
| W10 | S21-S24 | Client pilote, contrats (J4), facturation (K7) | 2 h |

---

## 5. Gouvernance

### 5.1 Point d'avancement (fichier `chantier/AVANCEMENT.md`, mis à jour par `crm-controle` chaque soir)

Un lot compte comme fait **seulement** quand il est fusionné et que sa preuve de réussite est verte. % = j-agent des lots faits / j-agent de la phase.

| Phase | Lots | j-agent | Faits | En cours | % |
|---|---|---|---|---|---|
| 0 Hors code (H1-H7) | 7 | — | 0 | 0 | 0 % |
| 1 V0 | 39 | 246 | 0 | 0 | 0 % |
| 2 V1 et console | 20 | 186 | 0 | 0 | 0 % |
| 3 V2 | 3 | 92 | 0 | 0 | 0 % |
| **Global** | **62** | **524** | **0** | **0** | **0 %** (plan : 100 % de 00 à 11 et 17 ; 12 à 16 non écrits) |

Plus une ligne par piste : lot en cours, PR, bloquant, prochain lot.

### 5.2 Fichier REPRENDRE du chantier (`chantier/REPRENDRE-CHANTIER.md`)

Le bloc du haut fait **40 lignes au plus**, toujours dans cet ordre : objectif (2 lignes), état global en %, jalon suivant et date, lots en cours par piste (une ligne chacun), PR dans le train du jour, bloquants, décisions attendues de Will, routines actives et leur fichier de consigne, règles de fer (lien), date de mise à jour. Sous le bloc : l'historique, qui n'est jamais relu en entier. Il est mis à jour par `crm-controle` à chaque passage et par chaque session qui reprend le chantier.

### 5.3 Registre des décisions (`chantier/DECISIONS.md`)

Une ligne par décision : `D-EXE-nn | date | question | choix de Will | qui l'a posée | lots touchés`. Une question tranchée ne se repose jamais. Les décisions déjà prises (24, 26, 27 et 30/10) sont recopiées telles quelles en tête : 24 mois puis clic, aucun dépôt privé, systeme.io rejeté, conservation des fiches de prospection sans débat. Aucun prix, aucun nom de client, aucun extrait juridique (dépôt public).

### 5.4 Critique de complétude à chaque fin de lot

`crm-controle` (Opus) se pose 6 questions :
1. La preuve de réussite est-elle verte, vue dans la CI ?
2. Les REQ du lot sont-elles toutes couvertes ?
3. Une garde de doctrine manque-t-elle ?
4. Un fichier a-t-il été touché hors de la propriété de la piste ?
5. Une donnée personnelle ou un secret est-il apparu ?
6. Qu'ajoute ce lot au plan (nouveau lot, nouvelle décision) ?

La réponse tient en 10 lignes dans `chantier/pistes/<X>.md`. Toute trouvaille devient un lot ou une décision, jamais une note perdue. En fin de phase, une critique de niveau 2 (comme le fichier 06) relit l'ensemble.

---

## 6. Risques d'exécution et parades

| # | Risque | Gravité | Parade |
|---|---|---|---|
| R1 | Secret ou donnée personnelle poussé sur le dépôt public (une branche poussée est déjà publique) | Critique | Gitleaks local avant le commit, Gitleaks exigé sur la PR, garde données personnelles, aucun secret dans une session ; en cas de fuite, rotation immédiate (le secret est perdu) |
| R2 | File de CI (14 tâches par PR, workflows de données en journée) | Majeur | Branches sans PR jusqu'au lot prêt, filtres de chemins, e2e sur étiquette, données la nuit, train quotidien |
| R3 | Collision de fichiers entre pistes ou avec les chantiers « fiche client », synchro et pharmacies | Majeur | Propriété par répertoire, fichiers chauds créés une fois par P1, réservations dans `PROPRIETE-FICHIERS.md`, migrations additives |
| R4 | Plafond de routines ou quotas Opus atteints | Majeur | 5 + 1 routines ; Opus réservé à la conception, à la sécurité et aux fins de lot ; si le plafond baisse, les pistes I et K attendent (V1), jamais la chaîne critique |
| R5 | Changement de compte Claude : routines arrêtées | Majeur | Consignes dans le dépôt, travail poussé toutes les heures, REPRENDRE de 40 lignes : reprise en 5 min |
| R6 | Port 25 refusé chez Hetzner et OVH | Majeur | Deux demandes en parallèle en S5 ; critère d'abandon (J3) : pas de réponse au 15 déc → troisième hébergeur ; la chaîne critique continue sur le banc |
| R7 | Will indisponible (décisions, train, réponses) | Majeur | Décisions groupées en S1, train de 10 min, délégation possible, frein et mode absence (E7) |
| R8 | Chauffe plafonnée faute de personnes titulaires des boîtes (06 B3) | Majeur | Décision W1 ; sinon, cible 600/j annoncée honnêtement |
| R9 | Estimations fausses de ± 30 % | Moyen | Avancement mesuré en j-agent réels ; calendrier recalé chaque vendredi par `crm-controle` |
| R10 | Un déploiement du train casse la production | Majeur | Module derrière drapeau, migrations compatibles avec la version précédente, déploiement d'activation unique et validé |
| R11 | Agent Sonnet qui « contourne » un test (skip, seuil abaissé) | Majeur | Interdit dans la consigne ; relecture Opus qui compare les tests avant et après ; garde CI contre `skip` ajouté |
| R12 | RLS prouvée en test mais pas en production | Critique | S7 : refus de démarrer sans RLS ; T1 rejoue le test des deux clients en préproduction |
| R13 | Interface jugée « pas assez claire » tard | Moyen | Maquettes testées en S3 avant le code, un écran par PR, U10 avant T1 |
| R14 | Fêtes de fin d'année | Faible | S8-S9 prévues creuses, pas de train les jours fériés |

---

## Verdict

- **Premier envoi réel limité (20 organisateurs) : vers le 2-3 février 2027.** Fourchette : fin janvier (décisions et achats en S1, 6 routines tenues) à début mars (port 25 refusé deux fois, ou plafond à 4 routines). Premier envoi interne vers le 27 janvier. Banc OK vers le 11 décembre.
- **Version console (client pilote installé, isolé, facturable) : vers le 15 avril 2027.** Fourchette : fin mars à mi-mai. Le client pilote envoie à volume réel vers juin 2027, après sa propre chauffe.
- **2 000 par jour pour Axion : vers le 4 mai 2027**, seulement si 14 à 16 boîtes ont des personnes titulaires. Sinon, environ 600 par jour.
- Ce qui ne s'accélère pas : 21 jours d'âge des domaines, un mois avant le port 25, 6 à 9 semaines de chauffe. Ce qui accélère vraiment : les décisions W1 et les achats **dès la semaine du 2 novembre**.

## Résumé (20 lignes)

1. Plan chiffré unique : 62 lots plus 7 actions hors code, chaque fonction comptée une fois. V0 ≈ 246 j-agent (283 avec relectures), V1 et console ≈ 186 (213), V2 ≈ 92 (106).
2. Jusqu'à la version console : ≈ 432 j-agent (≈ 496 avec relectures), à ± 30 %.
3. Les anciens totaux (223, 315, 338, 323-363) ne comptaient que l'envoi. Le « 185 j » de 02 fait en réalité 215 j. Les ≈ 46 j en double sont retirés.
4. Le plan intègre 04, 05, 07 (13 écrans), 08 (F1-F19), 11 (8 ajouts) et les manques de 06. N1-N5 et la marque blanche sont exclus ; F20 et F21 attendent une décision.
5. Les 8 règles de préparation sont des lots dès la V0 (P1-P6, S7).
6. Chaîne critique : P1 → P2 → E1 → E5 → E7 → C1 → écrans → T1, ≈ 52 j-agent en série, soit ≈ 13 semaines.
7. Parallélisme : 11 pistes possédant chacune leurs répertoires, 5 actives à la fois en Sonnet, plus 1 routine Opus de contrôle.
8. Les fichiers chauds (routes, provider, menu) sont créés une seule fois par P1, puis jamais partagés.
9. Hors code à lancer la semaine du 2 novembre : domaines (21 j), Hetzner et OVH (port 25 vers le 4 déc), boîtes, vérificateur, CNIL.
10. Les consignes des routines sont stockées dans le dépôt : un changement de compte Claude se répare en 5 min.
11. Les routines poussent leur branche en continu, ce qui ne lance aucune CI. Une PR par lot, ouverte seulement quand le lot est prêt.
12. Train de fusion quotidien à 18:00 : au plus 2 déploiements, module derrière drapeau, un seul déploiement d'activation en S13.
13. CI : 14 tâches par PR aujourd'hui. Filtres de chemins, e2e sur étiquette, workflows de données la nuit. Gitleaks et Semgrep exigés sans minute de plus.
14. Jamais en CI : SMTP, port 25, DNS réel, serveurs, secrets, coureurs payants.
15. Jalons : banc OK ≈ 11 déc ; premier envoi interne ≈ 27 janv ; premier envoi réel ≈ 2-3 fév 2027.
16. Montée : 250/j ≈ 22 mars, 1 000/j ≈ 13 avril, 2 000/j ≈ 4 mai (si boîtes tenues par de vraies personnes).
17. Version console ≈ 15 avril 2027 ; client pilote à volume réel ≈ juin 2027.
18. Will intervient 10 fois, surtout en S1 (décisions, achats, CNIL), puis environ 10 min par jour pour le train.
19. Gouvernance : avancement en % par phase (lot fait = fusionné et prouvé), REPRENDRE de 40 lignes, registre des décisions, critique en 6 questions à chaque lot.
20. Risques principaux : secret publié, file de CI, collisions, quotas, port 25, disponibilité de Will. Chacun a sa parade (§ 6).
