# Routine DM0-COL : Renommer les « campagnes » de collecte en « Collectes » (routes, dossier, API)

> Texte autonome, prêt à copier dans une routine cloud. Dépôt de code : `will383842/axion-crm-pro` (écriture **seulement** sur la branche du lot, par PR). Dépôt des plans : `will383842/axion-crm-pro-plans` (**lecture seule** pour cette routine).

## Contexte

Axion-IA construit deux produits facturés à part : **CRM Pro** (le CRM existant, bleu de marque `#0051bd`) et **Envoi** (envoi d'e-mails en masse : campagnes, chauffe, domaines, serveurs, boîtes, réponses, désinscriptions ; turquoise pétrole `#0b7285` ; n'existe pas encore). Envoi se branchera sur plusieurs CRM par un adaptateur ; le CRM Pro est le premier. Entité d'envoi : SAS française. Décisions de Will : `plan/29-ADR-DEUX-PRODUITS.md` (6 OUI), `plan/20` § 12, `plan/30`. **Ordre voulu : le frontend d'abord, en démo présentable à des clients (données factices, faux serveur dans le navigateur), puis le serveur, puis le branchement.** Maquettes validées par Will (« PARFAIT ») : `maquettes/*.html` du dépôt des plans (ouvrez-les dans un navigateur ; le cadre violet « Maquette » n'est pas dans le produit). Guide : `maquettes/GUIDE-STYLE.md`. Par défaut : pas de mesure des ouvertures, pas de faux échanges de chauffe, pas de BIMI.

## Objectif du lot

Libérer le mot « campagnes » pour les **campagnes d'e-mails** d'Envoi (ADR-07 du plan 24, plan 28 § 3 n° 1). Aujourd'hui `/campaigns` = **collectes de données** (scraping) ; le menu dit déjà « Collectes ». Ce lot renomme **l'adresse, le dossier et l'API**, sans rien changer à l'écran ni aux données.
- Écrans : `/collectes`, `/collectes/new`, `/collectes/$collecteId` ; **redirection** de `/campaigns…` vers `/collectes…` (gardée 6 mois, avec test).
- Dossier `frontend/src/features/campaigns/` → `frontend/src/features/collectes/` (fichiers renommés en français : `CollectesListePage.tsx`, `CollecteAssistantPage.tsx`, `CollecteDetailPage.tsx`, `types.ts`, `fr-zones.ts`).
- API : nouvelles routes `/api/v1/collectes…` (mêmes actions : start, pause, resume, cancel, archive, unarchive, stats), **alias** des routes `/campaigns` qui restent (rien ne casse). Le frontend appelle `/collectes`.
- **Ne change pas** : la table `scraping_campaigns`, le modèle `ScrapingCampaign`, la commande `campaigns:start-scheduled`, le libellé « Collectes », le `data-tour="nav-campaigns"` (gardé tel quel pour la visite guidée).

## Fiche du lot

| | |
|---|---|
| Identifiant | **DM0-COL** |
| Vague | 0a |
| Dépend de | aucune (premier lot) |
| Taille | 0.5 j-agent |
| Modèle | Sonnet (code) ; relecture Opus |
| Branche | `feat/dm0-col-collectes` |
| Titre de la PR | `refactor(collectes) : /campaigns devient /collectes, avec redirections (DM0-COL)` |
| Maquettes | `maquettes/collectes.html`, `maquettes/collecte-nouvelle.html`, `maquettes/collecte.html (libellés seulement : aucun changement visuel dans ce lot)` |

## Fichiers autorisés (liste fermée : aucun autre fichier)

### Créés

- `frontend/src/features/collectes/*` (déplacés depuis features/campaigns/)
- `frontend/tests/screens/CollecteAssistantPage.saisie.test.tsx` (renommé)
- `frontend/tests/e2e/collectes-assistant.spec.ts` (renommé)
- `frontend/tests/components/redirection-collectes.test.tsx`
- `backend/tests/Feature/CollectesRoutesTest.php`

### Modifiés

- `frontend/src/app/routeTree.tsx` (routes collectes + redirections)
- `frontend/src/components/layout/Sidebar.tsx` (seulement `to: '/collectes'`)
- `frontend/src/components/layout/AutoBreadcrumbs.tsx`
- `frontend/src/features/dashboard/activite.ts` (liens seulement)
- `frontend/src/features/scraping/ScraperRunsPage.tsx` (liens)
- `frontend/src/features/international/RoumaniePage.tsx` (liens)
- `frontend/tests/components/navigation-cible.test.tsx`
- `frontend/tests/screens/redirections-navigation-cible.test.tsx`
- `.github/workflows/e2e.yml` (nom de la suite renommée, rien d'autre)
- `backend/routes/api.php` (groupe `/collectes` ajouté à côté de `/campaigns`)
- `backend/tests/Feature/NonRegression/instantanes/** et frontend/tests/non-regression/**` (seulement si R0 est déjà fusionné, avec « Filet modifié : pourquoi »)

### Supprimés ou vidés

- `frontend/src/features/campaigns/` (vidé par le déplacement : c'est un renommage, aucune donnée)

Tout autre fichier est **interdit** pour ce lot, notamment ceux que d'autres lots possèdent (tableau « Qui possède quoi » de `plan/30` § 4). Seule exception : un fichier régénéré par une commande du dépôt **pour votre zone** (types d'Envoi). `pnpm-lock.yaml` et `package.json` : **jamais** (sauf DM0-DEMO).

## Interdits propres à ce lot

- Toucher à la table, au modèle, aux jobs ou à la commande planifiée des collectes.
- Créer quoi que ce soit qui s'appelle « campagne » : c'est le rôle d'Envoi, plus tard.

## Tests à écrire d'abord (rouges avant le code)

- `redirection-collectes.test.tsx` : `/campaigns`, `/campaigns/new`, `/campaigns/42` mènent à `/collectes`, `/collectes/new`, `/collectes/42`.
- `navigation-cible.test.tsx` : l'entrée « Collectes » pointe sur `/collectes`, même libellé dans le menu, le titre et le fil d'Ariane.
- `CollectesRoutesTest.php` (Pest) : chaque route `/collectes…` répond comme sa jumelle `/campaigns…` (même contrôleur, mêmes droits, même RLS) ; les anciennes routes répondent toujours.
- Garde : `grep -rn "'/campaigns" frontend/src` ne trouve plus que les redirections.

## Critères de fin (tous vérifiables)

- `pnpm typecheck`, `pnpm lint`, `pnpm test`, `pnpm build` verts ; Pest et PHPStan verts ; CI verte (dont e2e.yml avec la suite renommée).
- Aucun changement visible à l'écran (capture avant/après de `/collectes` identique à `/campaigns`).
- Ligne de retour arrière : « revenir au commit précédent ; les alias `/campaigns` n'ont jamais été retirés ».

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

1. Clonez `will383842/axion-crm-pro` et partez de `main` à jour : `git fetch origin main && git checkout -B feat/dm0-col-collectes origin/main`.
2. **Écrivez d'abord les tests** listés plus bas (ils doivent échouer), poussez-les : premier commit `test(...) : … (étape 1/n)`.
3. Codez par petites étapes ; **à chaque étape** : `pnpm typecheck && pnpm lint && pnpm test` (et Pest si serveur), commit en français, **`git push -u origin feat/dm0-col-collectes`** (pousser à chaque étape, pour ne rien perdre si la routine s'arrête). En cas d'échec réseau : 4 essais (2 s, 4 s, 8 s, 16 s).
4. Ouvrez **une seule PR** vers `main`, titre exact : **`refactor(collectes) : /campaigns devient /collectes, avec redirections (DM0-COL)`**. Description : objectif, fichiers touchés, captures (1440 et 360 px) pour un écran, tests ajoutés, **ligne de retour arrière**, et « Filet modifié : pourquoi » si un test existant a dû changer. Terminez par la ligne d'attribution demandée par la session.
5. Abonnez la session à l'activité de la PR ; **surveillez la CI** jusqu'au vert : en cas de rouge, reproduisez en local, corrigez la cause (jamais en affaiblissant un test), poussez.
6. **Ne fusionnez pas vous-même.** **Ne déployez rien** (aucun serveur, aucune mise en ligne, aucun `workflow_dispatch` de déploiement). Aucun secret, aucun mot de passe, aucune IP réelle, aucun e-mail envoyé. N'écrivez aucun commentaire GitHub hors de votre PR.
7. Si un fichier hors de votre liste doit absolument changer : **ne le modifiez pas** ; notez-le dans la PR, section « Hors périmètre, à faire par un autre lot ».
8. En fin de routine, laissez un résumé de 10 lignes dans la PR : fait, non fait, risques.
