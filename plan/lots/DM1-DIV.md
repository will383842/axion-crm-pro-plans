# Routine DM1-DIV : Démo CRM Pro : Newsletter et guide, Candidats, Collectes, Carte de France

> Texte autonome, prêt à copier dans une routine cloud. Dépôt de code : `will383842/axion-crm-pro` (écriture **seulement** sur la branche du lot, par PR). Dépôt des plans : `will383842/axion-crm-pro-plans` (**lecture seule** pour cette routine).

## Contexte

Axion-IA construit deux produits facturés à part : **CRM Pro** (le CRM existant, bleu de marque `#0051bd`) et **Envoi** (envoi d'e-mails en masse : campagnes, chauffe, domaines, serveurs, boîtes, réponses, désinscriptions ; turquoise pétrole `#0b7285` ; n'existe pas encore). Envoi se branchera sur plusieurs CRM par un adaptateur ; le CRM Pro est le premier. Entité d'envoi : SAS française. Décisions de Will : `plan/29-ADR-DEUX-PRODUITS.md` (6 OUI), `plan/20` § 12, `plan/30`. **Ordre voulu : le frontend d'abord, en démo présentable à des clients (données factices, faux serveur dans le navigateur), puis le serveur, puis le branchement.** Maquettes validées par Will (« PARFAIT ») : `maquettes/*.html` du dépôt des plans (ouvrez-les dans un navigateur ; le cadre violet « Maquette » n'est pas dans le produit). Guide : `maquettes/GUIDE-STYLE.md`. Par défaut : pas de mesure des ouvertures, pas de faux échanges de chauffe, pas de BIMI.

## Objectif du lot

Faire tourner en démo, reprises à l'identique : `PersonnesPage`, `PersonneDetailPage`, `CandidatesPage` (console), les **Collectes** (dossier `features/collectes/` renommé par DM0-COL : liste, assistant, détail, avec des collectes factices de tous statuts) et la **Carte de France** (`CoveragePage`, `FranceCoverageMap` : style minimal forcé, aucune tuile externe).

## Fiche du lot

| | |
|---|---|
| Identifiant | **DM1-DIV** |
| Vague | 2 |
| Dépend de | DM0-* fusionnés ; démarre dès qu'une place se libère dans la vague 1 |
| Taille | 1.5 j-agent |
| Modèle | Sonnet (code) ; relecture Opus |
| Branche | `feat/dm1-div-base-et-collectes` |
| Titre de la PR | `feat(crm) : démo de la lettre et guide, des candidats, des collectes et de la carte (DM1-DIV)` |
| Maquettes | `maquettes/newsletter-guide.html`, `maquettes/personne-newsletter.html`, `maquettes/candidats.html`, `maquettes/collectes.html`, `maquettes/collecte-nouvelle.html`, `maquettes/collecte.html`, `maquettes/carte-france.html` |

## Fichiers autorisés (liste fermée : aucun autre fichier)

### Créés

- `frontend/src/demo/handlers/crm/alimenter.handlers.ts`
- `frontend/src/demo/donnees/crm/alimenter.ts`
- `frontend/tests/e2e/demo/dm1-div.spec.ts`

### Modifiés

- `frontend/src/features/crm-console/PersonnesPage.tsx`
- `frontend/src/features/crm-console/PersonneDetailPage.tsx`
- `frontend/src/features/crm-console/CandidatesPage.tsx`
- `frontend/src/features/collectes/**`
- `frontend/src/features/coverage/**`
- `frontend/tests/screens/PersonnesLettreGuide.test.tsx`
- `frontend/tests/screens/CarteDeFrance.test.tsx`
- `frontend/tests/screens/CollecteAssistantPage.saisie.test.tsx`

### Supprimés ou vidés

- (aucun)

Tout autre fichier est **interdit** pour ce lot, notamment ceux que d'autres lots possèdent (tableau « Qui possède quoi » de `plan/30` § 4). Seule exception : un fichier régénéré par une commande du dépôt **pour votre zone** (types d'Envoi). `pnpm-lock.yaml` et `package.json` : **jamais** (sauf DM0-DEMO).

## Interdits propres à ce lot

- Toute requête vers un serveur de tuiles ou un service extérieur.

## Tests à écrire d'abord (rouges avant le code)

- `dm1-div.spec.ts` : ouvrir une collecte, voir sa progression ; la carte s'affiche sans requête externe (aucune requête hors `demo.invalid`).
- Tests existants verts.

## Critères de fin (tous vérifiables)

- Chaque page du lot s'ouvre en démo (`pnpm dev:demo`, offre « les deux ») avec des données factices et **agit** (les gestes modifient `demoDb` et se voient après rechargement).
- Les 4 états (normal, vide `?demo-etat=vide`, erreur, chargement) sont propres sur chaque page.
- Comparaison visuelle avec la maquette à 1440 et 360 px jointe à la PR ; écarts expliqués.
- 0 violation axe critique ; 360 px sans défilement horizontal ; zones tactiles de 44 px au téléphone ; clavier seul possible.
- CI verte : typecheck, lint, Vitest, build, build de démo, e2e de démo, e2e existants.

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

1. Clonez `will383842/axion-crm-pro` et partez de `main` à jour : `git fetch origin main && git checkout -B feat/dm1-div-base-et-collectes origin/main`.
2. **Écrivez d'abord les tests** listés plus bas (ils doivent échouer), poussez-les : premier commit `test(...) : … (étape 1/n)`.
3. Codez par petites étapes ; **à chaque étape** : `pnpm typecheck && pnpm lint && pnpm test` (et Pest si serveur), commit en français, **`git push -u origin feat/dm1-div-base-et-collectes`** (pousser à chaque étape, pour ne rien perdre si la routine s'arrête). En cas d'échec réseau : 4 essais (2 s, 4 s, 8 s, 16 s).
4. Ouvrez **une seule PR** vers `main`, titre exact : **`feat(crm) : démo de la lettre et guide, des candidats, des collectes et de la carte (DM1-DIV)`**. Description : objectif, fichiers touchés, captures (1440 et 360 px) pour un écran, tests ajoutés, **ligne de retour arrière**, et « Filet modifié : pourquoi » si un test existant a dû changer. Terminez par la ligne d'attribution demandée par la session.
5. Abonnez la session à l'activité de la PR ; **surveillez la CI** jusqu'au vert : en cas de rouge, reproduisez en local, corrigez la cause (jamais en affaiblissant un test), poussez.
6. **Ne fusionnez pas vous-même.** **Ne déployez rien** (aucun serveur, aucune mise en ligne, aucun `workflow_dispatch` de déploiement). Aucun secret, aucun mot de passe, aucune IP réelle, aucun e-mail envoyé. N'écrivez aucun commentaire GitHub hors de votre PR.
7. Si un fichier hors de votre liste doit absolument changer : **ne le modifiez pas** ; notez-le dans la PR, section « Hors périmètre, à faire par un autre lot ».
8. En fin de routine, laissez un résumé de 10 lignes dans la PR : fait, non fait, risques.
