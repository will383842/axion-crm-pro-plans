# 10 : Tout ce qu'il faut faire, toutes les fonctions, et l'équipe (30/10/2026)

Synthèse de mes lectures des rapports 01 à 09 (constats d'agents non rejoués, pas encore relue par le critique). RIEN N'EST CODÉ. Le total de jours sera recalculé dans le plan corrigé (les trois totaux actuels se contredisent, environ 46 jours sont comptés en double).

## 0. Conditions de Will à respecter partout
- Complet en fonctions ; « démarrer petit » ne concerne QUE les volumes d'envoi (V0 environ 20-50 puis 300 par jour, V1 1 000-2 000, V2 jusqu'à 5 000).
- Les campagnes sont au cœur de l'outil.
- Ni PowerMTA ni MailWizz : KumoMTA, avec repli Postfix + rspamd ; moteur remplaçable.
- Ordre : d'abord le CRM Pro et l'envoi d'Axion, puis la version pour la console des automatisations, avec 8 règles de préparation dès le début (voir § 8).
- Dans la console : le CRM Pro est le module de base, l'envoi une option ; moteur partagé, séparé par client ; installation chez le client en V2 (décision du 24/10).
- Aucune connexion à systeme.io ; aucun des 6 ajouts qui en venaient (décision du 30/10).
- 2FA par e-mail, pas par application.
- Interface : parfaitement organisée, moderne, peu de texte, boutons et appels à l'action clairs, meilleures pratiques de début 2027, blocs colorés validés ; clair seul (mode sombre retiré le 02/10, à reconfirmer).
- Alertes dans la console et par e-mail, jamais de notification sur téléphone.
- Jamais de suppression de données de personnes ; jamais payer GitHub ; dépôt axion-crm-pro public, sans secret ni donnée personnelle ; jamais axion-ia.com comme expéditeur de masse ; ZeptoMail transactionnel intouchable ; aucun pixel de suivi ; le prix informe, ne bloque pas ; jamais Haiku ; réponses en français.

## 1. Sécurité et socle (avant tout le reste)
- 2FA par code e-mail à 6 chiffres (10 min, 5 essais, 10 codes de secours, mailer isolé « Axion_CRM_Pro »).
- Permission sur la modification en masse ; un admin ne peut plus nommer un owner ; segments sensibles fermés par défaut.
- Isolation entre clients ACTIVE ET PROUVÉE (rôle applicatif Postgres), test avec deux clients factices.
- Corriger le décalage horaire de 2 h avant toute planification d'envoi.
- Retirer ce qui est propre à Axion du code (édition « produit »).

## 2. CRM au quotidien
Modifier et retirer un contact (aujourd'hui « pas implémenté »), ajout rapide d'une personne, import de fichier depuis l'interface, champs personnalisés, pipeline Kanban, tâches « Mes tâches » et rappels, montants informatifs seulement, synchro CRM vers console (champs à choisir), exports journalisés, doublons, étiquettes, listes, audiences, demandes RGPD, journal d'audit, sauvegardes (copie hors site plus fréquente).

## 3. Serveur d'envoi et délivrabilité

## 4. Campagnes (le cœur)
Ciblage par étiquettes et listes en ET/OU/SAUF, exclusions, liste figée au départ, gabarits versionnés avec variables autorisées, relecture des formulations interdites (règles de Will), validation par Will attachée à une version, planification, séquences de 1 à 4 étapes en jours ouvrés, arrêt automatique à la réponse ou au rendez-vous, limite de pression par personne, variantes et test A/B, lien Calendly, campagnes presse (un média précis, jamais en masse), statistiques sans pixel, campagnes déclenchées par un événement, lettre d'information (double inscription, formulaires, centre de préférences, éditeur de blocs, version web, groupe d'IP séparé), pause, arrêt et retrait des messages en attente.

## 5. Réponses, rendez-vous, mesure
Relève des boîtes de réponse, tri automatique, STOP qui inscrit l'opposition, opposition par domaine entier, écran Réponses, alerte si une réponse attend plus de 24 h, frein quand les réponses s'accumulent, attribution d'un RDV à sa campagne, passage automatique en « opportunité » (à confirmer), désinscription en un clic (RFC 8058) sous le domaine d'envoi, traitement des rebonds et plaintes, tableau de bord de santé.

## 6. Conformité et juridique

## 7. Clients et console des automatisations
Édition produit, création de client (commande et écran), configuration hors dépôt, quotas et usage remontés à la console (API signée, remise à zéro à la date anniversaire), forfait et volume d'e-mails, diagnostic par client, export complet, sauvegarde chiffrée par client, facturation (acompte, options, impayés, TVA, Tiime), export des données en fin de contrat (à concilier avec « jamais de suppression »), base de prospection d'Axion jamais fournie (à confirmer), importation au catalogue.

## 8. Les 8 règles de préparation (dès le début)
Rien d'Axion en dur ; identifiant d'espace sur toutes les tables du module d'envoi (dont opposition et suppression) ; contrat unique avec le serveur d'envoi ; API signée ; aucun secret ni nom de client ni IP dans le dépôt ; gardes d'envoi « par entité » ; test à deux clients factices ; l'espace Axion traité comme un client parmi d'autres.

## 9. Interface (document 07)
13 écrans avec leurs 4 états : accueil « que dois-je faire aujourd'hui ? », fiche, pipeline et tâches, listes et étiquettes, assistant de campagne en 5 étapes, éditeur de message avec aperçu, boîte de réponses, santé des envois (feux), domaines et boîtes, liste d'opposition, statistiques, paramètres et clients (bascule de client), connexion et 2FA. Menu à 7 entrées. 12 principes (un bouton principal par écran, vocabulaire sans jargon, annuler pendant 8 s, accessibilité WCAG 2.2 AA). 5 parcours, cibles : campagne lancée en 5 minutes et 15 clics, « Tout arrêter » en 2 clics. Test de 45 minutes avec Will avant de coder les écrans d'envoi. Fichiers de style privés à recaler.

## 10. À faire par Will, hors code (délais incompressibles)
Acheter 2 domaines d'envoi (21 jours d'âge), compte Hetzner « envoi » (port 25 : un mois et une première facture) et VPS OVH en secours, compte Cloudflare « envoi », 14 à 16 boîtes de réponse (titulaires), hébergeur des boîtes, vérificateur d'adresses, rédaction des premiers messages, téléphone pour les pharmacies.

## 11. Équipe et hiérarchie
Règles : Opus pour concevoir, relire et auditer, Sonnet pour exécuter, jamais Haiku ; une commande lourde à la fois sur le PC (verrou) ; une PR par sujet ; coordination avec les autres sessions avant de toucher aux mêmes fichiers ; tests écrits d'abord.

- Will : décide, valide les écrans et les messages.
- Chef de chantier (session principale) : coordonne, tient le point d'avancement en tableau, le REPRENDRE et le registre des décisions.
- Leads (Opus), un par zone : Envoi et délivrabilité ; Campagnes ; Sécurité et isolation ; CRM au quotidien ; Clients et console ; Interface.
- Zone Interface :
  - Directeur UX/UI (Opus) : principes, système de design, parcours, cohérence avec « blocs colorés » ;
  - Rédaction UX (micro-texte en français simple, états vides, vocabulaire) ;
  - Développeurs front (Sonnet) : un écran par PR, avec composants du design système ;
  - Relecteur accessibilité et qualité (Opus) ;
  - Test utilisateur avec Will, 45 minutes, 7 tâches.
- Transversaux (Opus) : architecte (schéma, ADR), auditeur sécurité (isolation, IDOR), relecteur qualité avant chaque PR, gardien de la spec (registre des exigences), juriste (article 14, conditions générales, contrats), documentaliste, critique de complétude à chaque fin de lot.
- Développeurs back (Sonnet) : une tâche par PR, test rouge d'abord.

## 12. Ordre proposé
1. Hors code : domaines, comptes, boîtes (les délais courent pendant le code).
2. Sécurité et socle (§ 1) et les 8 règles (§ 8).
3. Serveur d'envoi et délivrabilité (§ 3) sur banc, puis essai à blanc.
4. Campagnes (§ 4), réponses (§ 5), écrans (§ 9).
5. Premier envoi réel limité : Will et 4 boîtes témoins, puis 20 organisateurs.
6. Montée de volume selon les rebonds et plaintes.
7. Version console (§ 7).
