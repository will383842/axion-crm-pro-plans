# 27 : AUDIT DE COMPLÉTUDE : écrans et serveur (lot V1 de vérification) : 01/11/2026

**Question de Will.** Est-ce que l'outil aura **vraiment tout**, dans les écrans **comme** dans le serveur, pour être extrêmement complet, facile à utiliser, facile à piloter, avec du **suivi partout** ?

**Méthode.** Lecture seule. Sources : plan 20 (lots), plan 21 (relevé du CRM existant), plan 23 et dossier `maquettes/` (45 pages, texte de chaque page relu), plan 24 (ADR), plan 26 (contrat d'envoi). Liste de référence construite à partir de ce que font les meilleurs outils : MailWizz et Lemlist, Instantly, Smartlead (prospection et envoi en masse), HubSpot et Pipedrive (CRM), PowerMTA et KumoMTA (serveur d'envoi). Rien n'a été exécuté, aucun code du CRM n'a été modifié. Aucune donnée réelle, aucune adresse de serveur.

**Lecture des colonnes.**
- **Plan 20** : la fonction est-elle dans un lot ? (lot entre parenthèses).
- **Maquette** : la fonction se voit-elle dans une page de `maquettes/` ? (nom de la page).
- **Existant** : le CRM actuel l'a-t-il déjà côté serveur (relevé du plan 21, complété par une lecture des contrôleurs) ? oui / non / partiel.
- **Verdict** : **OK** (prévue et visible, ou prévue en V1/V2 avec son écran) ; **À AJOUTER** (manque dans le plan, dans les maquettes, ou les deux) ; **VOLONTAIREMENT ÉCARTÉ** (décision de Will, ou choix du plan à faire confirmer).
- **Ajout** : pour chaque ligne À AJOUTER : lot proposé, effort en jours-agent (± 30 %), priorité V0 / V1 / V2.

**Écarts voulus par Will, respectés ici** : jamais systeme.io ; pas de constructeur visuel d'automatisations ; pas de modèles clients ; pas d'agenda par client ; pas de MCP ; pas de marque blanche ; pas d'alertes par téléphone ni Telegram ; clair seulement.

---

## 1. En bref (12 lignes)

1. **241 fonctions** contrôlées, en 12 blocs.
2. **176 OK** : prévues au plan et visibles (ou prévues en V1/V2 avec leur écran).
3. **52 À AJOUTER**, pour ≈ **48 j-agent** en tout : V0 ≈ 24,5 j, V1 ≈ 19,5 j, V2 ≈ 4 j.
4. **13 VOLONTAIREMENT ÉCARTÉES** : 10 par décision de Will, 3 par choix du plan (à confirmer par Will).
5. **Le socle est très complet** : sécurité, envoi, chauffe, DNS, conformité, alertes, sauvegardes sont tous prévus et maquettés.
6. **Le vrai manque est le pilotage fin** : pas de fiche d'un domaine ni d'une boîte, pas d'état par destinataire, pas de recherche « où est parti ce message ? ».
7. **Deuxième manque : les gestes de tous les jours sur une campagne** : dupliquer, reprogrammer, arrêter, mettre en pause depuis la liste.
8. **Troisième manque : cibler une étiquette directement** et voir les critères d'une liste dynamique.
9. **Côté serveur existant**, 3 fonctions sont prêtes mais sans bouton : export, vues sauvegardées, liens entre entreprises. Les brancher coûte peu.
10. **Répondre depuis le CRM** est en V1 : on propose de l'avancer en V0 « b » (sinon Will jongle entre deux outils).
11. **Test de simplicité** : sur 10 parcours, **4 tiennent en 3 clics ou moins**, 6 dépassent (dont 3 où le geste est impossible ou l’information absente dans les maquettes actuelles : P2 après programmation, P9, P10). Voir § 4.
12. Aucun ajout ne touche aux écarts de Will ; aucun ne demande de toucher au dépôt du CRM avant le feu vert.

---

## 2. Liste de contrôle de référence (241 lignes)

### A. Ciblage (listes, étiquettes, import, vérification)

| N° | Fonction | Plan 20 | Maquette | Existant (21) | Verdict | Ajout : lot · jours · priorité | Remarque |
|---|---|---|---|---|---|---|---|
| 1 | Listes fixes | oui (Q1, C1) | oui (Listes) | oui | OK |  | listes manuelles déjà en place |
| 2 | Étiquettes (créer, poser, retirer) | oui (Q1b) | oui (Listes › Étiquettes) | oui | OK |  |  |
| 3 | Listes dynamiques (mises à jour seules) | oui (C1) | oui (Listes) | oui | OK |  | « audiences » existantes |
| 4 | Éditeur des critères d'une liste dynamique (ET / OU / SAUF) | oui (C1) | non (seule la liste est montrée) | oui | **À AJOUTER** | U1 (maquette) puis U2-U9 · 0,5 j · **V0** | l'écran le plus utilisé pour cibler |
| 5 | Lancer une campagne vers une étiquette (sans créer de liste) | partiel (C1 : « ciblage ») | non (étape 1 : listes seulement) | oui (étiquettes) | **À AJOUTER** | C1 + U2-U9 · 0,5 j · **V0** | demande explicite de Will |
| 6 | Exclure des adresses, organisations, domaines | oui (C1) | oui (Nouvelle campagne, étape 1) | partiel | OK |  |  |
| 7 | Exclure d'office les clients et affaires en cours (étape Devis, Gagné) | non | non | non | **À AJOUTER** | C1 · 0,5 j · **V0** | évite d'écrire en froid à un client |
| 8 | Import CSV / Excel avec choix des colonnes | oui (Q1) | oui (Contacts › Importer, 3 étapes) | partiel (import dans une liste) | OK |  |  |
| 9 | Rapport d'import (lignes refusées, doublons, sans provenance) | non | partiel (étape « Contrôle ») | non | **À AJOUTER** | Q1 · 0,5 j · **V0** |  |
| 10 | Gros import en arrière-plan avec barre d'avancement | non | non | partiel (tâches de fond) | **À AJOUTER** | Q1 · 1 j · **V0** | 10 000 lignes sans bloquer l'écran |
| 11 | Provenance obligatoire à l'ajout et à l'import | oui (Q1) | oui (Contacts) | oui | OK |  |  |
| 12 | Export d'une liste ou d'une sélection (CSV) | oui (Q2, V1) | non (aucun bouton sur Contacts ou Listes) | oui (entreprises, personnes) | **À AJOUTER** | U2-U9 (brancher l'existant) · 0,5 j · **V0** | le serveur sait déjà le faire |
| 13 | Enrichissement automatique (SIREN, site, téléphone) | oui (reprise, S7) | oui (Collectes, Outils techniques) | oui | OK |  |  |
| 14 | « Compléter cette fiche » à la demande | non | non | partiel (workflows lancés à la main) | **À AJOUTER** | nouveau lot Q4 · 1 j · **V1** |  |
| 15 | Vérification des adresses (domaine, fournisseur, cascade) | oui (E4) | oui (Listes › Joignables) | partiel (domaine seulement) | OK |  | à étendre, pas réécrire |
| 16 | Revérification avant envoi (adresse vue il y a plus de 30 jours) | oui (E4) | oui (Nouvelle campagne) | non | OK |  |  |
| 17 | Adresses génériques, grand public, « fourre-tout » repérées | oui (C3, E4) | partiel (« Refusées ») | partiel | OK |  |  |
| 18 | Doublons : détection et fusion avec annulation | oui (reprise) | oui (Doublons) | oui | OK |  |  |
| 19 | Doublons vérifiés à la saisie | oui (Q1) | oui (Contacts › Ajouter) | partiel | OK |  |  |
| 20 | Champs personnalisés (texte, liste, date) | oui (K9, V1) | oui (Écrans V1) | non | OK |  |  |
| 21 | Vues sauvegardées (filtres gardés) | oui (Q2, V1) | non | oui (serveur sans écran) | **À AJOUTER** | U2-U9 (brancher l'existant) · 0,5 j · **V0** | le serveur existe déjà : peu coûteux |
| 22 | Score de priorité simple (règles en phrases, sans IA opaque) | non | non | partiel (confiance de l'adresse, signaux) | **À AJOUTER** | nouveau lot Q4 · 3 j · **V1** | « qui appeler en premier ? » |
| 23 | Recherche partout (Ctrl K) et actions rapides | oui (U0) | oui (en-tête) | oui | OK |  |  |
| 24 | Actions de masse avec aperçu et annulation | oui (Q1b) | oui (Contacts) | partiel (serveur sans écran) | OK |  |  |
| 25 | Pression commerciale (1 message / 5 jours, 3 par organisation / 30 jours) | oui (C1) | oui (Règles de prudence) | non | OK |  |  |
| 26 | Base sectorielle attribuée et retirable | oui (K12, V1) | non | non | OK |  | maquette à faire avant U13 |
| 27 | Carte de France des fiches | oui (reprise) | oui (Entreprises, Statistiques) | oui | OK |  |  |

### B. Contenu (messages types, variables, aperçu, test, A/B)

| N° | Fonction | Plan 20 | Maquette | Existant (21) | Verdict | Ajout : lot · jours · priorité | Remarque |
|---|---|---|---|---|---|---|---|
| 28 | Messages types versionnés, jamais supprimés (archivés) | oui (C1) | oui (Messages types) | non | OK |  |  |
| 29 | Validation d'une version avant usage | oui (C1) | oui (Éditeur de message) | non | OK |  |  |
| 30 | Champs à insérer ({prénom}, {entreprise}, {lien_rdv}) | oui (C1, C2) | oui (Éditeur) | non | OK |  |  |
| 31 | Valeur de repli si un champ est vide, et blocage si champ obligatoire manquant | non | non | non | **À AJOUTER** | C1 · 0,5 j · **V0** | évite « Bonjour , » |
| 32 | Aperçu réel pour un destinataire choisi | oui (U2-U9) | oui (Éditeur) | non | OK |  |  |
| 33 | Aperçu sur téléphone | non | non | non | **À AJOUTER** | U2-U9 · 0,5 j · **V1** |  |
| 34 | « M'envoyer un test » (moi, boîtes témoins) | oui (C2) | oui (Éditeur, Nouvelle campagne) | non | OK |  |  |
| 35 | Contrôleur de contenu (mots interdits, liens, bloc art. 14) | oui (C1) | oui (Éditeur › Contrôles) | non | OK |  |  |
| 36 | Score anti-spam du contenu | oui (C5, V1) | non | non | OK |  | maquette à faire avant U13 |
| 37 | Texte simple par défaut (HTML minimal), pièces jointes refusées en froid | non | non | non | **À AJOUTER** | C1 (règle du contrôleur) · 0,5 j · **V0** | règle de délivrabilité à écrire |
| 38 | Versions de l'objet (A/B) | oui (C5, V1) | oui (Éditeur › « Ajouter une version ») | non | OK |  |  |
| 39 | Comparaison de versions du texte, gagnant choisi sur les réponses | oui (C5, V1) | non | non | OK |  | maquette à faire avant U13 |
| 40 | Variantes courtes de phrases (anti-répétition) | non | non | non | **À AJOUTER** | C5 · 2 j · **V2** | variantes lisibles, jamais de texte brouillé |
| 41 | Bibliothèque de blocs réutilisables (signatures, paragraphes, appels à l'action) | non | non | non | **À AJOUTER** | C5 · 2 j · **V1** |  |
| 42 | Signature par boîte | oui (E3) | oui (Boîtes › Ajouter) | non | OK |  |  |
| 43 | Lien de rendez-vous {lien_rdv} | oui (C2) | oui (Identité) | non | OK |  |  |
| 44 | Brouillon de séquence par l'IA | oui (Q1b) | non | partiel (routeur d'IA) | **À AJOUTER** | U12 (maquette) · 0,5 j · **V0** |  |
| 45 | Accroche IA par destinataire, figée avant validation | oui (K10, V1) | non | partiel (routeur d'IA) | OK |  | maquette avant U13 |
| 46 | Page « pourquoi ce message » | oui (C4) | oui (Page de désinscription) | non | OK |  |  |
| 47 | Mesure des ouvertures (pixel) | non (garde « aucun pixel », C2) | non | non | VOLONTAIREMENT ÉCARTÉ (plan, à confirmer) |  | choix du plan : seules les réponses comptent |
| 48 | Suivi des clics (domaine de suivi) | non (décision 41 : non à F21) | non | non | VOLONTAIREMENT ÉCARTÉ (Will) |  | décision de Will du 01/11 |

### C. Campagnes (création, programmation, séquences)

| N° | Fonction | Plan 20 | Maquette | Existant (21) | Verdict | Ajout : lot · jours · priorité | Remarque |
|---|---|---|---|---|---|---|---|
| 49 | Création guidée en 5 étapes | oui (C1, U2-U9) | oui (Nouvelle campagne) | non | OK |  |  |
| 50 | Programmer jour et heure de départ | oui (C1) | oui (étape 3 « Départ ») | non | OK |  |  |
| 51 | Reprogrammer une campagne programmée (changer la date) | non | non | non | **À AJOUTER** | C1 + U2-U9 · 1 j · **V0** |  |
| 52 | Dupliquer une campagne | non | non | non | **À AJOUTER** | C1 + U2-U9 · 1 j · **V0** | repartir d'une campagne qui a marché |
| 53 | Pause et reprise | oui (C1) | oui (Suivi de campagne) | non | OK |  |  |
| 54 | Pause depuis la liste des campagnes (sans ouvrir) | non | non | non | **À AJOUTER** | U2-U9 · 0,25 j · **V0** | voir parcours P7 |
| 55 | Arrêter définitivement (terminer) | non | non | non | **À AJOUTER** | C1 + U2-U9 · 0,5 j · **V0** |  |
| 56 | Ajouter un lot de destinataires à une campagne en cours (nouvelle validation) | non (liste figée) | non | non | **À AJOUTER** | C5 · 1,5 j · **V1** | garde la liste figée : un lot = une validation |
| 57 | Plafond quotidien propre à une campagne | non | non | non | **À AJOUTER** | C1 · 0,5 j · **V1** |  |
| 58 | Jours et heures d'envoi, jours fériés | oui (C1) | oui (Règles de prudence, étape 3) | non | OK |  |  |
| 59 | Fuseau du destinataire (Outre-mer) | non (France, heure de Paris) | non | partiel (fuseau de Paris) | **À AJOUTER** | C1 · 1 j · **V1** | la Réunion = Paris + 3 h |
| 60 | Séquences de 1 à 4 messages, délais en jours ouvrés | oui (C1) | oui (étape 2) | non | OK |  |  |
| 61 | Relance dans le même fil, même boîte | oui (C1) | oui (« même fil ») | non | OK |  |  |
| 62 | Arrêt automatique à la réponse | oui (C1) | oui (Suivi : « arrêtée pour 3 entreprises ») | non | OK |  |  |
| 63 | Arrêt pour toute l'entreprise quand une personne répond | oui (C1) | oui (Fiche entreprise) | non | OK |  |  |
| 64 | Pause sur absence du bureau, reprise au retour | oui (C1) | oui (Suivi) | non | OK |  |  |
| 65 | Arrêt quand un rendez-vous est pris | oui (RP2) | oui (Fiche entreprise) | non | OK |  |  |
| 66 | Étape « tâche manuelle » dans une séquence (appel, visite) | partiel (Q3 : appel) | non | non | **À AJOUTER** | Q3 · 1 j · **V1** | générique, pas seulement le téléphone |
| 67 | Branches conditionnelles dessinées (si… alors…) | non | non | non | VOLONTAIREMENT ÉCARTÉ (Will) |  | pas de constructeur visuel d'automatisations |
| 68 | Répartition sur plusieurs boîtes | oui (C1, E7) | oui (étape 3) | non | OK |  |  |
| 69 | Durée et date de fin estimées | oui (C2) | oui (étape 3, récapitulatif) | non | OK |  |  |
| 70 | 7 contrôles avant lancement | oui (C1, C3) | oui (étape 4) | partiel (gardes de la préparation) | OK |  |  |
| 71 | Validation par code e-mail et 5 min pour annuler | oui (S3, C1) | oui (étape 5) | non | OK |  |  |
| 72 | Brouillon enregistré tout seul | oui (U2-U9) | oui (récapitulatif) | non | OK |  |  |
| 73 | Liste et filtres par statut (en cours, à valider, programmées…) | oui (UI-58) | oui (Campagnes) | non | OK |  |  |
| 74 | Calendrier des envois prévus (toutes campagnes) | non | non | non | **À AJOUTER** | RP4 · 1,5 j · **V1** | voir la semaine d'un coup d'œil |
| 75 | Campagnes récurrentes | oui (C5, V1) | non | non | OK |  |  |
| 76 | Messages déclenchés (formulaire en une phrase) | oui (C5, V1) | oui (Écrans V1) | non | OK |  |  |
| 77 | Envoi unitaire depuis une fiche | oui (C2) | oui (Fiche contact › Écrire) | non | OK |  |  |
| 78 | Déclarer un envoi fait à la main | oui (C2) | oui (Fiche contact) | partiel (commande retours) | OK |  |  |
| 79 | Campagne e-mail + appel | oui (Q3, V1) | non | non | OK |  |  |
| 80 | Première campagne d'un client validée par Axion | oui (décision 34) | non | non | OK |  | à mettre dans K3 |

### D. Envoi et délivrabilité (domaines, boîtes, IP, chauffe)

| N° | Fonction | Plan 20 | Maquette | Existant (21) | Verdict | Ajout : lot · jours · priorité | Remarque |
|---|---|---|---|---|---|---|---|
| 81 | Registre des domaines d'envoi | oui (E3) | oui (Domaines) | non | OK |  |  |
| 82 | Assistant DNS SPF, DKIM, DMARC, PTR avec vérification | oui (E3) | oui (Domaines › Ajouter) | non | OK |  |  |
| 83 | Contrôle DNS quotidien et alerte si une ligne disparaît | oui (§ 9 point 7, E3) | partiel | non | OK |  |  |
| 84 | DMARC progressif (none → quarantine → reject) avec rappel de date | oui (R5) | non | non | **À AJOUTER** | U12 (pastille sur Domaines) · 0,5 j · **V0** |  |
| 85 | Rapports DMARC : « qui envoie en votre nom ? » | oui (E8, U12) | oui (Domaines) | non | OK |  |  |
| 86 | MTA-STS et rapports TLS sur les domaines | non | non | non | **À AJOUTER** | E9 · 0,5 j · **V1** |  |
| 87 | Fiche d'un domaine (historique 30 jours : volume, refus, plaintes) | partiel (RP3) | non (aucun bouton Ouvrir) | non | **À AJOUTER** | U2-U9 · 1 j · **V0** | voir parcours P4 |
| 88 | Expiration des domaines | oui (E9, V1) | oui (Domaines : « Expire le ») | non | OK |  |  |
| 89 | Garde anti-dispersion (2 domaines par IP, 1 ressource / 15 jours) | oui (E3) | oui (Domaines, Règles) | non | OK |  |  |
| 90 | Registre des boîtes, ajout avec test de connexion | oui (E3, U11) | oui (Boîtes) | non | OK |  |  |
| 91 | Fiche d'une boîte (envois, refus, réponses, chauffe) | partiel (RP3 : par expéditeur) | non (« Ouvrir » mène à la chauffe) | non | **À AJOUTER** | U2-U9 · 1 j · **V0** | voir parcours P9 |
| 92 | Plafond par boîte (150 / jour) | oui (E3) | oui (Boîtes) | non | OK |  |  |
| 93 | Registre des adresses IP et nom inverse | oui (E3) | oui (Serveurs › Adresses IP) | non | OK |  |  |
| 94 | Formulaire « Ajouter une adresse IP » avec application immédiate | oui (U11) | partiel (bouton sans fenêtre) | non | **À AJOUTER** | U1 (maquette) + U11 · 0,5 j · **V0** | voir parcours P5 |
| 95 | Chauffe des IP par paliers | oui (E7) | oui (Serveurs : « Palier 3 sur 5 ») | non | OK |  |  |
| 96 | Chauffe par boîte en jours effectifs, recul d'un palier | oui (E7) | oui (Montée en douceur) | non | OK |  |  |
| 97 | Réseau d'échange de faux messages pour « chauffer » | non | non | non (ébauche jamais utilisée) | VOLONTAIREMENT ÉCARTÉ (plan, à confirmer) |  | contraire aux règles des messageries |
| 98 | Rythme par messagerie destinataire (Gmail, Orange, Microsoft) | partiel (E2 : contre-pression) | non | non | **À AJOUTER** | E2 + Santé · 1 j · **V0** | réglé dans KumoMTA, visible dans Santé |
| 99 | Flux séparés (prospection, lettre, codes) par IP ou domaine | partiel (S2 pour les codes) | non | non | **À AJOUTER** | E9 + C6 · 1 j · **V1** | la lettre ne doit pas abîmer la prospection |
| 100 | Réputation Gmail Postmaster et Microsoft SNDS affichée | partiel (E8 inscription, E9 statut) | non | non | **À AJOUTER** | E9 + U13 · 1 j · **V1** |  |
| 101 | Surveillance des listes noires | oui (E8) | oui (Domaines, Serveurs) | oui (tâche horaire) | OK |  | éviter le doublon avec l'existant |
| 102 | Que faire si listé : fiche par liste noire, lien de demande de retrait | non | non | non | **À AJOUTER** | E8 · 0,5 j · **V0** |  |
| 103 | Rebonds durs et mous classés | oui (E5) | partiel (« Refusées ») | partiel (commande retours) | OK |  |  |
| 104 | Raison du refus en français (code serveur traduit) | non | non | non | **À AJOUTER** | E5 + U2-U9 · 1 j · **V0** |  |
| 105 | Plaintes toutes sources (réponse hostile, abuse@, postmaster@) | oui (E5) | oui (Désinscriptions › Plaintes) | partiel | OK |  |  |
| 106 | Boucles de retour Microsoft (JMRP) et Yahoo | partiel (E8 : Signal Spam seulement) | non | non | **À AJOUTER** | E8 · 0,5 j · **V0** | inscription à faire au premier envoi |
| 107 | Test du matin (boîtes témoins : boîte de réception ou indésirables) | oui (E8) | oui (Santé, Serveurs) | non | OK |  |  |
| 108 | Disjoncteurs (ralentir, arrêter une boîte) | oui (E7) | oui (Règles de prudence, Alertes) | non | OK |  |  |
| 109 | « Tout arrêter » en 2 clics | oui (E7, P5) | oui (en-tête) | non | OK |  |  |
| 110 | Arrêt par client | oui (P5) | partiel | non | OK |  |  |
| 111 | Frein humain (15 réponses en attente) | oui (E7) | oui (Règles de prudence) | non | OK |  |  |
| 112 | Mode absence (je pars une semaine) | oui (E7) | non | non | **À AJOUTER** | U11 (maquette) · 0,25 j · **V0** |  |
| 113 | File d'attente visible | oui (E2, V1 files) | oui (Serveurs) | non | OK |  |  |
| 114 | Configuration depuis l'écran, versionnée, retour automatique | oui (E3b) | oui (Configuration technique) | non | OK |  |  |
| 115 | Ajout d'un serveur par empreinte | oui (U13) | oui (Serveurs) | non | OK |  |  |
| 116 | Santé du serveur (disque, mémoire, service, liaison) | oui (E2) | oui (Serveurs) | partiel (observabilité) | OK |  |  |
| 117 | Désinscription en un clic dans l'en-tête (RFC 8058) | oui (E6) | oui (Page publique) | non | OK |  |  |
| 118 | Adresse de retour par message (VERP) | oui (E5) | non (technique) | non | OK |  |  |
| 119 | Repli Postfix + rspamd | oui (E10, V2 ; avancé en V0 b proposé) | non | non | OK |  |  |
| 120 | Relais tiers de secours | oui (F20) | non | non | OK |  |  |
| 121 | Plusieurs serveurs, 5 000 / jour | oui (X1, V2) | non | non | OK |  |  |
| 122 | Logo dans les messageries (BIMI) | non | non | non | VOLONTAIREMENT ÉCARTÉ (plan, à confirmer) |  | exige DMARC reject et une marque déposée |

### E. Réponses et boîte commune

| N° | Fonction | Plan 20 | Maquette | Existant (21) | Verdict | Ajout : lot · jours · priorité | Remarque |
|---|---|---|---|---|---|---|---|
| 123 | Relève de toutes les boîtes (IMAP) | oui (E5) | oui (Règles › Automatismes) | non | OK |  |  |
| 124 | Boîte commune de toutes les réponses | oui (RP1) | oui (Réponses) | non | OK |  |  |
| 125 | Classement automatique (intéressé, plus tard, absent, STOP…) | oui (RP1) | oui (Réponses) | non | OK |  |  |
| 126 | Rattachement à la fiche, et file « à rattacher » | oui (RP1, U11) | oui (Réponses à rattacher) | non | OK |  |  |
| 127 | Suggestion appliquée en un geste (tâche, étape, arrêt) | oui (RP1) | oui (Réponses) | non | OK |  |  |
| 128 | STOP confirmé → opposition partout | oui (RP1, E5) | oui (Réponses) | partiel (commande retours) | OK |  |  |
| 129 | « Transmis à un collègue » → nouvelle personne | oui (U11) | oui (Réponses à rattacher › Créer) | non | OK |  |  |
| 130 | Répondre depuis le CRM (même fil, même boîte) | oui (RP4, V1) | non | non | **À AJOUTER** | RP4 avancé en V0 b + maquette · 4 j · **V0** | sinon Will jongle entre 2 outils |
| 131 | Réponses rapides enregistrées | non | non | non | **À AJOUTER** | RP4 · 1 j · **V1** |  |
| 132 | Attribuer une réponse à un collègue | partiel (K10 : propriétaire) | non | non | **À AJOUTER** | RP4 · 0,5 j · **V1** |  |
| 133 | Alerte « réponse en attente depuis 24 h » | oui (RP4) | oui (Réglages des alertes) | non | OK |  |  |
| 134 | Avis immédiat « intéressé » regroupé, sans nom | oui (RP1) | oui (Réglages des alertes) | non | OK |  |  |
| 135 | Raccourcis clavier pour trier (J, K, 1, 2, 3, S) | oui (U2-U9) | oui (Réponses) | non | OK |  |  |

### F. CRM (fiches, affaires, tâches, historique)

| N° | Fonction | Plan 20 | Maquette | Existant (21) | Verdict | Ajout : lot · jours · priorité | Remarque |
|---|---|---|---|---|---|---|---|
| 136 | Fiche contact complète (étape, historique, droit d'écrire) | oui (Q1) | oui (Fiche contact) | partiel (fiche personne) | OK |  |  |
| 137 | Fiche entreprise (personnes, affaire, historique) | oui (U2-U9) | oui (Fiche entreprise) | oui | OK |  |  |
| 138 | Modifier et retirer (corbeille restaurable) | oui (Q1) | oui (Fiche contact › Autres actions) | oui (serveur sans écran) | OK |  |  |
| 139 | Étapes de Will (à contacter → gagné / perdu) | oui (Q1b) | oui (Fiche, Affaires) | non | OK |  |  |
| 140 | Affaires en colonnes, déplacement au clavier | oui (Q2, V1) | oui (Affaires) | partiel (table d'ébauche) | OK |  |  |
| 141 | Affaire : date de signature prévue et chance de réussite | non | non (montant seulement) | non | **À AJOUTER** | Q2 · 0,5 j · **V1** | prévoir le chiffre du mois |
| 142 | Raison de perte (liste courte) | non | non | non | **À AJOUTER** | Q2 · 0,5 j · **V1** | apprendre de ce qui rate |
| 143 | Mes tâches (jour, en retard, semaine) | oui (Q1b) | oui (Tâches) | partiel (tâches par fiche) | OK |  |  |
| 144 | Tâches créées par les réponses | oui (Q1b) | oui (Tâches) | non | OK |  |  |
| 145 | Rappel du matin par e-mail | oui (Q1b) | oui (Tâches) | non | OK |  |  |
| 146 | Notes | oui (Q2) | oui (Fiche contact) | partiel (activités) | OK |  |  |
| 147 | Noter un appel | oui (Q2, Q3) | oui (Fiche contact) | partiel (activités) | OK |  |  |
| 148 | Historique complet (messages, réponses, notes, RDV) | oui (Q2) | oui (Fiches) | oui (chronologie) | OK |  |  |
| 149 | Rappel planifié sur une fiche | oui (Q1b) | oui (Fiche contact) | partiel | OK |  |  |
| 150 | Rendez-vous par lien externe + bouton « RDV pris » | oui (RP2, RP4) | oui (Fiche entreprise) | non | OK |  |  |
| 151 | Agenda par client dans le CRM | non | non | non | VOLONTAIREMENT ÉCARTÉ (Will) |  | décision de Will |
| 152 | Devis et factures | non (Hub de la console) | non | non | VOLONTAIREMENT ÉCARTÉ (Will) |  | décision 35 : facturation dans le Hub |
| 153 | Documents joints à une fiche (devis PDF, compte rendu) | non | non | partiel (presse seulement) | **À AJOUTER** | Q2 · 1,5 j · **V1** |  |
| 154 | Propriétaire d'une fiche, transfert | oui (K10, K1) | oui (« Responsable ») | non | OK |  |  |
| 155 | Liens entre entreprises (groupe, filiale) | non (reprise) | non | oui | **À AJOUTER** | U2-U9 (afficher l'existant) · 0,5 j · **V1** |  |
| 156 | Propositions venues du site à valider | oui (reprise) | oui (À valider) | oui | OK |  |  |
| 157 | Fédérations, événements, réseaux | oui (reprise) | oui (Réseaux) | oui | OK |  |  |
| 158 | Presse (médias, journalistes, communiqués) | oui (reprise, C5) | oui (Presse) | oui | OK |  |  |
| 159 | Téléphone : file d'appels, script, issues | oui (Q3, V1) | non | non | OK |  | maquette avant Q3 |

### G. Conformité

| N° | Fonction | Plan 20 | Maquette | Existant (21) | Verdict | Ajout : lot · jours · priorité | Remarque |
|---|---|---|---|---|---|---|---|
| 160 | Page de désinscription en un clic, option « toute mon organisation » | oui (E6) | oui (Page publique) | non | OK |  |  |
| 161 | Page gardée 3 ans après la fin d'un domaine | oui (E6, décision 33) | non | non | OK |  |  |
| 162 | STOP élargi (non merci, retirez-moi…) | oui (C3) | oui (Réponses) | non | OK |  |  |
| 163 | « Puis-je écrire à… ? » | oui (U2-U9) | oui (Désinscriptions, Ctrl K) | partiel (règle d'éligibilité) | OK |  |  |
| 164 | Liste « ne plus écrire » (empreinte, jamais retirée) | oui (P2) | oui (Désinscriptions) | oui (opt_out, suppressions) | OK |  |  |
| 165 | Export du registre des oppositions (preuve) | non | non | partiel (export RGPD) | **À AJOUTER** | U12 · 0,5 j · **V0** | à montrer en cas de contrôle |
| 166 | Bloc d'information art. 14 et date de premier message | oui (J1) | oui (Identité, Fiche contact) | partiel (date posée) | OK |  |  |
| 167 | Alerte J+21 et refus J+30 (art. 14) | oui (J1) | non | non | OK |  | à rendre visible dans Aujourd'hui |
| 168 | Demandes RGPD avec délai restant | oui (U11) | oui (Demandes RGPD) | oui | OK |  |  |
| 169 | Export RGPD d'une personne | oui (S7) | oui (Demandes RGPD) | oui | OK |  |  |
| 170 | Effacement avec empreinte d'opposition gardée | oui (J3) | oui (Demandes RGPD) | oui | OK |  |  |
| 171 | Registre des traitements, sous-traitants | oui (J2, J4) | oui (Demandes RGPD, V1) | non | OK |  |  |
| 172 | Registre de l'IA | oui (reprise) | oui (Demandes RGPD) | oui | OK |  |  |
| 173 | Garde Sirene « non diffusible », entreprises fermées | oui (C3) | oui (Collectes) | oui | OK |  |  |
| 174 | France seulement, webmail refusé en froid | oui (C3) | oui (Réseaux) | partiel | OK |  |  |
| 175 | 3 ans sans échange : alerte, sans suppression | oui (J4) | non | non | OK |  |  |
| 176 | Journal d'audit inaltérable, sans e-mail en clair | oui (S7, S11) | oui (Journal) | oui | OK |  |  |
| 177 | Opposition par téléphone | oui (Q3) | non | non | OK |  |  |

### H. Suivi et statistiques

| N° | Fonction | Plan 20 | Maquette | Existant (21) | Verdict | Ajout : lot · jours · priorité | Remarque |
|---|---|---|---|---|---|---|---|
| 178 | Suivi d'une campagne (progression, ce qui se passe) | oui (RP3) | oui (Suivi de campagne) | non | OK |  |  |
| 179 | Résultats par message de la séquence | oui (RP3) | oui (Suivi de campagne) | non | OK |  |  |
| 180 | État de chaque destinataire (en file, parti, refusé, répondu) | partiel (RP3) | non (« Voir la liste figée » sans écran) | non | **À AJOUTER** | RP3 + U2-U9 · 1 j · **V0** | « où en est Paul Martin ? » |
| 181 | Résultats par boîte, par domaine, par liste | oui (RP3) | non (par campagne seulement) | non | **À AJOUTER** | U2-U9 (onglets Statistiques) · 1 j · **V0** |  |
| 182 | Résultats par message type (toutes campagnes, par version) | non | non | non | **À AJOUTER** | RP3 · 0,5 j · **V1** |  |
| 183 | Entonnoir (envoyés → réponses → RDV → gagnés) | oui (RP4) | oui (Statistiques) | non | OK |  |  |
| 184 | Comparaison avec la période d'avant, objectif | oui (RP3) | oui (Statistiques) | non | OK |  |  |
| 185 | Rapport du matin par e-mail | oui (S9, Q1b) | oui (Règles › Automatismes) | non | OK |  |  |
| 186 | Rapports hebdomadaires planifiés | oui (RP4, V1) | oui (Statistiques › Rapports) | non | OK |  |  |
| 187 | Export des chiffres (CSV, PDF) | oui (RP4) | oui (Statistiques) | partiel | OK |  |  |
| 188 | Chercher un envoi : une adresse → tous ses messages et codes serveur | non | non | non | **À AJOUTER** | E5 + U12 · 1 j · **V0** | le journal de bord de PowerMTA |
| 189 | Tableau « Aujourd'hui » | oui (U2-U9) | oui (Aujourd'hui) | partiel (tableau de bord) | OK |  |  |
| 190 | Coûts visibles (vérification, serveur) | oui (RP4, E4) | partiel (Listes) | non | OK |  |  |
| 191 | Chiffre d'affaires attribué aux campagnes | oui (X1, V2) | non | non | OK |  |  |
| 192 | Suivi des tâches de fond (dernier passage, échec) | oui (S9) | oui (Règles › Automatismes) | oui (battement) | OK |  |  |
| 193 | Mesure de la vérification des adresses (résultats, coût) | oui (E4) | oui (Listes › Joignables) | partiel | OK |  |  |

### I. Équipe, droits, sécurité

| N° | Fonction | Plan 20 | Maquette | Existant (21) | Verdict | Ajout : lot · jours · priorité | Remarque |
|---|---|---|---|---|---|---|---|
| 194 | Rôles (propriétaire, envois, commercial, lecteur) | oui (S6, K1) | oui (Équipe) | oui | OK |  |  |
| 195 | Inviter, désactiver (jamais supprimer) | oui (K1) | oui (Équipe) | oui | OK |  |  |
| 196 | Code par e-mail (2FA), codes de secours | oui (S3) | oui (Connexion, Compte) | partiel (TOTP) | OK |  |  |
| 197 | Appareils de confiance 30 jours, retrait à distance | oui (S3) | oui (Compte) | non | OK |  |  |
| 198 | Code redemandé pour les gestes sensibles | oui (S3) | oui (étape 5, Journal) | non | OK |  |  |
| 199 | Journal des connexions | oui (S7) | oui (Journal › Accès) | oui | OK |  |  |
| 200 | Accès du support limité et tracé | oui (K1, V1) | oui (Écrans V1) | non | OK |  |  |
| 201 | Isolation entre clients (RLS) | oui (S7) | non (invisible) | partiel (drapeau) | OK |  |  |
| 202 | Connexion par compte Google ou Microsoft | non | non | non | **À AJOUTER** | K1 · 2 j · **V2** | confort, pas urgent |

### J. Alertes

| N° | Fonction | Plan 20 | Maquette | Existant (21) | Verdict | Ajout : lot · jours · priorité | Remarque |
|---|---|---|---|---|---|---|---|
| 203 | Centre d'alertes (en cours, résolues) | oui (U11) | oui (Alertes) | partiel (notifications) | OK |  |  |
| 204 | « Ce que le système a fait » et « que faire » | oui (U11) | oui (Alertes) | non | OK |  |  |
| 205 | Réglage type × canal (console, e-mail) | oui (U11) | oui (Alertes et avis) | non | OK |  |  |
| 206 | Alerte de test | oui (S9) | oui (Alertes et avis) | non | OK |  |  |
| 207 | Seconde adresse hors domaine Axion | oui (S9) | oui (Alertes et avis) | non | OK |  |  |
| 208 | Battement externe (le CRM se tait → e-mail) | oui (S9) | non (invisible) | partiel (battement interne) | OK |  |  |
| 209 | Regroupement anti-bruit (15 min) | oui (U11) | oui (Alertes et avis) | non | OK |  |  |
| 210 | Alertes par SMS, téléphone ou Telegram | non | non | partiel (ancien Telegram) | VOLONTAIREMENT ÉCARTÉ (Will) |  | décision de Will : console + e-mail |

### K. Sauvegardes et administration

| N° | Fonction | Plan 20 | Maquette | Existant (21) | Verdict | Ajout : lot · jours · priorité | Remarque |
|---|---|---|---|---|---|---|---|
| 211 | Sauvegarde quotidienne et copie hors site | oui (S9) | oui (Sauvegardes) | partiel (surveillance) | OK |  |  |
| 212 | Restauration testée et chronométrée | oui (S9) | oui (Sauvegardes) | non | OK |  |  |
| 213 | Restauration d'un seul client | oui (K5, V1) | non | non | OK |  |  |
| 214 | Réglages rangés par groupes | oui (U0) | oui (Réglages) | partiel | OK |  |  |
| 215 | Identité de l'expéditeur | oui (U11) | oui (Identité) | non | OK |  |  |
| 216 | Règles de prudence en phrases (durcir seulement en V0) | oui (U11) | oui (Règles de prudence) | non | OK |  |  |
| 217 | Mise en route en 5 jalons | oui (U12) | oui (Mise en route) | non | OK |  |  |
| 218 | Écran « Feu vert » (15 critères avant le premier envoi) | oui (T1) | non | non | **À AJOUTER** | U1 (maquette) + T1 · 0,5 j · **V0** | écran clé du lancement |
| 219 | Clients (console), création en 3 étapes | oui (K3, V1) | oui (Écrans V1) | non | OK |  |  |
| 220 | Usage et état d'abonnement | oui (K6, K7) | oui (Écrans V1) | non | OK |  |  |
| 221 | Mises à jour par vagues, retour arrière | oui (K4) | oui (Écrans V1) | non | OK |  |  |
| 222 | Collectes de données (ex-« campagnes ») | oui (§ 11 point 5) | oui (Collectes) | oui | OK |  |  |
| 223 | Aide intégrée et mode d'emploi | oui (Q1, U13) | partiel (bouton « ? ») | non | OK |  |  |
| 224 | Marque blanche | non | non | non | VOLONTAIREMENT ÉCARTÉ (Will) |  | décision de Will |
| 225 | Catalogue de modèles pour les clients | non | non | non | VOLONTAIREMENT ÉCARTÉ (Will) |  | décision de Will (K2 = réglages seulement) |
| 226 | Connecteur systeme.io | non | non | non | VOLONTAIREMENT ÉCARTÉ (Will) |  | décision de Will : jamais |
| 227 | Mode sombre | non | non | non | VOLONTAIREMENT ÉCARTÉ (Will) |  | décision de Will : clair seulement |

### L. API, webhooks, performance, accessibilité

| N° | Fonction | Plan 20 | Maquette | Existant (21) | Verdict | Ajout : lot · jours · priorité | Remarque |
|---|---|---|---|---|---|---|---|
| 228 | API par espace, clés révocables à portée limitée | oui (K9, V1) | oui (Écrans V1) | partiel (jetons de connexion) | OK |  |  |
| 229 | Documentation d'API fermée au public | oui (S11) | non | partiel | OK |  |  |
| 230 | Contrat d'API entre écrans et serveur (test en CI) | oui (U0, § 11) | non (invisible) | non | OK |  |  |
| 231 | Webhooks entrants signés (site, partenaires) | oui (P4) | oui (Écrans V1 : synchro) | oui | OK |  |  |
| 232 | Webhooks sortants signés (réponse, RDV, opposition) | oui (X3, V2) | non | non | **À AJOUTER** | X3 avancé en V1 · 0 j · **V1** | même lot, 3 j déjà comptés : avancer |
| 233 | Serveur MCP | non | non | non | VOLONTAIREMENT ÉCARTÉ (Will) |  | décision de Will |
| 234 | Limiteur de requêtes | oui (S1) | non (invisible) | oui | OK |  |  |
| 235 | Budget de vitesse : liste de 50 000 fiches < 1 s, test de charge en CI | non | non | partiel (tests de charge) | **À AJOUTER** | nouveau lot R1 · 2 j · **V0** | la base grossit vite (collectes) |
| 236 | Envoi : contre-pression, reprises, pas de double envoi | oui (E2, plan 26) | non (invisible) | non | OK |  |  |
| 237 | Clavier seul, lecteur d'écran, WCAG 2.2 AA | oui (U10) | oui (contrôle axe : 0 erreur) | oui (CI a11y) | OK |  |  |
| 238 | Téléphone 360 px | oui (U10) | oui (contrôle 360 px) | partiel | OK |  |  |
| 239 | États vide, erreur, chargement sur chaque écran | oui (U0) | oui (toutes les pages) | partiel | OK |  |  |
| 240 | Annuler après un geste réversible | oui (U0) | oui (petit message « Annuler ») | non | OK |  |  |
| 241 | Raccourcis clavier (G puis A, R, C…) | oui (U0) | oui (Compte) | non | OK |  |  |

---

## 3. Les ajouts, rangés par lot

Les lots existants grossissent un peu ; un seul nouveau petit lot est proposé (**Q4** « fiches enrichies et priorité », V1) et un petit lot **R1** « vitesse » (V0), à coller au filet R0.

| Lot proposé | Lignes | Jours | Priorité |
|---|---|---|---|
| C1 | 7, 31, 57, 59 | 2,5 | V0, V1 |
| C1 (règle du contrôleur) | 37 | 0,5 | V0 |
| C1 + U2-U9 | 5, 51, 52, 55 | 3 | V0 |
| C5 | 40, 41, 56 | 5,5 | V1, V2 |
| E2 + Santé | 98 | 1 | V0 |
| E5 + U12 | 188 | 1 | V0 |
| E5 + U2-U9 | 104 | 1 | V0 |
| E8 | 102, 106 | 1 | V0 |
| E9 | 86 | 0,5 | V1 |
| E9 + C6 | 99 | 1 | V1 |
| E9 + U13 | 100 | 1 | V1 |
| K1 | 202 | 2 | V2 |
| Q1 | 9, 10 | 1,5 | V0 |
| Q2 | 141, 142, 153 | 2,5 | V1 |
| Q3 | 66 | 1 | V1 |
| RP3 | 182 | 0,5 | V1 |
| RP3 + U2-U9 | 180 | 1 | V0 |
| RP4 | 74, 131, 132 | 3 | V1 |
| RP4 avancé en V0 b + maquette | 130 | 4 | V0 |
| U1 (maquette) + T1 | 218 | 0,5 | V0 |
| U1 (maquette) + U11 | 94 | 0,5 | V0 |
| U1 (maquette) puis U2-U9 | 4 | 0,5 | V0 |
| U11 (maquette) | 112 | 0,25 | V0 |
| U12 | 165 | 0,5 | V0 |
| U12 (maquette) | 44 | 0,5 | V0 |
| U12 (pastille sur Domaines) | 84 | 0,5 | V0 |
| U2-U9 | 33, 54, 87, 91 | 2,75 | V0, V1 |
| U2-U9 (afficher l'existant) | 155 | 0,5 | V1 |
| U2-U9 (brancher l'existant) | 12, 21 | 1 | V0 |
| U2-U9 (onglets Statistiques) | 181 | 1 | V0 |
| X3 avancé en V1 | 232 | 0 | V1 |
| nouveau lot Q4 | 14, 22 | 4 | V1 |
| nouveau lot R1 | 235 | 2 | V0 |

**Effet sur le total du plan 20** : V0 + 24,5 j, V1 + 19,5 j, V2 + 4 j. Le X3 (webhooks sortants, 3 j) change seulement de phase (V2 → V1) : il est compté à 0 ici et déplacé.

**Effet sur la date du premier envoi** : sur les 24,5 j de V0, ≈ 8 j (fiches domaine et boîte, répondre depuis le CRM, état par destinataire, résultats par boîte) peuvent aller en V0 « b », après le premier envoi. Restent ≈ 16,5 j avant le premier envoi : avec 6 à 8 routines en parallèle, **2 à 3 jours de calendrier**.

---

## 4. Test de simplicité : 10 parcours sans friction

**Comment on compte.** Départ depuis « Aujourd'hui » (`maquettes/index.html`), groupe du menu déjà ouvert. Un clic = un clic ou une touche qui fait avancer ; la saisie de texte ne compte pas. Compté en lisant les maquettes du 01/11 (pages et fenêtres). Seuil demandé : **3 clics**.

| # | Parcours | Chemin dans les maquettes actuelles | Clics | Verdict | Correction proposée (clics après) |
|---|---|---|---|---|---|
| P1 | Lancer une campagne vers une étiquette | Impossible directement : l'étape 1 ne propose que des listes. Détour : Listes › Créer une liste (dynamique sur l'étiquette) › enregistrer, puis Nouvelle campagne › liste › Continuer › message › Continuer › Continuer › Continuer › code › Valider | ≈ 13 | **DÉPASSE** (impossible sans détour) | Bouton « Campagne vers cette étiquette » sur l'étiquette, cible pré-remplie (ligne 5) : 1 clic pour ouvrir, puis 5 étapes ≈ 7 clics. Une campagne reste un geste en 5 étapes : c'est voulu (sécurité), mais 1 clic pour **démarrer**. |
| P2 | La programmer demain à 9 h | Dans l'étape 3 : champ « Départ » › choisir demain › 09:00 (≈ 3 clics de plus). Pour une campagne **déjà programmée** : aucun bouton « Changer la date » | +3 (création) ; impossible (après) | **DÉPASSE** pour une campagne déjà programmée | Bouton « Changer la date » sur le suivi et dans la liste (ligne 51) : 3 clics (Campagnes › Changer la date › Demain 9 h). |
| P3 | Voir le suivi d'une campagne | Campagnes › Ouvrir | 2 | OK | Ajouter la campagne en cours sur « Aujourd'hui » : 1 clic. |
| P4 | Voir qu'un domaine chauffe mal | Santé des envois (feux par domaine visibles) ; le détail : « Voir ce qui s'est passé » | 1 à 2 | OK pour **voir** ; l'**historique** du domaine n'existe pas | Fiche d'un domaine (ligne 87) : Santé › clic sur le feu = 2 clics, avec 30 jours d'historique. |
| P5 | Ajouter une adresse IP | Serveurs › onglet Adresses IP › Ajouter une adresse IP (fenêtre absente des maquettes) › Valider › puis Configuration technique › Appliquer la version | ≈ 6 | **DÉPASSE** | Fenêtre d'ajout avec « Ajouter et appliquer » (ligne 94) + action dans Ctrl K : 3 clics (Ctrl K › Ajouter une IP › Ajouter et appliquer). |
| P6 | Traiter une réponse intéressée | Traiter les réponses › Appliquer la suggestion | 2 | OK | — |
| P7 | Mettre une campagne en pause | Campagnes › Ouvrir › Mettre en pause › confirmer | 4 | **DÉPASSE** | Bouton « Pause » dans la ligne de la liste (ligne 54) : 3 clics (Campagnes › Pause › confirmer). |
| P8 | Savoir si on peut écrire à une adresse | Ctrl K › « Puis-je écrire à… ? » › Vérifier | 2 | OK | — |
| P9 | Voir les résultats d'une boîte d'envoi | Boîtes › Ouvrir… mène à la page de chauffe : envois, refus et réponses de la boîte introuvables | impossible | **DÉPASSE** (manque) | Fiche d'une boîte (ligne 91) : Boîtes › Ouvrir = 2 clics. |
| P10 | Retrouver ce qui est arrivé au message envoyé à une personne | Contacts › chercher › Ouvrir › Historique : on voit « envoyé », pas « accepté / refusé et pourquoi » | 3, réponse incomplète | **DÉPASSE** (information absente) | État par destinataire + « Chercher un envoi » (lignes 180 et 188) : Ctrl K › adresse = 2 clics. |

**Bilan du test.** 4 parcours sur 10 tiennent en 3 clics ou moins (P3, P4, P6, P8). 6 dépassent : P1, P2, P5, P7, P9, P10. Après les corrections proposées, **les 10 tiennent en 3 clics** pour démarrer le geste (la création d'une campagne garde ses 5 étapes de sécurité, voulues).

**Autres parcours vérifiés, sans problème** : Tout arrêter (2 clics) ; enregistrer un STOP depuis « Aujourd'hui » (3) ; ajouter une boîte (3) ; voir les tâches du jour (1) ; envoyer une alerte de test (2).

---

## 5. Tableau final

| Verdict | Lignes |
|---|---|
| OK | 176 |
| À AJOUTER | 52 (≈ 48 j : V0 24,5, V1 19,5, V2 4) |
| VOLONTAIREMENT ÉCARTÉ | 13 (Will : 10 ; plan, à confirmer : 3) |
| **Total** | **241** |

**Les 3 écarts du plan à faire confirmer par Will** : pas de mesure des ouvertures (seules les réponses comptent) ; pas de réseau d'échange de faux messages pour chauffer ; pas de logo dans les messageries (BIMI).

### Les 15 ajouts les plus importants

| Rang | N° | Ajout | Pourquoi c'est important | Lot | Jours | Priorité |
|---|---|---|---|---|---|---|
| 1 | 5 | Lancer une campagne vers une étiquette (sans créer de liste) | demande directe de Will ; geste le plus fréquent | C1 + U2-U9 | 0,5 | V0 |
| 2 | 87 | Fiche d'un domaine (historique 30 jours : volume, refus, plaintes) | voir **pourquoi** un domaine chauffe mal, pas seulement qu'il va mal | U2-U9 | 1 | V0 |
| 3 | 91 | Fiche d'une boîte (envois, refus, réponses, chauffe) | suivre chaque expéditeur ; aujourd'hui « Ouvrir » ne mène nulle part d'utile | U2-U9 | 1 | V0 |
| 4 | 180 | État de chaque destinataire (en file, parti, refusé, répondu) | répondre à « où en est cette personne ? » sans chercher | RP3 + U2-U9 | 1 | V0 |
| 5 | 181 | Résultats par boîte, par domaine, par liste | comparer boîtes, domaines et listes : le cœur du pilotage | U2-U9 (onglets Statistiques) | 1 | V0 |
| 6 | 130 | Répondre depuis le CRM (même fil, même boîte) | un seul outil pour lire et répondre | RP4 avancé en V0 b + maquette | 4 | V0 |
| 7 | 51 | Reprogrammer une campagne programmée (changer la date) | corriger une date sans tout refaire | C1 + U2-U9 | 1 | V0 |
| 8 | 52 | Dupliquer une campagne | relancer vite une campagne qui a marché | C1 + U2-U9 | 1 | V0 |
| 9 | 54 | Pause depuis la liste des campagnes (sans ouvrir) | geste d'urgence à 3 clics au lieu de 4 | U2-U9 | 0,25 | V0 |
| 10 | 55 | Arrêter définitivement (terminer) | fermer proprement une campagne | C1 + U2-U9 | 0,5 | V0 |
| 11 | 94 | Formulaire « Ajouter une adresse IP » avec application immédiate | parcours P5 : ajouter une IP en 3 clics, appliquée tout de suite | U1 (maquette) + U11 | 0,5 | V0 |
| 12 | 188 | Chercher un envoi : une adresse → tous ses messages et codes serveur | retrouver un message précis et la raison d'un refus | E5 + U12 | 1 | V0 |
| 13 | 4 | Éditeur des critères d'une liste dynamique (ET / OU / SAUF) | voir et corriger ce que contient une liste dynamique | U1 (maquette) puis U2-U9 | 0,5 | V0 |
| 14 | 12 | Export d'une liste ou d'une sélection (CSV) | le serveur sait déjà exporter : il manque juste le bouton | U2-U9 (brancher l'existant) | 0,5 | V0 |
| 15 | 165 | Export du registre des oppositions (preuve) | preuve à fournir en cas de contrôle de la CNIL | U12 | 0,5 | V0 |

Total des 15 : ≈ 14,25 j-agent.

---

## 6. Limites honnêtes

- Clics comptés **en lisant** les maquettes, sans chronomètre ni test avec Will (le test de 45 min reste à faire).
- La colonne « Existant » s'appuie sur le relevé 21 et une lecture rapide des contrôleurs : « partiel » veut dire « une partie existe », pas « marche en production ».
- La liste de référence vient de la connaissance générale des outils cités, **pas** d'une relecture de leur documentation du jour.
- Efforts à ± 30 %, comme le plan 20 ; ils ne sont **pas encore** reportés dans le total du plan 20 (à faire par une décision de Will).

