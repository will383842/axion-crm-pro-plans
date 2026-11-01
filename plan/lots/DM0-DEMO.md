# Routine DM0-DEMO : Socle de démo : faux serveur MSW, jeu factice à graine fixe, contrat d'API d'Envoi, CI de démo

> Texte autonome, prêt à copier dans une routine cloud. Dépôt de code : `will383842/axion-crm-pro` (écriture **seulement** sur la branche du lot, par PR). Dépôt des plans : `will383842/axion-crm-pro-plans` (**lecture seule** pour cette routine).

## Contexte

Axion-IA construit deux produits facturés à part : **CRM Pro** (le CRM existant, bleu de marque `#0051bd`) et **Envoi** (envoi d'e-mails en masse : campagnes, chauffe, domaines, serveurs, boîtes, réponses, désinscriptions ; turquoise pétrole `#0b7285` ; n'existe pas encore). Envoi se branchera sur plusieurs CRM par un adaptateur ; le CRM Pro est le premier. Entité d'envoi : SAS française. Décisions de Will : `plan/29-ADR-DEUX-PRODUITS.md` (6 OUI), `plan/20` § 12, `plan/30`. **Ordre voulu : le frontend d'abord, en démo présentable à des clients (données factices, faux serveur dans le navigateur), puis le serveur, puis le branchement.** Maquettes validées par Will (« PARFAIT ») : `maquettes/*.html` du dépôt des plans (ouvrez-les dans un navigateur ; le cadre violet « Maquette » n'est pas dans le produit). Guide : `maquettes/GUIDE-STYLE.md`. Par défaut : pas de mesure des ouvertures, pas de faux échanges de chauffe, pas de BIMI.

## Objectif du lot

Construire le **mode démo** de l'ADR-15 (plan 29 § 15.1 et 15.2) : le **vrai** frontend du CRM, branché sur un **faux serveur dans le navigateur** (MSW, déjà dans les dépendances de test), avec un **jeu factice réaliste à graine fixe** pour les deux produits, et le **contrat d'API d'Envoi** (OpenAPI) dont les écrans d'Envoi tireront leurs types. Ce lot fixe tout ce que les lots suivants **utilisent sans le modifier** : il doit être décrit au point qu'un lot d'écran n'ait qu'à écrire ses handlers et ses pages (voir le « Contrat du socle de démo » ci-dessous, que vous **réalisez**).

À livrer :
1. **Démarrage** : `src/demo/demarrer.ts` démarre `setupWorker` de `msw/browser` **seulement** si `import.meta.env.VITE_DEMO === '1'`, par import dynamique (le build normal ne contient aucun octet de démo : test qui le vérifie dans `dist/`). `frontend/public/mockServiceWorker.js` (généré par `msw init`). `src/main.tsx` attend le démarrage avant de monter l'application et monte `BandeauDemo` au-dessus de tout (y compris les écrans de connexion).
2. **Scripts** (`frontend/package.json`) : `dev:demo`, `build:demo` (`tsc --noEmit && vite build --mode demo --outDir dist-demo`), `api:envoi` (génère les types). `frontend/.env.demo` : `VITE_DEMO=1`, `VITE_API_BASE_URL=https://demo.invalid`, `VITE_ECHO_DISABLED=true` (aucun secret). **Seule dépendance ajoutée permise** : `openapi-typescript` en devDependency (version exacte, publiée depuis plus de 2 semaines) ; MSW est déjà là.
3. **Garde de construction** (`vite.config.ts`, mode `demo`) : refuse de construire si `VITE_API_BASE_URL` n'est pas `https://demo.invalid`, si une variable `VITE_SENTRY_DSN` ou `VITE_REVERB_*` est réglée, ou si `VITE_BUILD_CIBLE=prod`. Page non indexée (`<meta name="robots" content="noindex">` en mode démo).
4. **Base en mémoire** `src/demo/base.ts` : `demoDb` (collections typées, identifiants stables, `reinitialiser()`, `etendre(zone, fabrique)`, persistance de session dans `sessionStorage` pour qu'un rechargement garde les gestes, effacée par « Remettre la démo à zéro »).
5. **Graine et horloge** : `src/demo/graine.ts` (générateur pseudo-aléatoire maison, type mulberry32, graine `20270112`, `graine(zone)` dérivée par zone), `src/demo/horloge.ts` (`maintenant()` = mardi 12 janvier 2027 09:30 Europe/Paris ; 30 jours d'historique avant).
6. **Jeu factice** (`src/demo/donnees/`) : listes de prénoms, noms, villes, raisons sociales **inventées** (`noms-fictifs.ts`) ; ≈ 300 entreprises, 900 contacts, médias, journalistes, fédérations, événements, audiences, listes, étiquettes, utilisateurs, 1 espace « Axion (démo) » ; **Envoi** : 12 campagnes (tous statuts), 4 domaines `.example`, 8 boîtes, 2 serveurs (adresses de documentation seulement), 60 réponses, 30 jours d'événements d'envoi (remis, rebonds durs et mous avec code serveur traduit en français, plaintes, désinscriptions ; **aucune ouverture, aucun clic**), messages types versionnés, règles d'alerte, désinscriptions, registre d'opposition. Reprendre **les mêmes repères que les maquettes** (Paul Morin, Yves Roche, Boulangerie des Tilleuls, Le Courrier du Rhône, Léa Fournier, Fédération BTP Rhône, Salon des artisans de Vienne, étiquette `salon-artisans-2026`, campagne « Organisateurs Rhône-Alpes », `prospection-a.example`, `will@prospection-b.example`) : lisez `maquettes/_fabrique/pages_*.py` du dépôt des plans. Pour le CRM, reprenez **les formes JSON réelles** attendues par les écrans existants (types dans `frontend/src/features/*/types.ts` et fixtures des tests `frontend/tests/**`).
7. **Contrat d'Envoi** : `backend/openapi/envoi/commun.yaml` (schémas partagés : Pagination, Erreur, CampagneResume, BoiteResume, DomaineResume, Destinataire, EvenementEnvoi, EtatFeu…), et une description **par zone**, chacune document OpenAPI 3.1 complet qui référence `commun.yaml` : `socle.yaml` (`/config/features` avec `produits`, `/notifications` avec `produit` et `lien`, `/envoi/etat`, `/envoi/tout-arreter`, `/envoi/reprendre`, `/envoi/compteurs`), `campagnes.yaml` (liste, filtres par statut, fiche, pause, reprise, terminer, dupliquer, changer la date, destinataires et état par destinataire, calendrier), `creation.yaml` (brouillon, 5 étapes, cible par liste/audience/**étiquette**, exclusions, séquence 1-4, A/B d'objet, programmation, 7 contrôles, validation par code e-mail, annulation 5 min, messages types, versions, aperçu, « m'envoyer un test »), `pilotage.yaml` (résultats par campagne/boîte/domaine/liste/message, santé, chercher un envoi, feu vert), `reponses.yaml` (file, classement, suggestion, rattacher, répondre dans le même fil, raccourcis), `infrastructure.yaml` (boîtes, fiche boîte, domaines, fiche domaine 30 jours, DNS, DMARC progressif, serveurs, adresses IP « ajouter et appliquer », configuration versionnée, chauffe, listes noires), `conformite.yaml` (désinscriptions, « Puis-je écrire à… ? », export du registre, alertes d'envoi, réglages d'envoi, identité, règles et horaires, connexion au CRM, carnet de destinataires, page publique de désinscription). Types générés : `frontend/src/features/envoi/api/<zone>.d.ts`. Garde CI : fichiers générés à jour.
8. **Handlers du socle** (`src/demo/handlers/socle/*.handlers.ts`) : CSRF, `/auth/me`, connexion + **code e-mail de démo affiché dans le bandeau** (aucun compte réel), `/config/features` selon l'offre « Voir comme », `/notifications` (6 alertes des deux produits, comme la cloche des maquettes), état des envois, « Tout arrêter » / « Reprendre », compteurs d'Envoi. **Les handlers des écrans ne sont pas dans ce lot** (un par lot d'écran).
9. **Outils** `src/demo/outils.ts` : `api()`, `paginer()`, `filtrerTexte()`, `delai()`, `etatForce()` (`?demo-etat=vide|erreur|chargement`). `src/demo/offres.ts` (« les deux », « CRM seul », « Envoi seul »). `src/demo/scenarios.ts` : moteur de scénarios rejoués (une réponse « intéressée » arrive 30 s après l'ouverture, un domaine passe ambre) ; scénarios désactivables (`?demo-scenarios=non`, utilisé par les e2e).
10. **Agrégateur** `src/demo/handlers/index.ts` : charge tout seul `./**/*.handlers.ts` (`import.meta.glob`, eager) ; un fichier de handlers sans export `handlers` fait échouer un test.
11. **CI de démo** `.github/workflows/demo.yml` (pull_request vers main et push main ; `ubuntu-24.04` ; `timeout-minutes: 20` ; aucune clé) : install figée, `pnpm build:demo`, garde « aucune URL réelle dans `dist-demo` » (grep des domaines du projet et d'`api.` hors `demo.invalid`), `playwright test --config playwright.demo.config.ts` (Chromium, `vite preview` de `dist-demo`, dossier `tests/e2e/demo/`), dépôt de `dist-demo` en artefact (rétention 7 jours). `infra/scripts/garde-donnees-personnelles.sh` passe sur `frontend/src/demo/`.
12. **Garde de couverture e2e** (`frontend/tests/couverture-e2e.test.ts`) : accepter qu'un workflow cite un **dossier** (`tests/e2e/demo/`) ; toutes ses suites comptent alors comme jouées ; ajouter le cas témoin. `frontend/playwright.demo.config.ts` et `tests/e2e/demo/outils.ts` (`ouvrirDemo(page, chemin, { offre, etat })`, contrôle axe, passage à 360 px).

## Fiche du lot

| | |
|---|---|
| Identifiant | **DM0-DEMO** |
| Vague | 0b |
| Dépend de | aucune ; peut tourner en même temps que DM0-COL et DM0-COQ (fichiers disjoints) |
| Taille | 9 j-agent |
| Modèle | **Opus** (conçoit et code : c'est le socle dont dépendent 16 lots) ; relecture par une 2e routine Opus |
| Branche | `feat/dm0-demo-socle` |
| Titre de la PR | `feat(demo) : mode démo, faux serveur MSW, jeu factice à graine fixe, contrat Envoi (DM0-DEMO)` |
| Maquettes | toutes (les données factices doivent reproduire celles des maquettes : `maquettes/_fabrique/*.py` contient les noms, chiffres et textes) |

## Fichiers autorisés (liste fermée : aucun autre fichier)

### Créés

- `frontend/src/demo/**` (demarrer.ts, base.ts, graine.ts, horloge.ts, outils.ts, offres.ts, scenarios.ts, BandeauDemo.tsx, noms-fictifs.ts, donnees/**, handlers/index.ts, handlers/socle/*.handlers.ts)
- `frontend/public/mockServiceWorker.js`
- `frontend/.env.demo`
- `backend/openapi/envoi/*.yaml` (commun, socle, campagnes, creation, pilotage, reponses, infrastructure, conformite)
- `frontend/src/features/envoi/api/*.d.ts` (générés)
- `frontend/scripts/generer-api-envoi.mjs`
- `frontend/playwright.demo.config.ts`
- `frontend/tests/e2e/demo/outils.ts`
- `frontend/tests/e2e/demo/socle-demo.spec.ts`
- `frontend/tests/lib/demo-donnees-factices.test.ts`
- `frontend/tests/lib/demo-handlers-charges.test.ts`
- `frontend/tests/lib/demo-absent-du-build-normal.test.ts`
- `frontend/tests/lib/interdits-communication.test.ts`
- `frontend/tests/lib/contrat-envoi-a-jour.test.ts`
- `.github/workflows/demo.yml`

### Modifiés

- `frontend/package.json` (scripts + 1 devDependency)
- `pnpm-lock.yaml` (ou frontend/pnpm-lock.yaml selon l'emplacement réel)
- `frontend/src/main.tsx`
- `frontend/vite.config.ts` (mode demo et garde)
- `frontend/tests/couverture-e2e.test.ts` (dossier cité)

### Supprimés ou vidés

- (aucun)

Tout autre fichier est **interdit** pour ce lot, notamment ceux que d'autres lots possèdent (tableau « Qui possède quoi » de `plan/30` § 4). Seule exception : un fichier régénéré par une commande du dépôt **pour votre zone** (types d'Envoi). `pnpm-lock.yaml` et `package.json` : **jamais** (sauf DM0-DEMO).

## Interdits propres à ce lot

- Modifier `routeTree.tsx`, `Sidebar.tsx`, `Header.tsx`, `RootLayout.tsx`, `NotificationsBell.tsx`, `src/components/**`, `src/styles/**` (c'est DM0-COQ).
- Écrire des handlers d'écrans métier (c'est le lot de chaque écran).
- Toute donnée qui ressemble à une vraie personne, une vraie entreprise, un vrai domaine ou une vraie IP.
- Mesure des ouvertures ou des clics dans le contrat (règle « aucun pixel »).

## Tests à écrire d'abord (rouges avant le code)

- `demo-donnees-factices.test.ts` : toutes les adresses de `demoDb` finissent par `@example.test` ou un domaine `.example` ; toute IP est dans les plages de documentation ; tout SIREN a une clé de Luhn **fausse** ; aucun nom de la liste des personnes réelles connues du projet ; deux générations avec la même graine sont identiques à l'octet.
- `interdits-communication.test.ts` : aucun des mots interdits (« Grenoble », « Aucun gain garanti », « certifié », « Qualiopi », « agréé », « labellisé », « accrédité ») dans `frontend/src/**` ni dans `backend/openapi/**` (insensible à la casse et aux accents).
- `demo-handlers-charges.test.ts` : chaque `*.handlers.ts` exporte `handlers` ; aucune route n'est déclarée deux fois.
- `demo-absent-du-build-normal.test.ts` : après `pnpm build`, `dist/` ne contient ni `mockServiceWorker`, ni `demoDb`, ni `BandeauDemo`.
- `contrat-envoi-a-jour.test.ts` : régénérer les types ne change rien ; chaque document de zone est un OpenAPI 3.1 valide.
- `socle-demo.spec.ts` : le bandeau est là sur la connexion et dans l'application ; « Voir comme : Envoi seul » cache le CRM ; « Remettre la démo à zéro » restaure les données ; le code de démo est affiché et accepté ; 0 violation axe critique ; 360 px sans défilement horizontal.

## Critères de fin (tous vérifiables)

- `pnpm build` (normal) et `pnpm build:demo` verts ; CI verte, **dont le nouveau job de démo** ; temps du job de démo < 10 min.
- `pnpm dev:demo` ouvre l'écran de connexion, le code de démo connecte, le tableau de bord actuel s'affiche avec des données factices (les écrans pas encore servis peuvent afficher leur état d'erreur : c'est le travail des lots suivants).
- Le « Contrat du socle de démo » (plus bas) est exact : chaque nom de fichier, fonction et commande qu'il cite existe.
- Retour arrière : supprimer `src/demo/`, `.env.demo`, `demo.yml` ; le build normal n'a jamais dépendu de la démo.

## Ce que les lots suivants attendront de vous

Le bloc ci-dessous est copié dans **chacun** des 16 lots d'écrans. Vous le **réalisez** : à la fin, chaque nom qu'il cite doit exister et marcher (DM0-DEMO pour la partie démo, DM0-COQ pour la partie coquille).

## Contrat du socle de démo (livré par DM0-COL, DM0-DEMO et DM0-COQ : à UTILISER, pas à modifier)

**Mode démo.** `pnpm dev:demo` et `pnpm build:demo` (mode Vite `demo`, `VITE_DEMO=1`). Le faux serveur est **MSW dans le navigateur** (`src/demo/demarrer.ts`, importé dynamiquement : absent du build normal). Aucune requête ne sort du navigateur. Bandeau permanent « Démonstration : données fictives », bouton « Voir comme : les deux produits | CRM seul | Envoi seul », bouton « Remettre la démo à zéro ».

**Où mettre vos fichiers (un fichier = un seul lot propriétaire).**
- Vos handlers : `frontend/src/demo/handlers/crm/<zone>.handlers.ts` ou `frontend/src/demo/handlers/envoi/<zone>.handlers.ts`, qui exportent `export const handlers: HttpHandler[]`. Ils sont chargés **tout seuls** par `src/demo/handlers/index.ts` (`import.meta.glob`) : ne modifiez pas `index.ts`.
- Écrivez les chemins avec `api('/chemin')` de `src/demo/outils.ts` (motif `*/api/v1/chemin`, valable en démo et sous Vitest). Le **même** tableau `handlers` sert à vos tests Vitest (`renderScreen(..., { handlers })`) et à vos e2e de démo : un seul faux serveur.
- Données : lisez et écrivez la base en mémoire `demoDb` de `src/demo/base.ts` (collections typées, identifiants stables, `demoDb.reinitialiser()`). Si votre zone a besoin de données que `demoDb` n'a pas, ajoutez **votre** générateur `src/demo/donnees/<produit>/<zone>.ts` (utilisez `graine('<zone>')` de `src/demo/graine.ts` : même graine = mêmes données) et branchez-le par `demoDb.etendre('<zone>', fabrique)`.
- Outils : `paginer()`, `filtrerTexte()`, `delai()` (latence réaliste 150-400 ms), `etatForce(request)` qui lit `?demo-etat=vide|erreur|chargement` pour montrer les 4 états de chaque écran ; `maintenant()` de `src/demo/horloge.ts` (aujourd'hui fixe : **mardi 12 janvier 2027, 09:30, Europe/Paris**) ; jamais `new Date()` dans une donnée de démo.
- Personnages et objets repères (déjà dans `demoDb`, à garder cohérents) : Paul Morin (réponse intéressée), Yves Roche (refus « Adresse inexistante »), Boulangerie des Tilleuls, Le Courrier du Rhône, Léa Fournier, Fédération BTP Rhône, Salon des artisans de Vienne, étiquette `salon-artisans-2026`, campagne « Organisateurs Rhône-Alpes », domaines `prospection-a.example` et `prospection-b.example`, boîte `will@prospection-b.example`.
- Contrat d'API d'Envoi : `backend/openapi/envoi/<zone>.yaml` (une description par zone, schémas communs dans `commun.yaml`) ; types générés `frontend/src/features/envoi/api/<zone>.d.ts` par `pnpm api:envoi`. Vous pouvez **compléter la description de votre zone** (ajouter un champ, une route) puis régénérer **votre** fichier de types ; ne touchez pas `commun.yaml` (notez le besoin dans la PR).

**Coquille (DM0-COQ).**
- Routes : **toutes** les routes des deux produits existent déjà dans `routeTree.tsx` et pointent vers un fichier de page « en attente » à votre nom (`<PageEnAttente lot="…" />`). Vous **remplacez le contenu** de vos fichiers de page ; vous ne touchez **pas** `routeTree.tsx`.
- Produit courant : `useProduitCourant()` (`src/features/socle/produit/`) ; la racine porte `data-produit="crm|envoi|commun"` ; couleurs par jetons `bg-produit`, `text-produit`, `bg-produit-pale`, `ring-produit` (jamais de couleur d'identité en dur, **jamais** sur une pastille d'état : les états gardent `StatusPill`).
- Droits : `useProduits()` → `{ crm, envoi }` valant `actif | suspendu | resilie | absent` ; `useAccesProduit('envoi')` pour l'utilisateur. Une route d'un produit absent répond « introuvable ».
- En-tête de page : `PageHeader` accepte `surTitre` (« CRM Pro », « Envoi » ou « Commun ») ; un **seul bouton plein** par écran (`<Button variant="primary">`, couleur du produit).
- Recherche Ctrl K : ajoutez vos actions dans **votre** fichier `src/features/<produit>/<zone>/commandes.ts` (`export const commandes: CommandeRecherche[]`), chargé tout seul par `src/features/socle/commandes/registre.ts`.
- Cloche : lit `GET /notifications` (champ `produit` et `lien`) ; pour qu'un événement de votre zone apparaisse, ajoutez-le dans vos données de démo (`demoDb.notifications`).
- « Tout arrêter » et le feu des envois : déjà dans l'en-tête (DM0-COQ), ne pas refaire.

**E2E de démo.** Votre suite va dans `frontend/tests/e2e/demo/<lot>.spec.ts` (jouée par `.github/workflows/demo.yml` sur le build de démo, Chromium, avec contrôle axe à 0 violation critique et un passage à 360 px). Utilisez les aides `tests/e2e/demo/outils.ts` (`ouvrirDemo(page, chemin, { offre })`).

## Règles de fer (à respecter sans exception)

1. **Tout en français** : code métier, commentaires, textes affichés (vouvoiement), commits, PR.
2. **Jamais de suppression de données de personnes** (ni en base, ni en démo, ni en migration) : on archive, on retire d'une liste, on marque « ne plus écrire ».
3. **Mode CLAIR seulement** (aucun mode sombre).
4. **Alertes : console (cloche) + e-mail seulement.** Jamais de téléphone, SMS, Telegram.
5. **2FA par code e-mail.**
6. **Jamais** : systeme.io, constructeur visuel d'automatisations, modèles clients (catalogue), agenda par client, serveur MCP, marque blanche.
7. **Jamais payer GitHub** : toute la CI tourne dans le dépôt public sur les machines standard gratuites (`ubuntu-24.04`) ; pas de « grosse machine », pas de service de test payant.
8. **Dépôt public** : aucun secret, aucun mot de passe, aucune adresse IP réelle, aucun nom de serveur réel. Seules les plages de documentation sont permises (`192.0.2.0/24`, `198.51.100.0/24`, `203.0.113.0/24`, `2001:db8::/32`).
9. **Interdits de communication** (jamais dans un texte, une donnée de démo ou un commentaire visible) : « Grenoble », « Aucun gain garanti », « certifié », « Qualiopi », « agréé », « labellisé », « accrédité ».
10. **Fidélité au vrai CRM** : avant de modifier une page qui existe, **lire le composant réel** en entier (et ses tests) ; garder ses titres, colonnes, filtres, actions et textes, sauf ce que la maquette validée change.
11. **Échelle typographique du vrai CRM** : Inter ; texte 14 px (`text-sm`), détails 12 px (`text-xs`, jamais moins) ; titres de page `text-2xl` (`md:text-3xl`), titres de section `text-lg font-bold` ; boutons et champs `h-9` (36 px), 44 px au téléphone ; aucune autre taille inventée.
12. **Données factices uniquement** : noms inventés, e-mails en `@example.test`, domaines en `.example`, SIREN invalides (clé de Luhn fausse), aucune personne réelle.

## Conventions du dépôt `axion-crm-pro` (lues dans le code, à suivre)

- Pas de CLAUDE.md : la règle est `CONTRIBUTING.md`. Conventional Commits **en français** (`feat`, `fix`, `test`, `docs`, `chore`, `refactor`, `ci`), squash & merge.
- Frontend : pnpm 9, Node ≥ 22, React 19, Vite 6, TanStack Router 1 (routes **en code** dans `frontend/src/app/routeTree.tsx`), TanStack Query 5, Tailwind v4 (jetons dans `frontend/src/styles/index.css`, bloc `@theme`, **pas** de tailwind.config), axios (`src/lib/api.ts`, base `VITE_API_BASE_URL + '/api/v1'`, cookies Sanctum), composants maison `src/components/ui/*` (Button, Card, KpiCard, StatusPill, PageHeader, PageShell, Tabs, Modal, EmptyState, QueryErrorState, Skeleton…), icônes lucide-react.
- Commandes qui doivent passer : `pnpm typecheck`, `pnpm lint` (**0 avertissement**), `pnpm test` (Vitest), `pnpm build` ; côté serveur `composer analyse` (PHPStan 8), Pint, Pest.
- Tests d'écran dans `frontend/tests/` (pas à côté du code) : `tests/screens/<Ecran>.test.tsx`, `tests/components/<nom-en-francais>.test.tsx`, rendu par `tests/helpers/renderScreen.tsx` (`renderScreen(<Ecran/>, { path, url, handlers })`), MSW avec `onUnhandledRequest: 'error'` (toute requête doit avoir un handler).
- Gardes de langue **bloquantes** : `tests/lib/vouvoiement.test.ts`, `tests/lib/sans-emoji.test.ts` (aucun émoji : icônes lucide), `tests/lib/jargon.test.ts` (pas de « Workspace », « Pending », « Timeline »…), `tests/components/navigation-cible.test.tsx` (même libellé dans le menu, le titre et le fil d'Ariane).
- Garde e2e : `frontend/tests/couverture-e2e.test.ts` : toute suite `*.spec.ts` doit être jouée par un workflow (les suites de `tests/e2e/demo/` le sont toutes par `demo.yml`, une fois DM0-DEMO fusionné).
- **Dépendances gelées** : n'ajoutez ni ne montez **aucune** dépendance (seul DM0-DEMO en a le droit, écrit dans son lot). Ne touchez pas `pnpm-lock.yaml` sauf ce lot.
- Jamais `continue-on-error`, jamais de test mis en quarantaine ou sauté pour passer au vert.

## Procédure (une PR pour ce lot)

1. Clonez `will383842/axion-crm-pro` et partez de `main` à jour : `git fetch origin main && git checkout -B feat/dm0-demo-socle origin/main`.
2. **Écrivez d'abord les tests** listés plus bas (ils doivent échouer), poussez-les : premier commit `test(...) : … (étape 1/n)`.
3. Codez par petites étapes ; **à chaque étape** : `pnpm typecheck && pnpm lint && pnpm test` (et Pest si serveur), commit en français, **`git push -u origin feat/dm0-demo-socle`** (pousser à chaque étape, pour ne rien perdre si la routine s'arrête). En cas d'échec réseau : 4 essais (2 s, 4 s, 8 s, 16 s).
4. Ouvrez **une seule PR** vers `main`, titre exact : **`feat(demo) : mode démo, faux serveur MSW, jeu factice à graine fixe, contrat Envoi (DM0-DEMO)`**. Description : objectif, fichiers touchés, captures (1440 et 360 px) pour un écran, tests ajoutés, **ligne de retour arrière**, et « Filet modifié : pourquoi » si un test existant a dû changer. Terminez par la ligne d'attribution demandée par la session.
5. Abonnez la session à l'activité de la PR ; **surveillez la CI** jusqu'au vert : en cas de rouge, reproduisez en local, corrigez la cause (jamais en affaiblissant un test), poussez.
6. **Ne fusionnez pas vous-même.** **Ne déployez rien** (aucun serveur, aucune mise en ligne, aucun `workflow_dispatch` de déploiement). Aucun secret, aucun mot de passe, aucune IP réelle, aucun e-mail envoyé. N'écrivez aucun commentaire GitHub hors de votre PR.
7. Si un fichier hors de votre liste doit absolument changer : **ne le modifiez pas** ; notez-le dans la PR, section « Hors périmètre, à faire par un autre lot ».
8. En fin de routine, laissez un résumé de 10 lignes dans la PR : fait, non fait, risques.
