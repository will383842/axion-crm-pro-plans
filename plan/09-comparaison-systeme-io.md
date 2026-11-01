# 09 : CRM Pro face à systeme.io : que nous manque-t-il ? (30/10/2026)

Lecture seule : aucun compte créé, aucun e-mail, rien exécuté. Sources web consultées le 30/10/2026 (liste en fin de fichier). Plan comparé : fichiers 00, 02, 03, 08 de ce dossier ; dépôt `C:\Users\willi\Documents\Projets\Axion-CRM-Pro` (lecture rapide, pas de Stripe ni de clé d'API publique dans `backend/app`). RIEN n'est codé côté envoi : « prévu » veut dire « écrit dans le plan ».

## Verdict

**Pour le métier de Will (prospection B2B à froid de TPE/PME, puis un outil installé chez des clients), il ne manque rien d'essentiel par rapport à systeme.io : le plan couvre déjà, ou prévoit, tout ce que systeme.io fait en e-mailing et en CRM, et va plus loin là où ça compte.** Ce ne sont pas deux outils concurrents : systeme.io INTERDIT la prospection à froid (« listes achetées, récupérées sur internet ou sans consentement explicite interdites », vérifiées à l'import, envoi suspendu sinon). Il est fait pour vendre à un public déjà abonné.

Il reste **5 petits écarts pertinents, absents du plan, environ 20 jours-agent** (§ 3) : un constructeur visuel d'automatisations, une bibliothèque de modèles prêts pour les clients, le branchement de l'agenda de chaque client, un connecteur entrant systeme.io (et outils semblables), un serveur MCP sur l'API publique. Plus un reclassement : la marque blanche (02 M4) passe de P2 à V1 si Will revend l'outil.

**Tout le reste de systeme.io est hors périmètre et doit le rester** : tunnels de vente, site et pages, blog, boutique et paiements, formations, communautés, webinaires, affiliation, SMS. Will a déjà le site axionia (pages, blog, formulaires, Tour France IA), la console (Stripe décidé le 27/10, dossier client), Zernio pour les réseaux. Pour un client qui en a besoin : **s'intégrer** (systeme.io → CRM par webhook), ne pas reconstruire.

**Là où systeme.io reste devant aujourd'hui** : il existe et marche tout de suite, en libre-service, pour 0 à 97 $/mois ; notre envoi reste à construire (≈ 323-363 j d'envoi + ≈ 185 j de CRM selon 00 et 08). Ce retard est le vrai écart, pas une liste de fonctions.

---

## 1. Ce que fait systeme.io (relevé du 30/10/2026)

Éditeur : ITACWT Limited (Dublin, Irlande) ; serveurs AWS en Irlande (politique de confidentialité). Plus de 500 000 utilisateurs revendiqués.

| Domaine | Ce que fait systeme.io | Source |
|---|---|---|
| E-mailing | Newsletters (campagnes ponctuelles), campagnes en séquence (autorépondeur), éditeur glisser-déposer, planification, envoi de test ; statistiques avec **ouvertures** (pixel) ; analyses jugées « basiques » par les avis | API (ressource Mailing), Capterra, GetApp |
| Automatisations | Règles « déclencheur → action » (inscription à un formulaire, achat, étiquette ajoutée → ajouter/retirer étiquette, inscrire à une campagne ou une formation, envoyer un e-mail, webhook) ; **workflows** visuels (en bêta dans l'API). Avis : pas de « si/alors » avancé | API, avis 2026 |
| Tags, segmentation | Étiquettes, champs personnalisés (`ContactField`), segmentation par étiquette et critères | API, Capterra |
| CRM / contacts | Contacts, **pipelines** Kanban (étapes, notes, règles simples), y compris en gratuit ; pas de vrai suivi d'opportunités à la GoHighLevel | page « crm-pipelines », comparatifs |
| Tunnels et pages | Tunnels de vente (3 à illimité selon l'offre), pages, site, modèles, test A/B des pages | page tarifs, Capterra |
| Formulaires | Formulaires et pages de capture intégrés aux tunnels | Capterra, Zapier (« New Form Submission ») |
| Boutique, paiements | Produits numériques et physiques, offres, coupons, abonnements, Stripe et PayPal, 0 % de commission systeme.io | API, page tarifs |
| Formations, membres | Formations, modules, leçons, élèves illimités ; communautés | API, page tarifs |
| Webinaires | Webinaires automatisés (offre Webinar et plus) | page tarifs |
| Affiliation | Programme d'affiliation intégré, sur toutes les offres | page tarifs |
| Blog | Blog intégré | page tarifs |
| Agenda | Calendrier de réservation (événements, disponibilités) | API (Booking Calendar) |
| SMS | Modèles et envoi de SMS | API, page d'accueil |
| Intégrations | **API publique** (`/api/v2`, clé en en-tête) ; **webhooks** : CONTACT_OPT_IN, CONTACT_CREATED, CONTACT_TAG_ADDED/REMOVED, SALE_NEW, SALE_CANCELED ; Zapier ; **guide de serveur MCP** | developer.systeme.io, Zapier |
| Domaines | Domaines personnalisés pour les pages ; **authentification du domaine d'envoi** (SPF, DKIM, DMARC par enregistrements CNAME) exigée pour une adresse pro | aide 4247, 272, Namecheap |
| Multi-utilisateurs | « Assistants » invités, droits par section (e-mails, formations, tunnels…), propriétaire seul sur facturation et moyens de paiement ; sans coût par siège sur les offres payantes | aide 1709, page « team-management » |
| Agences | Sous-comptes illimités (chacun avec les limites de l'offre), tableau de bord unique, marque blanche annoncée sur la page agences (sources tierces contradictoires) | page tarifs, page « for-agencies » |
| Délivrabilité | **IP mutualisées**, réputation collective ; chaque compte classé dans 5 groupes (Nouvel utilisateur, Faible, Modéré, Élevé, Quarantaine) selon **ouvertures**, plaintes et rebonds (faible risque : ouvertures > 20 %, plaintes < 0,25 %, rebonds < 0,7 % ; quarantaine : plaintes > 1 % ou rebonds > 5 %). Nouveau compte : pause d'analyse tous les 100 e-mails jusqu'à 500 (jusqu'à 6 h). Import de liste : origine contrôlée, envoi suspendu le temps de la validation. Contenu suspect : envoi suspendu et relu | aide 4472, 227 |
| RGPD | Politique de confidentialité : ITACWT responsable de traitement pour ses propres traitements, données « non transférées hors UE » (texte ambigu ailleurs) ; **aucun DPA trouvé** en ligne pour les contacts des clients (non vérifié auprès du support) | politique de confidentialité |
| Tarifs | Free 0 $ (2 000 contacts, 3 tunnels, 1 formation, 1 règle d'automatisation, 1 domaine), Startup 17 $/mois (5 000 contacts), Webinar 47 $ (10 000), Unlimited 97 $ (illimité) ; annuel = 2 mois offerts ; envois d'e-mails illimités sur toutes les offres (page officielle, 30/10/2026 ; certains sites tiers citent encore 27 $ pour Startup) | page tarifs |

## 2. Comparaison point par point

Légende des colonnes : **(a)** couvert ou prévu chez nous ; **(b)** manque et pertinent ; **(c)** hors périmètre voulu ; **(d)** nous faisons mieux. Références = lignes des fichiers 02, 03, 08.

| Fonction systeme.io | Classe | Chez nous |
|---|---|---|
| Contacts, étiquettes, listes | (a) EXISTE | 02 A1, A2, C1, C2 |
| Segmentation | (a)+(d) | Audiences dynamiques EXISTENT (02 C3) ; ET/OU/SAUF, exclusions par historique, segment figé prévus (C8, C9). Mieux : ciblage par les données d'entreprise (secteur, taille, région, étape, fonction) que systeme.io n'a pas |
| Champs personnalisés | (a) prévu | 02 A12, remonté en V1 par 08 F7 (3 j) |
| Newsletters et campagnes | (a) prévu | 02 E1-E11, 03 § 2 ; lettre d'information par le moteur du CRM (décision de Will, 00) |
| Séquences (autorépondeur) | (a)+(d) prévu | 02 E3 ; mieux : arrêt sur réponse, RDV, opposition, passage client ; pression commerciale toutes campagnes confondues (E10) |
| Éditeur glisser-déposer | (a) prévu en V2 | Texte d'abord pour la prospection (voulu) ; éditeur par blocs pour la lettre : 08 F16 (6 j, V2) |
| Test A/B | (a) prévu V1 | 02 E12 (sur les réponses, pas les ouvertures) |
| Statistiques | (a)+(d) prévu | 02 H3-H8 ; mieux : réponses classées et RDV attribués à la campagne, sans pixel (les ouvertures sont faussées par Apple MPP) |
| Règles d'automatisation simples | (a) partiel | Règles automatiques d'étiquettes EXISTENT (C1) ; tâches automatiques (D7), messages déclenchés par un événement (E19, remonté V1 par 08 F10) |
| **Constructeur visuel de workflows** | **(b)** | Absent du plan. Voir § 3, N1 |
| Pipelines Kanban | (a) prévu P1 | 02 D2 (Kanban, 3 j), D3 (opportunités, 2 j) |
| Formulaires, pages de capture | (a) prévu V1 | 08 F9 (formulaire intégrable + pages « merci / confirmez / désinscrit », 4 j) ; le site axionia a déjà les siens |
| Double inscription (opt-in) | (a) prévu V1 | 08 F8 (3 j) |
| Désinscription, centre de préférences | (a) prévu | 03 § 5 (un clic RFC 8058) ; préférences 08 F17 (V2) |
| Authentification du domaine d'envoi | (a)+(d) prévu | 03 § 7.2 ; mieux : domaines et IP **dédiés**, contrôle quotidien SPF/DKIM/DMARC/PTR, chauffe pilotée par les résultats |
| Assistants, droits | (a) partiel | 4 rôles, 16 permissions EXISTENT ; rôles par client et fins prévus (02 I8, M2) ; 2FA par e-mail (I1) |
| Sous-comptes, agences | (a)+(d) prévu | 02 M0-M13 ; mieux : une installation par client, données isolées, réputation séparée |
| Marque blanche | (a) prévu P2 → **à remonter en V1** si revente | 02 M4 (3 j) |
| API publique | (a) prévu V1 | 08 F11 (5 j, dès le 1er client) |
| Webhooks sortants | (a) prévu V2 | 08 F19 (3 j) |
| **Serveur MCP** | **(b)** | Absent. Voir N5 |
| **Agenda de réservation** | **(b)** pour les clients | Calendly d'Axion reçu par le site (02 G1, derrière drapeau) ; rien pour l'agenda d'un client. Voir N3 |
| **Modèles prêts à l'emploi** | **(b)** | Bibliothèque de modèles de systeme.io ; chez nous gabarits vides. Voir N2 |
| Import de contacts | (a) prévu | Import par l'interface 02 B4 (4 j) ; mieux : provenance obligatoire et date de collecte (art. 14) |
| Tunnels de vente, site, pages, blog | (c) | Le site axionia les fait déjà pour Axion |
| Boutique, paiements, abonnements | (c) | Stripe dans la console (décision du 27/10) ; le CRM n'encaisse rien |
| Formations, communautés, élèves | (c) | Hors métier du CRM |
| Webinaires | (c) | Hors métier |
| Affiliation | (c) | Le réseau d'apporteurs (Axion Partners) vit à part |
| SMS | (c) | Prospection par SMS : le consentement préalable s'applique (L.34-5 CPCE), donc sans intérêt pour du froid ; un rappel de RDV par SMS resterait possible plus tard |
| Inscription en libre-service, offre gratuite | (c) pour l'instant | Décision « installation par client d'abord » (00). Le libre-service est une V2 à décider si Will veut un vrai SaaS |

### Ce que notre outil fait mieux (d), en résumé
1. **Prospection à froid conforme** : information art. 14, provenance de chaque fiche, opposition unique revérifiée juste avant l'envoi, opposition par domaine, segments sensibles fermés par défaut, contrôle « objet lié à la profession », validation de chaque version de texte par Will (02 J, E6-E8 ; 08 § D). systeme.io ne le permet tout simplement pas.
2. **Ciblage par le CRM** : base INSEE, FINESS, événements, fonction de la personne, étape commerciale, historique de contact ; systeme.io ne voit que ses propres contacts inscrits.
3. **Isolation par client** : base, IP, domaines, boîtes, chauffe, liste d'opposition et sauvegardes propres à chaque client ; chez systeme.io, IP partagées et réputation collective, un mauvais voisin peut peser.
4. **Réponses et RDV** : relève des boîtes, tri (intéressé, STOP, demande RGPD…), arrêt des séquences, RDV rattaché à la campagne (02 F, G3). systeme.io mesure surtout des ouvertures.
5. **Propriété des données** : hébergement par Axion ou chez le client, code dans le dépôt, export complet (B7), aucune suppression imposée ; pas de plafond de contacts.

### Là où systeme.io reste meilleur (honnêteté)
- **Disponible aujourd'hui**, sans construction ni serveur à tenir ; prise en main en libre-service.
- **Coût d'entrée** : 0 à 97 $/mois, contre 35-90 € par mois en V0 pour notre envoi, plus le temps de construction (00).
- **Tout-en-un marketing grand public** (tunnels, paiement, formations) que nous ne ferons pas, volontairement.

## 3. Écarts pertinents absents du plan : effort et priorité

Les écarts déjà chiffrés dans 02 et 08 ne sont pas recomptés.

| # | Écart | Pourquoi c'est utile à la cible de Will | Effort (j-agent) | Prio |
|---|---|---|---|---|
| N1 | **Constructeur visuel d'automatisations** par espace : déclencheur (formulaire, étiquette, étape, réponse classée, RDV, import) → conditions → actions (étiquette, liste, séquence, tâche, webhook) ; réutilise les moteurs de séquence et de règles prévus ; chaque automatisation qui **envoie** passe par la validation (E8) | Un client TPE/PME veut régler ses relances sans développeur ; c'est ce qui rend systeme.io « simple » | 8 à 10 | V2 (V1 si les premiers clients le demandent) |
| N2 | **Bibliothèque de modèles prêts** : séquences B2B type (1er contact, relance, après RDV), gabarits avec blocs légaux, segments et étapes de pipeline types, installés à la mise en route d'un client (02 M13) | Le client démarre en une heure au lieu de partir d'une page blanche ; textes déjà conformes (jamais « Qualiopi », « certifié », « Grenoble ») | 3 | V1, avant le 1er client |
| N3 | **Agenda propre à chaque client** : connecteur Calendly (jeton et webhook signé par espace) et lien Google Agenda/Outlook ; même attribution des RDV aux campagnes que pour Axion (02 G3) | Aujourd'hui seul le Calendly d'Axion arrive (par le site) ; un client n'aurait aucun RDV rattaché | 3 | V1, avant le 1er client |
| N4 | **Connecteur entrant systeme.io (et outils semblables)** : recevoir CONTACT_OPT_IN, CONTACT_TAG_ADDED, SALE_NEW (webhook signé) → fiche, consentement daté, étape « client » ; **jamais** de poussée de contacts de prospection vers systeme.io (contraire à ses règles), seulement des contacts consentants | Un client qui vend déjà par systeme.io garde ses tunnels et voit ses acheteurs dans le CRM ; évite de reconstruire tunnels et boutique | 3 | V2 (après 08 F11 et F19) |
| N5 | **Serveur MCP** sur l'API publique par espace (lecture de fiches et de statistiques, création de tâches ; tout envoi reste soumis à validation) | Will et ses clients pilotent déjà par Claude ; systeme.io le propose | 2 à 3 | V2 |
| — | Reclassement : **marque blanche** 02 M4 (3 j) de P2 en V1 si Will revend l'outil sous son nom à des clients | Les agences de systeme.io l'ont | (déjà chiffré) | V1 si revente |
| | **Total des ajouts** | | **≈ 19 à 22 j** (+15 % de relecture ≈ 22 à 25 j) | V1 ≈ 6 j ; V2 ≈ 13 à 16 j |

Rien de tout cela n'est V0 : aucun de ces écarts ne bloque le premier envoi d'Axion.

## 4. Ce que change le fait que systeme.io vise un public abonné

- **Ses règles excluent le métier de Will.** L'aide officielle (article 227) interdit les listes « achetées, récupérées sur internet ou sans consentement explicite », contrôle l'origine à chaque import et suspend l'envoi. Ni Axion ni un client ne peut faire de la prospection à froid avec systeme.io sans risquer la fermeture du compte. Comparer « fonction par fonction » est donc en partie trompeur : les deux outils ne font pas le même travail.
- **Ses seuils supposent un public engagé.** Le groupe « faible risque » exige plus de 20 % d'ouvertures ; un premier message de prospection obtient bien moins, et nous refusons de mesurer les ouvertures (pas de pixel, règle de Will). Sur des IP mutualisées, notre trafic serait vite en quarantaine.
- **Conséquence pour nous** : nous devons porter nous-mêmes la réputation (IP et domaines dédiés, chauffe lente, vérification des adresses, disjoncteurs). C'est ce qui rend notre plan plus long et plus cher que « s'abonner à systeme.io » : c'est le prix de la prospection à froid, pas un défaut de conception.
- **La conformité est plus exigeante** pour nous : pour un abonné, le consentement suffit ; pour la prospection B2B, il faut l'intérêt légitime, l'objet lié à la profession, l'information art. 14 et l'opposition simple. Le plan les code en gardes (08 § D, 03 § 8).
- **Pour la lettre d'information à des abonnés**, systeme.io est en revanche un bon outil, peu cher. Will a décidé que la lettre passe par le moteur du CRM (00) : les ajouts 08 F8, F9, F16-F18 (≈ 16 j) restent donc nécessaires. Il faudra un groupe d'envoi et des domaines **séparés** de la prospection pour que l'une ne dégrade pas l'autre (03 § 1.2, pools).
- **Pour un client qui vend en ligne** (formations, tunnels), le bon montage est : systeme.io pour ses abonnés et ses ventes, notre CRM pour sa prospection B2B, relié par le connecteur N4 dans un seul sens.

## Sources (consultées le 30/10/2026)

Officielles :
- [systeme.io : tarifs](https://systeme.io/pricing) et [tarifs FR](https://systeme.io/fr/pricing) (tableau partiellement vide au chargement ; plafonds pris dans la FAQ)
- [systeme.io : page d'accueil FR](https://systeme.io/fr)
- [systeme.io : CRM pipelines](https://systeme.io/crm-pipelines) · [agences](https://systeme.io/for-agencies/) · [gestion d'équipe](https://systeme.io/team-management)
- [systeme.io : documentation développeur (API, webhooks, MCP)](https://developer.systeme.io/)
- [systeme.io : politique de confidentialité](https://systeme.io/fr/privacy-policy)

Tierces (à recouper) :
- [SchoolMaker : tarifs 2026](https://schoolmaker.com/fr/blog/tarifs-systeme-io) (concurrent, mis à jour le 10/09/2026, chiffres de tunnels différents de la page officielle)
- [Capterra : avis et fonctions](https://www.capterra.com/p/198994/Systeme/reviews/) · [GetApp : avis](https://www.getapp.com/all-software/a/systeme/reviews/)
- [Netpartners : revue 2026](https://netpartners.marketing/systeme-io-review-features-pricing-alternatives-2026/) · [Consultevo : GoHighLevel contre systeme.io](https://consultevo.com/gohighlevel-vs-systeme-io-2026-comparison/)
- [Zapier : déclencheurs systeme.io](https://zapier.com/apps/systemeio/integrations/webhook) · [Namecheap : authentification du domaine](https://www.namecheap.com/support/knowledgebase/article.aspx/10701/2175/how-to-configure-your-private-email-account-with-systemeio/)

Non vérifié : existence d'un DPA systeme.io pour les contacts des clients ; détail exact de la marque blanche (sources contradictoires) ; plafonds par offre des workflows, tags, A/B, assistants (le tableau officiel ne s'est pas chargé).
