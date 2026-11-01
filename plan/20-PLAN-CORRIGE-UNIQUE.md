# 20 : PLAN CORRIGÉ UNIQUE : CRM Pro complet d'Axion-IA (01/11/2026)

**Document de référence.** Il remplace tous les totaux et tous les calendriers des fichiers 00 à 17. Si un autre fichier dit autre chose, c'est ce fichier qui fait foi, sauf décision contraire de Will.

Rédigé par le chef de chantier, en lecture seule. **RIEN N'EST CODÉ.** Aucun e-mail envoyé, aucun serveur touché, aucun secret lu ni recopié.

_[Passage retiré du dépôt public : voir les notes privées.]_

**Sources** : `plan/00` à `11`, puis les 6 vérifications `12` (interface), `13` (envoi et infrastructure), `14` (sécurité et isolation), `15` (conformité), `16` (campagnes et CRM), `17` (exécution cloud et calendrier).

**Unité** : 1 jour-agent (j) = une journée de travail d'un agent, tests compris. Les relectures Opus ajoutent + 15 %. Toutes les estimations sont incertaines à **± 30 %**.

---

## 1. Vue d'ensemble (15 lignes)

1. **Quoi** : un CRM Pro complet avec son module d'envoi d'e-mails (campagnes au cœur), d'abord pour Axion, puis pour les clients de la console des automatisations.
2. **Moteur d'envoi** : KumoMTA, sur un serveur séparé. Repli prévu : Postfix + rspamd.
3. **Règle d'or** : toutes les fonctions sont livrées complètes. Seuls les **volumes** démarrent petit (20 messages par jour au début).
4. **V0 (Axion seul)** : sécurité complète, CRM du quotidien, chaîne de campagne complète, envoi réel limité.
5. **V1 (console mutualisée)** : un seul logiciel pour plusieurs clients ; CRM Pro = module de base ; envoi = option ; un moteur d'envoi séparé par client.
6. **V2 (chez le client)** : installation sur le serveur du client, mises à jour par vagues, repli Postfix, 5 000 par jour.
7. **Ordre** : sécurité et isolation d'abord, puis moteur d'envoi, puis campagnes, puis écrans, puis essai complet.
8. **Semaine 1 (2 novembre)** : feu vert de Will, achats (domaines, serveurs), dossier CNIL, rotation des clés.
9. **Banc d'essai prêt** : vers le **11 décembre 2026**.
10. **Premier envoi interne** (Will + 4 boîtes témoins) : vers le **27 janvier 2027**.
11. **Premier envoi réel limité** (20 organisateurs) : vers le **2-3 février 2027**.
12. **Version console** (client pilote installé, isolé) : vers le **15 avril 2027**.
13. **Charge** : V0 ≈ **323 j**, V1 ≈ **212 j**, V2 ≈ **115 j**, soit ≈ **650 j-agent** (≈ 747 avec relectures).
14. **Condition des dates** : 6 routines Sonnet + 1 Opus jusqu'au premier envoi, puis 5 + 1. Avec 5 routines dès le début, le premier envoi glisse vers le **16-17 février**.
15. **Will** intervient 10 fois, surtout la semaine du 2 novembre, puis 10 minutes par jour (train de fusion).

---

## 2. Un seul total

### 2.1 Pourquoi les chiffres se contredisaient

| Chiffre annoncé | Où | Ce qu'il compte vraiment | Problème |
|---|---|---|---|
| V0 ≈ 246, V1 ≈ 186, V2 ≈ 92 | 17 | Tous les plans 00 à 11, sans doublon | **Écrit avant 12 à 16** : ne contient aucune de leurs corrections. « 432 j » = V0 + V1 seulement (V2 en plus : 524 j). |
| V0 ≈ 222, V1 ≈ 274, V2 ≈ 107 = 603 | 16 | Plans 00 à 11 + ses propres corrections (59 j) | Prend la V1 du module d'envoi de 03 **en bloc** (125 j), alors qu'une grande partie est déjà comptée dans les lots CRM, campagnes et écrans. |
| ≈ 82 j d'interface | 12 | Écrans manquants et corrections d'écrans | ≈ 36 j déjà comptés : dans les écrans de 17 (lot U), dans les lots de fonctions qui ont leur écran, et 6 j de travail serveur déjà dans 13 et 17. |
| ≈ 34 j de conformité | 15 | Gardes, textes, contrats | ≈ 22 j déjà dans les lots J1 à J4 et C3 de 17. |
| + 19 j en V0 | 13 | 27 corrections de l'envoi | ≈ 2,5 j déjà dans 17 (rapports DMARC, frein « réponses en attente »). |
| ≈ 27 j V0 + 5 j V1 | 14 | Correctifs de sécurité | ≈ 16 j déjà dans les lots S1 à S7 de 17. |
| V1/V2 de 17 | 17 | V1 = « confort et console », V2 = « 5 000/j » | **Pas la grille de Will.** Will : V1 = mutualisé, V2 = chez le client. 19 j passent donc de V1 à V2 (installation en une commande, repli Postfix). |

### 2.2 Le pont de calcul (méthode : base 17, plus le **net** de chaque rapport)

| Étape | V0 | V1 | V2 | Total |
|---|---|---|---|---|
| Base : fichier 17 | 246 | 186 | 92 | **524** |
| + 12 Interface (82 annoncés, 36 déjà comptés) | + 24 | + 19,5 | + 2,5 | + 46 |
| + 13 Envoi (≈ 20 annoncés, 2,5 déjà comptés) | + 16,5 | + 1 | 0 | + 17,5 |
| + 14 Sécurité (32 annoncés, ≈ 16 déjà comptés) | + 11,5 | + 4,5 | + 0,5 | + 16,5 |
| + 15 Conformité (34 annoncés, ≈ 22 déjà comptés) | + 6,5 | + 4,5 | + 1 | + 12 |
| + 16 Campagnes et CRM (59 annoncés, ≈ 25 déjà comptés) | + 10 | + 23,5 | 0 | + 33,5 |
| Déplacements V1 → V0 (tâches du jour, étapes de Will, appareil de confiance) | + 7,5 | − 7,5 | 0 | 0 |
| Déplacements V1 → V2 (grille de Will) | 0 | − 19 | + 19 | 0 |
| Arrondis | + 1 | − 0,5 | 0 | + 0,5 |
| **TOTAL RETENU** | **≈ 323** | **≈ 212** | **≈ 115** | **≈ 650** |

Le total retenu est **la somme exacte des lots du § 3**. Rien n'est compté deux fois.

### 2.3 Tableau final par phase

| Phase | Pour qui | j-agent | Avec relectures (+ 15 %) | Fourchette (± 30 %, sans relectures) |
|---|---|---|---|---|
| **V0 Axion** | Axion seul, envoi réel 20 → 250-300/j | **323** (dont 300 avant le 1er envoi, 23 pendant la montée) | **371** | 225 à 420 |
| **V1 Console mutualisée** | Axion + clients de la console (1er client : pharmacies) | **212** | **244** | 150 à 275 |
| **Jusqu'à la version console** | | **535** | **615** | 375 à 695 |
| **V2 Chez le client** | Clients en vente directe, jusqu'à 5 000/j | **115** | **132** | 80 à 150 |
| **TOUT** | | **≈ 650** | **≈ 747** | 455 à 845 |

Pourquoi plus que 17 (524) : les 6 vérifications ont trouvé de vrais trous (durcissement de l'isolation, configuration du serveur faite à la main, base sectorielle absente, téléphone absent, écrans d'exploitation absents). Pourquoi moins que la somme brute (524 + 82 + 34 + 19 + 32 + 59 ≈ 750) : ≈ 100 j étaient comptés deux fois.

---

## 3. Liste des lots finale

**Légende.** Modèle : **S** = Sonnet exécute ; **O** = Opus conçoit, relit ou audite (jamais Haiku). « a » = avant le premier envoi réel ; « b » = pendant la montée en volume (après le premier envoi, avant 250/jour). Chaque lot fini passe la relecture Opus et la critique de complétude.

Références des corrections : **12** C-xx et UI-xx ; **13** C1 à C27 (notées « E-Cxx ») ; **14** PR-0 à PR-13 ; **15** C-xx, C-Gxx et D1 à D14 ; **16** CC-xx.

### 3.1 Phase V0 : Axion (≈ 323 j)

#### Sécurité et socle (pistes A, B, C)

| ID | Contenu (corrections intégrées) | Dépend de | j | Quand | Modèle | Preuve de réussite |
|---|---|---|---|---|---|---|
| **S1** | Durcir l'authentification ; anti-rejeu ; limiteur par compte (14 PR-0) | — | 1 | a | S + audit O | tests rouges puis verts ; rejeu refusé |
| **S2** | Mailer d'authentification isolé, jamais journalisé ; démarrage refusé en production s'il est mal réglé (04 PR-C, 14 PR-1) | — | 1,5 | a | S | test « aucun envoi commercial par ce canal » ; démarrage refusé si mal réglé |
| **S3** | 2FA par code e-mail complète : codes de secours et liens à usage unique consommés de façon atomique ; changement d'adresse validé par l'ancienne ; réinitialisation qui prévient l'utilisateur ; session 12 h + appareil de confiance 30 jours révocable ; code redemandé pour les gestes sensibles (04 PR-D, 14 PR-4, 16 X-2) | S2 | 6 | a | S + audit O | 16 tests de 04 + tests d'atomicité verts |
| **S4** | Écrans « Connexion et code » et « Sécurité du compte » (07 § 3.13 ; 12 C-04, UI-12) | S3, U0 | 3 | a | S | parcours complet en e2e ; 0 violation d'accessibilité |
_[Passage retiré du dépôt public : voir les notes privées.]_
| **S6** | Droits : permission sur l'action de masse ; un admin ne nomme jamais un owner ; segments sensibles **fermés par défaut**, réglés **par espace** (presse ouverte seulement pour Axion) (14 PR-2, PR-3, PR-10 ; 16 CC-20, X-3) | — | 3 | a | S + audit O | tests d'autorisation verts ; nouvel espace = tout fermé |
| **S7** | Isolation entre clients : barrière Postgres (RLS) armée par défaut, refus de démarrer sans elle ; commandes sous contexte d'espace ; appartenance à l'espace vérifiée ; droits RGPD (export, effacement) **par espace** ; tables sans `workspace_id` migrées ; suite « deux clients factices » bloquante (14 PR-5 à PR-8 ; 17 S7, P6) | — | 14,5 | a | S + audit O sécurité | suite à deux clients verte sous le rôle de production ; démarrage refusé sans RLS |
| **S8** | Corriger le décalage de 2 h des horodatages (02 L9) | — | 1 | a | S | test heure de Paris |
| **S9** | Exploitation : copie hors site quotidienne, restauration testée, alertes console + e-mail, bouton « alerte de test », battement externe qui écrit à Will si le CRM se tait, seconde adresse d'alerte hors domaine Axion, workflows de purge éteints **après** la garde Sirene (C3) (17 S9 ; 16 CC-17) | — | 9 | a | S + relecture O | alerte de test reçue ; battement coupé → e-mail reçu ; restauration chronométrée |

#### Préparation multi-client (les 8 règles, dès la V0)

| ID | Contenu | Dépend de | j | Quand | Modèle | Preuve de réussite |
|---|---|---|---|---|---|---|
| **P1** | Décision d'architecture (ADR), drapeau du module (éteint), permissions, gardes CI « jamais axion-ia.com », fichiers partagés créés une seule fois (03 E0, 05 M0) | — | 6 | a | **O conçoit**, S code | ADR fusionné ; chaque garde a son test |
| **P2** | `workspace_id` sur l'opposition et les suppressions ; identité légale et quotas par espace (03 E1 ; 15 C-08) | P1 | 4 | a | S + audit O | l'opposition de A ne bloque pas B ; celle d'Axion gagne partout dans l'espace Axion |
| **P3** | Rien d'Axion en dur : Axion = un client parmi d'autres (05 M3) | P1 | 5 | a | S + relecture O | espace « Client factice » complet |
| **P4** | API signée CRM ↔ console, anti-rejeu | P1 | 2 | a | O conçoit, S code | tests de signature et de rejeu |
| **P5** | Arrêt d'envoi par client + arrêt général Axion (05 M5) | P2 | 3 | a | S | l'arrêt de A n'arrête pas B |

#### Envoi (pistes D, E, G)

| ID | Contenu | Dépend de | j | Quand | Modèle | Preuve de réussite |
|---|---|---|---|---|---|---|
| **E1** | Contrat « serveur d'envoi », simulateur, kit de conformité, banc fermé à Internet avec 20 scénarios, mode « témoins seulement » verrouillé côté serveur (03 E2 ; E-C21, E-C22) | P1 | 10,5 | a | O conçoit, S code | kit vert sur le simulateur ; 20 scénarios verts |
| **E2** | KumoMTA : image officielle figée par empreinte ; DKIM généré sur le serveur ; anti-relais ; tunnel privé ; authentification chiffrée obligatoire ; API d'administration jamais ouverte sans authentification ; client imposé par l'identité de connexion ; contre-pression ; homme mort ; sonde externe (03 E3 ; 08 F1, F2, F5 ; E-C8, E-C9, E-C17, E-C23, E-C24) | E1 | 20,5 | a | S + audit O sécurité | kit vert sur KumoMTA au banc ; relais refusé en boîte noire ; en-tête de routage falsifié ignoré |
| **E3** | Registres domaines, IP, boîtes, personnes titulaires ; plan DNS à deux familles (serveur + hébergeur des boîtes) ; garde anti-dispersion (2 domaines par IP au plus, 1 ressource nouvelle par 15 jours ouvrés) ; plafond par boîte en base (03 E4 ; E-C6, E-C18, E-C27 ; 16 CC-11) | P2 | 5 | a | S | DNS du banc contrôlé ; `axion-ia.com` refusé |
| **E3b** | **Configuration depuis la base** : l'interface décrit, le serveur **tire** un paquet signé, le valide à blanc, l'applique, retour automatique si échec ; socle local non pilotable ; contrôle de dérive toutes les 5 min (E-C16 ; 12 UI-15 partie serveur) | E2, E3 | 10 | a | O conçoit, S code | domaine ajouté par l'écran, appliqué sans SSH ; config falsifiée refusée |
| **E4** | Vérification des adresses : fournisseur, cascade, pré-vol de 30 jours ; coût affiché pour information (03 E5) | P2, H4 | 6 | a | S | 100 adresses factices ; coût affiché, rien bloqué |
| **E5** | Retours : webhook signé avec anti-rejeu, rebonds, VERP, relève IMAP (aucun port entrant public en V0), STOP, plaintes **toutes sources** (réponse hostile, `abuse@`, `postmaster@`) (03 E6 ; 08 F4 ; E-C4, E-C10, E-C11 ; 16 CC-19) | E1, E3 | 17 | a | S + audit O | doublons, désordre, retard 72 h, webhook falsifié : tous gérés |
| **E6** | Désinscription en un clic (RFC 8058) sous le domaine d'envoi ; page publique gardée après la fin d'un domaine (03 E7 ; 15 C-05, D2) | E5 | 6 | a | S | désinscription effective en moins d'une minute |
| **E7** | Chauffe et protections : courbe en jours effectifs, disjoncteurs, arrêt d'urgence, **frein humain** (capacité de réponse, 15/jour par défaut), mode absence (03 E8 ; E-C7 ; 16 CC-10) | E3, E5 | 15,5 | a | S + audit O | tests aux bornes ; « Tout arrêter » coupe l'envoi |
| **E8** | Surveillance : listes noires, boîtes témoins, test du matin, rapports DMARC (ingestion simple), inscription Postmaster/SNDS, boucle Signal Spam si elle existe ; sans Grafana (03 E11 ; E-C3, E-C12, E-C13 ; 16 CC-18) | E2, E5 | 8,5 | a | S | témoin rouge simulé → alerte console + e-mail |

#### Campagnes (piste F)

| ID | Contenu | Dépend de | j | Quand | Modèle | Preuve de réussite |
|---|---|---|---|---|---|---|
| **C1** | Moteur de campagnes : une seule porte d'envoi, ciblage ET/OU/SAUF, liste figée, gabarits versionnés, séquences 1-4 étapes, validation par version, relance dans le même fil, arrêt par entreprise, pause sur absence du bureau, contrôleur de contenu (règles de Will **par espace**, interdits élargis) (03 E9 ; 02 E1-E11 ; 15 C-06 ; 16 CC-07, CC-14) | E4, E6, E7 | 25,5 | a | S + relecture O | campagne de banc validée, figée, injectée ; personne en opposition jamais injectée |
| **C2** | Volume envoyable, lien de RDV, envoi unitaire, envoi fait à la main, « m'envoyer un test » (hors chauffe), garde « aucun pixel » (12 UI-06 ; 16 CC-15) | C1 | 7 | a | S | chaque fonction a son test |
| **C3** | Gardes légales : hors France refusé ; Sirene « diffusion partielle » jamais contactable (sans suppression) ; adresse de webmail refusée en froid ; questionnaire jamais automatique ; aucun lien vers `axion-ia.com` ; STOP élargi (06 C1, C2, M9 ; 15 C-G13, G14, G16, G18, C-07) | C1 | 4,5 | a | S | 6 tests rouges puis verts |
| **C4** | Rédaction des 3 séquences d'Axion (TPE/PME, organisateurs, fédérations) et de la page « pourquoi ce message » (16 CC-06) | J2 | 3 | a | **O rédige**, Will valide | textes validés par Will, contrôleur vert |

#### Réponses et mesure (piste G)

| ID | Contenu | Dépend de | j | Quand | Modèle | Preuve de réussite |
|---|---|---|---|---|---|---|
| **RP1** | Réponses : rattachement, tri, file, avis immédiat « intéressé » regroupé (sans nom dans l'e-mail) (03 E10 ; 12 UI-03) | E5 | 10 | a | S | 7 réponses factices triées ; STOP → opposition |
| **RP2** | RDV rattaché à la campagne, arrêt de séquence | RP1 | 3,5 | a | S | RDV factice rattaché |
| **RP3** | Résultats par campagne, étape, segment, expéditeur, sans ouvertures | C1, RP1 | 8 | a | S | chiffres du banc = journal |

#### Interface (piste H)

| ID | Contenu | Dépend de | j | Quand | Modèle | Preuve de réussite |
|---|---|---|---|---|---|---|
| **U0** | Système de design 2027 : clair seulement (pas de mode sombre), un seul bouton plein par écran, vocabulaire simple (12 C-03, C-09, C-10) | — | 5 | a | **O conçoit**, S code | gardes automatiques vertes |
| **U1** | Maquettes cliquables, test de 45 min avec Will | — | 4 | a | **O** | 7 tâches réussies |
| **U2-U9** | Écrans 1, 5 à 11 de 07, avec les corrections 12 C-01, C-02, C-05 à C-08, C-12, C-13, C-17 ; liste et suivi des campagnes (UI-58) | U0, U1 | 22 | a | S + relecture O | e2e par écran ; campagne en 5 min et 15 clics |
| **U10** | Passe finale : clavier seul, 360 px, lecteur d'écran | U2-U9 | 2 | a | **O** relit | critères 6.1 de 07 tenus |
| **U11** | Écrans d'exploitation indispensables avant l'envoi : centre d'alertes, réglages des alertes (console + e-mail seulement), serveurs et test du matin, adresses IP, ajout de boîte, règles de prudence (durcir seulement), configuration (écran de E3b), identité de l'expéditeur, frein, page publique de désinscription (12 UI-01, 02, 04, 05, 07, 13, 14, 15, 45, 62) | U0, lots servis | 12 | a | S | e2e par écran ; alerte de test reçue par les 2 canaux |
| **U12** | Autres écrans V0 : messages types, sauvegardes, journal, équipe, DMARC « qui envoie en votre nom », mise en route, vérification, horaires et pression, demandes RGPD, interrupteurs des automatismes, listes noires, ajout rapide, lien de RDV, réponses à rattacher (12 UI-08 à 11, 17, 19, 21, 26, 28, 30, 50, 55, 59, 61) | U0, lots servis | 12 | **b** | S | e2e par écran |

#### CRM du quotidien (piste I)

| ID | Contenu | Dépend de | j | Quand | Modèle | Preuve de réussite |
|---|---|---|---|---|---|---|
| **Q1** | Modifier et retirer un contact, ajout rapide, provenance, import de fichier, synchro sortante, mode d'emploi pour Will (02 A3, A4, J6, B4, K3, K6, L10) | S7 | 10,5 | a | S | modifier/retirer fonctionnent ; import de 100 lignes factices |
| **Q1b** | « Mes tâches » et rappel du matin ; étapes de Will (à contacter, contacté, répondu, rendez-vous, devis, gagné, perdu) ; actions de masse avec aperçu et annulation ; brouillon IA de séquence (16 CC-26, CC-13, CC-22, CC-08 a ; 17 Q4) | Q1 | 10,5 | **b** | S | tâches créées par les réponses ; lot de masse annulé |

#### Conformité (piste J)

| ID | Contenu | Dépend de | j | Quand | Modèle | Preuve de réussite |
|---|---|---|---|---|---|---|
| **J1** | Base légale par flux, bloc art. 14 par espace, registre art. 14 par adresse, alerte J+21 et refus J+30 (03 E13 ; 15 C-G15) | P2 | 6 | a | S + relecture O | premier message sans bloc art. 14 refusé |
_[Passage retiré du dépôt public : voir les notes privées.]_
| **J3** | Règles écrites : exception art. 17 et empreinte d'opposition gardée, tableau des tiers et DPA, repli hébergeur (06 M2, M3, M4 ; 15 C-10, C-11) | — | 2 | a | **O** | 3 fiches au registre des décisions |
| **D0** | Mise à jour des plans 00 à 11 selon ce fichier (volume 20/j, boîtes, DMARC, ports entrants, Telegram et marque blanche retirés, grille V0/V1/V2, renvois orphelins) (13 C1, C2, C5, C12, C19, C20, C25, C26 ; 16 CC-01, CC-05, CC-30, CC-31) | — | 1 | a | **O** | aucun chiffre contraire à ce fichier dans 00-11 |

#### Essai complet (piste T)

| ID | Contenu | Dépend de | j | Quand | Modèle | Preuve de réussite |
|---|---|---|---|---|---|---|
| **T1** | Scénarios complets, essai à blanc en production (zéro envoi), 3 jours « témoins seulement », écran « Feu vert » avec les 15 critères de 13 § 3.3 et les 8 bloquants de 15, J1 = 20 organisateurs (03 E14) | tout ce qui est « a » | 6 | a | S + audit O final | toutes les cases vertes ; authentification réussie chez les 4 témoins 3 jours de suite |

**Sous-total V0 : 300,5 j avant le premier envoi (a) + 22,5 j pendant la montée (b) = ≈ 323 j.**

### 3.2 Phase V1 : console mutualisée (≈ 212 j)

| ID | Contenu | Dépend de | j | Modèle | Preuve de réussite |
|---|---|---|---|---|---|
| **Q2** | Travail quotidien : notes et appels, Kanban « Affaires », opportunités, vues sauvegardées, export, historique ; écrans 2 à 4 (02 lot 2 sans Q1 ni Q1b) | Q1b, U0 | 27,5 | S + relecture O | Will travaille une journée entière dans le CRM, sans tableur |
| **Q3** | **Téléphone** : campagne multicanal (étapes e-mail + appel), file d'appels, script validé, issues fermées, opposition par téléphone, lien `tel:` sans numérotation automatique (16 CC-09) | Q2 | 9 | S | appel « opposition » → tous canaux arrêtés |
| **C5** | Campagnes V1 : comparaison de versions (A/B sur réponses positives), presse complète, messages déclenchés (formulaire en une phrase, **sans constructeur visuel**), récurrentes, score anti-spam | C1 | 15 | S | chaque fonction testée au banc |
| **C6** | Lettre d'information (si Will la confie au CRM) : double inscription, pages **au nom légal** du client (sans marque blanche) | C1 | 7 | S | inscription confirmée et journalisée |
| **RP4** | Répondre depuis la console, alerte à 24 h, entonnoir, rapports hebdomadaires, coûts visibles ; RDV d'un client par `{lien_rdv}` et bouton « RDV pris » (**sans agenda par client**) (16 CC-12) | RP3 | 15,5 | S | rapport hebdomadaire reçu ; RDV attribué à sa campagne |
| **E9** | Envoi V1 : files d'attente, rotation DKIM, expiration des domaines, Postmaster (statut de conformité), Cloudflare par API, capacité (13 : 3 j retirés, déjà faits par E3b) | V0 en production | 16 | S + audit O | alerte d'expiration 30 jours avant, testée |
| **J4** | Documents et contrôles V1 : D3 clients, D4 usage acceptable, D5 CGU/CGV, D6 contrat de sous-traitance et fin de contrat, D7 engagement de service, D8 notice, D12 AIPD complète, D13 base sectorielle ; contrôle d'entrée du client (SIREN, échantillon) ; règles 3 ans sans échange (sans suppression) ; aucune donnée client utilisée par Axion ; fiche FINESS/RPPS (15 C-12 à C-17, C-20, C-G17) | J2 | 15,5 | **O** juriste, S code | textes validés ; client factice refusé sans SIREN |
| **K1** | Rôles par client, accès du support limité et tracé, cycle de vie des utilisateurs (inviter, désactiver, transférer) (02 M2, I7-I10 ; 16 CC-25) | S7 | 9,5 | S + audit O | accès d'un client à un autre refusé |
| **K2** | Réglages plateforme → secteur → client ; options payantes (bouton grisé « Activer depuis la console ») ; **aucun catalogue de modèles** (02 M3 ; 16 CC-03) | P3 | 7 | O conçoit, S code | faux 2e secteur ajouté sans toucher au code |
| **K3** | Création d'un client (écran « Réglages › Clients », nom + repère couleur, sans étape « Marque ») et mise en route (02 M13 ; 12 C-11, C-15) | K2, U0 | 8 | S | client factice créé en 8 min |
| **K5** | Sauvegarde et restauration par client, chiffrement authentifié | S9 | 5 | S | restauration d'un seul client chronométrée |
| **K6** | Usage et état d'abonnement échangés avec la console par API signée ; un dépassement informe, ne bloque pas (02 M5 ; 16 CC-27) | P4 | 6 | S | compteur remis à zéro à la date anniversaire |
| **K7** | Effet de l'état d'abonnement : « suspendu » = envoi en pause, rien supprimé. **La facturation vit dans le Hub de la console** (16 CC-04) | K6 | 2 | O relit, S code | impayé simulé → envoi en pause, données intactes |
| **K8** | Diagnostic par client, supervision depuis la console | K6 | 6 | S | page de diagnostic d'un client factice |
| **K9** | API par espace, champs personnalisés, export complet et réversibilité ; export brut de la base sectorielle refusé (08 F7, F11 ; 16 CC-28) | K1 | 11 | S + audit O | clé d'API à portée limitée ; export brut refusé |
| **K10** | Propriétaire de fiche, recontact ; accroche IA par destinataire figée avant validation, sans fait inventé (16 CC-08 b) | Q2 | 9 | S + relecture O | phrase avec un fait inventé → rejetée |
| **K12** | **Base sectorielle** : fiche de référence + surcouche par client, attributions retirables sans rien supprimer, deux oppositions distinctes (16 CC-02) | K2, S7 | 12 | O conçoit, S code | base retirée → accès coupé, surcouche intacte |
| **S11** | Sécurité V1 : en-têtes de sécurité, journaux sans e-mail en clair, outils d'administration réservés à la plateforme, documentation d'API fermée, sauvegarde chiffrée authentifiée (catégories de 14 PR-11 à PR-13) ; déploiement du CRM par tirage d'image, sans clé SSH dans GitHub (E-C15) | S5 | 8,5 | S + audit O | plus aucune clé de serveur dans GitHub |
| **U13** | Écrans V1 de 12 non couverts par les lots ci-dessus : ajout de serveur, expiration, exports, conformité, synchro console, usage, clients et accès support, files, sources, mises à jour, accès API, rapports, tâches automatiques en phrases, aide (12 UI-16, 18, 20, 23-25, 27, 29, 31-44, 46, 56, 60) | U0 | 19,5 | S | e2e par écran |
| **K11** | Client pilote : deux clients factices puis le pilote, dans l'instance mutualisée | K1-K12 | 3 | S + audit O final | pilote isolé, sauvegardé à part, mis à jour sans coupure |

### 3.3 Phase V2 : chez le client (≈ 115 j)

| ID | Contenu | j | Modèle |
|---|---|---|---|
| **K4** | Installation en une commande sur le serveur du client, mise à jour par tirage, vagues, retour arrière (02 M8, M9 ; 05 M7) | 9 | S + audit O |
| **E10** | Repli Postfix + rspamd passé au même kit de conformité (05 M2) | 10 | S |
| **X1** | Plusieurs serveurs (résilience et clients, pas débit), 5 000/j, attribution du chiffre d'affaires, exercices, tests de charge | 80 (70 à 90) | S + O |
| **X2** | Lettre : éditeur par blocs, centre de préférences, version web | 9 | S |
| **X3** | Webhooks sortants signés | 3 | S |
| **S12** | Retrait de l'ancien code TOTP (04 PR-F) | 0,5 | S |
| **U14** | Écrans V2 de 12 (variante IA, import planifié, « à recontacter ») | 2,5 | S |
| **J5** | Fiches pays Belgique, Suisse, Canada (15 D14) | 1 | **O** |

Hors total, sur décision de Will : relais tiers (08 F20) et clics agrégés (08 F21), ≈ 5 j.

### 3.4 Où est passée chaque correction des rapports 12 à 17

| Rapport | Corrections | Où elles sont |
|---|---|---|
| 12 Interface | **71** : C-01 à C-17 (15 ; C-14 et C-16 n'existent pas) et 56 UI-xx | C-xx → U0, U2-U9, S4, K3 ; UI-xx → U11, U12, U13, U14 ; UI-03 → RP1 ; UI-06 → C2 ; UI-15 serveur → E3b ; UI-17 ingestion → E8 ; UI-58 → U2-U9 |
| 13 Envoi | **27** : C1 à C27 (25 en V0) | textes (C1, C2, C5, C12, C19, C20, C25, C26) → D0 ; code → E1, E2, E3, E3b, E5, E7, E8, S5, S11 |
| 14 Sécurité | PR-0 à PR-13, PR-C à PR-F | V0 → S1, S2, S3, S5, S6, S7 ; V1 → S11 ; V2 → S12 ; exigences du module d'envoi → E2, E5 |
| 15 Conformité | **14 documents** D1 à D14 ; gardes C-G13 à C-G18 ; C-01 à C-20 | V0 → J1, J2, J3, C3, C1, E6 ; V1 → J4 ; V2 → J5 ; C-01, C-18 → décisions de Will |
| 16 Campagnes | **CC-01 à CC-31** (CC-21 et CC-29 n'existent pas) | V0 → C1, C3, C4, E3, E7, E8, Q1b, S3, S6, S9, D0 ; V1 → Q3, RP4, K1, K2, K6, K7, K9, K10, K12 ; **aucune n'est rejetée** : CC-03 est gardée **sans catalogue de modèles**, CC-12 **sans agenda par client**, CC-31 retire marque blanche et Telegram |
| 17 Exécution | lots, pistes, routines, calendrier | repris tels quels, sauf la grille V1/V2 et le nombre de routines (§ 5) |

**Rien de rejeté par Will n'est au plan** : pas de constructeur visuel d'automatisations, pas de modèles clients, pas d'agenda par client, pas de connecteur systeme.io, pas de serveur MCP, pas de marque blanche, pas de mode sombre, pas d'alerte par téléphone ni Telegram.

---

## 4. Contradictions résiduelles à trancher

| # | Contradiction | Ce que disent les fichiers | Arbitrage proposé |
|---|---|---|---|
_[Passage retiré du dépôt public : voir les notes privées.]_
_[Passage retiré du dépôt public : voir les notes privées.]_
| R3 | **Volume de départ** | 01 et 02 : 150/jour ; 00 et 10 : 20-50 puis 300 ; 03 : 20/jour | **La courbe de 03 fait foi** : 20/jour au premier jour effectif, ≈ 250 en fin de V0, 2 000 au plus vers 66 jours effectifs. Plafond utile avec Will seul : **600 à 800/jour**. |
| R4 | **Boîtes d'envoi avec Will seul** | 03 et 06 : 14 à 16 boîtes avec des personnes réelles ; 13 : une boîte par domaine au nom de Will, 300/boîte ; 16 : une boîte par domaine au nom de Will, 150/boîte, 600/jour au plus | Accord sur le principe : **une boîte par domaine, toutes au nom de Will**. Écart sur le plafond par boîte : **150 en V0** (prudent, suffit pour 300/jour sur 2 boîtes), 300 seulement en V1 si les mesures sont vertes. **À valider par Will.** |
| R5 | **DMARC** | maquette de 03 : « none→ » sans date ; 17 : `p=none` à la création | **`p=none` avec rapports dès la création** ; **`quarantine`** après 4 semaines à 100 % d'alignement et au moins 500 messages ; **`reject`** en V1. |
| R6 | **Presse** | cahier : fermée ; décision du 01/10 : ouverte ; 14 : « fermé par défaut » recommandé | **Ouverte pour l'espace Axion seulement** (décision du 01/10, gardée en base avec sa date). **Tout nouvel espace démarre tout fermé.** Configuration absente = fermé. Les deux exigences sont tenues. |
| R7 | Sens de V1 et V2 | 03 et 17 : des volumes ; Will (24 et 26/10) : des modes de déploiement | Grille de Will : **V0 Axion, V1 mutualisé, V2 chez le client** (adoptée ici). |
| R8 | Durée de la 2FA | 04 : 12 h ; 02 : appareil de confiance 30 jours | Deux réglages différents : **les deux**, + code redemandé pour les gestes sensibles. |
| R9 | Ports entrants du serveur d'envoi | 03 : aucun ; 08 : rebonds reçus sur le port 25 | **V0 : aucun port entrant public.** Rebonds relevés chez l'hébergeur des boîtes. |
| R10 | Plafonds de coût | 03 : le plafond bloque ; 02, 05 : le prix informe | Plafond **technique** (messages/jour) = **dur**. Plafond **en euros** = **informe seulement**. |
| R11 | Base d'Axion chez un client | 03, 05 : jamais ; exemple de Will du 26/10 : base sectorielle vendue | Rien n'est **visible** chez un client **sauf** les fiches de la base sectorielle **attribuées**, tracées et retirables (K12). |
| R12 | Santé fermée contre 1er client pharmacies | 03 : santé fermée | Fermée chez Axion ; ouverte chez le client **par l'attribution** de la base Pharmacies. |
| R13 | Semgrep « exigé » | 04, 17 : l'exiger suffit ; 14 : inutile tant qu'il ne bloque pas | Semgrep **en cliquet bloquant** d'abord, puis exigé (S5). |
| R14 | Telegram et Grafana encore au plan, alerte Telegram encore dans un déploiement | 03, 08, 11 | **Retirés.** Alertes = console + e-mail. |
| R15 | Plaintes | 03 : seuil de plaintes ARF comme garde principal | La plupart des messageries B2B n'envoient pas d'ARF : **plaintes comptées toutes sources** (E5). |

---

## 5. Calendrier semaine par semaine (repris de 17, recalé)

**Ce qui change par rapport à 17** : la V0 passe de 246 à ≈ 300 j avant le premier envoi. Pour tenir les mêmes dates, il faut **6 routines Sonnet** (au lieu de 5) jusqu'à S13, plus la routine Opus de contrôle. Avec 5 seulement : premier envoi réel vers le **16-17 février 2027**. La marge du calendrier est presque nulle.

| Sem. | Dates | Contenu | Jalon / action de Will |
|---|---|---|---|
| S1 | 2-6 nov | S1, S2, S8, S5 (économie de CI), S7 démarre, P1 (ADR), U1, J2 | **W1 décisions, W2 achats, CNIL, rotation des clés** |
| S2 | 9-13 nov | S3, S7, S9, P2, E1 démarre, maquettes | ADR fusionné |
| S3 | 16-20 nov | S4, S6, P3, E1, E3, U0 | **W3 test des maquettes (45 min)** |
| S4 | 23-27 nov | P4, P5, E5, E2 (banc), E4, U0, écran 1 | domaines âgés de 21 jours (24 nov) |
| S5 | 30 nov-4 déc | E5, E2, E3b, C1 démarre, Q1, écrans 9 et 10 | **W4 demande de port 25 (Hetzner + OVH)** |
| S6 | 7-11 déc | E6, E7, E8, E3b, C1, RP1, écran 5, U11 | **BANC OK (≈ 11 déc)** |
| S7 | 14-18 déc | E7, E8, C1, RP1-RP2, écrans 6 et 7, U11 | **W5 relire art. 14 et séquences (1 h)** |
| S8-S9 | 21 déc-1er janv | lots sans décision de Will ; pas de train les jours fériés | semaines creuses |
| S10 | 4-8 janv | fin E7, C1, C2, C3, RP3, écrans 8 et 11, J1, J3 ; serveur réel si port 25 | port 25 obtenu (sinon : relais tiers temporaire, voir § 9, point 1) |
| S11 | 11-15 janv | fin C2-C3, RP3, U10, intégration | |
| S12 | 18-22 janv | T1 : scénarios complets, préproduction | **W6 second test (15 min)** |
| S13 | 25-29 janv | déploiement d'activation, essai à blanc, 3 jours « témoins seulement » | **PREMIER ENVOI INTERNE (≈ 27 janv)** ; passage à 5 routines |
| S14 | 1-5 fév | feu vert (toutes les cases), 20 organisateurs | **W7 ; PREMIER ENVOI RÉEL LIMITÉ (≈ 2-3 fév 2027)** |
| S15-S21 | 8 fév-26 mars | V0-b (U12, Q1b), puis Q2, Q3, C5, RP4, E9, K1, K2, K6, K12 ; montée P1 → P7 | ≈ 22 mars : 250/jour (fin de la montée V0) |
| S22-S23 | 29 mars-9 avril | K3, K5, K7-K10, J4, S11, U13 | client pilote sur le banc ; **W10** |
| S24 | 12-16 avril | K11 : client pilote dans l'instance mutualisée | **VERSION CONSOLE (≈ 15 avril 2027)** |
| S25-S27 | 19 avril-7 mai | début V2 ; 3e domaine acheté avant le 15 mars | 1 000/jour **seulement** si une 2e personne réelle ; sinon plafond 600-800 |
| S28-S32 | mai-juin | V2 ; chauffe du client pilote (6 à 9 semaines) | pilote à volume réel ≈ juin 2027 |

**Les 10 interventions de Will**

| # | Quand | Quoi | Temps |
|---|---|---|---|
| W1 | S1 | Feu vert + décisions urgentes du § 6 (bloc 1) | 1 h |
| W2 | S1 | Achats et comptes, CNIL, information du lot de septembre, rotation des clés (§ 7) | 2 h |
| W3 | S3 | Test des maquettes | 45 min |
| W4 | S5 | Demande de port 25 chez les deux hébergeurs, usage déclaré honnêtement | 20 min |
| W5 | S7 | Relire les textes art. 14 et les 3 séquences | 1 h |
| W6 | S12 | Second test en préproduction | 15 min |
| W7 | S13-S14 | Valider le premier message reçu, cocher le feu vert, autoriser l'activation | 30 min |
| W8 | chaque jour ouvré | Train de fusion de 18:00 (ou délégation, décision 11) | 10 min |
| W9 | dès S14 | Traiter les réponses et RDV (le frein le protège s'il s'absente) | 30-60 min/jour |
| W10 | S21-S24 | Client pilote, contrats (J4) | 2 h |

---

## 6. Décisions de Will (liste unique, dédoublonnée)

Une réponse courte suffit. **Recommandation en gras.** Les décisions déjà prises ne sont pas reposées (KumoMTA, alertes console + e-mail, pas de mode sombre, systeme.io et ajouts rejetés, Axion d'abord, aucun dépôt privé).

### Bloc 1 : cette semaine (S1)

| # | Question | Recommandation | Conséquence | Bloque |
|---|---|---|---|---|
| 1 | **Date de lancement du chantier : c'est Will qui la choisit** (rien ne démarre sans son feu vert explicite). Toutes les dates du plan se décalent d'autant. | **Décision de Will** | chaque semaine de retard décale toutes les dates | **BLOQUE LE PREMIER ENVOI** |
| 2 | ~~Entité expéditrice~~ **DÉCIDÉ : SAS française** (aucune société étrangère au plan) | — | les textes légaux sont écrits pour la SAS | — |
_[Passage retiré du dépôt public : voir les notes privées.]_
| 4 | Organisateurs collectés les 26-27/09 : leur envoyer d'abord une information sans offre, puis attendre 10 jours ouvrés ? | **Oui** | sinon ce lot (le premier ciblé) reste gelé | **BLOQUE LE PREMIER ENVOI** |
| 5 | Re-vérifier l'historique complet du dépôt et faire tourner les clés par précaution ? | **Oui, maintenant** | une clé publiée est perdue, même effacée ensuite | **BLOQUE LE PREMIER ENVOI** |
| 6 | Prospecter seulement en France pour l'instant ? | **Oui** | Suisse et Canada exigent un consentement même en B2B | **BLOQUE LE PREMIER ENVOI** |
| 7 | Une boîte d'envoi par domaine, toutes à votre nom ? | **Oui** | 2 boîtes en V0 ; plafond utile ≈ 600-800/jour tant que vous êtes seul | **BLOQUE LE PREMIER ENVOI** |
| 8 | Plafond par boîte : A = 150/jour, B = 300/jour ? | **A en V0**, B possible en V1 si les mesures sont vertes | A suffit jusqu'à 300/jour | non |
| 9 | Serveur d'envoi : compte Hetzner séparé **et** un VPS OVH en parallèle ? | **Oui** | port 25 : ≈ 5 à 7 semaines d'attente, refus possible | **BLOQUE LE PREMIER ENVOI** |
| 10 | Hébergeur des boîtes : exiger une boîte « fourre-tout » sur sous-domaine et la relève IMAP instantanée ? | **Oui** | sinon il faut ouvrir un port entrant sur le serveur d'envoi | **BLOQUE LE PREMIER ENVOI** |
| 11 | Train de fusion : A = vous fusionnez chaque soir, B = vous déléguez à la routine Opus les lots d'écrans et de textes, et gardez sécurité et envoi ? | **B** | 10 min/jour au lieu de 20 ; aucun lot sensible sans vous | non |
| 12 | 6 routines Sonnet + 1 Opus jusqu'au premier envoi (au lieu de 5 + 1) ? | **Oui** | sinon premier envoi ≈ 16-17 février | non (décale la date) |
| 13 | Mesurer sur le serveur l'état réel de l'isolation, du mode simulation et du mailer d'authentification, puis lancer S1 et S2 tout de suite ? | **Oui** | ferme les failles les plus graves en moins de 4 jours | non |
| 14 | Éteindre les workflows de purge qui suppriment des fiches, **après** la garde Sirene ? | **Oui** | conforme à « aucune suppression » sans rendre contactables des personnes protégées | **BLOQUE LE PREMIER ENVOI** (la garde) |

### Bloc 2 : avant fin novembre (réglages)

| # | Question | Recommandation | Conséquence |
|---|---|---|---|
| 15 | 2FA : session 12 h **et** appareil de confiance 30 jours révocable, code redemandé pour les gestes sensibles ? | **Oui** | un seul code par mois sur votre poste ; gestes risqués toujours protégés |
| 16 | Lien magique éteint quand la 2FA e-mail est active ? | **Oui** | durcit la 2FA |
| 17 | Expéditeur des codes : A = `crm@axion-ia.com` (transactionnel dédié), B = adresse du domaine du produit ? | **A** si le domaine est vérifié | n'utilise jamais un domaine d'envoi commercial |
| 18 | Garder 10 codes de secours et les paramètres (10 min, 5 essais, verrou 1 h) ? | **Oui** | — |
| 19 | Segments sensibles fermés pour tout nouvel espace, presse ouverte pour Axion seulement ? | **Oui** | respecte votre décision du 01/10 et protège les clients |
| 20 | Configuration du serveur appliquée depuis l'interface dès la V0 ? | **Oui** (déjà compté) | sinon chaque domaine ou boîte demande une intervention technique |
| 21 | DMARC : `none` puis `quarantine` après 4 semaines alignées, puis `reject` en V1 ? | **Oui** | protège vos domaines contre l'usurpation |
| 22 | Règles de prudence modifiables seulement dans le sens « plus prudent » en V0 ? | **Oui** | aucune fausse manœuvre possible au début |
| 23 | Contrôles exigés pour fusionner : Gitleaks + Semgrep bloquant ? | **Oui** | aucune minute de CI en plus |
| 24 | Capacité de réponses : 15 par jour par défaut ? | **Oui** | le frein ralentit les nouveaux messages si les réponses s'accumulent |
| 25 | Avis par e-mail regroupé pour chaque réponse « intéressée », sans nom dans l'e-mail ? | **Oui** | — |
| 26 | Interdits dans les messages : bloquer « agréé », « labellisé », « accrédité » **et** « Aucun gain garanti » (déjà interdit par vous), plus Grenoble, « certifié », Qualiopi ; « garanti » seul en avertissement ? | **Oui** | — |
| 27 | Menu « Pipeline » renommé « Affaires » ? | **Oui**, sauf si vous tenez au mot | vocabulaire sans anglicisme |
| 28 | Licence du code : A = propriétaire « source visible », B = AGPL ? | **A** | bloque la première vente, pas l'envoi |
| 29 | Téléphone : A = en V1 avec le premier client, B = dès la V0 pour vos prospects (+ 9 j) ? | **A** | B retarde le premier envoi d'environ 2 jours de calendrier |

### Bloc 3 : avant le premier client (décider d'ici fin janvier)

| # | Question | Recommandation | Conséquence |
|---|---|---|---|
| 30 | Base sectorielle (ex. pharmacies) : A = fournie aux clients en attribution retirable, B = jamais fournie ? | **A** (votre exemple du 26/10) | A ajoute un contrat propre et une information des pharmaciens |
| 31 | **Exception légale à votre règle « jamais de suppression »** : à la fin d'un contrat, Axion exécute une suppression **uniquement sur ordre écrit du client** (art. 28 RGPD) ? Axion ne décide jamais seule. | **Oui** | obligation légale ; ce n'est pas une suppression décidée par Axion |
| 32 | Données des clients jamais utilisées par Axion (pas de liste commune, pas d'entraînement d'IA) ? | **Oui** | Axion reste simple sous-traitant |
| 33 | Domaine et page de désinscription d'un client parti gardés 3 ans ? | **Oui** | les désinscriptions continuent de marcher |
| 34 | Première campagne de chaque client validée par un humain d'Axion ? | **Oui** | protège la réputation des serveurs |
| 35 | Facturation dans le Hub de la console ; le CRM reçoit seulement l'état d'abonnement ? | **Oui** (déjà compté) | 4 j économisés |
| 36 | Assistant client : un repère couleur à la place de l'étape « Marque » ? | **Oui** | cohérent avec « pas de marque blanche » |
| 37 | Devis d'assurance RC pro + cyber décrivant « envoi de prospection pour le compte de clients » ? | **Oui** | sans cette description, l'assureur peut refuser |
| 38 | Lettre d'information envoyée par le moteur du CRM ? | **Oui** | C6 en V1, sinon −7 j |
| 39 | Ouverture des TPE/PME (base INSEE) : date ? (seulement si pas déjà tranché) | **après la montée à 250/jour** | — |

### Bloc 4 : plus tard

| # | Question | Recommandation |
|---|---|---|
| 40 | Au-delà de 600-800/jour : nommer une 2e personne réelle pour des boîtes ? | à décider au printemps, selon les réponses |
| 41 | Relais tiers (F20) : l'autoriser **seulement comme secours temporaire** si le port 25 tarde ? Clics agrégés (F21) : non. | **Oui pour F20 en secours** (voir § 9), **non** pour F21 |
| 42 | Champs qui reviennent du CRM vers la console ? | à fixer pendant K6 |

---

## 7. Actions hors code de Will : semaine du 2 novembre

Ce sont des **horloges** : on ne peut pas les accélérer. Lancées le 2 novembre, elles sont prêtes avant la mi-décembre, **sauf le port 25** (5 à 7 semaines d'attente après la demande, voir § 9).

| # | Action | Délai incompressible | Remarque |
|---|---|---|---|
| H1 | Acheter **2 domaines d'envoi**, à des jours ou registraires différents, noms non en série ; DNS chez Cloudflare « envoi » ; DMARC `p=none` avec rapports dès la création | 21 jours d'âge (30 conseillés) | un site simple sur chaque domaine |
| H2 | Ouvrir le compte **Hetzner « envoi »** (séparé du compte du CRM, autant que possible) **et** un VPS OVH ; demander par écrit à Hetzner si une fermeture toucherait l'autre compte | 1 mois + 1re facture avant la demande de port 25 | usage à déclarer honnêtement en S5 |
| H3 | Choisir l'hébergeur des boîtes (fourre-tout sur sous-domaine, IMAP instantané) ; 2 boîtes à votre nom + 1 boîte technique avec alias | 1 à 2 jours | |
| H4 | Compte du vérificateur d'adresses et son contrat de sous-traitance | 1 à 2 semaines | |
| H5 | Entité expéditrice : **SAS française (décidé)** | — | les textes légaux sont écrits pour la SAS |
_[Passage retiré du dépôt public : voir les notes privées.]_
| H7 | **Sécurité** : rejouer Gitleaks sur l'historique complet, faire tourner les clés concernées, mesurer l'état réel du serveur (décisions 5 et 13) | 1 h | avant tout autre push sensible |
| H8 | Créer 4 boîtes témoins : Gmail, Outlook.com, Yahoo, Microsoft 365 pro (une 5e chez Orange ou OVH conseillée) | 1 h | servent au test du matin et à T1 |
| H9 | Mesurer la taille du vivier vérifiable (organisateurs, fédérations) | 1 h | à 300 nouveaux/jour, il faut > 6 000 adresses par mois |
| H10 | Lire les conditions Spamhaus pour un usage commercial | 30 min | les accès gratuits sont réservés au non commercial |
| Plus tard | 3e domaine **avant le 15 mars** ; devis d'assurance avant le 1er client | | |

---

## 8. Limites honnêtes

- **Rien n'est codé, rien n'est rejoué.** Tous les constats viennent de lectures de plans et de code par des agents, sans exécution.
- **Estimations à ± 30 %.** Les recouvrements retirés au § 2 (≈ 100 j) sont **mes** estimations : je n'ai pas relu chaque lot de 02 et 03 ligne à ligne pour savoir s'il contient déjà son écran.
- **Ce fichier n'a pas encore été relu** par un second agent (critique de complétude prévue par `REPRENDRE.md`).
- **Sécurité** : 14 a lu un clone partiel ; l'historique complet du dépôt n'est pas vérifié. L'état réel des réglages du serveur de production n'est pas mesuré. La protection de la branche `main` n'a pas été relue depuis le 30/10.
- **Envoi** : règles Gmail, Yahoo et Microsoft vues surtout de seconde main ; politique d'usage des hébergeurs face à la prospection non vérifiée par écrit ; prix non revérifiés en ligne.
- **Conformité** : textes de loi cités de mémoire par l'agent, à vérifier sur Légifrance et EUR-Lex avant validation. Aucun avis d'avocat.
- **Produit** : l'exemple de produit de Will du 26/10 est **reconstitué** par recoupement (document absent du dépôt).
- **Calendrier** : suppose 6 puis 5 routines tenues, 5 jours sur 7, des décisions en S1, un port 25 accordé. Marge presque nulle sur le premier envoi.
- **Humain** : la capacité de Will à traiter 15 à 25 réponses par jour est une hypothèse ; elle fixe le vrai plafond de volume.

---

## Résumé (20 lignes)

1. Un seul plan, une seule grille : **V0 Axion, V1 console mutualisée, V2 chez le client**. Complet en fonctions, petit en volume.
2. Total retenu : **V0 ≈ 323 j, V1 ≈ 212 j, V2 ≈ 115 j = ≈ 650 j-agent** (≈ 747 avec relectures), à ± 30 %.
3. Jusqu'à la version console : ≈ 535 j (≈ 615 avec relectures).
4. Les chiffres se contredisaient parce que 17 a été écrit avant 12-16, que 16 comptait la V1 d'envoi en bloc, et que 12, 14, 15 recomptaient des lots existants : ≈ 100 j de doublons retirés.
5. Les 6 vérifications ajoutent ≈ 126 j nets : isolation armée, configuration du serveur depuis l'interface, écrans d'exploitation, base sectorielle, téléphone, gardes légales.
6. 19 j passent de V1 à V2 pour suivre la grille de Will (installation chez le client, repli Postfix).
7. 71 lots au total (43 en V0, 20 en V1, 8 en V2) ; chaque correction de 12 à 17 a sa place (§ 3.4) ; aucune CC de 16 n'est rejetée.
8. Rien de rejeté par Will n'est au plan : ni constructeur visuel, ni modèles clients, ni agenda par client, ni systeme.io, ni MCP, ni marque blanche, ni mode sombre, ni Telegram.
9. Banc OK ≈ **11 décembre** ; premier envoi interne ≈ **27 janvier** ; premier envoi réel (20 organisateurs) ≈ **2-3 février 2027**.
10. Version console ≈ **15 avril 2027** ; client pilote à volume réel ≈ juin 2027.
11. Ces dates exigent **6 routines Sonnet** jusqu'au premier envoi ; sinon ≈ 16-17 février.
12. Volume : 20/jour au départ (courbe de 03), ≈ 250 fin mars, plafond utile **600-800/jour** tant que Will est seul.
13. Boîtes : une par domaine, toutes au nom de Will ; 150/jour par boîte en V0.
14. DMARC : `none` dès la création, `quarantine` après 4 semaines alignées, `reject` en V1.
15. Presse ouverte pour Axion seulement ; tout nouvel espace démarre tout fermé.
_[Passage retiré du dépôt public : voir les notes privées.]_
17. L'IP de production commitée est à retirer des fichiers, avec une garde CI.
18. 41 décisions simples (l'entité est décidée : SAS française), dont **9 BLOQUENT LE PREMIER ENVOI** (date de lancement, CNIL, lot de septembre, clés, France, boîtes, serveurs, hébergeur des boîtes, garde Sirene).
19. Semaine du 2 novembre : domaines, Hetzner + OVH, boîtes, vérificateur, entité, CNIL, rotation des clés, boîtes témoins, taille du vivier.
20. Limites : rien n'est rejoué, ce fichier n'est pas encore relu par un second agent, estimations à ± 30 %, marge du calendrier presque nulle.

---

## 9. Corrections issues de la relecture critique (01/11/2026)

Un second agent (Opus) a relu ce fichier. **Totaux recalculés : exacts** (323 / 212 / 115 = 650 j ; 71 lots ; 10 décisions bloquantes). Les points ci-dessous **s'ajoutent** au plan et priment sur les lignes contraires.

1. **Port 25 : le calendrier ne tient pas sans repli.** La demande part en S5 (début décembre), la réponse prend 5 à 7 semaines : accord entre le 6 et le 22 janvier. Un 3e hébergeur ne répare rien (il repart pour un mois). **Repli retenu : relais tiers temporaire (F20)** pour le premier envoi interne et réel, puis bascule vers le serveur propre dès l'accord. **Date réaliste :** premier envoi interne ≈ 27 janvier **seulement si** serveur réel ou relais prêt avant le 18 janvier ; sinon premier envoi réel limité décalé d'environ 3 semaines (fin février).
2. **Moteur de secours.** Le lot E10 (repli Postfix + rspamd) est en V2. **Proposition : l'avancer en V0 « b »** (après le premier envoi, +4 j environ) ; sinon écrire que le risque est accepté jusqu'en mai.
3. **Décisions déjà prises, reposées par erreur** (à traiter comme *confirmation*, pas comme question) : 11 (fusion déjà autorisée le 15/10 ; seule reste la délégation à plusieurs), 14 (purge déjà interdite), 19 (presse décidée le 01/10), 20 (déjà comptée), 35 (facturation dans le Hub décidée le 27/10), 39 (si pas déjà tranché).
4. **Décisions bloquantes absentes ou mal classées** : 17 (expéditeur des codes) à trancher **avant le 9 novembre** ; le choix du **vérificateur d'adresses** (H4) et de l'**hébergeur des boîtes** (H3) sont de vraies décisions qui bloquent E4 puis C1.
5. **Budget mensuel à annoncer avant les achats** : serveur d'envoi 30 à 80 €/mois en V0, plus domaines, vérificateur d'adresses et éventuelle licence Spamhaus (prix à revérifier).
6. **Questions trop techniques : à reformuler par leur effet** avant de vous les poser (10, 13, 16, 21, 23, 28). Les 15, 16 et 18 (2FA) fusionnent en une seule.
7. **Lots à corriger** : P1 doit inclure le **modèle de données de la base sectorielle** (double opposition) ; E3 doit retrouver le **PTR** (indispensable à l'envoi) et le **contrôle DNS quotidien** (+3 j) ; les écrans « réponses à rattacher » et « demandes RGPD » passent de U12 à U11 (avant le premier envoi) ; les étapes commerciales « rendez-vous » et « contacté » sont posées par RP2 et C1, pas par Q1b.
8. **Zone grise avec vos rejets** : l'héritage « plateforme → secteur → client » (lot K2) ressemble aux « modèles prêts à l'emploi » que vous avez rejetés. À présenter comme des **réglages**, ou à confirmer avec vous.
9. **Les 8 règles de préparation multi-client** sont toutes au plan, dispersées : règles de contrat unique dans E1 ; aucun secret/IP/nom de client dans S5 et P1 ; test à deux clients factices dans S7 ; les autres dans P1 à P5.
10. **Petites incohérences** : « banc OK 11 déc » alors que E7 et E8 finissent en S10 (le banc est « OK sans les derniers réglages ») ; 3e domaine « avant le 15 mars » ; plafond de réponses 15/jour ici, 20 dans le fichier 13 (à trancher : **15** retenu) ; arrondis 16,5 → 16 et 33,5 → 34 au § 2.2 sans effet sur les totaux ; le plafond de 8 routines en parallèle tient compte des autres chantiers.

---

## 10. Décisions de Will du 01/11/2026 (elles priment sur le § 6)

**Entité d'envoi : SAS française (décidé).** **Date de lancement : Will la choisit** ; rien ne démarre sans son feu vert explicite, toutes les dates se décalent d'autant.

| Décision | Réponse de Will |
|---|---|
| 3 (point juridique en retard) | Suivre la recommandation : régler maintenant (brouillon préparé dans les notes privées, dépôt par Will) |
| 4, 5, 6 | Oui (information du lot de septembre ; historique + rotation des clés ; France seulement) |
| 7 | Oui : une boîte par domaine, au nom de Will (expéditeur réel et identifié ; jamais de faux nom) |
| 8 | **A : 150 envois par boîte et par jour en V0** (la chauffe progressive reste la limite avant) |
| 9 | **Un seul serveur d'envoi au début, le second prévu pour plus tard** (moteur remplaçable ; risque : refus du port 25 = repli par relais tiers, décision 41) |
| 10, 14 à 16, 18 à 28 | Oui |
| 11 | B (délégation à la routine Opus des lots d'écrans et de textes ; Will garde sécurité et envoi) |
| 12 | Plus de 6 routines possibles (jusqu'à 8) ; les délais incompressibles (domaines, port 25) limitent plus que le code |
| 13 | Oui : mesurer l'état réel du serveur actuel du CRM, **dans le premier lot (S1/S2), au lancement** |
| 17 | A : codes envoyés depuis l'adresse transactionnelle dédiée ; vérifier que le domaine est vérifié (premier contrôle de S2) |
| 29 | A : téléphone en V1 |
| 31, 33 à 38, 40 | Oui |
| 32 | Jamais d'utilisation des données d'un client sans son accord écrit |
| 41 | Oui au relais tiers (F20) **en secours temporaire** ; non à F21 |
| 30, 39, 42 | Plus tard |

**Ce qui reste, côté plan :** rien. **Côté Will :** choisir la date de lancement, déposer la notification CNIL (brouillon prêt), changer le mot de passe exposé, puis les achats de la semaine de lancement (§ 7).
