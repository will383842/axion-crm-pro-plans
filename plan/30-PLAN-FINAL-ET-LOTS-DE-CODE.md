# 30 : PLAN FINAL ET LOTS DE CODE : la démo d'abord, la sécurité de l'existant en parallèle (lot W0, 01/11/2026)

## Résumé (15 lignes)

1. **Total consolidé : ≈ 685,5 j-agent** (≈ 788 avec relectures) = 637,5 j du plan 29 + **48 j des 52 ajouts du plan 27**, qui n'étaient pas encore dans les « ≈ 638 j » (détail : `plan/20` § 12).
2. **Par famille** : socle ≈ 157,5 j ; CRM Pro ≈ 108,5 j ; Envoi ≈ 419,5 j. **Déjà fait ≈ 14 j** (maquettes validées, ADR, spécifications) ; **rien n'est codé**.
3. La démo frontend (DM0 à DM3, ≈ 80 j) est découpée en **19 lots de code**, chacun exécutable par une routine cloud seule, avec son texte prêt à copier dans `plan/lots/<id>.md`.
4. **Vague 0 (3 lots, semaine 1)** : DM0-COL (renommer `/campaigns` en `/collectes`), puis DM0-COQ (coquille à deux produits) ; DM0-DEMO (faux serveur MSW, jeu factice à graine fixe, contrat d'Envoi, CI de démo) en même temps.
5. DM0 **pré-crée toutes les routes, les barres d'onglets, les registres (handlers, Ctrl K)** : les lots d'écrans ne touchent plus aucun fichier partagé.
6. **Vague 1 : 12 lots en parallèle** (6 CRM Pro, 6 Envoi), aucun fichier en commun (tableau § 4).
7. **Vague 2 : 3 lots** (Presse et Réseaux, Base et collectes, Technique), au fil des places libres. **Vague 3 : DM3** (démo réunie, parcours guidés, passe finale, recette des 7 tâches et 10 parcours).
8. **Démo publique prête ≈ semaine 7 (≈ 18 décembre 2026)**, mise en ligne seulement sur feu vert de Will (GitHub Pages du dépôt public, gratuit).
9. **En parallèle, sans écran** (décision Q6) : R0 (filet de non-régression) puis S1, S2, S6, S9, puis S3, S5, S7 : 8 lots serveur avec leur texte.
10. La cloche se remplit dans S9 (service `Notifier`, routes « lu ») ; en démo, elle se remplit dès DM0.
11. Le mot « campagnes » est libéré **avant tout** (DM0-COL) : les campagnes d'e-mails prennent `/envoi/campagnes`.
12. **Risque n° 1 : chaque fusion sur `main` déploie le CRM réel** ; tout ce qui est neuf reste invisible tant qu'Envoi est « absent », et la fusion reste un geste humain.
13. **Will** : protection de `main`, fusions des lots serveur, description privée de S5, 2 tests de la démo, feu vert de publication, et **tous les achats** (domaines, serveur, port 25, vérificateur, boîtes) : **jamais payés sans son feu vert explicite**.
14. Les achats qui ont un délai incompressible (âge des domaines 21 j, port 25 5 à 7 semaines) doivent partir **semaine 1** pour que le premier envoi réel reste vers la semaine 18.
15. Après la démo : chaîne serveur (P1-P5, F0, B1, E1-E8, A0, A1, C1-C3, RP1-RP3, J1, J3) et branchement BR écran par écran : lots à rédiger au lot W1.

---

## 1. Les lots de la démo (19) et les lots serveur sans écran (8)

Taille en j-agent (± 30 %). Modèle : **Sonnet** code, **Opus** conçoit ou relit (jamais Haiku). Chaque PR est relue par une routine Opus (`plan/lots/RELECTURE.md`).

### 1.1 Démo

| Lot | Vague | Objectif | Maquettes | j | Modèle | Dépend de | Branche | Titre de PR |
|---|---|---|---|---|---|---|---|---|
| **DM0-COL** | 0a | Renommer `/campaigns` (collectes) en `/collectes`, dossier et API (alias gardés) | collectes, collecte-nouvelle, collecte | 0,5 | Sonnet | — | `feat/dm0-col-collectes` | `refactor(collectes) : /campaigns devient /collectes, avec redirections (DM0-COL)` |
| **DM0-DEMO** | 0b | Mode démo, MSW navigateur, base en mémoire, graine, horloge, jeu factice, contrat OpenAPI d'Envoi par zone, handlers du socle, CI de démo | toutes (données) | 9 | **Opus** | — | `feat/dm0-demo-socle` | `feat(demo) : mode démo, faux serveur MSW, jeu factice à graine fixe, contrat Envoi (DM0-DEMO)` |
| **DM0-COQ** | 0c | Jetons d'identité, sélecteur de produit, navigation d'Envoi (10 entrées), toutes les routes en attente, barres d'onglets, droits par produit, cloche, Ctrl K, « Tout arrêter » | index, campagnes, plan-des-pages | 4 | **Opus** | DM0-COL | `feat/dm0-coquille-deux-produits` | `feat(socle) : coquille à deux produits, sélecteur, navigation Envoi et droits par produit (DM0-COQ)` |
| **DM1-ACC** | 1 | Tableau de bord, Mes tâches, Affaires, carte « Envoi aujourd'hui » | index, taches, affaires | 4 | Sonnet | DM0-* | `feat/dm1-acc-accueil` | `feat(crm) : démo du tableau de bord, Mes tâches et Affaires (DM1-ACC)` |
| **DM1-ENT** | 1 | Entreprises, fiche, export, vues sauvegardées | entreprises, entreprise | 3 | Sonnet | DM0-* | `feat/dm1-ent-entreprises` | `feat(crm) : démo des entreprises, export et vues sauvegardées (DM1-ENT)` |
| **DM1-CON** | 1 | Contacts, fiche, ajout rapide, import, modifier/retirer (corbeille) | contacts, contact | 4 | Sonnet | DM0-* | `feat/dm1-con-contacts` | `feat(crm) : démo des contacts, import et corbeille (DM1-CON)` |
| **DM1-ATR** | 1 | À traiter : doublons, personnes à rattacher, propositions, pastille | doublons, personnes-a-rattacher, propositions | 2 | Sonnet | DM0-* | `feat/dm1-atr-a-traiter` | `feat(crm) : démo de la section À traiter (DM1-ATR)` |
| **DM1-CIB** | 1 | Audiences (éditeur ET/OU/SAUF), listes, étiquettes, « Campagne vers cette étiquette » | audiences, audience-nouvelle, audience, listes, liste, etiquettes | 3 | Sonnet | DM0-* | `feat/dm1-cib-ciblage` | `feat(crm) : démo du ciblage, éditeur ET/OU/SAUF et campagne vers une étiquette (DM1-CIB)` |
| **DM1-COM** | 1 | Écrans communs : connexion + code e-mail, compte, utilisateurs (accès par produit), paramètres, RGPD, journal, introuvable | connexion, compte, parametres, utilisateurs, rgpd, journal, introuvable | 3,5 | Sonnet | DM0-* | `feat/dm1-com-ecrans-communs` | `feat(socle) : démo des écrans communs, connexion par code e-mail et accès par produit (DM1-COM)` |
| **DM2-CAM** | 1 | Liste des campagnes (pause, changer la date, dupliquer, terminer), calendrier, suivi, état par destinataire | campagnes, calendrier-envois, campagne-suivi | 6 | Sonnet | DM0-* | `feat/dm2-cam-campagnes` | `feat(envoi) : démo de la liste, du calendrier et du suivi des campagnes (DM2-CAM)` |
| **DM2-ASS** | 1 | Nouvelle campagne en 5 étapes (cible par étiquette, A/B, demain 9 h, 7 contrôles, code), messages types, éditeur | campagne-nouvelle, messages-types, message-editeur | 7 | Sonnet | DM0-* | `feat/dm2-ass-assistant` | `feat(envoi) : démo de la création de campagne en 5 étapes et des messages types (DM2-ASS)` |
| **DM2-PIL** | 1 | Résultats, santé des envois, chercher un envoi, feu vert | resultats, sante, chercher-envoi, feu-vert | 5 | Sonnet | DM0-* | `feat/dm2-pil-pilotage` | `feat(envoi) : démo des résultats, de la santé des envois et de la recherche d'un envoi (DM2-PIL)` |
| **DM2-REP** | 1 | Réponses (traiter, répondre depuis l'outil), à rattacher, traitées | reponses, reponses-a-rattacher | 5 | Sonnet | DM0-* | `feat/dm2-rep-reponses` | `feat(envoi) : démo de la boîte des réponses et des réponses à rattacher (DM2-REP)` |
| **DM2-INF** | 1 | Boîtes et fiche, domaines et fiche 30 jours, serveurs et IP, configuration, chauffe | boites, boite, domaines, domaine, serveurs, configuration, chauffe | 6 | Sonnet | DM0-* | `feat/dm2-inf-infrastructure` | `feat(envoi) : démo des boîtes, domaines, serveurs, configuration et chauffe (DM2-INF)` |
| **DM2-CNF** | 1 | Désinscriptions, alertes d'envoi, réglages d'envoi (5 pages), connexion au CRM, destinataires, page publique | desinscriptions, alertes, reglages-envoi, identite, reglages-alertes, regles-prudence, desinscription-publique | 4 | Sonnet | DM0-* | `feat/dm2-cnf-conformite-reglages` | `feat(envoi) : démo des désinscriptions, alertes, réglages d'envoi et page publique (DM2-CNF)` |
| **DM1-PRE** | 2 | Presse et réseaux (9 pages reprises) | medias, media, journalistes, journaliste, communiques, federations, federation, evenements, evenement | 2 | Sonnet | DM0-* | `feat/dm1-pre-presse-reseaux` | `feat(crm) : démo de la presse et des réseaux (DM1-PRE)` |
| **DM1-DIV** | 2 | Newsletter et guide, candidats, collectes, carte de France | newsletter-guide, personne-newsletter, candidats, collectes, collecte-nouvelle, collecte, carte-france | 1,5 | Sonnet | DM0-* | `feat/dm1-div-base-et-collectes` | `feat(crm) : démo de la lettre et guide, des candidats, des collectes et de la carte (DM1-DIV)` |
| **DM1-TEC** | 2 | Section Technique (7 pages reprises, carte Sauvegardes) | roumanie, historique-collectes, sante-systeme, moteurs-ia, serveurs-relais, rotation-acces, registre-ia | 1 | Sonnet | DM0-* | `feat/dm1-tec-technique` | `feat(crm) : démo de la section Technique (DM1-TEC)` |
| **DM3** | 3 | Démo réunie : 3 offres, 3 parcours guidés, scénarios vivants, passe finale U10, recette T1-T7 et P1-P10, paquet de publication prêt (non publié) | toutes | 9 | **Opus** + Sonnet | tous les DM | `feat/dm3-demo-reunie` | `feat(demo) : démo réunie, parcours guidés et passe finale (DM3)` |
| **Total démo** | | | | **≈ 79,5** | | | | (+ 1,5 j de maquettes déjà faites = 80,5 j du plan 29) |

### 1.2 Serveur, sans écran (en parallèle de la démo, décision Q6)

| Lot | Vague | Objectif | j | Modèle | Dépend de | Branche | Titre de PR |
|---|---|---|---|---|---|---|---|
| **R0** | S-a | Filet de non-régression (24 gardes, instantanés, job CI) + vérification de l'ancien S8 | 3,5 (reste) | Sonnet + audit Opus | — | `feat/r0-filet-non-regression` | `test(filet) : filet de non-régression bloquant, 24 gardes et instantanés (R0)` |
| **S1** | S-b | Anti-rejeu, limiteur par compte | 0,5 | Sonnet + audit Opus | R0 + protection de `main` | `feat/s1-durcir-authentification` | `fix(auth) : anti-rejeu et limiteur par compte (S1)` |
| **S2** | S-b | Courrier d'authentification isolé, gardes de démarrage | 1 | Sonnet + audit Opus | R0 | `feat/s2-courrier-authentification-isole` | `fix(auth) : courrier d'authentification isolé et démarrage refusé si mal réglé (S2)` |
| **S5** | S-b | Contenu privé (notes de Will) | (privé) | Sonnet + audit Opus | R0 + texte privé collé par Will | `feat/s5-securite` | `fix(securite) : lot S5 (S5)` |
| **S6** | S-b | Segments fermés par défaut et par espace, owner protégé, action de masse | 3 | Sonnet + audit Opus | R0 | `feat/s6-droits-et-segments` | `fix(droits) : segments fermés par défaut par espace, owner protégé (S6)` |
| **S9** | S-b | Alertes console + e-mail, la cloche se remplit, Telegram retiré, battement externe | 5,5 | Sonnet + relecture Opus | R0 ; DM0-COQ pour la cloche | `feat/s9-alertes-console-email` | `feat(alertes) : alertes console + e-mail, la cloche se remplit, Telegram retiré (S9)` |
| **S3** | S-c | 2FA par code e-mail (serveur), appareils de confiance, code redemandé | 5 | Sonnet + audit Opus | S1, S2 | `feat/s3-2fa-code-email` | `feat(auth) : 2FA par code e-mail, appareils de confiance et code redemandé (S3)` |
| **S7** | S-c | Isolation RLS armée par défaut, suite à deux espaces factices | 12,5 | Sonnet + **audit Opus obligatoire** | R0, S6 | `feat/s7-isolation-rls` | `fix(isolation) : RLS armée par défaut et suite à deux espaces factices (S7)` |

Tous dans le dépôt `will383842/axion-crm-pro`, une PR par lot, textes complets dans `plan/lots/`.

---

## 2. Vagues et calendrier

**S1 = semaine du lundi 2 novembre 2026** (Will a ordonné l'autopilote ; si le lancement glisse, tout glisse d'autant). Une « semaine » de routine ≈ 5 j-agent par routine.

| Semaine | Démo (écrans) | Serveur sans écran | Will |
|---|---|---|---|
| **S1** (2-6 nov.) | **Vague 0** : DM0-COL (lundi), DM0-DEMO (lundi → vendredi), DM0-COQ (dès COL fusionné) | **R0** | protection de `main` ; lancer les routines ; **achats à délai** (domaines, serveur, port 25) **après son feu vert** ; CNIL ; mot de passe et clés |
| **S2** (9-13 nov.) | **Vague 1** dès DM0 fusionné (≈ 10 nov.) : 12 lots | S1, S2, S6, S9 (et S5 si texte privé collé) | fusions des lots serveur |
| **S3** (16-20 nov.) | vague 1 (suite) ; **vague 2** au fil des places (DM1-ATR et DM1-ENT finissent les premiers) | S3, S7 | — |
| **S4** (23-27 nov.) | fin de la vague 1 (DM2-ASS, 7 j, est le plus long) et de la vague 2 | S7 (suite) | — |
| **S5** (30 nov.-4 déc.) | **Vague 3 : DM3** (tous les DM fusionnés) | S7 (fin, allumage en préproduction seulement) | — |
| **S6** (7-11 déc.) | DM3 : recette, **test 1 de 45 min avec Will**, corrections | — | test 1 |
| **S7** (14-18 déc.) | test 2 (15 min) ; **démo prête ≈ 18 déc.** | début de la chaîne serveur (lot W1) | **feu vert de publication** (ou non) |

- **Plafond de routines** : les lots permettent **12** routines d'écrans en même temps. La décision 12 de Will fixait « jusqu'à 8 » routines. Avec 8 : lancer d'abord les 8 plus longs (DM2-ASS, DM2-CAM, DM2-INF, DM2-PIL, DM2-REP, DM1-CON, DM1-ACC, DM2-CNF), puis DM1-COM, DM1-CIB, DM1-ENT, DM1-ATR, puis la vague 2 ; les lots serveur prennent les places restantes. Effet : démo ≈ 1 semaine plus tard (≈ 23-24 déc.). **Recommandation : 12 routines d'écrans + 2 serveur pendant S2-S4.**
- **Chemin critique** : DM0-DEMO (9 j, Opus) → DM2-ASS (7 j) → DM3 (9 j). Si DM0-DEMO glisse, tout glisse ; c'est pourquoi DM0-COQ et DM0-COL sont séparés de lui.
- **Après la démo** (plan 29 § 7.4) : P1-P5, F0, B1, E1 → E8, A0, A1, C1 → C3, RP1 → RP3, J1, J3, avec **BR** (branchement « démo → réel » groupe par groupe). Premier envoi interne ≈ S17, réel limité ≈ S18 (mi-mars 2027), **si** les domaines et le port 25 partent en S1.

---

## 3. Ce qui avance en parallèle sans écran

| Travail | Qui | Quand | Pourquoi maintenant |
|---|---|---|---|
| R0, S1-S3, S5-S7, S9 | routines (textes `plan/lots/`) | S1-S5 | aucun écran, réduit le risque sur l'existant (décision Q6) |
| Achat et **âge des domaines** d'envoi (21 jours au moins) | Will | S1 | délai incompressible |
| **Demande de port 25** chez l'hébergeur | Will | S1 | 5 à 7 semaines ; repli : relais tiers temporaire (F20) |
| Notification **CNIL** (brouillon prêt, `plan/25`) | Will | S1 | délai administratif |
| Rotation des clés, mot de passe exposé | Will | S1 | sécurité |
| Vérités du plan 28 § 6 sur le serveur réel (lecture seule) | Will ou session autorisée | S1-S2 | dimensionne P1, S6, S7, E4 |

**Ce qui n'avance pas pendant la démo** (décision Q6) : tout lot qui crée un écran hors démo ; la chaîne d'envoi (E1 et suivants) ; aucune campagne réelle.

---

## 4. Qui possède quoi (pour que deux lots ne touchent jamais le même fichier)

### 4.1 Fichiers partagés

| Fichier ou dossier | Propriétaire (dans l'ordre) | Les autres lots |
|---|---|---|
| `frontend/src/app/routeTree.tsx` | DM0-COL, puis DM0-COQ | **jamais** (toutes les routes sont pré-créées) ; DM3 seulement pour une correction |
| `frontend/src/components/layout/Sidebar.tsx` | DM0-COL (1 ligne), puis DM0-COQ | jamais |
| `Header.tsx`, `RootLayout.tsx`, `AutoBreadcrumbs.tsx`, `UserMenu.tsx`, `components/ui/*`, `styles/index.css` | DM0-COQ | jamais ; DM3 pour la passe finale |
| `NotificationsBell.tsx`, `tests/components/cloche-notifications.test.tsx` | DM0-COQ, puis S9 (bouton « Tout marquer comme lu », garde inversée) | jamais |
| `features/crm-console/useConsoleFeatures.ts` | DM0-COQ | jamais |
| `features/crm-console/types.ts`, `ConsoleGate.tsx` | **gelés** pendant la démo | chaque lot met ses types dans ses fichiers |
| Barres d'onglets (`OngletsTableauDeBord`, `OngletsCampagnes`, `OngletsSante`, `OngletsServeurs`, `OngletsReponses`, `OngletsReglages`) | DM0-COQ | jamais |
| `frontend/src/main.tsx`, `vite.config.ts`, `package.json`, lockfile, `public/mockServiceWorker.js`, `.env.demo` | DM0-DEMO | jamais |
| `frontend/src/demo/` (base, graine, horloge, outils, offres, scénarios, bandeau, `handlers/index.ts`, `handlers/socle/*` sauf `ecrans-communs`) | DM0-DEMO, puis DM3 (scénarios, bandeau, offres) | **chaque lot a son fichier** `handlers/<produit>/<zone>.handlers.ts` et `donnees/<produit>/<zone>.ts` |
| `backend/openapi/envoi/commun.yaml`, `socle.yaml` | DM0-DEMO | lecture seule ; besoin noté dans la PR |
| `backend/openapi/envoi/<zone>.yaml` + `features/envoi/api/<zone>.d.ts` | DM0-DEMO (création), puis le lot de la zone | — |
| `frontend/tests/msw/handlers.ts` | DM0-COQ | jamais |
| `frontend/tests/couverture-e2e.test.ts`, `.github/workflows/demo.yml` | DM0-DEMO | jamais (les suites de `tests/e2e/demo/` sont jouées d'office) |
| `tests/components/navigation-cible.test.tsx` | DM0-COL, puis DM0-COQ | jamais |
| `.github/workflows/ci.yml` | R0 | jamais |
| `.github/workflows/e2e.yml` | DM0-COL (nom de suite) | jamais |
| `.github/workflows/deploy-direct-ssh.yml` | S9 (retrait de l'étape Telegram) | jamais |
| `backend/routes/api.php` | DM0-COL (groupe collectes), S1 (authentification), S3 (2FA), S9 (notifications) | lignes de son groupe seulement ; S1 → S3 en série ; rebase avant de pousser |
| `backend/config/crm.php` | S6 (segments), puis S3 (2FA), puis S7 (RLS) | en série, clés de son lot seulement |

### 4.2 Routes et fichiers de page (créés « en attente » par DM0-COQ)

| Route | Fichier de page (`frontend/src/features/…`) | Lot qui la remplit |
|---|---|---|
| `/taches` (onglet du tableau de bord) | `crm/taches/MesTachesPage.tsx` | DM1-ACC |
| `/affaires` (onglet du tableau de bord) | `crm/affaires/AffairesPage.tsx` | DM1-ACC |
| `/compte` | `settings/ComptePage.tsx` | DM1-COM |
| `/collectes`, `/collectes/new`, `/collectes/$collecteId` | `collectes/*` (renommés par DM0-COL) | DM1-DIV |
| `/envoi` | redirection vers `/envoi/campagnes` | DM0-COQ |
| `/envoi/campagnes` | `envoi/campagnes/CampagnesPage.tsx` | DM2-CAM |
| `/envoi/campagnes/calendrier` | `envoi/campagnes/CalendrierEnvoisPage.tsx` | DM2-CAM |
| `/envoi/campagnes/$campagneId` | `envoi/campagnes/CampagneSuiviPage.tsx` | DM2-CAM |
| `/envoi/campagnes/nouvelle` | `envoi/campagnes/NouvelleCampagnePage.tsx` | DM2-ASS |
| `/envoi/campagnes/messages` | `envoi/messages/MessagesTypesPage.tsx` | DM2-ASS |
| `/envoi/campagnes/messages/$messageId` | `envoi/messages/MessageEditeurPage.tsx` | DM2-ASS |
| `/envoi/campagnes/resultats` | `envoi/pilotage/ResultatsPage.tsx` | DM2-PIL |
| `/envoi/campagnes/destinataires` (offre « Envoi seul ») | `envoi/conformite/DestinatairesPage.tsx` | DM2-CNF |
| `/envoi/reponses`, `/a-rattacher`, `/traitees` | `envoi/reponses/ReponsesPage.tsx`, `ReponsesARattacherPage.tsx`, `ReponsesTraiteesPage.tsx` | DM2-REP |
| `/envoi/boites`, `/envoi/boites/$boiteId` | `envoi/infrastructure/BoitesPage.tsx`, `BoitePage.tsx` | DM2-INF |
| `/envoi/domaines`, `/envoi/domaines/$domaineId` | `envoi/infrastructure/DomainesPage.tsx`, `DomainePage.tsx` | DM2-INF |
| `/envoi/serveurs`, `/envoi/serveurs/configuration` | `envoi/infrastructure/ServeursPage.tsx`, `ConfigurationPage.tsx` | DM2-INF |
| `/envoi/chauffe` | `envoi/infrastructure/ChauffePage.tsx` | DM2-INF |
| `/envoi/sante`, `/envoi/sante/chercher`, `/envoi/sante/feu-vert` | `envoi/pilotage/SantePage.tsx`, `ChercherEnvoiPage.tsx`, `FeuVertPage.tsx` | DM2-PIL |
| `/envoi/desinscriptions` | `envoi/conformite/DesinscriptionsPage.tsx` | DM2-CNF |
| `/envoi/alertes` | `envoi/conformite/AlertesEnvoiPage.tsx` | DM2-CNF |
| `/envoi/reglages` (+ `/identite`, `/alertes`, `/regles`, `/connexion-crm`) | `envoi/reglages/ReglagesEnvoiPage.tsx`, `IdentitePage.tsx`, `ReglagesAlertesPage.tsx`, `ReglesPrudencePage.tsx`, `ConnexionCrmPage.tsx` | DM2-CNF |
| `/desinscription/$jeton` (hors coquille, publique) | `envoi/public/DesinscriptionPubliquePage.tsx` | DM2-CNF |

Toutes les routes `/envoi/…` portent la garde `exigerProduit('envoi')` : sans Envoi, elles répondent « introuvable » (c'est le cas en production tant que la console n'a pas posé `produit_envoi`).

### 4.3 Le socle DM0 en une page (ce que les autres lots utilisent)

- **Mode démo** : `pnpm dev:demo` / `pnpm build:demo` ; MSW dans le navigateur, chargé seulement en mode démo ; bandeau « Démonstration : données fictives », « Voir comme » (3 offres), « Remettre la démo à zéro », code de connexion de démo affiché.
- **Données** : `demoDb` (`src/demo/base.ts`), graine fixe `20270112`, aujourd'hui fixe = mardi 12 janvier 2027 09:30 ; mêmes personnages que les maquettes ; `demoDb.etendre(zone, fabrique)` pour compléter.
- **Handlers** : un fichier par zone, chargé tout seul ; les mêmes servent aux tests Vitest et aux e2e de démo ; `?demo-etat=vide|erreur|chargement` montre les 4 états.
- **Contrat d'Envoi** : OpenAPI 3.1 par zone, types générés par zone (`pnpm api:envoi`), garde « à jour » en CI ; ce contrat servira au vrai serveur (branchement BR sans réécrire les écrans).
- **Coquille** : `data-produit`, jetons `*-produit`, `useProduits()`, `useAccesProduit()`, `exigerProduit()`, sélecteur, 10 entrées d'Envoi, `PageHeader surTitre`, bouton plein couleur du produit, cloche avec pastille de produit, Ctrl K par `commandes.ts`, « Tout arrêter » dans Envoi.
- **CI** : `demo.yml` (build de démo, garde « aucune URL réelle », e2e Chromium + axe + 360 px), sans clé, machines gratuites.

---

## 5. Risques

| # | Risque | Effet | Parade |
|---|---|---|---|
| 1 | **Chaque fusion sur `main` déploie le CRM réel** (`deploy-direct-ssh.yml`, `deploy-staging.yml`) | un lot de démo pourrait changer l'écran de Will en production | tout ce qui est neuf est caché tant qu'`envoi` est « absent » (valeur par défaut) ; test « menu identique à aujourd'hui » dans DM0-COQ ; la démo est absente du build normal (test) ; fusion humaine, jamais par la routine |
| 2 | Le bouton principal du CRM passe de l'ardoise à la couleur du produit (bleu `#0051bd`) | changement visible en production dès DM0-COQ | écart validé dans les maquettes M2 (« PARFAIT ») ; à signaler à Will dans la PR ; retour arrière = 1 jeton |
| 3 | DM0 sous-spécifié ou en retard | les 16 lots suivants attendent ou divergent | DM0 en 3 lots, Opus, contrat écrit dans chaque texte de lot, 2e relecture Opus ; vague 1 ne part qu'après les 3 fusions |
| 4 | La démo diverge du futur serveur | branchement long | contrat OpenAPI par zone dès DM0, types générés, mêmes handlers en test et en démo ; BR chiffré à 8 j |
| 5 | Conflits sur les quelques fichiers serveur partagés (`routes/api.php`, `config/crm.php`) | rebase pénible | lots en série (S1 → S3 ; S6 → S3 → S7), lignes de leur groupe seulement |
| 6 | Plafond de routines (8) | démo + 1 semaine | ordre de lancement donné au § 2 ; Will peut relever le plafond |
| 7 | CI longue ou rouge sur l'existant (suites e2e exclues, `auth.spec`) | faux rouges | R0 étape 0 mesure l'état de `main` avant tout ; job de démo séparé, < 15 min, machines gratuites |
| 8 | Une donnée factice ressemble à du réel | problème RGPD ou d'image | gardes : `@example.test`, `.example`, IP de documentation, SIREN invalides, garde données personnelles, mots interdits |
| 9 | Le menu d'Envoi des maquettes (10 entrées) contredit l'ADR-14 (4 entrées) | hésitation des routines | **les maquettes validées font foi** (plan 20 § 12.1) ; écrit dans DM0-COQ |
| 10 | S5 bloqué faute de texte privé | trou dans la sécurité | la routine s'arrête proprement et le signale ; Will colle le texte |
| 11 | « Tout arrêter » seulement dans Envoi | geste de sécurité moins visible depuis le CRM | point ouvert du test de Will ; constante prête pour l'afficher aussi dans le CRM |
| 12 | Délais incompressibles (domaines, port 25) | premier envoi réel repoussé | achats en S1 (sur feu vert) ; repli relais tiers F20 |
| 13 | Total plus haut que « 638 j » | surprise | écart expliqué (48 j du plan 27 non reportés) ; démo inchangée |

---

## 6. Ce qui exige Will (rien n'est payé sans son feu vert explicite)

**Gestes gratuits (GitHub, dépôt public)**
1. Poser la **protection de `main`** : contrôles obligatoires `filet-non-regression`, `backend`, `frontend`, `Suites e2e`, job de démo (10 min, gratuit) : après R0.
2. **Lancer les routines** (copier les textes de `plan/lots/`) et, si possible, relever le plafond à 12 + 2.
3. **Fusionner** les lots serveur (R0, S1-S9) ; dire qui fusionne les lots de démo sur verdict de relecture (décision 11 B : délégation à la routine Opus possible).
4. **Coller la description privée de S5** dans son texte de routine.
5. **Allumer l'isolation stricte (S7) en production**, après relecture.

**Démo**
6. **Test de 45 min** puis **second passage de 15 min** (7 tâches, `maquettes/LISEZ-MOI.md`), validation écrite.
7. **Feu vert de publication** de la démo (GitHub Pages du dépôt public : gratuit) ; une adresse de démo à soi demanderait un nom de domaine = **achat**.
8. Trancher les points ouverts du test : « Tout arrêter » aussi dans le CRM ? confirmer les 3 écarts par défaut (pas d'ouvertures, pas de faux échanges de chauffe, pas de BIMI).

**Achats et comptes (JAMAIS payés sans feu vert explicite ; budget annoncé avant : serveur 30 à 80 €/mois en V0, plus domaines, vérificateur, éventuelle licence de listes noires)**
9. **Domaines d'envoi** (2 au départ, un 3e avant le 15 mars) : au nom de la **SAS française** ; âge de 21 jours avant tout envoi.
10. **Serveur d'envoi Hetzner** (un seul au début, décision 9) et **demande de port 25** (5 à 7 semaines).
11. **Hébergeur des boîtes** (une boîte par domaine, au nom de Will, décision 7) : choix H3.
12. **Vérificateur d'adresses** : choix H4 (bloque E4 puis C1).
13. **Relais tiers de secours** (F20) si le port 25 tarde.
14. Comptes de suivi au premier envoi : Google Postmaster Tools, Microsoft SNDS et JMRP, Signal Spam (gratuits, mais à son nom).

**Juridique et sécurité**
15. **Notification CNIL** (brouillon prêt, `plan/25`) ; point juridique en retard ; identité légale de la SAS pour le bloc art. 14 et les CGV par produit (J4).
16. **Changer le mot de passe exposé**, **rotation des clés**.
17. Lire (ou faire lire par une session autorisée) les **10 vérités du plan 28 § 6** sur le serveur réel, en lecture seule.
18. Choisir la **date de lancement** : toutes les dates de ce fichier en dépendent.

---

## 7. Comment lancer

1. Lancer **DM0-COL**, **DM0-DEMO** et **R0** tout de suite ; **DM0-COQ** dès que DM0-COL est fusionné.
2. Pour chaque PR verte : lancer `plan/lots/RELECTURE.md` (Opus) avec le numéro de PR ; fusionner sur « PRÊTE À FUSIONNER ».
3. DM0 fusionné en entier → lancer les 12 lots de la vague 1 ; chaque fin de lot libère une place pour la vague 2.
4. Après la protection de `main` → S1, S2, S6, S9 (et S5 avec son texte) ; puis S3 et S7.
5. Tous les DM fusionnés → **DM3** ; puis tests avec Will.

## Limites

- Rien n'a été exécuté dans `axion-crm-pro` (lecture seule) ; les chemins de fichiers viennent d'une lecture du dépôt au 01/11 (fusion #388). Un fichier cité « à créer » peut demander un nom voisin : la routine le dit dans sa PR.
- Les tailles restent à ± 30 % ; le partage des lots « à découper » entre familles (§ 12.3 du plan 20) est une estimation.
- La chaîne serveur après la démo (P1 → T1, BR) n'est pas encore écrite en textes de routine : c'est le lot W1.
- Les textes de S5 et J2 restent privés.
