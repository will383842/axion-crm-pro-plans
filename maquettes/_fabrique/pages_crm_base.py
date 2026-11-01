# -*- coding: utf-8 -*-
"""Lot M1 · produit CRM Pro : Presse, À traiter, Ma base.

Chaque page REPREND le composant réel (chemin noté en tête de page) : mêmes titres,
colonnes, filtres, actions et textes, dans le nouveau style ; les ajouts du plan 27
viennent ensuite. Données factices (aucun vrai nom, domaines en .example).
"""
from socle import *  # noqa: F401,F403

P = {}
F = 'frontend/src/features/'


def _cel_nom(nom, href, sous='', teinte='bleu'):
    return '<div class="cellule-personne">%s<div><a href="%s">%s</a>%s</div></div>' % (
        initiales(nom, teinte), href, E(nom), ('<span class="sous">%s</span>' % sous) if sous else '')


CONF = {'A': ('vert', 'A'), 'B': ('bleu', 'B'), 'C': ('ambre', 'C')}


def _conf(x):
    t, m = CONF[x]
    return badge(t, m, '●')


# ======================= PRESSE =======================
MEDIAS = [('Le Courrier du Rhône', 'Journal', '69', 'Lyon', True, 'redaction@courrier-rhone.example', 'A', '04 00 00 11 20'),
          ('Radio Vallée FM', 'Radio', '38', 'Grenoble', True, 'antenne@radio-vallee.example', 'A', '04 00 00 22 31'),
          ('L’Écho des Alpes', 'Revue / périodique', '74', 'Annecy', False, 'echo.alpes@messagerie.example', 'C', '04 00 00 33 42'),
          ('Hebdo Loire Infos', 'Journal', '42', 'Saint-Étienne', True, 'contact@hebdo-loire.example', 'B', '04 00 00 44 53'),
          ('TV Sud-Est', 'Télévision', '13', 'Marseille', True, 'redac@tv-sudest.example', 'A', '04 00 00 55 64'),
          ('Agence Presse Régions', 'Agence de presse', '75', 'Paris', True, 'desk@apr.example', 'B', '01 00 00 66 75'),
          ('Portail Éco Lyon', 'Portail / site d’information', '69', 'Villeurbanne', False, '—', '', '—'),
          ('Le Journal des Artisans', 'Revue / périodique', '01', 'Bourg-en-Bresse', True, 'info@journal-artisans.example', 'B', '04 00 00 77 86')]


def _medias():
    lig = []
    for n, t, d, v, ok, mail, c, tel in MEDIAS:
        site = ('<a href="#">%s</a>' % n.lower().replace(' ', '-').replace('’', '')[:16] + '.example') if ok else '<span class="ancien">site deviné</span> <span class="sous">· non vérifié</span>'
        lig.append([_cel_nom(n, 'media.html'), E(t), '<span class="mono">%s</span>' % d, E(v), site, E(mail), _conf(c) if c else '—', '<span class="mono">%s</span>' % tel])
    haut = kpis(kpi('Total', '1 284', 'presse', 'bleu', 'Page 1 · 100 affichés'),
                kpi('Avec site vérifié', '71 %', 'domaine', 'violet', '912 sur 1 284', graph=jauge('Site vérifié', 71, 100, 'violet', '71 %')),
                kpi('Avec email', '64 %', 'message', 'vert', '822 sur 1 284', graph=jauge('Avec email', 64, 100, 'vert', '64 %')),
                kpi('Type le plus fréquent', 'Journal', 'stats', 'ambre', '486 médias · mis à jour 07:10'))
    f = filtres_champs([('r', 'Recherche', 'Rechercher un média…', 'm-q'),
                        ('s', 'Famille', ['Médias', 'Sociétés de production', 'Médias et sociétés de production'], 'm-fam'),
                        ('s', 'Type', ['Tous types', 'Journal', 'Revue / périodique', 'Autre presse', 'Radio', 'Télévision', 'Émission de télévision', 'Agence de presse', 'Portail / site d’information', 'Blog', 'Production audiovisuelle'], 'm-type'),
                        ('s', 'Périodicité', ['Toute périodicité', 'Quotidien', 'Hebdomadaire', 'Mensuel', 'Bimensuel', 'Trimestriel'], 'm-per'),
                        ('s', 'Site web', ['Site : tous', 'Avec site vérifié', 'Sans site vérifié'], 'm-site'),
                        ('s', 'E-mail', ['Email : tous', 'Avec email', 'Sans email'], 'm-mail'),
                        ('s', 'Fiabilité de l’e-mail', ['Confiance : toutes', 'A · email = domaine du site', 'B · domaine pro', 'C · boîte grand public'], 'm-conf'),
                        ('t', 'Département', 'ex. 75', 'm-dep')])
    t = tableau('Médias', ['Média', 'Type', 'Dept', 'Ville', 'Site', 'Email', 'Conf.', 'Téléphone'], lig, liens=['media.html'] * len(lig), secondaires=(2, 4, 7))
    normal = haut + f + t + pagination('Page 1 / 13 · 1 284 médias', False)
    P['medias.html'] = page('medias', 'Médias', 'Base médias &amp; presse · <strong>1 284</strong> médias', normal,
                            etat_vide('presse', 'Aucun média', 'Aucun média pour l’instant.', ''),
                            etat_erreur('La liste des médias n’a pas pu être lue. Rien n’est perdu.'),
                            actions=btn('Exporter CSV', 'plein', icone='export', attrs='data-toast="Export CSV téléchargé"'),
                            reprise=F + 'media/MediaListPage.tsx')


NATURES = ['Communiqué envoyé', 'Relance', 'Réponse reçue', 'Retombée publiée', 'Message LinkedIn', 'Appel']


def _journal_presse(vide_txt, items):
    consigner = bloc('Consigner un échange', champ('Nature', 'jp-nat', 'select', NATURES) + champ('En une ligne', 'jp-titre', attrs='placeholder="En une ligne : ce qui s’est passé"')
                     + champ('Détail', 'jp-det', 'textarea', attrs='placeholder="Détail (facultatif)" rows="3"'),
                     'bleu', 'note', mot='Saisie', pied=btn('Consigner', 'contour', icone='coche', attrs='data-toast="Échange consigné"'))
    hist = bloc('Historique · %d' % len(items), chrono(items) if items else '<p class="petit">%s</p>' % vide_txt, icone='horloge')
    return '<div class="grille deux">%s%s</div>' % (consigner, hist)


def _media():
    tete = '<div class="fiche-tete">%s<div class="meta">%s<span>Chaîne : <a href="#">Groupe Rhône Médias</a></span>%s<span>Fiche CRM : <a href="entreprise.html">voir la fiche</a></span></div></div>' % (
        initiales('Courrier Rhône', 'bleu').replace('initiales ', 'initiales grand '), badge('gris', 'Journal', '■'), badge('vert', 'enrichissement : réussi', '✓'))
    info = bloc('Informations', dl([('Type', 'Journal'), ('Famille', 'Rédactionnel'), ('Périodicité', 'Quotidien'), ('Thème éditorial', 'Actualité régionale'),
                                   ('Zone de diffusion', 'Rhône, Ain'), ('Éditeur', 'Éditions du Confluent (factice)'), ('Département', '69'), ('Région', 'Auvergne-Rhône-Alpes'),
                                   ('Ville', 'Lyon'), ('Code postal', '69002'), ('SIREN', '<span class="mono">000 000 001</span>'), ('N° CPPAP', '0000 C 00001'),
                                   ('N° ARCOM', '—'), ('Source', 'Annuaire presse (import)')]), icone='presse')
    contact_ = bloc('Contact rédaction', dl([('Site web', '<a href="#">courrier-rhone.example</a>'), ('Email rédaction', 'redaction@courrier-rhone.example ' + badge('vert', 'Confiance A', '●')),
                                            ('Téléphone', '<span class="mono">04 00 00 11 20</span>')], False), 'vert', 'message', mot='Diffusable')
    jl = tableau('Journalistes', ['Nom', 'Rôle', 'Rubrique', 'Email'], [
        [_cel_nom('Léa Fournier', 'journaliste.html'), 'Rédactrice en chef', 'Économie', 'l.fournier@courrier-rhone.example'],
        [_cel_nom('Bruno Lacombe', 'journaliste.html'), 'Journaliste', 'Société', 'b.lacombe@courrier-rhone.example'],
        [_cel_nom('Anaïs Perrin', 'journaliste.html', '', 'gris'), 'Pigiste', 'Culture', '<span class="badge rouge" data-s="■">opposé aux envois</span>']], liens=['journaliste.html'] * 3, secondaires=(2,))
    journ = _journal_presse('Aucun échange consigné avec cette rédaction — ni avec ses journalistes.', [
        ('02 oct. 2026', 'Communiqué : salon des artisans', 'Communiqué envoyé · via Will', 'envoi', 'bleu'),
        ('05 oct. 2026', 'Relance téléphonique', 'Relance · via Will', 'telephone', 'ambre'),
        ('09 oct. 2026', 'Article en page 6', 'Retombée publiée · via Léa Fournier', 'presse', 'vert')])
    lies = bloc('Émissions / médias liés (2)', '<div class="puces-etiq"><a class="puce-etiq" href="#">Courrier du Dimanche</a><a class="puce-etiq" href="#">Courrier Éco</a></div>', icone='lien')
    normal = tete + '<div class="grille deux-un">%s%s</div>' % (info, contact_) + bloc('Journalistes (3)', jl, icone='micro') + journ + lies
    P['media.html'] = page('media', 'Le Courrier du Rhône', 'Quotidien régional · <strong>3 journalistes</strong> · confiance A', normal,
                           erreur=etat_erreur('Ce média n’existe pas ou a été supprimé.', 'Média introuvable'), fil=[('Médias', 'medias.html', 'medias')],
                           reprise=F + 'media/MediaDetailPage.tsx')


def _journalistes():
    J = [('Léa Fournier', 'Le Courrier du Rhône', 'Rédactrice en chef', 'Économie', 'l.fournier@courrier-rhone.example'),
         ('Bruno Lacombe', 'Le Courrier du Rhône', 'Journaliste', 'Société', 'b.lacombe@courrier-rhone.example'),
         ('Samir Benali', 'Radio Vallée FM', 'Animateur', 'Matinale', 's.benali@radio-vallee.example'),
         ('Chloé Vasseur', 'TV Sud-Est', 'Reporter', 'Économie locale', 'c.vasseur@tv-sudest.example'),
         ('Anaïs Perrin', 'Le Courrier du Rhône', 'Pigiste', 'Culture', 'opposé aux envois'),
         ('Thomas Girard', 'Hebdo Loire Infos', 'Chef d’édition', 'Entreprises', 't.girard@hebdo-loire.example')]
    lig = [[_cel_nom(n, 'journaliste.html', '', 'gris' if m == 'opposé aux envois' else 'bleu'), E(me), E(r), E(ru),
            badge('rouge', m, '■') if m == 'opposé aux envois' else E(m)] for n, me, r, ru, m in J]
    haut = kpis(kpi('Total', '3 418', 'micro', 'bleu', 'Page 1'), kpi('Avec email', '2 207', 'message', 'violet', 'sur 3 418', graph=jauge('Avec email', 2207, 3418, 'violet', '65 %')),
                kpi('Opposés', '41', 'interdit', 'ambre', '126 lignes à vérifier, non comptées'))
    f = filtres_champs([('r', 'Recherche', 'Rechercher par nom…', 'j-q'),
                        ('s', 'Type de lignes', ['Personnes identifiées', 'À vérifier (émissions, chaînes, noms mal découpés)', 'Toutes les lignes'], 'j-type')],
                       '<span class="petit">L’export contient les personnes identifiées, sans les lignes « à vérifier ».</span>')
    normal = haut + f + tableau('Journalistes', ['Nom', 'Média', 'Rôle', 'Rubrique', 'Email'], lig, liens=['journaliste.html'] * len(lig), secondaires=(3,)) + pagination('Page 1 / 35', False)
    P['journalistes.html'] = page('journalistes', 'Journalistes', 'Contacts rédaction · <strong>3 418</strong> journalistes', normal,
                                  etat_vide('micro', 'Aucun journaliste', 'Aucun journaliste pour ces filtres.', ''),
                                  etat_erreur('La liste des journalistes n’a pas pu être lue.'),
                                  actions=btn('Exporter CSV', 'plein', icone='export', attrs='data-toast="Export CSV téléchargé"'), reprise=F + 'media/JournalistsListPage.tsx')


def _journaliste():
    porte = '<div class="bandeau vert">%s<span>%s Diffusable par mailing.</span></div>' % (ic('coche'), badge('vert', 'Email rédaction', '●'))
    coord = bloc('Coordonnées', dl([('Email', 'l.fournier@courrier-rhone.example'), ('LinkedIn', '<a href="#">/in/lea-fournier-factice</a>'),
                                    ('Relation', 'En relation (1er) · 14 sept. 2026')], False), icone='personne')
    cib = bloc('Ciblage', dl([('Rôle', 'Rédactrice en chef'), ('Rubrique', 'Économie'), ('Portée du média', 'Régionale'), ('Support', 'Presse écrite'),
                             ('Priorité', badge('terracotta', 'P1', '●')), ('Score de ciblage', '<strong>92 / 110</strong>'), ('Abonnés LinkedIn', '3 100'),
                             ('Provenance', 'Annuaire presse'), ('Collecté le', '12 sept. 2026')], False) + jauge('Score de ciblage', 92, 110, 'vert', '92 / 110'), icone='cible')
    journ = _journal_presse('Aucun échange consigné. Le premier communiqué envoyé apparaîtra ici.', [
        ('02 oct. 2026', 'Communiqué : salon des artisans', 'Communiqué envoyé · via Will', 'envoi', 'bleu'),
        ('09 oct. 2026', 'Article publié', 'Retombée publiée · via Will', 'presse', 'vert')])
    normal = porte + '<div class="grille deux">%s%s</div>' % (coord, cib) + journ
    P['journaliste.html'] = page('journaliste', 'Léa Fournier', '<a href="media.html">Le Courrier du Rhône</a> · rédactrice en chef', normal,
                                 erreur=etat_erreur('Cette fiche n’existe pas ou a été supprimée.', 'Contact introuvable'),
                                 actions=btn('← Tous les journalistes', 'contour', 'journalistes.html'), fil=[('Journalistes', 'journalistes.html', 'journalistes')],
                                 reprise=F + 'media/JournalistDetailPage.tsx')


def _communiques():
    R = [('12 oct. 2026', 'Retombée publiée', 'Le Courrier du Rhône', 'Le Courrier du Rhône', 'Salon des artisans : article p. 6', 'vert'),
         ('09 oct. 2026', 'Réponse reçue', 'Samir Benali', 'Radio Vallée FM', 'Invitation matinale du 20 oct.', 'violet'),
         ('05 oct. 2026', 'Relance', 'Léa Fournier', 'Le Courrier du Rhône', 'Salon des artisans : relance', 'ambre'),
         ('02 oct. 2026', 'Communiqué envoyé', 'Hebdo Loire Infos', 'Hebdo Loire Infos', 'Salon des artisans 2026', 'bleu'),
         ('02 oct. 2026', 'Communiqué envoyé', 'Agence Presse Régions', '', 'Salon des artisans 2026', 'bleu')]
    lig = [[E(d), badge(t, g, '●'), '<a href="media.html"><strong>%s</strong></a>' % E(c), E(r) if r else badge('ambre', 'à rattacher', '▲'), E(o)] for d, g, c, r, o, t in R]
    haut = kpis(kpi('Communiqués envoyés', '18', 'envoi', 'bleu', 'ce trimestre'), kpi('Relances', '9', 'rafraichir', 'ambre', ''),
                kpi('Réponses reçues', '6', 'reponses', 'violet', ''), kpi('Retombées publiées', '4', 'presse', 'vert', '+1 cette semaine'))
    f = filtres_champs([('s', 'Geste', ['Tous les gestes presse', 'Communiqué envoyé', 'Relance', 'Réponse reçue', 'Retombée publiée'], 'c-geste'),
                        ('r', 'Recherche', 'Rechercher dans l’objet de l’envoi…', 'c-q')], '<span class="petit">5 lignes</span>')
    normal = haut + f + tableau('Communiqués envoyés', ['Date', 'Geste', 'Cible', 'Rédaction', 'Objet'], lig, liens=['media.html'] * 5)
    P['communiques.html'] = page('communiques', 'Communiqués envoyés', 'Ce qui est parti à la presse, à qui, et quand.', normal,
                                 etat_vide('envoi', 'Aucun envoi consigné', 'Les envois se consignent depuis la fiche d’une rédaction ou d’un journaliste.', ''),
                                 etat_erreur('Le registre des envois n’a pas pu être chargé.', 'Registre indisponible'),
                                 actions=btn('Exporter CSV', 'contour', icone='export', attrs='data-toast="Export CSV téléchargé (ajout plan 27)"'),
                                 reprise=F + 'media/EnvoisPressePage.tsx')


# ======================= À TRAITER =======================
def _doublons():
    def carte(motif, a, b, certain=False):
        def cote(cl, lib, x):
            return '<div class="%s"><span class="etiquette-paire">%s</span><a href="entreprise.html"><strong>%s</strong></a><span>%s</span><span>%s</span><span class="petit">%s</span></div>' % (cl, lib, E(x[0]), x[1], x[2], x[3])
        return ('<section class="bloc teinte-ambre"><div class="bloc-tete">%s<h2>%s</h2>%s</div><div class="paire">%s%s</div>'
                '<div class="bloc-pied">%s%s</div></section>' % (ic('doublon'), E(motif), badge('vert', 'preuve certaine', '✓') if certain else '<span class="mot">À vérifier</span>',
                                                                 cote('', 'Fiche gardée', a), cote('absorbee', 'Fiche absorbée (corbeille)', b),
                                                                 btn('Fusionner', 'contour', icone='copie', attrs='data-toast="Fiches fusionnées (fusion n° 214, annulable)." data-annulable'),
                                                                 btn('Ce ne sont pas des doublons', 'petit-discret', attrs='data-toast="Paire écartée : elle ne sera plus proposée."')))
    haut = kpis(kpi('Paires à vérifier', '12', 'doublon', 'terracotta', 'dont 3 certaines'), kpi('Fusionnées ce mois', '48', 'coche', 'vert', 'toutes annulables'),
                kpi('Écartées', '9', 'croix', 'gris', 'jamais reproposées'), kpi('Adresses partagées', '17', 'message', 'ambre', 'jamais fusionnées'))
    resume = '<div class="bandeau bleu">%s<span>Adresses e-mail partagées par plusieurs fiches (jamais fusionnées pour autant) : 9 cabinet comptable, 5 domiciliation, 2 groupe ou siège, 1 nature inconnue.</span></div>' % ic('aide')
    f = filtres_champs([('s', 'Motif', ['Tous', 'Même nom + code postal (7)', 'Même site (3)', 'Même SIREN (2)'], 'd-motif')])
    cartes = '<div class="cartes-pile">%s%s%s</div>' % (
        carte('Même SIREN', ('Boulangerie des Tilleuls', 'SIREN 000 000 112', '69003 Lyon', '2 personnes · source Sirene'), ('Boulangerie Tilleuls SARL', 'SIREN 000 000 112', '69003 Lyon', '0 personne · source collecte'), True),
        carte('Même nom + code postal', ('Garage des Saules', 'SIREN 000 000 245', '38000 Grenoble', '3 personnes · source Sirene · protégée'), ('Garage des Saules', 'Sans identifiant', '38000 Grenoble', '1 personne · source site')),
        carte('Même site', ('Imprimerie du Lac', 'SIREN 000 000 378', '74000 Annecy', 'imprimerie-lac.example'), ('Imprim’Lac', 'Identifiant 88213', 'Adresse inconnue', 'imprimerie-lac.example')))
    normal = haut + resume + f + cartes + pagination('Page 1 sur 1 — 12 paires', False)
    P['doublons.html'] = page('doublons', 'Doublons à vérifier', 'Fusionner met la fiche de droite à la corbeille (jamais supprimée). <strong>Annulable.</strong>', normal,
                              etat_vide('coche', 'Aucun doublon à vérifier', 'Tout est en ordre : aucune paire de fiches n’attend votre décision.', ''),
                              etat_erreur('La file des doublons n’a pas pu être chargée.'), reprise=F + 'doublons/DoublonsPage.tsx')


def _rattacher():
    def carte(ent, titre, pers, mail, cp, ville, n):
        return ('<section class="bloc teinte-violet"><div class="bloc-tete">%s<h2>%s</h2><span class="mot">À rattacher</span></div><p class="petit" style="margin-bottom:12px">%s</p>%s'
                '<div class="ligne-champs" style="margin-top:14px">%s%s</div><div class="bloc-pied">%s%s</div></section>' % (
                    ic('balance'), E(ent), E(titre), dl([('Personne', pers), ('E-mail', mail), ('Code postal', cp), ('Ville', ville)]),
                    champ('Entreprise', 'ra-ent-%d' % n, attrs='placeholder="Nom, ville, SIREN ou SIRET" role="combobox" aria-expanded="false"', aide='Choisie : Boulangerie des Tilleuls' if n == 1 else 'Tapez au moins 3 lettres du nom de l’entreprise.'),
                    champ('Motif d’écartement', 'ra-mot-%d' % n, attrs='placeholder="ex. entreprise introuvable dans les registres"'),
                    btn('Rattacher', 'contour', icone='lien', attrs='data-toast="Rattaché — fiche personne créée ou retrouvée."'), btn('Écarter', 'petit-discret', attrs='data-toast="Écarté de la file, avec son motif."')))
    haut = kpis(kpi('À rattacher', '7', 'balance', 'violet', 'reçus sans SIREN'), kpi('Rattachées ce mois', '31', 'coche', 'vert', ''), kpi('Écartées', '4', 'croix', 'gris', 'avec motif'))
    normal = haut + '<div class="cartes-pile">%s%s</div>' % (
        carte('Boulangerie des Tilleuls', 'Demande de rendez-vous · 30 oct. 2026', 'Paul Morin', 'paul@boulangerie-tilleuls.example', '69003', 'Lyon', 1),
        carte('Entreprise non nommée', 'Avis client · 29 oct. 2026', 'Sarah Lemoine', 's.lemoine@messagerie.example', '42000', 'Saint-Étienne', 2))
    P['personnes-a-rattacher.html'] = page('personnes-a-rattacher', 'Personnes à rattacher', '<strong>7 événements</strong> reçus sans SIREN — à rattacher ou à écarter.', normal,
                                           etat_vide('balance', 'Aucune personne à rattacher', 'Aucun événement n’attend d’arbitrage dans cette file.', ''),
                                           etat_erreur('La file d’arbitrage n’a pas pu être lue.'), reprise=F + 'crm-console/ArbitragePage.tsx')


def _propositions():
    def carte(qui, origine, nom, champ_, ancien, nouveau, note=''):
        return ('<section class="bloc teinte-terracotta"><div class="bloc-tete">%s<h2>%s</h2><span class="mot">À valider</span></div><p class="petit">%s · %s propose</p>'
                '<p style="margin:10px 0"><strong>%s</strong> : <span class="ancien">%s</span> → <strong>%s</strong></p>%s'
                '<div class="bloc-pied">%s%s</div></section>' % (ic('boite-entree'), E(nom), qui, origine, E(champ_), E(ancien), E(nouveau),
                                                                 ('<div class="bandeau ambre" style="margin:0">%s</div>' % note) if note else '',
                                                                 btn('Accepter', 'contour', icone='coche', attrs='data-toast="C’est fait : la fiche a été mise à jour."'),
                                                                 btn('Refuser', 'petit-discret', attrs='data-toast="C’est noté : la fiche reste telle quelle."')))
    haut = kpis(kpi('Propositions à valider', '4', 'boite-entree', 'terracotta', 'rien ne change sans vous'), kpi('Acceptées ce mois', '22', 'coche', 'vert', ''), kpi('Refusées', '5', 'croix', 'gris', ''))
    normal = haut + '<div class="cartes-pile">%s%s%s</div>' % (
        carte('Entreprise', 'Un apporteur d’affaires', 'Garage des Saules', 'Téléphone', '04 00 00 10 10', '04 00 00 10 99'),
        carte('Personne', 'Le site vérifié de l’entreprise', 'Paul Morin', 'Fonction', 'Gérant', 'Co-gérant', 'Information déclarée par la personne elle-même.'),
        carte('Entreprise', 'L’annuaire officiel de l’administration', 'Imprimerie du Lac', 'Adresse', '(vide)', '4 quai des Pêcheurs, 74000 Annecy'))
    P['propositions.html'] = page('propositions', 'Propositions à valider', '<strong>4 propositions</strong> à valider. Rien ne change sans votre accord.', normal,
                                  etat_vide('boite-entree', 'Aucune proposition à valider', 'Quand un partenaire proposera une information différente, elle apparaîtra ici.', ''),
                                  etat_erreur('Les propositions n’ont pas pu être lues.'), reprise=F + 'propositions/PropositionsPage.tsx')


# ======================= MA BASE =======================
ENTS = [('Boulangerie des Tilleuls', 'Lyon (69003)', '3 à 5 salariés', 'Boulangerie et boulangerie-pâtisserie', 'TPE', ('vert', 'Complète 94'), '12/10/2026', 'haute'),
        ('Garage des Saules', 'Grenoble (38000)', '6 à 9 salariés', 'Entretien et réparation de véhicules', 'TPE', ('ambre', 'Partielle 71'), '08/10/2026', 'moyenne'),
        ('Imprimerie du Lac', 'Annecy (74000)', '20 à 49 salariés', 'Imprimerie', 'PME', ('vert', 'Complète 90'), '30/09/2026', 'haute'),
        ('Club de voile du Lac', 'Annecy (74000)', '0 salarié', 'Activités de clubs de sports', 'TPE', ('rouge', 'Basique 42'), '—', 'basse'),
        ('Comité des fêtes de Vienne', 'Vienne (38200)', '0 salarié', 'Autres organisations', 'TPE', ('ambre', 'Partielle 63'), '21/09/2026', 'moyenne'),
        ('Atelier Bois & Forme', 'Chambéry (73000)', '10 à 19 salariés', 'Menuiserie bois', 'PME', ('vert', 'Complète 92'), '02/10/2026', 'haute'),
        ('Office de tourisme du Val', 'Valence (26000)', '10 à 19 salariés', 'Information touristique', 'PME', ('ambre', 'Partielle 77'), '15/09/2026', 'moyenne'),
        ('Transports Rivière', 'Bourg-en-Bresse (01000)', '50 à 99 salariés', 'Transports routiers de fret', 'PME', ('vert', 'Complète 96'), '11/10/2026', 'haute')]
PRIO = {'haute': ('terracotta', 'Haute'), 'moyenne': ('ambre', 'Moyenne'), 'basse': ('gris', 'Basse')}


def _entreprises():
    lig = []
    for i, (n, v, eff, act, taille, q, enr, pr) in enumerate(ENTS):
        cel = ('<div class="cellule-personne"><input type="checkbox" aria-label="Choisir %s"%s>%s<div><a href="entreprise.html">%s</a><span class="sous">%s · %s</span></div></div>'
               % (E(n), ' checked' if i in (0, 2) else '', initiales(n, 'bleu'), E(n), E(v), E(eff)))
        lig.append([cel, E(act), badge('bleu', taille, '■'), badge(q[0], q[1], '●'), badge(PRIO[pr][0], PRIO[pr][1], '●'), '<span class="chiffre">%s</span>' % enr,
                    btn('Voir la fiche', 'petit-discret', 'entreprise.html')])
    haut = kpis(kpi('Total', '48 212', 'entreprise', 'bleu', 'Page 1 · 100 affichées'),
                kpi('Enrichies', '≈ 62 %', 'etincelle', 'violet', 'des fiches (estimation)', graph=jauge('Enrichies', 62, 100, 'violet', '62 %')),
                kpi('Taille la plus fréquente', 'TPE', 'stats', 'vert', '81 % de toutes les fiches', graph=jauge('TPE', 81, 100, 'vert', '81 %')),
                kpi('Secteur le plus fréquent', 'Commerce de détail', 'cible', 'ambre', '6 140 fiches (13 %)'))
    ong = '<nav class="onglets" aria-label="Statut de prospection"><a href="entreprises.html" aria-current="page">Tous <span class="nb">48 212</span></a><a href="#">Prospectables <span class="nb">21 904</span></a><a href="#">Partiels <span class="nb">9 310</span></a><a href="#">À compléter <span class="nb">15 877</span></a><a href="#">Archivés <span class="nb">1 121</span></a></nav>'
    f = filtres_champs([('r', 'Recherche', 'Rechercher une entreprise…', 'e-q'), ('s', 'Département', ['Tous départements', '01 · Ain', '38 · Isère', '69 · Rhône', '74 · Haute-Savoie'], 'e-dep'),
                        ('s', 'Taille', ['Toutes tailles', 'TPE', 'PME', 'ETI', 'Grand groupe'], 'e-taille'),
                        ('s', 'Secteur d’activité', ['Tous secteurs', 'Agriculture, sylviculture, pêche', 'Agroalimentaire et boissons', 'Industrie', 'Bâtiment et travaux publics', 'Commerce de détail', 'Restauration', 'Culture, sport et loisirs', 'Non classé'], 'e-sect'),
                        ('c', 'Afficher les entreprises fermées', '', 'e-ferm')],
                       btn('Plus de filtres (13)', 'petit', icone='filtre') + '<span class="petit">1 filtre actif</span>' + btn('Effacer les filtres', 'petit-discret')
                       + btn('Enregistrer cette vue', 'petit', icone='sauvegarde', attrs='data-toast="Vue enregistrée : « Rhône, TPE » (ajout plan 27)."'))
    masse = barre_masse('2 sélectionnées', '<label class="visuellement-cache" for="e-etiq">Étiquette existante</label><input type="text" id="e-etiq" placeholder="Étiquette existante (campagne-ro…)" style="flex:1 1 200px;min-width:0">'
                        + btn('Poser l’étiquette', 'petit', icone='diese') + btn('Ajouter à une liste…', 'petit', icone='liste-cochee')
                        + btn('Exporter la sélection', 'petit', icone='export', attrs='data-toast="2 fiches exportées en CSV."') + btn('Annuler la sélection', 'petit', attrs='data-toast="Sélection annulée."'))
    t = tableau('Entreprises', ['Entreprise', 'Activité', 'Taille', 'Qualité', 'Priorité', 'Enrichi', ''], lig, liens=['entreprise.html'] * len(lig), secondaires=(1, 4, 5, 6))
    normal = haut + ong + f + masse + t + pagination('Page <strong>1</strong> / 483 · 48 212 au total')
    P['entreprises.html'] = page('entreprises', 'Entreprises', '<strong>48 212</strong> entreprises actives', normal,
                                 etat_vide('entreprise', 'Aucune entreprise', 'Aucune entreprise pour l’instant. La carte de France permet d’en récupérer.', btn('Voir la carte', 'plein', 'carte-france.html', 'carte')),
                                 etat_erreur('Le serveur n’a pas pu lire la liste des entreprises. Vos données ne sont pas perdues : réessayez dans un instant.', 'Liste momentanément indisponible'),
                                 actions=btn('Exporter', 'contour', icone='export', attrs='data-toast="Export CSV téléchargé"') + btn('Récupérer des entreprises', 'plein', 'carte-france.html', 'carte'),
                                 reprise=F + 'companies/CompaniesListPage.tsx')


def _entreprise():
    tete = '<div class="fiche-tete">%s<div class="meta"><span class="mono">SIREN 000 000 112</span><span>Dept 69</span>%s%s%s</div></div>' % (
        initiales('Boulangerie Tilleuls', 'bleu').replace('initiales ', 'initiales grand '), badge('bleu', 'TPE', '■'), badge('vert', 'Complète 94', '●'), badge('terracotta', 'Priorité haute', '●'))
    ident = bloc('Informations entreprise', dl([('SIREN', '<span class="mono">000 000 112</span>'), ('Forme juridique', 'SARL'), ('Activité', 'Boulangerie et boulangerie-pâtisserie <span class="sous">10.71C</span>'),
                                               ('Effectif', '3 à 5 salariés'), ('Convention collective (IDCC)', 'Boulangerie-pâtisserie artisanale'), ('OPCO', 'OPCO EP'),
                                               ('Adresse', '12 rue des Tilleuls, 69003 Lyon'), ('Site web', '<a href="#">boulangerie-tilleuls.example</a>'), ('Téléphone', '<span class="mono">04 00 00 12 12</span>'),
                                               ('LinkedIn', '<a href="#">Voir le profil →</a>'), ('Date création', '04/03/2011'), ('Enrichi le', '12/10/2026 08:14')]), icone='entreprise')
    sources = bloc('Sources consultées', chrono([('12/10 08:14', 'INSEE Sirene', 'Réussi', 'coche', 'vert'), ('12/10 08:14', 'Base Adresse Nationale', 'Réussi', 'coche', 'vert'),
                                                 ('12/10 08:15', 'Lecture du site web', 'Partiel', 'alerte', 'ambre'), ('12/10 08:15', 'LinkedIn', 'Rien trouvé', 'croix', 'gris')]), icone='horloge')
    console = bloc('Reçu de la console', dl([('Statut', 'Prospect'), ('Questionnaire', 'reçu le 3 oct. · 2 sur 4'), ('Prochaine action', 'Rappel · avant le 6 nov.'), ('Étape', 'Devis envoyé'),
                                             ('Santé du compte', badge('vert', 'Bonne', '●'))], False) + '<p class="petit" style="margin-top:10px">Les actions se font dans la console d’Axion IA.</p>', 'violet', 'etincelle', mot='Console')
    relation = bloc('Type et étape', champ('Type de relation', 'r-type', 'select', ['Prospects', 'Clients', 'Presse & médias', 'Partenaires', 'Investisseurs', 'Conférences', 'Newsletter', 'Fournisseurs'])
                    + champ('Étape', 'r-etape', 'select', ['Qualifié', 'Nouveau', 'Opportunité', 'Client', 'Dormant', 'Perdu'], aide='Posée à la main le 8 oct. : l’import ne la modifiera plus.')
                    + '<p><strong>Joignabilité :</strong> %s</p>' % badge('vert', 'E-mail vérifié valide', '✓'), 'bleu', 'cible', mot='Relation', pied=btn('Enregistrer', 'contour', icone='coche', attrs='data-toast="Relation enregistrée"'))
    contacts_ = bloc('Contacts (2)', lignes(ligne('Paul Morin', 'Gérant · paul@boulangerie-tilleuls.example', initiales('Paul Morin'), badge('vert', 'Valide', '✓'), 'contact.html'),
                                           ligne('Julie Morin', 'Co-gérante · julie@boulangerie-tilleuls.example', initiales('Julie Morin'), badge('ambre', 'Catch-all', '▲'), 'contact.html')), icone='personnes')
    taches_ = bloc('Tâches du CRM', lignes(ligne('Rappeler pour le devis', 'À faire avant le 6 novembre 2026', '', btn('Marquer comme faite', 'petit-discret', attrs='data-toast="Tâche marquée comme faite."')),
                                           ligne('<span class="ancien">Envoyer la plaquette</span>', 'Faite', '', badge('vert', 'Faite', '✓'))), 'terracotta', 'taches', mot='1 à faire',
                   pied=btn('Ajouter une tâche CRM', 'contour', icone='plus', attrs='data-toast="Formulaire de tâche ouvert."'))
    etiq = bloc('Étiquettes (propres au CRM, non synchronisées)', '<div class="puces-etiq"><span class="puce-etiq">salon-artisans-2026 ×</span><span class="puce-etiq">rhone ×</span></div>'
                + '<div class="bloc-pied" style="margin-top:12px">%s</div>' % btn('Campagne vers cette étiquette', 'petit', 'campagne-nouvelle.html?cible=etiquette', 'envoi'), icone='diese')
    listes_ = bloc('Listes manuelles', lignes(ligne('Invités salon 2026', 'Organisation + 1 contact', '', btn('Retirer', 'petit-discret', attrs='data-toast="Fiche retirée de la liste (la fiche elle-même est intacte)."'))), icone='liste-cochee')
    qualite = bloc('Qualité de la donnée', anneau(94, 100, 'vert', '94', 'Complète', 'sur 100') + '<div class="pile" style="margin-top:14px;gap:10px">%s%s%s%s</div>' % (
        jauge('Email', 100, 100, 'vert', '100'), jauge('Téléphone', 100, 100, 'vert', '100'), jauge('Site web', 80, 100, 'vert', '80'), jauge('Contacts', 90, 100, 'vert', '90')), 'vert', 'stats', mot='Complète')
    ajouts = bloc('Liens et documents', mini_titre('Liens entre entreprises') + lignes(ligne('Groupe Tilleuls Holding', 'Société mère', initiales('G T', 'gris'), badge('gris', 'Groupe', '■'), 'entreprise.html'))
                  + mini_titre('Documents joints') + lignes(ligne('Devis-2026-114.pdf', 'Ajouté le 8 oct. par Will', '', btn('Ouvrir', 'petit-discret', attrs='data-toast="Aperçu du PDF (maquette)."'))),
                  'violet', 'lien', mot='Nouveau', pied=btn('Compléter cette fiche', 'petit', icone='etincelle', attrs='data-toast="Complément lancé : résultat dans 2 min."'))
    envois = bloc('Envois reçus (produit Envoi)', lignes(ligne('Organisateurs Rhône-Alpes · message 1', 'Accepté par le serveur · 28 oct. 09:12', '', badge('vert', 'Parti', '✓'), 'chercher-envoi.html')),
                  icone='envoi', pied=btn('Chercher un envoi', 'petit', 'chercher-envoi.html', 'chercher'))
    normal = (tete + '<div class="grille deux-un"><div class="pile">%s%s%s%s</div><div class="pile">%s%s%s%s%s%s%s</div></div>' % (
        ident, sources, ajouts, envois, console, relation, contacts_, taches_, etiq, listes_, qualite))
    P['entreprise.html'] = page('entreprise', 'Boulangerie des Tilleuls', 'Lyon · TPE · <strong>2 contacts</strong> · prospect', normal,
                                erreur=etat_erreur('Cette entreprise n’existe pas ou a été supprimée.', 'Entreprise introuvable'),
                                actions=btn('Exporter', 'contour', icone='export', attrs='data-toast="Fiche exportée (vCard)."') + btn('Enrichir maintenant', 'plein', icone='etincelle', attrs='data-toast="Enrichissement lancé"'),
                                fil=[('Entreprises', 'entreprises.html', 'entreprises')], reprise=F + 'companies/CompanyDetailPage.tsx')


def _contacts():
    ORGS = [('Boulangerie des Tilleuls', 'Prospects · Qualifié', 'Lyon', ['Paul Morin', 'Julie Morin'], ['Secteur · boulangerie', 'Zone · Rhône', 'Source · site']),
            ('Garage des Saules', 'Clients · Client', 'Grenoble', ['Marc Delorme'], ['Secteur · auto', 'Taille · TPE']),
            ('Imprimerie du Lac', 'Prospects · Opportunité', 'Annecy', ['Nadia Haddad', 'Yves Roche', 'Lina Costa'], ['Intérêt · catalogue', 'Rendez-vous · 7 nov.', 'Zone · Savoie', '+2']),
            ('Transports Rivière', 'Partenaires · Qualifié', 'Bourg-en-Bresse', ['Éric Vidal'], ['Secteur · transport'])]
    items = []
    for i, (n, t, v, pers, et) in enumerate(ORGS):
        pp = ' '.join('<label class="case" style="min-height:40px;padding:0"><input type="checkbox"%s> <a href="contact.html">%s</a></label>' % (' checked' if i == 0 else '', E(p)) for p in pers)
        items.append('<li class="ligne" style="display:grid;gap:8px"><div style="display:flex;flex-wrap:wrap;gap:10px;align-items:center"><input type="checkbox" aria-label="Choisir %s"%s><strong style="font-size:16px">%s</strong><span class="petit">%s · %s</span></div>'
                     '<div style="display:flex;flex-wrap:wrap;gap:4px 18px">%s</div><div class="puces-etiq">%s</div></li>' % (E(n), ' checked' if i == 0 else '', E(n), E(t), E(v), pp, ''.join('<span class="puce-etiq">%s</span>' % E(e) for e in et)))
    haut = kpis(kpi('Clients', '86', 'coche', 'vert', ''), kpi('Prospects', '1 412', 'cible', 'bleu', ''), kpi('Opportunités', '37', 'etincelle', 'violet', ''), kpi('Dormants', '204', 'horloge', 'gris', ''))
    ong = '<nav class="onglets" aria-label="Types"><a href="contacts.html" aria-current="page">Tous <span class="nb">1 739</span></a><a href="#">Prospects <span class="nb">1 412</span></a><a href="#">Clients <span class="nb">86</span></a><a href="#">Presse &amp; médias <span class="nb">58</span></a><a href="#">Partenaires <span class="nb">41</span></a><a href="#">Investisseurs <span class="nb">6</span></a><a href="#">Conférences <span class="nb">19</span></a><a href="#">Newsletter <span class="nb">102</span></a><a href="#">Fournisseurs <span class="nb">15</span></a></nav>'
    f = filtres_champs([('r', 'Recherche', 'Nom d’entreprise, SIREN, personne…', 'c-q'), ('s', 'Pays', ['Tous pays', 'France', 'Roumanie'], 'c-pays'),
                        ('s', 'Statut de prospection', ['Tous statuts', 'Contactables (e-mail exploitable)', 'Partiels (e-mail incertain)', 'Collectés, pas encore enrichis', 'Sans e-mail (archivés)'], 'c-stat')],
                       '<div class="barre-temperature" role="group" aria-label="Température"><button type="button" class="puce" aria-pressed="true">Contacts actifs</button><button type="button" class="puce" aria-pressed="false">Prospection (base froide)</button><button type="button" class="puce" aria-pressed="false">Tout</button></div>')
    masse = barre_masse('1 organisation, 1 personne cochée(s)', btn('Ajouter à une liste…', 'petit', icone='liste-cochee') + btn('Exporter (CSV)', 'petit', icone='export', attrs='data-toast="2 fiches exportées (ajout plan 27)."'))
    normal = haut + ong + f + masse + '<div class="bloc" style="margin-top:16px"><ul class="lignes">%s</ul></div>' % ''.join(items)
    ajout = fenetre('fen-ajout', 'Ajouter un contact', champ('Prénom et nom', 'aj-nom') + champ('E-mail', 'aj-mail', 'email', aide='Doublons vérifiés à la saisie.')
                    + champ('Entreprise', 'aj-ent', attrs='placeholder="Nom, ville, SIREN ou SIRET"') + champ('Provenance', 'aj-prov', 'select', ['Choisir…', 'Salon', 'Site internet', 'Recommandation', 'Fichier importé'], aide='Obligatoire.'),
                    '<button type="button" class="btn btn-contour" data-ferme>Annuler</button><button type="button" class="btn btn-plein" data-ferme data-toast="Contact ajouté.">Ajouter le contact</button>')
    P['contacts.html'] = page('contacts', 'Contacts', 'Tous les types — <strong>Contacts actifs</strong>', normal,
                              etat_vide('personnes', 'Aucun contact dans cette vue', 'Les fiches arrivent automatiquement depuis le site (formulaires, RDV, avis).', ''),
                              etat_erreur('La liste des fiches n’a pas pu être lue.'),
                              actions=btn('Ajouter un contact', 'plein', icone='ajout-personne', attrs='id="ajout" data-ouvre="fen-ajout"'), apres=ajout,
                              reprise=F + 'crm-console/ContactsHubPage.tsx (et contacts/ContactsListPage.tsx hors console)')


def _newsletter():
    PERS = [('Camille Brun', 'Abonné à la newsletter', 'Newsletter', 'Adresse professionnelle', ('vert', 'Rattachée · Imprimerie du Lac'), 'camille@imprimerie-lac.example', '28/10/2026'),
            ('Hugo Marchand', 'Sans abonnement', 'Guide IA entreprise', 'Adresse professionnelle', ('ambre', 'À rattacher'), 'h.marchand@cabinet-alpha.example', '27/10/2026'),
            ('e.leroy@messagerie.example', 'Abonné à la newsletter', 'Newsletter', 'Adresse personnelle', ('ambre', 'À rattacher'), 'e.leroy@messagerie.example', '25/10/2026'),
            ('Noémie Faure', 'Désabonné', 'Newsletter', 'Adresse professionnelle', ('vert', 'Rattachée · Transports Rivière'), 'n.faure@transports-riviere.example', '02/09/2026')]
    li = lignes(*[ligne('<a href="personne-newsletter.html">%s</a>' % E(n), '%s · %s · %s<br>%s · Dernière interaction : %s' % (E(s), E(so), E(t), E(m), d), initiales(n, 'bleu'), badge(r[0], r[1], '●' if r[0] == 'vert' else '▲')) for n, s, so, t, r, m, d in PERS])
    haut = kpis(kpi('Abonnés à la newsletter', '412', 'message', 'bleu', ''), kpi('Demandeurs du guide sans abonnement', '138', 'fichier', 'violet', ''),
                kpi('À rattacher', '96', 'balance', 'ambre', 'à une entreprise'), kpi('Désabonnés', '27', 'interdit', 'gris', ''))
    f = filtres_champs([('r', 'Recherche', 'Adresse, nom…', 'n-q'), ('s', 'Newsletter', ['Tous les statuts', 'Abonné à la newsletter', 'Désabonné', 'Sans abonnement'], 'n-stat'),
                        ('s', 'Source', ['Toutes les sources', 'Newsletter', 'Guide IA entreprise'], 'n-src'), ('s', 'Type d’adresse', ['Toutes les adresses', 'Adresse professionnelle', 'Adresse personnelle', 'Nature inconnue'], 'n-type'),
                        ('s', 'Rattachement', ['Rattachées ou non', 'À rattacher', 'Rattachées à une entreprise'], 'n-ratt'), ('c', 'Inclure les fermées', '', 'n-ferm')],
                       btn('Exporter le segment (CSV)', 'petit', icone='export', attrs='data-toast="Export CSV téléchargé"'))
    normal = haut + f + bloc('Personnes (4 sur 673)', li, icone='personnes')
    P['newsletter-guide.html'] = page('newsletter-guide', 'Newsletter et guide', 'Abonnés à la newsletter et demandeurs du guide, <strong>sans entreprise</strong>.', normal,
                                      etat_vide('message', 'Aucune personne dans ce segment', 'Les personnes arrivent depuis le site une fois le flux ouvert : rien à créer ici.', ''),
                                      etat_erreur('La liste des personnes n’a pas pu être lue.'), reprise=F + 'crm-console/PersonnesPage.tsx')


def _personne_nl():
    ident = bloc('Identité', dl([('E-mail', 'h.marchand@cabinet-alpha.example'), ('Type d’adresse', 'Adresse professionnelle'), ('Base légale', 'Intérêt légitime B2B'), ('Purge prévue le', '27/10/2029')], False)
                 + '<p style="margin-top:10px"><a href="contact.html">Tout l’historique de cette personne</a></p>', icone='personne')
    nl = bloc('Newsletter', '<p>%s</p>' % badge('gris', 'Sans abonnement', '○') + '<p class="petit" style="margin-top:10px">Copie du consentement : la preuve reste sur le site.</p>', icone='message')
    ent = bloc('Entreprise', '<p style="margin-bottom:12px">Non rattachée. Une fois rattachée, elle rejoint le hub de contacts et les audiences.</p>'
               + champ('Entreprise', 'pn-ent', attrs='placeholder="Nom, ville, SIREN ou SIRET"') + '<div class="ligne-champs">%s%s</div>' % (champ('Prénom (facultatif)', 'pn-pre', valeur='Hugo'), champ('Nom de famille (requis)', 'pn-nom', valeur='Marchand')),
               'ambre', 'balance', mot='À rattacher', pied=btn('Rattacher à cette entreprise', 'plein', icone='lien', attrs='data-toast="Rattachée — fiche contact créée."'))
    taches_ = bloc('Tâches et relances', '<div class="ligne-champs">%s%s</div>' % (champ('Tâche', 'pn-t', attrs='placeholder="ex. Retrouver l’entreprise (SIREN)"'), champ('Échéance', 'pn-d', 'date', '2026-11-05'))
                   + lignes(ligne('Retrouver l’entreprise', 'échéance 05/11/2026', '', btn('Terminer', 'petit-discret', attrs='data-toast="Tâche terminée."'))), icone='taches',
                   pied=btn('Poser', 'petit', icone='plus', attrs='data-toast="Tâche posée."'))
    hist = bloc('Historique', chrono([('27/10/2026', 'Guide téléchargé', 'Guide IA entreprise', 'fichier', 'violet')]), icone='horloge')
    normal = '<div class="grille deux"><div class="pile">%s%s%s</div><div class="pile">%s%s</div></div>' % (ident, nl, ent, taches_, hist)
    P['personne-newsletter.html'] = page('personne-newsletter', 'Hugo Marchand', 'Guide IA entreprise · arrivée le 27/10/2026', normal,
                                         erreur=etat_erreur('Cette personne n’existe pas dans votre univers.', 'Fiche introuvable'),
                                         fil=[('Newsletter et guide', 'newsletter-guide.html', 'newsletter-guide')], reprise=F + 'crm-console/PersonneDetailPage.tsx')


def _candidats():
    C = [('Inès Garnier', 'Commercial', 'Nouveau', 'terracotta', ['Offre · commercial terrain', 'Zone · Lyon', 'Dispo · janvier']),
         ('Rémi Caron', 'Vidéo', 'Présélection', 'bleu', ['Offre · monteur', 'Mobilité · oui']),
         ('Aya Mendes', 'Tech', 'Entretien', 'violet', ['IA · notions', 'B2B · 3 ans', 'Zone · distance']),
         ('Lucas Ferry', 'Autres métiers', 'Vivier', 'gris', ['Offre · assistant', 'Dispo · immédiate'])]
    li = lignes(*[ligne('<a href="contact.html">%s</a>' % E(n), '%s · %s<br>Dernière interaction : 20/10/2026 · Horloge CNIL : purge prévue le 20/10/2028 · CV stocké sur le site' % (E(fa), E(et)),
                        initiales(n, t), '<span class="puces-etiq">%s</span>' % ''.join('<span class="puce-etiq">%s</span>' % E(x) for x in tags)) for n, fa, et, t, tags in C])
    haut = kpis(kpi('À qualifier', '14', 'diplome', 'ambre', 'à traiter'), kpi('Présélection', '9', 'filtre', 'bleu', ''), kpi('Entretien', '4', 'calendrier', 'violet', ''), kpi('Conservés en vivier', '63', 'sauvegarde', 'gris', ''))
    ong = '<nav class="onglets" aria-label="Familles"><a href="candidats.html" aria-current="page">Tous les candidats <span class="nb">90</span></a><a href="#">Commercial <span class="nb">31</span></a><a href="#">Vidéo <span class="nb">12</span></a><a href="#">Tech <span class="nb">22</span></a><a href="#">Autres métiers <span class="nb">25</span></a></nav>'
    normal = haut + ong + filtres_champs([('r', 'Recherche', 'Nom, prénom, e-mail…', 'ca-q')]) + bloc('Candidats', li, icone='diplome')
    P['candidats.html'] = page('candidats', 'Candidats', 'Les candidats sont <strong>séparés</strong> des clients et prospects.', normal,
                               etat_vide('diplome', 'Aucun candidat dans cette vue', 'Les candidatures arrivent depuis le site, avec leur consentement v2.', ''),
                               etat_erreur('La liste des candidats n’a pas pu être lue.'), reprise=F + 'crm-console/CandidatesPage.tsx')


def _contact():
    ident = bloc('Identité', lignes(ligne('Paul Morin', 'paul@boulangerie-tilleuls.example · Boulangerie des Tilleuls', initiales('Paul Morin'), '', 'entreprise.html')), icone='personne')
    base = bloc('Base', '<ul class="lignes"><li class="ligne"><span class="quoi"><strong>Clients et prospects</strong></span>%s</li><li class="ligne"><span class="quoi"><strong>Candidats</strong></span>%s</li></ul>' % (
        badge('vert', 'Fiche présente', '✓'), badge('gris', 'Aucune fiche', '○')), icone='sauvegarde')
    ecrire = bloc('Peut-on lui écrire ?', verdict_global('Oui', 'Aucune opposition · adresse vérifiée il y a 9 jours', 'vert', 'coche'), 'vert', 'coche', mot='Joignable')
    hist = bloc('Historique', chrono([('28/10/2026', 'Message 1 parti (Envoi)', 'Clients et prospects · Organisateurs Rhône-Alpes', 'envoi', 'bleu'),
                                      ('30/10/2026', 'Réponse : « Rappelez-moi jeudi »', 'Clients et prospects · Réponses', 'reponses', 'vert'),
                                      ('03/10/2026', 'Questionnaire reçu (2 sur 4)', 'Clients et prospects · console', 'fichier', 'violet')]), icone='horloge')
    etat = bloc('État de ses messages (Envoi)', tableau('Messages', ['Message', 'État', 'Raison'], [
        ['Organisateurs RA · message 1', badge('vert', 'Parti', '✓'), 'Accepté par le serveur (250)'],
        ['Organisateurs RA · relance', badge('gris', 'Annulé', '○'), 'A répondu : séquence arrêtée']]), icone='envoi', pied=btn('Chercher un envoi', 'petit', 'chercher-envoi.html', 'chercher'))
    normal = '<div class="grille deux-un"><div class="pile">%s%s</div><div class="pile">%s%s%s</div></div>' % (hist, etat, ident, base, ecrire)
    P['contact.html'] = page('contact', 'Paul Morin', 'Tout ce qui concerne cette personne.', normal,
                             erreur=etat_erreur('Cette personne n’existe dans aucune base à laquelle vous avez accès.', 'Fiche introuvable'),
                             fil=[('Contacts', 'contacts.html', 'contacts')], reprise=F + 'crm-console/PersonTimelinePage.tsx')


for _f in (_medias, _media, _journalistes, _journaliste, _communiques, _doublons, _rattacher, _propositions,
           _entreprises, _entreprise, _contacts, _newsletter, _personne_nl, _candidats, _contact):
    _f()
