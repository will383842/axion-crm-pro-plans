# 13 : Vérification de l'envoi et de l'infrastructure (01/11/2026)

Rédigé par le responsable « envoi et infrastructure », en lecture seule. Aucun e-mail envoyé, aucun serveur touché, aucune commande réseau vers un serveur de messagerie, aucun secret recopié, aucun code applicatif écrit.

**Sources lues.**
- Plan : `00`, `01`, `03`, `05`, `06`, `08`, `10`, `11`, `REPRENDRE`.
- Code actuel `axion-crm-pro` (commit `ce80ca9`) : `.github/workflows/*`, `backend/config/mail.php`, `infra/`.
- Documentation officielle de KumoMTA, lue **dans son dépôt** (`KumoCorp/kumomta`, dossier `docs/`, commit `058a4de` du 26/10/2026). Le site `docs.kumomta.com` n'est pas joignable depuis cette session cloud (réseau non autorisé). Le contenu est le même, puisque le site est construit à partir de ce dossier.
- Recherche web pour Gmail, Yahoo, Microsoft, Hetzner et OVH. Les pages officielles (`support.google.com`, `senders.yahooinc.com`, `docs.hetzner.com`) sont **bloquées par le réseau de la session**. Les règles des messageries sont donc **de seconde main**, recoupées sur plusieurs sources ; seule la page Microsoft a été vue directement. Pour lever cette réserve, il faut autoriser ces domaines dans les réglages réseau de l'environnement, puis relancer la vérification.

**Niveaux de certitude.** « Vérifié » : lu dans la doc officielle ou le code. « Recoupé » : plusieurs sources secondaires concordent. « À vérifier » : hypothèse.

---

## 0. Verdict en une page

**La chaîne choisie est juste.** Elle va du CRM, par SMTP AUTH dans WireGuard, vers KumoMTA, qui signe en DKIM et envoie sur Internet. Les retours reviennent par webhook et par tirage. Les protections du plan dépassent ce que faisait SOS-Expat. KumoMTA a bien les fonctions dont le plan a besoin (vérifié) :
- API HTTP d'injection et d'administration ;
- `kcli` ;
- environ 140 métriques Prometheus ;
- contre-pression mémoire et spool ;
- validation de configuration à blanc (`kumod --validate`) ;
- contrôle d'accès par ACL depuis la version 2026.03.04.

**Elle n'est pas encore sûre telle qu'elle est écrite.** Cinq points sont faux ou dangereux, et il faut les corriger avant le lot E3 :

1. **`trusted_hosts` de l'API HTTP donne un accès SANS authentification à TOUTE l'API** : injection, rebond administratif, suspension. Si l'on y met le réseau WireGuard, tout ce qui touche le tunnel peut envoyer ou vider les files. Le plan ne le dit nulle part.
2. **SMTP AUTH n'est accepté par KumoMTA qu'après STARTTLS**, même dans le tunnel. Il faut un certificat sur l'écouteur interne. Le plan ne le prévoit pas. Autre piège : si l'IP WireGuard du CRM figure dans `relay_hosts`, le CRM peut relayer **sans** AUTH, ce qui supprime l'identité du locataire.
3. **La plupart des plaintes ne reviennent jamais en ARF.** Gmail n'envoie pas d'ARF par message. Les destinataires B2B français (Microsoft 365, Orange, OVH, hébergeurs) n'ont pas de boucle de retour. La règle « 0,1 % de plaintes ARF sur 1 000 livrés » ne se déclenchera presque jamais. Les vrais signaux sont les réponses « STOP » ou hostiles, les listages et les refus de réputation.
4. **Ports entrants : le plan se contredit.** 03 § 10.3 dit « aucun port public autre que SSH restreint et WireGuard ». 08 A7 et A10 font recevoir les DSN et les ARF par KumoMTA sur `bounce.<domaine>`, ce qui ouvre le port 25 entrant. 03 § 6 les fait relever par IMAP. Il faut choisir.
5. **La règle « aucune clé SSH dans GitHub » est déjà enfreinte par le code actuel.** 25 workflows utilisent `secrets.HETZNER_SSH_PRIVATE_KEY`, avec un accès `root` sur le serveur du CRM et `ssh-keyscan` sans empreinte épinglée. De plus, `deploy-direct-ssh.yml` alerte encore par **Telegram**. Ce modèle ne doit **jamais** être étendu au serveur d'envoi. La V1 du plan prévoit pourtant un « agent SSH » (03 § 13).

**Ce qui reste risqué**, même corrigé :
- le **port 25** (refus possible, au cas par cas) ;
- la **politique d'usage de l'hébergeur** face à la prospection à froid : une fermeture de compte est possible ;
- la **charge de réponses pour Will seul**, qui plafonne de fait le volume utile vers 500 à 800 premiers messages par jour ;
- le **faible volume**, qui rend les taux non significatifs et Postmaster muet ;
- **Ubuntu 24.04**, qui n'a **pas** de paquet officiel KumoMTA (vérifié) ;
- les règles Gmail et Yahoo, vues de seconde main seulement.

**Recommandation.** On garde KumoMTA et l'architecture. On applique les 27 corrections du § 5, dont 25 en V0, pour environ **19 jours-agent de plus en V0**. Une partie est compensée par ce que l'on retire : Grafana et Alertmanager en V0, 10 à 12 boîtes de réponse, l'agent SSH.

---

## 1. Justesse technique, point par point

### 1.1 Chaîne CRM → SMTP AUTH dans WireGuard → KumoMTA → Internet

| Point | Constat | Certitude | Correction |
|---|---|---|---|
| Injection SMTP AUTH | `smtp_server_auth_plain(authz, authc, password, conn_meta)` est un rappel Lua. KumoMTA « n'accepte AUTH PLAIN qu'une fois STARTTLS activé » et ne fournit pas de base d'utilisateurs : c'est à nous d'écrire la vérification. | Vérifié | **Certificat TLS sur l'écouteur interne** : une autorité privée créée sur le serveur, le CRM vérifie le certificat (aucune option « sans vérification »). **Refuser `authz ≠ authc`** : sinon un identifiant peut agir au nom d'un autre locataire. Mots de passe stockés **en empreinte** sur le serveur, jamais en clair dans le Lua (la doc le déconseille elle-même). Mise en cache par `kumo.memoize`. |
| `relay_hosts` | Par défaut, seul `127.0.0.1/::1` relaie sans AUTH. Une IP ajoutée à `relay_hosts` relaie **sans authentification**. | Vérifié | `relay_hosts` reste à **localhost seulement**. Le CRM n'y figure **jamais**. Test au banc : sans AUTH depuis l'IP WireGuard du CRM → refus. |
| Locataire | Le locataire et la file se posent par `msg:set_meta('tenant', …)` dans `smtp_server_message_received`. | Vérifié | Le locataire se déduit de `authc` (correspondance générée depuis la base), jamais d'un en-tête. Tout en-tête `X-Tenant` entrant est retiré (confirme 05 § B). |
| Écouteur | `start_esmtp_listener` peut écouter sur une adresse précise. Une authentification par certificat client est possible depuis 2025.10.06 (`tls_required_client_ca`). | Vérifié | Écoute sur l'**IP WireGuard seulement**, port 2525. Certificat client : facultatif en V0, recommandé en V1 (double facteur machine). |
| DKIM | La signature se fait dans le Lua (`msg:dkim_sign`), avec la clé lue depuis un fichier ou un coffre (`KeySource`). | Vérifié | Les clés sont générées **sur** le serveur. Le CRM ne reçoit que la clé **publique**, pour le plan DNS. Signer `From`, `To`, `Subject`, `Date`, `Message-ID`, `List-Unsubscribe`, `List-Unsubscribe-Post`, `Feedback-ID` (03 § 5). RSA 2048 en V0, Ed25519 en second sélecteur en V1 (RES-015). |
| Sortie | MTA-STS est appliqué par défaut en sortie (`enable_mta_sts = true`). DANE est facultatif (`enable_dane`). | Vérifié | Garder MTA-STS. DANE activé en V1, après essai au banc. |
| IPv4 seulement | Option `ip_lookup_strategy` sur le chemin de sortie. | Vérifié (existence de l'option) | La régler en IPv4 seulement (INF-016) et le tester. |
| WireGuard | Brique standard d'Ubuntu, sans difficulté. | — | Clés WireGuard générées sur chaque machine. On ne recopie que les clés **publiques** dans l'interface (§ 2). |

### 1.2 API HTTP d'injection et d'administration (vérifié en ligne, ce que les agents n'avaient pas fait)

- **Injection** : `POST /api/inject/v1`, corps JSON (`envelope_sender`, `content` en RFC 5322 ou construit, `recipients[]`). Réponse : `success_count`, `fail_count`, `failed_recipients`, `errors`.
  - **Piège 1** : l'API embarque le moteur de gabarits **MiniJinja**, actif par défaut. Le plan interdit tout moteur qui exécute du code sur des données (03 § 2.3, leçon Jinja2 de SOS-Expat). Si l'API HTTP sert un jour, `template_dialect = "Static"` est **obligatoire**.
  - **Piège 2** : `deferred_generation: true` répond tout de suite et supprime la contre-pression. On l'interdit.
  - **Décision proposée** : l'injection reste en **SMTP AUTH** (03 § 10.1). L'API HTTP ne sert qu'à l'**administration** et à la **lecture**.
- **Administration** : `suspend` et `suspend-ready-q` (POST, GET, DELETE), `bounce` (rebond administratif = retirer des messages), `rebind`, `inspect-message`, `inspect-sched-q`, `ready-q-states`, `bump-config-epoch`, `check-liveness`, `machine-info`, `memory/stats`, `metrics` et `metrics.json`. Les opérations `pause`, `reprise`, `retirer`, `etat` et `sante` du contrat `ServeurEnvoi` (03 § 10.1) **ont toutes un point d'API**. Correspondance : `retirer` = `POST /api/admin/bounce/v1` avec `campaign`, `tenant` ou `domain` ; `pause` = `POST /api/admin/suspend/v1`.
- **Authentification** : `trusted_hosts` (défaut : localhost) = « accès à toute l'API sans autre authentification ». Le reste passe par HTTP Basic (`http_server_validate_auth_basic`). Depuis 2026.03.04, les **ACL** `kumo.aaa` (`load_acl_map`) permettent de restreindre chaque point d'API à une identité et à un verbe.
  - **Réglage proposé** :
    - écoute sur `127.0.0.1` et l'IP WireGuard seulement ;
    - `trusted_hosts` = localhost seulement ;
    - identité « crm » en Basic sur TLS ;
    - ACL : la lecture (`metrics`, `inspect`, `ready-q-states`) et `suspend` / `bounce` sont permises ; `inject`, `rebind` et `xfer` sont refusés à « crm » ;
    - `check-liveness` est ouvert à la sonde.
- **`kcli`** (vérifié) : `/opt/kumomta/sbin/kcli`, point d'accès par défaut `http://127.0.0.1:8000`. Commandes : `queue-summary`, `bounce`, `bounce-list`, `bounce-cancel`, `suspend`, `suspend-list`, `suspend-cancel`, `rebind`, `inspect-message`, `inspect-sched-q`, `trace-smtp-client` et `trace-smtp-server`, `top`. **La doc précise que la sortie de `queue-summary` est instable et ne doit pas servir à l'automatisation.** Le CRM lit donc `metrics.json`, jamais la sortie de `kcli`. `kcli` reste l'outil de dépannage de Will, en local sur le serveur.
- **Métriques Prometheus** (vérifié, environ 142 noms) : `GET /metrics` au format texte Prometheus, et `metrics.json`. Les métriques utiles au plan existent :

  | Métrique | Usage |
  |---|---|
  | `scheduled_by_tenant`, `scheduled_by_tenant_campaign` | Files par locataire et par campagne (écran « Files ») |
  | `ready_full`, `delayed_due_to_ready_queue_full`, `delayed_due_to_message_rate_throttle` | Goulots |
  | `total_messages_delivered_by_provider`, `total_messages_fail_by_provider`, `total_messages_transfail_by_provider` | Santé par fournisseur |
  | `egress_source_health_suspended`, `egress_source_connection_failures_total` | Santé d'une IP |
  | `memory_usage`, `memory_limit`, `memory_over_limit_count`, `memory_low_count` | Contre-pression |
  | `disk_free_percent`, `rocks_spool_load_shed_active`, `rocks_spool_write_stopped` | Spool |
  | `log_hook_backlog_count`, `log_submit_full` | Santé du canal de retours (CHA-048 cas 5) |
  | `smtp_server_rejections`, `total_connections_denied` | Tentatives refusées (anti-relais) |

  **Conséquence** : **Prometheus, Grafana et Alertmanager ne sont pas nécessaires en V0** (contrairement à 08 A15). Le CRM lit `/metrics` par le tunnel toutes les 5 minutes et alerte dans la console et par e-mail, seuls canaux autorisés. Alertmanager ajouterait un troisième canal d'alerte à surveiller. Gain : environ 2 jours.
- **Contre-pression** (vérifié) :
  - au-dessus de la **limite mémoire douce** (75 % de la RAM par défaut), « le trafic entrant est refusé » : réponses temporaires SMTP 4xx ;
  - depuis 2026.09.22, une écriture au spool RocksDB bloquée **plus de 30 s** échoue (`store_deadline`) ;
  - l'injection HTTP synchrone attend que les messages soient en file.
  - **Conséquence pour le CRM** : un 4xx à l'injection = **report de la tranche** (CHA-030), jamais un échec ni un nouvel essai en boucle. `memory_over_limit_count > 0` ou `rocks_spool_load_shed_active = 1` met la vague en pause et lève une alerte.
- **Configuration** (vérifié) :
  - `kumod --policy … --validate` vérifie les assistants `sources`, `queues` et `shaping`, et leurs références croisées. Il peut tourner **à côté** du service actif. C'est exactement `validerConfiguration` (INF-038) ;
  - les fichiers TOML des assistants se rechargent par l'« époque » (`bump-config-epoch`) ;
  - le Lua est mis en cache 300 s ou 1 024 exécutions ;
  - un changement d'écouteur (adresse, TLS) demande un redémarrage.
- **Webhook** : les *log hooks* sont natifs (lots, réessais réglables), mais **sans signature intégrée**. `kumo.digest.hmac_sha256` existe : on signe le corps en Lua (en-tête `X-Envoi-Signature`, 03 § 6). Le secret HMAC vit sur le serveur, dans un fichier `0600` hors de la configuration générée. Il faut aussi une règle de *shaping* pour la file du hook (déjà noté en 08 A10).
- **FBL** : `log_arf` et `log_oob` existent. KumoMTA ajoute par défaut un en-tête `X-KumoRef`, encodé en base64 mais **non chiffré**. Il ne faut y mettre **aucune** métadonnée personnelle, et vérifier son contenu exact au banc. Le jeton d'envoi suffit.
- **Fichiers de *shaping*** : il existe un `shaping.toml` maintenu par l'éditeur et un autre par la communauté (`assets/community/shaping.toml`). On part de celui de l'éditeur, on fige sa version avec l'empreinte (comme le binaire, 05 § A), et on ajoute nos surcharges générées.
- **Changements récents à surveiller** : 2026.09.29 (taille maximale d'un enregistrement de journal) et 2026.09.22 (AUTH PLAIN en sortie seulement si le certificat est valide ; délai du spool). Aucun ne casse le plan. Cela confirme qu'il faut lire le journal des changements à chaque montée de version (08 E1).

### 1.3 Paquets Ubuntu 24.04 (vérifié : NON officiels)

La doc d'installation dit : « Pre-built releases are available for Rocky Linux 8/9, Ubuntu 20.04/22.04, and Amazon Linux 2/2023 ». Ubuntu 24 n'apparaît que dans la liste « community-tested ». Le dépôt de paquets n'a pas pu être interrogé (bloqué par la session).

**Options :**
- (a) **Image officielle `ghcr.io/kumocorp/kumomta` figée par empreinte**, sur Ubuntu 24.04, en réseau `host` : l'IP d'envoi et le WireGuard sont ceux de l'hôte. C'est cohérent avec « image publique, chaque instance tire sa version » (05).
- (b) Rocky Linux 9 avec le paquet officiel (support jusqu'en 2032).
- (c) Ubuntu 22.04 : à écarter, car son support standard finit en avril 2027, juste après le premier envoi.

**Recommandation : (a).** Le banc et la production lancent la même image, et la mise à jour se fait par changement d'empreinte, testé au banc (`--validate` puis kit de conformité). Les tags `latest` et `main` sont interdits.

### 1.4 DKIM, SPF, DMARC, MTA-STS, PTR (plan DNS par domaine d'envoi)

| Enregistrement | Valeur proposée | Remarque |
|---|---|---|
| SPF du domaine `From` (MAIL FROM = `bounce.<domaine>`) | `bounce.<domaine>` : `v=spf1 ip4:<ip-envoi> -all`. Domaine racine : `v=spf1 include:<hébergeur des boîtes> -all` | **Oubli du plan** : quand Will répond depuis le webmail de l'hébergeur des boîtes (V0, avant CAM-054), ces messages partent par l'hébergeur. Ils doivent passer SPF et DKIM **chez l'hébergeur**. Il faut donc deux familles d'enregistrements par domaine : KumoMTA pour les campagnes, l'hébergeur pour les réponses. |
| DKIM | Sélecteur KumoMTA (`k1._domainkey`) + sélecteur de l'hébergeur des boîtes | Alignement `d=<domaine From>` |
| DMARC | **V0 : `p=none; rua=mailto:dmarc@<domaine>; adkim=s; aspf=r; fo=1`** ; après 4 semaines avec 100 % d'alignement dans les rapports : `p=quarantine` ; V1 : `p=reject` | `rua` sur le même domaine, sinon il faut une autorisation inter-domaines. Gmail, Yahoo et Microsoft exigent un enregistrement DMARC et l'alignement (recoupé) ; `p=none` suffit à leurs règles, mais `p=reject` protège contre l'usurpation. |
| PTR | `<ip-envoi>` → `mta1.<domaine-1>`, avec HELO identique et A correspondant (FCrDNS) | Réglé à la main dans la console de l'hébergeur (V0) |
| MX | Domaine racine → hébergeur des boîtes (réponses) ; `bounce.<domaine>` → voir § 1.6 | |
| MTA-STS / TLS-RPT | Pour les domaines qui **reçoivent** (racine, chez l'hébergeur) : MTA-STS en `testing` puis `enforce` ; TLS-RPT vers `tls-rpt@` | Utile mais pas exigé par les messageries. V0 en `testing`. MTA-STS demande un petit site HTTPS `mta-sts.<domaine>`, que Cloudflare peut servir. |
| `go.<domaine>` | Page de désinscription (CRM, par Cloudflare) | Voir 06 C2 : aucun lien vers `axion-ia.com` dans les messages à froid |
| BIMI | Non | Inutile à ce volume |

### 1.5 FBL et plaintes : ce qui remonte vraiment

| Messagerie | Retour de plainte | Conséquence |
|---|---|---|
| Gmail | **Pas d'ARF par message.** Taux de spam agrégé dans Postmaster Tools, et seulement **au-delà d'un volume quotidien minimal** vers Gmail. Rapport « feedback loop » agrégé par `Feedback-ID`. | À 20-300 par jour, Postmaster sera **vide** : aucun signal Gmail en V0. |
| Yahoo / AOL | CFL (ARF) après inscription du domaine DKIM | Utile, peu de destinataires B2B français |
| Outlook.com / Hotmail | JMRP (ARF) et SNDS par IP | Inscrire l'IP dès qu'elle est attribuée |
| Microsoft 365 (entreprises), Orange, SFR, OVH, hébergeurs | **Aucun** | La majorité de nos destinataires B2B |

**Conséquence.** La règle « plaintes ARF > 0,1 % sur 7 jours, échantillon 1 000 » (03 § 3.2) reste, mais elle n'est **pas** le garde-fou principal. Il faut compter comme **plainte** (corrections C10 et C11) :
- toute réponse hostile ou qui demande « comment avez-vous eu mon adresse », classée par Will ;
- tout message reçu à `abuse@` ou `postmaster@` ;
- tout courrier de l'hébergeur au sujet d'un abus ;
- tout listage.

À faible volume, la **règle absolue** domine : 1 plainte de n'importe quelle source = palier tenu et relecture par Will ; 2 plaintes en 7 jours = arrêt 48 h. Le plan l'écrit déjà pour l'ARF ; il faut l'étendre aux autres sources.

### 1.6 Rebonds asynchrones, ARF et réponses : où arrive le courrier entrant

Le plan propose deux voies contradictoires (§ 0, point 4).

**Recommandation V0 : zéro port entrant public sur le serveur d'envoi.**
- `bounce.<domaine>` a pour MX l'**hébergeur des boîtes**, avec une boîte « fourre-tout » (*catch-all*) du sous-domaine `bounce.`, relevée par IMAP. L'hébergeur doit permettre le *catch-all* sur un sous-domaine : critère de choix (D-70).
- Le VERP `rb-<jeton>@bounce.<domaine>`, les DSN différés, les ARF (Yahoo, JMRP) et `desinscription+<jeton>@` arrivent tous dans cette boîte.
- Les réponses humaines arrivent dans la boîte de l'expéditeur.
- Les rebonds **synchrones** (de loin les plus nombreux) arrivent directement par les journaux de KumoMTA, puis par le webhook.

**V1 (facultatif)** : un écouteur entrant KumoMTA sur le port 25, limité au domaine `bounce.<domaine>`, avec `log_oob = "LogThenDrop"` et `log_arf`, sans relais. Il est prouvé au banc et par la sonde externe. Il supprime un intermédiaire, mais ajoute une surface d'attaque.

### 1.7 Webhook signé et relève IMAP

- Le webhook est conforme à 03 § 6, avec l'HMAC en Lua (§ 1.2). Ajouter au contrat :
  - **l'identité du serveur** dans la signature, pour qu'un serveur ne puisse pas parler pour un autre ;
  - **un numéro de séquence par serveur** : le CRM détecte un trou et déclenche la réconciliation tout de suite, sans attendre la nuit.
- La relève IMAP passe à **une seule tâche par boîte**, verrouillée (aucun double traitement), avec un curseur `UIDVALIDITY/UID`. Rien n'est supprimé chez l'hébergeur : on déplace dans un dossier « Traité », et le message est conservé (règle « jamais de suppression »).
- **Toutes les 5 minutes**, c'est raisonnable pour 2 à 6 boîtes. La plupart des hébergeurs limitent les connexions IMAP. À la place, on garde une connexion `IDLE` par boîte quand l'hébergeur le permet.
- Les identifiants IMAP sont **chiffrés en base** (clé hors git, dans l'environnement du serveur du CRM), jamais dans le dépôt.

### 1.8 Chauffe, paliers et seuils

- **La courbe de 03 § 3.1 est prudente et réaliste** pour une IP et des domaines neufs : 20 → 250 par jour en environ 35 jours effectifs, puis 2 000 vers 66 jours effectifs, soit 13 à 15 semaines réelles avec les jours sans envoi.
- **Le plafond « 150 par boîte » (CHA-037) vient des outils de prospection qui envoient par Google Workspace ou Microsoft 365**, où le compte lui-même est limité et surveillé. Avec notre propre serveur, la réputation suit **l'IP et le domaine**, pas la boîte. Garder un plafond par boîte a du sens pour deux raisons : rester crédible (une « personne » qui écrit 1 000 messages par jour ne l'est pas) et répartir les réponses. Mais 150 n'est pas une règle des messageries. **Proposition : 300 par boîte et par jour au plus** (correction C6).
- **Seuils** : 2 % de rebonds durs et 0,1 % de plaintes, c'est plus strict que les messageries (Gmail et Yahoo : rester sous 0,3 %, viser moins de 0,1 %, recoupé). C'est correct. On ajoute :
  - le **taux de reports** (4xx) par fournisseur : plus de 20 % sur 1 h vers un même fournisseur → pause de l'IP vers ce fournisseur ;
  - les **codes Microsoft** `5.7.515` (authentification insuffisante) et `S3150` / `5.7.606` (IP bloquée) dans la table des motifs (CHA-016).
- **Paliers multi-locataires** : corrects.

### 1.9 Débits par messagerie (V0)

Les surcharges suivantes s'ajoutent au `shaping.toml` de l'éditeur. Ce sont des **valeurs de départ prudentes**, à régler au banc et selon les retours, pas des chiffres publiés par les messageries.

| Groupe (MX regroupés) | Connexions simultanées | Messages par connexion | Débit |
|---|---|---|---|
| Gmail / Google Workspace | 2 | 10 | 20 par heure par IP en P1-P5, puis 60 par heure |
| Microsoft (Outlook.com et 365) | 1 | 5 | 10 par heure en P1-P5, puis 40 par heure |
| Yahoo / AOL | 1 | 5 | 10 par heure |
| Orange / SFR / Free / La Poste | 1 | 5 | 10 par heure |
| Autres | 2 | 10 | Pas de limite propre : le plafond du jour et des tranches s'applique |

Les tranches de 03 § 2.5, étalées sur la fenêtre de jour (± 2 min), font l'essentiel. Le débit KumoMTA sert de second verrou.

### 1.10 Règles Gmail, Yahoo et Microsoft (état au 01/11/2026, recoupé)

| Règle | Gmail | Yahoo | Microsoft (consommateurs) | Plan |
|---|---|---|---|---|
| Seuil « expéditeur de masse » | > 5 000 par jour vers Gmail | Pas de chiffre publié (5 000 cité) | ≥ 5 000 par jour (page Microsoft vue) | Sous le seuil jusqu'en V2, mais **on applique tout dès le premier message** : bonne pratique, et le seuil peut baisser. |
| SPF + DKIM + DMARC alignés | Exigé (masse) ; SPF ou DKIM pour tous | Exigé | Exigé, sinon `550 5.7.515` (application depuis le 05/05/2025) | Oui (§ 1.4) |
| Désinscription en un clic RFC 8058 | Exigée pour les messages commerciaux de masse ; en-tête, pas seulement un lien | Exigée ; **traiter sous 2 jours** | Recommandée | Oui, effet en moins d'une minute (RET-027) |
| Taux de plaintes | < 0,1 % visé, **jamais ≥ 0,3 %** | < 0,3 % | Pas de seuil publié | 0,1 % + règles absolues (§ 1.5) |
| PTR / FCrDNS, TLS | Exigés | Exigés | Recommandés | Oui |
| Durcissement | Montée de l'application depuis novembre 2025 ; refus 5xx signalés (non confirmé par Google) | — | Indésirables puis refus | Les refus 5.7.x entrent dans la table des motifs |
| Postmaster | **Postmaster Tools v2** : tableau « Compliance status » ; les écrans de réputation de domaine et d'IP sont **retirés** (dates contradictoires entre sources : septembre 2025 à septembre 2026) | Sender Hub | SNDS + JMRP | **Corriger 03** : lire en V1 le statut de conformité et le taux de spam, pas une « réputation ». En V0, Postmaster sera vide (volume). |

### 1.11 Port 25 : Hetzner, OVH, plan B

- **Hetzner Cloud** (recoupé, page officielle non lue) :
  - ports **25 et 465 sortants bloqués** sur tous les serveurs Cloud ;
  - déblocage sur demande « après un mois et le paiement de la première facture », pour un usage légitime, **au cas par cas** ;
  - la restriction s'applique **par compte**.
  - Comme la facture est mensuelle, il faut compter **5 à 7 semaines** entre l'ouverture du compte et un port 25 ouvert, si la réponse est positive.
- **Risque oublié par le plan** : la politique d'usage de Hetzner interdit l'envoi de courrier **non sollicité** en masse. La prospection B2B en opposition (*opt-out*) est légale en France, mais elle est « non sollicitée » au sens de la plupart des hébergeurs.
  - Il faut **déclarer honnêtement** l'usage (prospection B2B à faible volume, opposition en un clic, art. 14 ; SEC-033).
  - Il faut garder le compte « envoi » **strictement séparé** du compte qui porte le CRM, avec des moyens de paiement et des contacts distincts autant que possible. Une plainte pour abus peut faire fermer un compte, et un hébergeur peut relier deux comptes d'une même personne.
  - **Non vérifié** : si Hetzner ferme les deux comptes ensemble. À demander par écrit au support avant d'envoyer.
- **OVHcloud VPS** : versions contradictoires. Selon les sources, le port 25 est bloqué par défaut, ou bien ouvert mais surveillé par un anti-spam automatique. Ce qui est sûr : le blocage de l'IP se lève depuis l'espace client, et les récidives entraînent des blocages plus longs, peut-être définitifs (non vérifié). C'est un **plan B acceptable**, mais l'anti-spam automatique d'OVH peut couper l'IP sur un faux positif en pleine chauffe.
- **Plan B réaliste** : demander le déblocage chez **deux** hébergeurs en parallèle (Hetzner « envoi » et OVH), dès maintenant (03 R3). Le repli sur un relais payant (SES, Brevo…) reste **exclu pour le froid** (01 § 1). Un serveur **dédié** (et non Cloud) chez un hébergeur qui n'y bloque pas le port 25 est une troisième piste, **à vérifier** au cas par cas.
- **Port 587 et relais** : sans objet. Nous ne relayons pas par un tiers.

### 1.12 Nombre de domaines, d'IP et de boîtes ; risque *snowshoe*

- **V0** : 1 IP, 2 domaines, 2 identités. Aucun risque *snowshoe* (dispersion d'envois sur beaucoup d'IP et de domaines pour diluer les signaux).
- **V1** : 2 IP et 3 à 4 domaines, ajoutés par cohortes espacées d'au moins 15 jours ouvrés et motivées par le volume, jamais par un listage. C'est acceptable.
- **Signaux de *snowshoe* à éviter** :
  - domaines achetés le même jour chez le même registraire, avec la même structure et des contenus identiques ;
  - plus de 2 domaines par IP ;
  - des IP d'un même /24 ajoutées ensemble ;
  - une rotation de domaines après des rebonds.
- **Règle à écrire** (RES-060, à **remonter en V0** comme simple garde) :
  - au plus 2 domaines par IP ;
  - au plus 1 nouvelle ressource par période de 15 jours ouvrés ;
  - pour chaque domaine, un site visible (page qui présente Axion, mentions légales, art. 14) et une identité commune claire (« Axion-IA » dans le `From`).
- **Domaines** : en acheter **2 maintenant** (âge ≥ 21 jours ; 30 jours conseillés) et 2 de réserve plus tard. Il ne faut pas les acheter tous ensemble au même endroit avec des noms en série.

### 1.13 Volumes réalistes pour un expéditeur seul

| Étape | Plan | Lecture « Will seul » |
|---|---|---|
| V0 | 20 → environ 250-300 par jour | Réaliste techniquement. Avec 1 à 3 % de réponses, cela fait 3 à 9 réponses par jour à traiter : tenable. |
| V1 | 1 000 - 2 000 par jour | Techniquement possible vers la 13e à 15e semaine. **Humainement**, 2 000 premiers messages par jour donnent 20 à 60 réponses par jour, plus les RDV. Will seul en traite peut-être 15 à 25 par jour. **Plafond utile proposé : 600 à 800 par jour** (relances comprises), tant qu'une seconde personne n'est pas nommée. Le frein « réponses en attente » (06 C7) doit l'imposer automatiquement. |
| V2 | jusqu'à 5 000 par jour | C'est la somme des **locataires clients**, pas Axion seul. Au-delà de 5 000 par jour vers Gmail, les règles « masse » s'appliquent pleinement. |
| Audience | — | Le vivier (organisateurs, fédérations) **épuise** vite : à 300 nouveaux par jour, il faut plus de 6 000 adresses vérifiées par mois. Il faut vérifier la taille du vivier **avant** de viser la V1. Sinon la chauffe monte vers un volume qu'on ne pourra pas tenir, et une chute de volume fait reculer la chauffe (CHA-006). |

### 1.14 Alternative réaliste aux 14 à 16 boîtes de réponse

**Constat.** RES-039 exige des personnes réelles avec leur accord écrit. Will est seul (06 B3). Les 14 à 16 boîtes viennent du plafond de 150 par boîte. Ce plafond n'est pas une contrainte de notre propre serveur (§ 1.8).

**Proposition.**
1. **Une identité réelle par domaine, toutes au nom de Will** : `will@<domaine-1>`, `will@<domaine-2>` (ou prénom.nom). C'est la même personne, réelle et identifiable, avec la même signature (sans téléphone) et un `From` affiché « Will – Axion-IA ». Ce n'est pas trompeur : l'expéditeur réel est bien Will. **À faire valider par Will** comme lecture de RES-039 : « une personne réelle peut tenir une boîte par domaine ».
2. **Plafond de 300 par boîte et par jour** : 2 boîtes suffisent jusqu'à 600 par jour, 4 boîtes (4 domaines) jusqu'à 1 200 par jour, ce qui couvre le plafond humain du § 1.13.
3. **Boîtes techniques**, sans titulaire humain, car elles n'écrivent pas : `bounce.` (fourre-tout), `dmarc@`, `tls-rpt@`, `abuse@` et `postmaster@` (exigés par l'usage), `presse@` en V1. On peut les regrouper en **une seule boîte réelle avec des alias**, si l'hébergeur le permet.
4. **Toutes les réponses dans un seul écran** « Réponses » (relève IMAP de chaque boîte), si bien que Will ne surveille qu'un endroit.
5. **Au-delà de 1 200 par jour** : une seconde personne réelle (associé, assistant ou prestataire nommé, avec accord écrit) ou des locataires clients. C'est une décision de Will, à prendre plus tard, pas maintenant.

**Effet** : 2 boîtes en V0 et 4 en V1 au lieu de 14 à 16. Le poste « boîtes hébergées » de V1 passe d'environ 20-40 € à environ 8-15 € par mois.

### 1.15 Coûts (recalcul, ordre de grandeur HT, prix non revérifiés en ligne)

| Poste | V0 | V1 (≤ 800 par jour, Will seul) | Remarque |
|---|---|---|---|
| Serveur d'envoi (VPS 2 vCPU, 4 Go) | 5-10 € | 5-10 € | Un seul nœud suffit largement jusqu'à 5 000 par jour. Un second nœud sert la **résilience** et les **clients**, pas le débit. |
| IP d'envoi supplémentaire | 0-2 € | 2-4 € | Gestion ≠ envoi (INF-012) |
| Sonde externe (autre hébergeur) | 4-6 € | 4-6 € | |
| Domaines | ~2-3 € | ~4-5 € | |
| Boîtes (2 → 4 identités + 1 technique) | 3-8 € | 8-15 € | Au lieu de 20-40 € |
| Vérification d'adresses | 10-45 € | 30-90 € | Sur 800 par jour plutôt que 2 000 |
| Boîtes témoins | ~5 € | ~5 € | |
| Listes noires | 0 € à vérifier | à vérifier | **Point ouvert** : les miroirs publics et le DQS gratuit de Spamhaus sont réservés à un usage **non commercial**. Axion est commercial. Le contrôle de nos 1 à 2 IP et 2 à 4 domaines est minuscule, mais la licence reste à lire. |
| Surveillance de battement (06 C6) | 0 € | 0 € | Service externe gratuit |
| **Total** | **≈ 30 à 80 € par mois** | **≈ 60 à 140 € par mois** | Au lieu de 120 à 280 € en V1 |

---

## 2. Chaîne « ajouter un domaine, une boîte, une IP ou un serveur par l'interface »

**Principe.** La base dit **ce qui doit être**. Le serveur d'envoi **va chercher** sa configuration, la vérifie, l'applique et rend compte. **Personne ne pousse sur le serveur** : ni GitHub, ni le CRM, ni une clé SSH. La règle « aucune clé SSH ni secret dans GitHub » est donc tenue par construction.

```
 Console (owner, 2FA)        Base CRM (état souhaité)          Serveur d'envoi (agent "tireur")
 ─────────────────────       ─────────────────────────         ───────────────────────────────
 Ajouter domaine/IP/boîte ─► registre + version N (brouillon)
 Valider (risque ↑ = owner) ─► version N « validée »
                              générateur → paquet N            ◄── GET /interne/envoi/config  (WireGuard, toutes les 2 min)
                              (TOML + Lua de données,               vérifie signature Ed25519 + N > actuel
                               SANS secret, signé Ed25519)          écrit dans releases/N, kumod --validate
                                                                   bascule (lien symbolique), époque ou redémarrage
                                                                   contrôles de santé (§ 2.4)
                              rapport N : appliqué / refusé ◄──    échec → retour automatique à N-1 + rapport
 Écran « Serveurs » : version attendue = version chargée ? (dérive → pause + alerte console et e-mail)
```

### 2.1 État souhaité en base

Tables, toutes avec `workspace_id` :
- `envoi_serveurs` : nom, IP de gestion, IP WireGuard, clé **publique** WireGuard, clé **publique** de l'agent, version attendue, version chargée, empreinte du binaire ;
- `envoi_ip` : IP, serveur, PTR attendu, HELO, pool, locataire, état de chauffe ;
- `envoi_domaines` : domaine, locataire, sélecteur DKIM, clé DKIM **publique** remontée par le serveur, plan DNS, état ;
- `envoi_boites` : adresse, titulaire, accord écrit, hébergeur, identifiants IMAP **chiffrés** ;
- `envoi_identifiants_injection` : `authc`, locataire, pool, empreinte du mot de passe ;
- `envoi_config_versions` : numéro croissant, contenu, empreinte, auteur, validation, état.

Chaque changement crée une **version** ; rien n'est modifié en place.

### 2.2 Ce que contient le paquet généré (sans aucun secret)

- `sources.toml` (IP, EHLO, pools) ;
- `queues.toml` (locataire → pool, débits) ;
- surcharges de *shaping* ;
- `listener_domains.toml` (en V1 seulement, § 1.6) ;
- une table « `authc` → locataire, pool, empreinte du mot de passe » ;
- une table « domaine → sélecteur DKIM, **chemin** de la clé » ;
- les plafonds journaliers par locataire ;
- la liste des `MAIL FROM` autorisés (INF-021) ;
- l'empreinte attendue de l'image KumoMTA.

**Les secrets ne voyagent pas.** Les clés DKIM privées sont générées par l'agent **sur** le serveur, à la première apparition d'un domaine, et l'agent remonte la clé publique. Les mots de passe d'injection sont générés **par le CRM**, n'y sont stockés qu'en empreinte, et sont donnés au CRM (pour qu'il s'authentifie) par la variable d'environnement de M1, hors git. Le secret HMAC du webhook est créé sur le serveur et remonté une seule fois au CRM par le tunnel, puis chiffré en base.

### 2.3 Application sur le serveur, sans SSH depuis GitHub

- **L'agent tireur** est un petit programme public dans `axion-crm-pro` (`infra/envoi/agent/`), avec un minuteur systemd.
  - Il tire par WireGuard le paquet le plus récent.
  - Il vérifie la **signature Ed25519**. La clé privée de signature vit sur M1, dans l'environnement, hors git. La clé publique est posée sur le serveur au démarrage.
  - Il refuse toute version **inférieure ou égale** à la version active (pas de rejeu).
  - Il écrit dans `releases/N/`, lance `kumod --validate`, puis bascule le lien `current`. Il relance l'époque (TOML) ou redémarre le service (écouteurs, image).
- **Socle local non pilotable.** Un fichier local que le paquet ne peut **pas** modifier fixe :
  - `relay_hosts` = localhost ;
  - les adresses d'écoute (IP WireGuard seulement) ;
  - `trusted_hosts` = localhost ;
  - le **plafond dur global** journalier ;
  - l'homme mort ;
  - le pare-feu.
  
  **Pourquoi** : même un CRM compromis, qui signerait un paquet malveillant, ne peut ni ouvrir un relais, ni dépasser le plafond global, ni ouvrir un port. Pour changer ce socle, Will intervient à la main sur le serveur (console de l'hébergeur ou SSH **par le tunnel**, avec sa clé personnelle, jamais dans GitHub).
- **Changements qui augmentent le risque** (nouvelle IP, nouveau domaine, plafond relevé, nouveau locataire) : validation de l'owner avec la 2FA par e-mail, puis délai de 10 minutes annulable avant publication (INF-039).
- **Mise en service d'un serveur** (manuelle, une fois) :
  1. Will crée le VPS dans la console de l'hébergeur et colle un `cloud-init` **généré par la console du CRM**, qui ne contient que des valeurs publiques : version de l'agent, clé publique de signature, IP WireGuard attribuée.
  2. Le serveur génère ses clés WireGuard et d'agent, puis affiche ses clés **publiques**.
  3. Will les colle dans l'écran « Serveurs », ce qui ajoute le pair WireGuard sur M1 par le même mécanisme de tirage côté M1.
  4. Il reste un seul geste manuel sur M1 : ajouter le pair WireGuard, par un script local que Will lance (ou par un tirage symétrique en V1).

### 2.4 Contrôles de santé après application, et retour arrière

- **Contrôles, dans les 2 minutes qui suivent l'application** :
  - `check-liveness` = OK ;
  - les écouteurs attendus sont ouverts, et aucun autre : comparaison avec `ss -ltn` ;
  - une injection de test vers le **puits local** (domaine `.invalid` routé vers un puits sur le serveur) est signée DKIM et vérifiée ;
  - `metrics` est lisible.
- **Échec** : retour au lien `releases/N-1`, redémarrage, rapport « refusée : motif ». Le CRM met la version N en « refusée » et l'**envoi reste en pause** sur ce serveur jusqu'à décision.
- **Retour arrière voulu** : dans l'écran « Versions », [Revenir à la version K] crée une version **N+1 identique à K**. Le numéro ne recule jamais, ce qui rend le journal lisible et empêche tout rejeu. L'agent garde les 20 dernières versions sur disque.

### 2.5 Contrôle de dérive

- **Toutes les 5 minutes**, l'agent publie :
  - l'empreinte de la configuration chargée ;
  - l'empreinte de l'image KumoMTA ;
  - la liste des ports à l'écoute ;
  - les pairs WireGuard ;
  - l'empreinte du socle local ;
  - l'heure.
- Le CRM compare ces valeurs à l'attendu. **Un écart, ou un rapport absent pendant 15 minutes en fenêtre d'envoi**, met en **pause** l'envoi de ce serveur (échec fermé) et lève une alerte dans la console et par e-mail.
- La **sonde externe**, vue de l'extérieur, s'ajoute à ce contrôle : ports ouverts, relais, bannière.
- Au test de fumée de 06:45, on compare aussi l'empreinte (11 n° 3).
- **Ce contrôle passe en V0** (registre : V2 ; 11 : V1). Il ne coûte presque rien une fois l'agent écrit, et c'est lui qui rend la configuration générée sûre.

### 2.6 Ce qui est faisable dès la V0, ce qui reste manuel

| Objet | V0 par l'interface | V0 manuel (Will, guidé par un écran pas à pas) | V1 |
|---|---|---|---|
| Domaine | Saisie, garde de nommage, génération de la clé DKIM par l'agent, **plan DNS à copier**, vérification DNS automatique, configuration générée | Achat chez le registraire, saisie des enregistrements dans Cloudflare | Poussée DNS par l'API Cloudflare (jeton limité aux zones d'envoi, chiffré en base) |
| Boîte | Saisie, titulaire, accord écrit, identifiants IMAP chiffrés, test de relève, affectation au pool | Création chez l'hébergeur, DKIM et SPF de l'hébergeur | Connecteur de l'hébergeur s'il a une API (V2) |
| IP | Saisie, PTR attendu, contrôle PTR et FCrDNS, configuration générée, courbe de chauffe | Achat de l'IP et réglage du PTR dans la console de l'hébergeur, ajout de l'IP à l'interface réseau (paquet `netplan` généré, appliqué par l'agent **avec validation** en V1 ; en V0, à la main avec un modèle) | Agent applique `netplan` avec retour arrière |
| Serveur | Enregistrement, clés publiques, `cloud-init` généré, suivi de version et de dérive | Création du VPS, collage du `cloud-init`, ticket du port 25, ajout du pair sur M1 | Pair WireGuard ajouté sur M1 par tirage |
| Mise à jour de KumoMTA | Nouvelle empreinte d'image proposée → banc vert exigé → validation owner → tirage | — | Idem |

**Coût de la chaîne en V0** : environ **10 jours-agent**.

| Élément | j-agent |
|---|---|
| Générateur | 3 |
| Agent tireur, signature, retour arrière | 4 |
| Dérive | 1,5 |
| Écrans Serveurs et Versions | 1,5 |

Une partie remplace ce que 03 mettait en V1 (« configuration générée depuis la base, agent SSH »), et le runbook V0 « session déployeuse » disparaît.

---

## 3. Banc, essai à blanc, premier envoi

### 3.1 Banc jetable (aucun accès à Internet)

**Composition** : `docker compose` qui tourne en CI publique gratuite et sur le PC.
- L'**image KumoMTA figée** (la même que la production).
- Un **WireGuard** entre deux conteneurs : « crm-banc » (le vrai code du CRM) et « mta-banc ».
- Un **résolveur DNS local** qui sert de fausses zones (`gmail.test`, `outlook.test`, `exemple.test`) avec des MX vers des **puits**.
- Des **puits SMTP programmables**, qui répondent sur commande `250`, `421`, `450`, `550 5.1.1`, `550 5.7.1 … spamhaus`, `5.7.515`, ou une coupure en cours de transaction. Ils vérifient la signature DKIM de ce qu'ils reçoivent.
- Un **serveur IMAP local** pour les boîtes simulées.
- Le **réseau Docker en `internal: true`** : aucune sortie possible. Un test vérifie qu'une connexion vers une vraie IP échoue.

**Scénarios obligatoires** (en plus de 03 § 9) :

| # | Scénario | Attendu |
|---|---|---|
| B1 | Injection sans AUTH depuis l'IP WireGuard du CRM | Refus (§ 1.1) |
| B2 | AUTH sans STARTTLS | Refus |
| B3 | `authz ≠ authc` | Refus |
| B4 | `X-Tenant` falsifié dans le message | Ignoré ; le locataire suit `authc` |
| B5 | `MAIL FROM` hors registre ou `axion-ia.com` | Refus (INF-021, G1) |
| B6 | API HTTP depuis l'IP WireGuard sans identité | 401 ; `inject` refusé à l'identité « crm » par l'ACL |
| B7 | Mémoire au-delà de la limite douce (simulée) | 4xx à l'injection → tranche reportée, pause, alerte |
| B8 | Puits Microsoft `5.7.515` × 3 | Pause IP × Microsoft, alerte |
| B9 | 25 % de `421` vers « gmail.test » pendant 1 h | Pause IP × Gmail |
| B10 | Paquet de configuration mal signé, rejoué, ou cassé (`--validate` échoue) | Refusé ; version précédente conservée ; envoi en pause |
| B11 | Paquet qui tente de changer `relay_hosts` ou le plafond global | Sans effet (socle local) ; alerte de dérive |
| B12 | Arrêt de l'agent 15 min | Dérive → pause |
| B13 | Port inattendu ouvert sur « mta-banc » | Dérive → pause |
| B14 | Webhook : signature fausse, horodatage vieux, trou de séquence, doublons, 72 h de retard | Refus, refus, réconciliation immédiate, idempotence, rattrapage |
| B15 | CRM muet 15 min en fenêtre | Homme mort : files suspendues |
| B16 | Bouton « Tout arrêter » | `suspend` global ; plus aucune connexion vers les puits (mesuré dans les puits) |
| B17 | POST RFC 8058 | `peutRecevoir` faux en moins d'une minute ; message en file retiré (`bounce` administratif) |
| B18 | DSN différé et ARF dans la boîte IMAP `bounce.` | Rebond dur appliqué ; plainte → opposition + disjoncteur |
| B19 | Deux locataires | Aucune fuite de configuration, de file, d'opposition ou d'événement |
| B20 | Montée de version de l'image | Kit de conformité vert avant acceptation |

### 3.2 Essai à blanc en production (sans envoi réel)

1. **Étape « simulation »** (03 § 9.5) : une vraie campagne validée, transport en mode simulation, zéro SMTP. On compare les comptes (prévus = simulés = journalisés, 100 %).
2. **Étape « puits sur le vrai serveur »** :
   - le vrai KumoMTA, avec les **vraies clés DKIM** et la vraie configuration générée, reçoit l'injection par le vrai tunnel ;
   - une règle de routage **du socle local** envoie **tous** les destinataires vers le puits local du serveur ;
   - le port 25 sortant est **fermé au pare-feu** pendant cette étape, ce qui est vérifié par la sonde externe ;
   - on vérifie les signatures, les en-têtes, le webhook, la comptabilité et les métriques.
3. **Étape « témoins seulement »** :
   - le socle local passe en mode **liste blanche de destinataires** : le Lua refuse tout `RCPT` hors de la liste des boîtes témoins et de l'adresse de Will ;
   - le port 25 est ouvert ;
   - le **CRM ne peut donc rien envoyer d'autre, même par erreur**. Ce verrou est au niveau du serveur, pas seulement du CRM.

### 3.3 Critères de passage au premier envoi réel (tous obligatoires, affichés en cases dans l'écran « Feu vert »)

1. Port 25 ouvert **par écrit** par l'hébergeur, avec l'usage déclaré honnêtement.
2. PTR = HELO = A (FCrDNS). IP et domaines absents des listes Spamhaus (SBL, CSS, DBL), Barracuda et SpamCop.
3. Domaines âgés d'au moins 21 jours (30 conseillés), avec un site visible sur chaque domaine.
4. Sur les 4 témoins : `spf=pass`, `dkim=pass`, `dmarc=pass`, arrivée en **boîte de réception** 3 jours de suite.
5. Bouton « Se désabonner » de Gmail, ou un POST RFC 8058 externe, avec effet mesuré en moins d'une minute. Le lien visible fonctionne.
6. Scénarios B1 à B20 verts au banc **sur la version d'image et de configuration en production**.
7. Dérive : 7 jours verts de suite en production (agent, empreintes, ports).
8. Sonde externe : aucun relais, aucun port public autre que WireGuard (et SSH limité au tunnel).
9. **Chaîne d'alerte prouvée** : une alerte de test reçue par e-mail par Will, et le battement externe qui écrit à Will si le CRM se tait (06 C6).
10. Relève prouvée : une réponse d'un témoin apparaît dans « Réponses », un STOP d'un témoin écrit l'opposition.
11. Arrêt d'urgence et homme mort prouvés **en production**, à l'étape « témoins seulement ».
12. Textes art. 14, page « pourquoi ce message », entité expéditrice et pied légal validés par Will (D-07, D-26). Aucun lien vers `axion-ia.com` dans le corps (06 C2).
13. 20 adresses d'organisateurs vérifiées depuis moins de 30 jours, sans webmail, en France (06 C1).
14. Version du message validée par Will (empreinte), puis contrôleur de contenu vert.
15. Sauvegarde du CRM et restauration testées, avec l'envoi gelé après restauration (INF-057).

### 3.4 Plan du premier envoi

| Jour | Quoi | Volume | Arrêt si |
|---|---|---|---|
| T-3 à T-1 | Étape « témoins seulement » : chaque jour, 1 message par domaine vers Will et 4 témoins (Gmail grand public, Outlook.com, Yahoo, Microsoft 365 professionnel ; un 5e chez Orange ou OVH conseillé). Lecture des en-têtes, placement noté, désinscription testée sur un témoin, réponse testée sur un autre. | 10 à 12 par jour | Un témoin en indésirables 2 jours sur 3, un `fail` d'authentification, ou un écart de comptes |
| J1 | Le socle quitte le mode « liste blanche ». **20 organisateurs** : 10 par domaine, 2 tranches (10:00 et 14:00), Will et les témoins en copie cachée de contrôle (1 par tranche, **hors** comptage). | 20 + témoins | ≥ 2 rebonds durs sur 20 (liste suspecte : revérifier), 1 plainte de n'importe quelle source, un témoin en indésirables, un refus de réputation |
| J1 + 48 h | Bilan écrit en une phrase dans le journal : rebonds, reports, réponses, placement des témoins | — | Une règle non verte = on reste en P1 et Will relit |
| J2 à J5 effectifs | P1 continue à 20 par jour (courbe de 03 § 3.1), puis P2 à 35 | 20 → 35 | Règles de 03 § 3.2 + § 1.5 |

---

## 4. Incohérences à corriger dans 01, 03, 05 et 08 (et voisins)

| # | Incohérence | Où |
|---|---|---|
| I1 | Volume de départ : « 150 par jour au plus puis environ 1 500 après 6 à 9 semaines » contre P1 = 20, P7 = 250 et 2 000 vers 66 jours effectifs ; 00 dit « 20-50 puis environ 300 » | 01 § 1 ; 02 ; 03 § 3.1 ; 00 |
| I2 | Cohortes : « 1 IP + 2 domaines + 10 boîtes tous les 15 jours ouvrés » contre « + 1 domaine + 2 boîtes » à P11 et une 2e IP à P12 | 01 § 1 ; 03 § 3.1 |
| I3 | DMARC : RES-017 (rapports) dans la liste V0, « ingestion DMARC » en V1 ; politique de départ non écrite (`none→` dans une maquette) | 03 § 12, § 13, § 7.2 ; 11 n° 37 |
| I4 | Ports entrants : « aucun port public sauf SSH et WireGuard » contre `log_oob` / `log_arf` sur KumoMTA (port 25 entrant) contre FBL « relevée par IMAP » | 03 § 10.3, § 6 ; 08 A7, A10 |
| I5 | SSH : « SSH restreint » public, « agent SSH » en V1, contre la règle « aucune clé SSH dans GitHub » ; le code actuel contient 25 workflows avec `HETZNER_SSH_PRIVATE_KEY` (root) | 03 § 10.3, § 13 ; dépôt `.github/workflows` |
| I6 | Contrôle de dérive en V2 (registre), V1 (11), alors qu'il conditionne la sûreté de la configuration générée | 03 § 12 ; 11 n° 54 |
| I7 | Alertes : « Grafana + Alertmanager » en V0 contre « console + e-mail seulement » ; question encore posée à Will (03 § 15.2) alors qu'il a tranché ; `deploy-direct-ssh.yml` alerte encore par Telegram | 08 A15, C4 ; 03 § 7.8, § 15 ; dépôt |
| I8 | Repli : « Postfix + OpenDKIM » contre « Postfix + rspamd » | 01 § 1 ; 00 ; 05 § A |
| I9 | Paquets Ubuntu 24.04 « à vérifier » : ils ne sont **pas** officiels | 05 § A |
| I10 | API HTTP d'injection « gardée fermée » sans dire comment ; `trusted_hosts` et MiniJinja ignorés | 08 A16 ; 03 § 10.1 |
| I11 | SMTP AUTH sans mention du STARTTLS obligatoire ni de `relay_hosts` | 03 § 10.1 ; 08 A16 |
| I12 | Plaintes : seuil ARF présenté comme garde-fou principal, alors que la plupart des destinataires n'ont pas de FBL | 03 § 3.2 ; 06 |
| I13 | Postmaster et SNDS « inscrits en V0, lus par API en V1 » : Postmaster v2 n'a plus de réputation, et il est muet à ce volume | 03 § 12, § 13, Résumé 10 ; 08 C12 |
| I14 | Plafond de 150 par boîte présenté comme une contrainte, d'où 14 à 16 boîtes | 03 § 3.1 ; 10 § 10 ; 06 B3 |
| I15 | SPF et DKIM de l'hébergeur des boîtes absents du plan DNS (réponses de Will depuis le webmail) | 03 § 7.2 ; 07 (assistant DNS) |
| I16 | Port 25 : « environ un mois » contre « un mois **et** une première facture » ; risque de la politique d'usage non cité | 03 R3 ; 00 ; 10 § 10 |
| I17 | 03 § 9 saute l'étape 6 (« mode recette Will + 4 témoins »), que le résumé cite | 03 § 9 |
| I18 | Coûts V1 (120-280 €) calculés sur 2 000 par jour et 14-16 boîtes | 03 § 11 ; 00 |
| I19 | Spamhaus « DQS gratuit sous conditions » : les conditions (non commercial) excluent probablement Axion | 03 § 11 ; RES-053 |
| I20 | V2 « 5 000 par jour, plusieurs serveurs » présentée comme un besoin de débit ; c'est un besoin de résilience et de clients | 03 § 13 V2 |
| I21 | Volume utile de V1 non relié à la capacité de Will à répondre | 03 § 3.1 ; 06 C7 |

---

## 5. Corrections : texte exact, effort, priorité

Effort en jours-agent (j), tests compris, sans les 15 % de relecture. « 0 » = correction du texte du plan seulement.

| # | Fichier et endroit | Texte exact à mettre | j | Prio |
|---|---|---|---|---|
| C1 (I1) | 01 § 1, puce « Démarrage » | « Démarrage : 1 VPS d'envoi, 1 IP, 2 domaines neufs (âge ≥ 21 jours). Courbe unique de 03 § 3.1 : 20 par jour au premier jour effectif, environ 250 en fin de V0 (35 jours effectifs), 2 000 au plus vers 66 jours effectifs (13 à 15 semaines réelles). Plafond utile tant que Will est seul : 600 à 800 par jour. » Même phrase dans 00 (« Complet en fonctions ») et 02 (remplacer « premier envoi à 150 » et « première campagne de 150 messages » par « première campagne : 20 organisateurs »). | 0 | V0 |
| C2 (I2) | 01 § 1, fin de la puce | « Montée : une ressource nouvelle au plus tous les 15 jours ouvrés (une IP **ou** un domaine **ou** une identité), au plus 2 domaines par IP, seulement quand le goulot affiché le demande, jamais après un listage (03 § 3.1, P11 et P12). » | 0 | V0 |
| C3 (I3) | 03 § 7.2 et § 12 (RES) + nouvelle ligne dans E4 | « DMARC des domaines d'envoi : `p=none; rua=mailto:dmarc@<domaine>; adkim=s; aspf=r; fo=1` dès la création ; passage à `p=quarantine` quand les rapports montrent 100 % d'alignement sur 4 semaines et au moins 500 messages ; `p=reject` en V1. Ingestion minimale des rapports `rua` en V0 (comptes pass et fail par source, alerte sur une source inconnue) ; tableaux détaillés en V1. » Retirer « ingestion DMARC » de la ligne V1 du § 13. | 2 | V0 |
| C4 (I4) | 03 § 6 (lignes « Plaintes ARF » et « Rebonds asynchrones ») et 08 A7, A10 | « V0 : aucun port entrant public sur le serveur d'envoi. `bounce.<domaine>` a pour MX l'hébergeur des boîtes (boîte fourre-tout relevée par IMAP) : DSN différés, VERP, ARF, `desinscription+`. Les rebonds synchrones viennent des journaux de KumoMTA par le webhook. V1 facultatif : écouteur entrant KumoMTA limité à `bounce.<domaine>` (`log_oob = "LogThenDrop"`, `log_arf`), sans relais, prouvé par la sonde externe. » Critère ajouté au choix de l'hébergeur (D-70) : fourre-tout sur sous-domaine et IMAP IDLE. | 0 (le code est déjà compté en E6) | V0 |
| C5 (I5) | 03 § 10.3, 5e puce | « Aucun relais ouvert. Aucun port public autre que WireGuard ; SSH n'écoute que sur l'IP WireGuard, avec la clé personnelle de Will, jamais dans GitHub. Aucune clé SSH du serveur d'envoi ni du CRM n'est stockée dans GitHub. Envoi en IPv4 seulement. » § 13, ligne V1 : remplacer « agent SSH et configuration depuis la base » par « configuration depuis la base par l'agent tireur (§ 2 du fichier 13), déjà en V0 ». | 0 | V0 |
| C6 (I14) | 03 § 3.1, colonne « Par boîte », et § 1.2 | « Par boîte : 300 au plus par jour (plafond de crédibilité et de répartition des réponses ; la réputation suit l'IP et le domaine). Une personne réelle peut tenir une boîte par domaine d'envoi (lecture de RES-039, à valider par Will). V0 : 2 boîtes au nom de Will ; V1 : 4 boîtes au plus ; au-delà de 1 200 par jour, une seconde personne nommée ou des locataires clients. » Recalculer les colonnes « Ressources » (P13 : 2 IP, 4 domaines, 4 boîtes). 10 § 10 : remplacer « 14 à 16 boîtes de réponse » par « 2 boîtes au nom de Will (une par domaine) + 1 boîte technique avec alias ». | 0,5 (seuils en base) | V0 |
| C7 (I1, I21) | 03 § 2.5, nouvelle puce | « Frein humain : le volume de premiers messages du jour est plafonné à `min(courbe, capacité de réponse)`, où capacité = 20 réponses par jour × nombre de personnes réelles ÷ taux de réponse observé sur 14 jours (défaut 2 %). Plus de 10 réponses intéressées en attente depuis plus de 24 h → aucun nouveau premier message (relances autorisées). » (06 C7) | 1,5 | V0 |
| C8 (I11) | 03 § 10.1, ligne `injecter`, colonne « Exigences » | « SMTP AUTH PLAIN sur l'écouteur WireGuard (port 2525), **après STARTTLS** (exigé par KumoMTA), certificat d'une autorité privée créée sur le serveur et vérifié par le CRM ; `relay_hosts` = localhost seulement (le CRM n'y figure jamais) ; `authz` doit égaler `authc` ; locataire et pool déduits de `authc` ; tout `X-Tenant` entrant retiré ; mots de passe en empreinte sur le serveur. » | 1 | V0 |
| C9 (I10) | 08 A16 et 03 § 10.1 | « L'API HTTP de KumoMTA ne sert qu'à l'administration et à la lecture : écoute sur 127.0.0.1 et l'IP WireGuard ; `trusted_hosts` = localhost seulement (une IP de confiance a accès à toute l'API sans authentification) ; identité « crm » en HTTP Basic sur TLS ; ACL `kumo.aaa` : lecture, `suspend`, `bounce` permis ; `inject`, `rebind`, `xfer` refusés. Si l'injection HTTP sert un jour : `template_dialect = "Static"` obligatoire, `deferred_generation` interdit. » | 1 | V0 |
| C10 (I12) | 03 § 3.2, ligne « Plaintes authentifiées », colonne « Règle absolue » | « 1 plainte de **n'importe quelle source** (ARF, réponse hostile classée « plainte », message à `abuse@` ou `postmaster@`, avis de l'hébergeur) → palier tenu 3 jours et relecture par Will ; 2 en 7 jours → arrêt 48 h du domaine. Note : Gmail, Microsoft 365 et les messageries françaises n'envoient pas d'ARF ; le seuil en taux ne joue qu'au-delà de 1 000 livrés. » | 1 | V0 |
| C11 (I12) | 03 § 7 + E10 | Ajouter un classement « plainte » à la file Réponses et la relève des alias `abuse@` et `postmaster@` de chaque domaine. | 1 | V0 |
| C12 (I13) | 03 § 12 (remontées V1), Résumé 10 et 08 C12 | « Postmaster Tools (v2) : inscription des domaines en V0, lecture en V1 du statut de conformité et du taux de spam ; plus de réputation de domaine ni d'IP depuis 2025-2026. Pas de données attendues sous quelques centaines de messages par jour vers Gmail. SNDS et JMRP : inscription de l'IP dès son attribution (V0). » | 0 | V0 |
| C13 (I7) | 08 A15 | « Supervision V0 : le CRM lit `/metrics` (format Prometheus) par le tunnel toutes les 5 minutes, sans Prometheus, Grafana ni Alertmanager. Alertes uniquement dans la console et par e-mail à Will (décision de Will). Grafana reste un outil de dépannage facultatif en V1. » Effort de A15 : 2 j → 1 j. | −1 | V0 |
| C14 (I7) | 03 § 7.8 et § 15, question 2 ; 08 C4 | Remplacer la « décision à confirmer » par : « Décidé par Will : alertes dans la console et par e-mail, jamais par téléphone ni Telegram. Le connecteur Telegram n'est pas repris. » Retirer la question 2 du § 15. Dépôt : tâche OPS « retirer l'alerte Telegram de `deploy-direct-ssh.yml` et la remplacer par un e-mail ou une alerte console ». | 0,5 | V0 |
| C15 (I5) | Nouveau, 01 § 3 (gardes) | « Garde CI : aucun workflow ne référence une clé SSH ou un hôte du serveur d'envoi ; le serveur d'envoi n'accepte aucune connexion venant de GitHub. Dette existante : les 25 workflows qui utilisent `HETZNER_SSH_PRIVATE_KEY` (root) sur le serveur du CRM sont à migrer vers le même modèle de tirage (le serveur tire l'image GHCR publique), en V1 du CRM. » | 0,5 (garde) + 4 (migration CRM, V1) | V0 / V1 |
| C16 (I6) | 03 § 12 et § 13 (E3), 11 n° 54 | « Configuration générée depuis la base et appliquée par un agent tireur sur le serveur d'envoi (paquet signé Ed25519, version croissante, `kumod --validate`, bascule atomique, contrôles de santé, retour automatique) ; socle local non pilotable (relais, écoutes, plafond global, homme mort, pare-feu) ; contrôle de dérive toutes les 5 minutes avec pause en cas d'écart. Remontée en V0 : INF-036 à 040. » | 10 | V0 |
| C17 (I9) | 05 § A | « Ubuntu 24.04 n'a pas de paquet KumoMTA officiel (paquets : Rocky 8/9, Ubuntu 20.04/22.04, Amazon Linux ; Ubuntu 24 seulement testé par la communauté). Choix : image officielle `ghcr.io/kumocorp/kumomta` figée par empreinte, en réseau hôte, sur Ubuntu 24.04 ; même image au banc et en production ; tags `latest` et `main` interdits. » | 0,5 | V0 |
| C18 (I15) | 03 § 7.2, assistant DNS de 07 | « Le plan DNS de chaque domaine contient deux familles : KumoMTA (SPF de `bounce.`, DKIM `k1`, PTR et HELO) et l'hébergeur des boîtes (MX, SPF `include:`, DKIM de l'hébergeur), pour que les réponses de Will depuis le webmail soient authentifiées. Ajouter `abuse@`, `postmaster@`, MTA-STS `testing` et TLS-RPT. » | 1 | V0 |
| C19 (I8) | 01 § 1, puce « Logiciel de secours » | « Logiciel de secours : Postfix + rspamd (signature DKIM et contrôle), sans webhook natif, débits rudimentaires. » | 0 | V0 |
| C20 (I16) | 03 R3, 00 et 10 § 10 | « Port 25 Hetzner Cloud : bloqué par défaut, demande possible après un mois **et** le paiement de la première facture, au cas par cas, par compte ; compter 5 à 7 semaines. Déclarer l'usage honnêtement. Risque : la politique d'usage interdit le courrier non sollicité en masse, et une plainte peut faire fermer le compte ; garder le compte « envoi » séparé et demander par écrit au support si une fermeture toucherait l'autre compte. OVH en parallèle : anti-spam automatique, blocage de l'IP sur faux positif possible. » | 0 | V0 |
| C21 (I17) | 03 § 9 | Insérer l'étape 6 : « Mode témoins seulement : le socle local du serveur refuse tout destinataire hors de la liste des témoins et de Will ; 3 jours avec Will + 4 témoins (Gmail, Outlook.com, Yahoo, Microsoft 365 pro), puis levée par l'owner. » | 1 | V0 |
| C22 | 03 § 9, point 3 | Ajouter les scénarios B1 à B20 du § 3.1 du fichier 13, le réseau `internal: true` et les puits programmables. | 3 | V0 |
| C23 | 03 § 6, ligne « Authentification » | Ajouter : « La signature couvre aussi l'identité du serveur et un numéro de séquence par serveur ; un trou de séquence déclenche une réconciliation immédiate. HMAC calculé en Lua (`kumo.digest.hmac_sha256`), secret dans un fichier `0600` hors de la configuration générée. » | 0,5 | V0 |
| C24 | 03 § 2.5 et § 10.1 | « Un refus temporaire (4xx) à l'injection (contre-pression : mémoire au-delà de la limite douce, spool lent) = tranche reportée, jamais un nouvel essai en boucle ; `memory_over_limit_count` ou `rocks_spool_load_shed_active` → pause de la vague et alerte. » | 0,5 | V0 |
| C25 (I18, I19) | 03 § 11 | Remplacer la colonne V1 par le tableau du § 1.15 du fichier 13 (≈ 60 à 140 € par mois pour Axion seul). Ligne « Listes noires » : « licence Spamhaus à vérifier ; les miroirs publics et le DQS gratuit sont réservés au non commercial ». | 0 | V1 |
| C26 (I20) | 03 § 13, ligne V2 | « V2 : plusieurs serveurs pour la résilience et pour les locataires clients (un serveur par compte client de préférence, 05 D-C6), pas pour le débit d'Axion : un nœud tient 5 000 par jour. » | 0 | V2 |
| C27 | 03 § 1.12, nouvelle garde (RES-060 remontée) | « Garde anti-dispersion : au plus 2 domaines par IP, au plus 1 ressource nouvelle par 15 jours ouvrés, pas deux IP du même /24 ajoutées ensemble, pas de nouveau domaine dans les 30 jours qui suivent un listage. » | 1 | V0 |

**Total.** V0 : environ **+28 jours-agent bruts** (C3 2, C6 0,5, C7 1,5, C8 1, C9 1, C10 1, C11 1, C14 0,5, C15 0,5, C16 10, C17 0,5, C18 1, C21 1, C22 3, C23 0,5, C24 0,5, C27 1, C13 −1).

À déduire :
- environ 6 j que 03 comptait déjà dans E3 pour les gabarits de configuration et le runbook, que C16 remplace ;
- environ 3 j de travail de V1 (configuration générée, Cloudflare non compris) qui ne sont plus à refaire.

**Net : environ +19 jours-agent en V0.** V1 : +4 j (migration du déploiement du CRM vers le tirage, C15).

---

## 6. Ce qui reste risqué (après corrections)

| # | Risque | Gravité | Parade restante |
|---|---|---|---|
| RR1 | Port 25 refusé par les deux hébergeurs, ou compte fermé pour la politique d'usage | Majeur | Deux demandes en parallèle dès maintenant, usage déclaré honnêtement, compte séparé, troisième piste « serveur dédié » à étudier ; aucun relais payant pour le froid |
| RR2 | Signaux de plainte invisibles (pas de FBL en B2B) | Majeur | Règles absolues toutes sources (C10, C11), témoins chaque jour, frein sur les réponses hostiles |
| RR3 | Will seul : réponses non traitées, absences | Majeur | Frein humain (C7), mode absence (06 C7), plafond utile de 600 à 800 par jour |
| RR4 | CRM compromis qui signe une configuration malveillante | Majeur | Socle local non pilotable, validation de l'owner avec 2FA pour tout changement qui augmente le risque, délai de 10 minutes, dérive |
| RR5 | Dette SSH du CRM (clé root dans GitHub, `ssh-keyscan` sans épinglage) | Majeur | Hors périmètre de l'envoi, mais le serveur d'envoi ne doit jamais être joignable depuis M1 en SSH ; migration C15 en V1 |
| RR6 | Image KumoMTA non officielle sur Ubuntu 24.04 (réseau hôte, droits) | Moyen | Image officielle figée, kit de conformité, ou bascule vers Rocky 9 si un défaut apparaît |
| RR7 | Règles Gmail et Yahoo vues de seconde main | Moyen | Relire les pages officielles une fois les domaines autorisés dans la session ; appliquer de toute façon le niveau « masse » dès le premier message |
| RR8 | Licence Spamhaus pour un usage commercial | Faible | Lire les conditions ; sinon un abonnement modeste ou un contrôle manuel quotidien de 2 IP et 4 domaines |
| RR9 | Vivier trop petit pour la V1 | Moyen | Mesurer le vivier vérifié avant de dépasser P7 |
| RR10 | Hébergeur des boîtes sans fourre-tout sur sous-domaine | Moyen | Critère de choix D-70 ; sinon écouteur entrant KumoMTA (C4, V1) |

---

## Résumé (20 lignes)

1. L'architecture est juste : CRM, SMTP AUTH dans WireGuard, KumoMTA qui signe DKIM, Internet, webhook et tirage. On garde KumoMTA.
2. Vérifié dans la doc officielle (dépôt KumoMTA) : API d'injection et d'administration, kcli, environ 142 métriques Prometheus, contre-pression, `kumod --validate`, ACL depuis 2026.03.
3. Danger 1 : `trusted_hosts` ouvre toute l'API HTTP sans authentification. Réglage : localhost seulement, Basic + ACL, `inject` refusé au CRM.
4. Danger 2 : SMTP AUTH exige STARTTLS, même dans le tunnel, et `relay_hosts` ne doit jamais contenir le CRM ; `authz = authc` exigé.
5. Danger 3 : l'API d'injection HTTP lance MiniJinja par défaut ; « Static » obligatoire si elle sert.
6. Ubuntu 24.04 n'a pas de paquet officiel : image GHCR officielle figée par empreinte, en réseau hôte.
7. Gmail, Microsoft 365 et les messageries françaises n'envoient pas d'ARF : les plaintes se comptent toutes sources.
8. Ports entrants : le plan se contredit. V0 sans port entrant (`bounce.` chez l'hébergeur des boîtes, relevé par IMAP).
9. Le dépôt viole déjà la règle SSH (25 workflows avec une clé root) et alerte encore par Telegram : ne jamais l'étendre au serveur d'envoi.
10. Chaîne par l'interface : base, paquet signé sans secret, agent tireur, validation, bascule, santé, retour automatique, dérive toutes les 5 minutes. Faisable en V0 (≈ 10 j).
11. Restent manuels en V0 : achats, DNS dans Cloudflare, PTR, ticket du port 25, création des boîtes, création du VPS.
12. Le banc est fermé à Internet, avec 20 scénarios (relais, AUTH, ACL, contre-pression, configuration falsifiée, dérive, homme mort).
13. Essai à blanc en 3 étapes : simulation, puits sur le vrai serveur, puis « témoins seulement » verrouillé côté serveur.
14. 15 critères avant le premier envoi ; puis 3 jours Will + 4 témoins ; puis J1 = 20 organisateurs, arrêt à 2 rebonds durs ou 1 plainte.
15. Volume : la courbe de 03 (20 → 250 → 2 000) est la seule à garder ; 01 et 02 (150) sont à corriger.
16. Will seul ne traite que 15 à 25 réponses par jour : plafond utile de 600 à 800 par jour, avec un frein automatique.
17. Au lieu de 14 à 16 boîtes : une boîte par domaine au nom de Will, 300 par jour au plus, 2 boîtes en V0 et 4 en V1 (à valider par Will).
18. DMARC : `p=none` avec `rua` en V0, `quarantine` après 4 semaines alignées, `reject` en V1. Postmaster v2 sans réputation, et muet à ce volume.
19. Coûts : V0 ≈ 30-80 €, V1 ≈ 60-140 € par mois ; 27 corrections, net ≈ +19 j-agent en V0, +4 j en V1.
20. Risques restants : port 25 et politique d'usage de l'hébergeur, plaintes invisibles, Will seul, CRM compromis (parade : socle local), règles des messageries vues de seconde main.
