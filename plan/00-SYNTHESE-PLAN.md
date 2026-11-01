# Synthèse : rendre le CRM Pro complet (envoi, campagnes, clients) : 30/10/2026

RIEN N'EST CODÉ. Ce sont des plans écrits par des agents en lecture seule ; les constats n'ont pas été rejoués ni recoupés par un second relecteur (aucun passage du critique de complétude sur ce plan). Fichiers : 01 architecture et dépôt, 02 ce qui manque au CRM, 03 module d'envoi, 04 sécurité et 2FA par e-mail, 05 clients, licence et multi-locataire.

## Réponses aux questions de Will
- Sans PowerMTA ni MailWizz : OUI. KumoMTA (Apache-2.0 selon l'agent, gratuit, support payant facultatif), choisi par Will le 28/09 (D-02). Repli : Postfix + rspamd.
- KumoMTA payant un jour : non garanti. Les versions déjà publiées restent Apache-2.0 pour toujours ; protections : version figée par empreinte, copie du code et des binaires, contrat d'interface remplaçable, repli Postfix testé (8 à 15 jours-agent, sans nouvelle chauffe). Redis : rester en 7.2 ou passer à Valkey.
- Même dépôt ou autre ? MÊME dépôt (axion-crm-pro, public) pour le code et les modèles de configuration avec valeurs fictives ; secrets hors git ; données dans la base. Pas de dépôt privé (règle « jamais payer GitHub »).
- Chez des clients : oui, avec une installation par client d'abord ; le client est l'expéditeur, Axion son sous-traitant (art. 28).
- Campagnes : couvertes en entier (ciblage ET/OU/SAUF, séquences 1 à 4 étapes, gabarits, A/B, validation, planification, presse, stats sans pixel) ; la lettre d'information passe aussi par le moteur du CRM.
- Complet en fonctions : oui ; seuls les volumes démarrent petit (V0 20-50 puis environ 300 par jour, V1 1 000-2 000, V2 jusqu'à 5 000).

## Charge et coût (estimations d'agents, peu certaines)
- Module d'envoi : V0 environ 138 jours-agent (15 lots, 8 à 10 semaines avec 3 ou 4 agents), V1 115 à 135, V2 70 à 90.
- CRM hors envoi : environ 185 jours-agent en 5 lots (socle sûr 22, travail quotidien 38, campagnes 50, réponses/RDV/mesure 45, clients et échelle 60).
- Sécurité 2FA e-mail et correctifs : 7 petites PR.
- Coût mensuel : environ 35 à 90 € en V0, 120 à 280 € en V1, 400 à 650 € en V2 ; par client 25 à 60 €. Aucune licence.

## URGENT (décisions de Will, rien n'a été fait)
4. Notification CNIL de la fuite du 19/08 restée un brouillon.
5. Information art. 14 en retard pour les organisateurs collectés les 26-27/09.

## Hors code, avec délais incompressibles
Acheter 2 domaines d'envoi (21 jours d'âge), ouvrir le compte Hetzner « envoi » (un mois et une première facture avant la demande de port 25) et un VPS OVH en plan B, compte Cloudflare « envoi », hébergeur des boîtes de réponse, vérificateur d'adresses tiers.

## Décisions de Will (cumul)
Dépôt et licence : propriétaire source visible (recommandé) ou AGPL. Fin de contrat client : rendre les données par export (concilier « jamais de suppression » et art. 28.3.g). Base de prospection d'Axion jamais fournie aux clients. Installation par client d'abord. Serveur d'envoi sur le compte du client ou mutualisé. Liste d'opposition par client. Lettre d'information via le moteur du CRM. Plan accéléré D-86. Alertes dans la console et par e-mail, Telegram éteint (cohérent avec « plus de push » du 24/10) ; « engagement minimal 5 % » à redéfinir en réponses humaines (pas de pixel). Hébergeur de M3 (D-03), entité expéditrice SAS ou OÜ (D-07, D-26). 2FA e-mail : lien magique éteint ou non, expéditeur, codes de secours, paramètres. Un code à chaque connexion ou appareil de confiance 30 jours. Quels champs reviennent du CRM vers la console. Date d'ouverture des TPE/PME. Deux workflows qui suppriment encore des fiches : les éteindre ? Pas de validation de prix.

## Écran de pilotage
Source à reprendre : Backlink Engine (sauvegarde du 17/10 dans VS_CODE\Sauvegardes\Sauv_backlink_engine\2026-10-17_03-00-02\code\), 7 écrans spécifiés dans le fichier 03, refaits dans la console du CRM Pro. Mission Control n'apporte rien de vital.

## Décision de Will du 30/10 (systeme.io)
Aucun lien avec systeme.io. Les 6 ajouts N1 à N5 et la marque blanche du fichier 09 sont REJETÉS : ne pas les inclure dans le plan.
