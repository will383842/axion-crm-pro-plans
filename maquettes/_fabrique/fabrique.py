# -*- coding: utf-8 -*-
"""Fabrique toutes les maquettes HTML et l'index plan/23-MAQUETTES-INDEX.md.

Usage : python3 maquettes/_fabrique/fabrique.py
"""
import os
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
from socle import *  # noqa: E402,F401,F403
import pages_travail  # noqa: E402
import pages_prospecter  # noqa: E402
import pages_envois  # noqa: E402
import pages_reglages  # noqa: E402
import pages_reperes  # noqa: E402  (lot U1bis : 5 pages repères)

MAQ = os.path.dirname(ICI)
DEPOT = os.path.dirname(MAQ)

# Inventaire : (page, fichier, routes existantes, état, lot du plan 20, contenu en une phrase)
EX = 'Existante, reprise dans le nouveau style'
NV = 'Nouvelle'
INVENTAIRE = [
    ('Travailler', [
        ('Barre latérale et en-tête', 'index.html', 'coquille actuelle (Sidebar, Header)', EX, 'U0, U1', 'Menu groupé (Travailler, Prospecter, Envois, Mesurer, Réglages), recherche Ctrl K, feu des envois, cloche des alertes, « Tout arrêter ».'),
        ('Aujourd’hui (tableau de bord)', 'index.html', '/', EX, 'U2-U9 (07 § 3.1) ; frein UI-45 en U11', 'Ce qu’il faut faire aujourd’hui : réponses, tâches, campagne à valider, santé, mise en route.'),
        ('Mise en route', 'mise-en-route.html', '—', NV, 'U12 (UI-19)', 'Les 5 jalons jusqu’à la première campagne, avec le temps de chacun.'),
        ('Contacts (personnes)', 'contacts.html', '/contacts, /console/contacts, /crm (redirection)', EX, 'Q1 + U2-U9 (07 § 3.4) ; ajout rapide UI-55 en U12', 'Liste des personnes, filtres, ajout, import de fichier, actions de masse.'),
        ('Fiche contact', 'contact.html', '/console/personnes/$personKey', EX, 'U2-U9 (07 § 3.2) + Q1', 'Étape commerciale, historique, « peut-on lui écrire ? », prochaine tâche, notes.'),
        ('Entreprises', 'entreprises.html', '/companies', EX, 'U2-U9', 'Liste des entreprises avec secteur, ville, nombre de personnes et étape.'),
        ('Fiche entreprise', 'entreprise.html', '/companies/$companyId', EX, 'U2-U9 (07 § 3.2)', 'Affaire en cours, personnes, historique, questionnaire « X sur N », droit d’écrire.'),
        ('Réseaux (fédérations, événements, international)', 'reseaux.html', '/federations, /federations/$id, /evenements, /evenements/$id, /international/roumanie', EX, 'U2-U9 (reprise)', 'Fédérations et ordres, événements, entreprises hors de France (lecture seule).'),
        ('Listes, listes dynamiques, étiquettes', 'listes.html', '/listes, /listes/$id, /audiences, /audiences/new, /audiences/$id, /tags', EX, 'U2-U9 (07 § 3.4) ; vérification UI-21 en U12', 'Listes fixes et dynamiques, adresses joignables, étiquettes.'),
        ('Doublons à vérifier', 'doublons.html', '/doublons', EX, 'U2-U9 (reprise)', 'Paires de fiches à fusionner ou à écarter, avec annulation.'),
        ('À valider (venu du site)', 'a-valider.html', '/console/propositions, /console/arbitrage, /console/lettre-et-guide, /console/lettre-et-guide/$id, /console/vivier', EX, 'U2-U9 (reprise) ; synchro selon § 11 point 2', 'Propositions de la console du site, personnes à rattacher, abonnés lettre et guide (candidats : même écran, filtre).'),
        ('Affaires (tableau en colonnes)', 'affaires.html', '—', NV, 'Maquette en U1 ; codage en Q2 (V1)', 'Affaires par étape (à contacter → gagné / perdu), « Déplacer vers… » au clavier.'),
        ('Tâches', 'taches.html', '—', NV, 'Q1b (b)', 'Mes tâches du jour et en retard, créées aussi par les réponses ; rappel du matin.'),
    ]),
    ('Prospecter', [
        ('Campagnes (liste)', 'campagnes.html', '—', NV, 'U2-U9 (UI-58)', 'Toutes les campagnes avec statut (7 badges), étape, envoyés, réponses, désinscriptions.'),
        ('Campagne : création en 5 étapes', 'campagne-nouvelle.html', '—', NV, 'U2-U9 (07 § 3.5) + C1', 'Cible, message, envoi, vérification (7 contrôles), validation par code e-mail.'),
        ('Campagne : suivi', 'campagne-suivi.html', '—', NV, 'U2-U9 (UI-58) + RP3', 'Progression, ce qui se passe, résultats par message, pause.'),
        ('Messages types', 'messages-types.html', '—', NV, 'U12 (UI-08)', 'Liste des messages types avec version et statut (jamais supprimés : archivés).'),
        ('Éditeur de message', 'message-editeur.html', '—', NV, 'U2-U9 (07 § 3.6) ; test UI-06 en C2', 'Objet, texte, champs, aperçu réel, contrôles, « m’envoyer un test ».'),
        ('Réponses', 'reponses.html', '—', NV, 'U2-U9 (07 § 3.7) + RP1', 'File des réponses, suggestion en un geste, STOP à confirmer.'),
        ('Réponses à rattacher', 'reponses-a-rattacher.html', '—', NV, 'U11 (UI-61, avancé par § 9 point 7)', 'Une réponse d’adresse inconnue et 3 fiches proposées.'),
        ('Presse', 'presse.html', '/media, /media/$id, /journalists, /journalists/$id, /presse/envois', EX, 'Reprise ; UI-24 en U13 (V1)', 'Médias, journalistes, communiqués envoyés.'),
    ]),
    ('Envois', [
        ('Santé des envois', 'sante.html', '—', NV, 'U2-U9 (07 § 3.8, C-01, C-17)', 'Feux par domaine, test du matin, boîte ralentie, arrêt d’urgence.'),
        ('Boîtes d’envoi', 'boites.html', '—', NV, 'U11 (UI-14)', 'Boîtes, état, volume du jour, ajout avec test de connexion.'),
        ('Domaines', 'domaines.html', '—', NV, 'U2-U9 (07 § 3.9) ; UI-17 U12 ; UI-18 U13 ; UI-50 U12', 'Domaines d’envoi, assistant DNS, « qui envoie en votre nom ? », listes noires.'),
        ('Serveurs et test du matin', 'serveurs.html', '—', NV, 'U11 (UI-04, UI-05) ; UI-16 en U13', 'État du serveur, boîtes témoins, adresses IP, ajout d’un serveur.'),
        ('Montée en douceur (chauffe)', 'chauffe.html', '—', NV, 'U2-U9 (07 § 3.8)', 'Courbe de montée par boîte, avec texte équivalent et tableau.'),
        ('Alertes (centre d’alertes)', 'alertes.html', '—', NV, 'U11 (UI-01)', 'Alertes en cours, ce que le système a fait, que faire.'),
        ('Désinscriptions (ne plus écrire)', 'desinscriptions.html', '—', NV, 'U2-U9 (07 § 3.10, C-02)', '« Puis-je écrire à… ? » en premier, puis la liste des oppositions.'),
        ('Page publique de désinscription', 'desinscription-publique.html', '—', NV, 'U11 (UI-62)', 'Désinscription en un clic, option « toute mon organisation ».'),
    ]),
    ('Mesurer', [
        ('Statistiques', 'statistiques.html', '/coverage, /analytics (redirection)', EX, 'U2-U9 (07 § 3.11) ; rapports UI-43 en V1', 'Résultats, entonnoir, carte de France, rapports (sans mesure d’ouverture).'),
    ]),
    ('Réglages', [
        ('Réglages (accueil)', 'reglages.html', '/settings', EX, 'U0', 'Toutes les cartes de réglage, rangées en 6 groupes.'),
        ('Mon compte et sécurité', 'compte.html', '/settings (partie compte)', EX, 'S4 (UI-12)', 'Profil, codes de secours, appareils de confiance, raccourcis.'),
        ('Alertes et avis', 'reglages-alertes.html', '—', NV, 'U11 (UI-02, UI-03)', 'Type × canal : console et e-mail seulement ; alerte de test ; seconde adresse.'),
        ('Règles de prudence, horaires, automatismes', 'regles-prudence.html', '—', NV, 'U11 (UI-07) ; UI-26 et UI-30 en U12', 'Règles en phrases (durcir seulement en V0), fenêtre d’envoi, interrupteurs.'),
        ('Identité de l’expéditeur', 'identite.html', '—', NV, 'U11 (UI-13) ; lien RDV UI-59 en U12', 'Entité qui écrit, bloc d’information art. 14, lien de rendez-vous.'),
        ('Équipe et rôles', 'equipe.html', '/users', EX, 'U12 (UI-11)', 'Personnes, rôles, invitation, désactivation (jamais de suppression).'),
        ('Journal', 'journal.html', '/audit-logs', EX, 'U12 (UI-10)', 'Qui a fait quoi, filtres, export avec code e-mail.'),
        ('Sauvegardes', 'sauvegardes.html', '—', NV, 'U12 (UI-09)', 'Dernière sauvegarde, copie hors site, place, dernier exercice.'),
        ('Demandes RGPD et registre de l’IA', 'rgpd.html', '/rgpd/requests, /rgpd/ai-act', EX, 'U11 (UI-28, avancé par § 9 point 7)', 'Demandes avec délai restant, registre de l’IA, registre des traitements (V1).'),
        ('Configuration technique', 'configuration.html', '—', NV, 'U11 (UI-15) + E3b', 'Version prête, différences en clair, appliquer, historique, retour automatique.'),
        ('Outils techniques', 'technique.html', '/admin/observability, /llm/router, /llm/proxy-providers, /llm/rotations', EX, 'Reprise (U12)', 'Santé du système, moteurs d’IA, serveurs relais, rotation des accès.'),
        ('Collectes de données (ex-campagnes de collecte)', 'collectes.html', '/campaigns, /campaigns/new, /campaigns/$id, /scraper-runs', EX, '§ 11 point 5 : renommer avant C1 (redirection + test)', 'Collectes en cours et terminées, historique ; anciens liens redirigés.'),
        ('Écrans V1 et V2', 'v1-ecrans.html', '—', NV, 'U13, K3, C5, C6, RP4, K9 (V1)', 'Clients, synchro, usage, exports, messages déclenchés, lettre, files, mises à jour, API, champs, appels, aide.'),
    ]),
    ('Hors coquille', [
        ('Connexion et code par e-mail', 'connexion.html', '/login, /2fa, /magic-link, /magic-link/verify, /password-reset', EX, 'S4 (07 § 3.13, C-04)', 'E-mail + mot de passe, code à 6 chiffres (collage accepté), appareil de confiance, codes de secours.'),
        ('Page introuvable', 'introuvable.html', 'notFoundComponent, /pas-encore-livre, /cold-email et /linkedin (retirées)', EX, 'U2-U9 (reprise)', 'Lien ancien : retour à Aujourd’hui.'),
        ('Toutes les maquettes', 'plan-des-pages.html', '—', 'Outil de maquette', 'U1', 'Plan cliquable de toutes les pages.'),
    ]),
]


def plan_des_pages():
    h = []
    for groupe, items in INVENTAIRE:
        lignes = [['<a href="%s"><strong>%s</strong></a>' % (f, E(p)), badge('gris' if e.startswith('Existante') else 'violet', 'Reprise' if e.startswith('Existante') else ('Nouvelle' if e == NV else 'Outil'), '↻' if e.startswith('Existante') else '+'), E(l), E(c)] for p, f, r, e, l, c in items]
        h.append('<h2 class="mini-titre">%s</h2>' % E(groupe) + tableau(groupe, ['Page', 'État', 'Lot', 'Contenu'], lignes))
    n = sum(len(i) for _, i in INVENTAIRE)
    P = page('plan-des-pages', 'Toutes les maquettes', '<strong>%d pages</strong>. Chaque page a 4 états : normal, vide, erreur, chargement (cadre « Maquette » sous l’en-tête).' % n, ''.join(h))
    return P


def index_md():
    l = ['# 23 : Index des maquettes (lots U0 + U1) : 01/11/2026', '',
         '**But.** Montrer TOUTES les pages et la barre latérale avant tout codage d’écran (plan 20, lot U1). Ouvrir `maquettes/index.html` dans un navigateur (mode d’emploi : `maquettes/LISEZ-MOI.md`).', '',
         '**Sources.** Pages existantes : `frontend/src/app/routeTree.tsx` et `components/layout/Sidebar.tsx` du dépôt `axion-crm-pro` (lu, non modifié). Pages nouvelles : plan 20 § 3 (U0 à U13), § 9 à 11 ; `07-ux-ui-2027.md` (13 écrans) ; `12-verif-ui-ecran-par-ecran.md` (UI-xx).', '',
         '**Règles tenues partout.** Clair seulement. Un seul bouton plein visible par écran et par état. Vocabulaire simple (« Affaires », pas « Pipeline »). Blocs colorés au même sens que la console d’Axion. Alertes : console + e-mail seulement. Aucune marque blanche. Aucun constructeur visuel d’automatisations. Données factices (domaines en `.example`, aucune IP, aucune personne réelle).', '',
         '**États.** Chaque écran a un état normal, vide, erreur (et chargement), choisis par le cadre « Maquette » placé sous l’en-tête (dans le flux, jamais par-dessus le contenu) ou par l’adresse `?etat=vide`, `?etat=erreur`, `?etat=chargement`.', '']
    total = 0
    for groupe, items in INVENTAIRE:
        l.append('## %s' % groupe)
        l.append('')
        l.append('| Page | Maquette | Route(s) actuelle(s) | État | Lot du plan 20 | Contenu en une phrase |')
        l.append('|---|---|---|---|---|---|')
        for p, f, r, e, lot, c in items:
            total += 1
            l.append('| %s | `maquettes/%s` | %s | %s | %s | %s |' % (p, f, ('`' + r + '`') if r.startswith('/') else r, e, lot, c))
        l.append('')
    ex = sum(1 for _, it in INVENTAIRE for x in it if x[3] == EX)
    nv = sum(1 for _, it in INVENTAIRE for x in it if x[3] == NV)
    l += ['## Totaux', '', '- **%d pages** dans ce tableau (**%d fichiers HTML** : la barre latérale et « Aujourd\u2019hui » partagent `index.html`) : **%d existantes** reprises dans le nouveau style, **%d nouvelles**, 1 outil (plan des pages).' % (total, total - 1, ex, nv),
          '- **Toutes les routes de `routeTree.tsx` ont une place** (aucune page existante oubliée). Routes retirées sans écran : `/cold-email` et `/linkedin` (déjà redirigées), `/pas-encore-livre` (devient la page introuvable).',
          '- Fenêtres et tiroirs maquettés dans les pages : Tout arrêter, changer d’espace, ajouter un contact, importer, note, opposition (STOP), m’envoyer un test, pause de campagne, ajout de boîte, assistant DNS, « qui envoie en votre nom ? », détail d’alerte, inviter, joignables.', '',
          '## Écarts assumés (à valider par Will au test de 45 min)', '',
          '1. **Barre latérale à 18 entrées en 4 groupes repliables**, au lieu de 7 entrées avec onglets (07 § 2.1). Raison : la mission demande que boîtes, domaines, serveurs, chauffe, alertes et désinscriptions soient trouvables directement. Chaque groupe se replie (choix mémorisé). Si Will préfère 7 entrées, on garde les onglets déjà présents en haut des pages et on retire les entrées du menu.',
          '2. **Barre latérale claire** (blanche), et non bleu nuit (07 § 4.1) : Will veut le clair seulement ; la barre sombre ressemblait à un mode sombre partiel.',
          '3. **« Montée en douceur »** dans le menu (lexique de 07), avec « chauffe » entre parenthèses dans cet index.',
          '4. **Affaires** est maquetté maintenant, mais son codage reste en V1 (lot Q2), comme au plan 20.',
          '5. **Collectes de données** passent dans Réglages (07 § 2.1) : ce sont des outils pour alimenter la base, pas de la prospection.', '',
          '## Lot U1bis : refonte visuelle (01/11/2026)', '',
          'Retour de Will : éléments qui se chevauchent, trop de texte, pas assez de cadres, de blocs et de pastilles, boutons peu visibles, contraste faible. Réponse :',
          '- **Nouveau socle** (`maquettes/style.css`, `_fabrique/socle.py`) : cartes blanches à cadre net, blocs colorés par sens, pastilles pleines, tuiles à gros chiffres, jauges, anneaux, barres, courbes, grandes tuiles de feu, stepper, un seul gros bouton plein par écran. Guide : `maquettes/GUIDE-STYLE.md`.',
          '- **5 pages repères refaites** (`_fabrique/pages_reperes.py`) : Aujourd’hui, Contacts, Nouvelle campagne, Santé des envois, Réponses. Captures : `maquettes/captures/`.',
          '- **Contrôle automatique** `_fabrique/controle.py` (Playwright) : chevauchements, débordements, contrastes, taille du texte, bouton plein unique, à 1440 / 1024 / 768 / 360 px. Résultat : 0 problème sur les 45 pages.',
          '- Les 40 autres pages gardent leur contenu mais prennent le nouveau style ; elles seront refaites avec le guide.', '',
          '## Fabrication', '',
          'Les fichiers HTML sont produits par `maquettes/_fabrique/fabrique.py` (Python 3, sans dépendance) : modifier le script, puis relancer `python3 maquettes/_fabrique/fabrique.py`. Ce fichier 23 est régénéré en même temps.', '']
    return '\n'.join(l)


def main():
    pages = {}
    for m in (pages_travail, pages_prospecter, pages_envois, pages_reglages, pages_reperes):
        pages.update(m.P)
    pages['plan-des-pages.html'] = plan_des_pages()
    # Garde : chaque page de l'inventaire existe
    manquantes = [f for _, it in INVENTAIRE for (_, f, *_r) in it if f not in pages]
    if manquantes:
        raise SystemExit('Pages manquantes : %s' % manquantes)
    for nom, contenu in pages.items():
        with open(os.path.join(MAQ, nom), 'w', encoding='utf-8') as fh:
            fh.write(contenu)
    with open(os.path.join(DEPOT, 'plan', '23-MAQUETTES-INDEX.md'), 'w', encoding='utf-8') as fh:
        fh.write(index_md())
    print('%d pages écrites.' % len(pages))


if __name__ == '__main__':
    main()
