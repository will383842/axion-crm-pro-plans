# 15 : Vérification de conformité du plan « CRM Pro complet » (01/11/2026)

Responsable conformité, en LECTURE SEULE. Aucun e-mail envoyé, aucun serveur touché, aucun secret lu ni recopié. Je ne suis pas avocat : je donne l'état de la règle, la source, mon niveau de certitude (élevée / moyenne / faible) et ce que Will doit valider. Will a choisi de ne pas prendre de juriste : chaque point « à valider » est donc une décision de Will, tracée.

**Matière lue** : `plan/00`, `02`, `03` (§ 0, 1, 2, 4, 5, 8, 14, 15), `04`, `05`, `06` (§ 1, 5), `10`, `REPRENDRE.md`. Recherches web du 01/11/2026 (sources en fin de fichier). Les constats des agents précédents n'ont pas été rejoués sur le code.

**Décisions de Will respectées ici** : aucune suppression de données de personnes sauf instruction ; pas de juriste ; aucun pixel de suivi ; jamais « Grenoble » ni « certifié / Qualiopi » dans une communication ; conservation des fiches de prospection déjà tranchée (20/08 : je ne rouvre pas le débat, je signale seulement ce que le texte art. 14 doit contenir).

Légende des verdicts : **CONFORME** (le plan suffit), **À COMPLÉTER** (bonne direction, il manque une pièce), **RISQUE** (le plan tel qu'écrit expose Axion ou un client).

---

## 0. VERDICT : ce qui BLOQUE le premier envoi réel

Le premier envoi réel (Will + 4 boîtes témoins puis 20 organisateurs, fichier 10 § 12) ne doit pas partir tant que les 8 points suivants ne sont pas levés. Tout le reste peut suivre en V1/V2.

| # | Bloquant | Pourquoi | Levée |
|---|---|---|---|
| BL1 | **Entité expéditrice non choisie (D-07 : SAS ou OÜ)** | Sans elle : pas d'identité, pas d'adresse postale, pas de texte art. 14, pas de mentions légales. L.34-5 al. 4 CPCE interdit de dissimuler l'identité de l'expéditeur. Si OÜ : l'autorité chef de file pourrait devenir l'Estonie, et le droit applicable aux mentions change. | Décision de Will (Q1). |
| BL2 | **Texte d'information art. 14 non écrit et non validé (D-26)** | Art. 14.3.b RGPD : au plus tard à la première communication. Garde G11 du plan : sans texte, le contrôleur bloque (bon), donc rien ne part. | Doc D1, validé par Will. |
| BL3 | **Organisateurs collectés les 26-27/09 : délai art. 14.3.a d'un mois dépassé (≈ 27/10)** | L'art. 14.3.a fixe « un délai raisonnable, au plus un mois » ; l'usage pour une communication (14.3.b) ne prolonge pas ce délai (lignes directrices transparence du G29/CEPD, certitude moyenne-élevée). Le manquement existe déjà ; chaque jour l'aggrave. | Décision de Will D-01 (Q2) : information dédiée et non commerciale à ces personnes AVANT toute prospection, ou gel du lot. |
| BL4 | **Fuite du 19/08 : ni notification CNIL ni motif écrit de non-notification** | Art. 33.1 : 72 h, et au-delà la notification doit expliquer le retard ; art. 33.5 : documenter TOUTE violation, même non notifiée. Envoyer de la prospection à grande échelle avec une violation non traitée aggrave la position d'Axion en cas de contrôle. Ce n'est pas un bloquant technique, c'est un bloquant de prudence. | Décision de Will (Q3). Le brouillon reste NON ENVOYÉ par moi (lecture seule, action extérieure). |
| BL5 | **Pages publiques absentes** : page de désinscription `go.<domaine d'envoi>` et page « pourquoi ce message » (art. 14 complet), servies sous le domaine d'envoi, jamais sous `axion-ia.com` | RFC 8058 + règles Gmail/Yahoo (2024) et Microsoft (mai 2025) ; L.34-5 : moyen d'opposition gratuit et simple. Critique 06 C2 : pas de lien vers `axion-ia.com` dans un message à froid. | Docs D2 et D1 publiés, test « POST un clic → `peutRecevoir()` faux ». |
| BL6 | **Garde pays « hors France = refus »** absente (06 C1) | Suisse et Canada : consentement préalable même entre professionnels (voir § 1.5). | Garde codée (C-G13), défaut fermé. |
| BL7 | **Garde « statut de diffusion partielle Sirene » et garde « particulier / adresse de webmail »** absentes | Sirene : une entreprise individuelle en diffusion partielle (statut « P ») ne peut pas être utilisée à des fins de prospection (arrêté A123-96, certitude moyenne). Will veut ÉTEINDRE les workflows `purge-non-diffusible` (02 J9) : sans garde d'exclusion, l'arrêt de la purge rendrait ces personnes contactables. | Garde C-G14 codée AVANT d'éteindre la purge. |
| BL8 | **Registre art. 30 + analyse d'intérêt légitime (LIA) du flux « organisateurs »** non écrits (02 J8) | Art. 30 obligatoire (l'exemption < 250 salariés ne joue pas pour un traitement non occasionnel). La LIA est la preuve de la base légale (art. 6.1.f) que la CNIL demandera en premier. | Docs D10 et D11 (2 jours-agent). |

Ne bloquent PAS le premier envoi d'Axion, mais bloquent la **première vente à un client** : contrat de sous-traitance (D6), CGV/CGU (D5), politique d'usage acceptable (D4), contrôle d'entrée du client (KYC, 06 M8), RLS prouvée, assurance (Q9).

---

## 1. Mécanismes du plan : conforme, risque ou à compléter

### 1.1 Base légale de la prospection B2B par e-mail
- **Règle** : L.34-5 CPCE impose le consentement des **personnes physiques** pour la prospection par e-mail. Doctrine CNIL constante : une personne physique peut être prospectée sur son adresse **professionnelle** sans consentement préalable si (1) le message est en rapport avec sa profession, (2) elle est informée et peut s'opposer simplement et gratuitement dès le premier message. Base RGPD : intérêt légitime (art. 6.1.f) avec LIA documentée. Certitude : **élevée**.
- **Plan** : bon cadre (opposition avant tout envoi G3, bloc art. 14 G11, entité exigée). **À COMPLÉTER** : la condition « en rapport avec la profession » n'est contrôlée nulle part. Ajouter un champ « angle métier » obligatoire par campagne et par segment (ex. : « organisateurs d'événements → outils IA pour l'organisation d'événements »), relu par Will à la validation. REQ-SEC-011 (objet lié à la profession) est remontée en V1 par l'audit : la mettre en **V0**.

### 1.2 Information art. 14 avant le premier message
- **Règle** : art. 14 RGPD (identité et coordonnées du responsable, finalités, base légale et intérêt légitime poursuivi, catégories de données, **source**, destinataires dont sous-traitants, transferts hors UE, durée ou critères de conservation, droits dont opposition, réclamation CNIL). Délai : un mois après la collecte au plus, et au plus tard au premier message. Certitude : **élevée**.
- **Plan** : bloc `{bloc_information}` au premier message pour tout non-informé (G11), registre art. 14 par adresse (02 J5), provenance obligatoire (02 J6), mention du vérificateur (VER-030). **CONFORME sur le principe, À COMPLÉTER** :
  1. Le bloc dans le corps doit être court (identité, source, finalité, opposition, lien) et renvoyer à la page complète (information « à plusieurs niveaux », admise par le CEPD). Les deux niveaux doivent être versionnés ensemble.
  2. Le registre doit lier chaque adresse à la **version** du texte (02 J5 le prévoit : le passer en V0).
  3. La règle « au plus un mois » doit être codée : alerte à J+21 après collecte pour toute fiche non informée, et refus de l'éligibilité au-delà de J+30 sans décision tracée (C-G15). Sans cette garde, le cas des 26-27/09 se reproduira à chaque collecte.
  4. `first_info_at` posé « à la livraison » (RET-036) : correct ; un rebond dur ne doit pas le poser.

### 1.3 Liste d'opposition unique
- **Règle** : art. 21.2-3 RGPD (opposition à la prospection : absolue, sans motif) ; L.34-5 (moyen d'opposition). Certitude : **élevée**.
- **Plan** : une porte `peutRecevoir()`, appelée à la vague et à moins de 15 min de l'injection, retrait des messages en attente en moins de 5 min, levée impossible pour une opposition. **CONFORME** (au-dessus de la pratique courante).
- **À COMPLÉTER** : (a) migration `workspace_id` sur `opt_out` et `email_suppressions` en V0, en tenant compte du choix « `scope` » de la migration `2026_08_14_000004` (06 X10) ; (b) écrire que dans l'espace Axion « l'opposition gagne partout » (site, CRM, lettre, presse) ; (c) **conserver l'empreinte d'opposition même après un effacement art. 17** (c'est la seule façon de respecter l'opposition durablement ; CNIL l'admet) ; (d) opposition reçue par téléphone (pharmacies, 06 C5) → même porte.

### 1.4 Désinscription en un clic et STOP
- **Règle** : RFC 8058 (`List-Unsubscribe` + `List-Unsubscribe-Post`, signés DKIM) exigé par Gmail et Yahoo pour les expéditeurs en masse depuis 2024, traitement sous 2 jours ; lien visible dans le corps aussi (le lien du corps seul ne suffit pas pour Gmail/Yahoo) ; Microsoft (Outlook.com, Hotmail, Live) applique depuis mai 2025 SPF, DKIM, DMARC aux expéditeurs de plus de 5 000 messages par jour et recommande la désinscription fonctionnelle. Taux de plaintes : viser < 0,1 %, jamais ≥ 0,3 % (Google). Aucune nouvelle règle officielle 2026 trouvée (certitude moyenne : sources secondaires) ; le durcissement Gmail de novembre 2025 (rejets 5xx) est rapporté par des prestataires, non vérifié chez Google.
- **Plan** : en-têtes, `mailto:`, POST sans confirmation, opposition en moins d'une minute, page à l'entité, STOP = opposition (RET-025). **CONFORME** et plus strict que les règles (1 min contre 2 jours).
- **À COMPLÉTER** :
  1. **Durée de vie du lien** (06 M1) : le domaine d'envoi et la page `go.` doivent rester en service au moins 3 ans après le dernier envoi, y compris après le départ d'un client (sinon un domaine expiré racheté recevrait les désinscriptions). Renouvellement automatique des domaines.
  2. **STOP** : élargir la reconnaissance (« stop », « désinscrire », « ne plus m'écrire », « retirez-moi », « unsubscribe », « pas intéressé, ne me recontactez pas ») ; en cas de doute → opposition (le doute profite à la personne). L'onglet « À confirmer (STOP par réponse) » (03 § 7.5) ne doit **pas** retarder l'effet : opposer d'abord, confirmer ensuite.
  3. Page de désinscription : aucune connexion demandée, aucune question obligatoire, aucun traceur, pas de Google Fonts, rien sous `axion-ia.com`.

### 1.5 Destinataires hors France (Suisse, Canada, Belgique…)
- **Suisse** : LCD art. 3 al. 1 let. o : la publicité de masse par télécommunication exige le consentement préalable, sans exception B2B générale (exception : relation client existante). Certitude : **élevée**. → **RISQUE** : refus.
- **Canada** (LCAP / CASL) : consentement exprès ou tacite ; le tacite existe pour une adresse publiée bien en vue sans mention de refus et un message lié à la fonction, mais il faut le prouver adresse par adresse ; amendes jusqu'à 10 M$ CA. Québec : Loi 25 en plus. Certitude : **moyenne-élevée**. → **RISQUE** : refus.
- **Belgique** : Code de droit économique art. XII.13 et AR du 4 avril 2003 : consentement par défaut ; exception pour les adresses **impersonnelles** de personnes morales (info@, contact@) ; une adresse nominative d'un salarié reste soumise au consentement selon la lecture courante. Certitude : **moyenne**. → **RISQUE** : refus par défaut, ouverture possible plus tard « génériques seulement » après fiche validée par Will.
- **Luxembourg, Monaco, Maghreb, autres UE** : non étudiés → refus.
- **Plan** : rien (06 C1). **Correction** : garde C-G13 « destinataire hors France = refus » en V0, fondée sur le pays de l'organisation (SIREN/adresse), le domaine national (.ch, .ca, .be, .lu, .qc.ca) et, en doute, refus. Ouverture par pays = case tracée de Will après fiche pays. **Attention aussi au sens inverse** : si l'entité est l'OÜ estonienne, envoyer vers la France reste soumis à L.34-5 (le droit du destinataire s'applique en pratique ; certitude moyenne).

### 1.6 Cibles TPE/PME contre entreprises individuelles et particuliers
- **Règle** : une personne morale n'a pas de données personnelles (adresse `contact@` d'une SARL : hors RGPD, mais pas hors L.34-5 dans son esprit). Un **entrepreneur individuel / micro-entrepreneur** est une personne physique : la règle B2B s'applique s'il est contacté sur une adresse professionnelle pour son activité ; s'il utilise une adresse de webmail grand public (`@gmail.com`, `@orange.fr`, `@free.fr`), on ne peut pas distinguer le professionnel du particulier → traiter comme **particulier = consentement requis**. Certitude : **moyenne** (doctrine CNIL non écrite sur ce cas précis).
- **Sirene diffusion partielle (« P »)** : nom, adresse et enseigne ne doivent pas être utilisés à des fins de prospection par des tiers (A123-96, INSEE). Certitude : **moyenne-élevée**.
- **Plan** : « cible TPE/PME » (02), INSEE fermé par défaut (G4). **RISQUE** dès qu'INSEE s'ouvre (4,29 M d'entreprises, 1,32 M de personnes). **Corrections** :
  - C-G14 : statut de diffusion « P » = jamais contactable (exclusion, **sans suppression de la fiche**, conforme à l'ordre de Will). À coder **avant** d'éteindre `purge-non-diffusible` (02 J9).
  - C-G16 : adresse de webmail grand public = refus en prospection à froid, sauf preuve tracée qu'elle est l'adresse publiée de l'entreprise (site, annuaire) et décision de Will.
  - Exclusion des catégories juridiques « particulier » et des fiches sans SIREN actif ; vérification « entreprise radiée » au figé du segment (06 M1.3).

### 1.7 Santé, FINESS, pharmacies
- **Règle** : prospecter un pharmacien titulaire sur son adresse professionnelle pour un outil lié à son officine relève de la règle B2B (1.1). Ce ne sont pas des **données de santé** (art. 9) tant qu'on ne traite que l'identité professionnelle. FINESS : données publiques sous Licence Ouverte (certitude moyenne) ; **RPPS / Annuaire Santé** : conditions de réutilisation à relire (certitude **faible** sur l'admission de la prospection commerciale) ; ne pas croiser avec des données patients ou de prescription. Les pharmacies sont soumises à des règles déontologiques de publicité (CSP), qui pèsent sur ce que le CLIENT écrit à des tiers, pas sur la réception.
- **Plan** : santé/FINESS fermé par défaut (G4). **CONFORME** pour Axion. **À COMPLÉTER** pour Oury Création (06 B1, C5) : (a) fiche « source et licence » par référentiel (FINESS, RPPS) avant ouverture ; (b) si Axion **fournit** la base pharmacies au client, Axion est responsable de traitement de cette base et doit informer (art. 14) les pharmaciens de la transmission à des clients, avec base légale et contrat de mise à disposition (voir § 2.1) ; (c) téléphone : opposition par téléphone et vérification Bloctel ne s'appliquent pas en B2B pur, mais l'opposition orale doit écrire `opt_out` ; (d) formulations interdites santé (§ 4.3).

### 1.8 Presse
- **Règle** : journaliste nommé = personne physique sur adresse professionnelle → règle B2B (1.1) + art. 14 + opposition. Certitude : **élevée**. L'exemption « journalistique » (art. 85, loi 78-17 art. 80) protège le travail des journalistes, pas la prospection d'Axion vers eux.
- **Plan** : nature `presse` distincte, segment seul, `AdressePresseFiable`, art. 14 et opposition, désinscription presse = opposition dans tous les univers, communiqué par lien. **CONFORME**. **À COMPLÉTER** : un média précis par campagne (déjà dans 10 § 4) codé comme garde ; corriger le registre (« presse fermée » attribué à tort à Will, 06).

### 1.9 Opposition par domaine
- **Plan** : bouton « opposition pour toute mon organisation » (RET-026), onglet « Par domaine ». **CONFORME** (au-delà de l'obligation). **À COMPLÉTER** : refuser l'opposition par domaine sur les domaines de webmail (sinon un seul clic bloquerait tout `orange.fr`, ce qui est sans danger juridique mais fausse les statistiques) ; journaliser qui a demandé.

### 1.10 Durée de conservation
- **Règle** : art. 5.1.e (limitation de la conservation) ; art. 14.2.a impose d'annoncer la durée **ou les critères** pour la déterminer. Référence CNIL (référentiel gestion commerciale) : 3 ans à compter de la collecte ou du dernier contact émanant du prospect. Certitude : **élevée**.
- **Plan** : « conservation illimitée » (02 en-tête), « politique de conservation écrite (illimitée, motif) » (02 J7). Will a tranché le 20/08 et ne veut plus en débattre : je ne pose pas de question. **Je signale le RISQUE** pour qu'il soit connu : une durée « illimitée » écrite dans le texte art. 14 serait contraire à l'art. 5.1.e tel que la CNIL l'applique.
- **Formulation compatible avec « aucune suppression sauf instruction »** (à valider par Will, sans rouvrir la décision) : annoncer des **critères** plutôt qu'une durée — « vos coordonnées professionnelles sont utilisées pour la prospection pendant 3 ans après notre dernier échange ; au-delà, elles ne servent plus à vous contacter et sont réexaminées ». Techniquement : la fiche n'est pas effacée, elle sort de l'éligibilité (C-G17 « non contactable après 3 ans sans échange »). La suppression reste une décision de Will au cas par cas. Cela réduit le risque sans supprimer de donnée.
- **Exception écrite à « rien n'est jamais supprimé »** (06 M2) : l'effacement sur demande art. 17 est une obligation, pas un choix d'Axion. Écrire la règle : « aucune suppression automatique ni décidée par Axion ; effacement sur demande de la personne (art. 17) ou sur ordre écrit de Will ou du client ; empreinte d'opposition toujours gardée ».

### 1.11 Données collectées fin septembre (art. 14.3.a dépassé)
- Voir BL3. Options (Q2) :
  - **A (recommandée)** : message d'**information pure**, sans aucune offre ni appel à l'action commercial, envoyé par la porte unique avec désinscription, objet clair (« Information sur l'utilisation de vos coordonnées professionnelles »), puis 10 jours ouvrés minimum avant toute prospection. Régularise au mieux ; ne gomme pas le retard.
  - B : gel du lot (fiches gardées, non contactables) jusqu'à décision.
  - C (déconseillée) : prospecter directement avec le bloc art. 14 dans le premier message. 14.3.b serait respecté, 14.3.a ne l'est pas.
  - Dans tous les cas : noter le retard et sa cause dans le registre (redevabilité, art. 5.2) et coder C-G15 pour que cela ne se reproduise pas.

### 1.12 Vérification d'adresses par un tiers
- **Plan** : DPA obligatoire avant activation (VER-017), mention art. 14 (VER-030), jamais de sonde SMTP depuis une IP d'envoi. **CONFORME**. **À COMPLÉTER** : lieu d'hébergement et transferts du vérificateur (Hunter ou alternative UE) dans la liste des sous-traitants ; préférer un vérificateur hébergé dans l'UE.

### 1.13 Aucun pixel, aucun lien réécrit
- **Plan** : G5. **CONFORME** et favorable (pas de traceur au sens de l'art. 82 loi 78-17, donc pas de consentement « cookies » à gérer dans les e-mails). Garder aussi : pas de raccourcisseur, pas d'identifiant personnel dans une URL (le jeton de désinscription opaque est admis : finalité strictement nécessaire).

---

## 2. Multi-client

### 2.1 Sous-traitant ou responsable conjoint ?
| Cas | Qualification | Certitude | Condition pour que ça tienne |
|---|---|---|---|
| Client qui importe SES fichiers et prospecte avec le CRM | **Client = responsable ; Axion = sous-traitant (art. 28)** | élevée | Axion n'utilise pas les données pour ses propres fins : pas de « liste de protection de plateforme » partagée (03 § 1.3, garder « non » par défaut), pas d'entraînement d'IA sur les données client, statistiques de plateforme agrégées et anonymes seulement. |
| Axion fournit sa base sectorielle (pharmacies) au client (exemple de Will, 06 B1) | **Axion = responsable de traitement de la base ET de sa transmission** ; le client devient responsable **distinct** (pas conjoint) de l'usage qu'il en fait | moyenne | Information art. 14 par Axion de la transmission « à des clients abonnés » (catégories de destinataires) ; base légale de la cession (intérêt légitime, LIA dédiée) ; contrat de mise à disposition (finalité limitée, pas de revente, opposition remontée vers Axion, retour ou retrait en fin d'abonnement) ; traçabilité fiche → client → date. |
| Axion et le client décident ensemble des finalités et moyens (ex. Axion choisit ciblage et messages pour le client, « on s'occupe de tout ») | **Risque de responsabilité conjointe (art. 26)** | moyenne | À éviter : le client valide chaque campagne et chaque texte (case « validé par le client » tracée). Si Axion fait des campagnes « clés en main », il faut un accord art. 26 en plus du DPA. |
| Données des utilisateurs du client (comptes, journaux de connexion, 2FA) | Axion responsable pour la gestion de son service (facturation, sécurité), sous-traitant pour le reste | moyenne | À écrire dans la notice RGPD du CRM (D8). |

**Recommandation** : Axion sous-traitant par défaut ; base sectorielle traitée comme un **produit de données distinct** avec son propre contrat ; pas de campagne rédigée et décidée par Axion pour un client sans validation écrite du client.

### 2.2 Trame du contrat de sous-traitance (art. 28.3)
Objet, durée, nature et finalité, types de données et catégories de personnes ; instructions documentées (la console et les réglages du client valent instruction) ; confidentialité du personnel ; sécurité (annexe art. 32 : RLS, chiffrement, 2FA, sauvegardes, journaux sans adresse) ; sous-traitants ultérieurs (liste en annexe, information préalable 30 jours avant ajout, droit d'objection) ; assistance pour les droits des personnes (transmission sous 48 h, 03 § 1.4) ; assistance art. 32 à 36 (violation, AIPD) ; **notification de violation au client sous 24 à 48 h** ; sort des données en fin de contrat (§ 2.3) ; audits (questionnaire écrit d'abord, audit sur site à la charge du client, préavis 30 jours) ; transferts hors UE ; responsabilité et plafond ; obligations du client (base légale de ses fichiers, art. 14 à son nom, interdiction des fichiers achetés ou loués sans preuve, respect de la politique d'usage) ; droit de suspendre en cas d'abus.

### 2.3 Fin de contrat : concilier art. 28.3.g et « jamais de suppression décidée par Axion »
- **Règle** : au choix **du client**, le sous-traitant supprime OU renvoie les données, et détruit les copies sauf obligation légale de conservation. Certitude : **élevée**.
- **Lecture qui concilie** (06 X1 : Will a déjà fixé « export, puis proposition de suppression à 24 mois, puis son clic » pour la console) : ce n'est pas **Axion** qui décide de supprimer, c'est le **client** qui choisit. La clause de fin de contrat devient :
  1. export complet remis au client (format ouvert, 02 B7) ;
  2. le client choisit dans un formulaire : « restituer et supprimer » / « restituer et conserver N mois puis supprimer » ; la suppression s'exécute **sur son instruction écrite**, pas sur décision d'Axion ;
  3. sans réponse du client : conservation **chiffrée et gelée** (aucun traitement), proposition de suppression à 24 mois, clic de Will ; le DPA doit l'annoncer (sinon conserver indéfiniment les données d'un ex-client sans instruction viole 28.3.g) ;
  4. exceptions conservées par Axion : factures (10 ans, Code de commerce L.123-22), empreintes d'opposition si le client y consent (pour que sa page de désinscription continue de fonctionner, § 1.4).
- **Risque résiduel** : un « jamais de suppression » absolu, appliqué contre l'instruction d'un client qui demande la suppression, serait **non conforme**. Il faut que Will l'accepte (Q5).

### 2.4 Registre art. 30
- Deux registres : **responsable** (traitements d'Axion : prospection Axion par flux — organisateurs, fédérations, presse, pharmacies si base fournie ; lettre d'information ; clients et facturation ; comptes du CRM ; candidatures) et **sous-traitant** (art. 30.2 : un enregistrement par client, catégories de traitements, sous-traitants ultérieurs, transferts, mesures de sécurité). Vit **dans la base du CRM** (écran Conformité, 02 J12), jamais dans un dépôt (règle « jamais payer GitHub », dépôt public). Effort : 1,5 j-agent rédaction + écran déjà prévu.

### 2.5 Sous-traitants ultérieurs (à lister, lieu, garantie)
| Tiers | Rôle | Lieu / transfert | À vérifier |
|---|---|---|---|
| Hetzner (ou OVH) | serveur d'envoi, base | UE | DPA en ligne signé |
| Cloudflare | DNS, page `go.`, voit IP et jetons | US possible | certification Data Privacy Framework + CCT ; mention art. 14 (06 M4) |
| Vérificateur d'adresses (Hunter ou UE) | vérification | à vérifier | DPA, lieu, DPF |
| Hébergeur des boîtes de réponse (D-70) | réponses, plaintes ARF | à choisir | UE de préférence |
| ZeptoMail (Zoho) | 2FA, alertes (pas d'envoi commercial) | centre UE à confirmer | DPA |
| Backblaze B2 | sauvegardes chiffrées | choisir la région UE | DPA |
| Stripe, Tiime | facturation | Stripe US (DPF) | DPA |
| Fournisseur d'IA (classement des réponses, V2) | traite le texte des réponses | souvent US | DPF/CCT, pas d'entraînement, à annoncer AVANT activation |
| Spamhaus DQS | requêtes DNS sur IP/domaines | UE/hors UE | peu de données personnelles |
| GitHub | code public | US | **aucune donnée personnelle** (gitleaks + garde) |

### 2.6 Transferts hors UE
Chapitre V RGPD : DPF (décision d'adéquation UE-US du 10/07/2023, toujours en vigueur à ma connaissance ; certitude moyenne sur son avenir) ou CCT + analyse d'impact du transfert. **À COMPLÉTER** : colonne « transfert » dans le tableau des tiers, mention dans le texte art. 14, la notice du CRM et l'annexe du DPA. Préférer des prestataires UE quand l'écart de coût est faible.

### 2.7 AIPD (DPIA) : nécessaire ?
- **Axion** : **OUI, recommandée fortement**. Critères CEPD/CNIL réunis : grande échelle (base INSEE 4,29 M / 1,32 M personnes), croisement de sources (INSEE, FINESS, presse, collectes web), personnes non informées au départ (art. 14 indirect), usage innovant (classement par IA). Deux critères suffisent à la présumer requise. Le plan prévoit « AIPD v2 » (E13, 02 J8) : **V0**, avant ouverture d'INSEE ; pour le premier envoi limité aux organisateurs, une AIPD courte du flux suffit.
- **Clients** : c'est au client (responsable) de la faire ; Axion fournit un **modèle d'AIPD pré-rempli** (assistance art. 28.3.f), livré avec le DPA.

---

## 3. Documents à préparer (liste + plan, sans rédaction complète)

Méthode validée par Will le 27/10 : rédigés par l'IA, relus par un second agent Opus, validés par Will. Un modèle par entité (Axion) et un gabarit « au nom du client ».

| # | Document | Plan | Prio | Effort |
|---|---|---|---|---|
| D1 | **Information art. 14** (2 niveaux) | Niveau 1, dans le message (5 lignes) : qui écrit, d'où vient l'adresse, pourquoi, comment s'opposer en un clic, lien. Niveau 2, page « pourquoi ce message » sous le domaine d'envoi : responsable et contact ; finalité ; base légale et intérêt poursuivi ; données ; **source précise** (par flux) ; destinataires et sous-traitants ; transferts ; durée ou critères (§ 1.10) ; droits (accès, rectification, effacement, limitation, opposition) ; réclamation CNIL ; date et version. Variante « information pure » pour le lot de septembre (§ 1.11). | V0 | 1,5 |
| D2 | **Page de désinscription** | Titre « Vous ne recevrez plus de messages de <Entité> » ; confirmation immédiate (le GET n'exige rien, le POST suffit) ; option « toute mon organisation » ; lien « pourquoi ce message » ; contact pour autres droits ; aucun traceur ni police externe ; version client. | V0 | 0,5 |
| D3 | **Mentions légales par entité** | Pour Axion (SAS ou OÜ) et pour chaque client : dénomination, forme, capital, siège, SIREN/RCS (ou registre estonien), TVA, directeur de publication, hébergeur (LCEN art. 6-III) ; pied de message : dénomination, adresse postale, lien de désinscription. | V0 (Axion) / V1 (clients) | 0,5 |
| D4 | **Politique d'usage acceptable** | Usages permis (prospection B2B conforme, information) ; interdits (particuliers, fichiers achetés/loués sans preuve, pays fermés, données sensibles, contenus trompeurs, usurpation, pièces jointes, raccourcisseurs) ; seuils (plaintes 0,3 % / 7 j → pause, Spamhaus → pause, rebonds) ; contrôle d'entrée (SIREN, échantillon de fichier) ; suspension sans préavis en cas d'abus ; coopération en cas de plainte ; réparation. | V1 (avant 1er client) | 1 |
| D5 | **CGU/CGV du module** | Parties, objet (CRM de base + option envoi) ; abonnement et volumes remis à zéro à la date anniversaire (le dépassement informe, ne bloque pas) ; prix HT, acompte, engagement 12 mois, impayés (relance puis suspension) ; obligations du client (art. 14 à son nom, base légale) ; propriété (code, données du client) ; disponibilité (renvoi D7) ; responsabilité et plafond (§ 5) ; suspension ; fin de contrat (renvoi DPA) ; loi française, tribunal. | V1 | 2 |
| D6 | **Contrat de sous-traitance** | Trame § 2.2, annexes : sécurité art. 32, sous-traitants, fiche fin de contrat, modèle d'AIPD. | V1 (avant 1er client) | 2 |
| D7 | **Engagement de service** | Disponibilité cible (sans promesse de délivrabilité ni de réponses), RPO/RTO par client (aligner sur 1 h / 4 h de la console, 06 C10), heures et canal de support, délais de réponse, information en cas d'incident, maintenance annoncée ; pas de pénalités en V1 (avoirs plafonnés si Will veut). | V1 | 1 |
| D8 | **Notice RGPD du CRM** | Pour les utilisateurs du client et pour Axion : rôles (§ 2.1), données de compte et de sécurité, journaux, cookies strictement nécessaires, sous-traitants, transferts, durées, droits, contact. | V1 | 1 |
| D9 | **Procédure de violation de données** | Détection et escalade (qui, en combien de temps) ; qualification du risque (grille CNIL/CEPD) ; décision notifier / ne pas notifier **écrite** ; notification CNIL sous 72 h (téléservice), avec motif du retard si au-delà ; information des personnes si risque élevé (art. 34) ; information des clients sous 24-48 h (rôle de sous-traitant) ; registre des violations (art. 33.5) ; retour d'expérience. **Appliquer d'abord au 19/08** (Q3). | V0 | 1 |
| D10 | **Registre art. 30** (responsable + sous-traitant) | § 2.4. | V0 | 1,5 |
| D11 | **LIA par flux** (organisateurs, fédérations, presse, pharmacies) | Intérêt poursuivi, nécessité, mise en balance (attentes raisonnables d'un professionnel, lien avec la fonction, opposition simple, pas de pixel), garanties. | V0 (flux organisateurs) | 1 |
| D12 | **AIPD Axion** + modèle client | § 2.7. | V0 (court) / V1 (complet) | 2 |
| D13 | **Contrat de mise à disposition de base sectorielle** (si Q6 = oui) | Finalité, durée = abonnement, interdits (revente, enrichissement hors périmètre), opposition remontée à Axion sous 48 h, retrait en fin d'abonnement, traçabilité. | V1/V2 | 1,5 |
| D14 | **Fiches pays** (BE, CH, CA) | Règle, exceptions, preuve exigée, garde à ouvrir. | V2 | 1 |

Total documents : **≈ 18,5 jours-agent** de rédaction (+ relecture Opus et validation de Will).

---

## 4. Contenu des messages : règles à coder dans le contrôleur

### 4.1 Règles bloquantes (le message ne peut pas être validé)
| Règle | Source | Contrôle |
|---|---|---|
| `From` = nom d'une personne réelle + entité ; domaine du registre ; jamais `axion-ia.com` | L.34-5 al. 4 ; G1 ; RES-039 | registre des boîtes, accord écrit de la personne |
| Pied légal : dénomination, adresse postale, lien de désinscription | L.34-5 ; LCEN art. 20 | présence et non-vide |
| Bloc art. 14 pour tout non-informé | art. 14 ; G11 | présence, version validée |
| Lien de désinscription visible + en-têtes RFC 8058 signés | L.34-5 ; Gmail/Yahoo | présence, DKIM `h=` |
| Objet non trompeur : pas de faux « RE: », « TR: », « Fwd: » sans fil réel ; pas de « suite à notre échange / appel » sans trace d'échange dans le CRM ; pas de fausse urgence ni de faux suivi de commande | LCEN art. 20 ; pratiques commerciales trompeuses (Code conso L.121-2, applicable aussi entre professionnels pour partie) | liste de motifs + présence d'un fil de réponse réel |
| Message identifiable comme commercial dès sa réception | LCEN art. 20 | l'objet ou les premières lignes nomment l'entité |
| Angle lié à la fonction du destinataire | doctrine CNIL B2B | champ « angle métier » rempli et validé |
| Pas de pixel, de lien réécrit, de raccourcisseur, de pièce jointe, de téléphone | G5 ; décision Will | existant (03 § 2.3) |
| Pas de lien vers `axion-ia.com` dans un message à froid | 06 C2 | domaine principal interdit dans le corps |
| Lien ou gabarit du questionnaire jamais dans une séquence automatique | ordre de Will du 24/10 (06 M9) | garde C-G18 |

### 4.2 Interdits de Will (blocage dur, insensible à la casse et aux accents, y compris dans l'objet, la signature, le texte alternatif et les pages publiques)
- « Grenoble » (et variantes : « grenoblois », « Isère » à faire confirmer par Will).
- « certifié », « certifiée », « certification », « Qualiopi », « agréé », « labellisé », « accrédité » (les trois derniers par prudence : promesse d'un statut non détenu).
- « faites-le vous-même », « on s'occupe de tout » (interdits cités en 06 B4).

### 4.3 Formulations à bloquer ou à faire relire (avertissement, validation explicite de Will)
- Promesses chiffrées non prouvées : « garanti », « 100 % », « x10 », « doublez votre chiffre », « résultats assurés ».
- « gratuit » ou « offert » sans conditions écrites dans le message.
- Fausse rareté : « dernières places », « offre valable aujourd'hui seulement ».
- Fausse familiarité : « comme convenu », « vous m'avez demandé », « votre dossier ».
- Usurpation ou caution : noms de l'État, de la CNIL, de la CPAM, d'un ordre professionnel, logos de tiers, « partenaire officiel ».
- Santé (pharmacies) : aucune allégation sur des patients, des soins ou des médicaments ; aucune donnée de santé dans un champ variable.
- Variables : uniquement la liste blanche ; refus si une variable donnerait une information personnelle non professionnelle.

---

## 5. Assurance et responsabilité si un client abuse

- **Exposition** : (a) blocage du port 25 ou fermeture du compte d'hébergement d'Axion (préjudice commercial) ; (b) plaintes de destinataires ou contrôle CNIL/DGCCRF visant Axion comme sous-traitant (art. 82 : le sous-traitant répond s'il a manqué à ses obligations propres ou agi hors instructions) ; (c) réputation des IP/domaines partagés ; (d) atteinte à la marque Axion. Certitude : **moyenne**.
- **Mesures contractuelles** (D4, D5, D6) : le client garantit la licéité de ses fichiers et de ses messages et **indemnise** Axion des conséquences de son manquement ; plafond de responsabilité d'Axion (ex. montants payés sur 12 mois, sauf faute lourde ou dolosive, non limitables en droit français) ; droit de suspension immédiate ; coopération obligatoire en cas d'enquête.
- **Mesures techniques** déjà dans le plan : IP et domaines dédiés par client, pause auto à 0,3 % de plaintes ou listage Spamhaus, plafonds, arrêt de plateforme. **À ajouter** : contrôle d'entrée (SIREN actif, activité réelle, échantillon de fichier relu, refus des fichiers achetés) ; serveur d'envoi sur le compte d'hébergement **du client** quand c'est possible (05 D-C6) : une plainte ne touche que lui.
- **Assurance** : RC professionnelle couvrant l'activité de **sous-traitant de données et d'hébergement d'envois** + assurance cyber (frais de gestion de violation, perte d'exploitation, réclamations de tiers). Les **amendes administratives** CNIL ne sont en principe pas assurables en France (certitude moyenne). Action de Will : demander un devis en décrivant exactement l'activité (envoi de prospection pour le compte de clients), sinon l'assureur pourra refuser la garantie.

---

## 6. Tableau des corrections : effort, priorité, décision

Effort en jours-agent (code + rédaction), estimations d'agent, certitude faible à moyenne. V0 = avant le premier envoi réel d'Axion ; V1 = avant le premier client ; V2 = plus tard.

| Code | Correction du plan | Effort | Prio | Décision de Will ? |
|---|---|---|---|---|
| C-01 | Entité expéditrice D-07 + champs entité exigés | 0 (décision) | V0 | **Q1** |
| C-02 | D1 texte art. 14 (2 niveaux) + variante « information pure » | 1,5 | V0 | valide le texte |
| C-03 | Lot septembre : information dédiée avant prospection (voie A) | 0,5 | V0 | **Q2** |
| C-04 | Violation du 19/08 : notifier avec motif du retard ou motif écrit de non-notification ; D9 procédure | 1 | V0 | **Q3** |
| C-05 | Pages publiques `go.` (désinscription + pourquoi ce message), hors `axion-ia.com` | inclus E7 + 0,5 | V0 | non |
| C-G13 | Garde pays hors France = refus | 1 | V0 | **Q4** |
| C-G14 | Garde Sirene diffusion partielle = jamais contactable (sans suppression), avant d'éteindre la purge | 1 | V0 | non (conforme à ses ordres) |
| C-G15 | Garde art. 14 : alerte J+21, refus J+30 sans info | 1 | V0 | non |
| C-G16 | Garde webmail grand public = refus en froid | 0,5 | V0 | non |
| C-G17 | Hors éligibilité après 3 ans sans échange (aucune suppression) | 0,5 | V1 | valide la formulation § 1.10 |
| C-G18 | Garde questionnaire jamais automatique | 0,5 | V0 | non |
| C-06 | Contrôleur de contenu : règles § 4.1, interdits § 4.2, avertissements § 4.3, champ « angle métier », SEC-011 en V0 | 2,5 | V0 | valide la liste § 4.2-4.3 |
| C-07 | STOP élargi, opposition d'abord ; opposition téléphone | 1 | V0 | non |
| C-08 | `workspace_id` sur oppositions (en tenant compte de `scope`) ; « l'opposition gagne partout » dans l'espace Axion | inclus E1 | V0 | non |
| C-09 | Registre art. 30 + LIA organisateurs + AIPD courte | 3,5 | V0 | valide |
| C-10 | Exception art. 17 écrite + empreinte d'opposition gardée | 0,5 | V0 | non (06 M2) |
| C-11 | Tableau des tiers : DPA signés, lieu, transferts, mention art. 14 | 1 | V0 | non |
| C-12 | Domaine d'envoi et page `go.` gardés ≥ 3 ans après dernier envoi ; renouvellement auto | 0,5 | V1 | **Q7** |
| C-13 | DPA (D6) + fin de contrat § 2.3 + modèle d'AIPD client | 3 | V1 | **Q5** |
| C-14 | CGU/CGV (D5), usage acceptable (D4), engagement de service (D7), notice CRM (D8), mentions clients (D3) | 5,5 | V1 | valide |
| C-15 | Contrôle d'entrée client (KYC) et case « base légale » à l'import | 2 | V1 | non |
| C-16 | Qualification « base sectorielle fournie » + D13 + art. 14 de transmission + traçabilité | 3 | V1/V2 | **Q6** |
| C-17 | Pas d'usage des données client par Axion (pas de liste de plateforme, pas d'entraînement IA) | 0,5 | V1 | confirme (Q8) |
| C-18 | Assurance RC pro + cyber | 0 (achat) | V1 | **Q9** |
| C-19 | Fiches pays BE/CH/CA | 1 | V2 | plus tard |
| C-20 | Fiche source/licence FINESS, RPPS avant ouverture santé | 0,5 | V1 | non |

**Total conformité** : ≈ **V0 18 jours-agent**, **V1 15 jours-agent**, **V2 1 jour-agent**, soit ≈ 34 jours-agent, dont une partie recouvre E7, E9 et E13 du fichier 03 (E13 n'y comptait que 4 jours de code « + textes de Will » : sous-estimé d'environ 10 jours).

---

## 7. Questions à Will (une réponse courte suffit ; ma recommandation entre crochets)

1. **Entité expéditrice** : la SAS française ou l'OÜ estonienne ? [SAS française : même droit que les destinataires, CNIL autorité unique, mentions plus simples.]
2. **Organisateurs collectés les 26-27/09** : leur envoyer d'abord un message d'information sans offre, puis attendre 10 jours ouvrés avant toute prospection ? [Oui, voie A.]
3. **Fuite du 19/08** : notifier la CNIL maintenant en expliquant le retard, ou écrire un motif de non-notification (risque improbable pour les personnes) ? [Relire le brouillon : si des données de personnes ont pu être lues par un tiers, notifier maintenant ; sinon écrire le motif. Dans les deux cas, l'inscrire au registre des violations.]
4. **Pays** : prospecter seulement en France pour l'instant ? [Oui.]
5. **Fin de contrat d'un client du CRM** : le client choisit « restituer et supprimer » ou « restituer et conserver » ; sans réponse, gel chiffré puis proposition de suppression à 24 mois et votre clic. D'accord pour qu'Axion exécute une suppression quand c'est le client qui l'ordonne par écrit ? [Oui : c'est obligatoire (art. 28.3.g) et ce n'est pas une suppression décidée par Axion.]
6. **Base pharmacies pour Oury** : Axion la fournit-il au client ? [Si oui : traiter comme produit distinct avec son contrat et un message d'information aux pharmaciens avant la première transmission.]
7. **Désinscription d'un client parti** : garder son domaine d'envoi et sa page de désinscription 3 ans ? [Oui, 3 ans, renouvellement automatique.]
8. **Données des clients** : confirmer qu'Axion ne s'en sert jamais pour lui-même (pas de liste commune, pas d'entraînement d'IA) ? [Oui : c'est ce qui garde Axion simple sous-traitant.]
9. **Assurance** : demander un devis RC pro + cyber décrivant « envoi de prospection pour le compte de clients » ? [Oui, avant le premier client.]
10. **Interdits** : ajouter à la liste bloquée « agréé », « labellisé », « accrédité », « garanti » ? [Oui pour les trois premiers ; « garanti » en avertissement.]

---

## Sources consultées le 01/11/2026 (et références de texte)
- CNIL, « La prospection commerciale par courrier électronique, SMS-MMS et automate d'appel » : https://www.cnil.fr/fr/la-prospection-commerciale-par-sms-mms ; « Les règles d'or de la prospection par courrier électronique » : https://www.cnil.fr/fr/node/84701
- Position CNIL sur l'opposition en démarchage électronique (résumé secondaire) : https://www.journaldunet.com/martech/1031788-la-position-de-la-cnil-sur-le-droit-d-opposition-applique-au-demarchage-electronique/
- Conseil d'État, 11 mars 2015, n° 368624 (commentaire) : https://larevue.squirepattonboggs.com/prospection-directe-par-voie-electronique-necessite-absolue-du-consentement-specifique-et-informe_a2657.html
- INSEE, statut de diffusion Sirene : https://www.insee.fr/fr/information/7456564 ; https://www.insee.fr/fr/information/6043016 ; Lettre Sirene open data n° 3 : https://www.insee.fr/fr/information/4127417
- Règles Gmail/Yahoo/Microsoft (sources secondaires, aucune règle officielle 2026 trouvée) : https://www.suped.com/email-deliverability/answers/what-are-the-one-click-unsubscribe-requirements-for-gmail-and-yahoo-and-how-do-they-relate-to-ca ; https://www.paved.com/blog/bulk-sending-requirements-update/ ; https://prospeo.io/s/google-email-sender-guidelines ; https://docs.inboxally.com/compliance-industry-updates/
- Textes (de mémoire, à vérifier sur Légifrance / EUR-Lex avant validation) : CPCE L.34-5 ; LCEN art. 6-III et 20 ; RGPD art. 5, 6.1.f, 14, 17, 21, 26, 28, 30, 32 à 36, 44 à 49 ; loi 78-17 art. 82 ; LCD suisse art. 3 al. 1 let. o ; LCAP (Canada) ; Code belge de droit économique art. XII.13 et AR du 4 avril 2003 ; Code de commerce L.123-22 et A123-96 ; lignes directrices du CEPD sur la transparence (WP260 rév.01) et sur les AIPD (WP248).
- Certitudes à reprendre : RPPS/Annuaire Santé (réutilisation commerciale) faible ; Belgique moyenne ; règles 2026 des messageries moyenne (pas de source officielle lue).

---

## Résumé (20 lignes)
1. Le plan est bon sur l'opposition (porte unique, retrait en 5 min), la désinscription RFC 8058 et l'absence de pixel : conforme et au-dessus des règles Gmail/Yahoo/Microsoft.
2. BLOQUE le premier envoi : entité expéditrice non choisie (SAS ou OÜ) et texte art. 14 non écrit.
3. BLOQUE : lot des 26-27/09 hors délai art. 14 (un mois dépassé vers le 27/10) : information pure d'abord.
4. BLOQUE (prudence) : fuite du 19/08 sans notification CNIL ni motif écrit ; le brouillon n'est pas envoyé.
5. BLOQUE : pages publiques de désinscription et « pourquoi ce message » sous le domaine d'envoi, jamais `axion-ia.com`.
6. BLOQUE : aucune garde pays ; Suisse et Canada exigent un consentement même en B2B, Belgique aussi pour les adresses nominatives.
7. BLOQUE : aucune garde Sirene « diffusion partielle » ni « webmail = particulier » ; à coder avant d'éteindre la purge.
8. BLOQUE : registre art. 30, analyse d'intérêt légitime et AIPD courte du flux organisateurs.
9. Conservation « illimitée » : risque signalé sans rouvrir la décision ; formulation par critères (3 ans sans échange = non contactable, rien supprimé).
10. L'effacement art. 17 doit être écrit comme exception ; l'empreinte d'opposition est toujours gardée.
11. Multi-client : Axion sous-traitant si le client importe ses fichiers ; responsable de traitement s'il fournit la base pharmacies (contrat et art. 14 propres).
12. Fin de contrat : la suppression ordonnée par le client n'est pas une suppression décidée par Axion ; à accepter par Will (art. 28.3.g).
13. Aucune liste commune ni entraînement IA sur les données client, sinon risque de co-responsabilité.
14. 14 documents planifiés (≈ 18,5 j-agent de rédaction), dont 7 en V0.
15. Contrôleur de contenu : identité, adresse, désinscription, objet non trompeur, angle métier, interdits « Grenoble », « certifié », « Qualiopi ».
16. Client abusif : indemnisation, plafond, suspension, KYC, IP dédiée, assurance RC pro + cyber (amendes non assurables).
17. Effort conformité ≈ 34 j-agent (V0 18, V1 15, V2 1) ; E13 du fichier 03 était sous-estimé d'environ 10 jours.
18. 10 questions simples à Will avec recommandations (§ 7).
19. Certitudes faibles : RPPS, Belgique, règles messageries 2026 ; textes à relire sur Légifrance avant validation.
20. Rien n'a été envoyé, aucun serveur touché, aucune donnée supprimée.
