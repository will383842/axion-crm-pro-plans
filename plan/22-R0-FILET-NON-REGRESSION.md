# 22 : LOT R0 : filet de non-régression (01/11/2026)

**But.** Avant le premier lot de code du plan 20 (S1), poser une suite de tests qui dit « **ce qui marche aujourd'hui marche encore demain** ». Si un lot casse l'existant, la CI devient rouge et **rien ne part en production**.

**Base** : le relevé `plan/21-R0-RELEVE-EXISTANT.md` (risques R1 à R16) et le § 11 du plan 20.

**Rien n'est codé ici.** Ce fichier dit **quels tests écrire, dans quel ordre, combien de temps, et comment la CI les rend bloquants.**

---

## 1. En bref (10 lignes)

1. **24 tests** (ou petites familles de tests) : un par risque élevé ou moyen du fichier 21.
2. Ils vivent tous dans **un seul dossier** du CRM : `backend/tests/Feature/NonRegression/` (plus 3 tests côté frontend), marqués du groupe Pest `non-regression`.
3. Beaucoup de gardes **existent déjà** (391 fichiers de tests) : le filet **les cite et les verrouille**, il ne les réécrit pas.
4. Ordre : d'abord ce qui protège les personnes (opposition, gardes légales), puis l'isolation et les tâches planifiées, puis les canaux et le déploiement, puis les écrans.
5. Effort : **≈ 5,5 j-agent** (R0 était estimé à ≈ 4 j au § 11 du plan 20 : **+ 1,5 j**).
6. **Une photo de référence** (« instantané ») est prise une fois, sur la version actuelle : liste des tâches planifiées, des routes, des drapeaux, des tables de l'export RGPD. Les tests comparent à cette photo.
7. Chaque lot de code part **derrière un drapeau éteint par défaut** et a **une ligne de retour arrière**.
8. La CI existante (`ci.yml`) joue déjà toute la suite sur chaque PR : on ajoute **un job court et dédié**, qui part en premier.
9. Le dépôt est **public** : les machines standard de GitHub sont **gratuites et sans limite de minutes**. On n'utilise **ni grosse machine payante, ni service extérieur payant**.
10. Une **liste figée** des tests du filet empêche qu'un test soit retiré ou mis en quarantaine en silence.

---

## 2. Règles du filet

1. **Un test du filet ne se modifie que pour une raison écrite** (décision de Will ou changement voulu par un lot), dans la même PR que le changement, avec la ligne « Filet modifié : pourquoi ».
2. **Jamais de quarantaine** pour un test du filet (même règle que la CI actuelle depuis le 16/08).
3. **Tout se fait sur des données factices** : deux espaces factices (« Espace A », « Espace B »), des adresses en `example.test`, aucune personne réelle.
4. **Aucun test ne touche un serveur**, n'envoie un e-mail ou n'appelle un service extérieur (simulateurs obligatoires en test).
5. **Les tests tournent sous le rôle de base de production** (le rôle applicatif qui porte la RLS) dès que S7 commence, comme le font déjà les tests `…SousRlsTest`.
6. **Instantané** : les fichiers de référence sont rangés dans `backend/tests/Feature/NonRegression/instantanes/`. Les régénérer demande une commande explicite et apparaît en clair dans la PR.

---

## 3. La liste des tests (un par risque)

**Colonnes** : **Existe** = garde déjà présente dans le CRM qu'on rattache au filet ; **À écrire** = nouveau test ; **j** = effort en jours-agent.

### Bloc 1 : protéger les personnes (à faire en premier)

| N° | Risque (fichier 21) | Ce que le test vérifie | Existe déjà | À écrire | j |
|---|---|---|---|---|---|
| NR-01 | R3 opposition | Une adresse en `opt_out` ou en `email_suppressions` n'est **jamais** proposée, quel que soit le chemin (préparation, audience, export, futur moteur C1) | `EligibiliteCampagneTest`, `AucunEnvoiSansEligibiliteTest`, `OppositionCouvreTousLesUniversTest`, `ExportsRespectentOppositionsTest` | une version **« deux espaces »** : l'opposition d'Axion bloque dans l'espace Axion ; celle de A ne bloque pas B (prépare P2) | 0,5 |
| NR-02 | R4 préparation des destinataires | Sur un jeu factice fixe, `crm:campagne:destinataires` rend **exactement** la même liste et les mêmes compteurs d'écart qu'aujourd'hui (instantané) | `ResolveurDestinatairesTest`, `CampagneAdressesPartageesTest`, `CampagnesB2bTest` | l'instantané « liste + compteurs » | 0,5 |
| NR-03 | R5 retours | `crm:campagne:retours` : `envoye` pose la date art. 14 sans jamais la reculer ; désinscription et plainte = opposition définitive ; rebond dur = suppression ; rien n'est jamais **ajouté** ; `--dry-run` n'écrit rien | 3 tests existants citent la commande | un test « fichier de retours factice complet → état final de la base » | 0,5 |
| NR-04 | R2 garde Sirene | Une fiche non diffusible ou fermée n'est jamais contactable ; la sonde de 06:20 sort en échec si une fiche n'est pas marquée | `OppositionInseeNonDiffusibleTest`, `PurgeNonDiffusibleVariantesTest` | rattacher au groupe ; ajouter « non diffusible ⇒ jamais supprimée » (décision C3 : sans suppression) | 0,25 |
| NR-05 | R16 segments fermés | Sans `CRM_SEGMENTS_OUVERTS`, aucun segment sensible n'est ouvert ; un nouvel espace = tout fermé | — | à écrire | 0,25 |
| NR-06 | R13 export RGPD | L'export d'une personne factice contient **au moins** toutes les tables qu'il contient aujourd'hui (instantané de la liste des tables) ; l'effacement efface partout | `PortabiliteCompleteTest`, `GdprErasureTest`, `SiteGdprTest` | l'instantané « tables de l'export » (sert à l'arbitrage des tables d'ébauche) | 0,5 |

### Bloc 2 : l'isolation et les tâches qui tournent seules

| N° | Risque | Ce que le test vérifie | Existe déjà | À écrire | j |
|---|---|---|---|---|---|
| NR-07 | R1 tâches planifiées | **Liste des tâches** : noms, horaires, verrous, drapeaux de saut = instantané. Ajouter, retirer ou déplacer une tâche fait rougir le test tant que l'instantané n'est pas mis à jour **dans la même PR** | `VerrousDuPlanificateurTest`, `CommentairesDuPlanificateurTest` | l'instantané complet (44 tâches + battement) | 0,5 |
| NR-08 | R1 tâches sous RLS | Chaque tâche qui lit des fiches, lancée **sous le rôle de production** avec deux espaces factices, voit les lignes de **son** espace (pas zéro, pas celles de l'autre) | nombreux `…SousRlsTest`, `RafraichissementNocturneSousRlsTest` | une boucle sur les tâches de l'instantané NR-07 (en commençant par les 10 qui touchent les fiches) | 1 |
| NR-09 | R15 journal d'audit | La chaîne d'audit se vérifie ; la maintenance des partitions crée bien la partition suivante | garde existante sur la vérification de la chaîne | test « partition du mois suivant créée » | 0,25 |
| NR-10 | R8 purges | Drapeau `CRM_PURGE_ENABLED` éteint ⇒ purges **sautées et écrites au journal** ; les commandes de purge d'entreprises refusent sans `--force` ; aucune purge ne touche une fiche venue de la console | `AutomatismesDePurgeTest`, `PurgesDestructricesTest` | « fiche venue de la console jamais purgée » | 0,25 |

### Bloc 3 : les canaux, les drapeaux, le déploiement

| N° | Risque | Ce que le test vérifie | Existe déjà | À écrire | j |
|---|---|---|---|---|---|
| NR-11 | R6 synchro du site | Drapeau éteint ⇒ 503 et rien écrit ; signature fausse, horodatage trop vieux ou rejoué ⇒ refus ; un événement de chaque type connu donne le même résultat qu'aujourd'hui (instantané) | `SiteSyncIngestTest`, `SiteGdprTest` | l'instantané « un événement par type → fiche obtenue » | 0,5 |
| NR-12 | R7 CRM → site | Drapeau éteint ⇒ rien n'est envoyé ; ouvert (avec faux site) ⇒ une opposition née dans le CRM part une seule fois | `CrmOutboundTest` | rattacher au groupe | 0,1 |
| NR-13 | R6 Partners | Mode `off` ⇒ 404 ; mode ouvert ⇒ signature, rejeu, idempotence | `CanalPartnersSocleTest` | rattacher au groupe | 0,1 |
| NR-14 | — (moyen) webhook transactionnel | Sans jeton ⇒ 503 ; un rebond reçu ⇒ ligne de suppression | `ListeSuppressionTest` | rattacher au groupe | 0,1 |
| NR-15 | R9 simulateurs | En production, **chaque** `MOCK_*` (y compris `MOCK_MAIL`, `MOCK_IGN`, `MOCK_RPPS`) est refusé ; tout nouveau simulateur (serveur d'envoi de E1) doit être déclaré dans la garde | `AucunSimulacreEnProductionTest`, `DrapeauxMockAlignesTest`, `SimulacresLusHorsDeLaGardeTest` | étendre aux 3 drapeaux non couverts ; test « liste des simulateurs = liste de la garde » | 0,25 |
| NR-16 | R9 et § 4 drapeaux | **Instantané des drapeaux** : chaque `CRM_*` et `MOCK_*` a la même valeur par défaut qu'aujourd'hui (éteint). Un nouveau drapeau doit être éteint par défaut | — | à écrire (lecture de `config/*.php`) | 0,25 |
| NR-17 | R10 migrations | Toute **nouvelle** migration (après la date de R0) fait l'aller, le retour, puis l'aller sur une base jetable sans erreur ; les 23 anciennes au retour vide ou refusé sont listées et figées | `migrate:rollback` cité par 1 test | à écrire (job CI, voir § 6) | 0,5 |
| NR-18 | R11 déploiement | Les workflows de déploiement gardent `needs: [ci]` ; aucun workflow ne se connecte au serveur sans être dans la liste connue (25) ; la sauvegarde reste surveillée | `WorkflowsBornesDeDureeTest`, `SurveillanceCanauxWorkflowTest`, `ImagesConstruitesSontDeployeesTest` | « liste des workflows qui touchent un serveur = instantané » (elle ne peut que **baisser**, S11) | 0,25 |

### Bloc 4 : les écrans et l'API

| N° | Risque | Ce que le test vérifie | Existe déjà | À écrire | j |
|---|---|---|---|---|---|
| NR-19 | R12 « campagnes » | Les adresses actuelles `/campaigns…` (écran et API de collecte) répondent toujours, **ou** redirigent vers le nouveau nom après le renommage | `CampaignsTest`, e2e `campaigns-wizard` | test de route et de redirection | 0,25 |
| NR-20 | § 9 routes | **Instantané des routes** du serveur (méthode, chemin, protections) ; une route retirée fait rougir ; chaque appel du frontend vise une route qui existe | `PasDeStub501SousCrmEtAnalyticsTest` | à écrire (côté serveur + petit test Vitest côté frontend) | 0,5 |
| NR-21 | § 9 écrans | **Instantané de `routeTree`** : les 54 adresses d'écran existent toujours (ou redirigent) | e2e `navigation` | test Vitest | 0,1 |
| NR-22 | R14 connexion | Connexion complète avec la 2FA **actuelle** (mot de passe, code, lien magique, mot de passe oublié) en e2e, verte jusqu'à S12 | `LoginTest`, `MagicLinkServiceTest`, e2e `auth` | e2e de bout en bout (l'e2e `auth` était rouge en août : à remettre vert) | 0,25 |
| NR-23 | moyen : audiences | Une audience factice donne le même nombre de fiches avant et après un lot | tests audiences, e2e `audiences-builder` | instantané du compte | 0,1 |
| NR-24 | moyen : couverture | La matrice de couverture se rafraîchit sous le rôle de production | garde d'août sur la matrice | rattacher au groupe | 0,1 |

**Total bloc 1 à 4 : ≈ 7,7 j avant regroupement.** Une grande partie se fait en même temps (mêmes jeux factices, même dossier) : **effort retenu ≈ 4,5 j**, plus **1 j** pour le job CI, la liste figée et la photo de référence. **Total R0 (filet) ≈ 5,5 j-agent.**

---

## 4. Ordre et calendrier

| Étape | Contenu | j | Prérequis |
|---|---|---|---|
| 0 | Mesurer les « vérités à vérifier » du fichier 21 § 10 (points 1, 2, 7, 9) sur une copie locale à jour | 0,5 | copie locale du CRM à jour |
| 1 | Socle : dossier, groupe `non-regression`, deux espaces factices, outil d'instantané | 0,5 | étape 0 |
| 2 | Bloc 1 (NR-01 à NR-06) | 1,5 | 1 |
| 3 | Bloc 2 (NR-07 à NR-10) | 1,25 | 1 |
| 4 | Bloc 3 (NR-11 à NR-18) | 1 | 1 |
| 5 | Bloc 4 (NR-19 à NR-24) | 0,5 | 1 |
| 6 | Job CI, liste figée, protection de branche (Will) | 0,25 + 10 min de Will | 2 à 5 |

Les étapes 2 à 5 peuvent tourner **en parallèle** (2 routines). **Aucun lot S1 ne démarre avant la fin de l'étape 6.**

---

## 5. Drapeaux éteints par défaut et retour arrière (un par lot)

**Règle** : chaque lot qui change un comportement visible part derrière un drapeau **éteint par défaut** (`false` dans `config/*.php` et `.env.example`), vérifié par NR-16. Le retour arrière tient **en une ligne**.

| Lot | Drapeau (nom proposé) | Retour arrière en une ligne |
|---|---|---|
| S1 | `CRM_AUTH_DURCIE_ENABLED` | éteindre le drapeau |
| S2 | `CRM_MAILER_AUTH_ISOLE_ENABLED` | éteindre le drapeau (ancien mailer) |
| S3 | `CRM_2FA_EMAIL_ENABLED` | éteindre : la 2FA actuelle reste en place jusqu'à S12 |
| S4 | `CRM_ECRANS_SECURITE_V2` | éteindre : anciens écrans |
| S6 | `CRM_DROITS_V2_ENABLED` | éteindre le drapeau |
| S7 | `CRM_DB_APP_ROLE_ENABLED` (existe) | éteindre : retour au rôle actuel ; **jamais avant** rejeu en préproduction (NR-08) |
| S8 | `CRM_HORODATAGE_PARIS_ENABLED` | éteindre ; migration réversible |
| S9 | aucun drapeau (ajout pur) | désactiver la nouvelle tâche planifiée |
| P1 | `CRM_MODULE_ENVOI_ENABLED` | éteindre le module |
| P2 | `CRM_OPPOSITION_PAR_ESPACE_ENABLED` | éteindre : lecture comme aujourd'hui ; migration réversible (colonne ajoutée, rien retiré) |
| P3 | aucun (refonte interne) | revenir à la version précédente (`git revert` de la PR) |
| P4 | `CRM_CANAL_CONSOLE_MODE=off` | remettre `off` |
| P5 | `CRM_ARRET_PAR_ESPACE_ENABLED` | éteindre |
| E1 à E8 | `CRM_MODULE_ENVOI_ENABLED` + `CRM_ENVOI_TEMOINS_SEULEMENT=true` | éteindre le module ; témoins seulement reste verrouillé |
| C1 | `CRM_CAMPAGNES_EMAIL_ENABLED` | éteindre : la chaîne à la main (`crm:campagne:*`) reste utilisable |
| C1 (renommage) | aucun | redirection gardée ; `git revert` du renommage |
| C2, C3 | sous `CRM_CAMPAGNES_EMAIL_ENABLED` | éteindre (les gardes C3 restent **toujours** actives) |
| RP1 à RP3 | `CRM_REPONSES_ENABLED` | éteindre |
| U0 | aucun (types générés) | `git revert` |
| U2 à U12 | `CRM_ECRANS_2027` (par écran si possible) | éteindre : anciens écrans |
| Q1 | `CRM_CONTACTS_EDITION_ENABLED` | éteindre : liste en lecture seule comme aujourd'hui |
| Q1b | `CRM_TACHES_ENABLED` | éteindre |
| J1 | `CRM_ART14_BLOC_ENABLED` | **pas de retour arrière en production** une fois ouvert (obligation légale) : seulement en préproduction |
| ADR consoles / synchro | `CRM_SYNC_DOSSIER_CLIENT_STAGE` (existe), `CRM_OUTBOUND_ENABLED` (existe) | remettre à `false` |
| T1 | aucun | — |

**Migrations** : toute nouvelle migration a un `down()` qui marche (NR-17). Si une migration ne peut pas revenir en arrière (données retirées), elle est **découpée** : d'abord ajouter, ensuite (dans un lot plus tard, après une sauvegarde vérifiée) retirer.

---

## 6. Comment la CI rend le filet bloquant (sans minute payante)

**Situation actuelle (lue, à confirmer)** : `ci.yml` joue toute la suite Pest sur un vrai Postgres à chaque PR ; `e2e.yml` est bloquant ; les deux déploiements ont `needs: [ci]`. C'est une bonne base.

**Ce qu'on ajoute :**

1. **Un job `filet-non-regression`** dans `ci.yml` :
   - lance `pest --group=non-regression` (quelques minutes), **avant** le gros job backend ;
   - lance les 3 tests Vitest du filet (routes et `routeTree`) ;
   - lance le test des migrations aller-retour-aller (NR-17) sur la base Postgres jetable déjà créée par la CI ;
   - porte un `timeout-minutes` (règle existante) ;
   - **jamais** de `continue-on-error`.
2. **Une liste figée** `backend/tests/Feature/NonRegression/LISTE.json` : chaque test du filet y est nommé. Un test vérifie que chaque nom existe et porte le groupe `non-regression` ; retirer un test sans le retirer de la liste fait rougir.
3. **Le déploiement attend le filet** : il appelle déjà `ci.yml`, donc il attend le nouveau job sans rien changer d'autre.
4. **Protection de la branche `main`** (geste de Will, 10 minutes, dans les réglages GitHub) : rendre obligatoires les contrôles « filet-non-regression », « backend », « frontend » et « Suites e2e ». Sans ce geste, une fusion pourrait passer malgré un rouge. C'est **gratuit**.
5. **Pas de minute payante** :
   - le dépôt est public : les machines standard `ubuntu-24.04` de GitHub sont gratuites et sans limite de minutes ;
   - **ne pas** utiliser de « grosse machine » (payante même sur un dépôt public), ni de service de tests extérieur payant ;
   - garder le filet court (objectif : moins de 10 minutes) pour qu'il reste un premier verrou rapide ;
   - pas de lancement planifié en plus : le filet tourne **sur chaque PR** et sur l'appel du déploiement, c'est assez.
6. **Rien de secret dans la CI du filet** : pas de clé de serveur, pas de vrai service ; les secrets de test sont des valeurs factices écrites dans la config de test, comme aujourd'hui.

---

## 7. Ce qui reste à vérifier en exécution (par un agent, plus tard)

Reprend le fichier 21 § 10, avec ce qui concerne directement le filet :

1. La suite actuelle (Pest, Vitest, e2e) est-elle **verte** sur `main` aujourd'hui ? Sinon, réparer d'abord : un filet sur une base rouge ne protège rien.
2. Durée réelle de la CI actuelle (pour placer le job du filet sans dépasser les bornes).
3. Contrôles réellement **obligatoires** dans la protection de `main` (non lisible depuis le code).
4. `php artisan schedule:list` et `route:list --json` sur une copie locale : base des instantanés NR-07 et NR-20.
5. Les tâches planifiées donnent-elles le même nombre de lignes sous le rôle de production ? (base de NR-08).
6. Valeur réelle des drapeaux en production et préproduction (lecture seule, sans afficher de secret) : un drapeau **déjà allumé** sur le serveur change le sens de NR-11, NR-12 et NR-10.
7. Liste exacte des tables lues par l'export RGPD (base de NR-06).
8. Les 23 migrations au retour vide ou refusé : confirmées sur une base jetable.
9. L'e2e `auth` (rouge en août) est-il redevenu vert ?
10. Le workflow ancien de récupération (`diag-website-status`) est-il encore utile ? (sinon le retirer en premier dans S11).

---

## 8. Effet sur le plan 20

- **R0** = relevé (fichier 21, fait) + filet (ce fichier) ≈ **5,5 j-agent** au lieu de ≈ 4 j : **+ 1,5 j en V0**, à prendre dans l'enveloppe « + 15 à 20 j » du § 11 du plan 20.
- **S1 ne démarre qu'après** le job `filet-non-regression` vert et la protection de branche posée par Will.
- Chaque lot du plan 20 ajoute dans sa PR : son drapeau éteint, sa ligne de retour arrière, et, s'il change un instantané, la ligne « Filet modifié : pourquoi ».
