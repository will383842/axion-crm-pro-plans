# 23 : Index des maquettes (lot M1 : deux produits, menu réel, reprise fidèle) : 01/11/2026

**But.** Montrer TOUTES les pages avant tout codage d’écran. Ouvrir `maquettes/index.html` dans un navigateur (mode d’emploi : `maquettes/LISEZ-MOI.md`).

**Décisions de Will appliquées (lot M1).**
- **D1. Deux produits distincts**, facturés à part : **CRM Pro** (bleu de marque `#2448e5`) et **Envoi** (bleu-vert `#0a6e78`, texte blanc 6,0:1). Chaque page montre son produit : liseré coloré du menu, sélecteur de produit en haut du menu, badge et bande de couleur dans l’en-tête, bouton principal de la couleur du produit.
- **D2. Menu du CRM = menu réel de Will, à l’identique** (`Sidebar.tsx`) : Tableau de bord ; À traiter ; Ma base ; Presse ; Réseaux ; Ciblage ; Alimenter la base ; Réglages ; Technique (accordéon : une section ouverte à la fois). **Envoi** est un espace à part : Campagnes, Réponses, Boîtes d’envoi, Domaines, Serveurs et adresses IP, Chauffe, Santé des envois, Désinscriptions, Alertes d’envoi, Réglages d’envoi.
- **D3. Fidélité à l’existant** : chaque page qui existe dans le CRM réel reprend ses titres, colonnes, filtres, actions et textes (relevé du code, lecture seule). La colonne « Reprise de » donne le composant ; « Nouvelle » sinon. La même note est affichée en tête de chaque page (cadre « Maquette »).
- **D4. Style** : `maquettes/GUIDE-STYLE.md`. **D5. Ajouts** : les 52 ajouts du plan 27 (dont les 15 premiers) ; voir le tableau en fin de fichier. **D6.** La cloche se remplit (6 notifications, des deux produits). **D7.** Données factices réalistes, aucun vrai nom.

**États.** Chaque écran a un état normal, vide, erreur et chargement (cadre « Maquette » sous l’en-tête, ou `?etat=vide`, `?etat=erreur`, `?etat=chargement`).

## CRM Pro

| Page | Maquette | Produit | Reprise de |
|---|---|---|---|
| Bonjour Will | `maquettes/index.html` | CRM Pro | `frontend/src/features/dashboard/DashboardPage.tsx (+ AFaire, MesAudiences, SizeDistributionChart)` |
| Affaires | `maquettes/affaires.html` | CRM Pro | Nouvelle |
| Mes tâches | `maquettes/taches.html` | CRM Pro | Nouvelle |

## CRM Pro · À traiter

| Page | Maquette | Produit | Reprise de |
|---|---|---|---|
| Doublons à vérifier | `maquettes/doublons.html` | CRM Pro | `frontend/src/features/doublons/DoublonsPage.tsx` |
| Personnes à rattacher | `maquettes/personnes-a-rattacher.html` | CRM Pro | `frontend/src/features/crm-console/ArbitragePage.tsx` |
| Propositions à valider | `maquettes/propositions.html` | CRM Pro | `frontend/src/features/propositions/PropositionsPage.tsx` |

## CRM Pro · Ma base

| Page | Maquette | Produit | Reprise de |
|---|---|---|---|
| Entreprises | `maquettes/entreprises.html` | CRM Pro | `frontend/src/features/companies/CompaniesListPage.tsx` |
| Boulangerie des Tilleuls | `maquettes/entreprise.html` | CRM Pro | `frontend/src/features/companies/CompanyDetailPage.tsx` |
| Contacts | `maquettes/contacts.html` | CRM Pro | `frontend/src/features/crm-console/ContactsHubPage.tsx (et contacts/ContactsListPage.tsx hors console)` |
| Paul Morin | `maquettes/contact.html` | CRM Pro | `frontend/src/features/crm-console/PersonTimelinePage.tsx` |
| Newsletter et guide | `maquettes/newsletter-guide.html` | CRM Pro | `frontend/src/features/crm-console/PersonnesPage.tsx` |
| Hugo Marchand | `maquettes/personne-newsletter.html` | CRM Pro | `frontend/src/features/crm-console/PersonneDetailPage.tsx` |
| Candidats | `maquettes/candidats.html` | CRM Pro | `frontend/src/features/crm-console/CandidatesPage.tsx` |

## CRM Pro · Presse

| Page | Maquette | Produit | Reprise de |
|---|---|---|---|
| Médias | `maquettes/medias.html` | CRM Pro | `frontend/src/features/media/MediaListPage.tsx` |
| Le Courrier du Rhône | `maquettes/media.html` | CRM Pro | `frontend/src/features/media/MediaDetailPage.tsx` |
| Journalistes | `maquettes/journalistes.html` | CRM Pro | `frontend/src/features/media/JournalistsListPage.tsx` |
| Léa Fournier | `maquettes/journaliste.html` | CRM Pro | `frontend/src/features/media/JournalistDetailPage.tsx` |
| Communiqués envoyés | `maquettes/communiques.html` | CRM Pro | `frontend/src/features/media/EnvoisPressePage.tsx` |

## CRM Pro · Réseaux

| Page | Maquette | Produit | Reprise de |
|---|---|---|---|
| Fédérations et ordres | `maquettes/federations.html` | CRM Pro | `frontend/src/features/federations/FederationsPage.tsx` |
| Fédération BTP Rhône | `maquettes/federation.html` | CRM Pro | `frontend/src/features/federations/FederationDetailPage.tsx` |
| Événements | `maquettes/evenements.html` | CRM Pro | `frontend/src/features/evenements/EvenementsPage.tsx` |
| Salon des artisans de Vienne | `maquettes/evenement.html` | CRM Pro | `frontend/src/features/evenements/EvenementDetailPage.tsx` |

## CRM Pro · Ciblage

| Page | Maquette | Produit | Reprise de |
|---|---|---|---|
| Audiences | `maquettes/audiences.html` | CRM Pro | `frontend/src/features/audiences/AudiencesListPage.tsx` |
| Nouvelle audience | `maquettes/audience-nouvelle.html` | CRM Pro | `frontend/src/features/audiences/AudienceBuilderPage.tsx (+ éditeur ET / OU / SAUF : ajout plan 27 n° 4)` |
| Organisateurs Rhône-Alpes | `maquettes/audience.html` | CRM Pro | `frontend/src/features/audiences/AudienceDetailPage.tsx` |
| Listes | `maquettes/listes.html` | CRM Pro | `frontend/src/features/listes/ListesManuellesPage.tsx` |
| Invités salon des artisans | `maquettes/liste.html` | CRM Pro | `frontend/src/features/listes/ListeManuelleDetailPage.tsx` |

## CRM Pro · Alimenter la base

| Page | Maquette | Produit | Reprise de |
|---|---|---|---|
| Collectes | `maquettes/collectes.html` | CRM Pro | `frontend/src/features/campaigns/CampaignsListPage.tsx (route /campaigns → /collectes)` |
| Nouvelle collecte | `maquettes/collecte-nouvelle.html` | CRM Pro | `frontend/src/features/campaigns/CampaignWizardPage.tsx` |
| Rhône — PME artisanat | `maquettes/collecte.html` | CRM Pro | `frontend/src/features/campaigns/CampaignDetailPage.tsx` |
| Carte de France | `maquettes/carte-france.html` | CRM Pro | `frontend/src/features/coverage/CoveragePage.tsx (+ FranceCoverageMap.tsx)` |

## CRM Pro · Réglages

| Page | Maquette | Produit | Reprise de |
|---|---|---|---|
| Paramètres | `maquettes/parametres.html` | CRM Pro | `frontend/src/features/settings/SettingsPage.tsx` |
| Mon compte et sécurité | `maquettes/compte.html` | CRM Pro | `frontend/src/features/settings/ChangerMotDePasse.tsx (+ sécurité : nouvelle)` |
| Utilisateurs | `maquettes/utilisateurs.html` | CRM Pro | `frontend/src/features/users/UsersPage.tsx` |
| Étiquettes | `maquettes/etiquettes.html` | CRM Pro | `frontend/src/features/tags/TagsManagerPage.tsx (+ « Campagne vers cette étiquette » : ajout plan 27 n° 5)` |
| Demandes RGPD | `maquettes/rgpd.html` | CRM Pro | `frontend/src/features/rgpd/RgpdRequestsPage.tsx` |

## CRM Pro · Technique

| Page | Maquette | Produit | Reprise de |
|---|---|---|---|
| Entreprises en Roumanie | `maquettes/roumanie.html` | CRM Pro | `frontend/src/features/international/RoumaniePage.tsx` |
| Historique des collectes | `maquettes/historique-collectes.html` | CRM Pro | `frontend/src/features/scraping/ScraperRunsPage.tsx` |
| Santé du système | `maquettes/sante-systeme.html` | CRM Pro | `frontend/src/features/observability/ObservabilityPage.tsx (+ settings/ReglagesTechniques.tsx ; carte Sauvegardes : nouvelle)` |
| Moteurs d’IA | `maquettes/moteurs-ia.html` | CRM Pro | `frontend/src/features/llm/LlmRouterPage.tsx` |
| Serveurs relais | `maquettes/serveurs-relais.html` | CRM Pro | `frontend/src/features/llm/ProxyProvidersPage.tsx` |
| Rotation des accès | `maquettes/rotation-acces.html` | CRM Pro | `frontend/src/features/llm/RotationsPage.tsx` |
| Registre de l’IA | `maquettes/registre-ia.html` | CRM Pro | `frontend/src/features/rgpd/AiActRegisterPage.tsx` |
| Journal des actions | `maquettes/journal.html` | CRM Pro | `frontend/src/features/rgpd/AuditLogsPage.tsx` |

## Envoi

| Page | Maquette | Produit | Reprise de |
|---|---|---|---|
| Campagnes | `maquettes/campagnes.html` | Envoi | Nouvelle |
| Calendrier des envois | `maquettes/calendrier-envois.html` | Envoi | Nouvelle |
| Nouvelle campagne | `maquettes/campagne-nouvelle.html` | Envoi | Nouvelle |
| Organisateurs Rhône-Alpes | `maquettes/campagne-suivi.html` | Envoi | Nouvelle |
| Organisateurs · v3 | `maquettes/message-editeur.html` | Envoi | Nouvelle |
| Messages types | `maquettes/messages-types.html` | Envoi | Nouvelle |
| Résultats | `maquettes/resultats.html` | Envoi | Nouvelle |
| Réponses | `maquettes/reponses.html` | Envoi | Nouvelle |
| Réponse à rattacher | `maquettes/reponses-a-rattacher.html` | Envoi | Nouvelle |
| Boîtes d’envoi | `maquettes/boites.html` | Envoi | Nouvelle |
| will@prospection-b.example | `maquettes/boite.html` | Envoi | Nouvelle |
| Domaines | `maquettes/domaines.html` | Envoi | Nouvelle |
| prospection-a.example | `maquettes/domaine.html` | Envoi | Nouvelle |
| Serveurs et adresses IP | `maquettes/serveurs.html` | Envoi | Nouvelle |
| Configuration du serveur | `maquettes/configuration.html` | Envoi | Nouvelle |
| Chauffe | `maquettes/chauffe.html` | Envoi | Nouvelle |
| Santé des envois | `maquettes/sante.html` | Envoi | Nouvelle |
| Chercher un envoi | `maquettes/chercher-envoi.html` | Envoi | Nouvelle |
| Feu vert | `maquettes/feu-vert.html` | Envoi | Nouvelle |
| Désinscriptions | `maquettes/desinscriptions.html` | Envoi | Nouvelle |
| Alertes d’envoi | `maquettes/alertes.html` | Envoi | Nouvelle |
| Réglages d’envoi | `maquettes/reglages-envoi.html` | Envoi | Nouvelle |
| Identité de l’expéditeur | `maquettes/identite.html` | Envoi | Nouvelle |
| Alertes et avis | `maquettes/reglages-alertes.html` | Envoi | Nouvelle |
| Règles et horaires | `maquettes/regles-prudence.html` | Envoi | Nouvelle |

## Hors coquille (écrans seuls)

| Page | Maquette | Produit | Reprise de |
|---|---|---|---|
| Connexion | `maquettes/connexion.html` | CRM Pro | `frontend/src/features/auth/LoginPage.tsx, TwoFactorPage.tsx, MagicLinkPage.tsx, PasswordResetPage.tsx` |
| Se désinscrire | `maquettes/desinscription-publique.html` | Envoi | Nouvelle |
| Page introuvable | `maquettes/introuvable.html` | CRM Pro | `frontend/src/features/misc/NotFoundPage.tsx` |

## Totaux

- **72 pages** (+ le plan des pages) : **44 reprises** de l’existant, **28 nouvelles**. Produit CRM Pro : 47 ; produit Envoi : 25.
- Toutes les routes de `routeTree.tsx` ont une page : `/doublons`, `/console/arbitrage`, `/console/propositions`, `/companies(/$id)`, `/console/contacts` (et `/contacts`), `/console/lettre-et-guide(/$id)`, `/console/vivier`, `/console/personnes/$key`, `/media(/$id)`, `/journalists(/$id)`, `/presse/envois`, `/federations(/$id)`, `/evenements(/$id)`, `/audiences(/new, /$id)`, `/listes(/$id)`, `/campaigns(/new, /$id)` (= Collectes), `/coverage`, `/settings`, `/users`, `/tags`, `/rgpd/requests`, `/international/roumanie`, `/scraper-runs`, `/admin/observability`, `/llm/router`, `/llm/proxy-providers`, `/llm/rotations`, `/rgpd/ai-act`, `/audit-logs`, `/login`, `/2fa`, `/magic-link`, `/password-reset`, page introuvable.
- Pages sans entrée de menu (le menu reste celui de Will) : Mes tâches et Affaires (onglets du Tableau de bord), Mon compte (avatar), Sauvegardes (carte de Santé du système) ; côté Envoi : Résultats, Messages types, Calendrier (onglets de Campagnes), Chercher un envoi et Feu vert (onglets de Santé des envois), Configuration (onglet de Serveurs), fiches Boîte et Domaine.
- Pages retirées par rapport au lot U1bis : `a-valider`, `presse`, `reseaux`, `technique`, `statistiques`, `reglages`, `equipe`, `sauvegardes`, `mise-en-route`, `v1-ecrans` (leur contenu est réparti dans les pages ci-dessus, au bon endroit du menu de Will). Les écrans V1/V2 (clients, synchro, API…) restent décrits au plan 20.

## Contrôle automatique (01/11/2026)

`controle.py --toutes` : **73 pages × 4 largeurs (1440, 1024, 768, 360 px) = 1 300 vues** (4 états, chaque onglet, chaque étape d’assistant). Résultat : **0 chevauchement, 0 débordement, 0 contraste insuffisant, 0 texte sous 16 px (hors pastilles), 0 écran à deux boutons pleins, 0 erreur JavaScript.** Captures légères (premier écran) de 8 pages clés dans `maquettes/captures/`.

## Les 15 ajouts prioritaires du plan 27 : où les voir

| Rang | Ajout | Maquette |
|---|---|---|
| 1 | Campagne vers une étiquette | `etiquettes.html` (bouton plein), `entreprise.html`, `campagnes.html`, `campagne-nouvelle.html` (étape 1) |
| 2 | Fiche d’un domaine (30 jours) | `domaine.html` |
| 3 | Fiche d’une boîte | `boite.html` |
| 4 | État de chaque destinataire | `campagne-suivi.html` (onglet Destinataires), `contact.html` |
| 5 | Résultats par boîte, domaine, liste | `resultats.html` |
| 6 | Répondre depuis le CRM | `reponses.html` (bloc Répondre, même fil) |
| 7 | Reprogrammer (changer la date) | `campagnes.html`, `campagne-suivi.html` (fenêtre « Changer la date ») |
| 8 | Dupliquer | `campagnes.html`, `campagne-suivi.html` |
| 9 | Pause depuis la liste | `campagnes.html` (bouton Pause dans la ligne) |
| 10 | Terminer | `campagnes.html`, `campagne-suivi.html` |
| 11 | Ajouter une adresse IP (et appliquer) | `serveurs.html` (fenêtre), Ctrl K |
| 12 | Chercher un envoi | `chercher-envoi.html`, Ctrl K, `campagnes.html` |
| 13 | Éditeur ET / OU / SAUF | `audience-nouvelle.html` |
| 14 | Export d’une liste ou sélection | `entreprises.html`, `contacts.html`, `listes.html`, `liste.html`, `audience.html`, `etiquettes.html` |
| 15 | Export du registre des oppositions | `desinscriptions.html`, `rgpd.html` |
| + | Programmer / reprogrammer, test A/B | `campagne-nouvelle.html` (étapes 2 et 3), `campagne-suivi.html` (onglet Test A/B) |

## Fabrication

Les fichiers HTML sont produits par `maquettes/_fabrique/fabrique.py` (Python 3, sans dépendance). Contrôle : `python3 maquettes/_fabrique/controle.py --toutes` (Playwright). Ce fichier 23 est régénéré en même temps.
