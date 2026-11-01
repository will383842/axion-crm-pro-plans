# -*- coding: utf-8 -*-
"""Lot M1 · produit CRM Pro : Réglages, Technique, Mon compte, écrans hors coquille.
Reprise fidèle des composants réels, puis ajouts du plan 27. Données factices, aucun secret."""
from socle import *  # noqa: F401,F403

P = {}
F = 'frontend/src/features/'


# ======================= RÉGLAGES =======================
def _parametres():
    ent = bloc('Nom et budget', '<div class="ligne-champs">%s%s</div>' % (champ('Nom', 'p-nom', valeur='Axion-IA'), champ('Budget IA mensuel (€)', 'p-budget', 'number', '40', 'L’IA s’arrête d’elle-même quand le budget est atteint.')),
               icone='entreprise', pied=btn('Enregistrer', 'plein', icone='coche', attrs='data-toast="Réglages enregistrés"'))
    compte = bloc('Changer mon mot de passe', '<p>Le formulaire complet est sur <a href="compte.html">Mon compte et sécurité</a>.</p>', icone='cle', pied=btn('Ouvrir Mon compte', 'petit', 'compte.html', 'fleche'))
    util = bloc('Qui a accès à la console', '<p>Invitez une personne, changez son rôle ou fermez son accès.</p>', icone='equipe', pied=btn('Gérer les utilisateurs', 'petit', 'utilisateurs.html', 'equipe'))
    aff = bloc('Affichage tables', '<p style="margin-bottom:12px">Choisissez l’espacement des lignes dans les listes longues.</p>' + filtres(['Confortable', 'Compacte']), icone='liste')
    plus = bloc('Autres réglages', '<div class="reglages-liens">%s</div>' % ''.join('<a href="%s">%s<span><strong>%s</strong><small>%s</small></span></a>' % (h, ic(i), t, s) for h, i, t, s in [
        ('etiquettes.html', 'diese', 'Étiquettes', 'Classer les fiches'), ('rgpd.html', 'bouclier', 'Demandes RGPD', 'Délais et preuves'), ('sante-systeme.html#sauvegardes', 'sauvegarde', 'Sauvegardes', 'Copie chiffrée, hors site'),
        ('reglages-envoi.html', 'envoi', 'Réglages d’envoi', 'Produit Envoi (à part)')]), 'violet', 'reglages', mot='Nouveau')
    normal = onglets('Paramètres', [('ent', 'Mon entreprise', ent + plus), ('compte', 'Mon compte', compte), ('util', 'Utilisateurs', util), ('aff', 'Affichage', aff)])
    P['parametres.html'] = page('parametres', 'Paramètres', 'Votre entreprise, votre compte, les utilisateurs et l’affichage. ' + badge('gris', 'Axion-IA', '⚙'), normal,
                                erreur=etat_erreur('Les réglages de l’espace de travail n’ont pas pu être lus.'), reprise=F + 'settings/SettingsPage.tsx')


def _compte():
    mdp = bloc('Changer mon mot de passe', '<ul style="margin:0 0 14px;padding-left:20px"><li>12 caractères minimum.</li><li>Il ne doit pas figurer dans une fuite de données connue (vérification anonyme).</li><li>Vos autres appareils seront déconnectés ; celui-ci reste connecté.</li></ul>'
               + champ('Mot de passe actuel', 'c-act', 'password') + champ('Nouveau mot de passe', 'c-nv', 'password', attrs='placeholder="12 caractères minimum"') + champ('Confirmation du nouveau mot de passe', 'c-conf', 'password', attrs='placeholder="Retapez le même mot de passe"'),
               'bleu', 'cle', mot='Reprise', pied=btn('Enregistrer le nouveau mot de passe', 'plein', icone='cle', attrs='data-toast="Mot de passe modifié"'))
    deux = bloc('Double authentification', verdict_global('Activée', 'Code par e-mail à chaque connexion (plan : S3).', 'vert', 'bouclier') + chiffres([('8', 'codes de secours'), ('2', 'appareils de confiance')]),
                'vert', 'bouclier', mot='Active', pied=btn('Nouveaux codes de secours', 'petit', icone='rafraichir', attrs='data-toast="8 nouveaux codes générés (affichés une fois)."'))
    app = bloc('Appareils de confiance', lignes(ligne('Ordinateur du bureau', 'Lyon · vu aujourd’hui', ic('serveur'), badge('vert', 'Celui-ci', '✓')),
                                               ligne('Téléphone', 'vu il y a 3 jours', ic('telephone'), btn('Retirer', 'petit-discret', attrs='data-toast="Appareil retiré."'))), 'violet', 'verrou', mot='Nouveau')
    rac = bloc('Raccourcis clavier', interrupteur('Raccourcis activés', 'G puis A : tableau de bord · G puis R : réponses · Ctrl K : chercher.', 'c-rac'), icone='aide')
    normal = '<div class="grille deux">%s<div class="pile">%s%s%s</div></div>' % (mdp, deux, app, rac)
    P['compte.html'] = page('compte', 'Mon compte et sécurité', 'Will · <strong>propriétaire</strong> · 2FA activée', normal, reprise=F + 'settings/ChangerMotDePasse.tsx (+ sécurité : nouvelle)', menu='parametres')


ROLES = {'Propriétaire': 'rouge', 'Administrateur': 'ambre', 'Opérateur': 'bleu', 'Lecteur': 'gris'}


def _utilisateurs():
    U = [('Will', 'will@axion-ia.example', 'Propriétaire', True, '01/11/2026 08:02', True), ('Sophie Renard', 'sophie@axion-ia.example', 'Administrateur', True, '31/10/2026 17:40', False),
         ('Karim Saidi', 'karim@axion-ia.example', 'Opérateur', False, '29/10/2026 10:12', False), ('Élodie Brun', 'elodie@axion-ia.example', 'Lecteur', False, 'Jamais', False)]
    sel = lambda r: '<label class="visuellement-cache" for="r-%s">Rôle</label><select id="r-%s" style="width:auto">%s</select>' % (r, r, ''.join('<option%s>%s</option>' % (' selected' if o.startswith(r[:4]) else '', o) for o in ['Lecteur (lecture seule)', 'Opérateur (édition)', 'Administrateur (gère l’équipe)', 'Propriétaire']))
    lig = [['<div class="cellule-personne">%s<strong>%s</strong></div>' % (initiales(n, 'violet' if moi else 'bleu'), E(n)), E(m), badge(ROLES[r], r, '●'),
            badge('vert', 'Activé', '✓') if f else badge('ambre', 'Non activé', '▲'), d,
            '<span class="petit">Vous</span>' if moi else '<div class="ligne-actions">%s%s</div>' % (sel(r), '<button type="button" class="btn btn-contour petit-btn" data-ouvre="fen-fermer">Fermer</button>')]
           for n, m, r, f, d, moi in U]
    haut = kpis(kpi('Personnes', '4', 'equipe', 'bleu', ''), kpi('2FA activée', '2', 'bouclier', 'vert', 'sur 4', graph=jauge('2FA', 2, 4, 'vert', '50 %')), kpi('Sans 2FA', '2', 'alerte', 'ambre', 'à relancer'))
    inv = fenetre('fen-inviter', 'Inviter un utilisateur', '<p style="margin-bottom:12px">Le compte est créé immédiatement, sans mot de passe. La personne reçoit un lien pour en choisir un.</p>'
                  + champ('Email', 'i-mail', 'email', attrs='placeholder="prenom.nom@exemple.com"') + champ('Nom', 'i-nom', attrs='placeholder="Prénom Nom"') + champ('Rôle', 'i-role', 'select', ['Opérateur (édition)', 'Lecteur (lecture seule)', 'Administrateur (gère l’équipe)', 'Propriétaire']),
                  '<button type="button" class="btn btn-contour" data-ferme>Annuler</button><button type="button" class="btn btn-plein" data-ferme data-toast="Compte créé — l’invitation vient de partir par e-mail">Créer le compte</button>')
    fer = fenetre('fen-fermer', 'Fermer ce compte ?', '<p>Karim Saidi n’aura plus accès à cet espace de travail. Son appartenance est <strong>révoquée</strong>, pas effacée.</p>',
                  '<button type="button" class="btn btn-contour" data-ferme>Annuler</button><button type="button" class="btn btn-danger-plein" data-ferme data-toast="Compte fermé">Fermer le compte</button>')
    normal = haut + tableau('Utilisateurs', ['Utilisateur', 'Email', 'Rôles', '2FA', 'Dernière connexion', 'Actions'], lig, secondaires=(1, 4))
    P['utilisateurs.html'] = page('utilisateurs', 'Utilisateurs', 'Qui a accès à votre CRM, et <strong>avec quels droits</strong>.', normal,
                                  etat_vide('equipe', 'Aucun utilisateur', 'Aucun autre utilisateur pour l’instant.', btn('Inviter', 'plein', icone='ajout-personne', attrs='data-ouvre="fen-inviter"')),
                                  etat_erreur('La liste des membres de l’espace de travail n’a pas pu être lue.'),
                                  actions=btn('Inviter un utilisateur', 'plein', icone='ajout-personne', attrs='data-ouvre="fen-inviter"'), apres=inv + fer, reprise=F + 'users/UsersPage.tsx')


def _etiquettes():
    def nuage(items, manuelle=False):
        return '<div class="puces-etiq">%s</div>' % ''.join(
            '<span class="puce-etiq"><strong>%s</strong>&nbsp;<span class="chiffre">%s</span>%s</span>' % (E(n), c, (' <a href="campagne-nouvelle.html?cible=etiquette" aria-label="Campagne vers %s" title="Campagne vers cette étiquette">%s</a>' % (E(n), ic('envoi', 'petite'))) if manuelle else '') for n, c in items)
    haut = kpis(kpi('Total', '214', 'diese', 'bleu', 'tous axes confondus'), kpi('Automatiques', '176', 'rafraichir', 'vert', 'géographie, secteur, taille'),
                kpi('Personnalisées', '23', 'note', 'violet', 'créées à la main'), kpi('Proposées par l’IA', '15', 'etincelle', 'ambre', 'suggérées automatiquement'))
    vedette = bloc('salon-artisans-2026', '<p style="margin-bottom:12px"><strong class="chiffre">412 fiches</strong> · 388 joignables · créée le 2 oct.</p>' + jauge('Joignables', 388, 412, 'vert', '388 sur 412'),
                   'violet', 'diese', mot='Choisie', pied=btn('Campagne vers cette étiquette', 'plein', 'campagne-nouvelle.html?cible=etiquette', 'envoi') + btn('Exporter (CSV)', 'petit', icone='export', attrs='data-toast="412 fiches exportées."'))
    sections = ''.join(bloc('%s · %s' % (t, d), nuage(items, man), icone=i, mot=None) for t, d, i, items, man in [
        ('Géographie', 'Région et département (auto)', 'carte', [('Rhône', '4 120'), ('Isère', '2 980'), ('Haute-Savoie', '1 330'), ('Auvergne-Rhône-Alpes', '11 420')], False),
        ('Secteur et métier', 'depuis le code NAF (auto)', 'entreprise', [('Commerce de détail', '6 140'), ('Restauration', '3 210'), ('Bâtiment', '5 020')], False),
        ('Taille', 'Effectif (auto)', 'stats', [('TPE', '39 050'), ('PME', '7 940')], False),
        ('Personnalisées', 'Étiquettes créées à la main', 'note', [('salon-artisans-2026', '412'), ('vip-client', '18'), ('relance-printemps', '96')], True),
        ('Proposées par l’IA', 'suggérées par la classification IA', 'etincelle', [('intérêt-formation', '220'), ('intérêt-site-web', '140')], False)])
    normal = haut + vedette + '<div class="pile" style="margin-top:24px">%s</div>' % sections
    nv = fenetre('fen-etiq', 'Nouvelle étiquette', champ('Nom', 'et-nom', attrs='placeholder="Ex : VIP Client"') + champ('Catégorie', 'et-cat', 'select', ['Personnalisées', 'Géographie', 'Secteur et métier', 'Taille', 'Provenance et intérêt'])
                 + champ('Description (optionnel)', 'et-desc', 'textarea', attrs='placeholder="Notes internes…"'),
                 '<button type="button" class="btn btn-discret" data-ferme>Annuler</button><button type="button" class="btn btn-plein" data-ferme data-toast="Étiquette créée">Créer</button>')
    P['etiquettes.html'] = page('etiquettes', 'Étiquettes', 'Pour classer les entreprises : zone, secteur, taille, intérêt, et les vôtres.', normal,
                                etat_vide('diese', 'Aucune étiquette', 'Aucune étiquette pour l’instant.', btn('Créer une étiquette', 'plein', icone='plus', attrs='data-ouvre="fen-etiq"')),
                                etat_erreur('Les étiquettes n’ont pas pu être lues.'), actions=btn('Nouvelle étiquette', 'contour', icone='plus', attrs='data-ouvre="fen-etiq"'), apres=nv,
                                reprise=F + 'tags/TagsManagerPage.tsx (+ « Campagne vers cette étiquette » : ajout plan 27 n° 5)')


def _rgpd():
    R = [('Accès', 'demandeur-1@exemple.example', ('ambre', 'En attente'), '08/10/2026 10:14', '—', True, '5 jours restants'),
         ('Suppression', 'demandeur-2@exemple.example', ('vert', 'Traitée'), '02/10/2026 09:02', '03/10/2026 11:20', False, ''),
         ('Opposition', 'demandeur-3@exemple.example', ('bleu', 'En traitement'), '28/10/2026 16:45', '—', False, '27 jours restants'),
         ('Rectification', 'demandeur-4@exemple.example', ('gris', 'Rejetée'), '12/09/2026 14:00', '15/09/2026 09:30', False, '')]
    lig = [['<strong>%s</strong>' % t, E(p), badge(s[0], s[1], '●') + ('<span class="sous">%s</span>' % d if d else ''), dm, tr,
            btn('Traiter', 'petit', attrs='data-ouvre="fen-traiter"') if a else '—'] for t, p, s, dm, tr, a, d in R]
    haut = kpis(kpi('En attente', '1', 'horloge', 'ambre', 'plus proche : 5 jours'), kpi('En traitement', '1', 'rafraichir', 'bleu', ''), kpi('Traitées cette année', '14', 'coche', 'vert', 'toutes dans les délais'),
                kpi('Registre des oppositions', '146', 'interdit', 'gris', 'preuve exportable', 'desinscriptions.html'))
    f = filtres(['Toutes', 'Accès · art. 15', 'Portabilité · art. 20', 'Suppression · art. 17', 'Rectification · art. 16', 'Opposition · art. 21'])
    nv = fenetre('fen-rgpd', 'Nouvelle demande RGPD', '<p style="margin-bottom:12px">Enregistrer à la main une demande faite par une personne.</p>' + champ('Type', 'rg-type', 'select', ['Suppression (art. 17)', 'Accès (art. 15)', 'Portabilité (art. 20)', 'Rectification (art. 16)', 'Opposition (art. 21)'])
                 + champ('E-mail de la personne', 'rg-mail', 'email', attrs='placeholder="personne.concernee@exemple.com"'),
                 '<button type="button" class="btn btn-contour" data-ferme>Annuler</button><button type="button" class="btn btn-plein" data-ferme data-toast="Requête RGPD créée">Créer</button>')
    tr = fenetre('fen-traiter', 'Traiter la demande', '<p class="petit" style="margin-bottom:12px">ACCESS · demandeur-1@exemple.example</p>' + champ('Note interne (optionnelle)', 'rg-note', 'textarea', attrs='placeholder="Action effectuée, données purgées, motif de rejet…"'),
                 '<button type="button" class="btn btn-contour" data-ferme>Annuler</button><button type="button" class="btn btn-plein" data-ferme data-toast="Requête traitée">Marquer comme traitée</button>')
    normal = haut + f + tableau('Demandes RGPD', ['Type', 'Personne', 'Statut', 'Demande', 'Traitement', 'Actions'], lig, secondaires=(4,))
    P['rgpd.html'] = page('rgpd', 'Demandes RGPD', 'Demandes des personnes sur leurs données. <strong>1 en attente</strong>.', normal,
                          etat_vide('bouclier', 'Aucune demande RGPD', 'Les demandes apparaîtront ici dès qu’une personne en fera une.', btn('Créer une requête', 'plein', icone='plus', attrs='data-ouvre="fen-rgpd"')),
                          etat_erreur('Les demandes RGPD n’ont pas pu être lues.'),
                          actions=btn('Exporter le registre des oppositions', 'contour', icone='export', attrs='data-toast="Registre exporté (CSV signé) : ajout plan 27 n° 15."') + btn('Nouvelle requête', 'plein', icone='fichier', attrs='data-ouvre="fen-rgpd"'),
                          apres=nv + tr, reprise=F + 'rgpd/RgpdRequestsPage.tsx')


# ======================= TECHNIQUE =======================
def _roumanie():
    R = [('Ateliers Franco-Roumains', 'Entreprise', 'Bucarest', 'contact@afr.example', True), ('Chambre de commerce franco-roumaine', 'Chambre de commerce', 'Bucarest', 'info@ccfr.example', True),
         ('Lycée français de Cluj', 'Enseignement', 'Cluj-Napoca', '—', False), ('Cabinet Conseil Danube', 'Cabinet (conseil, avocats)', 'Timișoara', 'bureau@danube.example', True)]
    lig = [['<a href="entreprise.html"><strong>%s</strong></a>' % E(n), E(na), E(v), E(m), '<span class="mono">+40 000 000 000</span>' if ok else '—', '<a href="#">Voir</a>' if ok else '—',
            badge('vert', 'Contactable', '✓') if ok else '<span class="petit">Sans e-mail</span>'] for n, na, v, m, ok in R]
    haut = kpis(kpi('Fiches', '612', 'domaine', 'bleu', 'annuaire public'), kpi('Contactables', '388', 'coche', 'vert', ''), kpi('Sans e-mail', '224', 'message', 'gris', ''))
    f = filtres(['Tout', 'Entreprise', 'Association', 'Chambre de commerce', 'Enseignement', 'Cabinet (conseil, avocats)', 'Institution', 'Média', 'Réseau ou club d’affaires', 'Organisation professionnelle'])
    ong = '<nav class="onglets" aria-label="Statut de prospection"><a href="roumanie.html" aria-current="page">Tous</a><a href="#">Prospectables</a><a href="#">Partiels</a><a href="#">À compléter</a><a href="#">Archivés</a></nav>'
    normal = haut + f + ong + '<p class="petit" style="margin-bottom:8px">612 fiches</p>' + tableau('Roumanie', ['Dénomination', 'Nature', 'Ville', 'E-mail', 'Téléphone', 'Site', 'Statut'], lig, secondaires=(1, 4, 5)) + pagination('Page 1', False)
    P['roumanie.html'] = page('roumanie', 'Entreprises en Roumanie', 'Entreprises françaises implantées, entités locales et organismes francophones.', normal,
                              erreur=etat_erreur('Impossible de charger le vivier Roumanie.'), reprise=F + 'international/RoumaniePage.tsx')


def _historique():
    R = [('INSEE Sirene', '69', ('bleu', 'En cours'), '<strong>38</strong>/100', 'il y a 12s', 'arret'), ('France Travail', '69', ('vert', 'Terminé'), '<strong>30</strong>/30', 'il y a 5m', ''),
         ('INSEE Sirene', '38', ('rouge', 'Échec'), '—', 'il y a 3h', 'rafraichir'), ('INSEE Sirene', '73', ('vert', 'Terminé'), '<strong>100</strong>/100', 'il y a 2j', ''), ('BAN géocodage', '74', ('gris', 'Annulé'), '<strong>12</strong>/?', 'il y a 2j', 'rafraichir')]
    act = {'arret': btn('Annuler', 'petit-discret', icone='stop-carre', attrs='data-ouvre="fen-annuler-passage"'), 'rafraichir': btn('Relancer', 'petit-discret', icone='rafraichir', attrs='data-toast="Passage n° 4410 relancé"'), '': ''}
    lig = [['<strong>%s</strong>' % s, '<span class="mono">%s</span>' % z, badge(st[0], st[1], '●'), e, d, act[a]] for s, z, st, e, d, a in R]
    haut = kpis(kpi('Total', '418', 'sante', 'bleu', 'passages sur la période'), kpi('En cours', '1', 'lecture', 'violet', '+ 2 en attente'),
                kpi('Taux de succès', '94 %', 'coche', 'vert', '386 OK / 410 clos', graph=jauge('Succès', 94, 100, 'vert', '94 %')), kpi('Échecs', '24', 'alerte', 'rouge', 'à relancer'))
    f = filtres(['Tous · 418', 'En cours · 1', 'En attente · 2', 'Terminés · 386', 'Échec · 24', 'Annulés · 5']) + filtres_champs([('r', 'Recherche', 'Rechercher source, dept, id…', 'h-q')], '<span class="petit">418 passages</span>')
    fen = fenetre('fen-annuler-passage', 'Annuler ce passage ?', '<p>Passage n° 4411 · source INSEE Sirene. Les traitements en cours seront interrompus.</p>',
                  '<button type="button" class="btn btn-discret" data-ferme>Garder</button><button type="button" class="btn btn-danger-plein" data-ferme data-toast="Passage n° 4411 annulé">Annuler le passage</button>')
    normal = '<div class="bandeau bleu">%s<span>En direct · mis à jour toutes les 10 secondes</span></div>' % ic('rafraichir') + haut + f + tableau('Passages', ['Source', 'Zone', 'Statut', 'Entreprises', 'Démarré', 'Actions'], lig) + pagination('Page 1 / 28 · 418 passages', False)
    P['historique-collectes.html'] = page('historique-collectes', 'Historique des collectes', 'Chaque passage de collecte, en direct : <strong>en cours, terminés, en échec</strong>.', normal,
                                          etat_vide('fusee', 'Aucun passage pour l’instant', 'Aucun passage de collecte enregistré pour l’instant.', btn('Récupérer des entreprises', 'plein', 'carte-france.html', 'carte')),
                                          etat_erreur('L’historique des collectes n’a pas pu être lu.'), actions=btn('Exporter en CSV', 'contour', icone='export', attrs='data-toast="Export CSV téléchargé"'),
                                          apres=fen, reprise=F + 'scraping/ScraperRunsPage.tsx')


def _sante_systeme():
    haut = kpis(kpi('Erreurs d’enrichissement (24 h)', '3', 'alerte', 'gris', ''), kpi('Quota fiches locales (mois)', '8 400', 'carte', 'bleu', '70 % utilisé', unite='/ 12 000', graph=jauge('Quota', 8400, 12000, 'bleu', '70 %')),
                kpi('Quota vérification e-mail (mois)', '410', 'message', 'ambre', '82 % utilisé', unite='/ 500', graph=jauge('Quota', 410, 500, 'ambre', '82 %')),
                kpi('Entreprises archivées', '1 121', 'sauvegarde', 'gris', ''), kpi('Échecs de mise à jour d’audience (7 j)', '0', 'coche', 'vert', ''))
    arch = bloc('Archivages par raison', chiffres([('612', 'Entreprise radiée'), ('301', 'Sans e-mail'), ('142', 'Score de qualité trop bas'), ('48', 'Doublon'), ('18', 'Archivée à la main')]), icone='sauvegarde')
    ev = bloc('50 derniers événements', tableau('Événements', ['Date', 'Action', 'Élément'], [['01/11/2026 10:41', 'Enrichissement terminé', '<a href="entreprise.html">Entreprise n° 48 120</a>'],
                                                                                         ['01/11/2026 04:00', 'Audience mise à jour', '<a href="audience.html">Audience n° 3</a>'], ['31/10/2026 22:10', 'Adresse vérifiée', 'Adresse e-mail [masquée]']]), icone='journal')
    sauv = bloc('Sauvegardes', verdict_global('Sauvegarde de cette nuit réussie', '03:00 · copie chiffrée · copie hors site vérifiée', 'vert', 'sauvegarde')
                + chiffres([('03:00', 'dernière'), ('30 j', 'gardés'), ('12 oct.', 'dernier exercice de restauration')]), 'vert', 'sauvegarde', mot='Carte', attrs='id="sauvegardes"',
                pied=btn('Lancer un exercice de restauration', 'petit', icone='rafraichir', attrs='data-toast="Exercice programmé cette nuit."'))
    regl = bloc('Réglages techniques', '<div class="bandeau gris" style="border-color:var(--cadre);background:var(--gris-fond);color:var(--gris-texte)">Ces clés sont des <strong>secrets du serveur</strong>. Cet écran ne peut pas dire lesquelles sont renseignées, ni les modifier.</div>'
                + '<div class="grille deux">%s</div>' % ''.join('<div class="carte"><p class="petit mono">[masqué]_API_KEY</p><p style="display:flex;gap:8px;flex-wrap:wrap;align-items:center;justify-content:space-between"><strong>%s</strong>%s</p><p class="petit">%s</p></div>' % (t, badge(c, r, '●'), d) for t, r, c, d in [
                    ('Base entreprises officielle', 'Requise', 'vert', 'Base entreprises + données légales (gratuit)'), ('Service public de l’emploi', 'Requise', 'vert', 'Offres d’emploi + intentions de recrutement'),
                    ('IA principale', 'Requise', 'vert', 'Classe les entreprises par activité (hébergée en France)'), ('IA d’appoint', 'Optionnelle', 'bleu', 'Pour les tâches les plus délicates'),
                    ('Service de fiches locales', 'Optionnelle', 'bleu', 'Téléphone, horaires, site'), ('Serveurs relais', 'Plus tard', 'ambre', 'Pages Jaunes (plus tard)')]), icone='cle')
    normal = haut + '<div class="grille deux">%s%s</div>' % (arch, sauv) + ev + regl
    P['sante-systeme.html'] = page('sante-systeme', 'Santé du système', 'Les traitements automatiques tournent-ils bien ? <strong>Quotas, archivages, erreurs.</strong>', normal,
                                   erreur=etat_erreur('La santé du système n’a pas pu être lue.'),
                                   reprise=F + 'observability/ObservabilityPage.tsx (+ settings/ReglagesTechniques.tsx ; carte Sauvegardes : nouvelle)')


def _moteurs_ia():
    cas = tableau('Cas d’usage', ['Cas d’usage', 'Fournisseur', 'Modèle', 'Chaîne de repli', 'Plafond €', 'État'], [
        ['<span class="mono">classement_naf</span>', 'Fournisseur A', '<span class="mono">modele-a-moyen</span>', 'A → B', '15', badge('vert', 'Actif', '●')],
        ['<span class="mono">lecture_site</span>', 'Fournisseur A', '<span class="mono">modele-a-petit</span>', 'A → B → C', '10', badge('vert', 'Actif', '●')],
        ['<span class="mono">tri_reponses</span>', 'Fournisseur B', '<span class="mono">modele-b</span>', '—', '5', badge('gris', 'Arrêté', '○')]], secondaires=(2, 3))
    four = '<div class="grille trois">%s</div>' % ''.join(bloc('Fournisseur %s' % x, dl([('Clé d’accès', '<span class="mono">••••••••</span>'), ('Cas d’usage routés', n)], False), 'vert', 'robot', mot='Actif') for x, n in [('A', '4'), ('B', '2'), ('C', '1')])
    prompts = '<div class="grille trois">%s</div>' % ''.join(bloc(p, '<p class="petit">%s</p>' % d, icone='fichier', mot=None) for p, d in [('classement_naf v3', 'Classe une activité en clair.'), ('lecture_site v2', 'Lit les mentions légales.')])
    usage = kpis(kpi('Coût total 30j', '18,40 €', 'stats', 'violet', ''), kpi('Texte envoyé (24 h)', '1,2 M', 'envoi', 'bleu', 'estimé'), kpi('Texte reçu (24 h)', '0,3 M', 'reponses', 'vert', 'estimé'), kpi('Cas d’usage actifs', '6', 'robot', 'ambre', 'dernières 30j')) + bloc('Coût par fournisseur', jauge('Fournisseur A', 74, 100, 'violet', '13,60 € · 74 %') + jauge('Fournisseur B', 26, 100, 'violet', '4,80 € · 26 %'), icone='stats')
    normal = onglets('Moteurs', [('cas', 'Cas d’usage <span class="nb">7</span>', cas), ('four', 'Fournisseurs', four), ('pr', 'Prompts', prompts), ('us', 'Usage 30j', usage)])
    P['moteurs-ia.html'] = page('moteurs-ia', 'Moteurs d’IA', 'Quelle IA sert à quoi, avec quelle solution de secours et <strong>pour quel coût</strong>.', normal,
                                etat_vide('robot', 'Aucun cas d’usage configuré', 'Les usages de l’IA sont créés à l’installation du serveur.', ''), etat_erreur('Les moteurs d’IA n’ont pas pu être lus.'), reprise=F + 'llm/LlmRouterPage.tsx')


def _relais():
    lig = [['<strong>relais-%s</strong>' % i, badge(t, ty, '●'), '<span class="mono">%s</span>' % z, n, badge('vert', 'healthy', '●') + '<span class="sous">01/11 10:30</span>', p, btn('Tester', 'petit', attrs='data-toast="Opérationnel"')]
           for i, ty, t, z, n, p in [('a', 'residential', 'bleu', 'fr', '120', '3'), ('b', 'datacenter', 'vert', 'eu', '40', '1')]]
    normal = kpis(kpi('Fournisseurs', '2', 'reseau', 'bleu', ''), kpi('En bonne santé', '2', 'coche', 'vert', 'sur 2')) + tableau('Serveurs relais', ['Identifiant', 'Type', 'Zone', 'Points de sortie', 'État de santé', 'Poids', 'Actions'], lig, secondaires=(2, 5))
    P['serveurs-relais.html'] = page('serveurs-relais', 'Serveurs relais', 'Fournisseurs d’adresses réseau utilisés <strong>pour la collecte</strong>.', normal,
                                     etat_vide('domaine', 'Aucun fournisseur configuré', 'Aucun fournisseur de serveurs relais n’est configuré sur le serveur.', ''), etat_erreur('Les fournisseurs de proxies n’ont pas pu être lus.'),
                                     reprise=F + 'llm/ProxyProvidersPage.tsx')


def _rotation():
    def carte(titre, rows):
        t = tableau(titre, ['Identifiant', 'Poids', 'Délai d’attente', 'État', 'Dernière utilisation'], [['<span class="mono">%s</span>' % a, b, c, badge('vert', 'Actif', '●') if d else badge('gris', 'Arrêté', '○'), e] for a, b, c, d, e in rows]) if rows else '<p class="petit">Aucune rotation configurée pour cette dimension.</p>'
        return bloc(titre, t, icone='rafraichir', mot=None)
    normal = '<div class="pile">%s%s%s%s%s</div>' % (carte('Serveur relais', [('relais-a', '3', '30s', True, '01/11 10:41'), ('relais-b', '1', '30s', True, '01/11 09:12')]),
                                                     carte('User-agent', [('navigateur-1', '1', '10s', True, '01/11 10:41')]), carte('Cible', []),
                                                     carte('Moteur de recherche', [('moteur-1', '1', '20s', False, 'Jamais')]), carte('Fournisseur d’IA', [('fournisseur-a', '3', '60s', True, '01/11 10:40')]))
    P['rotation-acces.html'] = page('rotation-acces', 'Rotation des accès', 'Les accès qui tournent <strong>pour ne pas être bloqué</strong>.', normal,
                                    etat_vide('rafraichir', 'Aucune rotation configurée', 'Aucune rotation n’est configurée sur le serveur.', ''), etat_erreur('Les rotations n’ont pas pu être lues.'), reprise=F + 'llm/RotationsPage.tsx')


def _registre_ia():
    RISQ = {'Élevé': 'ambre', 'Limité': 'bleu', 'Faible': 'vert'}
    lig = [['<strong>%s</strong><span class="sous">%s</span>' % (n, f), badge(RISQ[r], r, '▲' if r == 'Élevé' else '●'), 'Fournisseur A<span class="sous mono">%s</span>' % m, badge(sc, s, '●'), resp, d]
           for n, f, r, m, s, sc, resp, d in [('Tri des réponses', 'Classer les réponses reçues', 'Limité', 'modele-a-petit', 'production', 'vert', 'Will', '12/09/2026'),
                                               ('Classement d’activité', 'Lire le code NAF en clair', 'Faible', 'modele-a-moyen', 'production', 'vert', 'Will', '12/09/2026'),
                                               ('Score de priorité', 'Proposer qui appeler en premier', 'Élevé', 'modele-b', 'draft', 'gris', '—', '—')]]
    haut = kpis(kpi('Total registres', '3', 'robot', 'gris', ''), kpi('Risque élevé', '1', 'alerte', 'rouge', 'dont prohibés : 0'), kpi('En production', '2', 'coche', 'vert', '67 % des systèmes'), kpi('Dernière revue', '12/09/2026', 'calendrier', 'ambre', 'Annuelle obligatoire'))
    normal = '<div class="bandeau bleu">%s<span>Un outil au niveau de risque <strong>élevé</strong> doit être décrit ici en détail : analyse des risques, mesures, contrôle humain, révision annuelle.</span></div>' % ic('fichier') + haut + tableau('Registre', ['Cas d’usage', 'Risque', 'Fournisseur · Modèle', 'Statut', 'Responsable', 'Dernière revue'], lig, secondaires=(2, 4))
    P['registre-ia.html'] = page('registre-ia', 'Registre de l’IA', 'Les outils d’IA utilisés et <strong>leur niveau de risque</strong>.', normal,
                                 etat_vide('robot', 'Aucun système IA enregistré', 'Les outils d’IA apparaissent ici une fois le serveur installé.', ''), etat_erreur('Le registre des outils d’IA n’a pas pu être lu.'),
                                 reprise=F + 'rgpd/AiActRegisterPage.tsx')


def _journal():
    G = {'info': 'bleu', 'warning': 'ambre', 'critical': 'rouge'}
    lig = [[q, '<strong>%s</strong>' % e, '<span class="mono">%s</span>' % s, a, badge(G[g], g, '●'), '<span class="mono">[masquée]</span>', '<span class="mono">%s…</span>' % h]
           for q, e, s, a, g, h in [('01/11 10:42', 'campagne.validee', '/campagnes/12', 'Will', 'info', '9f2c41ab07de'), ('01/11 09:15', 'connexion.reussie', '/login', 'Sophie Renard', 'info', '1b77e0c4d2aa'),
                                    ('31/10 18:02', 'export.entreprises', '/companies', 'Will', 'warning', 'c40d19e3f5b1'), ('31/10 08:00', 'rgpd.suppression', '/rgpd/requests', 'Will', 'critical', '7ae2b0d9c311')]]
    f = filtres_champs([('r', 'Recherche', 'Événement, écran, adresse IP, auteur…', 'jo-q'), ('s', 'Gravité', ['Toutes', 'Info', 'Attention', 'Erreur', 'Critique'], 'jo-g')])
    haut = kpis(kpi('Actions aujourd’hui', '86', 'journal', 'bleu', ''), kpi('Chaîne d’empreintes', 'Intacte', 'bouclier', 'vert', 'vérifiée cette nuit'), kpi('Critiques (30 j)', '2', 'alerte', 'rouge', ''))
    normal = haut + f + tableau('Journal', ['Quand', 'Événement', 'Écran ou action', 'Acteur', 'Gravité', 'Adresse IP', 'Empreinte'], lig, secondaires=(2, 5, 6))
    P['journal.html'] = page('journal', 'Journal des actions', 'Qui a fait quoi, et quand. <strong>Rien ne peut y être effacé.</strong>', normal,
                             etat_vide('parchemin', 'Aucun journal d’audit', 'Les actions sensibles seront inscrites ici, sans possibilité d’effacement.', ''), etat_erreur('Les journaux d’audit n’ont pas pu être lus.'),
                             actions=btn('Exporter (code par e-mail)', 'contour', icone='export', attrs='data-toast="Code envoyé par e-mail pour confirmer l’export."') + btn('Vérifier que rien n’a été modifié', 'plein', icone='bouclier', attrs='data-toast="Aucune modification détectée."'),
                             reprise=F + 'rgpd/AuditLogsPage.tsx')


# ======================= HORS COQUILLE =======================
def _connexion():
    def carte(titre, desc, corps):
        return '<div class="carte-seule" style="margin:0 auto"><div class="barre-marque" style="justify-content:center;margin-bottom:16px"><span class="barre-logo" aria-hidden="true">A</span><strong>Axion CRM Pro</strong></div><h1 style="text-align:center">%s</h1><p class="petit" style="text-align:center;margin:6px 0 18px">%s</p>%s</div>' % (titre, desc, corps)
    login = carte('Connexion', 'Accédez à votre CRM.', champ('Adresse e-mail', 'lg-mail', 'email') + champ('Mot de passe', 'lg-mdp', 'password') + '<label class="case"><input type="checkbox" checked> Se souvenir de moi</label>'
                  + '<button type="button" class="btn btn-plein large" data-toast="Code envoyé par e-mail.">Se connecter</button><p style="display:flex;justify-content:space-between;gap:8px;flex-wrap:wrap;margin-top:14px"><a href="#">Recevoir un lien de connexion</a><a href="#">Mot de passe oublié ?</a></p>')
    code = carte('Code à 6 chiffres', 'Saisissez le code reçu par e-mail (collage accepté).', '<div class="cases-code" style="justify-content:center">%s</div>' % ''.join('<input type="text" inputmode="numeric" maxlength="1" aria-label="Chiffre %d">' % (i + 1) for i in range(6))
                 + '<label class="case"><input type="checkbox"> Faire confiance à cet appareil 30 jours</label><button type="button" class="btn btn-plein large" data-toast="Connecté.">Vérifier</button><p style="text-align:center;margin-top:14px"><a href="#">Retour à la connexion</a></p>')
    lien = carte('Recevoir un lien de connexion', 'Recevez un lien de connexion par e-mail, sans mot de passe.', champ('Adresse e-mail', 'ml-mail', 'email', attrs='placeholder="prenom.nom@exemple.com"') + '<button type="button" class="btn btn-plein large" data-toast="Lien envoyé. Consultez votre boîte de réception.">Envoyer le lien</button>')
    oubli = carte('Réinitialiser le mot de passe', 'Indiquez votre adresse e-mail : nous vous envoyons un lien.', champ('Email', 'pr-mail', 'email', attrs='placeholder="prenom.nom@exemple.com"') + '<button type="button" class="btn btn-plein large" data-toast="Email envoyé">Envoyer le lien</button>')
    contenu = '<div style="width:min(560px,100%)">' + onglets('Écrans de connexion', [('login', 'Connexion', login), ('code', 'Code', code), ('lien', 'Lien', lien), ('oubli', 'Mot de passe oublié', oubli)]) + '</div>'
    P['connexion.html'] = ecran_seul('Connexion', contenu, cle='connexion', reprise=F + 'auth/LoginPage.tsx, TwoFactorPage.tsx, MagicLinkPage.tsx, PasswordResetPage.tsx')


def _introuvable():
    contenu = '<div class="carte-seule" style="text-align:center">%s<h1 style="margin:12px 0 8px">Page introuvable</h1><p class="petit" style="margin-bottom:18px">Ce lien est ancien ou a changé d’adresse.</p>%s</div>' % (
        ic('aide', 'grande'), btn('Retour au tableau de bord', 'plein', 'index.html', 'accueil'))
    P['introuvable.html'] = ecran_seul('Page introuvable', contenu, cle='introuvable', reprise=F + 'misc/NotFoundPage.tsx')


for _f in (_parametres, _compte, _utilisateurs, _etiquettes, _rgpd, _roumanie, _historique, _sante_systeme, _moteurs_ia, _relais, _rotation, _registre_ia, _journal, _connexion, _introuvable):
    _f()
