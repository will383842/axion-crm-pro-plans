# 03 : Module d'envoi du CRM Pro, démarrage petit puis montée (30/10/2026)

Rédigé par le responsable « module d'envoi » en lecture seule. Aucun e-mail envoyé, aucun accès serveur, rien de codé. Aucun secret ni contenu de licence n'est recopié.

**Sources lues** :
- le cahier `_PLAN-ENVOI-EMAILING-CRM-PRO-2026-09-28\04-final\` (`REGISTRE-REQ.csv`, 502 REQ) ;
- l'audit `_AUDIT-CRM-PRO-ENVOI-MASSE-2026-10-30\ZONE-4-envoi-en-masse.md` et `ZONE-5-delivrabilite-conformite.md` ;
- la reprise SOS-Expat `_AUDIT-SOS-EXPAT-REPRISE-2026-10-30\` (00, A, B, C, I) ;
- la sauvegarde Backlink Engine `VS_CODE\Sauvegardes\Sauv_backlink_engine\2026-10-17_03-00-02\code\` (pages `MailboxMonitor`, `Deliverability`, `Mailboxes`, `VpsHealth`, `Campaigns`, `PressCampaign`, `Suppression` ; services `warmupScheduler.ts`, `pressWarmup.ts`, `domainHealthMonitor.ts`, `pressHealthMonitor.ts`) ;
- le code `Axion-CRM-Pro\backend\app\Crm\Campagnes\*`, `Crm\Listes\*`, `Support\ListeSuppression.php`, `Support\EligibiliteCampagne.php` ;
- les fichiers voisins `01-architecture-et-depot.md` et `02-ce-qui-manque-crm.md`.

**Exigences de Will intégrées (message du 30/10)** :
1. Le CRM est aussi déployé chez des clients, donc il est multi-locataire.
2. Les campagnes sont le cœur du besoin et sont spécifiées en entier.
3. Le périmètre fonctionnel est complet : « petit » ne concerne que les volumes.
4. Le serveur d'envoi reste remplaçable. Le risque de licence de KumoMTA est étudié par le concepteur dans `05-clients-licence-et-multi-locataire.md`.

> **Vocabulaire.** Ici, **V0 / V1 / V2** désignent les étapes du module :
> - **V0** : premier envoi sûr, de 20-50 à quelques centaines de messages par jour ;
> - **V1** : 1 000 à 2 000 par jour, toutes les fonctions du quotidien ;
> - **V2** : jusqu'à 5 000 par jour durables (D-28), plusieurs serveurs, confort.
>
> Ne pas confondre avec la colonne `priorite` du registre, où « V0 » veut dire « préalable avant le code » et « V1 » « avant le premier envoi ».

---

## 0. Principes qui gouvernent tout le module

1. **Une seule voie** (REQ-CAM-001, 003). Tout message passe par `App\Emailing\EnvoiAutorise`, sans aucun repli. Le fichier JSONL de `crm:campagne:destinataires` cesse d'être une voie d'envoi : il ne sert plus qu'à l'audit (défaut M1 de la zone 4).
2. **Échec fermé** (REQ-CHA-022). Quand un état n'est pas lisible, on n'envoie pas. Contre-exemple à ne pas reprendre : `domainHealthMonitor.ts` de Backlink Engine renvoie « aucun domaine malsain » en cas d'erreur, donc il échoue ouvert.
3. **La volonté et le fait restent séparés** (REQ-RET-003). L'opposition (`opt_out`) et la suppression technique (`email_suppressions`) sont deux tables, et un retour ne peut que retirer (RET-001).
4. **Aucune ouverture ni aucun clic par personne** (REQ-SEC-016). Les colonnes « Ouverts », « Clics » et « Taux ouverture » de Backlink Engine ne sont **pas** reprises.
5. **Pas de faux trafic** (REQ-CHA-035). Mailflow, Lemwarm et les réseaux de chauffe de Backlink Engine ne sont pas repris.
6. **Rien n'est jamais supprimé.** C'est un ordre permanent de Will : un retour retire une adresse d'une campagne, il n'efface jamais une fiche (RET-037).
7. **Multi-locataire dès la première ligne.** Chaque table porte `workspace_id UUID NOT NULL`, avec une RLS `ENABLE` + `FORCE` (REQ-CON-031). Le locataire n°1 est Axion-IA. Un client est un autre locataire.
8. **Serveur d'envoi remplaçable** (REQ-INF-029). Le CRM ne parle qu'au contrat `ServeurEnvoi` (§ 10). Aucun écran ne nomme le logiciel du serveur.

---

## 1. Multi-locataire : ce qui change quand le CRM est chez un client

### 1.1 Deux modes de déploiement, un seul code

| Mode | Description | Quand |
|---|---|---|
| **Mutualisé** | Une instance Axion, plusieurs espaces (`workspaces`). Le serveur d'envoi est partagé, mais **chaque locataire a son IP d'envoi, ses domaines et ses boîtes**. | Petits clients. Seulement après la preuve que la RLS est active (02-ce-qui-manque, M0/M1). |
| **Dédié** | Une instance par client (sa base, son serveur d'envoi). C'est le même code, avec un seul espace. | Recommandé par le fichier 02 tant que la RLS n'est pas prouvée. Obligatoire si le client veut ses propres serveurs. |

### 1.2 Ce qui est propre à chaque locataire (jamais partagé)

| Objet | Règle |
|---|---|
| Entité expéditrice | Raison sociale, forme, SIREN, adresse postale, contact RGPD, URL de sa page « prospection » art. 14 et durée de conservation annoncée. Ces champs sont exigés avant la première campagne : c'est une case du « feu vert ». |
| Domaines d'envoi | Ils appartiennent au locataire. La garde de nommage (§ 8) refuse `axion-ia.com`, tout domaine d'un autre locataire et, sauf case tracée, le domaine principal du client lui-même. |
| IP d'envoi | **Une IP dédiée par locataire en prospection à froid**. On ne mélange jamais deux réputations sur une même IP. Le serveur peut être partagé, l'IP ne l'est pas. |
| Boîtes expéditrices | Ce sont des personnes réelles du client, avec leur accord écrit (RES-039) et une signature sans téléphone (RES-040). |
| Quotas | Plafond journalier contractuel, plafond de vérification en € par mois, plafond de coût IA (champ existant `Workspace.cost_cap_eur`). Le plafond le plus bas s'applique. |
| Liste d'opposition | `opt_out` **par locataire**. Une désinscription chez le client X ne vaut que pour X. Aujourd'hui, `opt_out` et `email_suppressions` n'ont pas de `workspace_id` (02-ce-qui-manque, M1) : il faut une migration, qui est une tâche de V0. |
| Gabarits, séquences, segments | Ils sont propres au locataire. Les familles « ouvertes » se règlent par locataire, et toutes sont fermées par défaut. |
| Réputation et santé | Les scores, les disjoncteurs et la chauffe sont calculés par locataire. La portée « locataire » est ajoutée aux portées de disjoncteur de REQ-CHA-044. |
| Droits | Rôles par espace : `owner` du client, membres, lecteurs. L'accès « support Axion » est limité dans le temps et tracé (02, M2). |
| Journal | `audit_logs` et `business_events` sont filtrés par espace. Le journal plateforme d'Axion est séparé. |

### 1.3 Ce qui est commun à la plateforme (côté Axion, l'opérateur)

- **Arrêt d'urgence de plateforme.** Axion peut couper un locataire ou tout le serveur. Le client voit le motif.
- **Politique d'usage acceptable** (clause du contrat). Un locataire dont les plaintes dépassent 0,3 % sur 7 jours, ou qui est listé chez Spamhaus, est **mis en pause automatiquement**, parce que le serveur et la sonde sont partagés.
- **Liste de protection de plateforme** (proposition, **à valider par Will**, faute de juriste). Elle ne contiendrait que des empreintes de faits techniques (rebond dur réel, piège à spam suspecté), jamais des oppositions. Le but est de protéger l'infrastructure commune. En mode dédié, cette liste n'existe pas. Partager des faits entre responsables de traitement reste un point de droit ouvert. **Option sûre par défaut : la liste n'est pas partagée.**
- **Les données d'Axion ne vont jamais chez un client** : base INSEE, presse, oppositions d'Axion (02, M1). Fournir des contacts à un client serait un autre traitement, hors de ce module.

### 1.4 Quand l'expéditeur est le client

| Sujet | Axion expéditeur | Client expéditeur |
|---|---|---|
| Responsable de traitement | Axion (entité D-07 : SAS ou OÜ) | **Le client**. Axion est sous-traitant (art. 28) : un DPA est signé, et les sous-traitants ultérieurs d'Axion (hébergeur, vérificateur, boîtes) sont listés. |
| Bloc art. 14 (`{bloc_information}`) | Texte d'Axion | Texte **du client** : son identité, sa finalité, la source réelle de l'adresse, sa durée, ses droits, la CNIL. Le CRM refuse la validation tant que ce texte n'est pas rempli et validé par l'`owner` du client. |
| Pied du message | Raison sociale et adresse d'Axion | Celles du client (LCEN art. 20, L.34-5 al. 4 : pas d'identité dissimulée) |
| Désinscription | `go.<domaine Axion>/d/{jeton}` : « Ne plus recevoir de messages d'Axion-IA » | `go.<domaine du client>/d/{jeton}` : « Ne plus recevoir de messages de <Client> ». La page est à son nom, et l'opposition s'inscrit **dans son espace**. |
| Racine du domaine d'envoi | Redirection 301 vers une page d'`axion-ia.com` (RES-020) | Redirection 301 vers le site du client |
| Plaintes et rebonds | Ils sont appliqués dans l'espace Axion. | Ils sont appliqués dans l'espace du client. Les compteurs de plateforme sont agrégés et anonymes. |
| Demandes de droits | `contact@` / `dpo@` d'Axion | Celles du client. Axion les lui transmet sous 48 h s'il les reçoit (clause du DPA). |

---

## 2. Module « Campagnes » (le cœur), spécification complète

### 2.1 Réutilisé tel quel ou étendu (déjà dans le CRM Pro)

| Brique | Fichier | Rôle dans le module |
|---|---|---|
| Résolveur de destinataires | `Crm/Campagnes/ResolveurDestinataires.php` | Dédoublonne par adresse et lit les canaux typés `signals.contact_channels` (CAM-082). Il est enveloppé par `EnvoiAutorise`. |
| Éligibilité | `Crm/Campagnes/EligibiliteAdresse.php` (13 motifs fermés), `Support/EligibiliteCampagne::peutRecevoir` | C'est la porte de l'opposition. Elle est appelée **à la construction de la vague ET moins de 15 minutes avant chaque tranche**. |
| Presse | `GardePresse.php`, `AdressePresseFiable.php` | La presse n'entre que par son segment, avec un contrôle de provenance. |
| Clients de la console | `GardeConsoleClient.php` | Un client de la console n'est jamais destinataire. |
| Listes manuelles, import | `Crm/Listes/ListesManuelles.php`, `ImportListe.php` | Listes statiques. |
| Préparation | `crm:campagne:destinataires` | Elle devient un **aperçu** et un export d'audit. Elle n'envoie toujours rien. |
| Réglage par fonction | `ReglageDestinataires.php` | Critère « fonction » (CAM-079). |

### 2.2 Ciblage (multi-étiquettes et listes)

- **Sources combinables** dans une même campagne : familles ouvertes, audiences enregistrées (DSL), listes manuelles et étiquettes, en ET / OU / SAUF avec `contains_any`, `contains_all`, `contains_none` et des groupes imbriqués sur 3 niveaux (CAM-008).
- **Critères** (CAM-007, 079, 083) :
  - entreprise : relation, étape, nature, région, secteur, taille ;
  - personne : fonction, nommée ou générique ;
  - adresse : verdict, informée ou non, origine ;
  - événement : « a un événement à venir », par `EvenementAVenir`.
- **Exclusions par historique** (CAM-080) : contacté depuis N jours, déjà ciblé par la campagne X, démarche en cours, client, RDV pris.
- **Exclusions manuelles par campagne** : une adresse, une organisation, un domaine destinataire. Registre V2 (CAM-012), **remontée en V1** parce que Will veut des campagnes complètes.
- **Segment dynamique ou figé** (CAM-081). Un segment figé est un instantané tracé (date, auteur, nombre).
- **Audience = photo** (CAM-010). La campagne recalcule ses critères à chaque vague, puis repasse **toujours** par `peutRecevoir`.
- **Aperçu en direct** (CAM-011) : éligibles, exclus par motif en toutes lettres, et 3 messages rendus en échantillon.
- **Garde-fous** : écosystème jamais prospecté (CAM-015), webmails jamais (CAM-016), dédoublonnage avec la lettre (CAM-017), adresse partagée = un seul destinataire (CAM-018), syndicats exclus sauf case tracée (CAM-078).
- **Pression commerciale unique** (CAM-014, 067) : au plus 1 message par 5 jours ouvrés, 4 par 60 jours, 2 séquences et 6 messages par 12 mois, 2 adresses par organisation et par vague.
- **Multi-locataire** : la pression se compte par locataire. CAM-013 (« une seule séquence active par adresse, tous espaces confondus ») est ramené **au locataire**. Sinon un client verrait l'activité d'un autre : c'est une fuite.

### 2.3 Gabarits, variables, personnalisation

- **Modèle versionné** (CAM-023) : objet, pré-en-tête facultatif, **texte brut obligatoire**, HTML minimal facultatif (`p`, `br`, `ul`, `li`, `a`, `strong`), jamais de téléphone.
- **Variables en liste blanche avec repli** (CAM-024) :
  - `{prenom}`, `{nom}`, `{formule_appel}` (civilité jamais devinée), `{fonction}`, `{organisation}` ;
  - `{evenement}`, `{ville}`, `{expediteur_*}` ;
  - `{bloc_information}` (art. 14, exigé pour un non-informé, SEC-015) ;
  - `{lien_desinscription}`.
  - Rendu par un moteur **sans exécution de code**. Contre-exemple de SOS-Expat : Jinja2 sans bac à sable (rapport A).
- **Contrôleur de contenu** unique, qui bloque ou avertit (CAM-027). Il rend le message sur 3 destinataires d'échantillon.
  - Il bloque : variable inconnue ou vide sans repli, objet hors limites, lien vers un domaine listé, `axion-ia.com` en lien de suivi, pixel, raccourcisseur, pièce jointe, bloc art. 14 absent pour un non-informé, pied légal absent, entité du locataire absente.
  - Il avertit : longueur, majuscules, mots à risque.
- **Variantes** d'objet (1 à 4) et de corps (1 à 3) avec poids (CAM-025). Elles personnalisent, elles ne trompent jamais. Une variante est retirée automatiquement après 2 plaintes ou un pic de rebonds (CAM-032).
- **Micro-variations bornées** `{a|b|c}` (CAM-026) : V2.
- **Accroche par IA, encadrée** (CAM-028, 030) : V2. Elle est soumise à un plafond de coût et validée avant envoi. Will a une règle : « jamais faites-le vous-même ».
- **Gabarits multilingues avec repli français** (idée de partner-engine) : non retenus, car Will a décidé « français uniquement » (CAM-074 retirée).
- **Aperçu fidèle et envoi test obligatoire** (CAM-034). L'aperçu se fait dans une `iframe` sans script et montre les en-têtes (`From`, `Reply-To`, `List-Unsubscribe`). L'envoi test va à Will et aux boîtes témoins, **par la même porte**.
- **Traçabilité** (CAM-033). Chaque message garde la version du modèle, la variante et la combinaison utilisées.

### 2.4 Séquences et relances

- **1 à 4 étapes en jours ouvrés** (CAM-035). Défaut organisateurs : J0, J+7, J+14. Défaut presse, repris de Backlink Engine : J0, J+5, J+10.
- **Arrêt immédiat par adresse** (CAM-036, 038) sur :
  - toute réponse humaine, un rebond dur, le 3e rebond mou ;
  - une désinscription, un STOP, une plainte ;
  - un RDV pris (02, G4), le passage en « client » ;
  - le geste « J'ai répondu ailleurs ».
- **Absence du bureau** : la séquence est mise en pause, pas arrêtée (CAM-037). Registre V2, **remontée en V1** : sans elle, une relance tombe pendant les vacances.
- **Relance d'une boîte indisponible** (CHA-068) : on attend 3 jours ouvrés, puis on annule.
- **Règles de passage entre campagnes** (demande de Will du 30/09, `NOTE-SCENARIOS-CONDITIONNELS-2026-09-30.md`) : V1, **à inscrire au registre** (ce n'est pas encore fait).

### 2.5 Planification, budget et file

- **Dates** (CAM-041) : début (au plus tôt le jour ouvré qui suit la validation), fin des premiers messages, fin.
- **Fenêtres nommées** (CHA-027) en heure de Paris, jours ouvrés, fériés exclus.
- **Construction des vagues chaque matin à 07:10** (CAM-039). La vague est découpée en **tranches horodatées** et étalée avec un décalage aléatoire de ± 2 minutes (idée de `pressWarmup.ts`).
- **Plusieurs campagnes en parallèle** (CAM-019) et **arbitrage du budget du jour** (CAM-020) : les relances dues passent d'abord, puis les premiers messages par priorité.
- **Plafond propre à la campagne** (CAM-021).
- **Prévision honnête** (CAM-022, V1) : « fin des premiers messages le JJ/MM ».
- **Report plutôt qu'échec** (CHA-030).
- **File atomique** : patron `ProcessEmailQueueJob` de Mission Control, avec `lockForUpdate` et `SKIP LOCKED` sous Postgres.
- **Affectation de l'expéditeur pondérée et collante** (CHA-033) : un destinataire garde sa boîte pour toute la séquence.

### 2.6 Validation, pause, arrêt

- **Cycle de vie** (CAM-042) : `brouillon` → `a_valider` → `validee` → `planifiee` → `en_cours` ⇄ `en_pause` → `terminee` | `annulee`.
  - La **validation est attachée à l'empreinte de la version**. Toute modification fait repasser la campagne en `a_valider`.
- **Qui valide** (CAM-043) : l'`owner` de l'espace, donc Will pour Axion et l'`owner` du client chez un client.
- **Mode « revue » par défaut** (idée de `outreachMode.ts`). L'option « validation message par message » (CAM-044) est remontée en V1 pour la presse.
- **Feu vert** (SEC-019) : une seule fonction, `ControleAvantEnvoi::evaluer()`. Elle est recalculée à la validation, au lancement et à chaque reprise. Elle reprend les 31 cases de la zone 5 § 5.
- **Pause, reprise, annulation** (CAM-040).
  - Pause : aucune nouvelle vague, les tranches non injectées sont retirées et `ServeurEnvoi.retirer()` est appelé pour les messages en attente au serveur.
  - Reprise : jamais au débit d'avant (CHA-021).
- **Retrait immédiat** (CAM-048). Toute nouvelle opposition ou suppression retire en moins de 5 minutes les messages en attente (file `emailing-urgent`).
- **Délai d'annulation de 5 minutes** avant une vague de plus de 500 destinataires (CAM-045) : V1.

### 2.7 Tests A/B

- **V1** (CAM-031, registre V2, remonté parce que Will le demande). On compare 2 à 4 variantes d'**un seul** élément.
- **Métrique principale : réponses positives classées.** Il n'y a pas d'ouvertures (pixel interdit).
- **Arrêt du perdant** au-delà d'un échantillon minimal (300 livrés par variante), avec la mention « pas assez de données » en dessous.
- L'écran reprend la forme de `AbTestResults.tsx` de Backlink Engine, **sans** les colonnes d'ouverture.

### 2.8 Réponses

- **Relève IMAP de chaque boîte toutes les 5 minutes** (RES-041).
- **Rattachement** par le jeton dans `In-Reply-To` / `References` (CAM-050).
- **Classement** (CAM-051) : des règles d'abord (réponse automatique, absence, STOP, plainte verbale), un classement manuel toujours possible, l'IA en V2.
  - Le prompt INTERESTED / NOT_INTERESTED de Backlink Engine sert de base pour la V2.
- **File « Réponses »** (CAM-053). Les actions se font en un clic (CAM-052) et l'opposition est immédiate.
- **Répondre depuis la console par la même porte** (CAM-054) : V1.
- **Fiche 360°** (CAM-057) : `email_sent`, `email_replied`, `email_bounced`… sans doublon.
- **Tâches issues des réponses** (CAM-058) : V1.

### 2.9 Campagnes presse et médias

- **Nature `presse`**, distincte de la prospection.
- **Entrée** : uniquement par le segment presse et l'audience presse (`GardePresse`), avec la provenance jugée par `AdressePresseFiable`.
- **Champs propres** : angle, communiqué joint **par lien** (jamais en pièce jointe), média, rubrique.
- **Boîtes** `presse@<domaine d'envoi>` dédiées, sur un pool à part : la réputation presse est séparée.
- **Relances** J+5 et J+10 au plus. Arrêt sur réponse.
- **Art. 14 et opposition** s'appliquent aux journalistes nommés (zone 5, cibles sensibles). Une désinscription presse vaut opposition dans **tous** les univers du locataire.
- **Décision à aligner** : le cahier dit « presse fermée » (CAM-064), le code l'a ouverte le 01/10. La décision de Will du 01/10 prime. Le registre doit être corrigé.
- **Repris de `PressCampaign.tsx`** : colonnes Média / Angle / Statut / Mise à jour, bouton « Lancer », répartition, pause et reprise globales. **Non repris** : colonnes DR et langue, 5 domaines SOS-Expat en dur, envoi sans validation.

### 2.10 Statistiques de campagne

- **Indicateurs uniques** (CON-028) : envoyés, livrés, reports, rebonds durs et mous, blocages, plaintes, désinscriptions, réponses par nature, réponses positives, RDV attribués (CAM-068).
- **Deux lectures** (CON-055) : par date d'envoi et par date d'événement.
- **Entrepôt horaire sans donnée personnelle** (CON-054, SEC-036).
- **Suivi par groupe ciblé et par étiquette** (CON-060) : V1.
- **Attribution du chiffre d'affaires** (CAM-066, 069) : V2.

---

## 3. Chauffe progressive par domaine, IP et boîte

### 3.1 Courbe « démarrage petit » (proposée, réglable)

La courbe est en **jours effectifs**, au sens de CHA-005 : un jour d'envoi réel d'au moins 50 % du budget. **Un jour sans envoi ne compte pas.** Backlink Engine faisait déjà ce bon réflexe. SOS-Expat comptait aussi les jours sans envoi, ce qui est un défaut.

| Palier | Jours effectifs | Total/jour (flux froid) | Par boîte (CHA-037, AX-BOITE-2027) | Ressources nécessaires |
|---|---|---|---|---|
| P1 | 1-5 | **20** | ≤ 20 | 1 IP, 2 domaines, 2 boîtes |
| P2 | 6-10 | **35** | ≤ 30 | idem |
| P3 | 11-15 | **50** | ≤ 40 | idem, puis 4 boîtes |
| P4 | 16-20 | 80 | ≤ 50 | 1 IP, 2 domaines, 4 boîtes |
| P5 | 21-25 | 120 | ≤ 70 | idem |
| P6 | 26-30 | 180 | ≤ 110 | idem |
| P7 | 31-35 | 250 | ≤ 150 | idem (**fin de V0** : « quelques centaines ») |
| P8 | 36-40 | 350 | ≤ 150 | 1 IP, 2 domaines, 4 boîtes (plafond 600 par les boîtes) |
| P9 | 41-45 | 500 | ≤ 150 | 1 IP, 2 domaines, 6 boîtes (**début de V1**) |
| P10 | 46-50 | 700 | ≤ 150 | 1 IP, 2 domaines (750/domaine), 6 boîtes |
| P11 | 51-55 | 1 000 | ≤ 150 | **2e cohorte** : + 1 domaine, + 2 boîtes |
| P12 | 56-65 | 1 300 → 1 600 | ≤ 150 | **2e IP** au 1 500/IP (CHA-037) ; 3 domaines, 11 boîtes |
| P13 | 66+ | **2 000** (fin de V1) | ≤ 150 | 2 IP, 3-4 domaines, 14-16 boîtes |

Règles associées :
- **Budget effectif = min(IP, domaine, boîte)** (CHA-004). Le goulot est affiché.
- **Âge des domaines ≥ 21 jours avant P1** (RES-009, remontée en V0 : c'est une horloge que personne ne peut accélérer).
- **Inactivité** (CHA-006) : recul à 75 % après 7 jours ouvrés, 25 % après 30 jours, retour au départ après 90 jours.
- **Montée par cohortes espacées** (CHA-036) : 1 IP + 1-2 domaines + boîtes. On n'ajoute **jamais** de domaines pour contourner un listage : c'est le risque « snowshoe » de la zone 5.
- **Hausse le lendemain, baisse tout de suite** (CHA-060).
- **Multi-locataire** : chaque locataire a sa courbe sur son IP et ses domaines. Le plafond local du serveur (INF-023) est découpé par locataire.

### 3.2 Règles d'arrêt (seuils de SOS-Expat calés sur un petit volume)

Toutes les valeurs vivent dans **une seule table versionnée** `emailing_seuils` (CHA-013). Un taux n'est calculé qu'au-delà d'un échantillon minimal. En dessous, ce sont des règles absolues qui s'appliquent (CHA-014).

| Règle | Seuil (taux) | Échantillon minimal | Règle absolue sous l'échantillon | Effet |
|---|---|---|---|---|
| **Rebonds durs** | > **2 %** sur 7 jours glissants | 100 livrés + rebonds | ≥ 3 rebonds durs dans la journée sur une ressource | **Retour au palier précédent** de la ressource, puis on tient 3 jours effectifs verts avant de remonter (CHA-043 : une remontée par jour au plus). |
| Rebonds durs, pic | > 5 % sur 24 h | 50 | ≥ 5 dans la journée | Pause de la **campagne** (cause liste) et revérification de ses adresses (SEC-022). |
| **Plaintes authentifiées** (ARF, RET-017) | > **0,1 %** sur 7 jours | 1 000 livrés | **1 plainte** → on tient le palier 3 jours et Will relit ; **2 plaintes en 7 jours** → règle ci-contre | **Arrêt 48 h** du domaine (et des boîtes qui ont reçu les plaintes), puis reprise **au palier inférieur** (CHA-021). |
| Blocage de réputation (`5.7.1 … spamhaus`, `S3150`…) | Série au seuil de CHA-016 | — | 3 refus de réputation en 1 h vers un même groupe | Pause de l'IP **vers ce fournisseur seulement** (CHA-016). Aucune compensation vers lui (CHA-047). |
| **Engagement minimal** | voir ci-dessous | 300 livrés | — | Le palier est tenu, il ne recule pas. |
| Listage DNSBL d'une IP ou d'un domaine d'envoi | Spamhaus SBL/CSS/DBL | — | 1 listage | Pause de la ressource + runbook « IP ou domaine listé » (SEC-021). |
| Arrêt d'urgence automatique | 6 cas fermés de CHA-048 | — | — | Tout s'arrête. La levée demande `approve`. |

**Engagement « minimal 5 % » : décision à prendre par Will.**
- Le chiffre de SOS-Expat reposait sur les **ouvertures**. Le pixel est interdit ici, donc ce chiffre n'est pas mesurable.
- Proposition :
  - engagement = **réponses humaines (hors absence) / livrés** sur 14 jours glissants ;
  - **alerte** sous 1 % (on tient le palier) ;
  - **revue** sous 0,5 %, si en plus une boîte témoin reçoit le message en spam.
- Un taux de 5 % de réponses est irréaliste en prospection à froid. Le garder comme objectif affiché, pas comme seuil d'arrêt.

### 3.3 Machine d'états et disjoncteurs

- **États par ressource** (RES-001) : `nouveau`, `en_chauffe`, `actif`, `au_repos`, `en_quarantaine`, `retire`. **Chaque état a une sortie**.
  - Le bug « quarantaine sans sortie » de SOS-Expat (rapport A, bug 2) est couvert par un test.
- **Disjoncteurs** (CHA-017) :
  - en V0, les portées sont : global, locataire, IP, IP × fournisseur, domaine, boîte, campagne, variante ;
  - en V1, la liste complète des 13 portées (CHA-044) avec escalade, recherche de cause (CHA-045) et redistribution bornée (CHA-046).
- **Décision quotidienne à 07:00** (CHA-012), après le test de fumée de 06:45 (INF-050). Elle est motivée en une phrase dans le journal.
- **Évaluation toutes les 5 minutes** pendant la fenêtre d'envoi (CHA-018).
- **« Tout arrêter »** (CHA-019) : un bouton dans l'en-tête de chaque page et `emailing:couper --global`. L'arrêt est prouvé par son effet : plus aucun message n'est injecté.

---

## 4. Vérification des adresses avant envoi

- **Fournisseur tiers HTTPS, enfichable** (VER-012).
  - Jamais de sonde SMTP depuis une IP d'envoi ou depuis le CRM (VER-001).
  - Candidat immédiat : `Services/Email/HunterEmailVerifier.php`, qui existe déjà mais n'est pas branché.
  - Alternative européenne : un vérificateur hébergé dans l'UE.
  - Le DPA est obligatoire avant activation (VER-017).
- **Cascade locale d'abord** (VER-005, 006), avec l'existant `CrmEmailsVerifier` : syntaxe, jetables, MX, rôle. Ensuite seulement le fournisseur.
  - Une panne DNS n'est jamais « invalide », une erreur n'est jamais « valide ».
- **Verdicts fermés** (VER-002). Un verdict par adresse, écrit par un seul service (VER-003). Il ne supprime jamais rien (VER-004).
- **Règle de démarrage petit : un verdict `valide` de moins de 30 jours est exigé à l'injection.**
  - C'est la demande de Will, plus stricte que les 90 jours de VER-019. Le réglage se fait par locataire.
  - Pré-vol (VER-020) : avant chaque tranche, les adresses au verdict absent ou périmé sont revérifiées ou reportées, **jamais envoyées**.
- **Quotas dans chaque tranche** (VER-025) :
  - `accepte_tout` à 0 % tant que la ressource est en chauffe, puis ≤ 10 % ;
  - `inconnu` à 0 % (dérogation tracée en V2, VER-026).
- **Le rebond réel prime** (VER-027) : il force `invalide/rebond_reel`.
- **Estimation du coût avant un lot** (VER-015). Le plafond est en € par mois et par locataire.
- **Première passe réelle** : le segment `organisateurs-evenements` (VER-031).
- **Information** : l'art. 14 et la politique de confidentialité mentionnent la vérification par un prestataire (VER-030).

---

## 5. Désinscription en un clic, page publique, liste de suppression unique

- **En-têtes** (RET-010) :
  - exactement un `List-Unsubscribe: <https://go.<domaine d'envoi>/d/<jeton>>, <mailto:desinscription+<jeton>@bounce.<domaine>>` ;
  - `List-Unsubscribe-Post: List-Unsubscribe=One-Click` ;
  - les deux sont couverts par la signature DKIM (`h=`).
- **Route publique** `GET` et `POST /d/{jeton}` (RET-020), hors console et hors `/api/v1`, servie sous `go.<domaine d'envoi>`. **Jamais sous `axion-ia.com`** : le one-click du site (`axionia/src/app/api/unsubscribe`) reste réservé aux e-mails du site.
  - `POST` : réponse 200 sans confirmation, opposition écrite en moins d'une minute (RET-027).
  - `GET` : page « Vous ne recevrez plus de messages de <Entité> », avec un bouton facultatif « opposition pour toute mon organisation » (RET-026) et un lien « pourquoi ce message » vers la page art. 14 de l'entité.
  - Le test passe **par l'effet** : après le POST, `peutRecevoir()` renvoie faux, et un message en attente est retiré.
- **Jeton** : opaque, d'au moins 128 bits. Seule son empreinte est stockée (RET-007, 021). Patron « jeton signé » de `press/unsubscribeToken.ts`.
- **Variante `mailto:`** traitée dès la V0 (RET-023, registre V2, remontée), puisque l'en-tête l'annonce.
- **Lien visible dans le corps et pied qui dit pourquoi** (RET-022).
- **STOP par réponse = opposition** (RET-025).
- **Liste de suppression unique** (RET-028) : une seule porte, `peutRecevoir()` (opposition + suppression + suppression par domaine).
  - Écran unique : « Oppositions », § 7.5.
  - Propagation CRM ⇄ site par l'outbox existante (RET-029, 030).
  - **Multi-locataire** : la porte prend `workspace_id`. Les oppositions d'Axion ne filtrent pas les envois d'un client, et inversement, sauf la liste de protection de plateforme si Will la valide (§ 1.3).
- **Levée d'une suppression** : rare, motivée, tracée, **jamais** pour une plainte ni une opposition (RET-031).
  - Le bouton « Supprimer » de `Suppression.tsx` (Backlink Engine) n'est **pas** repris.
- **Correctifs de l'existant** :
  - compteur de rebonds mous en base (RET-013, défaut M2 de `ListeSuppression.php:165`) ;
  - table fantôme `unsubscribes` retirée de la portabilité (RET-040) ;
  - empreinte SHA-256 déclarée comme pseudonymisation.

---

## 6. Réception des événements (webhook idempotent, qui remplace le fichier manuel)

**Arbitrage d'architecture.** REQ-INF-017 dit « le CRM tire les retours, rien n'entre dans M1 ». La demande de Will et le fichier 01 parlent de webhook. Proposition, à acter par ADR :
- **Poussée** : le serveur d'envoi envoie un webhook **par le tunnel privé seulement** (WireGuard). L'écouteur est lié à l'IP privée de M1 et n'est jamais public.
- **Tirage de réconciliation** : chaque nuit, le CRM tire la comptabilité par curseur (RET-046, INF-055). Un événement manqué est donc rattrapé.

Contrat d'entrée :

| Point | Spécification |
|---|---|
| Transport | `POST /interne/envoi/evenements` sur l'IP privée de M1. Le corps est un tableau JSON de 1 à 500 événements. |
| Authentification | HMAC-SHA256 du corps brut + horodatage, dans l'**en-tête** (`X-Envoi-Signature: t=<unix>,v1=<hex>`). Jamais dans l'URL (défaut m2 du webhook ZeptoMail actuel). Un écart de plus de 5 minutes est refusé. Secret absent → **refus** : l'option « ouvert par défaut » de SOS-Expat (rapport A, bug 4) est interdite. Un secret par locataire et par serveur. |
| Idempotence | Clé unique `(source, event_id)` en base. Un doublon donne 200 sans effet. Clés de RET-006. |
| Durabilité | Écriture brute dans `emailing_retours` **avant** application (RET-005). La réponse 2xx ne part qu'après le `COMMIT`. Le serveur rejoue avec un délai croissant pendant 72 h. |
| Ordre | État final monotone par envoi : `plainte` > `rebond_dur` > `livre` > `report`. Un « livré » qui arrive après un rebond dur ne rétablit rien. Un « livré » remet à zéro le compteur de rebonds mous (RET-013). |
| Application | Un seul service, `AppliquerRetour` (RET-002) : rebond dur = suppression + `invalid` sur toutes les fiches (RET-015) ; 3e mou = suppression ; plainte = opposition dans tous les univers du locataire (RET-018) ; désinscription = `opt_out` ; livraison = `first_info_at` posé **à la livraison** (RET-036). |
| Classement des rebonds | Table `smtp_response_patterns` (CHA-025), amorcée avec la table de 2 785 motifs de SOS-Expat **après vérification de son origine** (licence inconnue, rapport A) et **testée sur de vrais journaux** du banc. Les règles de classement intégrées au serveur d'envoi priment. |
| Plaintes ARF | Boîte `fbl@bounce.<domaine>` relevée par IMAP et analysée selon RFC 5965 (RET-016). Seules les plaintes **authentifiées** comptent pour les seuils (RET-017). |
| Rebonds asynchrones | DSN sur `bounce.` via VERP `rb-<jeton>@bounce.<domaine>` (RET-009). V1 pour l'analyse fine (RET-014). |
| Santé du canal | Aucun événement depuis 2 h pendant une campagne → arrêt automatique (CHA-048, cas 5 ; RET-035). |
| Ancien chemin | `crm:campagne:retours` devient une **source** `import` du même service. La clé d'idempotence corrige le double comptage lors d'un ré-import (défaut M2). |
| Données personnelles | Les événements portent l'**empreinte** du destinataire, jamais l'adresse en clair (RET-042, SEC-008). |

---

## 7. Écrans de la console « Envois » (repris de Backlink Engine, adaptés)

La section **ENVOIS** est placée entre COLLECTE et PILOTAGE, avec 7 entrées au plus (CON-001) : **Accueil · Campagnes · Modèles · Réponses · Délivrabilité · Oppositions · Alertes**, plus un menu « Plus » : Presse, Santé serveur, Réglages, Mise en route.

Règles communes :
- les primitives du kit existant, sans émoji, avec les 4 feux mot + icône (CON-041) ;
- un seul bouton principal par écran (CON-042) ;
- le bouton **« Arrêt d'urgence »** dans l'en-tête de chaque page (CON-071) ;
- la source et l'âge de chaque mesure (CON-008) ;
- le locataire courant affiché dans l'en-tête.

### 7.0 Correspondance avec Backlink Engine

| Écran Backlink Engine | Écran CRM Pro | Repris | Écarté |
|---|---|---|---|
| `MailboxMonitor.tsx` | Délivrabilité › Boîtes (+ carte Chauffe de l'Accueil) | « Readiness pour campagnes », activité par boîte (aujourd'hui, 7 j), échecs 72 h / 7 j, section « Blacklists · IP » | Ouverts, Clics, Taux d'ouverture, « Warmup Mailflow » (faux trafic) |
| `Deliverability.tsx` | Délivrabilité › Domaines | « Santé par domaine » : Envoyés, Rebonds, Rebonds %, Plaintes, Plaintes %, État | Seuils laxistes 5 % / 1 % (remplacés par § 3.2), « Couverture scraping » |
| `Mailboxes.tsx` | Réponses (lecture en fil) + fiche Boîte | Lecture d'une boîte, dossiers, rafraîchir | Envoi libre depuis la boîte hors porte, suppression de messages |
| `VpsHealth.tsx` | Plus › Santé serveur | Services, file d'attente, dernier envoi, disque, RAM | Lecture shell de `/proc`, noms « PMTA » et « Postfix » |
| `Campaigns.tsx`, `CampaignsHub.tsx` | Campagnes (liste, assistant, suivi) | Liste, inscrits, répondu, gagné | Ciblage par pays ou « tier » SEO |
| `PressCampaign.tsx`, `PressTemplates.tsx` | Plus › Presse | Contacts presse, angle, statut, lancer, pause, reprise, santé presse | DR, langue, domaines SOS-Expat en dur |
| `Suppression.tsx` | Oppositions | Liste, motif, source, date, ajout | Bouton « Retirer » sans motif, adresse en clair |
| `AbTestResults.tsx` | Campagne › onglet « Test A/B » (V1) | Comparaison des variantes | Métrique d'ouverture |

### 7.1 Monitoring des boîtes (Délivrabilité › onglet Boîtes)

```
ENVOIS › Délivrabilité › Boîtes                        [Locataire : Axion-IA]   [Arrêt d'urgence]
Phrase : « 4 boîtes sur 4 sont prêtes. Volume possible aujourd'hui : 120. Prochaine étape : 180 le 14/01. »
Filtres : Domaine [tous v]  État [tous v]  Période [7 j v]
┌──────────────────────────┬──────────┬─────────────┬────────┬───────┬──────────┬───────────┬──────────┬────────────────┐
│ Boîte                    │ État     │ Palier/jour │ Auj.   │ 7 j   │ Rebonds  │ Plaintes  │ Réponses │ Dernier envoi  │
├──────────────────────────┼──────────┼─────────────┼────────┼───────┼──────────┼───────────┼──────────┼────────────────┤
│ prenom.nom@<domaine-1>   │ ● Chauffe│ P5 · 30     │ 28/30  │ 140   │ 1 (0,7 %)│ 0         │ 3        │ 11:42          │
│ prenom2.nom@<domaine-1>  │ ● Prête  │ P5 · 30     │ 30/30  │ 151   │ 0        │ 0         │ 2        │ 11:40          │
│ prenom.nom@<domaine-2>   │ ▲ Surveil│ P4 · 25     │ 12/25  │  98   │ 3 (3,1 %)│ 0         │ 0        │ 10:05          │
└──────────────────────────┴──────────┴─────────────┴────────┴───────┴──────────┴───────────┴──────────┴────────────────┘
Ligne ▲ : « Rebonds 3,1 % sur 7 j > 2 % : palier ramené de P5 à P4 le 08/01 à 07:00. Reprise possible après 3 jours verts. »
Bloc « Listes noires » : IP <ip-1> : Spamhaus ✓ · Barracuda ✓ · SpamCop ✓ (contrôlé il y a 42 min, résolveur local)
                         Domaines : <domaine-1> DBL ✓ SURBL ✓ · <domaine-2> DBL ✓ SURBL ✓
Actions par ligne : [Mettre en pause] [Voir la fiche] (la fiche contient la courbe 30 j et le journal des décisions)
```

### 7.2 Délivrabilité (onglets Domaines · IP · Boîtes · Chauffe · Vérification · Serveurs)

```
ENVOIS › Délivrabilité › Domaines                                   [Arrêt d'urgence]
┌──────────────┬────────────┬─────┬──────┬───────┬─────┬──────────┬──────────┬─────────┬────────┬──────────────┐
│ Domaine      │ État       │ SPF │ DKIM │ DMARC │ PTR │ Envoyés 7j│ Rebonds %│ Plaintes│ Listé  │ Âge          │
├──────────────┼────────────┼─────┼──────┼───────┼─────┼──────────┼──────────┼─────────┼────────┼──────────────┤
│ <domaine-1>  │ ● Chauffe  │ ✓   │ ✓    │ none→ │ ✓   │ 410      │ 0,7 %    │ 0       │ non    │ 47 j         │
│ <domaine-2>  │ ▲ Ralentie │ ✓   │ ✓    │ none  │ ✓   │ 210      │ 3,1 %    │ 0       │ non    │ 47 j         │
│ axion-ia.com │ ◆ Protégé  │ lecture seule : DMARC p=reject vérifié chaque jour, jamais expéditeur de masse │
└──────────────┴────────────┴─────┴──────┴───────┴─────┴──────────┴──────────┴─────────┴────────┴──────────────┘
Source et âge : « contrôle DNS 06:30 », « comptabilité du serveur d'envoi, il y a 3 min ».
Bouton principal : [Ajouter un domaine] (V0 : saisie + plan DNS à poser + vérification ; V1 : poussée Cloudflare)
```

### 7.3 Campagnes

```
ENVOIS › Campagnes                                  [Nouvelle campagne]   [Arrêt d'urgence]
Filtres : Statut · Nature (prospection / presse / information art. 14 / suivi) · Famille · Étiquette · Boîte · Auteur
┌─────────────────────────────┬──────────┬────────────┬───────────┬────────┬────────┬─────────┬──────────┬─────────────────┐
│ Campagne                    │ Nature   │ Statut     │ Étape     │ Éligib.│ Envoyés│ Réponses│ Opposit. │ Fin prévue      │
├─────────────────────────────┼──────────┼────────────┼───────────┼────────┼────────┼─────────┼──────────┼─────────────────┤
│ Organisateurs T1            │ Prospect.│ ● En cours │ 2 / 3     │ 312    │ 188    │ 9 (2 +) │ 2        │ 1ers : 21/01    │
│ Communiqué Tour France IA   │ Presse   │ ◌ À valider│ —         │ 84     │ —      │ —       │ —        │ —               │
└─────────────────────────────┴──────────┴────────────┴───────────┴────────┴────────┴─────────┴──────────┴─────────────────┘
Assistant en 6 étapes (CON-013) : 1 Nature et objectif → 2 Ciblage (constructeur ET/OU/SAUF, aperçu en direct :
« 312 éligibles · 41 exclus : 18 opposés, 9 non vérifiés < 30 j, 7 adresses partagées, 4 clients, 3 webmails »)
→ 3 Séquence et modèles (aperçu bureau / mobile + en-têtes) → 4 Planification (fenêtre, dates, plafond, A/B en V1)
→ 5 Feu vert (31 cases recalculées, chacune ✓ ou ✗ avec sa cause en une ligne) → 6 Envoyer à la validation.
Validation (owner) : « Vous validez la version a3f9… : 312 destinataires, 3 étapes, du 13/01 au 03/02, expéditeurs :
4 boîtes de <domaine-1>/<domaine-2>. Ce qui va partir : [aperçu]. » [Valider] [Refuser avec motif]
Suivi : Pause / Reprendre / Annuler (motif), entonnoir par étape, exclus du jour par motif, journal des décisions.
```

### 7.4 Presse

```
ENVOIS › Plus › Presse                     [Lancer la campagne presse]  [Pause presse]  [Arrêt d'urgence]
Santé presse : boîtes presse@ 2/2 prêtes · rebonds 7 j 0,0 % · plaintes 0 · volume possible aujourd'hui : 25
┌──────────────────────┬─────────────────┬──────────────────────┬────────────┬──────────────┬─────────────┐
│ Média                │ Rubrique        │ Angle                │ Provenance │ Statut       │ Mise à jour │
├──────────────────────┼─────────────────┼──────────────────────┼────────────┼──────────────┼─────────────┤
│ <média régional>     │ Économie        │ IA pour les TPE      │ ✓ fiable   │ Relance J+5  │ 12/01       │
│ <magazine pro>       │ Numérique       │ Tour France IA       │ ▲ à revoir │ Exclu (prov.)│ 10/01       │
└──────────────────────┴─────────────────┴──────────────────────┴────────────┴──────────────┴─────────────┘
« Les journalistes n'entrent que par ce segment. Opposition et information art. 14 s'appliquent. Communiqué par lien, jamais en pièce jointe. »
```

### 7.5 Liste de suppression (Oppositions)

```
ENVOIS › Oppositions                                              [Ajouter une opposition]
Recherche : [adresse ou domaine]  → « Cette adresse NE PEUT PAS recevoir : opposée depuis le 14/01 (lien de désinscription,
campagne Organisateurs T1). Portée : toute prospection de <Entité>. Définitif. »
Onglets : Oppositions (volonté) · Suppressions (faits : rebond dur, 3 rebonds mous, plainte) · Par domaine · À confirmer (STOP par réponse)
┌──────────────┬──────────────┬────────────────────┬───────────────┬────────────┬──────────────────────┐
│ Empreinte    │ Type         │ Motif              │ Source        │ Depuis     │ Levée                │
├──────────────┼──────────────┼────────────────────┼───────────────┼────────────┼──────────────────────┤
│ 3fa1c0de…    │ Opposition   │ désinscription     │ one-click     │ 14/01      │ impossible           │
│ 9bc27e11…    │ Suppression  │ rebond dur 5.1.1   │ serveur envoi │ 13/01      │ [Lever, motif requis]│
│ @<domaine>   │ Par domaine  │ « plus personne »  │ réponse       │ 12/01      │ owner seulement      │
└──────────────┴──────────────┴────────────────────┴───────────────┴────────────┴──────────────────────┘
Aucune adresse en clair dans la liste ; on retrouve une adresse en la tapant (comparaison d'empreintes).
```

### 7.6 Santé serveur (Plus › Santé serveur)

```
ENVOIS › Plus › Santé serveur                                       [Arrêt d'urgence]
┌──────────────────┬──────────┬───────────────────────────────────────────────────────────────┐
│ Machine          │ État     │ Détail (relevé toutes les 5 min, source : agent, il y a 2 min) │
├──────────────────┼──────────┼───────────────────────────────────────────────────────────────┤
│ Serveur d'envoi 1│ ● Sain   │ Service d'envoi actif · liaison privée 12 s · disque 31 % · RAM libre 61 % │
│                  │          │ File : 14 messages (le plus ancien : 4 min) · plafond local restant : 96 / 120 │
│                  │          │ Dernier envoi 11:42 · configuration v7 appliquée le 09/01 (empreinte ok)       │
│ Sonde externe    │ ● Saine  │ Anti-relais OK 06:40 · ports exposés : aucun inattendu (IPv4/IPv6)            │
│ CRM (files)      │ ● Sain   │ emailing-urgent 0 · emailing-envoi 14 · retours 0 en retard                  │
└──────────────────┴──────────┴───────────────────────────────────────────────────────────────┘
Test de fumée 06:45 : message reçu par la boîte témoin, spf=pass dkim=pass dmarc=pass.
```

### 7.7 Autres écrans

| Écran | Contenu | Étape |
|---|---|---|
| **Accueil** (CON-010) | Bandeau d'état global, « Aujourd'hui » (volume possible, prochaine étape), réponses à traiter, pauses en cours, premiers pas | V0 |
| **Modèles** (CON-016) | Versions, statut, campagnes qui les utilisent, contrôleur de contenu | V0 |
| **Réponses** (CAM-053) | File, filtres, lecture en fil, classement en un clic | V0 |
| **Alertes** (CON-023, 024) | Règles fermées, gravité, action déjà prise, fermeture automatique | V0 |
| **Réglages** (CON-027) | Identité légale **du locataire**, interrupteurs, seuils | V0 |
| **Résultats** (CON-057) | Vues de résultats | V1 |
| **Capacité** (CON-053) | Capacité et réserve | V1 |
| **Coulisses techniques** (CON-074) | Exploitation | V1 |
| **Mise en route** en 22 étapes (CON-068) | Assistant de démarrage | V1 |

### 7.8 Canal des alertes (décision à confirmer par Will)

Le 24/10, Will a demandé « plus aucune notification push ». Le fichier 02 (L4) prévoit des alertes **par e-mail**. Proposition :
- **console** : cloche, bandeau, écran Alertes et rapport quotidien archivé ;
- **e-mail à Will** pour les alertes critiques et le rapport du matin. Envoi par le canal de service du CRM, **jamais par le serveur de prospection** ;
- **Telegram en connecteur éteint par défaut**. `TelegramAlertService.php` de Mission Control pourrait être repris en 0,3 jour si Will le rallume.
- Pas d'urgence au téléphone : les actions critiques sont **déjà automatiques et fermées** (pause, arrêt).

---

## 8. Gardes de doctrine codées (tests rouges avant verts)

| # | Garde | Où | Test |
|---|---|---|---|
| G1 | **Jamais `axion-ia.com`** ni ses sous-domaines comme domaine d'envoi, `MAIL FROM`, `From`, `Reply-To` ou lien de suivi d'une campagne. Même règle pour le domaine principal de chaque client, sauf case tracée. | Registre des domaines (RES-007), composition (CAM-076), configuration du serveur (INF-021 : refus de tout `MAIL FROM` hors registre) | Unitaire + garde CI qui cherche le littéral dans `app/Emailing` + test de bout en bout au banc |
| G2 | **ZeptoMail intouchable** : le module n'importe ni n'appelle le client ZeptoMail. ZeptoMail n'est jamais un `ServeurEnvoi`. | Architecture | Garde CI : aucune référence à ZeptoMail sous `app/Emailing/**`. Le webhook ZeptoMail existant reste en écoute seule (son jeton passe dans un en-tête). |
| G3 | **Opposition avant tout envoi** : `peutRecevoir()` est appelée à la vague **et** moins de 15 minutes avant l'injection. Une seule façade, `EnvoiAutorise`. | CAM-003, 004 | `AucunEnvoiSansEligibiliteTest`, réécrit (il ne doit plus être « vide ») ; mutation qui retire l'appel → rouge |
| G4 | **Segments sensibles fermés** : syndicats de salariés, santé/FINESS, INSEE, Roumanie. La presse n'entre que par son segment. Tout est fermé par défaut, et chaque ouverture est une case tracée de l'owner. | `Segments`, `GardePresse`, CAM-078 | Variable d'environnement absente → tout fermé (corrige `OUVERTS_PAR_DEFAUT`) |
| G5 | **Pas de pixel, pas de lien réécrit**, pas d'identifiant personnel dans une URL. | Composition, contrôleur | Garde CI + contrôleur de contenu |
| G6 | **Pas de proxy sur le chemin d'envoi** ; `residential` refusé (corrige `IPRoyalProvider.php:38`). | RES-046, 051 | Garde CI |
| G7 | **Pas de simulacre en production** (`MOCK_*` → refus). | SEC-009 | Test de démarrage |
| G9 | **Journaux sans adresse** (empreinte tronquée à 8 caractères). | SEC-008 | Garde sur les appels au journal |
| G10 | **Cloisonnement par locataire** : RLS `FORCE`, `workspace_id` partout, IDOR testé. | CON-031 | Test sous le rôle applicatif + auditeur sécurité |
| G11 | **Bloc art. 14 et entité du locataire** exigés pour tout non-informé. | SEC-015 | Le contrôleur bloque |
| G12 | **Clients de la console jamais destinataires** (existant). | `GardeConsoleClient` | Test existant |

---

## 9. Tests et « essai à blanc » avant le premier envoi réel

1. **Unitaires et gardes** : G1 à G12 et les machines d'états (chaque état a une sortie). Les seuils sont testés aux bornes : 1,99 % / 2,01 %, échantillon 99 / 100, 1 et 2 plaintes.
2. **Kit de conformité du contrat `ServeurEnvoi`** (§ 10). Toute implémentation doit le passer : simulateur, KumoMTA au banc, et Postfix de secours si un jour il sert.
3. **Banc jetable** (INF-061) : serveur d'envoi + liaison privée + puits SMTP.
   - Injection, signature DKIM vérifiée, anti-relais en 4 couches testé en boîte noire, homme mort (INF-025), plafond local.
   - Retours rejoués : doublons, désordre, retard de 72 h, webhook falsifié refusé.
4. **Scénarios de bout en bout** (SEC-027). Sous-ensemble V0 obligatoire :
   - injection → témoins `spf/dkim/dmarc=pass` ;
   - désinscription POST → effet en moins d'une minute ;
   - rebond dur → suppression sur toutes les fiches ;
   - plainte ARF → opposition + disjoncteur ;
   - arrêt d'urgence → plus rien n'est injecté ;
   - restauration du CRM → envoi gelé (INF-057) ;
   - locataire A ne voit rien de B, et l'opposition de A ne bloque pas B.
5. **Essai à blanc en production** (« dry run »). Une vraie campagne validée tourne en entier avec le transport en **mode simulation** : vague, tranches, `peutRecevoir`, vérification de moins de 30 jours, composition, en-têtes, journal, statistiques. **Zéro connexion SMTP.** On compare les comptes prévus, simulés et journalisés. La complétude doit être de 100 % (CON-056).
7. **Premier message reçu et validé par Will** sur sa propre adresse.
8. **Premier envoi réel** : P1 = 20 organisateurs vérifiés de moins de 30 jours, adresses professionnelles seulement, aucun webmail.
9. **Feu vert de 31 cases tout vert** (zone 5 § 5), sous la forme d'un écran, pas d'un document.

---

## 10. Contrat d'interface avec le serveur d'envoi (agnostique)

L'option de serveur est choisie par un autre agent (KumoMTA par défaut selon D-02, risque de licence étudié dans le fichier 05, Postfix + OpenDKIM en secours). Le CRM ne connaît que ceci.

### 10.1 Opérations (`App\Emailing\ServeurEnvoi`)

| Opération | Entrée | Sortie | Exigences |
|---|---|---|---|
| `injecter(lot)` | Messages **déjà composés** par le CRM (RFC 5322 complet, DKIM non signé), enveloppe `MAIL FROM` VERP, `RCPT TO`, groupe d'envoi (locataire + pool + IP), jeton d'envoi | Par message : `accepte` + `id_file` du serveur, ou `refuse` + motif | SMTP AUTH sur la liaison privée (un identifiant par groupe et par locataire, INF-083) ou API HTTP équivalente. **Idempotent par jeton** : un jeton déjà accepté n'est pas renvoyé. |
| `retirer(cible)` | Liste de jetons, empreinte d'adresse, campagne, locataire | Nombre de messages retirés de la file | En moins de 5 minutes (CAM-048, RET-039) |
| `pause(portee)` / `reprise(portee)` | Portée : global, locataire, pool, IP, IP × groupe de fournisseurs, domaine | Accusé + état | La reprise demande un ordre signé |
| `etat()` | — | Files (nombre, âge), ralentissements par groupe, version et empreinte de la configuration chargée, plafond local restant **par locataire**, battement | Lecture seule |
| `validerConfiguration(v)` / `appliquerConfiguration(v)` | Version générée depuis la base (IP, PTR, pools, domaines, sélecteurs DKIM, limites par groupe de fournisseurs, plafonds par locataire) | Validation à blanc, puis application avec retour arrière automatique si la vérification échoue (INF-038) | Ce qui augmente le risque attend l'owner (INF-039). V0 : application par le runbook de la session déployeuse. V1 : par l'agent. |
| `evenements` (poussée) | — | Webhook § 6 | HMAC dans l'en-tête, rejoué 72 h |
| `lireComptabilite(curseur)` (tirage) | Curseur | Événements normalisés depuis le curseur | Gardée 30 jours (INF-055), sert à la réconciliation nocturne |
| `recapitulatif(jour)` | Date | Comptes par type, par groupe et par locataire | Réconciliation (RET-046) |
| `sante()` | — | Version, temps de fonctionnement, disque, file, homme mort armé | Toutes les 5 minutes (INF-045) |

### 10.2 Événement normalisé

```
{ "event_id": "uuid", "source": "serveur-envoi-1", "type": "injecte|livre|report|rebond_dur|rebond_mou|blocage|plainte|expire",
  "horodatage": "2027-01-13T10:42:05Z", "locataire": "uuid", "jeton_envoi": "base64url(≥128 bits)",
  "destinataire_empreinte": "sha256", "smtp_code": 550, "dsn": "5.1.1", "categorie_serveur": "…",
  "diagnostic": "texte expurgé, sans adresse" }
```

### 10.3 Invariants que toute implémentation doit tenir

- Un **plafond journalier dur local**, par locataire et global, que le CRM ne peut pas dépasser (INF-023).
- L'**homme mort** : le serveur met ses files en pause si le CRM se tait 15 minutes pendant une fenêtre d'envoi (INF-025).
- **Refus de tout `MAIL FROM` hors registre** (INF-021).
- Le serveur est le **seul signataire DKIM**. Les clés privées ne le quittent jamais (INF-027).
- **Aucun relais ouvert**, aucun port public autre que SSH restreint et WireGuard, envoi en IPv4 seulement (INF-013, 016, 020).
- **IPv4 d'envoi ≠ IP de gestion** (INF-012). PTR = HELO (RES-034).

Un **mode `simulation`** (puits) implémente le même contrat pour la préproduction, la CI et l'essai à blanc (INF-059). Changer de serveur revient à écrire une nouvelle implémentation et à faire passer le kit de conformité, sans toucher au CRM.

---

## 11. Coûts mensuels réalistes

Estimations HT à vérifier chez chaque fournisseur. Il n'y a **aucune licence** de serveur d'envoi si KumoMTA ou Postfix est confirmé par le fichier 05.

| Poste | V0 (20 → ~300/j, 1 locataire) | V1 (1 000-2 000/j) | V2 (≤ 5 000/j) |
|---|---|---|---|
| Serveur d'envoi (VPS, port 25 ouvert par écrit) | 5-10 € | 10-20 € | 2 serveurs : 30-60 € |
| IP supplémentaires (gestion ≠ envoi) | 1-2 € | 2-5 € (2 IP d'envoi) | 5-10 € |
| Sonde externe chez un autre hébergeur | 4-6 € | 4-6 € | 4-6 € |
| Domaines d'envoi (10-15 €/an chacun) | 2 domaines : ~2-3 € | 4 domaines : ~5 € | 8-10 : ~10-12 € |
| Boîtes hébergées (expéditrices + bounce, fbl, desinscription, dmarc, presse) | 5-15 € | 20-40 € | 50-90 € |
| Vérification d'adresses (≈ 0,003-0,008 € l'adresse ; cache de 30 jours) | 3 000-6 000 adresses : 10-45 € | 20 000-30 000 : 60-200 € | Plafond D-32 : 250-400 € TTC |
| Boîtes témoins (M365 payant, les autres gratuites) | ~5 € | ~5 € | 10-15 € (Workspace, Yahoo…) |
| Listes noires (Spamhaus DQS : gratuit sous conditions, à vérifier ; sinon payant) | 0 € | 0 € à ~? | Payant probable |
| Cloudflare, Google Postmaster, Microsoft SNDS | 0 € | 0 € | 0 € |
| **Total** | **≈ 35 à 90 € par mois** | **≈ 120 à 280 € par mois** | **≈ 400 à 650 € par mois** |

- **Par client en mutualisé** : il faut ajouter son IP dédiée (1-2 €), ses domaines, ses boîtes et ses vérifications, à refacturer au client.
- **En dédié** : le client paie son propre serveur d'envoi et sa sonde, soit au moins 10-16 € par mois en plus.
- **Hors coûts** : le temps des agents (abonnement Claude) et une éventuelle relecture juridique (Will a dit : pas de juriste).

---

## 12. REQ retenues pour la V0 (sous-ensemble du registre)

Le calcul a été fait par script sur `REGISTRE-REQ.csv`. **268 REQ sont retenues pour la V0** : 11 « V0 », 254 « V1 » et 3 remontées de « V2 ». **129 REQ « V0/V1 » du registre sont reportées en V1/V2 du module.** Le sous-ensemble est large parce que la sûreté du premier envoi est la priorité du cahier. Ce qui est réduit, c'est l'outillage et l'automatisation de l'exploitation, jamais les protections.

**Retenues en V0** (numéros par domaine) :
- **INF** (37) : 001 002 003 004 007 008 010 012 013 014 015 016 017* 020 021 023 025 026 027 029 042 043 044 045 046 047 050 054 055 056 059 060 061 062 080 082 083. (*017 est amendée par ADR : webhook sur la liaison privée et tirage nocturne, § 6.)
- **RES** (32) : 001 003 004 005 007 **009↑** 010 011 012 013 014 016 017 020 021 022 023 026 029 032 034 038 039 040 041 042 046 051 053 054 056 057.
- **VER** (20) : 001 002 003 004 005 006 007 012 013 014 015 017 019* 020 023 024 025 027 030 031. (*019 avec une validité de 30 jours, demande de Will.)
- **CHA** (31) : 001 002* 004 005 006 007 009 010 012 013 014 017 018 019 020 021 022 023 024 025 027 028 029 030 033 035 037 048 060 061 068. (*002 avec la courbe du § 3.1.)
- **CAM** (52) : 001 003 004 005 006 007 008 010 011 013* 014 015 016 017 018 019 020 021 023 024 027 032 033 034 035 036 038 039 040 041 042 043 048 050 051 052 053 057 058 060 061 062 067 075 076 077 078 079 080 081 082 083. (*013 ramenée au locataire.)
- **RET** (41) : 001 à 007, **008↑** 009 010 011 012 013 015 016 017 018 020 021 022 **023↑** 024 025 026 027 028 029 030 031 035 036 037 038 039 040 041 042 045 046 047 048.
- **CON** (30) : 001 005 006 007 008 009 010 012 013 014 015 016 017 020 022 023 024 027 030 031 032 033 038 041 042 043 067 070 071 073. (CON-025, Telegram, est remplacée en V0 par la console et l'e-mail, § 7.8 ; le connecteur Telegram facultatif est en V1.)
- **SEC** (25) : 001 002 004 005 007 008 009 010 012 013 014 015 016 018 019 020 021 024 027 028 029 032 033 036 037.

↑ = remontée de V2 : RES-009 (âge des domaines), RET-008 (`Feedback-ID`), RET-023 (`mailto:`).

**Reportées en V1 du module** (fonctions complètes, 1 000-2 000/j) :
- **INF** : 011 018 019 022 024 036 037 038 039 041 048 052 057 067 069-078 081. L'agent à commande forcée, la configuration générée depuis la base, les connecteurs et les écrans d'exploitation arrivent en V1. En V0, le serveur est réglé par runbook et gabarits.
- **RES** : 002 006 033 045 047-050 052 060 062 063 064-067. Assistants complets, poussée DNS par Cloudflare, score, connecteurs.
- **VER** : 008 009 010 029.
- **CHA** : 008 015 016 036 038 040-047 049-052 055-057 059 062-064 066 067 069. Machine de santé complète, 13 portées, projection, rythmes.
- **CAM** : 022 025 054 059 068 070 072, plus 012, 031, 037, 044, 064 (presse), remontées de V2 vers la V1 à la demande de Will.
- **RET** : 043, plus 014 (asynchrones fins).
- **CON** : 003 018 019 025 028 029 034 035 037 039 040 044-066 068 069 072 074-078.
- **SEC** : 003 006 034 038-041.
- **Remontées de V2 vers V1 par l'audit** : RES-055 (Postmaster API), RES-036 (SNDS/JMRP), RES-015 (DKIM à deux sélecteurs), SEC-011 (objet lié à la profession).

**V2 du module** :
- REQ « V2 » restantes : multi-serveurs (INF-066, 068), IA (CAM-026, 028, 030), attribution (CAM-066, 069, 071), exercices mensuels (SEC-031, 035), tests de charge (SEC-030) ;
- plus les « plus-tard » : suivi des clics sur décision, fuseaux d'outre-mer, domaines défensifs.

---

## 13. Lots et estimation en jours-agent

Les estimations incluent les tests. Ajouter environ 15 % pour les relectures Opus et les audits de sécurité et d'intégration aux fins de lot.

| Lot | Contenu | REQ principales | j-agent | Dépend de |
|---|---|---|---|---|
| **E0 Cadre** | 2 ADR (dont l'amendement webhook privé), dictionnaire, arbitrage des tables échafaudées (`email_sends`, `campaigns`, `unsubscribes`…), relevé de prod, drapeau du module, 8 permissions, gardes CI G1-G9 | INF-001-003, CAM-004/005, CON-030, SEC-007 | 6 | — |
| **E1 Multi-locataire de l'envoi** | `workspace_id` sur `opt_out` et `email_suppressions`, identité légale par locataire, quotas, portée « locataire », tests RLS et IDOR | CON-031, VER-023, § 1 | 6 | E0, preuve RLS (fichier 04) |
| **E2 Contrat `ServeurEnvoi`** | Interface, simulateur et puits, kit de conformité, banc jetable | INF-029, 059, 061 | 6 | E0 |
| **E3 Implémentation du serveur** | Gabarits de configuration, DKIM, anti-relais en 4 couches, WireGuard, plafond local, homme mort, preuve d'injection, sauvegarde, sonde externe | INF-012-016, 020-027, 047, 054, 082, 083 | 12 | E2, port 25 obtenu |
| **E4 Registres et DNS** | Domaines, IP, boîtes, personnes signataires, garde de nommage, plan DNS généré, contrôle DNS quotidien, PTR, `axion-ia.com` protégé | RES-001-014, 016, 020-023, 026, 032-042 | 8 | E1 |
| **E5 Vérification** | Fournisseur branché, cascade, porte qualité, pré-vol de 30 jours, quotas, estimation du coût | VER-* (20) | 6 | E1 |
| **E6 Retours** | Webhook HMAC idempotent, `emailing_retours`, `AppliquerRetour`, rebonds mous en base, classement, VERP, ARF, relève IMAP, STOP, réconciliation nocturne | RET-001-018, 025-031, 035-048, RES-041 | 14 | E2, E4 |
| **E7 Désinscription** | Route publique `go.`, POST un clic, page à l'entité, `mailto:`, opposition par domaine, retrait immédiat | RET-010, 020-024, 026, CAM-048 | 5 | E6 |
| **E8 Chauffe et protections** | Courbe, jours effectifs, budget min des trois niveaux, décision de 07:00, seuils, disjoncteurs (8 portées), arrêt d'urgence, échec fermé, groupes de fournisseurs | CHA-* (31) | 12 | E4, E6 |
| **E9 Campagnes** | `EnvoiAutorise`, ciblage étendu, pression, modèles, variables, contrôleur, variantes de base, séquences, vagues, tranches, validation versionnée, pause et annulation, composition, injection, feu vert, art. 14 | CAM-* (52), SEC-010, 015, 019 | 22 | E5, E7, E8 |
| **E10 Réponses** | Rattachement, classement par règles, file, fiche 360°, organisateurs | CAM-050-053, 057-061 | 6 | E6 |
| **E11 Surveillance** | Listes noires (résolveur local, DQS), boîtes témoins, test de fumée, santé par domaine et par boîte, alertes console et e-mail, rapport du matin | RES-053, 054, 056, 057, INF-045, 050, CON-023, 024 | 7 | E3, E6 |
| **E12 Console V0** | Accueil, Campagnes (liste, assistant, validation, suivi), Modèles, Réponses, Délivrabilité (Domaines, IP, Boîtes, Chauffe, Vérification), Oppositions, Alertes, Presse (lecture), Santé serveur, Réglages, arrêt d'urgence | CON-* (30) | 18 | E8-E11 |
| **E13 Conformité** | Base légale par flux, LIA, AIPD v2, bloc art. 14 par locataire, sous-traitants, registre | SEC-001, 004, 012-014, 018 | 4 (code) + textes de Will | décisions D-07, D-26 |
| **E14 Bout en bout** | Scénarios du banc, essai à blanc, recette, premier message à Will, J1 = 20 organisateurs | SEC-027, 028, INF-060 | 6 | tous |
| **Total V0** | | 268 REQ | **≈ 138 j-agent** (≈ 160 avec les relectures) | |
| **V1** | A/B, presse complète, réponses depuis la console, IA de classement, Postmaster et SNDS par API, ingestion DMARC, agent SSH et configuration depuis la base, Cloudflare par API, assistants complets, 13 portées, capacité et projection, résultats et rapports, coulisses, mise en route, multi-locataire en libre-service, Telegram facultatif | ≈ 129 reportées + 9 remontées | **≈ 115 à 135 j-agent** | V0 en production |
| **V2** | Plusieurs serveurs, 5 000/j, micro-variations et accroches IA, attribution du chiffre d'affaires, connecteurs (registraire, hébergeur de boîtes), exercices, tests de charge | REQ « V2 » | **≈ 70 à 90 j-agent** | V1 |

**Ordre de grandeur calendaire de la V0** : 8 à 10 semaines avec 3 ou 4 agents en parallèle.
- Ces semaines tournent **en même temps que les horloges** que personne n'accélère : âge des domaines (21 jours), ticket port 25 (environ un mois), DPA du vérificateur, textes art. 14.
- Comparaison : l'option accélérée D-86 du cahier (223,5 j-agent) inclut l'outillage d'exploitation, que cette version reporte en V1.

---

## 14. Risques

| # | Risque | Gravité | Parade |
|---|---|---|---|
| R1 | Envoi par un outil hors CRM (JSONL confié ailleurs) avant la fin de la V0 | Critique | Une seule voie (G3). Le JSONL n'est plus qu'un aperçu. Will est prévenu. |
| R2 | Information art. 14 non prête (organisateurs en retard depuis le 27/10 environ) | Critique | E13 et décision D-01 avant E14. Chaque premier message sans bloc aggrave l'écart. |
| R3 | Port 25 refusé ou tardif chez l'hébergeur | Majeur | Deux demandes en parallèle (hébergeur principal et plan B) dès maintenant, volumes déclarés honnêtement (SEC-033). |
| R4 | Fuite entre locataires (RLS non prouvée, oppositions sans `workspace_id`) | Critique | E1 avant tout client. Mode dédié par défaut. Auditeur sécurité IDOR. |
| R5 | Un client abîme une réputation partagée | Majeur | IP dédiée par locataire, pause automatique à 0,3 % de plaintes, politique d'usage acceptable, plafond local par locataire. |
| R6 | Risque de licence ou d'abandon du serveur d'envoi | Moyen | Contrat `ServeurEnvoi` + kit de conformité + Postfix de secours (fichier 05). |
| R7 | Table de 2 785 motifs de rebonds d'origine inconnue | Moyen | Vérifier la licence, tester sur les journaux du banc, sinon partir des classements fournis avec le serveur. |
| R8 | Seuils « engagement 5 % » non mesurables sans pixel | Moyen | Redéfinition proposée (§ 3.2), à décider par Will. |
| R9 | Taux non significatifs à 20-50 envois par jour | Moyen | Règles absolues sous l'échantillon (CHA-014), boîtes témoins chaque jour. |
| R10 | Dérive « snowshoe » à la montée | Majeur | Cohortes espacées, anti-dispersion (RES-060 en V1), cible de 5 000/j au plus (D-28). |
| R11 | Listes noires mal mesurées (Spamhaus via un résolveur public) | Moyen | Résolveur local ou clé DQS (RES-053). SORBS retiré. |
| R12 | Secret poussé dans le dépôt public | Critique | G8, gitleaks bloquant, secrets hors git (fichier 01). |
| R13 | Copie de seuils laxistes de SOS-Expat (5 % / 1 %) | Moyen | Table unique `emailing_seuils` avec les valeurs du § 3.2. |
| R14 | Presse : contradiction entre le cahier et le code | Faible | Corriger le registre selon la décision du 01/10. |

---

## 15. Décisions attendues de Will

1. **Engagement minimal** : remplacer les « 5 % d'ouvertures » par la règle « réponses humaines / livrés » (alerte sous 1 %) ?
2. **Canal d'alerte** : console + e-mail à Will, Telegram éteint, comme proposé ?
3. **Liste de protection de plateforme** (rebonds durs partagés entre locataires) : non par défaut, ou oui après validation ?
4. **Modèle client** : instance dédiée par défaut tant que la RLS n'est pas prouvée (fichier 02, M0) ?
5. **Entité expéditrice d'Axion** (D-07 : SAS ou OÜ) et **textes art. 14** (D-26), à fournir avant le lot E14.
6. **Organisateurs en retard art. 14** : voie D-01.
8. **Validation de 30 jours** pour le verdict de vérification (au lieu de 90 jours) : confirmée comme réglage par défaut ?

---

## Résumé (20 lignes au plus)

1. Le CRM Pro n'envoie rien aujourd'hui. Il prépare (`ResolveurDestinataires`, `EligibiliteAdresse`, `peutRecevoir`) et importe des retours. Ces briques sont reprises comme fondations.
2. Le module est spécifié en entier. « Petit » ne vise que les volumes : V0 de 20-50 à environ 300/j, V1 de 1 000 à 2 000/j, V2 jusqu'à 5 000/j.
3. Multi-locataire dès la V0 : chaque client a son entité, ses domaines, son IP dédiée, ses boîtes, ses quotas, son opposition, ses gabarits, ses droits et son journal. Quand le client envoie, l'art. 14, le pied et la désinscription sont à son nom, et Axion est sous-traitant.
4. Les campagnes sont complètes : ciblage ET/OU/SAUF multi-étiquettes et listes, exclusions, séquences de 1 à 4 étapes avec arrêts, gabarits versionnés et variables en liste blanche, variantes, A/B en V1, validation attachée à une version, pause, arrêt et retrait, presse, statistiques sans pixel.
5. La chauffe suit des paliers 20 → 35 → 50 → … → 250 (V0) → 500 → 1 000 → 2 000 (V1), en jours effectifs, avec le budget le plus bas entre IP, domaine et boîte.
6. Règles d'arrêt : plus de 2 % de rebonds durs → palier précédent ; plus de 0,1 % de plaintes → arrêt 48 h ; sous l'échantillon, des règles absolues ; l'« engagement 5 % » est à redéfinir sans pixel (décision de Will).
7. Vérification par un fournisseur HTTPS (Hunter déjà présent), verdict `valide` de moins de 30 jours exigé à l'injection, pré-vol par tranche.
8. Désinscription RFC 8058 sur `go.<domaine d'envoi>`, `mailto:` traité, page à l'entité, une seule porte `peutRecevoir()` par locataire.
9. Les événements arrivent par un webhook HMAC dans l'en-tête, sur la liaison privée, idempotent et écrit avant d'être appliqué, avec un tirage nocturne pour la réconciliation. Le JSONL manuel devient une simple source d'import.
10. La surveillance couvre les listes noires (résolveur local), SPF/DKIM/DMARC/PTR chaque jour, les boîtes témoins, la santé par domaine et par boîte. Postmaster et SNDS sont inscrits en V0 et lus par API en V1.
11. Alertes : console + e-mail à Will, Telegram éteint (plus de push depuis le 24/10).
12. Sept écrans sont repris de Backlink Engine sans les ouvertures et clics, sans Mailflow et sans suppression libre. Leurs maquettes texte sont au § 7.
13. Douze gardes de doctrine sont codées : jamais `axion-ia.com`, ZeptoMail intouchable, opposition avant tout envoi, segments sensibles fermés par défaut, cloisonnement, pas de pixel ni de proxy.
14. Tests : kit de conformité du contrat, banc, scénarios de bout en bout, essai à blanc en production sans SMTP, mode recette (Will + 4 témoins), puis J1 = 20 organisateurs.
15. Le contrat `ServeurEnvoi` est agnostique : 9 opérations, un événement normalisé, des invariants (plafond local, homme mort, DKIM sur place) et un mode simulation. Le serveur est remplaçable.
16. Coûts : environ 35 à 90 €/mois en V0, 120 à 280 € en V1, 400 à 650 € en V2, sans licence.
17. REQ : 268 retenues en V0 (dont 3 remontées de V2), 129 reportées en V1/V2, avec la liste par domaine au § 12.
18. Estimation : V0 ≈ 138 j-agent (≈ 160 avec les relectures) en 15 lots, V1 ≈ 115 à 135, V2 ≈ 70 à 90.
19. Risques majeurs : envoi hors CRM, art. 14 en retard, port 25, fuite entre locataires, réputation partagée.
20. Les horloges hors code (domaines de 21 jours, port 25) sont à lancer dès maintenant par Will.
