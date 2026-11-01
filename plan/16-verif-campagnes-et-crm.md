# 16 : Vérification « campagnes et CRM » du plan CRM Pro complet (01/11/2026)

Responsable : campagnes et CRM. **Lecture seule** : aucun code applicatif modifié, aucun e-mail envoyé, aucun serveur touché, aucun secret lu ni recopié. Rien n'est codé.

**Matière lue** : `plan/00`, `01`, `02`, `03`, `04`, `05`, `06`, `08`, `10`, `11`, `REPRENDRE.md` ; le code `axion-crm-pro` au commit `ce80ca9` (31/10, soit 5 PR après le `1f7b0caa` lu par le plan : #382 à #386, toutes sur la carte « Reçu de la console » de la fiche entreprise). Vérifié dans le code : `ContactsController.php:165-185` (modifier et retirer un contact répondent toujours 501) ; `routes/api.php:607-608` (`/cold-email` et `/linkedin` toujours en 501) ; `EnsureTwoFactorPassed.php:34` (`VALIDITY_SECONDS = 43200`, soit 12 h) ; `Crm/Campagnes/Segments.php:66` (`OUVERTS_PAR_DEFAUT = CONNUS` : presse **ouverte** par défaut, réglage **global** par variable d'environnement, pas par espace) ; `Crm/Pharmacies/*` (import FINESS, téléphones FINESS, groupements : la donnée des pharmacies existe déjà) ; `Crm/Outbound/` (seul `ConsentOutboundRecorder` : le sens CRM → console ne porte encore que les oppositions).

**Exemple de produit de Will** (document du 26/10, absent du dépôt, reconstitué par recoupement de `06` B1, B2, B6, M5, M7 et § 4.5, et de `10` § 0 et § 7) :
1. un **seul logiciel** CRM qui sert **plusieurs clients en même temps** ;
2. un **socle vendu** qui comprend une **base de prospects sectorielle**, propriété d'Axion, **attribuée ou retirée** par la console ;
3. des **options payantes** déverrouillées une à une (campagnes, assistant IA, tableau de bord avancé) : bouton grisé, activation à la souscription, désactivation à l'arrêt ;
4. trois niveaux de réglages avec héritage : plateforme, puis secteur, puis client ; un 2e secteur s'ajoute **sans toucher au code** ;
5. des étapes commerciales : à contacter, contacté, répondu, rendez-vous, devis, gagné, perdu ;
6. facturation : acompte avant de commencer, mise en place puis abonnement, impayé = relance puis suspension ;
7. ordre conseillé : fondation multi-clients, console avec paiement, bases sectorielles, campagnes, IA ;
8. **premier client : une société qui vend aux pharmacies** (module « Pharmacies », téléphone connu pour environ 87 % des officines, e-mail pour environ 5 %).

**Décisions de Will rappelées** : V1 = mise en place puis abonnement, **tout sur notre moteur mutualisé**, installation chez le client = V2 (24/10, « ne pas redemander ») ; **deux modes de vente permanents** : vente directe sur **son** serveur, ou mise en place + abonnement (26/10) ; complet en fonctions, seuls les volumes démarrent petit ; campagnes au cœur ; alertes **console + e-mail seulement** ; aucun lien avec systeme.io.

**Hors champ, volontairement** (consigne de Will) : constructeur visuel d'automatisations, modèles clients, agenda par client, connecteur systeme.io, serveur MCP, marque blanche. Rien de ce fichier ne les propose. Le § 4.B dit au contraire où le plan les contient encore et qu'il faut les retirer.

---

## 1. Le plan couvre-t-il l'exemple de produit et les décisions de Will ?

| # | Exigence | Ce que dit le plan | Verdict | Correction (n° du § 6) |
|---|---|---|---|---|
| P1 | Un seul logiciel pour tous les clients (mutualisé) | 02 M0, 03 § 1.1 et R4, 05 D-C5 : « une installation par client **d'abord**, mutualisé plus tard, sous conditions » | **CONTRAIRE** à la décision du 24/10 | CC-01 |
| P2 | Deux modes de vente permanents (26/10) | Le plan mélange les deux : il fait de « l'installation dédiée » le mode par défaut, alors que c'est le mode « vente directe » | **CONFUS** | CC-01 |
| P3 | Base sectorielle vendue, attribuée ou retirée | 03 § 1.3, 05 D-C3, 02 M1 : « les données d'Axion ne vont **jamais** chez un client » | **CONTRAIRE** (déjà signalé par 06 B1, non corrigé) | CC-02 |
| P4 | Options payantes déverrouillées une à une | Rien. 02 M5 ne prévoit que des compteurs et un lien Stripe | **ABSENT** | CC-03 |
| P5 | Réglages plateforme, puis secteur, puis client | 02 M3 : réglages par client seulement | **ABSENT** (niveau secteur) | CC-03 |
| P6 | Étapes commerciales de Will | 02 D1 : taxonomie du code (nouveau, qualifié, opportunité, client, dormant, perdu) | **ÉCART** | CC-13 |
| P7 | Facturation (acompte, abonnement, impayé) | 02 M5 « Stripe » ; rien sur l'endroit où vivent les factures | **ABSENT** (06 B6, non corrigé) | CC-04 |
| P8 | Premier client vendant aux pharmacies | Segment santé/FINESS **fermé** par défaut (03 G4), canal téléphone en P1 seulement (02 E4) | **BLOQUANT** pour ce client | CC-02, CC-09 |
| P9 | CRM = module de base de la console, envoi = option | 10 § 0 le dit ; aucun lot ne code « l'envoi est une option activable » | **PARTIEL** | CC-03, CC-27 |
| P10 | Moteur d'envoi partagé, séparé par client | 03 § 1.2 : IP, domaines, boîtes, opposition, chauffe par locataire | **COUVERT** | — |
| P11 | Alertes console + e-mail seulement | 03 § 7.8, § 13 V1 et 08 C4 gardent un « connecteur Telegram facultatif » | **ÉCART** à retirer | CC-31 |
| P12 | Ordre de l'exemple (fondation multi-clients d'abord) | Le plan commence par l'envoi d'Axion | **À DÉCIDER** par Will (06 Q2) ; ma recommandation : V0 Axion, mais modèle de données mutualisé et base sectorielle **conçus dès la V0** (CC-02, CC-05) | CC-05 |

**Conclusion du § 1** : la partie « envoi » couvre l'exemple ; la partie « produit vendu » le contredit sur 3 points (P1, P3, P8) et l'ignore sur 3 autres (P4, P5, P7). La critique 06 l'avait vu ; **aucun fichier n'a été corrigé depuis**.

---

## 2. Parcours de bout en bout d'une campagne

Chaque étape : ce que le plan prévoit, puis le trou. Les trous renvoient au § 6.

| Étape | Prévu (référence) | Trou | n° |
|---|---|---|---|
| **1. Choisir la cible** | Ciblage ET/OU/SAUF imbriqué, exclusions par historique, aperçu en direct, volume envoyable (03 § 2.2 ; 02 E2, C9, C10) | (a) Un client ne peut pas cibler la **base sectorielle** qu'on lui vend (P3). (b) Les pharmacies sont dans un segment fermé, et l'ouverture des segments est un **réglage global** (`CRM_SEGMENTS_OUVERTS`), pas un réglage par espace (`Segments.php:66`). (c) Avec environ 5 % d'e-mails connus, l'aperçu dira « 95 % non joignables » sans proposer d'autre canal. | CC-02, CC-09, CC-20 |
| **2. Écrire les messages** | Gabarits versionnés, variables en liste blanche, contrôleur (03 § 2.3 ; 02 E5, E7) | **Personne n'écrit les textes** (06 B4 non corrigé). La cible de Will (TPE/PME qui ne savent pas par où commencer avec l'IA) n'a aucune séquence. Pour un client, rien ne dit qui rédige : lui ou Axion pendant la mise en place. | CC-06 |
| **3. Règles de contenu de Will** | Liste dans 02 « Cadre » ; contrôleur « formulations interdites » (02 E7) | La liste n'est **ni une table ni un test** : elle vit dans un paragraphe. « On s'occupe de tout » (06 B4) n'y figure pas. Les règles sont celles **d'Axion** et ne doivent pas s'imposer à un client, qui a les siennes. Le questionnaire « jamais automatique » (06 M9) et « aucun lien vers axion-ia.com dans un message à froid » (06 C2) ne sont pas codés. | CC-07 |
| **4. Personnaliser par IA** | V2 seulement (03 § 2.3, CAM-026/028/030) ; P2 dans 02 E13 | Will veut un outil complet, et « assistant IA » est une **option payante** de son exemple : la V2 est trop tard. Le plan ne dit pas comment concilier un texte différent par destinataire avec « validation attachée à **une** version ». | CC-08 |
| **5. Valider** | Validation par l'owner sur l'empreinte de la version, aperçu de 20 messages, feu vert de 31 cases (03 § 2.6) | Pas de bouton « m'envoyer un test » par modèle (11 n° 1). Sinon couvert. | CC-15 |
| **6. Planifier et envoyer** | Fenêtres de Paris, vagues de 07:10, tranches, pression, chauffe (03 § 2.5, § 3) | Décalage de 2 h (02 L9) en P0 : bien. **Aucune garde sur le pays** du destinataire (06 C1). | CC-16 |
| **7. Rebond** | Webhook idempotent, rebond dur = suppression, 3e mou = suppression, seuils 2 % (03 § 3.2, § 6) | Couvert. Manque : un rebond dur sur l'adresse d'une officine dont on a le téléphone devrait proposer une **tâche d'appel** au lieu de laisser la fiche morte. | CC-09 |
| **8. Plainte** | ARF par IMAP, plaintes authentifiées seules dans les seuils, pause du locataire à 0,3 % (03 § 1.3, § 6) | (a) Les grandes messageries françaises (Orange, SFR, Free) ne passent pas par les FBL citées (Microsoft, Yahoo) : rien n'est prévu pour Signal Spam (à vérifier). (b) La **plainte écrite dans une réponse** (« c'est du spam », « je vais signaler à la CNIL ») n'a pas de règle propre. | CC-18, CC-19 |
| **9. STOP** | STOP clair → opposition, sinon file « à confirmer » ; opposition par domaine (02 F3, J3) | Le STOP **dit au téléphone** n'a aucun chemin vers `opt_out` (06 C5). La portée « ne plus figurer dans la base d'Axion » (base sectorielle) n'existe pas : seule l'opposition « à ce client » existe. | CC-02, CC-09 |
| **10. Réponse** | Relève IMAP, tri par règles, écran Réponses, arrêt de séquence, alerte à 24 h (02 F1-F9) | (a) Pas d'**avis immédiat** pour un « intéressé » (11 n° 2). (b) **Aucun frein** quand les réponses s'accumulent (06 C7). (c) Pas de mode « absence de Will ». (d) **Boîtes de réponse tenues par une seule personne** : la courbe exige 14 à 16 boîtes nominatives en V1, Will est seul (06 B3). | CC-10, CC-11 |
| **11. Relance** | 1 à 4 étapes en jours ouvrés, expéditeur collant, absence = pause (03 § 2.4) | (a) La pause sur absence du bureau est en **V1** : en V0, une relance tombera pendant les congés. (b) Rien ne dit que la relance part **dans le même fil** (« Re: », `In-Reply-To`) et sans répéter le bloc art. 14. (c) Pas d'étape « appel » en V0. | CC-14, CC-09 |
| **12. Arrêt** | Arrêt par adresse sur réponse, rebond, STOP, plainte, RDV, client, « répondu ailleurs » (03 § 2.4) | Arrêt « au niveau de l'entreprise » laissé « au choix » (02 F9) : pour une officine ou une TPE, il faut l'arrêt par entreprise **par défaut**. Une issue d'appel « pas intéressé » n'arrête pas les e-mails. | CC-14, CC-09 |
| **13. RDV pris** | Calendly reçu du site, attribution à la campagne sur 90 jours, arrêt de séquence (02 G1-G4) | Valable pour **Axion seulement**. Un client n'a pas le Calendly d'Axion, et il ne faut pas lui construire d'agenda. Rien n'est prévu pour un RDV pris **au téléphone**. G4 pose « opportunité » alors que l'exemple de Will a une étape « rendez-vous ». | CC-12, CC-13 |

**Conclusion du § 2** : la chaîne technique (cibler, composer, envoyer, retours, arrêts) est complète. Les trous sont **humains et métier** : qui écrit, quelles règles de contenu, quelle IA, quel canal quand il n'y a pas d'e-mail, que faire quand Will ne suit pas, combien de personnes réelles derrière les boîtes, et le RDV d'un client.

---

## 3. CRM au quotidien : est-ce complet ?

| Fonction | État du code (31/10) | Plan | Verdict | n° |
|---|---|---|---|---|
| Fiches entreprise | EXISTE | 02 A1 | Complet | — |
| Fiches personne : modifier, retirer | **501** (`ContactsController.php:165-185`) | 02 A3, P0 | Couvert | — |
| Ajout rapide, notes, appels | MANQUE / PARTIEL | 02 A4, A5, P1 | Couvert, mais l'**issue d'appel** n'est pas modélisée | CC-09 |
| Import de fichier par l'interface | MANQUE (CLI seulement) | 02 B4, **P1** | **Trop tard** : c'est la 1re action d'un client à la mise en route | CC-23 |
| Doublons | EXISTE (fusion réversible) | 02 A8 | Complet ; le dédoublonnage à l'import est prévu dans B4 | — |
| Étiquettes | EXISTE | 02 C1 | Complet | — |
| Listes, audiences | EXISTE | 02 C2, C3 | Complet | — |
| Vues sauvegardées | API sans écran | 02 C4, P1 | Couvert | — |
| **Actions de masse** | partielles (pose d'étiquettes) | Citées dans le lot 2 et dans 10 § 1 (« permission sur la modification en masse »), **sans ligne ni effort** | **TROU** | CC-22 |
| Pipeline Kanban | MANQUE | 02 D2, P1 | Couvert, mais avec les **mauvaises étapes** | CC-13 |
| Tâches, « Mes tâches », rappels | Tâches par fiche EXISTE ; vue et rappels MANQUE | 02 D4-D7, P1 | À passer en **V0** : les étapes d'appel et les réponses créent des tâches | CC-26 |
| Champs personnalisés | MANQUE (JSONB `signals`) | 02 A12 **P2** ; 08 F7 « V1 » | Contradiction de priorité ; **P0 avant le 1er client** | CC-24 |
| Rôles | 4 rôles et 16 permissions figés | 02 I8 (P1), M2 (P0 client) | Couvert pour les rôles ; **cycle de vie des utilisateurs absent** (inviter, désactiver, départ d'un salarié du client, réinitialiser la 2FA, dernier owner protégé) | CC-25 |
| Exports | EXISTE, journalisés, droit `data.export` | 02 B1, B5, B7 | Couvert pour Axion ; **aucune limite à l'export de la base sectorielle** par un client, qui repartirait avec la propriété d'Axion | CC-28 |
| Synchro avec la console **du site** (dossier client) | Console → CRM EXISTE et s'enrichit (#379 à #386) ; CRM → console = oppositions seulement | 02 K1-K6, K2 en P0 | Couvert ; le plan n'a pas vu les PR #379-#386 : K2 reste le vrai manque | — |
| Synchro avec la console **des automatisations** (CRM vendu comme module) | Rien | 02 M5, M11 ; 05 « API signée » ; 10 § 7 | **PARTIEL** : usage et quotas seulement. Manquent : activer ou suspendre un espace, activer ou retirer une option, état d'abonnement, attribution de base, santé et version | CC-27 |
| Journal, RGPD, corbeille | EXISTE | 02 J1, J4 | Complet | — |

**Conclusion du § 3** : le CRM quotidien d'Axion sera complet une fois le lot 2 de 02 fait, **plus** les actions de masse (CC-22) et « Mes tâches » remontée en V0 (CC-26). Pour un client, il manque 5 choses : import par l'interface, champs personnalisés, cycle de vie des utilisateurs, limites d'export de la base, pilotage par la console.

---

## 4. Contradictions entre fichiers, et mon arbitrage

### 4.A Les 5 contradictions demandées

| # | Sujet | Positions | Arbitrage recommandé | Fichiers à corriger |
|---|---|---|---|---|
| X-1 | **Volume de départ** | 01 § 1 : « 150 par jour au plus » ; 02 lot 3 : « première campagne de 150 messages » et « premier envoi à 150 messages par jour » ; 03 § 3.1 : P1 = **20**/jour, 250 en fin de V0 ; 00 et 10 : « 20-50 puis environ 300 » | **La courbe de 03 fait foi** : 20 → 35 → 50 → … → 250 en V0, en jours effectifs. C'est la plus prudente, et c'est la seule qui soit liée à des ressources (boîtes, domaines). La sortie du lot 3 de 02 devient : « première campagne validée, partie au palier P1 (20/jour), suivie jusqu'au palier P3 sans incident ». | 01 § 1 ; 02 lot 3 et paragraphe « Ce qui démarre petit » |
| X-2 | **Durée de la 2FA** | 04 décision 4 et code : 2FA valable **12 h** (`VALIDITY_SECONDS = 43200`) ; 02 décision 4 : **appareil de confiance 30 jours** (recommandé) | Ce sont **deux réglages différents**, pas deux réponses à la même question. Je recommande de garder les deux : (1) **session de 12 h au plus** (réglage actuel, inchangé) ; (2) **appareil de confiance 30 jours**, c'est-à-dire pas de nouveau code à la connexion sur cet appareil, mais un cookie signé, lié à l'appareil, révocable dans la liste des appareils (02 I9, remontée en V0) et perdu dès que le mot de passe change ; (3) **code toujours redemandé** pour les gestes sensibles : export, levée d'une suppression, ouverture d'un segment, validation d'une campagne, levée d'un arrêt d'urgence, ajout d'un utilisateur. Une seule question à poser à Will : « 30 jours, oui ou non ». | 02 décision 4 ; 04 décision 4 ; 06 Q6 |
| X-3 | **Presse ouverte ou fermée** | Cahier CAM-064 : fermée ; code (`Segments.php:30`, 01/10) : **ouverte par défaut** ; 03 § 2.9 : « la décision de Will du 01/10 prime » ; 03 G4 et 02 « Cadre » : « segments presse et santé fermés par défaut » ; 02 décision 7 : « presse rouverte par réglage explicite ? » ; 06 : « presse fermée attribuée à tort à Will » | **La presse est ouverte dans l'espace Axion** : c'est la décision du 01/10, à ne pas redemander. **Tout nouvel espace démarre tout fermé** (règle G4), et chaque ouverture est une case tracée de l'owner. Le réglage passe de la variable d'environnement globale à un **réglage par espace** : l'ouverture d'Axion est reprise à la migration avec la date du 01/10 comme trace. On corrige le registre (CAM-064) et la phrase de 02 « Cadre ». | 02 « Cadre » et décision 7 ; 03 G4 ; registre CAM-064 |
| X-4 | **Plafonds de coût** contre « le prix informe, ne bloque pas » | 03 § 1.2 : « le plafond le plus bas s'applique » ; VER-015 et CAM-030 passent en « indisponible » au plafond ; 02 « Cadre », 02 H8, 05 § B, 08 B18 : le prix informe | **Séparer deux plafonds.** (1) Le **plafond technique**, en messages par jour (chauffe, réputation, plafond local du serveur), reste **dur** : c'est de la sécurité, pas du prix. (2) Tout **plafond en euros** (vérification, IA, serveurs, usage d'un client) **informe** : alerte console + e-mail à 80 % et à 100 %, ligne au rapport du matin, **jamais de blocage ni de clic de validation**. Le risque de dérive reste borné sans plafond en euros : on ne vérifie que ce qu'on enverra sous 30 jours, et ce volume est lui-même plafonné par la chauffe. Chez un client, le dépassement est facturé selon son forfait (05 § B). VER-015 et CAM-030 passent de « bloque » à « informe ». La question 06 Q9 disparaît. | 03 § 1.2 et § 4 ; registre VER-015, CAM-030 ; 06 Q9 |
| X-5 | **Chiffrages concurrents** | 223,5 j (D-86 accéléré du cahier) ; ≈ 315 j (D-86 complet, synthèse de l'audit) ; ≈ 338 j (critique de l'audit) ; 323 à 363 j (03 : V0 138 + V1 115-135 + V2 70-90) ; plus 185 j de CRM (02), dont environ 46 j en double (06 § 4.2 ; 10) ; plus 49 j (08 § F) et 4,25 j (11 § 18) ; 04 et 05 non chiffrés | **Retirer les trois premiers chiffres** : ils viennent du cahier d'envoi seul, sur un autre périmètre. Garder **un seul total, calculé lot par lot** et découpé selon la grille de versions de CC-05. Mon calcul est au § 5.3 : **V0 ≈ 222 j, V1 ≈ 274 j, V2 ≈ 107 j, soit ≈ 603 j-agent** (± 30 %, plus 15 % de relectures). Il est à reprendre tel quel dans le plan corrigé, puis à recouper par le fichier 17 (calendrier). | 00 ; 03 § 13 ; 08 E10 ; 10 en-tête ; 06 Q5 |

### 4.B Autres contradictions trouvées

| # | Sujet | Arbitrage |
|---|---|---|
| X-6 | **V0/V1/V2 ne veulent pas dire la même chose.** Dans 03, ce sont des **volumes** (V1 = 1 000 à 2 000 par jour). Pour Will (24/10), ce sont des **modes de déploiement** (V1 = mutualisé, V2 = chez le client). | Une seule grille, qui tient les deux : CC-05. |
| X-7 | « Données d'Axion jamais chez un client » (03 § 1.3, 05 D-C3, 02 M1) contre la base sectorielle vendue de l'exemple | L'exemple de Will prime : CC-02. La phrase devient : « aucune donnée d'Axion n'est **visible** chez un client **sauf** les fiches de la base sectorielle qui lui sont **attribuées**, tracées et retirables ». |
| X-8 | « Santé/FINESS fermé par défaut » (03 G4) contre un premier client qui vend aux pharmacies | Fermé dans l'espace Axion ; ouvert dans l'espace du client **par l'attribution** de la base Pharmacies (case tracée de son owner) : CC-20. |
| X-9 | Marque blanche encore au plan : 02 M4 (3 j, P2) ; 08 F9 et B13 (« pages à la marque du client ») | **Retirer 02 M4.** Dans 08 F9 et B13, remplacer « à la marque du client » par « **au nom légal du client** » : identité de l'annonceur, exigée par la LCEN, sans logo ni couleurs. |
| X-10 | Telegram « facultatif » (03 § 7.8, § 13 V1, § 15.2 ; 08 C4 ; 11 n° 18-20 « réutilisable en 0,3 j ») ; 06 X2 propose de rouvrir la question | **Retirer le connecteur.** Alertes = console + e-mail, c'est la consigne actuelle. La question 06 Q7 disparaît. |
| X-11 | Étape posée au RDV : « opportunité » (02 G4) ; l'exemple de Will a « rendez-vous » | « rendez-vous » : CC-13. |
| X-12 | Champs personnalisés : P2 (02 A12), V1 (08 F7) | P0 avant le premier client (CC-24). |
| X-13 | Avis de réponse : « alerte à 24 h seulement » (02 F8, P1) ; « avis immédiat » (11 n° 2, V0) | Les deux, en V0 (CC-10). |
| X-14 | Battement externe : V1 (11 n° 8) ; « silence impossible » (06 C6) | V0, parce que c'est de la sécurité (CC-17). |
| X-15 | Cible de Will (TPE/PME) ; premier segment ouvert = organisateurs et fédérations ; INSEE fermé (06 B4) | La V0 écrit les 3 séquences (CC-06). L'ouverture INSEE reste une décision de Will (02 décision 7), sans la redemander si elle a déjà été tranchée. |
| X-16 | **Trous du document lui-même** : 02 n'a pas de « lot 1 » (00 l'annonce à 22 j) ; 02 saute C5-C7, I2-I4 et L3 alors que L3 (« mailer ») est cité 4 fois ; 03 cite G8 (R12) absent du tableau § 8 ; 03 § 9 saute l'étape 6 (mode recette, citée dans le résumé) ; 04 a 3 sections vides ; 10 § 3 et § 6 sont vides ; la liste « URGENT » de 00 commence au n° 4 | Correction documentaire (CC-30) : rétablir ou supprimer chaque renvoi orphelin. |

---

## 5. Versions V0 / V1 / V2

### 5.1 Grille unique (CC-05)

| Version | Pour qui | Déploiement | Volume d'envoi | Contenu |
|---|---|---|---|---|
| **V0** | Axion seul | Instance d'Axion, **déjà multi-espace** (Axion = un espace parmi d'autres, 8 règles de 10 § 8) | 20 → 250-300 par jour (paliers P1-P7 de 03) | Toute la sécurité (§ 5.2), toute la chaîne de campagne e-mail, le CRM quotidien d'Axion |
| **V1** | Axion + clients de la console (1er client : pharmacies) | **Mutualisé** : mode « mise en place + abonnement » (24/10) | Par espace : sa propre courbe. Axion jusqu'à 600 par jour avec Will seul, jusqu'à 2 000 avec des personnes nommées (CC-11) | Base sectorielle, options, droits, état d'abonnement, téléphone, IA, import par l'interface, champs personnalisés, lettre d'information |
| **V2** | Clients en vente directe | **Installation sur le serveur du client** (2e mode de vente, 26/10) : même image, mise à jour par tirage | jusqu'à 5 000 par jour (D-28), plusieurs serveurs | Installation en une commande, mises à jour par vagues, repli Postfix, confort |

### 5.2 V0 minimale, mais complète en sécurité

« Minimale » veut dire : un seul espace réel (Axion) et un seul canal automatique (l'e-mail). **Aucune protection n'est reportée.** Liste fermée de ce que la V0 doit contenir :

1. **Accès** : 2FA par code e-mail (04 PR-0 à PR-E), session de 12 h, appareil de confiance 30 jours révocable, code redemandé pour les gestes sensibles (X-2), liste des appareils et déconnexion à distance (02 I9, remontée), lien magique atomique et codes non réutilisables (02 I10, remontée), mailer d'authentification isolé.
2. **Cloisonnement** : RLS armée, **refus de démarrer** sans elle (02 I5), tests sous le rôle applicatif, test à deux espaces factices, IDOR en boîte noire, `workspace_id` sur `opt_out` et `email_suppressions` (03 E1). Le mutualisé de la V1 n'a ainsi plus rien à prouver.
3. **Droits** : permission sur les actions de masse (CC-22) ; un admin ne peut plus nommer un owner ; segments sensibles fermés par défaut et réglés **par espace** (X-3).
4. **Envoi** : une seule porte `EnvoiAutorise`, `peutRecevoir()` à la vague et moins de 15 minutes avant l'injection, échec fermé, gardes G1 à G12 avec G8 rétablie, garde pays France (CC-16), garde questionnaire (CC-07), aucun lien vers axion-ia.com dans un message à froid (CC-07), pas de pixel, désinscription RFC 8058 et `mailto:`, retrait en moins de 5 minutes, disjoncteurs (8 portées), homme mort, plafond local dur, arrêt d'urgence prouvé par son effet.
5. **Contenu** : règles de contenu en table et testées (CC-07), bloc art. 14 et identité de l'entité exigés, validation attachée à la version.
6. **Humain** : frein de capacité de réponse et mode absence (CC-10), avis immédiat pour un « intéressé ».
7. **Surveillance** : alertes console + e-mail, **battement externe** qui écrit à Will si le CRM se tait (CC-17), alerte de test hebdomadaire de bout en bout, sonde externe du serveur d'envoi, boîtes témoins.
8. **Données** : sauvegarde chiffrée, copie hors site quotidienne, restauration testée et datée (02 L2), sauvegarde rapprochée des oppositions, journal d'audit chaîné, exports journalisés avec code 2FA.
9. **Dépôt** : Gitleaks et Semgrep exigés pour fusionner, aucun secret, aucun nom de client, aucune IP.

Ce qui est **fonctionnellement** dans la V0 : chaîne de campagne e-mail complète (§ 2 étapes 1 à 13, avec le RDV Calendly d'Axion), CRM du lot 2 de 02 (avec « Mes tâches » et les rappels), textes des 3 séquences d'Axion, brouillon IA de séquence (CC-08 a).

Ce qui attend la **V1** : base sectorielle, options et droits, état d'abonnement, téléphone, accroche IA par destinataire, import par l'interface, champs personnalisés, cycle de vie des utilisateurs, A/B, presse complète, lettre d'information.

Je mets le **téléphone en V1**, parce qu'il sert le premier client. Si Will veut appeler ses propres TPE/PME dès la V0, CC-09 passe en V0 (+9 j) : rien dans la conception ne l'empêche.

### 5.3 Enveloppe unique (remplace 223 / 315 / 338 / 323-363)

| Source | V0 | V1 | V2 | Note |
|---|---|---|---|---|
| 03 module d'envoi | 138 | 125 (milieu de 115-135) | 80 (milieu de 70-90) | — |
| 02 CRM hors envoi (185 − 46 en double − 3 de marque blanche = 136) | 49 (lot 1 = 22, part V0 du lot 2 ≈ 12, lignes CRM des lots 3-4 hors 03 ≈ 15) | 87 | — | Le découpage V0 est le mien |
| 04 sécurité (7 PR, non chiffrées) | 6 | — | — | Mon estimation |
| 05 lots uniques (copie de KumoMTA, repli Postfix + rspamd) | 0,5 | — | 10 | Le reste de 05 recouvre 02 lot 5 et 03 E1 |
| 08 § F (49 − 5 déjà dans 02 A12 et E19, tous deux en V1) | 6,5 | 20,5 | 17 | — |
| 11 § 18 | 2,25 | 2 | — | — |
| **Ce fichier** (§ 6) | 20 | 39 | — | Détail au § 6 |
| **Total** | **≈ 222** | **≈ 274** | **≈ 107** | **≈ 603 j-agent**, ± 30 %, + 15 % de relectures ≈ 690 |

Le chemin critique de la V0 (environ 92 j en série selon 06 § 4.1) et les horloges hors code (domaines de 21 jours, port 25) relèvent du fichier 17.

---

## 6. Trous : correction exacte, effort, priorité

Effort en jours-agent, tests compris, hors relectures (+15 %). Priorité : **P0-V0** avant le premier envoi d'Axion ; **P0-V1** avant le premier client ; **P1** dans la version indiquée.

| n° | Trou | Correction exacte | Effort | Priorité |
|---|---|---|---|---|
| **CC-01** | Modèle de déploiement contraire aux décisions du 24 et du 26/10 | Réécrire 02 M0, 03 § 1.1 et R4, 05 B et D-C5 : « **V1 = mutualisé** (mode "mise en place + abonnement") ; **V2 = installation sur le serveur du client** (mode "vente directe") ; même image, même code ». Le motif de prudence (RLS non prouvée) devient une **condition d'entrée de la V1** : RLS armée, tests sous le rôle applicatif, test à deux espaces factices, IDOR. Elle est déjà dans la V0 (§ 5.2 point 2), donc elle ne retarde rien. | 0,5 (doc) | P0-V0 |
| **CC-02** | Base sectorielle vendue absente, et même interdite | **Modèle « fiche de référence + surcouche »** : la fiche de référence (FINESS, INSEE…) appartient à la plateforme, en lecture seule pour les espaces ; chaque espace a sa surcouche (étape, notes, étiquettes, champs, tâches, oppositions). Table `attributions_base` (secteur, espace, début, fin, motif, auteur). **Retrait** à la fin de l'abonnement : l'accès à la référence est coupé sans rien supprimer, et la surcouche du client lui reste exportable. Les mises à jour FINESS se propagent à tous les espaces attribués. **Deux oppositions distinctes** : « ne plus être contacté par ce client » (dans l'espace du client) et « ne plus figurer dans la base d'Axion » (sur la référence, qui retire la fiche de toutes les attributions et que tous les clients respectent). Textes : art. 14 d'Axion (transmission à des clients), art. 14 du client (source = base d'Axion), contrat de mise à disposition (rédigé par l'IA puis relu avec Will, méthode du 27/10). Réécrire 03 § 1.3, 05 D-C3, 02 M1. | 10 (code) + 2 (textes) | P0-V1 ; **modèle de données conçu en V0** dans l'ADR E0 |
| **CC-03** | Options payantes et réglages par secteur absents | Table `fonctions_espace` (CRM de base ; options : Envoi, Téléphone, Assistant IA, Tableau de bord avancé, une ligne par base sectorielle). Héritage **plateforme → secteur → espace** pour les réglages (critères de ciblage, étapes du pipeline, champs, heures d'envoi, segments ouverts), **sans catalogue de modèles**. Option inactive = bouton grisé avec « Activer depuis la console ». Option retirée = données en lecture seule, campagnes en cours mises en pause proprement, rien de supprimé. Les ordres viennent de la console par l'API signée (CC-27). Test exigé par l'exemple : « ajouter un faux 2e secteur sans toucher au code ». | 6 | P0-V1 |
| **CC-04** | Facturation non située | Écrire : « les factures, l'acompte, Stripe et Tiime vivent dans le **Hub de la console** (décision du 27/10) ; le CRM ne facture rien ». Le CRM reçoit l'**état d'abonnement** (actif, impayé, suspendu, résilié). En état « suspendu », il **suspend l'envoi** (pause propre, aucune donnée touchée) et garde la lecture. Il remonte l'usage (02 M5). C'est un statut commercial décidé dans la console, pas une validation de prix. | 2 (côté CRM) | P0-V1 |
| **CC-05** | Grille de versions double | Adopter la grille du § 5.1 dans 00, 03 (encadré « Vocabulaire ») et 10 § 0. | 0,5 (doc) | P0-V0 |
| **CC-06** | Personne n'écrit les messages | Lot « rédaction » : un rédacteur Opus écrit **3 séquences** pour Axion (TPE/PME, organisateurs, fédérations), chacune avec objet, J0, J+7, J+14, signature sans téléphone, et la page publique « pourquoi ce message » servie **sous le domaine d'envoi**. Chaque texte passe le contrôleur (CC-07) et la validation de Will. Pour un client : les textes sont écrits **pendant la mise en place** (prestation d'Axion, hors code) ou par le client, puis saisis dans **ses** gabarits et validés par **son** owner. Le brouillon IA (CC-08 a) sert aux deux. | 3 (+ temps de Will) | P0-V0 |
| **CC-07** | Règles de contenu de Will non codées | Table versionnée `regles_contenu` **par espace** : expression, effet (bloque ou avertit), motif, auteur, date. Elle est amorcée pour Axion avec la liste de 02 « Cadre », plus « on s'occupe de tout », plus toute promesse de gain. Un client démarre avec les seules règles **légales** de la plateforme (identité, art. 14, pas de pixel) et ajoute les siennes. Un test par règle. Deux gardes de plateforme : (1) le lien ou le gabarit du questionnaire est **refusé** dans toute séquence et tout envoi automatique (06 M9) ; (2) **aucun lien vers `axion-ia.com`** dans un message à froid, la page art. 14 et le RDV étant servis sous le domaine d'envoi (06 C2). | 3 (dont 2 déjà dans 02 E7) | P0-V0 |
| **CC-08** | IA de personnalisation trop tardive (V2) et mal encadrée | **(a) V0, brouillon de séquence** : à partir d'un brief (cible, offre, ton), l'IA propose objet et étapes ; le texte devient un gabarit ordinaire, contrôlé et validé. **(b) V1, option « Assistant IA », accroche par destinataire** : une phrase générée **avant la validation**, à partir des seuls champs autorisés de la fiche (secteur, ville, événement, fonction). Garde « aucun fait inventé » : tout nom propre ou chiffre de la phrase doit venir des champs fournis, sinon la phrase est rejetée et le gabarit sans accroche est utilisé. Le contrôleur passe sur 100 % des messages rendus. L'owner valide un échantillon de 20 et la liste des rejets. Le texte est **figé par empreinte**, et rien n'est généré au moment de l'envoi. La règle « validation attachée à une version » tient donc toujours. Modèle Sonnet (**jamais Haiku**), fournisseur sous contrat de sous-traitance, coût affiché (informe, X-4). Remplace CAM-026/028/030 en V2 et 02 E13 en P2. | 2 (a) + 4 (b) | (a) P0-V0 ; (b) P0-V1 |
| **CC-09** | Pas de canal téléphone (officines : e-mail connu pour environ 5 %) | **Campagne multicanal** : une séquence mêle étapes e-mail et étapes **appel**. L'appel crée une tâche dans une **file d'appels** ordonnée, avec plages horaires réglables (heures d'ouverture des officines), lien `tel:` (aucune numérotation automatique, aucun enregistrement) et **script** versionné et validé comme un gabarit. **Issues fermées** : joint, absent, rappeler le…, intéressé, pas intéressé, opposition, mauvais numéro, RDV pris, a donné son e-mail. « Opposition » écrit `opt_out` (canal téléphone) et arrête **tous** les canaux. « Pas intéressé » arrête la séquence. « A donné son e-mail » crée l'adresse avec la provenance « recueillie par téléphone le … » et le bloc art. 14 au premier e-mail. Un rebond dur sur une fiche qui a un téléphone propose une étape d'appel. **Pression commune** e-mail + téléphone. Statistiques : appels, joints, intéressés, RDV. Fiche juridique courte : démarchage téléphonique entre professionnels, objet lié à l'activité, liste d'opposition interne toujours tenue, applicabilité des règles d'opt-in du démarchage des consommateurs **à vérifier**. Les numéros FINESS existent déjà (`Crm/Pharmacies/TelephonesFiness.php`). | 9 | P0-V1 (P0-V0 si Will appelle lui-même) |
| **CC-10** | Aucun frein quand les réponses s'accumulent ; pas d'avis immédiat ; pas de mode absence | (1) Réglage par espace : « réponses que je peux traiter par jour » (15 par défaut). (2) **Budget des premiers messages** = min(chauffe, capacité ÷ taux de réponse observé sur 14 jours), jamais sous P1. (3) **Frein dur** : plus de 10 « intéressé » ou plus de 25 réponses à traiter depuis plus de 24 h ouvrées → plus de premiers messages, plus de nouvelles vagues, relances suspendues. Les STOP, oppositions, retraits et arrêts continuent. Levée automatique quand le stock redescend, journalisée. (4) **Mode absence** (dates) : même effet, relances décalées, récapitulatif au retour. (5) **Avis immédiat** console + e-mail pour un « intéressé », regroupé par 15 minutes, sans donnée personnelle dans l'objet (11 n° 2). Bandeau d'accueil : « 12 réponses attendent, envois ralentis ». | 3 | P0-V0 |
| **CC-11** | Boîtes nominatives et une seule personne | Règle écrite : **une boîte par personne réelle et par domaine**, au plus 4 domaines par personne, 150 messages par jour par boîte (CHA-037). Avec Will seul : 4 boîtes, soit **600 par jour au plus**. La V0 (≤ 4 boîtes) passe telle quelle. 2 000 par jour en V1 demande environ 14 boîtes, donc environ 4 personnes nommées, avec leur accord écrit (RES-039). Sinon Axion plafonne à 600. Toutes les boîtes relèvent dans **un seul écran Réponses** : une seule personne peut tout lire, et c'est CC-10 qui protège sa capacité. Registre « personne signataire » dans E4. Recalculer 03 § 3.1 (P8 à P13) et § 11 avec cette règle. | 1 | P0-V0 (décision) |
| **CC-12** | RDV d'un client (sans agenda par client) et RDV pris par téléphone | Variable `{lien_rdv}` réglée par espace (l'outil de prise de RDV du client, quel qu'il soit). Bouton **« RDV pris »** sur une réponse, une issue d'appel ou une fiche : il arrête la séquence, pose l'étape « rendez-vous » et attribue le RDV à la dernière campagne et étape qui ont touché la personne (fenêtre de 90 jours, comme 02 G3). L'attribution automatique par Calendly reste réservée à l'espace Axion. Aucun agenda n'est construit. | 1,5 | P0-V1 |
| **CC-13** | Étapes commerciales différentes de celles de Will | Jeu par défaut de l'exemple : à contacter, contacté, répondu, rendez-vous, devis, gagné, perdu. Réglable par secteur, puis par espace (CC-03). Correspondance écrite avec `Taxonomy.php:239-246` (migration sans perte, ancienne valeur à l'historique). Automatismes : premier envoi → contacté, réponse → répondu, RDV → rendez-vous. Jamais de recul automatique. Pour Axion, « devis » reste informatif (le devis vit dans la console du site). Réécrire 02 D1, G4. | 2 | P0-V0 |
| **CC-14** | Relances et arrêts incomplets | (1) Pause sur absence du bureau (CAM-037) **remontée en V0**. (2) Relance **dans le même fil** (`In-Reply-To`, « Re: » + objet), même boîte, sans répéter le bloc art. 14 s'il a déjà été livré. (3) Arrêt **par entreprise par défaut** pour les entreprises de moins de 10 salariés et les officines, réglable. (4) Geste « a répondu ailleurs » disponible sur la fiche et dans la file d'appels. | 1,5 | P0-V0 |
| **CC-15** | Pas de test par modèle ou par campagne | Bouton « M'envoyer un test » par modèle et par campagne, hors comptage de la chauffe, par la même porte (11 n° 1). | 0,5 (déjà compté dans 11) | P0-V0 |
| **CC-16** | Pas de garde sur le pays | Destinataire hors France = **refus** (pays de l'organisation, domaine national, indicatif téléphonique). Ouverture par pays seulement après une fiche juridique validée par Will (06 C1). | 1 | P0-V0 |
| **CC-17** | Personne ne surveille le système d'alerte | Battement de cœur vers un service externe gratuit, qui écrit à Will si le CRM se tait. Alerte de test hebdomadaire de bout en bout. Seconde adresse de réception des alertes, hors du domaine d'Axion (06 C6, 11 n° 8 remonté). | 0,5 (déjà compté dans 11) | P0-V0 |
| **CC-18** | Pas de FBL française | Vérifier, puis inscrire les domaines d'envoi à la boucle de retour de Signal Spam. Si elle existe, la relever comme une FBL (même service `AppliquerRetour`). | 0,5 | P1-V0 |
| **CC-19** | Plainte écrite dans une réponse | Règle de tri : expressions « spam », « signaler », « CNIL », « harcèlement » → **opposition immédiate**, arrêt par entreprise, alerte, et comptage comme « plainte non authentifiée » (alerte et tenue du palier, sans disjoncteur). | 0,5 | P0-V0 |
| **CC-20** | Segments réglés globalement | Passer `CRM_SEGMENTS_OUVERTS` à un **réglage par espace** (table, avec auteur et date). Reprise de l'ouverture presse d'Axion du 01/10 (X-3). Santé/FINESS ouvert seulement par une attribution de base (CC-02). Variable absente = tout fermé pour un nouvel espace. | 1 | P0-V0 |
| **CC-22** | Actions de masse sans ligne ni permission | Sélection (liste, filtre, audience) → étiquette, liste, étape, propriétaire, corbeille. Permission `fiches.modifier_en_masse`, limite de 5 000 par action, aperçu « N fiches vont changer », journal d'une ligne par lot, **annulation** du lot (8 s à l'écran, puis restauration par le journal), jamais de suppression. | 2 | P0-V0 |
| **CC-23** | Import par l'interface trop tardif | 02 B4 passe de P1 à **P0-V1**, avec en plus, pour un client, la case « je garantis la base légale de ce fichier » et le contrôle d'un échantillon avant la première campagne (06 M8). | 0 (déjà 4 j dans 02) | P0-V1 |
| **CC-24** | Champs personnalisés en P2 | 02 A12 passe en **P0-V1**, avec héritage secteur → espace (CC-03) et usage comme variables de gabarit (liste blanche) et comme critères de ciblage. | 0 (déjà 3 j dans 02) | P0-V1 |
| **CC-25** | Cycle de vie des utilisateurs d'un espace | Inviter (lien à usage unique, 2FA dès la première connexion), désactiver (jamais supprimer), transférer le portefeuille et les tâches, réinitialiser la 2FA avec code de l'owner, dernier owner protégé, accès du support d'Axion limité dans le temps et journalisé (02 M2). | 1,5 (en plus de 02 M2) | P0-V1 |
| **CC-26** | « Mes tâches » et rappels en P1 | 02 D5, D6 et D7 passent en **P0-V0** : les étapes d'appel, les réponses et les RDV créent des tâches. Le rappel du matin passe par e-mail et par la console. | 0 (déjà 5 j dans 02) | P0-V0 |
| **CC-27** | Pilotage par la console des automatisations | API signée (HMAC dans l'en-tête, idempotente, rejouable), dans les deux sens. **Console → CRM** : créer, suspendre ou réactiver un espace ; activer ou retirer une option (CC-03) ; attribuer ou retirer une base (CC-02) ; état d'abonnement (CC-04). **CRM → console** : usage (remise à zéro à la date anniversaire), santé, version, alertes de l'espace. Écran « Santé de la liaison » (comme 02 K4). | 2 (en plus de 02 M5 et M11) | P0-V1 |
| **CC-28** | Export de la base sectorielle sans limite | Dans un espace client, l'export porte sur la **surcouche** et sur les fiches que le client a **travaillées** (contactées, notées, en pipeline). L'export brut de la référence attribuée est refusé. Plafond par export, code 2FA, journal, alerte à Axion au-delà d'un seuil. | 1 | P0-V1 |
| **CC-30** | Trous du document (X-16) | Ajouter le lot 1 dans 02 ; rétablir ou retirer C5-C7, I2-I4, L3, G8 et l'étape 6 de 03 § 9 ; remplir ou retirer les sections vides de 04 et de 10 § 3 et § 6 ; renuméroter la liste URGENT de 00. | 0,5 | P0-V0 (plan corrigé) |
| **CC-31** | Éléments refusés encore au plan (X-9, X-10) | Retirer 02 M4 (marque blanche, −3 j). Retirer le connecteur Telegram de 03 § 7.8, § 13 V1, § 15.2 et de 08 C4 (−0,3 j). Dans 08 F9 et B13, remplacer « à la marque du client » par « au nom légal du client ». Retirer 06 Q7. | 0,25 | P0-V0 (plan corrigé) |

**Totaux de ce fichier** (nouveaux jours seulement, hors lignes déjà chiffrées ailleurs) : **V0 ≈ 20 j**, soit CC-01, 05, 06, 07 (+1), 08 a, 10, 11, 13, 14, 16, 18, 19, 20, 22, 30 et 31 ; **V1 ≈ 39 j**, soit CC-02, 03, 04, 08 b, 09, 12, 25, 27 et 28. Total **≈ 59 j-agent**, ≈ 68 avec les relectures.

**Questions à poser à Will** (une à une, avec la recommandation ; rien de ce qu'il a déjà tranché) :
1. Appareil de confiance 30 jours, en plus de la session de 12 h : oui (recommandé) ?
2. Combien de personnes réelles peuvent prêter leur nom à des boîtes d'envoi ? Sans réponse, Axion plafonne à 600 par jour.
3. Le téléphone en V0 pour vos propres prospects, ou en V1 avec le premier client (recommandé) ?
4. Capacité de traitement des réponses : 15 par jour par défaut, est-ce juste ?

---

## 7. Verdict

**Complet pour Axion ? Pas encore, mais presque.** La chaîne d'envoi et de campagne est spécifiée en entier et souvent mieux que les anciens outils. Il manque environ **20 jours-agent**, surtout humains et métier : les textes (personne ne les écrit), les règles de contenu de Will codées, le frein quand les réponses s'accumulent et le mode absence, la règle « une boîte par personne réelle » (600 par jour avec Will seul), les étapes commerciales de Will, les actions de masse, la garde pays et le battement externe. Avec ces ajouts, la V0 (≈ 222 j-agent) est **complète pour Axion**, sans aucune protection reportée.

**Complet pour être mis dans la console ? Non.** Le plan **contredit** l'exemple de produit de Will sur 3 points : il installe chez le client d'abord au lieu du mutualisé du 24/10, il interdit la base sectorielle qu'il faut vendre, et il ferme le secteur santé du premier client. Il **ignore** les options payantes, les réglages par secteur, l'état d'abonnement et le pilotage par la console. Il n'a **pas de téléphone**, alors que le premier client n'a d'e-mail que pour environ 5 % des officines. Il faut les corrections CC-01 à CC-04, CC-09, CC-12, CC-20 et CC-23 à CC-28, soit environ **39 j-agent** en plus de la V1 déjà prévue. La V1 (≈ 274 j) devient alors un vrai module de base de la console, avec l'envoi en option.

---

## Résumé (20 lignes)

1. Lecture seule : plan 00 à 11 et code au commit `ce80ca9` ; rien n'est codé, aucun envoi, aucun secret.
2. L'exemple de produit de Will, reconstitué depuis 06 et 10 : un logiciel pour tous, base sectorielle vendue, options payantes, 1er client qui vend aux pharmacies.
3. Le plan contredit le 24/10 (V1 mutualisée) et le 26/10 (deux modes de vente) : il installe chez le client d'abord. Correction CC-01.
4. Il interdit la base sectorielle (« données d'Axion jamais chez un client ») : fiche de référence + surcouche par espace + attributions retirables (CC-02, 12 j).
5. Options payantes, réglages par secteur et état d'abonnement sont absents (CC-03, CC-04, CC-27).
6. Parcours de campagne : la technique est complète, les trous sont humains et métier.
7. Personne n'écrit les messages : lot rédaction de 3 séquences (CC-06). Règles de contenu de Will en table testée par espace (CC-07).
8. IA : brouillon de séquence en V0, accroche par destinataire en V1, figée avant validation, sans fait inventé, jamais Haiku (CC-08).
9. Téléphone absent alors que l'e-mail n'est connu que pour ~5 % des officines : campagne multicanal, file d'appels, issues, opposition téléphonique (CC-09, 9 j).
10. Frein de capacité de réponse, mode absence, avis immédiat d'un « intéressé » (CC-10). Une boîte par personne réelle : Will seul = 600/jour (CC-11).
11. RDV d'un client sans agenda : `{lien_rdv}` + bouton « RDV pris » (CC-12) ; étapes de Will par défaut (CC-13).
12. CRM quotidien : complet pour Axion avec les actions de masse (CC-22) et « Mes tâches » en V0 ; pour un client, il manque l'import, les champs, les utilisateurs et la limite d'export.
13. Volume de départ : la courbe de 03 fait foi (20/jour, 250 en fin de V0) ; corriger 01 et 02.
14. 2FA : session 12 h ET appareil de confiance 30 jours révocable, code redemandé pour les gestes sensibles.
15. Presse : ouverte dans l'espace Axion (01/10), tout fermé par défaut ailleurs, réglage par espace.
16. Coûts : plafond technique dur, plafond en euros qui informe seulement.
17. Chiffrages : une seule enveloppe, V0 ≈ 222, V1 ≈ 274, V2 ≈ 107, soit ≈ 603 j-agent (± 30 %).
18. Grille unique : V0 Axion, V1 console mutualisée, V2 chez le client. V0 minimale en fonctions, complète en sécurité (§ 5.2).
19. Marque blanche (02 M4) et Telegram (03, 08) encore au plan : à retirer (CC-31).
20. Verdict : complet pour Axion après ≈ 20 j d'ajouts ; pas complet pour la console sans ≈ 39 j d'ajouts en V1.
