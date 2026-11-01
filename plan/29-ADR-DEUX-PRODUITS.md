# 29 : ADR : deux produits (CRM Pro et Envoi), adaptateurs, démo d'abord (01/11/2026)

**Lot P2 (plan).** Ce fichier intègre les **4 nouvelles décisions de Will** (D1 à D4). Elles **priment** sur le plan 20, sur l'ADR 24 et sur la carte du menu du plan 28 en cas de conflit. **RIEN N'EST CODÉ.**

Rédigé en lecture seule. Sources : plans `20`, `23`, `24`, `26`, `27`, `28` ; code de `axion-crm-pro` (barre latérale `F/components/layout/Sidebar.tsx`, `FeaturesController.php`). Aucun secret, aucune IP, aucune donnée de personne. Seuls des **noms** de fichiers et de tables sont cités.

**Décisions de Will intégrées (non reposées)**
- **D1** : CRM Pro et Envoi sont **deux produits distincts**, **facturés séparément**, distingués visuellement partout.
- **D2** : Envoi doit pouvoir se brancher sur **plusieurs types de CRM** : il est autonome, avec une porte d'entrée standard (adaptateurs).
- **D3** : Envoi fonctionne **d'abord chez nous**, dans le CRM Pro, comme **premier adaptateur**. Les deux se vendent ensemble ou séparément.
- **D4** : le **frontend est fait en premier, en entier**, comme **démo cliquable** présentable à des clients (données factices, sans serveur réel), pour les deux produits. Le serveur vient ensuite.
- Rappels gardés : maquettes de toutes les pages validées par Will avant tout codage d'écran ; UI très moderne début 2027, clair seulement ; entité d'envoi = SAS française ; aucune suppression de données de personnes ; jamais systeme.io, constructeur visuel, marque blanche, MCP.

**Format de chaque ADR** : contexte, options, **recommandation**, conséquences, retour arrière, au plus **une** question oui/non.

**Vocabulaire figé (ajouts au fichier 24)**
- **CRM Pro** = le produit de gestion des contacts et de la prospection (le CRM actuel).
- **Envoi** = le produit d'envoi d'e-mails (campagnes, boîtes, domaines, serveurs…). Nom de travail : le libellé est un réglage, il peut changer sans code.
- **Socle commun** = ce que les deux produits partagent (connexion, espace, équipe, journal…). Il n'est **pas vendu seul** : il vient avec chaque produit.
- **Adaptateur** = le morceau qui relie Envoi à **un** CRM. Le CRM Pro a le premier.
- **Démo** = le vrai frontend, branché sur un **faux serveur** dans le navigateur, avec des données factices.

---

## 0. En bref pour Will (12 lignes)

1. On a maintenant **deux produits** : **CRM Pro** (bleu) et **Envoi** (turquoise). Chacun a sa facture.
2. Un client peut prendre **CRM seul**, **Envoi seul**, ou **les deux**. Axion prend les deux.
3. Ce qui est commun (connexion, équipe, journal, oppositions) vient d'un **socle** inclus dans chaque produit.
4. Envoi ne lit **jamais** les tables du CRM directement : il passe par un **adaptateur** (une porte standard).
5. Le premier adaptateur est celui du **CRM Pro**. Un second, **générique** (fichier ou API), sert les autres CRM.
6. Sans CRM, Envoi garde un **petit carnet de destinataires** (pas d'affaires, pas de tâches).
7. Le menu montre ou cache chaque produit selon ce que le client a payé (un **drapeau par espace**).
8. Votre menu actuel **reste**. Envoi a **son propre espace**, avec 4 entrées : Campagnes, Envois, Réponses, Réglages d'envoi.
9. On passe d'un produit à l'autre par un **sélecteur** en haut de la barre ; la couleur change avec le produit.
10. On construit d'abord la **démo** des deux produits (≈ 6 semaines), avec un **lien public** sans aucune vraie donnée.
11. Ensuite le serveur, puis le branchement écran par écran. Premier envoi réel : **≈ 4 semaines plus tard** que prévu.
12. Charge : **589 j → ≈ 638 j** (+ 49 j) ; avec relectures ≈ 733 j. **6 questions oui/non** en fin de fichier.

---

## ADR-09 : Limites entre les deux produits

**Contexte.** Le plan 20 voyait l'envoi comme un **module optionnel** du CRM. Avec D1 et D2, l'envoi devient un **produit** qui doit vivre sans le CRM Pro. Il faut dire, pour chaque fonction, à qui elle appartient, et d'où vient ce qui est partagé.

**Options.**
- A. Tout partager (une seule base de données logique, chacun lit tout) : rapide, mais Envoi ne peut plus se brancher sur un autre CRM.
- B. Tout séparer (deux équipes, deux connexions, deux journaux) : propre, mais double travail et double connexion pour Axion.
- C. **Deux produits + un socle commun mince**, chacun propriétaire de ses données, échanges seulement par l'adaptateur.

**RECOMMANDATION : C.**

### 9.1 Ce que contient le CRM Pro seul

| Domaine | Contenu | Existe déjà (plan 28) |
|---|---|---|
| Base | entreprises, fiches entreprise, contacts, fiches contact, candidats, lettre et guide (personnes et abonnements) | oui |
| Organisation | listes manuelles, audiences ET/OU/SAUF, segments, étiquettes, doublons, vues sauvegardées, champs personnalisés | oui (vues : serveur seul) |
| Commercial | étapes (`lifecycle_stage`), affaires (Kanban, V1), tâches et notes (`activities`), appels et motifs, propriétaire de fiche | partiel |
| Presse et réseaux | médias, journalistes, registre des communiqués, fédérations et ordres, événements | oui |
| Alimenter la base | collectes (`/collectes`), carte de France, import de fichier, ajout rapide, provenance | oui (import par rapprochement) |
| Données de référence | base sectorielle (fiche de référence + surcouche, K12), Sirene, FINESS/RPPS | partiel |
| Conformité côté données | base légale par flux (`contacts.legal_basis`), date de première information art. 14 (`first_info_at`), gardes « données » (non diffusible, entrepreneur individuel, entreprise fermée) | oui |
| Synchro | dossier client avec la console du site, synchro sortante | oui (éteinte) |

### 9.2 Ce que contient Envoi seul

| Domaine | Contenu |
|---|---|
| Campagnes | campagnes, création en 5 étapes, séquences 1-4 étapes, liste figée (copie des destinataires à la validation), validation par version, résultats par campagne (sans ouvertures) |
| Contenu | messages types, éditeur, variables, aperçu, « m'envoyer un test », contrôleur de contenu, accroche IA figée |
| Infrastructure | boîtes, domaines, serveurs, groupes d'envoi, contrat `ServeurEnvoi` (simulation, KumoMTA, Postfix), configuration tirée depuis la base (E3b) |
| Délivrabilité | chauffe (« montée en douceur »), plafonds, disjoncteurs, frein « réponses en attente », listes noires, boîtes témoins, DMARC, test du matin, vérification des adresses (pré-vol, cascade) |
| Retours | événements (remis, rebonds, plaintes), VERP, relève IMAP, désinscription en un clic, page publique de désinscription |
| Réponses | boîte des réponses, tri (intéressé, pas intéressé, absent, STOP), réponses à rattacher, répondre depuis Envoi |
| Alertes d'envoi | règles d'alerte d'envoi, « Tout arrêter », arrêt par client (P5), arrêt général |
| Gardes au moment d'envoyer | France seulement, webmail refusé en froid, aucun lien vers le site d'Axion, bloc art. 14 présent, opposition et liste de sécurité vérifiées **à chaque envoi** |
| Sans CRM | **carnet de destinataires** (ADR-11 § 11.5) |

### 9.3 Ce qui est partagé (socle commun) et d'où il vient

| Partagé | Où il vit | D'où il vient aujourd'hui | Règle |
|---|---|---|---|
| Connexion, 2FA par e-mail, sessions | socle | CRM (`TwoFactorService`, page `/2fa`) | une seule connexion pour les deux produits |
| Espace (`workspace`) | socle | CRM | un client = un espace, même s'il n'a qu'Envoi |
| Équipe, invitations, rôles | socle | CRM (`UsersController`, `user_workspaces.role_slug`) | un rôle par espace + **accès par produit** (cases CRM / Envoi) ; permissions préfixées `crm.*` et `envoi.*` |
| Journal des actions | socle | CRM (`audit_logs` chaîné) | une colonne `produit` (`crm`, `envoi`, `socle`) ; une seule chaîne |
| Centre d'alertes (cloche) | socle | CRM (table `notifications`) | chaque alerte porte son produit et sa couleur |
| **Registre d'opposition** | socle | CRM (`opt_out`, `email_suppressions`, avec `workspace_id` ajouté par P2) + `suppression_plateforme` (ADR-02) | **une seule source par espace**. Le CRM Pro et Envoi y écrivent tous les deux. Un adaptateur externe le **synchronise** (ADR-11). L'opposition gagne partout. Rien n'est supprimé. |
| Désinscriptions | socle (même registre) | — | Envoi les **reçoit** (lien en un clic, STOP) et les **écrit** dans le registre ; le CRM les **lit** (pastille sur la fiche) |
| Demandes RGPD | socle | CRM (`RgpdRequestsPage`) | l'export d'une personne couvre **les deux produits** de l'espace ; effacement seulement sur ordre écrit (règle existante) |
| Sauvegardes, drapeaux, canal signé, observabilité, moteurs d'IA | socle | CRM | inchangés |

**Pourquoi le registre d'opposition est dans le socle.** C'est Envoi qui envoie : la loi s'applique au moment de l'envoi. Mais c'est souvent le CRM qui reçoit l'opposition (appel, formulaire, console du site). Un seul registre par espace évite deux vérités. Pour un CRM d'un autre éditeur, le registre reste chez nous et se synchronise par l'adaptateur.

**Cas limites tranchés.**
- **Presse** : le carnet presse est au CRM. L'envoi d'un communiqué est une **campagne Envoi** qui cible l'audience « presse » par l'adaptateur. Un client CRM seul garde le registre des communiqués à la main.
- **Vérification des adresses** (E4) : appartient à **Envoi** (elle sert la délivrabilité). Le code existant (`VerificationEmail`, mêmes clés de résultat) est repris par Envoi. Le CRM **affiche** le résultat que l'adaptateur lui écrit.
- **Éligibilité** : le CRM dit « ce contact est autorisé » (faits sur la donnée : base légale, segments fermés, Sirene, presse). Envoi **revérifie toujours** ses propres gardes (opposition, sécurité, France, webmail, art. 14). Envoi ne fait jamais confiance au seul CRM.
- **Étapes commerciales** : posées par le CRM. Envoi ne fait que **proposer** (« répondu », « rendez-vous ») par un événement ; le CRM applique « on ne recule jamais ».
- **Mes tâches** : CRM. Une réponse « intéressée » crée une tâche **dans le CRM** par l'adaptateur.

**Conséquences.** Les lots du plan 20 se découpent en trois familles : socle, CRM, Envoi (§ 7). Les tables d'envoi vivent dans un schéma Postgres à part (`envoi`), toutes avec `workspace_id` et RLS (ADR-02 inchangé). L'ADR-03 (`App\Emailing\ServeurEnvoi`) devient `App\Envoi\…`.

**Retour arrière.** Tant qu'aucun client n'a « Envoi seul », la frontière est une règle de code (ADR-10) : on peut la desserrer sans migration de données.

**Question pour Will (oui/non) :** les **réponses** aux campagnes vivent dans **Envoi**, et le CRM ne reçoit qu'un **résumé** (classement, date, lien, tâche créée) ? **Recommandation : oui** (Envoi seul doit pouvoir traiter ses réponses sans CRM).

---

## ADR-10 : Où vit le code d'Envoi

**Contexte.** D2 demande un Envoi autonome. Mais refaire connexion, équipe, journal et RLS dans un second logiciel coûte cher et double les failles possibles.

**Options.**
- A. Envoi reste un module mélangé au CRM (plan 20) : impossible à brancher sur un autre CRM.
- B. Un logiciel séparé dès le début (dépôt, serveur, base à part) : autonomie totale, mais ≈ 40 à 60 j de plus (socle refait) et deux mises à jour à suivre.
- C. **Même dépôt et même serveur, frontière stricte**, extractible plus tard.

**RECOMMANDATION : C.**
- Trois zones de code : `App\Socle`, `App\Crm`, `App\Envoi` (côté serveur) ; `features/socle`, `features/crm`, `features/envoi` (côté écrans).
- **Garde CI** : `App\Envoi` n'importe **jamais** `App\Crm`, et l'inverse non plus. Seuls passages permis : le socle, et l'adaptateur CRM Pro (`App\Crm\AdaptateurEnvoi`), qui vit **côté CRM** et réalise le contrat d'Envoi.
- Tables d'Envoi dans le schéma `envoi` ; Envoi ne lit **aucune** table du CRM (test SQL en CI : aucune requête d'Envoi ne cite une table hors `envoi` et socle).
- Routes : `/envoi/...` pour les écrans, `/api/v1/envoi/...` pour l'API. Description OpenAPI séparée (`openapi/envoi.yaml`, ADR-06).
- Le socle existant **n'est pas déplacé d'un coup** : le code neuf respecte la règle, l'ancien est rangé quand un lot le touche.
- Si un jour Envoi doit tourner sans le CRM sur un serveur à part (V2), on sort `App\Envoi` + `App\Socle` : la frontière est déjà testée.

**Conséquences.** + 3 j (garde CI, schéma, rangement des noms). L'ADR-03 et l'ADR-06 sont appliqués par zone.

**Retour arrière.** La garde CI peut passer en « avertir » le temps d'une correction ; rien ne change en base.

**Question pour Will (oui/non) :** Envoi reste dans **le même dépôt et le même serveur** que le CRM, avec une frontière stricte, plutôt qu'un logiciel séparé dès le début ? **Recommandation : oui.**

---

## ADR-11 : Modèle d'adaptateur (la porte d'entrée d'Envoi)

**Contexte.** Envoi doit lire des contacts autorisés dans un CRM, et y renvoyer ce qui s'est passé. Il faut un contrat **minimal**, testable, qui marche pour le CRM Pro, pour un fichier, et pour l'API d'un autre CRM.

**Options.**
- A. Un connecteur sur mesure par CRM : cher, sans fin.
- B. **Un contrat unique `SourceContacts` côté Envoi + un kit de conformité**, plusieurs réalisations (même méthode que `ServeurEnvoi`, ADR-03).
- C. Copier tout le CRM dans Envoi chaque nuit : lourd, données en double, contraire à la minimisation.

**RECOMMANDATION : B.**

### 11.1 Le contrat minimal qu'un CRM offre à Envoi

| # | Opération | Sens | Ce qui passe | Obligatoire |
|---|---|---|---|---|
| 1 | `capacites()` | CRM → Envoi | version du contrat, opérations prises en charge (étiquettes, étapes, tâches…) | oui |
| 2 | `listerAudiences()` | CRM → Envoi | listes, audiences, étiquettes : identifiant, nom, type, taille | oui |
| 3 | `lireContactsAutorises(audience, curseur)` | CRM → Envoi | par pages : identifiant externe, e-mail, prénom, nom, entreprise, fonction, pays, langue, base légale, date de première information, **champs de personnalisation sur liste blanche** ; **seulement** les contacts que le CRM autorise | oui |
| 4 | `lireContact(id)` | CRM → Envoi | relecture juste avant l'envoi (contact retiré ou opposé entre-temps) | oui |
| 5 | `lireOppositions(depuis)` | CRM → Envoi | oppositions nouvelles depuis un curseur | oui |
| 6 | `ecrireOpposition(opposition)` | Envoi → CRM | désinscription, STOP, plainte | oui |
| 7 | `ecrireEvenement(evenement)` | Envoi → CRM | envoyé, remis, rebond dur ou mou, plainte, désinscription (format normalisé du plan 26 § 1.4 ; **jamais d'ouverture**) | oui |
| 8 | `ecrireReponse(reponse)` | Envoi → CRM | classement, date, lien vers la réponse dans Envoi, extrait court optionnel | oui |
| 9 | `proposerEtape(contact, etape)` | Envoi → CRM | « répondu », « rendez-vous » | non (si `capacites` le dit) |
| 10 | `creerTache(contact, motif)` | Envoi → CRM | « rappeler », « répondre » | non |

**Règles du contrat (toutes testées par le kit).**
- **Envoi revérifie toujours** ses gardes, même si le CRM dit « autorisé ».
- **L'opposition gagne partout**, dans les deux sens, même si l'autre valeur est plus récente.
- **Aucune suppression ne se propage**, dans aucun sens.
- Chaque écriture porte une **clé d'idempotence** ; rejouer ne crée rien en double.
- Lecture par **curseur** (pas de copie complète) ; Envoi garde seulement la **liste figée** de chaque campagne (preuve de qui a reçu quoi) et les événements.
- Champs de personnalisation : **liste blanche** par espace ; tout autre champ est ignoré.
- Par HTTP : **canal signé v2** (ADR-04 § 4.2), un secret par espace et par sens.
- Une panne du CRM **met en pause** la campagne ; elle n'envoie jamais à l'aveugle.

### 11.2 Le kit de conformité d'adaptateur

≈ 25 tests communs : contact retiré entre validation et envoi → pas d'envoi ; opposition côté CRM → pas d'envoi en moins de 5 min ; STOP côté Envoi → opposition visible dans le CRM ; événement rejoué → pas de doublon ; CRM injoignable → pause ; champ hors liste blanche → ignoré ; aucune suppression transmise. Un adaptateur qui échoue n'est pas branché.

### 11.3 Schéma de l'adaptateur CRM Pro (le premier)

```
           ESPACE (socle : connexion, équipe, journal, registre d'opposition)
   ┌───────────────────────────────┐          ┌──────────────────────────────┐
   │ CRM Pro (App\Crm)             │          │ Envoi (App\Envoi)            │
   │  audiences, listes, étiquettes│          │  campagnes, liste figée      │
   │  ResolveurDestinataires       │◀─ 2,3,4 ─│  contrat SourceContacts      │
   │  EligibiliteCampagne          │          │  gardes d'envoi (toujours)   │
   │  activities, lifecycle_stage  │◀─ 7..10 ─│  événements, réponses        │
   │  AdaptateurEnvoi (réalise le  │          │                              │
   │  contrat, dans le même serveur)│         │                              │
   └──────────────┬────────────────┘          └──────────────┬───────────────┘
                  └──── 5, 6 : registre d'opposition du socle (une seule source) ───┘
```

- **Dans le même serveur**, sans HTTP : appel direct de la classe `AdaptateurEnvoi`, qui **réutilise** `ResolveurDestinataires`, `EligibiliteCampagne`, les audiences, les listes et les étiquettes (plan 28, doublons n° 3, 8, 9). Aucun code recopié.
- Événements écrits dans `activities` (types `email_envoye`, `email_reponse`…) ; étapes via `lifecycle_stage` avec « on ne recule jamais » ; tâches dans `activities` type `task`.
- Opposition : les deux produits lisent et écrivent **le même registre** du socle ; les opérations 5 et 6 sont donc instantanées.
- Le **même kit** passe sur cet adaptateur et sur l'adaptateur générique : c'est la preuve qu'Envoi ne dépend pas du CRM Pro.

### 11.4 Schéma de l'adaptateur générique (CRM d'un client)

```
   CRM du client                         Envoi (espace du client)
   ─────────────                         ─────────────────────────
   (a) Fichier :  export CSV  ───────▶   import : destinataires + listes + oppositions
                  import CSV  ◀───────   export : événements, réponses, oppositions (quotidien)
   (b) API :      appels signés ─────▶   API publique d'Envoi : pousser contacts, listes, oppositions
                  webhooks    ◀───────   webhooks signés : événements, réponses, oppositions
```

- Le client **pousse** ses contacts (fichier ou API) ; il n'a **rien à programmer** pour recevoir, sauf une adresse de webhook (ou il télécharge le fichier du jour).
- Les contacts poussés vont dans le **carnet de destinataires** (§ 11.5) ; l'adaptateur générique lit ce carnet pour réaliser les opérations 2 à 5.
- Webhooks signés (canal v2), rejouables, avec écran « Santé de la connexion » (ce qui est parti, ce qui a échoué, bouton « Renvoyer »).
- Des connecteurs dédiés à tel ou tel CRM du marché ne sont **pas** au plan : ils viendront seulement si un client le demande (même contrat, même kit).

### 11.5 Ce qu'Envoi stocke en propre quand il tourne sans CRM (carnet de destinataires)

| Table (schéma `envoi`) | Contenu | Ce qui n'y est pas |
|---|---|---|
| `envoi_destinataires` | e-mail, empreinte, prénom, nom, entreprise, fonction, pays, langue, base légale, date de première information, source (fichier, API, saisie), champs de personnalisation (liste blanche) | ni affaires, ni tâches, ni notes, ni fiche entreprise, ni étapes |
| `envoi_listes` + `envoi_liste_membres` | listes simples (pas d'audiences ET/OU/SAUF) | — |
| `envoi_etiquettes` | étiquettes simples | — |

- Toutes les tables avec `workspace_id` et RLS. Un destinataire **n'est jamais supprimé** : il peut être retiré d'une liste ou marqué « ne plus écrire ».
- Écran : onglet **Campagnes › Destinataires** (import, liste, fiche minimale). Il n'apparaît que si l'espace **n'a pas** le CRM Pro.
- Si le client prend plus tard le CRM Pro : un import unique du carnet vers le CRM (par rapprochement, provenance « Envoi »), puis l'adaptateur passe au CRM Pro.

**Conséquences.** Nouveaux lots A0 (contrat + kit, 3 j), A1 (adaptateur CRM Pro, 5 j), A2 (adaptateur générique, 10 j), A3 (carnet, 6 j). C1 **appelle l'adaptateur** au lieu des classes du CRM (− 2 j). Les webhooks sortants (X3, V2) sont absorbés par A2.

**Retour arrière.** Chaque espace a son adaptateur en réglage ; repasser un espace sur « simulation » coupe tout échange réel en une ligne.

**Question pour Will :** _aucune_ (découle de D2 et D3).

---

## ADR-12 : Facturation et droits d'accès par produit

**Contexte.** Un client peut avoir CRM seul, Envoi seul ou les deux. La facturation vit déjà dans le **Hub de la console** (décision du 27/10). Le CRM a déjà des drapeaux (`config/crm.php`, `FeaturesController`) et une barre latérale construite à partir de ces drapeaux (`sectionsDeNavigation(features)`).

**Options.**
- A. Deux instances séparées, une par produit : lourd, double connexion.
- B. **Un drapeau par produit et par espace**, posé par la console, lu par le serveur **et** par les écrans.

**RECOMMANDATION : B.**
- Table `fonctions_espace` (ADR-08) : deux lignes de base, `produit_crm` et `produit_envoi`, chacune avec un **état** : `actif`, `suspendu`, `resilie` (ADR-04 § 4.6, maintenant **par produit**).
- Posé **seulement** par la console des automatisations (canal signé v2) ; l'espace Axion a les deux, en ligne de réglage datée (aucun cas spécial en dur).
- **Serveur** : un garde `produit:envoi` / `produit:crm` sur chaque route. Produit absent = la route répond « introuvable » (pas d'indice). C'est le serveur qui protège ; le menu ne fait qu'afficher.
- **Écrans** : `FeaturesController` renvoie déjà `universes` ; il renvoie aussi `produits: { crm, envoi }`. La barre latérale montre le sélecteur et les entrées du produit seulement s'il est actif.
- **Utilisateur** : en plus du rôle, une case « accès à Envoi » / « accès au CRM ». Un utilisateur sans accès à un produit ne le voit pas, même si l'espace l'a payé.
- **Compteurs d'usage** envoyés à la console **par produit** (K6) : CRM = utilisateurs, fiches ; Envoi = messages envoyés, boîtes, domaines. Un dépassement **informe**, ne bloque pas (règle R10), sauf le plafond technique d'envoi.

**Ce que voit chaque client.**

| Offre | Barre latérale | Sélecteur | Adaptateur d'Envoi |
|---|---|---|---|
| CRM seul | menu de Will, sans espace Envoi ; à la place, une carte grisée « Envoi : activer depuis la console » dans Réglages | caché | — |
| Envoi seul | espace Envoi seulement + Réglages du socle (compte, équipe, journal, RGPD) | caché | générique, ou carnet seul |
| Les deux (Axion) | les deux espaces | visible | CRM Pro |

**Effets d'un changement d'état (rien n'est jamais supprimé).**
- Envoi `suspendu` : envois en pause ; lecture gardée. Envoi `resilie` : espace Envoi en lecture seule (export, preuves gardées), adaptateur coupé, aucun envoi.
- CRM `suspendu` ou `resilie` avec Envoi actif : le CRM passe en lecture seule ; l'adaptateur garde la **lecture** des contacts autorisés, sans création ; Envoi propose d'importer dans son carnet.

**Conséquences.** Lot B1 (droits par produit : drapeaux, gardes de route, menus, cases par utilisateur), 3 j. K6/K7 comptent et appliquent par produit (+ 2 j). J4 : **deux jeux** de conditions de vente et d'annexes de sous-traitance, un par produit (+ 1 j).

**Retour arrière.** Les deux drapeaux à « actif » = comportement d'aujourd'hui pour Axion.

**Question pour Will (oui/non) :** si un client **résilie le CRM mais garde Envoi**, Envoi garde la **lecture seule** des contacts du CRM (sans création) jusqu'à l'import dans son carnet ? **Recommandation : oui** (aucune campagne cassée, aucune donnée perdue).

---

## ADR-13 : Identité visuelle par produit

**Contexte.** D1 : les deux produits doivent se distinguer **partout**. Le guide (`maquettes/GUIDE-STYLE.md`) a déjà des **couleurs de sens** : vert = fait, terracotta = à faire, ambre = attention, bleu = en cours, violet = nouveau, rouge = arrêté, gris = neutre. La marque est `#2448e5`.

**Options.**
- A. Même couleur partout, seulement le nom change : pas assez distinct.
- B. Couleur d'identité forte sur tout l'écran (fond, pastilles) : se mélange aux couleurs de sens.
- C. **Couleur d'identité sur le cadre seulement** (barre, en-tête, bouton principal), jamais sur un état.

**RECOMMANDATION : C.**

| Produit | Teinte | Plein (texte blanc) | Foncé (survol) | Pâle (fond actif) | Contraste avec blanc |
|---|---|---|---|---|---|
| **CRM Pro** | bleu de marque | `#2448e5` | `#1b37b8` | `#e8edff` | 6,7:1 |
| **Envoi** | turquoise pétrole | `#0b7285` | `#085563` | `#e3f3f6` | 5,6:1 |
| **Commun** (écrans partagés) | ardoise | `#334155` (bandeau) ; bouton plein = bleu de marque | — | `#eef1f6` | 10:1 |

**Pourquoi ce turquoise.** Teinte ≈ 190°, entre le vert de sens (≈ 142°) et le bleu de sens (≈ 224°), donc loin des deux ; assez foncé pour un texte blanc lisible (AA). Un turquoise clair aurait été illisible avec du texte blanc.

**Règle d'or.** La couleur d'identité **ne sert jamais** à une pastille, une jauge, un feu ou un graphique qui veut dire un état. Les pages d'Envoi gardent les couleurs de sens. Garde automatique : `_fabrique/controle.py` (puis un test des écrans) refuse une pastille en teinte produit.

**Où on la montre.**
1. **Barre latérale** : liseré vertical de 4 px sur le bord gauche ; entrée active en fond pâle + barre de 3 px de la teinte.
2. **Sélecteur de produit** (haut de la barre) : pastille carrée de 32 px avec l'initiale (« C » bleu, « E » turquoise) + nom du produit.
3. **En-tête de page** : bande de 4 px en haut du contenu + sur-titre « CRM Pro » ou « Envoi » au-dessus du titre.
4. **Bouton principal** (le seul bouton plein de l'écran) : teinte du produit, avec son ombre.
5. Anneau de focus clavier, onglet actif, liens : teinte du produit.
6. Onglet du navigateur : « Envoi · Campagnes » ; e-mails d'alerte : sujet préfixé « [Envoi] » ou « [CRM Pro] ».
7. Cloche : chaque alerte porte une petite pastille d'identité (forme carrée, pour ne pas la confondre avec une pastille d'état ronde).

**Jetons.** `--produit`, `--produit-fonce`, `--produit-pale`, `--produit-ombre`, choisis par `data-produit="crm|envoi|commun"` sur la page. Une seule feuille de style ; aucune couleur en dur dans les écrans.

**Écrans partagés (identité « Commun »).** Connexion et code, Mon compte et sécurité, Équipe (Utilisateurs), Journal des actions, Centre d'alertes, Demandes RGPD, « Puis-je écrire à… ? » (registre d'opposition), recherche Ctrl K (résultats marqués par produit), page introuvable. Bandeau ardoise, sur-titre « Commun ». Ouverts depuis un produit, ils gardent la barre latérale de ce produit.

**Conséquences.** Les maquettes (plan 23) prennent les jetons et le sélecteur (U1quater, 1,5 j). Le guide de style reçoit une section « Identité des produits ».

**Retour arrière.** Changer une teinte = changer 4 jetons.

**Question pour Will (oui/non) :** le **turquoise pétrole** (`#0b7285`) pour Envoi vous va ? **Recommandation : oui.**

---

## ADR-14 : Menu

**Contexte.** Le menu actuel de Will reste : Tableau de bord, À traiter, Ma base, Presse, Réseaux, Ciblage, Alimenter la base, Réglages, Technique. Le plan 28 (§ 4) ajoutait **Campagnes** et **Envois** au milieu de ce menu, et **Réponses** dans À traiter. Avec D1, Envoi forme un **espace à part**.

**Options.**
- A. Une seule barre, avec un bloc Envoi en bas sous un séparateur turquoise : les deux restent visibles, mais le menu grossit et la frontière est faible.
- B. **Sélecteur de produit en haut de la barre** : la barre montre le menu d'**un** produit à la fois ; la couleur change avec lui.

**RECOMMANDATION : B.**

**Espace CRM Pro (bleu) : le menu de Will, inchangé.**

| Section | Entrées |
|---|---|
| Tableau de bord | Tableau de bord (+ une carte « Envoi aujourd'hui » si Envoi est actif : réponses à traiter, état des envois, lien vers Envoi) |
| À traiter | Doublons à vérifier, Personnes à rattacher, Propositions à valider, **Mes tâches** (nouvelle ligne, déjà proposée au plan 28) |
| Ma base | Entreprises, Contacts, Newsletter et guide, Candidats, Affaires (V1) |
| Presse | Médias, Journalistes, Communiqués envoyés |
| Réseaux | Fédérations et ordres, Événements |
| Ciblage | Audiences, Listes |
| Alimenter la base | Collectes (`/collectes`), Carte de France |
| Réglages | Paramètres, Utilisateurs, Étiquettes, Demandes RGPD |
| Technique | inchangé (Roumanie, Historique des collectes, Santé du système, Moteurs d'IA, Serveurs relais, Rotation des accès, Registre de l'IA, Journal des actions) |

**Retiré du menu CRM par rapport au plan 28** : les sections Campagnes et Envois, et la ligne Réponses d'À traiter. La pastille d'À traiter ne compte que des choses du CRM.

**Espace Envoi (turquoise) : 4 entrées, avec des onglets en haut des pages.**

| Entrée | Onglets (pages du plan 23) |
|---|---|
| **Campagnes** (`/envoi/campagnes`) | Campagnes (liste, création en 5 étapes, suivi) ; Messages types (et éditeur) ; Résultats ; **Destinataires** (seulement sans CRM Pro) |
| **Envois** (`/envoi/envois`) | Santé des envois ; Boîtes ; Domaines ; Serveurs et test du matin ; Montée en douceur ; Alertes d'envoi ; Ne plus écrire (« Puis-je écrire à… ? ») |
| **Réponses** (`/envoi/reponses`) | À traiter ; À rattacher ; Traitées (pastille = réponses à traiter) |
| **Réglages d'envoi** (`/envoi/reglages`) | Identité de l'expéditeur ; Règles de prudence et horaires ; Réglages des alertes ; Lien de RDV ; Connexion au CRM (adaptateur, santé de la connexion) ; Configuration technique ; DMARC « qui envoie en votre nom » ; Listes noires |

- « **Tout arrêter** » (rouge) reste dans l'en-tête **dans les deux espaces** dès qu'Envoi est actif : c'est un bouton de sécurité.
- Le sélecteur garde la dernière page ouverte de chaque produit.
- Avec un seul produit, le sélecteur disparaît.
- Code (plus tard) : `Sidebar.tsx` construit déjà les sections depuis `features` ; on ajoute `sectionsEnvoi(features)` et le sélecteur. Garde de navigation (`tests/components/navigation-cible.test.tsx`) étendue aux deux espaces.

**Conséquences.** La carte du menu du plan 28 (§ 4) est remplacée pour Campagnes, Envois et Réponses ; le reste du plan 28 tient. Les maquettes changent leur barre latérale (U1quater).

**Retour arrière.** Le sélecteur est une vue : revenir à l'option A ne touche que la barre.

**Question pour Will (oui/non) :** un **sélecteur en haut de la barre** (la barre montre un produit à la fois), plutôt que les deux menus empilés dans une seule barre ? **Recommandation : oui.**

---

## ADR-15 : Frontend d'abord : la démo, puis le serveur, puis le branchement

**Contexte.** D4 : le frontend complet des deux produits est fait **en premier**, comme démo cliquable pour des clients, sans serveur réel. Le plan 20 faisait l'inverse (sécurité, moteur, campagnes, puis écrans).

**Options.**
- A. Démo en HTML (prolonger les maquettes du plan 23) : rapide, mais **jetable** ; tout serait refait en vrai.
- B. **Démo = le vrai frontend React du CRM**, branché sur un **faux serveur dans le navigateur** qui suit la description OpenAPI (ADR-06).
- C. Démo sur un vrai serveur rempli de données factices : il faut d'abord le serveur, contraire à D4.

**RECOMMANDATION : B.**
- Faux serveur : bibliothèque d'interception dans le navigateur (type « Mock Service Worker »), réponses **générées depuis `openapi/crm.yaml` et `openapi/envoi.yaml`**. Les types des écrans sont les mêmes que ceux du vrai serveur : le branchement ne réécrit pas les écrans.
- Ces mêmes scénarios servent ensuite de **jeux d'essai e2e** : la démo ne se périme pas, elle est testée à chaque fusion.
- **Branchement route par route** : un réglage dit, pour chaque groupe de routes, « démo » ou « réel ». La démo publique reste toujours 100 % « démo ».

### 15.1 Ce qui est simulé

| Simulé | Comment |
|---|---|
| Données | **jeu factice réaliste** généré par un script à graine fixe : ≈ 300 entreprises fictives, 900 contacts, 12 campagnes, 4 domaines en `.example`, 8 boîtes, 60 réponses, 30 jours d'historique d'envoi. Noms inventés, e-mails en `example.test`, aucune IP affichée, aucun SIREN réel. |
| Trois offres | CRM seul, Envoi seul (carnet ou adaptateur générique), les deux : un bouton « Voir comme : … » dans le bandeau de démo |
| Temps | une horloge de démo (« aujourd'hui » fixe) pour que les graphiques soient toujours pleins |
| Actions | créer, modifier, lancer une campagne, répondre, « Tout arrêter » : tout marche **dans le navigateur**, rien ne part ; « Remettre la démo à zéro » |
| Connexion | écran de connexion réel ; code de démo affiché à l'écran ; aucun compte réel |
| Alertes et réponses | scénarios rejoués (une réponse arrive après 30 s, un domaine passe ambre) pour une présentation vivante |

### 15.2 Comment la démo est montrée à un client

- **Lien public** sur une adresse de démonstration séparée, site **statique** (aucun serveur, aucune base, aucun secret).
- Bandeau permanent « Démonstration : données fictives » ; page non indexée ; aucun formulaire qui collecte quoi que ce soit ; aucun e-mail envoyé.
- **Garde de construction** : la démo refuse de se construire si une adresse de serveur réel est réglée, et passe la garde des données personnelles existante (`infra/scripts/garde-donnees-personnelles.sh`) sur le jeu factice.
- 3 parcours guidés de 5 min (« Préparer une campagne », « Suivre ses envois », « Traiter une réponse et créer une tâche »).

### 15.3 Étapes, critères de fin, effort

| Étape | Contenu | Critère de fin | j |
|---|---|---|---|
| **DM-a** Maquettes à jour | sélecteur, espace Envoi, identité (U1quater) ; **validation écrite de Will** avant tout codage d'écran | Will valide les maquettes des deux espaces | 1,5 |
| **DM0** Socle de démo | système de design (U0), jetons d'identité, contrat OpenAPI des deux produits, faux serveur, jeu factice, bandeau, remise à zéro, hébergement statique, gardes | toutes les routes décrites répondent en démo ; démo en ligne, garde verte | 4 + 6 + 3 = 13 |
| **DM1** Démo CRM Pro | tous les écrans du CRM dans le nouveau style : connexion (S4), tableau de bord, entreprises, contacts, fiches, listes, audiences, étiquettes, doublons, presse, réseaux, collectes, Mes tâches, ajout rapide, import, modifier/retirer, Affaires et vues (avancés de V1), équipe, journal, RGPD | chaque écran du menu CRM s'ouvre et agit ; 7 parcours CRM ; 0 violation d'accessibilité ; 360 px | 24 |
| **DM2** Démo Envoi | campagnes (5 étapes, suivi, résultats), messages types, destinataires, santé, boîtes, domaines, serveurs, montée en douceur, alertes, ne plus écrire, réponses, réglages d'envoi, connexion au CRM, page publique de désinscription, écrans V1 visibles par un client | les 10 parcours du plan 27 § 4 tiennent ; campagne en 5 min et 15 clics ; 0 violation d'accessibilité | 33 |
| **DM3** Démo réunie | sélecteur, 3 offres, carte « Envoi aujourd'hui », parcours guidés, passe finale (U10), corrections après 2 tests avec Will | Will présente la démo à un prospect ; au plus 1 point bloquant | 3 + 2 + 4 = 9 |
| **Total démo** | | | **≈ 80,5 j** (dont ≈ 18 j vraiment nouveaux, le reste déplacé des lots U, S4, Q et V1) |
| **SV** Serveur | lots du plan 20 dans leur ordre de dépendance (sécurité, socle, envoi, campagnes…), + F0, A0, A1, B1 en V0 ; A2, A3 en V1 | chaque lot : sa preuve de réussite du plan 20 | (lots existants) |
| **BR** Branchement | chaque groupe d'écrans passe de « démo » à « réel » quand son lot serveur est fini ; le même scénario e2e passe sur la démo **et** sur le réel ; test de contrat vert | aucun écran ne reste en « démo » dans l'application réelle au feu vert (T1) | 8 (écarts démo/réel sur ≈ 50 écrans) |

**Ce qui peut avancer pendant la démo (sans écran).** Les délais incompressibles ne dépendent pas du code : achats et âge des domaines (21 jours au moins), demande de port 25, CNIL, rotation des clés. Les **correctifs de sécurité du CRM existant** (S1-S3, S5-S7, S9, R0) ne créent aucun écran. Je recommande de les laisser courir en parallèle ; c'est la seule question de cet ADR.

### 15.4 Impact sur le calendrier (semaines comptées depuis le feu vert de Will, L = semaine 1)

| Jalon | Plan 20 (avec la date du 2 nov.) | Avec la démo d'abord (et sécurité en parallèle) | Écart |
|---|---|---|---|
| Maquettes des deux espaces validées | S3 | **S2** | − 1 sem. |
| **Démo publique des deux produits** | — | **≈ S6-S7** | nouveau |
| Banc d'essai prêt | S6 | ≈ S9-S10 | + 3 à 4 sem. |
| Premier envoi interne | S13 | ≈ S17 | + 4 sem. |
| Premier envoi réel limité | S14 | ≈ S18 | + 4 sem. |
| Version console (client pilote) | S24 | ≈ S29 | + 5 sem. |

- Sans travail serveur en parallèle (réponse « non » à la question) : premier envoi réel ≈ **S20** (+ 6 sem.).
- L'âge des domaines et le port 25 restent **hors du chemin critique** s'ils démarrent en S1.
- Gain : des clients peuvent voir le produit **≈ 10 semaines avant** le premier envoi réel ; les écrans validés tôt évitent des retouches (− 4 j comptés).

### 15.5 Impact sur le total (base : 589 j après rapprochement, plan 28 § 5.4)

| Changement | V0 | V1 | V2 | Total |
|---|---|---|---|---|
| Base (plan 28) | 282 | 192,5 | 114,5 | **589** |
| DM0 : faux serveur, mode démo, hébergement, gardes | + 6 | | | + 6 |
| Jeu factice réaliste (2 produits, 3 offres) | + 3 | | | + 3 |
| DM3 : sélecteur, 3 offres, parcours guidés | + 3 | | | + 3 |
| U1quater : maquettes refaites (sélecteur, Envoi, identité) | + 1,5 | | | + 1,5 |
| Allers-retours de validation de la démo avec Will | + 4 | | | + 4 |
| BR : branchement démo → réel | + 8 | | | + 8 |
| F0 : frontière stricte (ADR-10) | + 3 | | | + 3 |
| A0 : contrat d'adaptateur + kit | + 3 | | | + 3 |
| A1 : adaptateur CRM Pro | + 5 | | | + 5 |
| B1 : droits par produit | + 3 | | | + 3 |
| A2 : adaptateur générique (API, webhooks, fichiers) | | + 10 | | + 10 |
| A3 : carnet de destinataires + écrans | | + 6 | | + 6 |
| K6/K7 par produit (+ 2) ; J4 deux jeux de contrats (+ 1) | | + 3 | | + 3 |
| C1 appelle l'adaptateur au lieu des classes du CRM | − 2 | | | − 2 |
| Moins de retouches d'écrans (validés en démo) | − 4 | | | − 4 |
| X3 (webhooks sortants) absorbé par A2 | | | − 2,5 | − 2,5 |
| K9 en partie couvert par l'API d'Envoi (A2) | | − 1,5 | | − 1,5 |
| Écrans V1 avancés dans la démo (Affaires et vues 5 ; écrans V1 visibles par un client 7) | + 12 | − 12 | | 0 |
| **Nouveau total** | **≈ 327,5** | **≈ 198** | **≈ 112** | **≈ 637,5 j** |

**≈ 638 j** (+ 48,5 j, soit + 8 %). Avec relectures (+ 15 %) : **≈ 733 j** (au lieu de 677). Fourchette ± 30 % : 446 à 829 j. Toujours hors total : les ≈ 15 à 20 j du § 11 du plan 20 (en partie faits).

**Conséquences.** Le § 5 du plan 20 (calendrier) se décale comme au § 15.4 ; l'ordre des pistes change : **H (interface) passe en tête**, en démo.

**Retour arrière.** La démo ne touche ni la base ni le serveur ; si elle prend du retard, on peut lancer la chaîne d'envoi plus tôt sans rien défaire.

**Question pour Will (oui/non) :** pendant la démo, on laisse courir **seulement** les travaux sans écran (achats et âge des domaines, port 25, correctifs de sécurité du CRM existant) ? **Recommandation : oui** (gain ≈ 2 semaines sur le premier envoi).

---

## 7. Ce que cela change dans les lots du plan 20

### 7.1 Classement de chaque lot : socle, CRM, Envoi, ou à découper

| Famille | Lots |
|---|---|
| **Socle** (inclus dans les deux produits) | R0, S1, S2, S3, S5, S6, S7, S8 (supprimé), S9, S11, S12, P1, P2 (registre d'opposition), P3, P4, K1, K2, K3 (création d'un client : choisir ses produits), K5, K8, U0 |
| **CRM Pro** | Q1, Q1b, Q2, K12 ; écrans CRM de U2-U9 et U12 |
| **Envoi** | E1 à E10 (dont E4 vérification), P5 (arrêts d'envoi), C1, C2, C4, C5, C6 (lettre d'information), RP1, RP2, RP3, RP4, X1, X2 ; écrans Envoi de U2-U9, U11, U12, U13 |
| **À découper** | **C3** (gardes « données » au CRM, gardes « au moment d'envoyer » dans Envoi) ; **J1** (date de première information au CRM, refus J+30 dans Envoi) ; **Q3** (file d'appels et script au CRM ; étape « appel » d'une campagne multicanal dans Envoi, qui crée une tâche par l'adaptateur) ; **K6/K7** (par produit) ; **K9** (API du CRM au CRM ; API d'Envoi dans A2) ; **K10** (propriétaire de fiche au CRM ; accroche IA dans Envoi) ; **J4** (deux jeux de documents) ; **S4** (écrans de connexion : socle, faits en démo) ; **U2-U9, U12, U13** (une part CRM, une part Envoi) ; **T1** (feu vert d'Envoi, avec l'adaptateur CRM Pro) |

_(C6, la lettre d'information, part par Envoi : elle est rangée dans Envoi. Le registre des abonnés reste au CRM, comme aujourd'hui.)_

### 7.2 Lots nouveaux

| ID | Contenu | Phase | j | Dépend de |
|---|---|---|---|---|
| **U1quater** | Maquettes : sélecteur, espace Envoi, jetons d'identité ; validation de Will | V0 | 1,5 | U1 |
| **DM0** | Socle de démo : faux serveur, jeu factice, bandeau, remise à zéro, hébergement statique, gardes | V0 | 9 (6 + 3) | U0, U1quater |
| **DM1** | Démo CRM Pro (écrans pris dans U2-U9, U12, S4, Q1, Q1b, Q2) | V0 | (déplacé) | DM0 |
| **DM2** | Démo Envoi (écrans pris dans U2-U9, U11, U12, U13, RP) | V0 | (déplacé) | DM0 |
| **DM3** | Démo réunie : sélecteur, 3 offres, parcours guidés, validation | V0 | 7 (3 + 4) | DM1, DM2 |
| **BR** | Branchement démo → réel, groupe par groupe | V0 | 8 | chaque lot serveur |
| **F0** | Frontière stricte socle / CRM / Envoi (garde CI, schéma `envoi`) | V0 | 3 | P1 |
| **A0** | Contrat `SourceContacts` + kit de conformité d'adaptateur | V0 | 3 | F0, E1 |
| **A1** | Adaptateur CRM Pro (réutilise `ResolveurDestinataires`, `EligibiliteCampagne`, `activities`) | V0 | 5 | A0, P2 |
| **B1** | Droits par produit : `produit_crm` / `produit_envoi`, gardes de route, menus, accès par utilisateur | V0 | 3 | P1, S6 |
| **A2** | Adaptateur générique : API publique d'Envoi, webhooks signés, import/export de fichiers, santé de la connexion | V1 | 10 | A0, P4 |
| **A3** | Carnet de destinataires (Envoi seul) + onglet Destinataires | V1 | 6 | A0 |

### 7.3 Lots modifiés

| Lot | Changement |
|---|---|
| **P1** | l'ADR inclut ce fichier 29 ; drapeaux **par produit** ; `App\Emailing` devient `App\Envoi` |
| **P2** | le registre d'opposition est **dans le socle** et sert les deux produits et tous les adaptateurs |
| **C1** | ne lit plus le CRM directement : il appelle l'adaptateur (A1) ; − 2 j |
| **C3, J1, Q3, K10** | découpés comme au § 7.1 (sans changement de charge) |
| **E4** | rangé dans Envoi ; réutilise `VerificationEmail` et ses clés ; écrit le résultat au CRM par l'adaptateur |
| **K3** | la création d'un client choisit ses produits |
| **K6, K7** | usage et états **par produit** ; + 2 j |
| **K9** | API du CRM seulement (l'API d'Envoi est dans A2) ; − 1,5 j |
| **J4** | deux jeux de CGV et d'annexes de sous-traitance ; + 1 j |
| **U0** | jetons d'identité `--produit-*` ; contrat OpenAPI **par produit** |
| **U2-U9, U11, U12, U13** | absorbés par DM1 et DM2 (écrans faits en démo, puis branchés par BR) ; − 4 j de retouches |
| **Q2, part écrans de U13** | écrans avancés de V1 en V0 (démo) ; le serveur reste en V1 |
| **X3** | supprimé (absorbé par A2) ; − 2,5 j |
| **T1** | le feu vert vérifie aussi le kit d'adaptateur sur A1 |

### 7.4 Nouvel ordre (V0)

1. **S1** : U1quater (maquettes des deux espaces) → validation de Will. En parallèle (si oui à la question d'ADR-15) : R0, S1-S3, S5-S7, S9, achats, domaines, port 25, CNIL.
2. **S2-S3** : U0 + DM0 (socle de démo, contrat OpenAPI des deux produits), F0, B1.
3. **S3-S6** : DM1 et DM2 en parallèle (3 routines chacune).
4. **S6-S7** : DM3 → **démo publique**.
5. **S6 et après** : chaîne serveur du plan 20 (P1-P5, E1 → E8, A0, A1, C1 → C3, RP1 → RP3, J1, J3), avec **BR** au fil de l'eau.
6. **≈ S16-S18** : T1, premier envoi interne puis réel limité.
7. **V1** : A2, A3, puis les lots V1 du plan 20 ; version console ≈ S29.

### 7.5 Ce qui change dans les autres fichiers du plan

- **Plan 20** : § 1 (points 5, 7, 13), § 2.3 (totaux), § 3 (lots, voir § 7.1 à 7.3), § 5 (calendrier, voir § 15.4).
- **Plan 24** : ADR-03 (`App\Envoi`), ADR-04 § 4.6 (états **par produit**), ADR-08 (drapeaux `produit_crm`, `produit_envoi`).
- **Plan 28** : § 4 (menu) remplacé pour Campagnes, Envois et Réponses par l'ADR-14 ; § 5.4 (total) remplacé par l'ADR-15 § 15.5.
- **Plan 23 et maquettes** : barre latérale avec sélecteur ; jetons d'identité ; onglet Destinataires ; écran « Connexion au CRM ».
- **Guide de style** : section « Identité des produits » (ADR-13).

---

## Questions pour Will (résumé, 6 oui/non)

| # | Question | Recommandation |
|---|---|---|
| Q1 (ADR-09) | Les réponses aux campagnes vivent dans Envoi ; le CRM n'en reçoit qu'un résumé (classement, date, lien, tâche) ? | **Oui** |
| Q2 (ADR-10) | Envoi reste dans le même dépôt et le même serveur que le CRM, avec une frontière stricte ? | **Oui** |
| Q3 (ADR-12) | CRM résilié mais Envoi gardé : Envoi garde la lecture seule des contacts du CRM jusqu'à l'import ? | **Oui** |
| Q4 (ADR-13) | Turquoise pétrole (`#0b7285`) pour Envoi ? | **Oui** |
| Q5 (ADR-14) | Sélecteur de produit en haut de la barre (un produit à la fois) ? | **Oui** |
| Q6 (ADR-15) | Pendant la démo, seuls les travaux sans écran avancent (domaines, port 25, sécurité de l'existant) ? | **Oui** |

_(6 questions au total : une par ADR qui en a besoin ; l'ADR-11 n'en a pas.)_

---

## Limites

- **Console des automatisations et Hub non lus** : la façon dont le Hub facture deux produits (deux abonnements ou deux lignes) est à relire contre leur cahier avant K6.
- **Code lu, rien exécuté** ; le CRM local lu s'arrête à la fusion #386 (#388 en tête du dépôt, sans effet ici).
- **Estimations ± 30 %** ; la part « vraiment nouvelle » de la démo (≈ 18 j) est la plus sûre ; le branchement (8 j) dépend de la qualité du contrat OpenAPI.
- **Noms des produits** : « CRM Pro » et « Envoi » sont des noms de travail ; un changement de nom ne coûte qu'un libellé.
- Les connecteurs dédiés à des CRM du marché ne sont **pas** chiffrés (hors plan, seulement sur demande d'un client).

---

## Résumé (15 lignes)

1. CRM Pro et Envoi deviennent deux produits facturés à part ; un socle commun (connexion, équipe, journal, opposition) vient avec chacun.
2. Le registre d'opposition est unique par espace, dans le socle ; il gagne partout ; rien n'est supprimé.
3. Envoi ne lit jamais les tables du CRM : il passe par un contrat d'adaptateur de 10 opérations (8 obligatoires).
4. Premier adaptateur : CRM Pro, dans le même serveur, qui réutilise le ciblage et l'éligibilité existants.
5. Adaptateur générique : fichier ou API publique + webhooks signés ; même kit de tests que le CRM Pro.
6. Sans CRM, Envoi garde un carnet de destinataires minimal (onglet Campagnes › Destinataires).
7. Code : même dépôt, trois zones (socle, CRM, Envoi), frontière testée en CI, schéma `envoi` à part.
8. Droits : drapeaux `produit_crm` et `produit_envoi` par espace, posés par la console, gardés côté serveur.
9. Identité : CRM bleu de marque `#2448e5`, Envoi turquoise pétrole `#0b7285`, jamais sur une pastille d'état.
10. Menu de Will inchangé ; Envoi = espace à part (Campagnes, Envois, Réponses, Réglages d'envoi) via un sélecteur.
11. Démo d'abord : le vrai frontend sur un faux serveur, jeu factice, lien public sans aucune donnée réelle.
12. Démo ≈ 80 j dont ≈ 18 j nouveaux ; démo publique ≈ semaine 6-7 après le feu vert.
13. Premier envoi réel ≈ + 4 semaines ; version console ≈ + 5 semaines.
14. Total : 589 → ≈ 638 j (+ 48,5 j) ; ≈ 733 j avec relectures.
15. 6 questions oui/non pour Will, toutes avec recommandation « oui ».
