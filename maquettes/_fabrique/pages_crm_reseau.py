# -*- coding: utf-8 -*-
"""Lot M1 · produit CRM Pro : Tableau de bord, Réseaux, Ciblage, Alimenter la base
(+ Mes tâches et Affaires, pages sans entrée de menu, ouvertes depuis le tableau de bord).
Reprise fidèle des composants réels, puis ajouts du plan 27. Données factices."""
from socle import *  # noqa: F401,F403

P = {}
F = 'frontend/src/features/'
ONG_TDB = lambda actif: onglets_nav('Sections du tableau de bord', [('index.html', 'Tableau de bord', ''), ('taches.html', 'Mes tâches', '5'), ('affaires.html', 'Affaires', '9')], actif)


def _carte_afaire(n, lib, icone, teinte, href):
    return kpi(lib, n, icone, teinte, 'Ouvrir →', href)


# ======================= TABLEAU DE BORD =======================
def _index():
    afaire = kpis(_carte_afaire('12', 'Doublons à vérifier', 'doublon', 'terracotta', 'doublons.html'),
                  _carte_afaire('7', 'Personnes à rattacher', 'balance', 'violet', 'personnes-a-rattacher.html'),
                  _carte_afaire('3', 'Événements à relancer', 'calendrier', 'vert', 'evenements.html#relances'))
    base = kpis(kpi('Entreprises', '48 212', 'entreprise', 'bleu', '81 % de TPE', 'entreprises.html'),
                kpi('Prospects joignables', '21 904', 'coche', 'vert', 'hors sites devinés non vérifiés', 'audiences.html'),
                kpi('Fiches enrichies', '62 %', 'etincelle', 'violet', '', graph=jauge('Fiches enrichies', 62, 100, 'violet', '62 %')),
                kpi('Qualité moyenne', '74', 'stats', 'ambre', '', unite='/ 100', graph=jauge('Qualité moyenne', 74, 100, 'ambre', '74 / 100')))
    taille = bloc('Par taille', '<div class="pile" style="gap:12px">%s%s%s%s</div>' % (
        jauge('TPE', 39050, 48212, 'bleu', '39 050'), jauge('PME', 7940, 48212, 'bleu', '7 940'), jauge('ETI', 1010, 48212, 'bleu', '1 010'), jauge('Grand groupe', 212, 48212, 'bleu', '212')), icone='stats')
    aud = bloc('Mes audiences', lignes(ligne('Prospects contactables', 'Mise à jour cette nuit', initiales('P C', 'vert'), '<strong class="chiffre">21 904</strong>', 'audience.html'),
                                       ligne('Organisateurs Rhône-Alpes', 'Mise à jour cette nuit', initiales('O R', 'bleu'), '<strong class="chiffre">312</strong>', 'audience.html'),
                                       ligne('Presse régionale AURA', 'Mise à jour cette nuit', initiales('P R', 'violet'), '<strong class="chiffre">186</strong>', 'audience.html')),
               icone='personnes', pied=btn('Tout voir', 'petit', 'audiences.html', 'fleche') + '<span class="petit">Mises à jour chaque nuit</span>')
    taches_ = bloc('Mes tâches du jour', lignes(
        ligne('Relancer la fédération du bâtiment', 'Fédération BTP Rhône', '', badge('rouge', 'En retard', '■'), 'taches.html'),
        ligne('Rappeler Paul Morin', 'Boulangerie des Tilleuls · 11:00', '', badge('bleu', '11:00', '◷'), 'taches.html'),
        ligne('Envoyer le devis', 'Imprimerie du Lac · 14:00', '', badge('bleu', '14:00', '◷'), 'taches.html')), 'bleu', 'taches', mot='5 aujourd’hui',
        pied=btn('Toutes les tâches', 'petit', 'taches.html', 'fleche'), attrs='data-nouveau')
    collecte = bloc('Collecte en cours', chiffres([('1 240', 'créées'), ('62 %', 'du budget'), ('48 min', 'restantes')]) + '<div style="margin-top:12px">%s</div>' % jauge('Entreprises', 620, 1000, 'bleu', '620 / 1 000'),
                    'bleu', 'campagne', mot='En cours', pied=btn('Voir la collecte', 'petit', 'collecte.html', 'fleche'))
    normal = (mini_titre('À faire') + afaire + '<div style="display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap">%s<span class="petit">Chiffres mis à jour il y a 2 min</span></div>' % mini_titre('Ma base')
              + base + '<div class="grille deux">%s%s</div>' % (taille, aud) + '<div class="grille deux">%s%s</div>' % (taches_, collecte))
    vide = etat_vide('entreprise', 'Votre base est vide', 'Aucune entreprise pour l’instant. Choisissez un département sur la carte de France.', btn('Récupérer des entreprises', 'plein', 'carte-france.html', 'carte'))
    P['index.html'] = page('index', 'Bonjour Will', 'Tableau de bord · <strong>dimanche 1er novembre</strong> · 22 choses à traiter', normal, vide,
                           etat_erreur('Les chiffres du tableau de bord n’ont pas pu être lus.'), onglets_haut=ONG_TDB('index.html'),
                           reprise=F + 'dashboard/DashboardPage.tsx (+ AFaire, MesAudiences, SizeDistributionChart)')


def _taches():
    def t(titre, sous, droite, cid, coche=False):
        return ('<li><label class="ligne" for="%s"><input type="checkbox" id="%s"%s data-toast="Tâche faite." data-annulable><span class="quoi"><strong>%s</strong><span>%s</span></span>%s</label></li>'
                % (cid, cid, ' checked' if coche else '', E(titre), E(sous), droite))
    haut = kpis(kpi('Aujourd’hui', '5', 'taches', 'bleu', ''), kpi('En retard', '1', 'alerte', 'rouge', 'depuis hier'), kpi('Cette semaine', '14', 'calendrier', 'violet', ''), kpi('Faites ce mois', '38', 'coche', 'vert', ''))
    jour = bloc('Aujourd’hui', '<ul class="lignes">%s</ul>' % ''.join([
        t('Relancer la fédération du bâtiment', 'Fédération BTP Rhône · créée par une réponse', badge('rouge', 'En retard', '■'), 't1'),
        t('Rappeler Paul Morin', 'Boulangerie des Tilleuls', badge('bleu', '11:00', '◷'), 't2'),
        t('Envoyer le devis', 'Imprimerie du Lac', badge('bleu', '14:00', '◷'), 't3'),
        t('Préparer le salon', 'Salon des artisans de Vienne', badge('gris', 'Sans heure', '○'), 't4'),
        t('Vérifier la liste presse', 'Presse régionale AURA', badge('gris', 'Sans heure', '○'), 't5')]), 'bleu', 'taches', mot='5 à faire')
    semaine = bloc('Plus tard cette semaine', lignes(ligne('Rendez-vous Club de voile', 'Mardi 3 nov. · 10:00', '', badge('violet', 'Rendez-vous', '✦')),
                                                    ligne('Relance événement CCI', 'Jeudi 5 nov.', '', badge('gris', 'Relance', '○'))), icone='calendrier')
    rappel = bloc('Rappel du matin', interrupteur('Recevoir mes tâches à 08:00', 'Par e-mail, jours ouvrés.', 'rap-matin'), 'violet', 'cloche', mot='Nouveau')
    normal = haut + '<div class="grille deux-un">%s<div class="pile">%s%s</div></div>' % (jour, semaine, rappel)
    P['taches.html'] = page('taches', 'Mes tâches', '<strong>5 tâches</strong> aujourd’hui, 1 en retard.', normal,
                            etat_vide('taches', 'Rien à faire aujourd’hui', 'Toutes vos tâches sont faites.', ''),
                            actions=btn('Ajouter une tâche', 'plein', icone='plus', attrs='data-toast="Nouvelle tâche (maquette)."'), onglets_haut=ONG_TDB('taches.html'), menu='index')


def _affaires():
    COL = [('Nouveau', 'gris', [('Club de voile du Lac', '—')]), ('Qualifié', 'bleu', [('Boulangerie des Tilleuls', '1 200 €'), ('Office de tourisme du Val', '3 400 €')]),
           ('Opportunité', 'violet', [('Imprimerie du Lac', '8 900 €'), ('Transports Rivière', '12 000 €')]), ('Client', 'vert', [('Garage des Saules', '2 600 €')]),
           ('Perdu', 'rouge', [('Atelier Bois & Forme', '4 000 €')])]
    cols = []
    for i, (n, t, cartes) in enumerate(COL):
        cc = ''.join('<div class="carte-affaire"><a href="entreprise.html">%s</a><div class="bas"><strong>%s</strong>%s</div>'
                     '<label class="visuellement-cache" for="dep-%d-%d">Déplacer vers…</label><select id="dep-%d-%d" data-deplacer><option value="">Déplacer vers…</option>%s</select></div>'
                     % (E(a), m, badge(t, n, '●'), i, j, i, j, ''.join('<option value="col-%d">%s</option>' % (k, x[0]) for k, x in enumerate(COL) if k != i)) for j, (a, m) in enumerate(cartes))
        cols.append('<section class="colonne" id="col-%d"><h2><span>%s</span><span class="badge %s" data-s="●">%d</span></h2><div class="cartes-col">%s</div></section>' % (i, n, t, len(cartes), cc))
    haut = kpis(kpi('Affaires ouvertes', '9', 'affaires', 'bleu', ''), kpi('Montant en jeu', '28 100 €', 'stats', 'violet', 'chance pondérée : 11 900 €'),
                kpi('Signature prévue ce mois', '2', 'calendrier', 'ambre', ''), kpi('Gagnées ce trimestre', '3', 'coche', 'vert', ''))
    normal = haut + '<div class="colonnes">%s</div>' % ''.join(cols) + '<p class="petit" style="margin-top:12px">Étapes reprises de l’existant (Taxonomy.php : nouveau → perdu). Raison de perte demandée au passage en « Perdu ».</p>'
    P['affaires.html'] = page('affaires', 'Affaires', '<strong>9 affaires</strong> ouvertes · 28 100 € en jeu', normal,
                              etat_vide('affaires', 'Aucune affaire', 'Passez une entreprise en « Opportunité » pour créer une affaire.', ''),
                              onglets_haut=ONG_TDB('affaires.html'), menu='index')


# ======================= RÉSEAUX =======================
FED_FAM = ['Toutes', 'Confédération interprofessionnelle', 'Fédération ou syndicat professionnel', 'Ordre professionnel', 'Chambre ou compagnie de profession réglementée', 'Chambre consulaire',
           'Syndicat de salariés', 'Association de métier ou de fonction', 'Association d’entreprises ou de dirigeants', 'Interprofession ou organisme technique', 'Pôle de compétitivité ou cluster',
           'Financeur de la formation (OPCO…)', 'Développement économique', 'Association d’élus', 'Mutuelle ou caisse agricole', 'Propriétaires et locataires']
PART = {'Accepté': 'vert', 'Proposé': 'ambre', 'En discussion': 'ambre', 'Refusé': 'rouge', 'Pas encore proposé': 'gris'}
PERT = {'Haute': 'vert', 'Moyenne': 'ambre', 'Faible': 'gris'}


def _federations():
    R = [('Fédération BTP Rhône', 'FBTP 69', 'Fédération ou syndicat professionnel', 'Départemental', 'Bâtiment et travaux publics', 'Lyon', '69 · Auvergne-Rhône-Alpes', 'Fédération nationale du BTP', 'Haute', 'E-mail vérifié', 'En discussion', True),
         ('Ordre régional des architectes', 'ORA', 'Ordre professionnel', 'Régional', 'Architecture, ingénierie, contrôle technique', 'Lyon', '69 · Auvergne-Rhône-Alpes', '—', 'Haute', 'Formulaire seulement', 'Proposé', False),
         ('Chambre des métiers de l’Isère', 'CMA 38', 'Chambre consulaire', 'Départemental', 'Interprofessionnel', 'Grenoble', '38 · Auvergne-Rhône-Alpes', 'CMA régionale', 'Moyenne', 'E-mail vérifié', 'Accepté', True),
         ('Union des commerçants de Vienne', 'UCV', 'Association d’entreprises ou de dirigeants', 'Local', 'Commerce de détail', 'Vienne', '38 · Auvergne-Rhône-Alpes', '—', 'Moyenne', 'Téléphone seulement', 'Pas encore proposé', False),
         ('Syndicat des transporteurs alpins', 'STA', 'Fédération ou syndicat professionnel', 'Régional', 'Transport et logistique', 'Chambéry', '73 · Auvergne-Rhône-Alpes', '—', 'Faible', 'Aucun contact', 'Refusé', False)]
    lig = [['<a href="federation.html"><strong>%s</strong></a><span class="sous">%s · 2 antennes%s</span>' % (E(n), s, ' · <span style="color:var(--vert-texte)">Événement à venir</span>' if ev else ''),
            E(fa), E(ni), E(se), '%s<span class="sous">%s</span>' % (E(v), dr), ('<a href="federation.html">%s</a>' % E(tr)) if tr != '—' else '—', badge(PERT[pe], pe, '●'), E(co), badge(PART[pa], pa, '●')]
           for n, s, fa, ni, se, v, dr, tr, pe, co, pa, ev in R]
    haut = kpis(kpi('Organismes', '1 486', 'monument', 'bleu', 'tous niveaux'), kpi('Partenariats acceptés', '23', 'coche', 'vert', ''),
                kpi('En discussion', '11', 'reponses', 'ambre', 'relance à suivre'), kpi('Événement à venir', '64', 'calendrier', 'violet', 'organismes concernés'))
    f = filtres_champs([('s', 'Famille', FED_FAM, 'f-fam'), ('s', 'Niveau', ['Tous', 'National', 'Régional', 'Départemental', 'Local'], 'f-niv'),
                        ('s', 'Secteur représenté', ['Tous', 'Bâtiment et travaux publics', 'Commerce de détail', 'Transport et logistique', 'Interprofessionnel', 'Culture, sport et loisirs'], 'f-sect'),
                        ('s', 'Région', ['Toutes', 'Auvergne-Rhône-Alpes', 'Île-de-France', 'Occitanie', 'La Réunion'], 'f-reg'), ('t', 'Département', '69, 2A, 974', 'f-dep'),
                        ('s', 'Taille des adhérents', ['Toutes', 'TPE', 'PME', 'ETI', 'Grand groupe'], 'f-taille'), ('s', 'Pertinence', ['Toutes', 'Haute', 'Moyenne', 'Faible'], 'f-pert'),
                        ('s', 'Contactabilité', ['Toutes', 'E-mail vérifié', 'Formulaire seulement', 'Téléphone seulement', 'Site ou LinkedIn seulement', 'Aucun contact'], 'f-cont'),
                        ('s', 'Partenariat', ['Tous', 'Pas encore proposé', 'Proposé', 'En discussion', 'Accepté', 'Refusé'], 'f-part'),
                        ('s', 'Événement à venir', ['Peu importe', 'Avec un événement à venir', 'Sans événement à venir'], 'f-ev'), ('r', 'Recherche', 'Nom, sigle, ville', 'f-q')],
                       '<span class="petit">1 486 organismes</span>')
    t = tableau('Fédérations', ['Organisme', 'Famille', 'Niveau', 'Secteurs représentés', 'Où', 'Tête de réseau', 'Pertinence', 'Contact', 'Partenariat'], lig, liens=['federation.html'] * 5, secondaires=(1, 2, 3, 5, 7))
    normal = haut + f + t + pagination('Page 1 / 30', False)
    P['federations.html'] = page('federations', 'Fédérations et ordres', 'Qui représente qui, où, et <strong>où en est le partenariat</strong>.', normal,
                                 etat_vide('monument', 'Aucun organisme', 'Aucun organisme ne correspond à ces filtres.', ''), etat_erreur('Impossible de charger les fédérations.'),
                                 actions=btn('Exporter CSV', 'contour', icone='export', attrs='data-toast="Export CSV téléchargé (ajout plan 27)."'), reprise=F + 'federations/FederationsPage.tsx')


def _demarche(options, etapes, hist):
    form = (champ('Étape', 'dm-etape', 'select', options) + champ('Prochaine relance', 'dm-rel', 'date', '2026-11-12')
            + champ('Note (jamais de coordonnées : elles vont sur la fiche contact)', 'dm-note', 'textarea', 'Rencontre au salon, intéressés par une intervention.'))
    part = bloc('Partenariat' if etapes else 'Ma démarche', form, 'ambre', 'reponses', mot='En discussion', pied=btn('Enregistrer', 'plein', icone='coche', attrs='data-toast="Démarche enregistrée"'))
    h = bloc('Historique', chrono(hist), icone='horloge')
    return part + h


def _federation():
    org = bloc('L’organisme', dl([('Sigle', 'FBTP 69'), ('Nom développé', 'Fédération du bâtiment et des travaux publics du Rhône'), ('Famille', 'Fédération ou syndicat professionnel'),
                                  ('Niveau', 'Départemental'), ('Secteurs représentés', 'Bâtiment et travaux publics'), ('Taille des adhérents', 'TPE, PME'), ('Pertinence', badge('vert', 'Haute', '●')),
                                  ('Contactabilité', 'E-mail vérifié'), ('Où', '8 rue des Bâtisseurs · 69 · Auvergne-Rhône-Alpes'), ('SIREN', '<span class="mono">000 000 501</span>'),
                                  ('Site', '<a href="#">Ouvrir</a>'), ('E-mail générique', 'contact@fbtp69.example · domaine vérifié le 02/10/2026')])
               + '<p style="margin-top:12px"><a href="entreprise.html">Voir la fiche entreprise complète</a></p>', icone='monument')
    reseau = bloc('Réseau', '<p style="margin-bottom:10px">Fédération nationale du BTP › FFB Auvergne-Rhône-Alpes › <strong>FBTP 69</strong></p>' + mini_titre('Antennes (2)')
                  + lignes(ligne('<a href="federation.html">Antenne Villefranche</a>', 'Local · Villefranche-sur-Saône'), ligne('<a href="federation.html">Antenne Givors</a>', 'Local · Givors')), icone='reseau')
    cont = bloc('Contacts', tableau('Contacts', ['Nom', 'Fonction', 'E-mail', 'Informé (art. 14)'], [
        ['Bernard Coste', 'Président', 'b.coste@fbtp69.example', badge('vert', 'Oui', '✓')], ['Hélène Mazet', 'Déléguée générale', 'h.mazet@fbtp69.example', 'Non — mention au premier message']]), icone='personnes')
    ev = bloc('Événements', lignes(ligne('<a href="evenement.html">Assemblée annuelle du BTP</a>', '20/11/2026 · Lyon', '', badge('gris', 'Repéré', '○') + ' ' + badge('ambre', 'Proposée', '▲'))), icone='calendrier')
    lat = _demarche(['En discussion', 'Pas encore proposé', 'Proposé', 'Accepté', 'Refusé'], True,
                    [('02/10/2026', 'Partenariat proposé', 'par Will', 'envoi', 'ambre'), ('18/10/2026', 'Partenariat en discussion', 'par Will', 'reponses', 'bleu')])
    normal = '<div class="grille deux-un"><div class="pile">%s%s%s%s</div><div class="pile">%s</div></div>' % (org, reseau, cont, ev, lat)
    P['federation.html'] = page('federation', 'Fédération BTP Rhône', 'Fédération ou syndicat professionnel · Départemental · Lyon', normal,
                                erreur=etat_erreur('Organisme introuvable.'), actions=btn('← Toutes les fédérations', 'contour', 'federations.html'),
                                fil=[('Fédérations et ordres', 'federations.html', 'federations')], reprise=F + 'federations/FederationDetailPage.tsx')


INTERV = {'Acceptée': 'vert', 'Réalisée': 'vert', 'Proposée': 'ambre', 'Refusée': 'rouge', 'Pas encore proposée': 'gris'}


def _evenements():
    E_ = [('12/11/2026', '09:00', 'Salon des artisans de Vienne', 'Salon', 'Vienne', 'Auvergne-Rhône-Alpes', 'Union des commerçants de Vienne', 'Oui', 'Inscrit', 'Proposée', '05/11/2026'),
          ('20/11/2026', '18:30', 'Assemblée annuelle du BTP', 'Conférence', 'Lyon', 'Auvergne-Rhône-Alpes', 'Fédération BTP Rhône', 'Inconnu', 'Repéré', 'Pas encore proposée', '—'),
          ('26/11/2026', '08:00', 'Petit-déjeuner CCI Isère', 'Petit-déjeuner', 'Grenoble', 'Auvergne-Rhône-Alpes', 'CCI de l’Isère', 'Non', 'Inscrit', 'Acceptée', '—'),
          ('03/12/2026', '14:00', 'Atelier IA pour TPE', 'Atelier', 'Annecy', 'Auvergne-Rhône-Alpes', 'Club entreprises Annecy', 'Oui', 'Repéré', 'Refusée', '—')]
    lig = [['%s<span class="sous">%s</span>' % (d, h), '<a href="evenement.html"><strong>%s</strong></a>' % E(n), E(t), '%s<span class="sous">%s</span>' % (E(v), r), '<a href="entreprise.html">%s</a>' % E(o),
            badge('bleu', 'Oui', '●') if a == 'Oui' else E(a), E(p), badge(INTERV[i], i, '●'), E(rl)] for d, h, n, t, v, r, o, a, p, i, rl in E_]
    cols = ['Quand', 'Événement', 'Type', 'Où', 'Organisateur', 'Appel à intervenants', 'Ma participation', 'Intervention', 'Relance']
    f = filtres_champs([('s', 'Période', ['À venir', 'Passés', 'Récurrents / sans date', 'Tous'], 'v-per'), ('s', 'Région', ['Toutes régions', 'Auvergne-Rhône-Alpes', 'Île-de-France'], 'v-reg'),
                        ('s', 'Type', ['Tous types', 'Salon', 'Conférence', 'Atelier', 'Club d’affaires', 'Réseau d’entrepreneurs', 'Afterwork', 'Petit-déjeuner', 'Table ronde', 'Pitch', 'Remise de prix', 'Festival', 'Ciné-débat', 'Autre'], 'v-type'),
                        ('s', 'Ma participation', ['Toutes', 'Repéré', 'Inscrit', 'Rencontré'], 'v-part'), ('s', 'Intervention', ['Toutes', 'Pas encore proposée', 'Proposée', 'Acceptée', 'Refusée', 'Réalisée'], 'v-int'),
                        ('s', 'Appel à intervenants', ['Tous', 'Oui', 'Non', 'Inconnu'], 'v-appel'), ('r', 'Recherche', 'Nom, ville, organisateur', 'v-q')], '<span class="petit">4 événements</span>')
    tab_ev = f + tableau('Événements', cols, lig, liens=['evenement.html'] * 4, secondaires=(2, 4, 5, 6, 8)) + pagination('Page 1 / 1', False)
    orgs = filtres(['Tous', 'Entreprise', 'Association', 'Chambre de commerce', 'Enseignement', 'Cabinet (conseil, avocats)', 'Institution', 'Média', 'Réseau ou club d’affaires', 'Organisation professionnelle']) + tableau(
        'Organisateurs', ['Organisateur', 'Nature', 'Ville', 'E-mail', 'Site'], [
            ['<a href="entreprise.html"><strong>CCI de l’Isère</strong></a>', 'Chambre de commerce', 'Grenoble', 'evenements@cci38.example', '<a href="#">Voir</a>'],
            ['<a href="entreprise.html"><strong>Union des commerçants de Vienne</strong></a>', 'Association', 'Vienne', 'bureau@ucv.example', '—']])
    relances = tableau('Relances à faire', cols, lig[:1], liens=['evenement.html'], secondaires=(2, 4, 5, 6, 8))
    haut = kpis(kpi('À venir', '42', 'calendrier', 'bleu', 'dans 90 jours'), kpi('Interventions acceptées', '6', 'coche', 'vert', ''), kpi('Relances à faire', '3', 'rafraichir', 'terracotta', 'cette semaine'),
                kpi('Appels à intervenants', '9', 'micro', 'violet', 'ouverts'))
    normal = haut + onglets('Événements', [('ev', 'Événements <span class="nb">42</span>', tab_ev), ('org', 'Organisateurs <span class="nb">118</span>', orgs), ('relances', 'Relances à faire <span class="nb">3</span>', relances)])
    P['evenements.html'] = page('evenements', 'Événements', 'Salons, clubs d’affaires, ateliers CCI : <strong>où aller, qui relancer</strong>.', normal,
                                etat_vide('calendrier', 'Aucun événement', 'Aucun événement ne correspond à ces filtres.', ''), etat_erreur('Impossible de charger les événements.'),
                                reprise=F + 'evenements/EvenementsPage.tsx')


def _evenement():
    ev = bloc('L’événement', dl([('Quand', '12/11/2026 · 09:00'), ('Où', 'Halle des expositions · Vienne · 38 · Auvergne-Rhône-Alpes'), ('Public', 'Artisans, commerçants'), ('Taille', '≈ 800 visiteurs'),
                                 ('Prix', 'Gratuit'), ('Appel à intervenants', 'Oui · limite 05/11/2026'), ('Page de l’événement', '<a href="#">Ouvrir</a>'), ('Inscription', '<a href="#">S’inscrire</a>'),
                                 ('Vérifié', badge('vert', 'Oui', '✓'))]), icone='calendrier')
    org = bloc('Organisateurs', lignes(ligne('<a href="entreprise.html">Union des commerçants de Vienne</a>', 'Association · Vienne<br><a href="#">Site</a> · <a href="#">Formulaire de contact</a> · Contacts : sur la fiche de l’organisateur')), icone='monument')
    lat = _demarche(['Inscrit', 'Repéré', 'Rencontré'], False, [('14/10/2026', 'Événement repéré', 'par Will', 'calendrier', 'gris'), ('20/10/2026', 'Inscrit', 'par Will', 'coche', 'vert'), ('22/10/2026', 'Intervention proposée', 'par Will', 'micro', 'ambre')])
    normal = '<div class="grille deux-un"><div class="pile">%s%s</div><div class="pile">%s</div></div>' % (ev, org, lat)
    P['evenement.html'] = page('evenement', 'Salon des artisans de Vienne', 'Salon · 12/11/2026 · Vienne', normal, erreur=etat_erreur('Événement introuvable.'),
                               actions=btn('← Tous les événements', 'contour', 'evenements.html'), fil=[('Événements', 'evenements.html', 'evenements')], reprise=F + 'evenements/EvenementDetailPage.tsx')


# ======================= CIBLAGE =======================
def _carte_aud(nom, desc, membres, active, maj, href='audience.html'):
    return ('<section class="bloc teinte-%s"><div class="bloc-tete">%s<h2><a href="%s">%s</a></h2>%s</div><p class="petit" style="margin-bottom:12px">%s</p>'
            '<div class="puces-etiq" style="margin-bottom:12px">%s%s</div>%s<p class="petit" style="margin-top:10px">Dernière mise à jour : %s</p>'
            '<div class="bloc-pied">%s%s%s</div></section>' % (
                'vert' if active else 'gris', ic('personnes'), href, E(nom), '<span class="mot">%s</span>' % ('Active' if active else 'Inactive'), E(desc),
                badge('vert', 'Active', '●') if active else badge('gris', 'Inactive', '○'), ' ' + badge('bleu', 'Mise à jour auto', '↻') if active else '',
                chiffres([(membres, 'Membres')]), maj, btn('Actualiser', 'petit-discret', icone='rafraichir', attrs='data-toast="Audience rafraîchie"'),
                btn('Campagne vers cette audience', 'petit', 'campagne-nouvelle.html', 'envoi'), btn('Détails →', 'petit-discret', href)))


def _audiences():
    haut = kpis(kpi('Total audiences', '9', 'personnes', 'bleu', 'segments configurés'), kpi('Actives', '7', 'rafraichir', 'vert', 'mises à jour chaque nuit'),
                kpi('Membres cumul', '24 830', 'stats', 'violet', 'entreprises × audiences'))
    cartes = '<div class="grille trois">%s%s%s%s</div>' % (
        _carte_aud('Prospects contactables', 'Toutes les fiches joignables, hors relations établies.', '21 904', True, 'il y a 6 h'),
        _carte_aud('Organisateurs Rhône-Alpes', 'Organisateurs d’événements en AURA.', '312', True, 'il y a 6 h'),
        _carte_aud('Presse régionale AURA', 'Audience presse : adresses de provenance fiable.', '186', True, 'il y a 6 h'),
        _carte_aud('Ancienne cible 2025', 'Gardée pour mémoire.', '1 204', False, '12/03/2026'))
    normal = haut + cartes
    P['audiences.html'] = page('audiences', 'Audiences', 'Des listes mises à jour <strong>chaque nuit</strong>, prêtes pour un envoi.', normal,
                               etat_vide('personnes', 'Aucune audience pour l’instant', 'Créez une audience pour cibler des entreprises par département, taille ou secteur.', btn('Créer une audience', 'plein', 'audience-nouvelle.html', 'plus')),
                               etat_erreur('Les audiences n’ont pas pu être lues.', 'Le serveur est en panne'),
                               actions=btn('Nouvelle audience', 'plein', 'audience-nouvelle.html', 'plus'), reprise=F + 'audiences/AudiencesListPage.tsx')


def _puces(items, actifs=()):
    return '<div class="filtres" role="group">%s</div>' % ''.join('<button type="button" class="puce" aria-pressed="%s">%s</button>' % ('true' if x in actifs else 'false', E(x)) for x in items)


def _audience_nouvelle():
    def carte(titre, icone, corps, teinte=None):
        return bloc(titre, corps, teinte, icone, mot=None if not teinte else 'Nouveau')
    # Éditeur ET / OU / SAUF (ajout n° 4 du plan 27)
    editeur = carte('Éditeur des critères (ET / OU / SAUF)', 'filtre',
                    '<div class="groupe-criteres"><div class="critere"><span class="operateur">ET</span><select aria-label="Champ"><option>Département</option></select><select aria-label="Opérateur"><option>est l’un de</option></select><input type="text" aria-label="Valeur" value="69, 38, 74"></div>'
                    '<div class="critere"><span class="operateur">ET</span><select aria-label="Champ"><option>Joignabilité</option></select><select aria-label="Opérateur"><option>est</option></select><input type="text" aria-label="Valeur" value="E-mail vérifié valide"></div>'
                    '<div class="groupe-criteres" style="border-color:var(--violet-filet)"><div class="critere"><span class="operateur ou">OU</span><select aria-label="Champ"><option>Étiquettes</option></select><select aria-label="Opérateur"><option>contient</option></select><input type="text" aria-label="Valeur" value="salon-artisans-2026"></div>'
                    '<div class="critere"><span class="operateur ou">OU</span><select aria-label="Champ"><option>Nature d’organisation</option></select><select aria-label="Opérateur"><option>est</option></select><input type="text" aria-label="Valeur" value="Réseau ou club d’affaires"></div></div>'
                    '<div class="critere"><span class="operateur sauf">SAUF</span><select aria-label="Champ"><option>Type de relation</option></select><select aria-label="Opérateur"><option>est l’un de</option></select><input type="text" aria-label="Valeur" value="Clients, Partenaires"></div></div>'
                    '<div class="bloc-pied">%s%s%s</div>' % (btn('+ Critère ET', 'petit'), btn('+ Groupe OU', 'petit'), btn('+ SAUF', 'petit')), 'violet')
    info = carte('Informations', 'etincelle', champ('Nom *', 'au-nom', valeur='Organisateurs Rhône-Alpes', aide='24 / 120') + champ('Description (optionnel)', 'au-desc', 'textarea', 'Pour la campagne d’automne.', aide='0 / 500'))
    geo = carte('Géographie', 'carte', '<p class="lib">Départements</p>' + _puces(['75 Paris', '92 Hauts-de-Seine', '69 Rhône', '38 Isère', '74 Haute-Savoie', '13 Bouches-du-Rhône', '33 Gironde'], ('69 Rhône', '38 Isère', '74 Haute-Savoie'))
                + champ('Pays', 'au-pays', 'select', ['Tous pays', 'France', 'Étranger (hors France)']))
    rel = carte('Relation et joignabilité', 'personnes', '<p class="lib">Types de relation EXCLUS</p><p class="petit">Clients, partenaires, presse, fournisseurs et investisseurs sont exclus par défaut d’une prospection.</p>'
                + _puces(['Prospects', 'Clients', 'Presse & médias', 'Partenaires', 'Investisseurs', 'Fournisseurs'], ('Clients', 'Presse & médias', 'Partenaires', 'Investisseurs', 'Fournisseurs'))
                + '<p class="lib">Joignabilité visée</p>' + _puces(['E-mail vérifié valide (part en campagne)', 'E-mail non vérifié', 'Sans e-mail, avec téléphone'], ('E-mail vérifié valide (part en campagne)',)))
    taille = carte('Taille et secteur', 'entreprise', '<p class="lib">Tailles d’entreprise</p>' + _puces(['TPE', 'PME', 'ETI', 'Grand groupe'], ('TPE', 'PME')))
    qual = carte('Qualité et statut', 'stats', '<p class="lib">Statuts prospection</p>' + _puces(['Contactables (e-mail exploitable)', 'Partiels (e-mail incertain)'], ('Contactables (e-mail exploitable)',))
                 + champ('Score qualité minimum : 50', 'au-score', 'number', '50') + '<label class="case"><input type="checkbox" checked> A au moins un contact avec email</label>')
    dest = carte('Destinataires', 'envoi', '<fieldset style="border:0;padding:0;margin:0"><legend class="lib">À qui écrire dans chaque organisation</legend>'
                 '<label class="case"><input type="radio" name="au-dest" checked> La personne nommée, sinon l’adresse générique</label><label class="case"><input type="radio" name="au-dest"> L’adresse générique seulement</label>'
                 '<label class="case"><input type="radio" name="au-dest"> Les personnes nommées seulement</label><label class="case"><input type="radio" name="au-dest"> Les deux</label></fieldset>'
                 '<p class="lib">Fonctions des personnes (facultatif)</p>' + _puces(['Président', 'Dirigeant', 'Directeur général', 'Délégué général', 'Secrétaire général', 'Gérant', 'Chargé des événements'], ('Président', 'Chargé des événements')))
    etiq = carte('Étiquettes personnalisées', 'diese', champ('Étiquettes, séparées par une virgule ou une espace', 'au-etiq', attrs='placeholder="ex : decisionnaire, growth, fintech"'))
    apercu = bloc('Aperçu en direct', chiffres([('312', 'Entreprises'), ('348', 'Contacts')]) + mini_titre('Destinataires (rien n’est envoyé)')
                  + chiffres([('290', 'Adresses distinctes'), ('276', 'Organisations'), ('41', 'Génériques'), ('249', 'Nominatives')])
                  + mini_titre('Exclues (22)') + lignes(ligne('Ne plus écrire (opposition ou suppression)', '9', '', badge('rouge', '9', '■')), ligne('Adresse personnelle (gmail…)', '8', '', badge('ambre', '8', '▲')),
                                                        ligne('Entreprise fermée selon l’INSEE', '5', '', badge('gris', '5', '○')))
                  + mini_titre('Critères (5)') + '<p class="mono">ET département ∈ 69,38,74<br>ET joignabilité = vérifiée<br>OU étiquette = salon-artisans-2026<br>SAUF relation ∈ clients</p>',
                  'bleu', 'oeil', mot='Direct', pied=btn('Créer l’audience', 'plein', icone='coche', attrs='data-toast="Audience créée"') + btn('Annuler', 'petit-discret', 'audiences.html'))
    normal = '<div class="assistant"><div class="pile">%s%s%s%s%s%s%s%s</div><aside class="recap">%s</aside></div>' % (editeur, info, geo, rel, taille, qual, dest, etiq, apercu)
    P['audience-nouvelle.html'] = page('audience-nouvelle', 'Nouvelle audience', 'Le nombre de fiches se met à jour <strong>à chaque choix</strong>.', normal,
                                       fil=[('Audiences', 'audiences.html', 'audiences')], reprise=F + 'audiences/AudienceBuilderPage.tsx (+ éditeur ET / OU / SAUF : ajout plan 27 n° 4)')


def _audience():
    haut = kpis(kpi('Membres', '312', 'personnes', 'bleu', 'entreprises + contacts'), kpi('Dernière mise à jour', 'il y a 6 h', 'horloge', 'vert', 'chaque nuit à 4 h'),
                kpi('Statut', 'Active', 'coche', 'vert', 'mise à jour chaque nuit'), kpi('Mise à jour auto', 'Oui', 'rafraichir', 'bleu', 'chaque jour'))
    membres = tableau('Membres', ['Entreprise', 'Dépt', 'Taille', 'Secteur', 'Contact email'], [
        [_e('Comité des fêtes de Vienne'), '<span class="mono">38</span>', 'TPE', 'Culture, sport et loisirs', 'Martine Lenoir · contact@cdf-vienne.example'],
        [_e('Union des commerçants de Vienne'), '<span class="mono">38</span>', 'TPE', 'Commerce de détail', 'Pierre Dumas · bureau@ucv.example'],
        [_e('Club entreprises Annecy'), '<span class="mono">74</span>', 'TPE', 'Services aux entreprises', '<em>aucun email</em>']], liens=['entreprise.html'] * 3, secondaires=(1, 3))
    crit = bloc('Critères de l’audience', lignes(ligne('<strong>Département</strong> : 69, 38, 74', 'AU MOINS UN DE'), ligne('<strong>Joignabilité</strong> : E-mail vérifié valide', ''),
                                                  ligne('<strong>Type de relation</strong> : Clients, Partenaires', 'SAUF')), icone='filtre', pied=btn('Modifier les critères', 'petit', 'audience-nouvelle.html', 'filtre'))
    prep = bloc('Préparation campagne', '<p>Cette audience part dans le produit <strong>Envoi</strong> en un clic, liste figée au lancement.</p>', 'violet', 'envoi', mot='Envoi',
                pied=btn('Campagne vers cette audience', 'plein', 'campagne-nouvelle.html', 'envoi'))
    dest = bloc('Aperçu (rien n’est envoyé)', chiffres([('290', 'Adresses distinctes'), ('276', 'Organisations'), ('41', 'Génériques'), ('249', 'Nominatives')]), icone='oeil')
    normal = haut + onglets('Audience', [('m', 'Membres <span class="nb">312</span>', membres + '<p class="petit" style="margin-top:10px">Affichage des 100 premiers membres.</p>'),
                                         ('d', 'Destinataires', dest), ('c', 'Critères <span class="nb">3</span>', crit), ('p', 'Préparation campagne', prep)])
    P['audience.html'] = page('audience', 'Organisateurs Rhône-Alpes', 'Organisateurs d’événements en AURA · ' + badge('vert', 'Active', '●'), normal,
                              erreur=etat_erreur('Cette audience n’a pas pu être lue.'),
                              actions=btn('Mettre à jour', 'contour', icone='rafraichir', attrs='data-toast="Audience rafraîchie"') + btn('Exporter CSV', 'contour', icone='export', attrs='data-toast="312 membres exportés (ajout plan 27)."')
                              + '<button type="button" class="btn btn-danger" data-toast="Audience supprimée">Supprimer</button>',
                              fil=[('Audiences', 'audiences.html', 'audiences')], reprise=F + 'audiences/AudienceDetailPage.tsx')


def _e(n):
    return '<div class="cellule-personne">%s<a href="entreprise.html">%s</a></div>' % (initiales(n, 'gris'), E(n))


def _listes():
    creer = bloc('Créer une liste', '<div class="ligne-champs">%s%s</div>' % (champ('Nom de la liste', 'l-nom', attrs='placeholder="Ex. : Invités salon des artisans"'), champ('Description (facultative)', 'l-desc', attrs='placeholder="Pour quelle campagne ?"')),
                 'bleu', 'plus', mot='Nouvelle', pied=btn('Créer la liste', 'plein', icone='plus', attrs='data-toast="Liste « Invités salon » créée."'))
    L = [('Invités salon des artisans', 'Pour la campagne d’automne', '86', '41', '28/10/2026'), ('Partenaires presse', '', '12', '19', '15/10/2026'), ('Exclusions clients', 'À exclure de toute prospection', '86', '0', '02/10/2026')]
    lig = [['<a href="liste.html"><strong>%s</strong></a><span class="sous">%s</span>' % (E(n), E(d)), o, p, m, btn('Exporter', 'petit-discret', attrs='data-toast="Liste exportée en CSV (ajout plan 27)."')] for n, d, o, p, m in L]
    corbeille = tableau('Corbeille', ['Liste', 'Organisations', 'Personnes', 'Modifiée', ''], [['Ancienne liste salon 2025', '40', '12', '01/03/2026', btn('Sortir de la corbeille', 'petit-discret', attrs='data-toast="Liste sortie de la corbeille."')]])
    normal = creer + onglets('Listes', [('l', 'Listes <span class="nb">3</span>', tableau('Listes', ['Liste', 'Organisations', 'Personnes', 'Modifiée', ''], lig, liens=['liste.html'] * 3)), ('c', 'Corbeille <span class="nb">1</span>', corbeille)])
    P['listes.html'] = page('listes', 'Listes', 'Des fiches choisies <strong>à la main</strong>, sous un nom.', normal,
                            etat_vide('liste-cochee', 'Aucune liste pour l’instant', 'Créez une liste, puis cochez des fiches dans Entreprises ou Contacts, ou importez un fichier.', ''),
                            etat_erreur('Les listes manuelles n’ont pas pu être lues.'), reprise=F + 'listes/ListesManuellesPage.tsx')


def _liste():
    imp = bloc('Importer un fichier', '<p style="margin-bottom:12px">CSV ou JSONL : une ligne par fiche — SIREN, identifiant CRM ou adresse e-mail <strong>déjà présente</strong> dans le CRM. Rien n’est jamais créé.</p>'
               + champ('Fichier', 'li-f', valeur='invites-salon-factice.csv')
               + '<div class="bandeau bleu" style="margin:0">%s<span><strong>Analyse (rien n’a été écrit)</strong> · 120 lignes lues, 112 rapprochées · rejetées : 6 absentes du CRM, 2 illisibles</span></div>' % ic('aide'),
               'bleu', 'fichier', mot='Import', pied=btn('Analyser (rien n’est écrit)', 'contour') + btn('Importer 112 lignes', 'plein', icone='collecte', attrs='data-toast="112 lignes rapprochées, 8 rejetées."'))
    masse = barre_masse('2 cochées', btn('Retirer de la liste', 'petit', attrs='data-toast="2 fiches retirées de la liste — les fiches elles-mêmes sont intactes."') + btn('Annuler la sélection', 'petit'))
    t = tableau('Membres', ['Fiche', 'Organisation', 'Adresse', 'Ajoutée'], [
        ['<div class="cellule-personne"><input type="checkbox" checked aria-label="Cocher">%s<span>Paul Morin · Gérant</span></div>' % ic('personne'), '<a href="entreprise.html">Boulangerie des Tilleuls</a>', '<span class="mono">paul@boulangerie-tilleuls.example</span>', 'cochée le 28/10/2026'],
        ['<div class="cellule-personne"><input type="checkbox" checked aria-label="Cocher">%s<span>Organisation</span></div>' % ic('entreprise'), '<a href="entreprise.html">Garage des Saules</a>', '<span class="mono">contact@garage-saules.example</span>', 'importée le 27/10/2026'],
        ['<div class="cellule-personne"><input type="checkbox" aria-label="Cocher">%s<span>Nadia Haddad · Directrice</span></div>' % ic('personne'), '<a href="entreprise.html">Imprimerie du Lac</a>', '—', 'cochée le 26/10/2026']], secondaires=(2,))
    normal = imp + masse + bloc('Membres', t + pagination('Page 1 / 3 — 127 fiches', False), icone='liste-cochee')
    P['liste.html'] = page('liste', 'Invités salon des artisans', '<strong>86 organisations</strong> · 41 personnes', normal, erreur=etat_erreur('Cette liste n’a pas pu être lue.'),
                           actions=btn('Renommer', 'contour', icone='note') + btn('Exporter CSV', 'contour', icone='export', attrs='data-toast="127 fiches exportées (ajout plan 27)."')
                           + btn('Campagne vers cette liste', 'contour', 'campagne-nouvelle.html', 'envoi') + '<button type="button" class="btn btn-danger" data-toast="Liste mise à la corbeille (elle peut en sortir).">Corbeille</button>',
                           fil=[('Listes', 'listes.html', 'listes')], reprise=F + 'listes/ListeManuelleDetailPage.tsx')


# ======================= ALIMENTER LA BASE =======================
STAT = {'En cours': ('bleu', '▶'), 'En pause': ('ambre', '❚❚'), 'Terminée': ('vert', '✓'), 'Planifiée': ('violet', '◷'), 'Brouillon': ('gris', '○'), 'Échec': ('rouge', '■')}


def _collectes():
    def carte(nom, desc, st, sources, zones, cr, mx, du, dmx, raison=''):
        t, s = STAT[st]
        pied = {'En cours': btn('Pause', 'petit-discret', icone='pause', attrs='data-toast="Collecte mise en pause"') + btn('Annuler', 'petit-discret', attrs='data-toast="Collecte annulée"'),
                'En pause': btn('Reprendre', 'petit-discret', icone='lecture', attrs='data-toast="Collecte reprise"')}.get(st, '')
        return ('<section class="bloc teinte-%s"><div class="bloc-tete">%s<h2><a href="collecte.html">%s</a></h2>%s</div><p class="petit">%s</p>'
                '<div class="puces-etiq" style="margin:10px 0">%s</div><div class="puces-etiq" style="margin-bottom:12px">%s</div>%s<div style="margin-top:10px">%s</div>'
                '<div class="bloc-pied">%s%s</div></section>' % (t, ic('campagne'), E(nom), badge(t, st + raison, s), E(desc),
                                                              ''.join('<span class="puce-etiq">%s</span>' % x for x in sources), ''.join('<span class="badge bleu" data-s="◉">%s</span>' % z for z in zones),
                                                              jauge('Entreprises', cr, mx, 'vert' if st == 'En cours' else 'bleu', '%s / %s' % (cr, mx)), jauge('Durée', du, dmx, 'bleu', '%d / %d min' % (du, dmx)),
                                                              pied, btn('Voir détails →', 'petit-discret', 'collecte.html')))
    haut = kpis(kpi('Total', '14', 'campagne', 'bleu', 'collectes'), kpi('En cours', '1', 'lecture', 'violet', '+ 1 en pause'),
                kpi('Terminées', '11', 'coche', 'vert', 'succès complets'), kpi('Entreprises créées', '9 870', 'entreprise', 'ambre', 'cumul toutes collectes'))
    barre = (filtres(['Toutes · 14', 'Brouillons · 1', 'Planifiées · 0', 'En cours · 1', 'En pause · 1', 'Terminées · 11'])
             + filtres_champs([('r', 'Recherche', 'Rechercher par nom…', 'co-q'), ('c', 'Afficher les collectes archivées', '', 'co-arch')]))
    cartes = '<div class="grille trois">%s%s%s</div>' % (
        carte('Rhône — PME artisanat', 'Semaine 44', 'En cours', ['INSEE Sirene', 'France Travail'], ['Dépt 69'], 620, 1000, 132, 180),
        carte('Isère — commerces', 'Avant le salon', 'En pause', ['INSEE Sirene'], ['Dépt 38'], 400, 400, 60, 180, ' · Quota entreprises atteint'),
        carte('Savoie — tourisme', 'Saison d’hiver', 'Terminée', ['INSEE Sirene', 'Annuaire entreprises', 'BAN géocodage'], ['Dépt 73', 'Dépt 74'], 850, 1000, 170, 180))
    normal = '<div class="bandeau bleu">%s<span>En direct · Mis à jour toutes les 10 secondes</span></div>' % ic('rafraichir') + haut + barre + cartes
    P['collectes.html'] = page('collectes', 'Collectes', 'Vos collectes d’entreprises.', normal,
                               etat_vide('campagne', 'Aucune collecte pour l’instant', 'Aucune collecte pour l’instant.', btn('Créer une collecte', 'plein', 'collecte-nouvelle.html', 'plus')),
                               etat_erreur('Les collectes n’ont pas pu être lues.'), actions=btn('Nouvelle collecte', 'plein', 'collecte-nouvelle.html', 'plus'),
                               reprise=F + 'campaigns/CampaignsListPage.tsx (route /campaigns → /collectes)')


def _collecte_nouvelle():
    et = ['Identité', 'Zones', 'Sources', 'Budget & sécurité']

    def etape(n, titre, icone, corps, aide, dernier=False):
        pied = ('<button type="button" class="btn btn-plein" data-aller="%d">Continuer %s</button>' % (n + 1, ic('fleche'))) if not dernier else (
            btn('Créer en brouillon', 'contour', attrs='data-toast="Collecte créée en brouillon"') + '<a class="btn btn-plein" href="collecte.html" data-toast="Collecte lancée">%sCréer et lancer</a>' % ic('etincelle'))
        pied += ('<button type="button" class="btn btn-contour" data-aller="%d">Précédent</button>' % (n - 1)) if n > 1 else btn('Annuler', 'contour', 'collectes.html')
        return ('<section class="bloc teinte-bleu" data-etape="%d" aria-label="Étape %d"><div class="bloc-tete">%s<h2>%s</h2><span class="mot">Étape %d sur 4</span></div><p class="petit" style="margin-bottom:14px">%s</p>%s<div class="bloc-pied">%s</div></section>'
                % (n, n, ic(icone), E(titre), n, E(aide), corps, pied))
    e1 = etape(1, 'Identité', 'note', champ('Nom de la collecte *', 'cn-nom', valeur='Rhône — PME artisanat', aide='21 / 120') + champ('Description (optionnel)', 'cn-desc', 'textarea', 'Notes internes pour l’équipe')
               + '<div class="filtres" role="group" aria-label="Planification" data-unique><button type="button" class="puce" aria-pressed="true">Lancer maintenant</button><button type="button" class="puce" aria-pressed="false">Planifier plus tard</button></div>',
               'Nom et description visibles dans la liste des collectes.')
    e2 = etape(2, 'Zones cibles', 'carte', filtres(['Départements', 'Régions', 'Villes']) + champ('Rechercher un dépt…', 'cn-z', 'search')
               + '<div class="bandeau bleu">%s<span><strong>2 zones sélectionnées</strong> · ~4 120 entreprises connues</span></div>' % ic('carte')
               + _puces(['01 Ain ~1 240', '38 Isère ~2 980', '69 Rhône ~4 120', '73 Savoie ~1 010', '74 Haute-Savoie ~1 330'], ('69 Rhône ~4 120', '38 Isère ~2 980')), 'Choisissez les zones à couvrir.')
    e3 = etape(3, 'Sources de découverte', 'collecte', '<div class="choix"><label><span class="choix-tete"><input type="checkbox" checked><strong>INSEE Sirene</strong></span><span>Base officielle entreprises FR (~30M entreprises légales)</span>%s</label>'
               '<label><span class="choix-tete"><input type="checkbox"><strong>France Travail</strong></span><span>Entreprises qui recrutent dans la zone : signe d’un besoin</span>%s</label></div>'
               % (badge('ambre', 'Clé d’accès requise', '▲'), badge('ambre', 'Clé d’accès requise', '▲'))
               + '<div class="bandeau bleu">%s<span><strong>Enrichissement automatique.</strong> Annuaire Entreprises, BODACC, BAN géocodage, mentions légales des sites, Google Places, IA : elles tournent toutes seules.</span></div>' % ic('etincelle'),
               'Au moins une source obligatoire.')
    e4 = etape(4, 'Budget et sécurité anti-blacklist', 'bouclier', '<div class="ligne-champs">%s%s%s</div>' % (
        champ('Entreprises max', 'cn-max', 'number', '1000', '1 — 50 000'), champ('Durée max (minutes)', 'cn-dur', 'number', '180', '5 — 1440 (24h)'), champ('Débit max', 'cn-deb', 'number', '30', '30 req/min'))
        + '<div class="bandeau vert">%s<span><strong>Budget estimé</strong> : jusqu’à 1 000 entreprises sur 3h00, à 30 req/min.</span></div>' % ic('coche'), 'Trois garde-fous : volume max, temps max, débit max.', True)
    normal = '<div data-assistant>%s%s%s%s%s</div>' % (frise(et, 1), e1, e2, e3, e4)
    P['collecte-nouvelle.html'] = page('collecte-nouvelle', 'Nouvelle collecte', 'Quatre étapes : <strong>nom, zones, sources, limites</strong>.', normal,
                                       fil=[('Collectes', 'collectes.html', 'collectes')], reprise=F + 'campaigns/CampaignWizardPage.tsx')


def _collecte():
    haut = kpis(kpi('Entreprises créées', '620', 'entreprise', 'vert', '+4,7/min'), kpi('Passages', '41/66', 'rafraichir', 'bleu', '62 % terminés', graph=jauge('Passages', 41, 66, 'bleu', '62 %')),
                kpi('Débit max', '30/min', 'sante', 'gris', 'anti-blacklist'), kpi('ETA fin', '0h 48m', 'horloge', 'violet', 'estimation'))
    prog = '<div class="grille deux">%s%s</div>' % (bloc('Entreprises créées', jauge('Entreprises', 620, 1000, 'vert', '620 / 1 000 (62 %)'), icone='entreprise'), bloc('Temps écoulé', jauge('Temps', 132, 180, 'bleu', '132 / 180 min (73 %)'), icone='horloge'))
    suivi = chrono([('10:42:10', 'INSEE Sirene · réussi', 'Passage n° 4412 →', 'coche', 'vert'), ('10:41:52', 'France Travail · en cours', 'Passage n° 4411 →', 'rafraichir', 'bleu'), ('10:40:03', 'INSEE Sirene · échec (délai dépassé)', 'Passage n° 4410 →', 'croix', 'rouge')])
    sources = tableau('Sources', ['Source', 'Statut', 'Passages', 'Succès', 'Échecs', 'Entreprises'], [['INSEE Sirene', badge('bleu', 'En cours', '▶'), '38', '36', '2', '590'], ['France Travail', badge('vert', 'Terminé', '✓'), '3', '3', '0', '30']])
    zones = tableau('Zones', ['Type', 'Code', 'Libellé'], [['Département', '<span class="mono">69</span>', 'Rhône']])
    conf = bloc('Configuration de la collecte', dl([('Nom', 'Rhône — PME artisanat'), ('Statut', 'En cours'), ('Sources', 'INSEE Sirene, France Travail'), ('Zones', '1 zone'), ('Max entreprises', '1 000'),
                                                    ('Max durée (min)', '180'), ('Max req/min', '30'), ('Démarrée', '01/11/2026 08:30')]), icone='reglages', pied=btn('Dupliquer', 'petit', 'collecte-nouvelle.html', 'copie'))
    normal = prog + haut + onglets('Collecte', [('s', 'Suivi temps réel', suivi), ('so', 'Sources', sources), ('z', 'Zones', zones), ('p', 'Passages', '<p>Voir <a href="historique-collectes.html">l’historique des collectes</a>.</p>'), ('c', 'Configuration', conf)])
    P['collecte.html'] = page('collecte', 'Rhône — PME artisanat', 'Lancée il y a 2 h · 132 min écoulées · reste 48 min · <strong>620/1 000 entreprises</strong>', normal,
                              erreur=etat_erreur('Cette collecte n’a pas pu être lue.'), actions=btn('Pause', 'contour', icone='pause', attrs='data-toast="Collecte mise en pause"') + btn('Annuler', 'petit-discret', attrs='data-toast="Collecte annulée"'),
                              fil=[('Collectes', 'collectes.html', 'collectes')], reprise=F + 'campaigns/CampaignDetailPage.tsx')


# Carte de France stylisée : 13 régions (polygones simplifiés, pas une carte exacte)
REGIONS = [('Hauts-de-France', 'M250 20 L330 30 L340 95 L265 105 L235 70Z', 4), ('Normandie', 'M120 70 L235 70 L265 105 L230 140 L130 130Z', 3),
           ('Île-de-France', 'M265 105 L320 110 L320 150 L270 155 L245 135Z', 4), ('Grand Est', 'M340 95 L330 30 L420 60 L460 120 L430 190 L340 170 L320 110Z', 3),
           ('Bretagne', 'M20 120 L130 130 L130 175 L40 180Z', 2), ('Pays de la Loire', 'M130 130 L230 140 L215 210 L140 230 L130 175Z', 2),
           ('Centre-Val de Loire', 'M230 140 L245 135 L270 155 L320 150 L320 210 L265 250 L215 210Z', 2), ('Bourgogne-Franche-Comté', 'M320 150 L340 170 L430 190 L420 250 L330 270 L320 210Z', 2),
           ('Nouvelle-Aquitaine', 'M140 230 L215 210 L265 250 L270 330 L210 410 L150 400 L165 300Z', 1), ('Auvergne-Rhône-Alpes', 'M265 250 L320 210 L330 270 L420 250 L440 330 L370 360 L280 340 L270 330Z', 4),
           ('Occitanie', 'M210 410 L270 330 L280 340 L370 360 L350 420 L270 450 L220 440Z', 1), ('Provence-Alpes-Côte d’Azur', 'M370 360 L440 330 L470 380 L420 420 L350 420Z', 2),
           ('Corse', 'M470 420 L490 425 L492 480 L475 490 L465 450Z', 0)]
TEINTES = ['#e7ebf2', '#c9d6fb', '#93aef5', '#5277e9', '#1d4ed8']


def _carte_svg():
    p = ''.join('<path d="%s" fill="%s"><title>%s</title></path>' % (d, TEINTES[n], E(r)) for r, d, n in REGIONS)
    leg = '<div class="legende" aria-hidden="true">%s</div>' % ''.join('<span><i style="background:%s;border:1px solid var(--cadre)"></i>%s</span>' % (TEINTES[i], l) for i, l in enumerate(['aucune', 'moins de 500', '500 à 2 000', '2 000 à 5 000', '5 000 et plus']))
    return '<svg class="carte-france" viewBox="0 0 500 500" role="img" aria-label="Carte de France : entreprises par région. Auvergne-Rhône-Alpes, Île-de-France et Hauts-de-France en tête.">%s</svg>%s' % (p, leg)


def _carte_france():
    haut = kpis(kpi('Couverture', '41 %', 'carte', 'bleu', '40 / 101 dépts', graph=jauge('Couverture', 41, 100, 'bleu', '41 %')),
                kpi('Entreprises trouvées', '48 212', 'entreprise', 'violet', 'dont 31 004 au score ≥ 50'), kpi('Niveau', 'Départements', 'liste', 'ambre', '101 zones'))
    barre = '<div class="barre-outils">%s<span class="petit" style="margin-left:auto">48 212 entreprises au total</span></div>' % filtres(['Régions', 'Départements', 'Villes'])
    sel = bloc('Sélection', '<p style="margin-bottom:12px"><span class="badge gris" data-s="■">69</span> <strong>Rhône</strong></p>' + chiffres([('4 120', 'Entreprises'), ('2 870', 'Score ≥ 50')])
               + '<p style="margin-top:12px"><a href="entreprises.html">Voir les entreprises de ce département</a></p><p class="petit" style="margin-top:8px">Étape 1 : récupérer les entreprises. Étape 2 : les enrichir.</p>',
               'bleu', 'cible', mot='Rhône', pied=btn('Récupérer 100 entreprises de ce département', 'plein', icone='collecte', attrs='data-ouvre="fen-recup"') + btn('Enrichir (emails · téléphones · dirigeants)', 'petit', icone='etincelle'))
    top = bloc('Top zones', lignes(*[ligne('<span class="badge gris" data-s="■">%s</span> %s' % (c, n), '', '', '<strong class="chiffre">%s</strong>' % v) for c, n, v in
                                    [('69', 'Rhône', '4 120'), ('38', 'Isère', '2 980'), ('74', 'Haute-Savoie', '1 330'), ('01', 'Ain', '1 240'), ('73', 'Savoie', '1 010')]]), icone='stats')
    normal = '<div class="bandeau vert">%s<span>Mis à jour chaque minute</span></div>' % ic('rafraichir') + haut + barre + '<div class="grille deux-un">%s<div class="pile">%s%s</div></div>' % (bloc('Entreprises par zone', _carte_svg(), icone='carte'), sel, top)
    fen = fenetre('fen-recup', 'Récupérer 100 entreprises ?', '<p><strong>Département : Rhône (69)</strong></p><p style="margin-top:8px">La collecte va chercher 100 entreprises auprès des services publics. Elle se poursuit en arrière-plan.</p>',
                  '<button type="button" class="btn btn-contour" data-ferme>Annuler</button><button type="button" class="btn btn-plein" data-ferme data-toast="Récupération lancée : Rhône (69)">Confirmer</button>')
    P['carte-france.html'] = page('carte-france', 'Carte de France', 'Cliquez sur un département pour voir <strong>ses entreprises</strong>.', normal,
                                  erreur=etat_erreur('La couverture de la France n’a pas pu être lue.'), apres=fen, reprise=F + 'coverage/CoveragePage.tsx (+ FranceCoverageMap.tsx)')


for _f in (_index, _taches, _affaires, _federations, _federation, _evenements, _evenement, _audiences, _audience_nouvelle, _audience, _listes, _liste,
           _collectes, _collecte_nouvelle, _collecte, _carte_france):
    _f()
