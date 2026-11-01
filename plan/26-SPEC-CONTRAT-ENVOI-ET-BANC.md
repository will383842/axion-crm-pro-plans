# 26 : SPEC LOT E1 : contrat d'envoi, banc d'essai, chauffe, DNS, gardes (01/11/2026)

**Lot servi : E1** du plan de référence `plan/20-PLAN-CORRIGE-UNIQUE.md` (§ 3.1, « Contrat serveur d'envoi, simulateur, kit de conformité, banc fermé à Internet avec 20 scénarios, mode témoins seulement verrouillé côté serveur »). Ce fichier sert aussi d'entrée aux lots **E2** (KumoMTA), **E3/E3b** (registres et configuration), **E5** (retours), **E7** (chauffe), **E10** (repli Postfix), **C1 à C3** (campagnes et gardes) et au **§ 9** du plan 20 (port 25, moteur de secours).

**Sources** : `plan/20` (fait foi), `plan/03` § 3, § 6, § 8 à § 10 ; `plan/08` blocs A et F ; `plan/13` § 1 à § 3.

**Règles de rédaction** : dépôt **public**. Aucun secret, aucune IP, aucun nom de domaine réel, aucun mot de passe. Les exemples utilisent des domaines réservés aux essais (`*.test`, `*.example`) et des marqueurs entre chevrons (`<domaine-1>`, `<ip-envoi>`). **Rien n'est codé, aucun serveur touché, aucun e-mail envoyé.**

**Décisions de Will reprises telles quelles** : moteur **KumoMTA**, repli **Postfix + rspamd** ; **un seul serveur d'envoi** au départ, un second plus tard ; **une boîte par domaine**, au nom de Will ; **150 messages par boîte et par jour** en V0 ; chauffe à partir de **20 par jour** ; DMARC **none → quarantine → reject** ; **France seulement** ; relais tiers (F20) **en secours temporaire** seulement ; capacité de réponse **15 par jour**.

---

## 1. Le contrat `ServeurEnvoi` (agnostique du moteur)

### 1.1 Idée générale

- Le CRM ne connaît **que ce contrat**. Il ne sait pas si derrière il y a KumoMTA, Postfix, un relais tiers ou le simulateur.
- Changer de moteur = écrire une nouvelle **implémentation** et lui faire passer le **kit de conformité** (§ 3.5). On ne touche pas au CRM.
- Le contrat a **trois canaux**, tous dans le **tunnel privé** (WireGuard) entre le serveur du CRM et le serveur d'envoi. Aucun n'est exposé sur Internet.

| Canal | Sens | Transport | Pourquoi ce choix |
|---|---|---|---|
| **Injection** | CRM → serveur | SMTP sur le port 2525, STARTTLS obligatoire, AUTH PLAIN, un identifiant par espace (locataire) | Contre-pression native (réponse 4xx quand le serveur sature), standard pour tous les moteurs |
| **Commandes** | CRM → serveur | HTTPS + signature HMAC (§ 1.5), vers la **passerelle d'envoi** | Une seule façon de signer, quel que soit le moteur |
| **Événements** | serveur → CRM | HTTPS + signature HMAC, poussée par lots, plus tirage par curseur | Poussée = rapide ; tirage = rien ne se perd |

### 1.2 La passerelle d'envoi (proposition, à acter dans l'ADR de P1)

- Un **petit service** tourne sur le serveur d'envoi, à côté du moteur. C'est le même agent que celui du lot E3b (il tire la configuration signée).
- Il **implémente le contrat** côté serveur : il vérifie les signatures, appelle le moteur **en local** (adresse locale « localhost »), signe et pousse les événements.
- Avantage : la signature HMAC, la séquence, l'anti-rejeu et le journal des commandes sont écrits **une seule fois** et servent à KumoMTA, à Postfix et au relais tiers.
- Le moteur (KumoMTA ou Postfix) n'écoute **jamais** ses API d'administration ailleurs qu'en local.
- La passerelle n'a **aucune** commande pour lire une clé DKIM privée, changer le socle local (§ 1.8) ou ouvrir un port.

### 1.3 Opérations

| Opération | Canal | Entrée | Sortie | Délai maximal |
|---|---|---|---|---|
| `injecter(message)` | Injection | Message **déjà composé** par le CRM (RFC 5322 complet, non signé DKIM) ; enveloppe `MAIL FROM` en VERP (`rb-<jeton>@bounce.<domaine>`) ; `RCPT TO` ; en-tête `X-Envoi-Jeton: <jeton>` ; identité AUTH = espace | `250` + identifiant de file, ou `4xx` (report), ou `5xx` + motif (refus) | 30 s par message |
| `etatEnvoi(jetons[])` | Commandes | 1 à 500 jetons | Pour chaque jeton : `inconnu`, `en_file`, `livre`, `report`, `rebond`, `retire`, `expire` | 10 s |
| `retirer(cible)` | Commandes | Jetons, ou empreinte d'adresse, ou campagne, ou espace | Nombre de messages retirés | **5 min** (de bout en bout) |
| `pause(portee)` | Commandes | Portée : global, espace, IP, IP × fournisseur, domaine, boîte, campagne ; durée facultative | Accusé + état | 1 min |
| `reprise(portee)` | Commandes | Même portée + motif | Accusé + état | 1 min ; jamais au débit d'avant |
| `modeTemoins(actif, liste)` | Commandes | Liste blanche d'empreintes (témoins + Will) | Accusé | 1 min ; **ne peut être levé que par le socle local**, voir § 1.8 |
| `etat()` | Commandes | — | Files (nombre, âge du plus ancien), pauses actives, version et empreinte de la configuration, plafond restant **par espace** et global, homme mort armé ou non | 10 s |
| `sante()` | Commandes | — | Version du moteur, empreinte de l'image, disque, mémoire, file des événements en retard, battement | 5 s ; appelée toutes les 5 min |
| `validerConfiguration(paquet)` | Commandes | Paquet signé généré depuis la base (E3b) | `valide` ou liste d'erreurs ; **rien n'est appliqué** | 60 s |
| `appliquerConfiguration(paquet)` | Commandes | Même paquet | `applique` (nouvelle empreinte) ou `annule` (retour automatique à la version d'avant) | 5 min |
| `lireEvenements(curseur)` | Événements (tirage) | Curseur (`serveur_id`, `sequence`) | Jusqu'à 500 événements après le curseur | 30 s ; gardés **30 jours** |
| `recapitulatif(jour)` | Commandes | Date (heure de Paris) | Comptes par type, par espace, par domaine, par boîte | 30 s |
| `evenements` (poussée) | Événements | — | Lots de 1 à 500 événements (§ 1.4) | Toutes les 10 s s'il y a quelque chose |

### 1.4 Format des événements

**Enveloppe d'un lot poussé** (le corps brut est signé, § 1.5) :

```json
{
  "version": "1",
  "serveur_id": "envoi-1",
  "sequence_debut": 18231,
  "sequence_fin": 18233,
  "emis_le": "2027-01-13T10:42:15Z",
  "evenements": [ ... ]
}
```

**Champs communs à tout événement** :

| Champ | Type | Règle |
|---|---|---|
| `event_id` | UUID v7 | Unique. Sert à l'idempotence avec `source`. |
| `source` | texte | `envoi-1`, `releve-imap`, `relais-tiers`, `simulateur`, `import` |
| `sequence` | entier | Croissant **par source**, sans trou. Un trou déclenche un tirage immédiat. |
| `type` | énuméré | `injecte`, `livre`, `report`, `rebond_dur`, `rebond_mou`, `blocage`, `expire`, `plainte`, `reponse`, `desinscription`, `retire` |
| `horodatage` | ISO 8601 UTC | Moment du fait, pas de l'envoi du lot |
| `espace` | UUID | Imposé par l'identité AUTH, **jamais** lu dans un en-tête du message |
| `jeton_envoi` | base64url, ≥ 128 bits | Relie l'événement à un envoi. Absent seulement pour une plainte ou une réponse non rattachée. |
| `destinataire_empreinte` | SHA-256 hex | **Jamais d'adresse en clair** |
| `domaine_envoi_ref`, `boite_ref`, `ip_ref` | identifiants internes | Jamais le nom du domaine ni l'IP en clair dans les journaux |

**Exemples par type** (valeurs fictives) :

```json
{ "event_id": "0190a1b2-...", "source": "envoi-1", "sequence": 18231, "type": "livre",
  "horodatage": "2027-01-13T10:42:05Z", "espace": "…", "jeton_envoi": "Zm9v…",
  "destinataire_empreinte": "9f2c…", "fournisseur": "microsoft",
  "smtp_code": 250, "tentatives": 1 }

{ "type": "rebond_dur", "smtp_code": 550, "dsn": "5.1.1",
  "classe": "adresse_inconnue", "synchrone": true,
  "diagnostic": "texte expurgé, sans adresse", "...": "champs communs" }

{ "type": "report", "smtp_code": 451, "dsn": "4.7.1", "classe": "limite_debit",
  "tentative": 2, "prochain_essai": "2027-01-13T11:12:05Z", "...": "champs communs" }

{ "type": "plainte", "origine": "arf|abuse|postmaster|reponse_hostile|hebergeur|listage",
  "authentifiee": true, "feedback_id": "…", "...": "champs communs" }

{ "type": "reponse", "source": "releve-imap", "classe": "humaine|absence|stop|hostile|rebond_asynchrone",
  "message_id_reponse_empreinte": "…", "boite_ref": "…", "en_reponse_a_jeton": "Zm9v…",
  "...": "champs communs" }
```

- `rebond_mou` et `rebond_dur` ont les mêmes champs. La **classe** vient du classifieur du moteur ; la décision dur ou mou se refait côté CRM avec la table `smtp_response_patterns` (CHA-025).
- `reponse` et la plupart des `plainte` ne viennent **pas** du serveur d'envoi : elles viennent de la **relève IMAP** (aucun port entrant public en V0, plan 20 R9). Elles utilisent le **même format** et entrent par le **même service** `AppliquerRetour`.
- **Ordre final par envoi (monotone)** : `plainte` > `desinscription` > `rebond_dur` > `livre` > `report`. Un `livre` reçu après un `rebond_dur` ne rétablit rien.

### 1.5 Signature HMAC (dans les deux sens)

**En-tête** (jamais dans l'URL) :

```
X-Envoi-Signature: k=<id-cle>,t=<unix>,s=<serveur_id>,n=<nonce>,v1=<hex>
```

- **Chaîne signée** : `t + "." + s + "." + n + "." + corps_brut`, en HMAC-SHA256.
- **Secret** : un par **espace et par serveur**. Il vit hors du dépôt (environnement du serveur du CRM, fichier `0600` sur le serveur d'envoi). Il n'apparaît jamais dans un journal.
- **Rotation** : deux clés actives au plus (`k=` ancienne et nouvelle) pendant 7 jours, puis l'ancienne est retirée.
- **Fenêtre** : écart de plus de **5 minutes** entre `t` et l'horloge du receveur → refus `401`.
- **Anti-rejeu** : le nonce est gardé 10 minutes ; un nonce déjà vu → refus `409`. Pour les lots d'événements, `(serveur_id, sequence)` sert aussi d'anti-rejeu.
- **Secret absent ou vide → refus** (jamais « ouvert par défaut », bug 4 de SOS-Expat).
- **Identité** : `s=` est comparé à l'identité attendue du canal. Un serveur ne peut pas parler au nom d'un autre.
- **Comparaison** en temps constant.

### 1.6 Idempotence

| Cas | Règle |
|---|---|
| Injection rejouée (coupure réseau après le `DATA`) | Côté CRM : un envoi passe `a_injecter` → `injection_en_cours` → `accepte`. Après une coupure, le CRM appelle **`etatEnvoi(jeton)`** avant de réinjecter. Côté serveur, second verrou : un `X-Envoi-Jeton` déjà accepté dans les 7 derniers jours renvoie `250` avec le même identifiant de file, **sans nouvel envoi**. |
| Événement en double | Clé unique `(source, event_id)` en base. Doublon → `200` sans effet. |
| Lot en double | `(serveur_id, sequence)` déjà vu → `200` sans effet. |
| Commande rejouée | Chaque commande porte un `commande_id` (UUID). Même `commande_id` → même réponse, sans refaire l'action. |
| Ré-import de l'ancien fichier | Source `import`, même clé d'idempotence : plus de double comptage. |

### 1.7 Délais et reprises

| Situation | Comportement |
|---|---|
| Injection : `4xx` (saturation, contre-pression) | **Report de la tranche** (CHA-030), jamais un échec. Nouvel essai à la tranche suivante. 3 reports de suite → pause de la vague + alerte. |
| Injection : `5xx` | Refus définitif de **ce** message. 3 refus `5xx` d'injection en 10 min → pause de la vague + alerte (c'est un bug de configuration). |
| Injection : délai dépassé (30 s) | `etatEnvoi(jeton)` puis décision. Jamais de boucle. |
| Livraison vers Internet | Réessais du moteur : 10 min, puis montée exponentielle jusqu'à 1 h ; **expiration après 24 h** (`expire`). |
| Poussée des événements | Le serveur rejoue avec un délai croissant (10 s, 30 s, 1 min, 5 min, 15 min, puis toutes les heures) pendant **72 h**. Le CRM ne répond `2xx` qu'**après** l'écriture en base (`COMMIT`). |
| Trou de séquence | Le CRM tire tout de suite `lireEvenements(curseur)`. |
| Réconciliation | Chaque nuit à 02:30 : `recapitulatif(veille)` comparé au journal du CRM. Écart → alerte. |
| Commandes | Délai de 10 s, 3 essais avec le même `commande_id`, puis alerte. |
| Homme mort | Le CRM appelle `sante()` toutes les 5 min. Sans appel pendant **15 min** en fenêtre d'envoi, la passerelle met **toutes** les files en pause. |
| Canal des retours muet | Aucun événement depuis **2 h** pendant une campagne → arrêt automatique (CHA-048, cas 5). |
| Retrait urgent | Une nouvelle opposition retire les messages en attente en **moins de 5 min**. |

### 1.8 Le socle local (ce que le CRM ne peut jamais changer)

Ces réglages sont **sur le serveur**, hors du paquet de configuration. Une commande ou un paquet qui tente de les changer est refusé et lève une alerte de dérive.

- Plafond **journalier dur** global et par espace (le CRM ne peut pas le dépasser, même par erreur).
- Refus de tout `MAIL FROM` hors registre ; refus permanent du domaine principal d'Axion et de ses sous-domaines.
- Aucun relais sans AUTH ; `relay_hosts` (ou équivalent) = localhost seulement.
- **Mode témoins** : quand il est actif, tout `RCPT` hors liste blanche est refusé **par le serveur**. Le CRM peut l'**allumer**, jamais l'**éteindre** : l'extinction est un geste local, journalisé (plan 13 § 3.2, étape 3).
- Envoi en IPv4 seulement ; IP d'envoi différente de l'IP de gestion.
- Clés DKIM privées générées sur le serveur, jamais exportées.

### 1.9 Ce que le CRM envoie, ce qu'il reçoit

| Le CRM **envoie** | Le CRM **reçoit** |
|---|---|
| Messages composés (en-têtes, corps, `List-Unsubscribe`, `List-Unsubscribe-Post`, `Feedback-ID`, `X-Envoi-Jeton`) | Accusé d'injection (`250` / `4xx` / `5xx`) |
| Commandes signées : `retirer`, `pause`, `reprise`, `modeTemoins`, `etatEnvoi` | Événements normalisés (livre, report, rebonds, blocage, expire, retire) |
| Paquet de configuration signé (domaines, sélecteurs DKIM publics, IP, PTR attendus, débits par fournisseur, plafonds souhaités) | Clé **publique** DKIM de chaque sélecteur, pour le plan DNS |
| Appels `sante()` toutes les 5 min (qui arment l'homme mort) | État des files, pauses, plafonds restants, empreinte de configuration |
| — | Récapitulatif du jour (réconciliation) |
| **Jamais** : un secret en clair dans un message, une adresse en clair dans une commande (empreintes seulement), un ordre de lever le mode témoins | **Jamais** : une clé privée, une adresse en clair dans un événement |

---

## 2. Traduire le contrat vers KumoMTA, puis vers Postfix + rspamd

### 2.1 Vers KumoMTA (lot E2, déjà chiffré à 20,5 j)

| Élément du contrat | KumoMTA | Point d'attention |
|---|---|---|
| Injection SMTP AUTH | `start_esmtp_listener` sur l'IP WireGuard, port 2525 ; `smtp_server_auth_plain` en Lua ; certificat d'une autorité privée | AUTH seulement après STARTTLS ; refuser `authz ≠ authc` ; mots de passe en empreinte |
| Espace imposé | `msg:set_meta('tenant', …)` depuis `authc` ; en-tête `X-Tenant` retiré | Garde F1 ; scénario B4 |
| Idempotence du jeton | Lua à la réception : table locale des jetons acceptés 7 jours | Ne rien mettre de personnel dans `X-KumoRef` |
| `retirer` | `POST /api/admin/bounce/v1` (par campagne, espace ou domaine) ; par jeton via `inspect` puis rebond administratif | L'événement `retire` vient du journal `AdminBounce` |
| `pause` / `reprise` | `POST` / `DELETE /api/admin/suspend/v1` et `suspend-ready-q` | Pause IP × fournisseur = suspension de la file prête de la source |
| `etat`, `sante` | `metrics.json`, `check-liveness`, `ready-q-states` | Ne **jamais** lire la sortie de `kcli` (instable) |
| `validerConfiguration` | `kumod --policy … --validate` à côté du service actif | Change d'écouteur = redémarrage |
| `appliquerConfiguration` | Fichiers TOML `sources`, `queues`, `shaping` + `bump-config-epoch` ; retour à l'ancienne version si la vérification échoue | Fichier de *shaping* de l'éditeur figé par empreinte |
| Événements | *Log hook* natif vers la passerelle en local ; la passerelle signe et numérote | Règle de *shaping* pour la file du hook |
| Classement des rebonds | `configure_bounce_classifier` + règles TOML | Validateur de fichier en CI (F4) |
| Homme mort, plafond du jour, registre `MAIL FROM`, mode témoins | Lua + minuterie (absent en natif) | Tests aux bornes, redémarrage, changement de jour (F5) |
| API d'administration | Écoute en local (« localhost ») seulement ; `trusted_hosts` = localhost | Jamais le réseau WireGuard dans `trusted_hosts` |

**Répartition indicative de E2** : image figée et réseau hôte 1,5 j ; écouteur, TLS, AUTH, espace 3 j ; anti-relais en 4 couches 2 j ; DKIM sur le serveur 1,5 j ; Lua socle (plafond, registre, homme mort, témoins) 4 j ; adaptateur passerelle ↔ API admin 2,5 j ; *log hook* et classifieur 2 j ; *shaping* et règles TSA 2 j ; kit de conformité et scénarios B1 à B20 2 j. **Total ≈ 20,5 j.**

### 2.2 Vers Postfix + rspamd (lot E10, plan de repli)

| Élément du contrat | Postfix + rspamd | Point d'attention |
|---|---|---|
| Injection SMTP AUTH | Service `submission` sur l'IP WireGuard, port 2525 ; SASL (Dovecot en mode authentification seule) ; `smtpd_tls_auth_only = yes` | `mynetworks` = localhost seulement |
| Espace imposé | `smtpd_sender_login_maps` + `reject_sender_login_mismatch` ; espace déduit du login SASL | Retirer `X-Tenant` par `header_checks` |
| Registre `MAIL FROM` | Même table `smtpd_sender_login_maps`, générée depuis la base | Domaine principal d'Axion en refus fixe |
| DKIM | Module `dkim_signing` de rspamd en *milter* ; clés générées sur le serveur | Signer les mêmes en-têtes qu'avec KumoMTA |
| Plafond du jour, mode témoins, idempotence du jeton | **Service de politique** (`check_policy_service`) écrit par nous + module `ratelimit` de rspamd en second verrou | Le jeton se lit à l'étape des en-têtes : contrôle dans rspamd (règle Lua), pas dans le service de politique |
| `retirer` | La passerelle garde la table `jeton → identifiant de file Postfix` (lue dans le journal) ; `postsuper -d` | Rapide tant que la file est petite (V0) |
| `pause` / `reprise` | `postsuper -h` / `-H` (mise en attente) ; pause par fournisseur = transport dédié + `defer_transports` | Moins fin que KumoMTA : pas de pause « IP × fournisseur » native |
| Débits par fournisseur | Transports par groupe de MX (`*_destination_concurrency_limit`, `*_destination_rate_delay`) | Valeurs du plan 13 § 1.9 |
| Événements | La passerelle lit le journal de Postfix (statut `sent`, `deferred`, `bounced`, `expired`) et le transforme en événements normalisés | Pas de poussée native : c'est le point le plus long à écrire |
| Classement des rebonds | DSN + texte du serveur distant passés à la table `smtp_response_patterns` | Même table que pour KumoMTA |
| `validerConfiguration` / `appliquer` | `postfix check`, `postmap`, `rspamadm configtest`, puis `postfix reload` ; retour arrière par copie de la version d'avant | |
| Réessais, expiration | `maximal_queue_lifetime = 1d`, `bounce_queue_lifetime = 1d` | |
| Homme mort | Minuterie de la passerelle → `postsuper -h ALL` | |

**Effort du repli (E10)** : SASL, TLS, anti-relais 1,5 j ; rspamd DKIM 1 j ; service de politique (plafonds, registre, témoins) 2 j ; lecteur de journal → événements, séquence, poussée 2,5 j ; adaptateur passerelle (retirer, pause, état, santé) 1,5 j ; kit de conformité et banc 1,5 j. **Total ≈ 10 j** (fourchette 8 à 13 j).

**Proposition** (plan 20 § 9, point 2) : avancer E10 en **V0 « b »**, juste après le premier envoi réel. Grâce à la passerelle commune, le coût réel est d'environ **+4 j** sur la V0 (le reste est déjà payé par E1 et E2). Sinon, écrire noir sur blanc que le risque « KumoMTA indisponible » est accepté jusqu'en mai. **Décision de Will.**

---

## 3. Le banc d'essai (faux serveur d'envoi, fausses boîtes)

### 3.1 But

Tester **toute la chaîne** (campagne → gardes → injection → serveur → faux destinataires → retours → relève → CRM) **sans port 25, sans domaine réel, sans Internet**. Le banc tourne en CI publique gratuite et sur un poste de travail. Il sert à E1 (simulateur), puis à E2 (vraie image KumoMTA), puis à E10 (Postfix).

### 3.2 Composants (`docker compose`, réseau `internal: true`)

| # | Composant | Rôle |
|---|---|---|
| 1 | **crm-banc** | Le vrai code du CRM, base Postgres jetable, données factices seulement |
| 2 | **simulateur** (faux serveur d'envoi) | Implémente tout le contrat en mémoire : injection SMTP, commandes signées, événements, socle local, mode témoins, homme mort. Rapide : sert à la CI de chaque lot. |
| 3 | **mta-banc** | La passerelle + l'image KumoMTA figée par empreinte (E2) ou Postfix + rspamd (E10). Même place que le simulateur. |
| 4 | **wg-banc** | Tunnel WireGuard entre crm-banc et mta-banc (clés générées à chaque démarrage, jamais commitées) |
| 5 | **dns-banc** | Résolveur local avec de fausses zones : `domaine-a.test`, `domaine-b.test` (nos faux domaines d'envoi), `gmail.test`, `outlook.test`, `yahoo.test`, `orange.test`, `exemple.test`. SPF, DKIM, DMARC, PTR, MTA-STS factices. |
| 6 | **puits SMTP programmables** | Faux serveurs des destinataires. Ils répondent selon la partie locale de l'adresse : `ok@`, `inconnu@` (`550 5.1.1`), `plein@` (`452`), `lent@` (`421` puis `250`), `reputation@` (`550 5.7.1`), `ms515@` (`550 5.7.515`), `coupe@` (coupure en plein `DATA`). Ils **vérifient** SPF, DKIM et DMARC avec dns-banc et notent le résultat. |
| 7 | **imap-banc** | Fausses boîtes : `will@domaine-a.test`, `will@domaine-b.test`, la boîte fourre-tout `*@bounce.domaine-a.test`, 4 boîtes témoins (`temoin@gmail.test`, etc.) |
| 8 | **faux-repondeur** | Dépose dans imap-banc, sur commande : réponse humaine, absence du bureau, STOP, réponse hostile, DSN différé, ARF, message à `abuse@` |
| 9 | **horloge simulée** | Avance le temps du CRM et du simulateur : jours effectifs, 72 h de retard, changement de jour, fériés |
| 10 | **sonde réseau** | Vérifie qu'aucune connexion ne sort vers une vraie IP, et qu'aucun port inattendu n'est ouvert |
| 11 | **compteur** | Compare prévus, injectés, reçus par les puits, journalisés : doit donner 100 % |

### 3.3 Les 20 scénarios de chaîne (E1)

Ils tournent d'abord sur le **simulateur**, puis sur **mta-banc**. Les scénarios B1 à B20 du plan 13 § 3.1 (propres à KumoMTA : AUTH, ACL, contre-pression, dérive) s'y ajoutent dans E2.

| # | Scénario | Réussite si |
|---|---|---|
| S01 | Campagne de 20 adresses `ok@` validée puis lancée | 20 injectées, 20 `livre`, comptes à 100 % |
| S02 | Signature des messages reçus par les puits | `spf=pass`, `dkim=pass`, `dmarc=pass` alignés sur `domaine-a.test` |
| S03 | Adresse en opposition dans la liste | Jamais injectée (vérifié au puits) |
| S04 | Opposition posée pendant que le message est en file | Retiré en moins de 5 min ; événement `retire` |
| S05 | POST RFC 8058 sur la page `go.domaine-a.test` | Opposition écrite en moins d'une minute |
| S06 | `inconnu@` | `rebond_dur` → suppression sur toutes les fiches |
| S07 | `plein@` trois fois | 3e rebond mou → suppression |
| S08 | `lent@` | `report` puis `livre` ; état final `livre` |
| S09 | DSN différé déposé dans la boîte `bounce.` | Relevé par IMAP, rattaché par VERP, rebond appliqué |
| S10 | ARF déposé, puis réponse hostile, puis message à `abuse@` | Trois `plainte` comptées (toutes sources) ; 1re = palier tenu ; 2e en 7 jours = arrêt 48 h du domaine |
| S11 | Réponse humaine d'un destinataire | Apparaît dans « Réponses », séquence arrêtée pour ce contact |
| S12 | Réponse « STOP » | Opposition écrite |
| S13 | Absence du bureau | Séquence en pause, pas d'arrêt |
| S14 | Webhook : signature fausse, horodatage vieux de 6 min, nonce rejoué | `401`, `401`, `409` ; rien appliqué |
| S15 | Webhook : doublons, désordre, trou de séquence, 72 h de retard | Idempotence, état final monotone, tirage immédiat, rattrapage |
| S16 | « Tout arrêter » | Plus aucune connexion vers les puits (mesuré dans les puits) |
| S17 | CRM muet 15 min en fenêtre | Homme mort : files en pause |
| S18 | Mode témoins actif, campagne vers 20 adresses | Seuls les témoins reçoivent ; les 20 autres refusés **par le serveur** ; le CRM ne peut pas lever le mode |
| S19 | Plafond du jour atteint (chauffe et 150 par boîte) | Le surplus est reporté au lendemain, jamais envoyé |
| S20 | Deux espaces (Axion + client factice) | Aucune fuite de file, d'opposition, d'événement ni de configuration |

### 3.4 Critères de réussite du banc

1. Les **20 scénarios verts 3 fois de suite**, sur le simulateur **et** sur mta-banc (KumoMTA).
2. **Aucune** connexion sortante réussie vers Internet (sonde réseau).
3. Comptes **prévus = injectés = reçus = journalisés** à 100 %.
4. Durée de la suite en CI : **moins de 15 minutes**.
5. Toutes les images figées **par empreinte** (jamais `latest`).
6. Aucun secret dans le dépôt : clés et mots de passe générés au démarrage du banc, détruits à l'arrêt ; Gitleaks vert.
7. Le **kit de conformité** (§ 3.5) passe sur le simulateur ; il passera ensuite sur KumoMTA (E2) et Postfix (E10).

### 3.5 Kit de conformité

- Une suite de tests **écrite contre le contrat**, pas contre un moteur : chaque opération du § 1.3, chaque règle des § 1.5 à 1.8.
- Elle prend en paramètre l'adresse de la passerelle et du port d'injection.
- Une implémentation n'est acceptée que si **tout** le kit est vert. Une montée de version du moteur aussi.

### 3.6 Calendrier jusqu'au 11 décembre

| Semaine | Livré |
|---|---|
| S2 (9-13 nov) | Contrat écrit en code (interfaces, formats JSON, signature), simulateur minimal (injection + événements) |
| S3 (16-20 nov) | Kit de conformité, socle local du simulateur, dns-banc, puits programmables |
| S4 (23-27 nov) | imap-banc, faux-répondeur, horloge simulée, sonde réseau ; S01 à S10 verts sur le simulateur |
| S5 (30 nov-4 déc) | S11 à S20 sur le simulateur ; mta-banc avec l'image KumoMTA (début E2) |
| S6 (7-11 déc) | **Banc OK** : 20 scénarios verts sur le simulateur, S01 à S08 et S14 à S18 verts sur KumoMTA |

**Honnêteté** : les scénarios qui dépendent de E7 (chauffe) et E8 (surveillance) — S10 et S19 en partie — sont écrits pour le 11 décembre mais ne seront verts sur KumoMTA qu'en S10 (début janvier). Le banc du 11 décembre est donc « **OK sans les derniers réglages** » (plan 20 § 9, point 10).

---

## 4. Courbe de chauffe et plafonds par boîte

### 4.1 Règles

- Les jours sont des **jours effectifs** : un jour où l'on a envoyé au moins 50 % du budget. Un jour sans envoi ne compte pas.
- **Budget du jour = le plus petit** de : courbe, plafond par boîte × nombre de boîtes, plafond par domaine, plafond du serveur, capacité de réponse (§ 6.5). Le goulot est affiché.
- **V0** : 1 serveur, 1 IP, 2 domaines, **1 boîte par domaine au nom de Will**, **150 par boîte et par jour** au plus. Plafond technique V0 : **2 × 150 = 300 par jour**.
- Domaines âgés d'au moins **21 jours** (30 conseillés) avant le premier jour.
- **Hausse le lendemain, baisse tout de suite.** Une remontée de palier par jour au plus.
- Le total compte **premiers messages et relances**. Les messages aux témoins et « m'envoyer un test » sont **hors** chauffe.

### 4.2 Tableau

| Palier | Jours effectifs | Total par jour | Par boîte (2 boîtes) | Plafond par boîte | Ressources |
|---|---|---|---|---|---|
| P1 | 1 à 5 | **20** | 10 | 150 | 1 IP, 2 domaines, 2 boîtes |
| P2 | 6 à 10 | 35 | 18 | 150 | idem |
| P3 | 11 à 15 | 50 | 25 | 150 | idem |
| P4 | 16 à 20 | 80 | 40 | 150 | idem |
| P5 | 21 à 25 | 120 | 60 | 150 | idem |
| P6 | 26 à 30 | 180 | 90 | 150 | idem |
| P7 | 31 à 35 | **250** | 125 | 150 | idem (**fin de la montée V0**) |
| P8 | 36 à 40 | 300 | 150 | 150 | idem : **plafond V0 atteint** |
| P9 et + | 41 et + | 350 → 600-800 | 150 | 150 (300 en V1 si mesures vertes) | 3e domaine et 3e boîte (achetés avant le 15 mars), puis 2e serveur ; plafond utile **600 à 800** tant que Will est seul |

### 4.3 Freins (valeurs dans la table versionnée `emailing_seuils`)

| Frein | Seuil (taux) | Échantillon minimal | Règle absolue sous l'échantillon | Effet |
|---|---|---|---|---|
| **Rebonds durs** | **> 2 %** sur 7 jours glissants | 100 (livrés + rebonds) | ≥ 3 rebonds durs dans la journée sur une ressource | **Retour au palier précédent** ; 3 jours effectifs verts avant de remonter |
| Pic de rebonds durs | > 5 % sur 24 h | 50 | ≥ 5 dans la journée | Pause de la **campagne** et revérification de ses adresses |
| **Plaintes (toutes sources)** | **> 0,1 %** sur 7 jours | 1 000 livrés | **1 plainte** → palier tenu 3 jours + Will relit ; **2 plaintes en 7 jours** → arrêt 48 h du domaine, reprise au palier inférieur | Comme ci-contre |
| Reports par fournisseur | > 20 % sur 1 h vers un même fournisseur | 20 | 3 refus de réputation en 1 h | Pause de l'IP **vers ce fournisseur seulement** |
| Listage (liste noire) | 1 listage d'IP ou de domaine | — | — | Pause de la ressource + procédure « listé » |
| Témoin en indésirables | 2 jours sur 3 | — | — | Palier tenu + relecture du message |
| Inactivité | 7 jours ouvrés sans envoi → 75 % ; 30 jours → 25 % ; 90 jours → retour à P1 | — | — | Recul automatique |

Les seuils se testent **aux bornes** : 1,99 % / 2,01 % ; échantillon 99 / 100 ; 1 puis 2 plaintes ; 0,09 % / 0,11 %.

---

## 5. Liste de contrôle DNS et authentification (par domaine d'envoi)

À refaire **pour chaque domaine**. Aucune valeur réelle ici : les valeurs sont générées par E3 et contrôlées chaque jour (contrôle DNS quotidien, plan 20 § 9, point 7).

| # | Enregistrement | Nom | Valeur modèle | Contrôle | Quand |
|---|---|---|---|---|---|
| 1 | Âge du domaine | — | — | ≥ 21 jours (30 conseillés) | avant P1 |
| 2 | Site visible | `<domaine>` et `www` | page de présentation, mentions légales, art. 14 | réponse HTTPS 200 | avant P1 |
| 3 | MX racine | `<domaine>` | hébergeur des boîtes (réponses) | une réponse arrive dans la boîte de Will | avant témoins |
| 4 | MX rebonds | `bounce.<domaine>` | hébergeur des boîtes, boîte fourre-tout | un DSN de test arrive dans la boîte `bounce.` | avant témoins |
| 5 | SPF rebonds | `bounce.<domaine>` | `v=spf1 ip4:<ip-envoi> -all` | `spf=pass` chez les témoins | avant témoins |
| 6 | SPF racine | `<domaine>` | `v=spf1 include:<hebergeur-boites> -all` | les réponses de Will passent SPF | avant témoins |
| 7 | DKIM serveur | `<selecteur-serveur>._domainkey.<domaine>` | clé publique RSA 2048 générée **sur** le serveur | `dkim=pass`, `d=<domaine>` aligné | avant témoins |
| 8 | DKIM hébergeur | `<selecteur-hebergeur>._domainkey.<domaine>` | clé publique fournie par l'hébergeur des boîtes | les réponses de Will passent DKIM | avant témoins |
| 9 | DMARC | `_dmarc.<domaine>` | **dès l'achat** : `v=DMARC1; p=none; rua=mailto:dmarc@<domaine>; adkim=s; aspf=r; fo=1` | rapports reçus et lus (E8) | dès l'achat |
| 10 | DMARC étape 2 | idem | `p=quarantine` | **4 semaines** à 100 % d'alignement **et** au moins 500 messages | V0, après la montée |
| 11 | DMARC étape 3 | idem | `p=reject` | 4 semaines de plus sans source inconnue | V1 |
| 12 | PTR | `<ip-envoi>` | `mta1.<domaine-1>` | PTR = HELO = A (FCrDNS) | réglé chez l'hébergeur du serveur, avant témoins |
| 13 | A du serveur | `mta1.<domaine-1>` | `<ip-envoi>` | idem | avant témoins |
| 14 | MTA-STS | `_mta-sts.<domaine>` + `mta-sts.<domaine>/.well-known/mta-sts.txt` | `mode: testing`, puis `enforce` | politique lisible en HTTPS | V0 en `testing` |
| 15 | TLS-RPT | `_smtp._tls.<domaine>` | `v=TLSRPTv1; rua=mailto:tls-rpt@<domaine>` | rapports reçus | avec MTA-STS |
| 16 | Désinscription | `go.<domaine>` | page publique du CRM | POST RFC 8058 → effet en moins d'une minute | avant témoins |
| 17 | Hors domaine principal | — | aucun lien ni adresse vers le domaine principal d'Axion | garde G1 | toujours |
| 18 | Listes noires | IP et domaine | absents de Spamhaus (SBL, CSS, DBL), Barracuda, SpamCop | contrôle quotidien | avant P1 puis chaque jour |
| 19 | Inscriptions | — | SNDS et JMRP (Microsoft), CFL (Yahoo), Postmaster (Google) | compte actif | dès l'IP attribuée |
| 20 | BIMI | — | **non** (inutile à ce volume) | — | — |

**Garde anti-dispersion** : au plus 2 domaines par IP ; au plus 1 ressource nouvelle par 15 jours ouvrés ; domaines achetés à des jours ou chez des registraires différents, noms non en série.

---

## 6. Gardes d'envoi

Toutes passent par **une seule porte** : `EnvoiAutorise` (qui appelle `peutRecevoir()`), à la vague **et** moins de 15 minutes avant l'injection. Chaque garde a un test rouge puis vert.

### 6.1 Par entité (espace)

| Garde | Règle | Test |
|---|---|---|
| Entité expéditrice | Chaque message porte l'entité légale de l'espace (SAS pour Axion) et son pied légal | message sans entité → refusé |
| Bloc art. 14 | Exigé pour tout destinataire non encore informé ; alerte à J+21, refus à J+30 | premier message sans bloc → refusé |
| Plafond par espace | Plafond dur dans le socle local du serveur + plafond en base | dépassement → reporté au lendemain |
| Arrêt par espace | L'arrêt de l'espace A n'arrête pas B ; l'arrêt général arrête tout | scénario S20 |
| Oppositions par espace | L'opposition de A ne bloque pas B ; celle d'Axion gagne partout dans l'espace Axion | test P2 |

### 6.2 Par domaine

| Garde | Règle |
|---|---|
| Registre | `MAIL FROM`, `From`, `Reply-To` et liens seulement sous un domaine **du registre** de l'espace, refusés ailleurs par le CRM **et** par le serveur |
| Domaine principal | Le domaine principal d'Axion (et celui de chaque client, sauf case tracée) n'est **jamais** domaine d'envoi |
| Prêt à envoyer | Âge ≥ 21 jours, DMARC présent, SPF et DKIM vérifiés au contrôle du jour, absent des listes noires ; sinon le domaine est en pause |
| Plafond | Le domaine suit son palier de chauffe ; recul tout de suite sur un frein |

### 6.3 Pays : France seulement

- Le destinataire doit avoir une **fiche rattachée à la France** : SIREN valide ou adresse de l'organisation en France. Le domaine de l'adresse (`.fr` ou non) **ne suffit pas**.
- Pays inconnu → **refusé** (jamais « par défaut France »).
- Suisse, Canada, Belgique et autres : **refusés** en V0 (fiches pays en V2, lot J5).
- Test : une fiche hors France ou sans pays n'est jamais injectée.

### 6.4 Personnes protégées (jamais contactées)

| Cas | Règle |
|---|---|
| Opposition, désinscription, plainte | Jamais contactée, dans tout l'espace ; empreinte gardée |
| Suppression (rebond dur, 3e mou) | Jamais contactée ; levée rare, motivée, tracée, **jamais** pour une plainte |
| Sirene « diffusion partielle » | Jamais contactable, sans supprimer la fiche (C3) |
| Segments sensibles | Syndicats de salariés, santé, INSEE, Roumanie : **fermés par défaut** ; ouverture = case tracée de l'owner, par espace. Presse ouverte pour l'espace Axion seulement |
| Adresse de webmail grand public | Refusée en premier contact à froid |
| Clients de la console | Jamais destinataires (garde existante) |
| Adresse non vérifiée | Verdict `valide` de moins de 30 jours exigé ; `inconnu` et `accepte_tout` à 0 % pendant la chauffe |

### 6.5 Frein « réponses en attente » (frein humain)

- **Capacité de réponse** : **15 réponses par jour** par personne réelle (décision de Will ; une seule personne en V0).
- **Premiers messages du jour** ≤ `min(courbe, capacité ÷ taux de réponse observé sur 14 jours)` ; taux par défaut 2 % tant qu'on n'a pas assez de mesures. Exemple : 15 ÷ 2 % = 750 → pas limitant en V0 ; il le devient vers 600-800 par jour.
- **Réponses en attente** = réponses humaines non traitées depuis plus de 24 h ouvrées.
  - **≥ 10 réponses « intéressées » en attente** → **aucun nouveau premier message** ; les relances déjà prévues continuent.
  - **≥ 15 réponses en attente** (tous types) → relances suspendues aussi.
  - Retour à la normale le lendemain du jour où l'attente redescend sous le seuil.
- **Mode absence** de Will → tout l'envoi de l'espace en pause (rien n'est perdu).
- Test aux bornes : 9 / 10 et 14 / 15 réponses en attente.

---

## 7. Plan de repli si le port 25 tarde : relais tiers temporaire (F20)

### 7.1 Pourquoi

La demande de port 25 part en S5 ; la réponse prend 5 à 7 semaines (accord entre le 6 et le 22 janvier), avec un refus possible. Un seul serveur est prévu au départ. Will a accepté le relais tiers **en secours temporaire** (décision 41). Le plan 13 l'excluait pour le froid : la décision de Will prime, **avec les conditions ci-dessous**.

### 7.2 Conditions (toutes obligatoires)

1. **Date de décision : 18 janvier.** Si le serveur propre n'est pas prêt (port 25 ouvert par écrit, B1 à B20 verts), on active le relais.
2. **Fournisseur choisi par Will** sur ces critères : hébergé dans l'UE ; contrat de sous-traitance signé ; **conditions d'utilisation qui acceptent par écrit** la prospection B2B à faible volume avec opposition en un clic (à demander au support **avant** de payer) ; DKIM sur **notre** domaine (`d=<domaine>` aligné) ; `MAIL FROM` personnalisé sous `bounce.<domaine>` ; suivi des ouvertures et réécriture des liens **désactivables** ; webhooks signés.
3. **Implémentation `relais-tiers`** du contrat (≈ 3 j, F20) qui passe le **kit de conformité**. Ce qui n'existe pas chez le relais (homme mort, mode témoins côté serveur) est tenu par la passerelle du CRM ; l'écart est écrit dans l'écran « Feu vert ».
4. **Toutes les gardes du CRM restent identiques** (§ 6), ainsi que la chauffe (§ 4) et les freins.
5. **Volume plafonné** : P1 à P3 seulement (≤ 50 par jour), **6 semaines au plus**.
6. **Aucun pixel, aucun lien réécrit** : vérifié sur un message reçu par un témoin.
7. Les **3 jours « témoins seulement »** se font aussi par le relais avant tout envoi réel.
8. DNS : ajout temporaire du relais dans le SPF de `bounce.<domaine>` et de son sélecteur DKIM ; **retirés** à la fin de la bascule.

### 7.3 Bascule vers le serveur propre

| Étape | Condition | Répartition |
|---|---|---|
| 0 | Port 25 ouvert par écrit, B1 à B20 verts sur la production, 7 jours de dérive verte | 100 % relais |
| 1 | 3 jours « témoins seulement » sur le serveur propre | 100 % relais pour les vrais destinataires |
| 2 | Témoins verts 3 jours de suite | Serveur propre au **palier P1 de l'IP** (20 par jour) ; le relais porte le reste du budget du domaine |
| 3 | 5 jours effectifs verts sur l'IP | Serveur propre P2 ; relais en baisse |
| 4 | Le palier de l'IP rattrape celui du domaine | **100 % serveur propre** ; relais coupé, DNS nettoyé, compte du relais fermé |

- La réputation du **domaine** continue ; celle de l'**IP** repart de zéro : c'est pourquoi l'IP suit sa propre courbe.
- Tout frein déclenché pendant la bascule **arrête la bascule** (on reste sur la répartition du moment).
- Effort total : ≈ **3 j** (implémentation) + **1 j** (bascule, tests, nettoyage), hors total du plan 20 (§ 3.3).

---

## 8. Ce qui ne peut être vérifié qu'avec de vrais domaines et un vrai serveur

Le banc ne prouve **pas** ces points. Ils sont dans l'écran « Feu vert » (plan 13 § 3.3) et se vérifient en production, à l'étape « témoins seulement » ou après.

1. Le **port 25** ouvert par écrit par l'hébergeur, et l'acceptation de l'usage déclaré.
2. Le **PTR** réel et la cohérence PTR = HELO = A (FCrDNS).
3. La **publication DNS** réelle (SPF, DKIM, DMARC, MTA-STS, TLS-RPT) et sa propagation.
4. L'**arrivée en boîte de réception** chez les 4 témoins (Gmail, Outlook.com, Yahoo, Microsoft 365), 3 jours de suite.
5. L'affichage du bouton **« Se désabonner »** de Gmail et le POST RFC 8058 envoyé par une vraie messagerie.
6. Les **rapports DMARC** et TLS-RPT réels (format, fréquence, sources inconnues).
7. L'absence réelle des **listes noires** (IP neuve parfois déjà listée par un ancien locataire).
8. Les **textes réels des rebonds** de Microsoft, Orange, OVH, etc., pour ajuster la table des motifs.
9. Le comportement réel de l'**hébergeur des boîtes** : boîte fourre-tout sur sous-domaine, IMAP `IDLE`, limites de connexions.
10. L'**anti-spam de l'hébergeur du serveur** (coupure automatique possible en pleine chauffe).
11. La **contre-pression** sous la vraie mémoire et le vrai disque du serveur.
12. Le **certificat TLS** réel de `mta-sts.<domaine>` et de `go.<domaine>`.
13. Les **inscriptions** SNDS, JMRP, CFL, Postmaster (Postmaster restera vide à ce volume).
14. Les **délais réels** des rebonds asynchrones et des plaintes.
15. Le **relais tiers** (si on l'active) : vraies conditions d'utilisation, vraie désactivation du suivi, vrai alignement DKIM.
16. La **sonde externe** : aucun relais ouvert, aucun port public autre que WireGuard (SSH limité au tunnel).
17. La **capacité réelle de Will** à traiter les réponses (elle fixe le vrai plafond de volume).
18. L'**homme mort** et « Tout arrêter » prouvés **en production**.

---

## 9. Effort et suite

| Lot | Contenu de ce fichier | j |
|---|---|---|
| E1 | Contrat (§ 1), simulateur, kit de conformité, banc et 20 scénarios (§ 3), mode témoins côté serveur | 10,5 (inchangé) |
| E2 | Traduction KumoMTA (§ 2.1) | 20,5 (inchangé) |
| E7 | Courbe et freins (§ 4), frein humain (§ 6.5) | 15,5 (inchangé) |
| E3 | Liste DNS (§ 5), contrôle quotidien, PTR | 5 + 3 (plan 20 § 9, point 7) |
| C3 | Gardes pays et personnes protégées (§ 6.3, § 6.4) | 4,5 (inchangé) |
| E10 | Repli Postfix (§ 2.2) | 10 (≈ +4 j si avancé en V0 « b ») |
| F20 | Relais temporaire (§ 7) | 3 + 1 (hors total) |

**Décisions à demander à Will** (courtes) :
1. Valider la **passerelle d'envoi** commune (§ 1.2) dans l'ADR de P1.
2. Avancer E10 (Postfix) en V0 « b » (≈ +4 j) ? **Recommandé : oui.**
3. Choisir le **fournisseur du relais tiers** avant le 11 janvier, pour être prêt le 18.
4. Valider les seuils du frein humain : 10 « intéressées » / 15 au total en attente.

---

## Résumé (15 lignes)

1. Ce fichier spécifie le lot E1 : contrat d'envoi, banc d'essai, chauffe, DNS, gardes, repli, limites.
2. Le CRM ne parle qu'au contrat `ServeurEnvoi` : injection SMTP AUTH, commandes signées, événements signés.
3. Proposition clé : une **passerelle** sur le serveur d'envoi qui signe et vérifie pour tous les moteurs.
4. Événements normalisés : livré, report, rebond dur et mou, blocage, plainte (toutes sources), réponse, désinscription.
5. HMAC-SHA256 dans l'en-tête, fenêtre 5 min, nonce, séquence par serveur, clé par espace et par serveur.
6. Idempotence par jeton d'envoi, `event_id`, séquence et `commande_id` ; rejeu des retours pendant 72 h.
7. KumoMTA : tout le contrat a un équivalent (E2, 20,5 j) ; Postfix + rspamd : ≈ 10 j, ≈ +4 j si avancé en V0 « b ».
8. Banc fermé à Internet : simulateur, KumoMTA figé, faux DNS, puits programmables, fausses boîtes IMAP, horloge simulée.
9. 20 scénarios de chaîne, verts 3 fois de suite, comptes à 100 %, moins de 15 min en CI.
10. Banc OK vers le 11 décembre, sans les derniers réglages de chauffe et de surveillance (verts début janvier).
11. Chauffe : 20 par jour au 1er jour effectif, 250 vers le 31e, plafond V0 = 2 boîtes × 150 = 300.
12. Freins : rebonds durs > 2 % → palier précédent ; plaintes > 0,1 % (ou 2 en 7 jours) → arrêt 48 h.
13. Liste DNS de 20 points par domaine, sans valeur réelle ; DMARC none → quarantine → reject.
14. Gardes : entité, domaine, France seulement, personnes protégées, frein humain à 15 réponses par jour.
15. Port 25 en retard : relais tiers temporaire décidé le 18 janvier, 6 semaines au plus, puis bascule par paliers ; 18 points restent à vérifier en réel.
