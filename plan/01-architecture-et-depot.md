# 01 : Architecture de l'envoi en masse et choix du dépôt, CRM Pro (30/10/2026)

Version condensée du rapport du concepteur (le rapport complet était dans le message de l'agent). Conception en lecture seule, constats d'agent, sources web consultées le 30/10/2026. ATTENTION : les exigences de Will ajoutées après ce rapport (déploiement chez des clients, campagnes au cœur, CRM complet en fonctions) sont traitées dans le fichier 05-clients-licence-et-multi-locataire.md.

## 1. Envoyer sans PowerMTA ni MailWizz : oui (certitude élevée selon l'agent)
- Option retenue : KumoMTA (dépôt KumoCorp, licence Apache-2.0 selon l'agent), déjà choisie par Will le 28/09 (D-02). Fait pour le volume : DKIM, groupes d'IP, débits par messagerie, classement des rebonds, webhook JSON natif. Config en Lua.
- Logiciel de secours : Postfix + OpenDKIM (pas de webhook, débits rudimentaires).
- Écartés : Haraka (envoi pauvre), Stalwart (double licence AGPL + propriétaire), relais payants Amazon SES / Brevo / Mailgun / SendGrid (la prospection à froid est contraire à leurs règles, risque de compte suspendu), boîtes Google/Microsoft envoyant en SMTP (contraire à leur politique).
- Hébergeur : port 25 sortant bloqué par défaut chez Hetzner (déblocage demandé après un mois de compte et une première facture, au cas par cas, refus possible) ; OVH incertain ; Scaleway demande des pièces. Ouvrir tout de suite un compte Hetzner « envoi » séparé et un VPS OVH en plan B.
- Coût de départ estimé par le cahier : environ 22 à 45 € HT par mois, plus les domaines (10 à 15 € par an chacun). Aucune licence.
- Démarrage : 1 VPS d'envoi, 1 IP, 2 domaines neufs, 150 par jour au plus puis environ 1 500 par jour après 6 à 9 semaines de chauffe. Montée : une cohorte (1 IP + 2 domaines + 10 boîtes) tous les 15 jours ouvrés, puis un second nœud.

## 2. Ce qui remplace MailWizz dans le CRM Pro
Existe : listes manuelles, segments (partiel, environ 50 %), liste de suppression et `peutRecevoir`. À créer dans `backend/app/Emailing/` : campagnes et composition, serveurs/rotation, désinscription en un clic RFC 8058, webhook d'événements, FBL/plaintes (ARF), statistiques (aucun pixel d'ouverture), revérification de l'éligibilité au moment de l'injection.

## 3. Dépôt (recommandation de l'agent, à confirmer par Will)
Trois lieux, zéro dépôt privé :
- Code applicatif et modèles de configuration du serveur (avec valeurs fictives) : `axion-crm-pro`, public.
- Valeurs d'exploitation et données personnelles : base du CRM.
Raisons : un secret n'a sa place dans aucun dépôt ; la règle « jamais payer GitHub » du 25/10 exclut un dépôt privé avec CI ; le dépôt public est définitif (26/08). Gardes à ajouter : bloquer clés PEM, IP publiques et `axion-ia.com` comme expéditeur ; rendre gitleaks et la garde des données personnelles obligatoires pour fusionner.

## 4. Flux
CRM (EnvoiAutorise, re-vérifie à l'injection) → SMTP AUTH dans un tunnel WireGuard → KumoMTA sur serveur séparé (DKIM) → Internet. Événements : webhook KumoMTA signé HMAC (en-tête, jamais dans l'URL) → table idempotente → AppliquerRetour (rebond dur = suppression, mou = compteur en base, plainte = opposition, désinscription = opt_out). Réponses, STOP, rebonds différés, ARF : relevés par IMAP. Désinscription : go.<domaine d'envoi>. Sonde externe quotidienne (coupe-circuit). ZeptoMail inchangé.

## 5. Étapes E0 à E11 (chacune avec son test)
E0 gardes de sécurité exigées pour fusionner ; E1 ADR + dictionnaire ; E2 module fermé par drapeau + permissions ; E3 registres domaines/IP/boîtes + garde « jamais axion-ia.com » ; E4 rebonds mous en base ; E5 désinscription RFC 8058 ; E6 webhook signé + table d'événements ; E7 EnvoiAutorise + composition + injection ; E8 modèles de config KumoMTA + pare-feu + WireGuard ; E9 relève IMAP ; E10 chauffe minimale + console « Envois » ; E11 bout en bout sur banc puis premier message reçu par Will.

## 6. Pièges
Secret poussé dans le dépôt public (perdu) ; relais ouvert (incident SOS-Expat d'avril 2026) ; webhook falsifié ; envoi depuis la machine du CRM (interdit) ; trop de domaines d'un coup (snowshoe) ; port 25 refusé ; information art. 14 non prête (bloquant avant le premier envoi réel) ; décalage horaire de 2 h à corriger.

## 7. Décisions de Will
Confirmer « aucun dépôt privé » ; hébergeur du serveur d'envoi (D-03) ; achat de 2 domaines et compte Cloudflare « envoi » (D-40), hébergeur des boîtes (D-70) ; D-86 plan accéléré ; textes art. 14 et entité expéditrice (D-07, D-26) ; alertes dans la console ou Telegram.
