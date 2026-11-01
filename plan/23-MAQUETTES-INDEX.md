# 23 : Index des maquettes (lots U0 + U1) : 01/11/2026

**But.** Montrer TOUTES les pages et la barre latérale avant tout codage d’écran (plan 20, lot U1). Ouvrir `maquettes/index.html` dans un navigateur (mode d’emploi : `maquettes/LISEZ-MOI.md`).

**Sources.** Pages existantes : `frontend/src/app/routeTree.tsx` et `components/layout/Sidebar.tsx` du dépôt `axion-crm-pro` (lu, non modifié). Pages nouvelles : plan 20 § 3 (U0 à U13), § 9 à 11 ; `07-ux-ui-2027.md` (13 écrans) ; `12-verif-ui-ecran-par-ecran.md` (UI-xx).

**Règles tenues partout.** Clair seulement. Un seul bouton plein visible par écran et par état. Vocabulaire simple (« Affaires », pas « Pipeline »). Blocs colorés au même sens que la console d’Axion. Alertes : console + e-mail seulement. Aucune marque blanche. Aucun constructeur visuel d’automatisations. Données factices (domaines en `.example`, aucune IP, aucune personne réelle).

**États.** Chaque écran a un état normal, vide, erreur (et chargement), choisis par le sélecteur « Maquette » en bas à droite ou par l’adresse `?etat=vide`, `?etat=erreur`, `?etat=chargement`.

## Travailler

| Page | Maquette | Route(s) actuelle(s) | État | Lot du plan 20 | Contenu en une phrase |
|---|---|---|---|---|---|
| Barre latérale et en-tête | `maquettes/index.html` | coquille actuelle (Sidebar, Header) | Existante, reprise dans le nouveau style | U0, U1 | Menu groupé (Travailler, Prospecter, Envois, Mesurer, Réglages), recherche Ctrl K, feu des envois, cloche des alertes, « Tout arrêter ». |
| Aujourd’hui (tableau de bord) | `maquettes/index.html` | `/` | Existante, reprise dans le nouveau style | U2-U9 (07 § 3.1) ; frein UI-45 en U11 | Ce qu’il faut faire aujourd’hui : réponses, tâches, campagne à valider, santé, mise en route. |
| Mise en route | `maquettes/mise-en-route.html` | — | Nouvelle | U12 (UI-19) | Les 5 jalons jusqu’à la première campagne, avec le temps de chacun. |
| Contacts (personnes) | `maquettes/contacts.html` | `/contacts, /console/contacts, /crm (redirection)` | Existante, reprise dans le nouveau style | Q1 + U2-U9 (07 § 3.4) ; ajout rapide UI-55 en U12 | Liste des personnes, filtres, ajout, import de fichier, actions de masse. |
| Fiche contact | `maquettes/contact.html` | `/console/personnes/$personKey` | Existante, reprise dans le nouveau style | U2-U9 (07 § 3.2) + Q1 | Étape commerciale, historique, « peut-on lui écrire ? », prochaine tâche, notes. |
| Entreprises | `maquettes/entreprises.html` | `/companies` | Existante, reprise dans le nouveau style | U2-U9 | Liste des entreprises avec secteur, ville, nombre de personnes et étape. |
| Fiche entreprise | `maquettes/entreprise.html` | `/companies/$companyId` | Existante, reprise dans le nouveau style | U2-U9 (07 § 3.2) | Affaire en cours, personnes, historique, questionnaire « X sur N », droit d’écrire. |
| Réseaux (fédérations, événements, international) | `maquettes/reseaux.html` | `/federations, /federations/$id, /evenements, /evenements/$id, /international/roumanie` | Existante, reprise dans le nouveau style | U2-U9 (reprise) | Fédérations et ordres, événements, entreprises hors de France (lecture seule). |
| Listes, listes dynamiques, étiquettes | `maquettes/listes.html` | `/listes, /listes/$id, /audiences, /audiences/new, /audiences/$id, /tags` | Existante, reprise dans le nouveau style | U2-U9 (07 § 3.4) ; vérification UI-21 en U12 | Listes fixes et dynamiques, adresses joignables, étiquettes. |
| Doublons à vérifier | `maquettes/doublons.html` | `/doublons` | Existante, reprise dans le nouveau style | U2-U9 (reprise) | Paires de fiches à fusionner ou à écarter, avec annulation. |
| À valider (venu du site) | `maquettes/a-valider.html` | `/console/propositions, /console/arbitrage, /console/lettre-et-guide, /console/lettre-et-guide/$id, /console/vivier` | Existante, reprise dans le nouveau style | U2-U9 (reprise) ; synchro selon § 11 point 2 | Propositions de la console du site, personnes à rattacher, abonnés lettre et guide (candidats : même écran, filtre). |
| Affaires (tableau en colonnes) | `maquettes/affaires.html` | — | Nouvelle | Maquette en U1 ; codage en Q2 (V1) | Affaires par étape (à contacter → gagné / perdu), « Déplacer vers… » au clavier. |
| Tâches | `maquettes/taches.html` | — | Nouvelle | Q1b (b) | Mes tâches du jour et en retard, créées aussi par les réponses ; rappel du matin. |

## Prospecter

| Page | Maquette | Route(s) actuelle(s) | État | Lot du plan 20 | Contenu en une phrase |
|---|---|---|---|---|---|
| Campagnes (liste) | `maquettes/campagnes.html` | — | Nouvelle | U2-U9 (UI-58) | Toutes les campagnes avec statut (7 badges), étape, envoyés, réponses, désinscriptions. |
| Campagne : création en 5 étapes | `maquettes/campagne-nouvelle.html` | — | Nouvelle | U2-U9 (07 § 3.5) + C1 | Cible, message, envoi, vérification (7 contrôles), validation par code e-mail. |
| Campagne : suivi | `maquettes/campagne-suivi.html` | — | Nouvelle | U2-U9 (UI-58) + RP3 | Progression, ce qui se passe, résultats par message, pause. |
| Messages types | `maquettes/messages-types.html` | — | Nouvelle | U12 (UI-08) | Liste des messages types avec version et statut (jamais supprimés : archivés). |
| Éditeur de message | `maquettes/message-editeur.html` | — | Nouvelle | U2-U9 (07 § 3.6) ; test UI-06 en C2 | Objet, texte, champs, aperçu réel, contrôles, « m’envoyer un test ». |
| Réponses | `maquettes/reponses.html` | — | Nouvelle | U2-U9 (07 § 3.7) + RP1 | File des réponses, suggestion en un geste, STOP à confirmer. |
| Réponses à rattacher | `maquettes/reponses-a-rattacher.html` | — | Nouvelle | U11 (UI-61, avancé par § 9 point 7) | Une réponse d’adresse inconnue et 3 fiches proposées. |
| Presse | `maquettes/presse.html` | `/media, /media/$id, /journalists, /journalists/$id, /presse/envois` | Existante, reprise dans le nouveau style | Reprise ; UI-24 en U13 (V1) | Médias, journalistes, communiqués envoyés. |

## Envois

| Page | Maquette | Route(s) actuelle(s) | État | Lot du plan 20 | Contenu en une phrase |
|---|---|---|---|---|---|
| Santé des envois | `maquettes/sante.html` | — | Nouvelle | U2-U9 (07 § 3.8, C-01, C-17) | Feux par domaine, test du matin, boîte ralentie, arrêt d’urgence. |
| Boîtes d’envoi | `maquettes/boites.html` | — | Nouvelle | U11 (UI-14) | Boîtes, état, volume du jour, ajout avec test de connexion. |
| Domaines | `maquettes/domaines.html` | — | Nouvelle | U2-U9 (07 § 3.9) ; UI-17 U12 ; UI-18 U13 ; UI-50 U12 | Domaines d’envoi, assistant DNS, « qui envoie en votre nom ? », listes noires. |
| Serveurs et test du matin | `maquettes/serveurs.html` | — | Nouvelle | U11 (UI-04, UI-05) ; UI-16 en U13 | État du serveur, boîtes témoins, adresses IP, ajout d’un serveur. |
| Montée en douceur (chauffe) | `maquettes/chauffe.html` | — | Nouvelle | U2-U9 (07 § 3.8) | Courbe de montée par boîte, avec texte équivalent et tableau. |
| Alertes (centre d’alertes) | `maquettes/alertes.html` | — | Nouvelle | U11 (UI-01) | Alertes en cours, ce que le système a fait, que faire. |
| Désinscriptions (ne plus écrire) | `maquettes/desinscriptions.html` | — | Nouvelle | U2-U9 (07 § 3.10, C-02) | « Puis-je écrire à… ? » en premier, puis la liste des oppositions. |
| Page publique de désinscription | `maquettes/desinscription-publique.html` | — | Nouvelle | U11 (UI-62) | Désinscription en un clic, option « toute mon organisation ». |

## Mesurer

| Page | Maquette | Route(s) actuelle(s) | État | Lot du plan 20 | Contenu en une phrase |
|---|---|---|---|---|---|
| Statistiques | `maquettes/statistiques.html` | `/coverage, /analytics (redirection)` | Existante, reprise dans le nouveau style | U2-U9 (07 § 3.11) ; rapports UI-43 en V1 | Résultats, entonnoir, carte de France, rapports (sans mesure d’ouverture). |

## Réglages

| Page | Maquette | Route(s) actuelle(s) | État | Lot du plan 20 | Contenu en une phrase |
|---|---|---|---|---|---|
| Réglages (accueil) | `maquettes/reglages.html` | `/settings` | Existante, reprise dans le nouveau style | U0 | Toutes les cartes de réglage, rangées en 6 groupes. |
| Mon compte et sécurité | `maquettes/compte.html` | `/settings (partie compte)` | Existante, reprise dans le nouveau style | S4 (UI-12) | Profil, codes de secours, appareils de confiance, raccourcis. |
| Alertes et avis | `maquettes/reglages-alertes.html` | — | Nouvelle | U11 (UI-02, UI-03) | Type × canal : console et e-mail seulement ; alerte de test ; seconde adresse. |
| Règles de prudence, horaires, automatismes | `maquettes/regles-prudence.html` | — | Nouvelle | U11 (UI-07) ; UI-26 et UI-30 en U12 | Règles en phrases (durcir seulement en V0), fenêtre d’envoi, interrupteurs. |
| Identité de l’expéditeur | `maquettes/identite.html` | — | Nouvelle | U11 (UI-13) ; lien RDV UI-59 en U12 | Entité qui écrit, bloc d’information art. 14, lien de rendez-vous. |
| Équipe et rôles | `maquettes/equipe.html` | `/users` | Existante, reprise dans le nouveau style | U12 (UI-11) | Personnes, rôles, invitation, désactivation (jamais de suppression). |
| Journal | `maquettes/journal.html` | `/audit-logs` | Existante, reprise dans le nouveau style | U12 (UI-10) | Qui a fait quoi, filtres, export avec code e-mail. |
| Sauvegardes | `maquettes/sauvegardes.html` | — | Nouvelle | U12 (UI-09) | Dernière sauvegarde, copie hors site, place, dernier exercice. |
| Demandes RGPD et registre de l’IA | `maquettes/rgpd.html` | `/rgpd/requests, /rgpd/ai-act` | Existante, reprise dans le nouveau style | U11 (UI-28, avancé par § 9 point 7) | Demandes avec délai restant, registre de l’IA, registre des traitements (V1). |
| Configuration technique | `maquettes/configuration.html` | — | Nouvelle | U11 (UI-15) + E3b | Version prête, différences en clair, appliquer, historique, retour automatique. |
| Outils techniques | `maquettes/technique.html` | `/admin/observability, /llm/router, /llm/proxy-providers, /llm/rotations` | Existante, reprise dans le nouveau style | Reprise (U12) | Santé du système, moteurs d’IA, serveurs relais, rotation des accès. |
| Collectes de données (ex-campagnes de collecte) | `maquettes/collectes.html` | `/campaigns, /campaigns/new, /campaigns/$id, /scraper-runs` | Existante, reprise dans le nouveau style | § 11 point 5 : renommer avant C1 (redirection + test) | Collectes en cours et terminées, historique ; anciens liens redirigés. |
| Écrans V1 et V2 | `maquettes/v1-ecrans.html` | — | Nouvelle | U13, K3, C5, C6, RP4, K9 (V1) | Clients, synchro, usage, exports, messages déclenchés, lettre, files, mises à jour, API, champs, appels, aide. |

## Hors coquille

| Page | Maquette | Route(s) actuelle(s) | État | Lot du plan 20 | Contenu en une phrase |
|---|---|---|---|---|---|
| Connexion et code par e-mail | `maquettes/connexion.html` | `/login, /2fa, /magic-link, /magic-link/verify, /password-reset` | Existante, reprise dans le nouveau style | S4 (07 § 3.13, C-04) | E-mail + mot de passe, code à 6 chiffres (collage accepté), appareil de confiance, codes de secours. |
| Page introuvable | `maquettes/introuvable.html` | notFoundComponent, /pas-encore-livre, /cold-email et /linkedin (retirées) | Existante, reprise dans le nouveau style | U2-U9 (reprise) | Lien ancien : retour à Aujourd’hui. |
| Toutes les maquettes | `maquettes/plan-des-pages.html` | — | Outil de maquette | U1 | Plan cliquable de toutes les pages. |

## Totaux

- **46 pages** dans ce tableau (**45 fichiers HTML** : la barre latérale et « Aujourd’hui » partagent `index.html`) : **21 existantes** reprises dans le nouveau style, **24 nouvelles**, 1 outil (plan des pages).
- **Toutes les routes de `routeTree.tsx` ont une place** (aucune page existante oubliée). Routes retirées sans écran : `/cold-email` et `/linkedin` (déjà redirigées), `/pas-encore-livre` (devient la page introuvable).
- Fenêtres et tiroirs maquettés dans les pages : Tout arrêter, changer d’espace, ajouter un contact, importer, note, opposition (STOP), m’envoyer un test, pause de campagne, ajout de boîte, assistant DNS, « qui envoie en votre nom ? », détail d’alerte, inviter, joignables.

## Écarts assumés (à valider par Will au test de 45 min)

1. **Barre latérale à 18 entrées en 4 groupes repliables**, au lieu de 7 entrées avec onglets (07 § 2.1). Raison : la mission demande que boîtes, domaines, serveurs, chauffe, alertes et désinscriptions soient trouvables directement. Chaque groupe se replie (choix mémorisé). Si Will préfère 7 entrées, on garde les onglets déjà présents en haut des pages et on retire les entrées du menu.
2. **Barre latérale claire** (blanche), et non bleu nuit (07 § 4.1) : Will veut le clair seulement ; la barre sombre ressemblait à un mode sombre partiel.
3. **« Montée en douceur »** dans le menu (lexique de 07), avec « chauffe » entre parenthèses dans cet index.
4. **Affaires** est maquetté maintenant, mais son codage reste en V1 (lot Q2), comme au plan 20.
5. **Collectes de données** passent dans Réglages (07 § 2.1) : ce sont des outils pour alimenter la base, pas de la prospection.

## Fabrication

Les fichiers HTML sont produits par `maquettes/_fabrique/fabrique.py` (Python 3, sans dépendance) : modifier le script, puis relancer `python3 maquettes/_fabrique/fabrique.py`. Ce fichier 23 est régénéré en même temps.
