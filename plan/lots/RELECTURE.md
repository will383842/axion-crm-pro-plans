# Routine RELECTURE : relire la PR d'un lot (Opus)

> Texte autonome, prêt à copier. Une routine **Opus** par PR de lot, lancée quand la CI de la PR est verte. Dépôt `will383842/axion-crm-pro` en **lecture**, plus le droit de commenter **la PR relue**. Paramètre à remplir : `<NUMERO_PR>` et `<ID_LOT>`.

## Ce que vous faites

1. Lisez le texte du lot dans `will383842/axion-crm-pro-plans`, fichier `plan/lots/<ID_LOT>.md`, et `plan/30-PLAN-FINAL-ET-LOTS-DE-CODE.md` § 4 (« Qui possède quoi »).
2. Lisez **tout le diff** de la PR `<NUMERO_PR>`.
3. Vérifiez, et notez chaque écart avec fichier et ligne :
   - **Périmètre** : aucun fichier hors de la liste fermée du lot (sinon : bloquant).
   - **Règles de fer** (ci-dessous) : chacune, une par une.
   - **Fidélité** : pour une page qui existe dans le CRM, titres, colonnes, filtres et textes gardés, sauf ce que la maquette validée change ; comparez les captures jointes à `maquettes/<page>.html`.
   - **Échelle** : seulement 12, 14, 16, 18, 20, 24 px (30 px pour les titres de page dès 768 px, comme le vrai CRM) ; un seul bouton plein par écran ; couleur d'identité jamais sur une pastille d'état.
   - **Tests** : ils échouent sans le code (lisez-les comme un attaquant : un test qui passerait toujours ne compte pas) ; aucun test existant affaibli sans « Filet modifié : pourquoi ».
   - **Données** : toutes factices (`example.test`, `.example`, IP de documentation, SIREN invalides) ; aucun secret ; aucun mot interdit.
   - **Production** : rien de visible en production tant qu'Envoi est absent (chaque fusion déploie le CRM réel).
4. Rendez un verdict dans **un seul** commentaire de PR : « PRÊTE À FUSIONNER » ou « À CORRIGER » + liste numérotée (bloquant / à améliorer), terminée par la ligne d'attribution de la session.
5. Vous ne poussez pas de code, ne fusionnez pas, ne déployez rien. Les lots d'écrans et de textes (démo) peuvent être fusionnés sur votre verdict par la personne ou la routine que Will a désignée (décision 11 B) ; les lots **serveur et sécurité** (R0, S1-S9) sont fusionnés **par Will seulement**.

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
