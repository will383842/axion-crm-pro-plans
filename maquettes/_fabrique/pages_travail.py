# -*- coding: utf-8 -*-
"""Pages du groupe « Travailler ». Données factices."""
from socle import *  # noqa: F401,F403

P = {}


# ---------------- Aujourd'hui (tableau de bord) ----------------
def _index():
    normal = (
        tuiles([('Réponses à traiter', '7', 'dont 2 intéressées · il y a 3 min'),
                ('Tâches du jour', '5', '1 en retard'),
                ('À valider', '1', 'campagne « Fédérations T1 »'),
                ('Envoyés hier', '96', 'sur 120 possibles')])
        + '<div class="grille deux">'
        + bloc('Réponses du matin', '<ul class="liste">'
               '<li>%s<span class="quoi"><strong>Claire Durand · Garage Durand</strong><small>« Pouvez-vous me rappeler jeudi ? »</small></span></li>'
               '<li>%s<span class="quoi"><strong>Hugo Petit · Club de voile du Lac</strong><small>« Envoyez-moi une proposition. »</small></span></li>'
               '<li>%s<span class="quoi"><strong>5 autres réponses</strong><small>3 absences, 1 STOP, 1 à rattacher</small></span></li></ul>'
               % (badge('terracotta', 'Intéressé'), badge('terracotta', 'Intéressé'), badge('gris', 'À trier', '○')),
               'terracotta', 'reponses', pied=btn('Traiter les réponses', 'plein', 'reponses.html', 'fleche'),
               attrs='aria-label="Réponses du matin"')
        + bloc('Mes tâches du jour', '<ul class="liste">'
               '<li><input type="checkbox" aria-label="Marquer faite : Appeler Claire Durand" data-toast="Tâche faite." data-annulable style="width:20px;height:20px"><span class="quoi"><strong>Appeler Claire Durand</strong><small>Avant 11:00 · Garage Durand</small></span>%s</li>'
               '<li><input type="checkbox" aria-label="Marquer faite : Envoyer le devis" data-toast="Tâche faite." data-annulable style="width:20px;height:20px"><span class="quoi"><strong>Envoyer le devis</strong><small>Club de voile du Lac</small></span></li>'
               '<li><input type="checkbox" aria-label="Marquer faite : Relancer la fédération" data-toast="Tâche faite." data-annulable style="width:20px;height:20px"><span class="quoi"><strong>Relancer la fédération</strong><small>En retard depuis hier</small></span>%s</li></ul>'
               % (badge('bleu', '11:00', '◷'), badge('rouge', 'En retard', '■')),
               'bleu', 'taches', pied=btn('Voir toutes les tâches', 'petit', 'taches.html'))
        + '</div><div class="grille trois" style="margin-top:16px">'
        + bloc('Campagne à valider', '<p><strong>Fédérations T1</strong> · 84 personnes · message n° 2</p><p class="petit" style="margin-top:6px">Contrôles : 7 sur 7 au vert.</p>',
               'terracotta', 'campagne', pied=btn('Relire et valider', 'petit', 'campagne-suivi.html'))
        + bloc('Santé des envois', '<p>%s 4 boîtes sur 4 prêtes.</p><p class="petit" style="margin-top:6px">Volume possible aujourd’hui : 120. Test du matin réussi à 07:05.</p>' % feu('vert'),
               'vert', 'sante', pied=btn('Voir le détail', 'petit', 'sante.html'))
        + bloc('Mise en route : 3 sur 5', '<div class="barre-progression" role="progressbar" aria-valuemin="0" aria-valuemax="5" aria-valuenow="3" aria-label="Mise en route : 3 jalons faits sur 5"><span style="width:60%"></span></div><p class="petit" style="margin-top:10px">Suivant : premier message (≈ 10 min).</p>',
               'violet', 'etincelle', pied=btn('Continuer la mise en route', 'petit', 'mise-en-route.html'))
        + '</div>'
        + bloc('À valider venant du site', '<ul class="liste"><li>%s<span class="quoi"><strong>3 propositions de fiches</strong><small>Venues de la console du site</small></span><a class="btn btn-discret petit-btn" href="a-valider.html">Ouvrir</a></li>'
               '<li>%s<span class="quoi"><strong>2 personnes à rattacher</strong><small>Même e-mail, deux fiches possibles</small></span><a class="btn btn-discret petit-btn" href="a-valider.html#rattacher">Ouvrir</a></li></ul>' % (badge('gris', '3', '○'), badge('gris', '2', '○')),
               'gris', 'liste')
    )
    vide = etat_vide('taches', 'Rien à faire aujourd’hui', 'Aucune réponse, aucune tâche, aucune alerte. Profitez-en pour préparer la prochaine campagne.', btn('Créer une campagne', 'plein', 'campagne-nouvelle.html'))
    P['index.html'] = page('index', 'Aujourd’hui', 'Bonjour Will. <strong>7 réponses</strong> et <strong>5 tâches</strong> vous attendent. Envois : tout va bien.',
                           normal, vide, actions=btn('Nouvelle campagne', 'contour', 'campagne-nouvelle.html', 'plus'))


# ---------------- Contacts (personnes) ----------------
_PERS = [('Paul Martin', 'Boulangerie Martin', 'Gérant', 'Contacté', 'vert', 'Joignable'),
         ('Claire Durand', 'Garage Durand', 'Dirigeante', 'Répondu', 'vert', 'Joignable'),
         ('Hugo Petit', 'Club de voile du Lac', 'Président', 'Rendez-vous', 'vert', 'Joignable'),
         ('Inès Moreau', 'Fédération des Fêtes de Village', 'Secrétaire', 'À contacter', 'ambre', 'À revérifier'),
         ('Louis Bernard', 'Atelier Bernard', 'Artisan', 'Perdu', 'gris', 'Ne plus écrire')]


def _contacts():
    lignes = []
    for n, e, r, et, f, j in _PERS:
        lignes.append(['<input type="checkbox" aria-label="Choisir %s" style="width:20px;height:20px;vertical-align:middle;margin-right:8px"><a href="contact.html"><strong>%s</strong></a>' % (n, n),
                       '<a href="entreprise.html">%s</a>' % e, r, badge('bleu' if et not in ('Perdu',) else 'gris', et, '◆'),
                       feu(f, j), btn('Ouvrir', 'petit-discret', 'contact.html')])
    liste = (filtres(['Toutes', 'Moi', 'À contacter', 'Ont répondu', 'Ne plus écrire'])
             + tableau('Personnes', ['Personne', 'Entreprise', 'Rôle', 'Étape', 'Joignable', ''], lignes)
             + '<div class="barre-selection" role="region" aria-label="Sélection">2 personnes choisies %s %s %s</div>'
             % (btn('Ajouter à une liste', 'petit'), btn('Ajouter une étiquette', 'petit'), btn('Changer l’étape', 'petit')))
    ajout = fenetre('fen-ajout', 'Ajouter un contact',
                    champ('Prénom et nom', 'aj-nom', valeur='') + champ('E-mail', 'aj-mail', 'email', aide='On vérifie les doublons pendant la saisie.')
                    + champ('Entreprise', 'aj-ent') + champ('Provenance', 'aj-prov', 'select', ['Choisir…', 'Salon', 'Site internet', 'Recommandation', 'Fichier importé'], aide='Obligatoire : d’où vient ce contact ?'),
                    '<button type="button" class="btn btn-contour" data-ferme>Annuler</button><button type="button" class="btn btn-plein" data-ferme data-toast="Contact ajouté.">Ajouter le contact</button>')
    import_ = fenetre('fen-import', 'Importer un fichier',
                      '<ol class="etapes-com" style="margin-bottom:16px"><li aria-current="step">1. Fichier</li><li>2. Colonnes</li><li>3. Contrôle</li></ol>'
                      + champ('Fichier (CSV ou Excel)', 'imp-fichier', 'text', 'contacts-salon-factice.csv') + champ('Provenance', 'imp-prov', 'select', ['Salon des artisans 2026', 'Autre…']),
                      '<button type="button" class="btn btn-contour" data-ferme>Annuler</button><button type="button" class="btn btn-contour" data-ferme data-toast="100 lignes lues : 92 nouvelles, 8 doublons à vérifier.">Continuer : colonnes</button>')
    vide = etat_vide('personnes', 'Aucun contact pour l’instant', 'Importez un fichier ou ajoutez votre premier contact à la main.', btn('Importer un fichier', 'plein', attrs='data-ouvre="fen-import"'))
    P['contacts.html'] = page('contacts', 'Contacts', '<strong>1 248 personnes</strong> · 1 102 joignables · 8 doublons à vérifier.',
                              liste, vide,
                              actions=btn('Importer', 'contour', icone='collecte', attrs='data-ouvre="fen-import"') + btn('Ajouter un contact', 'plein', icone='plus', attrs='id="ajout" data-ouvre="fen-ajout"'),
                              onglets_haut='<nav class="onglets" aria-label="Sections de Contacts"><a href="contacts.html" aria-current="page">Personnes</a><a href="listes.html">Listes</a><a href="listes.html#etiquettes">Étiquettes</a><a href="doublons.html">Doublons (8)</a><a href="a-valider.html">À valider (5)</a></nav>',
                              apres=ajout + import_)


# ---------------- Fiche contact ----------------
def _contact():
    gauche = (bloc('Étape', '<ol class="etapes-com" aria-label="Étapes commerciales"><li class="passe">À contacter</li><li class="passe">Contacté</li><li aria-current="step">Répondu</li><li>Rendez-vous</li><li>Devis</li><li>Gagné</li><li>Perdu</li></ol>')
              + bloc('Historique', '<ol class="chronologie">'
                     '<li><span class="rond">%s</span><strong>Réponse reçue</strong> · hier 16:20<br><small>« Pouvez-vous me rappeler jeudi ? » · classée Intéressé</small></li>'
                     '<li><span class="rond">%s</span><strong>Message 2 envoyé</strong> · 28 oct.<br><small>Campagne Organisateurs Rhône-Alpes · boîte claire@</small></li>'
                     '<li><span class="rond">%s</span><strong>Note</strong> · 20 oct.<br><small>Rencontré au salon, intéressé par l’automatisation des devis.</small></li>'
                     '<li><span class="rond">%s</span><strong>Fiche créée</strong> · 18 oct.<br><small>Provenance : Salon des artisans 2026</small></li></ol>' % (ic('reponses'), ic('envoi'), ic('note'), ic('plus')),
                     pied=btn('Ajouter une note', 'petit', icone='note', attrs='data-ouvre="fen-note"') + btn('Noter un appel', 'petit', icone='telephone', attrs='data-ouvre="fen-note"')))
    droite = (bloc('Coordonnées', '<dl class="infos"><dt>E-mail</dt><dd>claire@garage-durand.example</dd><dt>Téléphone</dt><dd>01 00 00 00 00</dd><dt>Entreprise</dt><dd><a href="entreprise.html">Garage Durand</a></dd><dt>Rôle</dt><dd>Dirigeante</dd><dt>Responsable</dt><dd>Will</dd></dl>')
              + bloc('Peut-on lui écrire ?', '<p>%s Oui. Adresse vérifiée il y a 9 jours.</p><p class="petit" style="margin-top:6px">Information art. 14 donnée le 28 oct.</p>' % feu('vert', 'Joignable'), 'vert', 'bouclier', mot='En règle')
              + bloc('Prochaine tâche', '<p><strong>Rappeler jeudi</strong> · 11:00</p>', 'bleu', 'taches')
              + bloc('Étiquettes', '<p>%s %s</p>' % (badge('gris', 'Salon 2026', '#'), badge('gris', 'Garages', '#')), pied=btn('Ajouter', 'petit-discret', icone='plus')))
    normal = '<div class="fiche"><div>%s</div><div>%s</div></div>' % (gauche, droite)
    note = fenetre('fen-note', 'Ajouter une note', champ('Note', 'note-txt', 'textarea', aide='Visible par l’équipe. Jamais envoyée au contact.'),
                   '<button type="button" class="btn btn-contour" data-ferme>Annuler</button><button type="button" class="btn btn-plein" data-ferme data-toast="Note ajoutée.">Enregistrer la note</button>')
    plus = fenetre('fen-plus', 'Autres actions', '<ul class="liste"><li><span class="quoi"><strong>Modifier la fiche</strong></span>%s</li><li><span class="quoi"><strong>Déclarer un envoi fait à la main</strong><small>Compte dans la pression commerciale</small></span>%s</li><li><span class="quoi"><strong>Enregistrer une opposition</strong><small>Définitif : plus aucun message</small></span>%s</li><li><span class="quoi"><strong>Mettre en corbeille</strong><small>Restaurable à tout moment</small></span>%s</li></ul>'
                   % (btn('Modifier', 'petit'), btn('Déclarer', 'petit'), btn('Enregistrer', 'petit', href='desinscriptions.html'), btn('Mettre en corbeille', 'petit', attrs='data-ferme data-toast="Fiche mise en corbeille." data-annulable')), '<button type="button" class="btn btn-contour" data-ferme>Fermer</button>')
    vide = etat_vide('personne', 'Fiche introuvable', 'Cette personne a peut-être été mise en corbeille. Elle reste restaurable.', btn('Retour aux contacts', 'plein', 'contacts.html'))
    P['contact.html'] = page('contact', 'Claire Durand', 'Dirigeante · <a href="entreprise.html">Garage Durand</a> · a répondu hier, intéressée.', normal, vide,
                             actions=btn('Autres actions', 'contour', attrs='data-ouvre="fen-plus" aria-label="Autres actions"') + btn('Écrire un message', 'contour', icone='message', attrs='data-toast="L’éditeur s’ouvre (même porte d’envoi que les campagnes)."') + btn('Planifier un rappel', 'plein', icone='calendrier', attrs='data-toast="Rappel créé pour jeudi 11:00." data-annulable'),
                             fil=[('Contacts', 'contacts.html', 'contacts')], apres=note + plus)


# ---------------- Entreprises ----------------
_ENT = [('Boulangerie Martin', 'Commerce', 'Lyon (69)', '3', 'Contacté'), ('Garage Durand', 'Automobile', 'Voiron (38)', '2', 'Répondu'),
        ('Club de voile du Lac', 'Association', 'Annecy (74)', '4', 'Rendez-vous'), ('Fédération des Fêtes de Village', 'Fédération', 'Valence (26)', '6', 'À contacter'),
        ('Atelier Bernard', 'Artisanat', 'Chambéry (73)', '1', 'Perdu')]


def _entreprises():
    lignes = [['<a href="entreprise.html"><strong>%s</strong></a>' % n, s, v, '<span class="chiffre">%s</span>' % p, badge('bleu' if e != 'Perdu' else 'gris', e, '◆'), btn('Ouvrir', 'petit-discret', 'entreprise.html')] for n, s, v, p, e in _ENT]
    normal = filtres(['Toutes', 'Moi', 'Commerces', 'Associations', 'Fédérations', 'Événements']) + tableau('Entreprises', ['Entreprise', 'Secteur', 'Ville', 'Personnes', 'Étape', ''], lignes)
    vide = etat_vide('entreprise', 'Aucune entreprise', 'Ajoutez une entreprise ou lancez une collecte de données pour remplir la base.', btn('Ajouter une entreprise', 'plein', attrs='data-toast="Fenêtre d’ajout ouverte."'))
    P['entreprises.html'] = page('entreprises', 'Entreprises', '<strong>412 entreprises</strong> · 37 en discussion · carte et réseaux en onglets.', normal, vide,
                                 actions=btn('Voir la carte', 'contour', 'statistiques.html#carte', 'carte') + btn('Ajouter une entreprise', 'plein', icone='plus', attrs='data-toast="Fenêtre d’ajout ouverte."'),
                                 onglets_haut='<nav class="onglets" aria-label="Sections d’Entreprises"><a href="entreprises.html" aria-current="page">Toutes</a><a href="reseaux.html">Fédérations et ordres</a><a href="reseaux.html#evenements">Événements</a><a href="reseaux.html#international">International</a></nav>')


# ---------------- Fiche entreprise ----------------
def _entreprise():
    pers = tableau('Personnes de l’entreprise', ['Personne', 'Rôle', 'Joignable', ''],
                   [['<a href="contact.html"><strong>Paul Martin</strong></a>', 'Gérant', feu('vert', 'Oui'), btn('Ouvrir', 'petit-discret', 'contact.html')],
                    ['<a href="contact.html"><strong>Julie Martin</strong></a>', 'Comptable', feu('vert', 'Oui'), btn('Ouvrir', 'petit-discret', 'contact.html')],
                    ['<a href="contact.html"><strong>Marc Leroy</strong></a>', 'Vendeur', feu('ambre', 'À revérifier'), btn('Ouvrir', 'petit-discret', 'contact.html')]])
    gauche = (bloc('Affaire en cours', '<p><strong>Automatisation des commandes</strong> · 1 800 € HT · étape Devis</p><div class="barre-progression" style="margin-top:10px" aria-hidden="true"><span style="width:70%"></span></div>', 'bleu', 'affaires', pied=btn('Ouvrir l’affaire', 'petit', 'affaires.html'))
              + bloc('Personnes (3)', pers)
              + bloc('Historique', '<ol class="chronologie"><li><span class="rond">%s</span><strong>Rendez-vous fait</strong> · 30 oct.<br><small>Avec Paul Martin · 30 min</small></li><li><span class="rond">%s</span><strong>Message 1 envoyé</strong> · 21 oct.<br><small>Campagne Commerces de Lyon</small></li><li><span class="rond">%s</span><strong>Questionnaire reçu</strong> · 2 sur 3<br><small>Il manque la réponse de Marc Leroy</small></li></ol>' % (ic('calendrier'), ic('envoi'), ic('taches'))))
    droite = (bloc('Identité', '<dl class="infos"><dt>SIREN</dt><dd>000 000 000 (factice)</dd><dt>Secteur</dt><dd>Commerce de détail</dd><dt>Ville</dt><dd>Lyon (69)</dd><dt>Site</dt><dd>boulangerie-martin.example</dd><dt>Responsable</dt><dd>Will</dd></dl>')
              + bloc('Peut-on lui écrire ?', '<p>%s Oui, 2 personnes sur 3.</p><p class="petit" style="margin-top:6px">Aucune opposition « toute l’organisation ».</p>' % feu('vert', 'Joignable'), 'vert', 'bouclier', mot='En règle')
              + bloc('Campagnes', '<p>%s Commerces de Lyon · arrêtée pour cette entreprise (rendez-vous pris).</p>' % badge('vert', 'Terminée', '✓'), 'gris', 'campagne'))
    normal = '<div class="fiche"><div>%s</div><div>%s</div></div>' % (gauche, droite)
    vide = etat_vide('entreprise', 'Entreprise introuvable', 'Elle a peut-être été fusionnée avec un doublon.', btn('Retour aux entreprises', 'plein', 'entreprises.html'))
    P['entreprise.html'] = page('entreprise', 'Boulangerie Martin', 'Commerce · Lyon · 3 personnes · affaire en cours : <strong>1 800 € HT</strong>.', normal, vide,
                                actions=btn('Ajouter une personne', 'contour', icone='plus', attrs='data-toast="Fenêtre d’ajout ouverte."') + btn('Planifier un rendez-vous', 'plein', icone='calendrier', attrs='data-toast="Lien de rendez-vous copié."'),
                                fil=[('Entreprises', 'entreprises.html', 'entreprises')])


# ---------------- Réseaux : fédérations, événements, international (existant) ----------------
def _reseaux():
    fed = tableau('Fédérations et ordres', ['Nom', 'Type', 'Membres', 'Étape', ''], [
        ['<strong>Fédération des Fêtes de Village</strong>', 'Fédération', '<span class="chiffre">240</span>', badge('bleu', 'À contacter', '◆'), btn('Ouvrir', 'petit-discret', 'entreprise.html')],
        ['<strong>Ordre régional factice</strong>', 'Ordre', '<span class="chiffre">1 100</span>', badge('bleu', 'Contacté', '◆'), btn('Ouvrir', 'petit-discret', 'entreprise.html')]])
    ev = tableau('Événements', ['Événement', 'Date', 'Lieu', 'Organisateur', ''], [
        ['<strong>Fête du Lac 2027</strong>', '12 juin 2027', 'Annecy', 'Club de voile du Lac', btn('Ouvrir', 'petit-discret', 'entreprise.html')],
        ['<strong>Salon des artisans</strong>', '3 mars 2027', 'Lyon', 'Chambre factice', btn('Ouvrir', 'petit-discret', 'entreprise.html')]])
    intl = bloc('Entreprises hors de France', '<p>Consultation seulement : la prospection par e-mail est limitée à la France.</p><p class="petit" style="margin-top:6px">Roumanie : 58 fiches (reprise de l’écran existant).</p>', 'gris', 'domaine', mot='Lecture')
    normal = onglets('Réseaux', [('federations', 'Fédérations et ordres', fed), ('evenements', 'Événements', ev), ('international', 'International', intl)])
    P['reseaux.html'] = page('reseaux', 'Réseaux', '<strong>2 fédérations</strong>, <strong>14 événements</strong> à venir.', normal,
                             etat_vide('entreprise', 'Aucun réseau', 'Ajoutez une fédération ou un événement pour suivre les organisateurs.', btn('Ajouter un réseau', 'plein', attrs='data-toast="Fenêtre d’ajout ouverte."')),
                             actions=btn('Ajouter un réseau', 'plein', icone='plus', attrs='data-toast="Fenêtre d’ajout ouverte."'), fil=[('Entreprises', 'entreprises.html', 'entreprises')])


# ---------------- Listes, listes dynamiques, étiquettes ----------------
def _listes():
    l = tableau('Listes', ['Liste', 'Sorte', 'Personnes', 'Joignables', 'Mise à jour', ''], [
        ['<strong>Organisateurs Rhône-Alpes</strong>', badge('violet', 'Dynamique', '↻'), '<span class="chiffre">312</span>', '<button type="button" class="btn btn-discret petit-btn" data-ouvre="tir-joignables" aria-label="290 joignables : voir le détail">290</button>', 'il y a 2 h', btn('Ouvrir', 'petit-discret')],
        ['<strong>Salon des artisans 2026</strong>', badge('gris', 'Fixe', '■'), '<span class="chiffre">100</span>', '<button type="button" class="btn btn-discret petit-btn" data-ouvre="tir-joignables" aria-label="92 joignables : voir le détail">92</button>', '18 oct.', btn('Ouvrir', 'petit-discret')],
        ['<strong>Fédérations nationales</strong>', badge('violet', 'Dynamique', '↻'), '<span class="chiffre">84</span>', '<button type="button" class="btn btn-discret petit-btn" data-ouvre="tir-joignables" aria-label="80 joignables : voir le détail">80</button>', 'il y a 2 h', btn('Ouvrir', 'petit-discret')]])
    et = '<p>%s %s %s %s</p>' % (badge('gris', 'Salon 2026 · 100', '#'), badge('gris', 'Garages · 34', '#'), badge('gris', 'Associations · 210', '#'), badge('gris', 'Presse · 41', '#'))
    normal = onglets('Listes et étiquettes', [('listes', 'Listes', l), ('etiquettes', 'Étiquettes', bloc('Étiquettes', et, pied=btn('Nouvelle étiquette', 'petit', icone='plus')))])
    tir = tiroir('tir-joignables', 'Joignables : Organisateurs Rhône-Alpes',
                 '<dl class="infos"><dt>Vérifiées (moins de 30 j)</dt><dd>290</dd><dt>À revérifier</dt><dd>14</dd><dt>Refusées</dt><dd>5</dd><dt>Inconnues</dt><dd>3</dd></dl><p class="petit" style="margin-top:16px">Coût estimé de la vérification : 0,17 € (pour information).</p>',
                 '<button type="button" class="btn btn-plein" data-ferme data-toast="Vérification lancée : 17 adresses.">Vérifier les adresses</button>')
    P['listes.html'] = page('listes', 'Listes', '<strong>3 listes</strong> dont 2 dynamiques (mises à jour toutes seules).', normal,
                            etat_vide('liste', 'Aucune liste', 'Une liste dynamique se met à jour toute seule selon vos critères.', btn('Créer une liste dynamique', 'plein', attrs='data-toast="Créateur de liste ouvert."')),
                            actions=btn('Créer une liste', 'plein', icone='plus', attrs='data-toast="Créateur de liste ouvert."'), fil=[('Contacts', 'contacts.html', 'contacts')],
                            onglets_haut='', apres=tir)


# ---------------- Doublons ----------------
def _doublons():
    paire = lambda a, b, raison: bloc('%s / %s' % (a, b), '<p class="petit">%s</p><div class="grille deux" style="margin-top:12px"><div class="bloc"><strong>%s</strong><br><small>Créée le 18 oct. · 3 échanges</small></div><div class="bloc"><strong>%s</strong><br><small>Créée le 2 nov. · 0 échange</small></div></div>' % (raison, a, b),
                                      pied=btn('Fusionner', 'petit', attrs='data-toast="Fiches fusionnées." data-annulable') + btn('Ce ne sont pas les mêmes', 'petit-discret', attrs='data-toast="Paire écartée." data-annulable'))
    normal = paire('Paul Martin', 'P. Martin', 'Même e-mail, même entreprise.') + paire('Garage Durand', 'Garage Durand SARL', 'Même SIREN (factice).')
    P['doublons.html'] = page('doublons', 'Doublons à vérifier', '<strong>8 paires</strong> à vérifier. Rien n’est fusionné sans vous.', normal,
                              etat_vide('doublon', 'Aucun doublon', 'Toutes les fiches sont uniques. Bravo.', btn('Retour aux contacts', 'plein', 'contacts.html')),
                              actions=btn('Fusionner la première paire', 'plein', attrs='data-toast="Fiches fusionnées." data-annulable'), fil=[('Contacts', 'contacts.html', 'contacts')])


# ---------------- À valider (propositions et personnes à rattacher venues du site) ----------------
def _a_valider():
    prop = tableau('Propositions', ['Proposition', 'Source', 'Reçue', ''], [
        ['<strong>Nouvelle fiche : Café des Arts</strong>', 'Formulaire du site', 'il y a 1 h', btn('Accepter', 'petit', attrs='data-toast="Fiche créée." data-annulable')],
        ['<strong>Nouveau téléphone : Garage Durand</strong>', 'Console du site', 'hier', btn('Accepter', 'petit', attrs='data-toast="Fiche mise à jour." data-annulable')]])
    rat = tableau('Personnes à rattacher', ['Personne', 'Fiches possibles', ''], [
        ['<strong>j.martin@boulangerie-martin.example</strong>', 'Julie Martin · Paul Martin', btn('Choisir', 'petit', attrs='data-toast="Personne rattachée." data-annulable')]])
    normal = onglets('À valider', [('propositions', 'Propositions (3)', prop), ('rattacher', 'Personnes à rattacher (2)', rat), ('lettre', 'Lettre et guide', bloc('Abonnés venus du site', '<p>214 abonnés consentants, séparés de la prospection.</p>', 'gris', 'message'))])
    P['a-valider.html'] = page('a-valider', 'À valider', '<strong>5 éléments</strong> venus de la console du site attendent votre accord.', normal,
                               etat_vide('taches', 'Rien à valider', 'Les propositions venues du site apparaîtront ici.', btn('Retour à Aujourd’hui', 'plein', 'index.html')),
                               actions=btn('Accepter la première', 'plein', attrs='data-toast="Fiche créée." data-annulable'), fil=[('Contacts', 'contacts.html', 'contacts')])


# ---------------- Affaires (tableau en colonnes) ----------------
_COLS = [('a-contacter', 'À contacter', [('Atelier Bernard', '600 €')]), ('contacte', 'Contacté', [('Fédération des Fêtes', '2 400 €'), ('Café des Arts', '900 €')]),
         ('repondu', 'Répondu', [('Garage Durand', '1 200 €')]), ('rdv', 'Rendez-vous', [('Club de voile du Lac', '3 000 €')]),
         ('devis', 'Devis', [('Boulangerie Martin', '1 800 €')]), ('gagne', 'Gagné', []), ('perdu', 'Perdu', [])]


def _affaires():
    options = ''.join('<option value="col-%s">%s</option>' % (c, l) for c, l, _ in _COLS)
    cols = []
    for cid, lib, cartes in _COLS:
        cc = ''.join('<article class="carte-affaire"><a href="entreprise.html">%s</a><span class="petit">%s HT · Will</span><div class="bas"><label class="visuellement-cache" for="dep-%s-%d">Déplacer %s vers</label><select id="dep-%s-%d" data-deplacer style="min-height:36px;padding:4px 8px;width:auto"><option value="">Déplacer vers…</option>%s</select></div></article>'
                     % (n, m, cid, i, n, cid, i, options) for i, (n, m) in enumerate(cartes))
        cols.append('<section class="colonne" id="col-%s" aria-label="%s"><h2><span>%s</span><span class="petit">%d</span></h2><div class="cartes-col">%s</div></section>' % (cid, lib, lib, len(cartes), cc))
    normal = filtres(['Toutes', 'Moi', 'Ce mois-ci']) + '<div class="colonnes">%s</div>' % ''.join(cols)
    P['affaires.html'] = page('affaires', 'Affaires', '<strong>6 affaires</strong> en cours · <strong>9 900 € HT</strong> au total · 1 rendez-vous cette semaine.', normal,
                              etat_vide('affaires', 'Aucune affaire', 'Une affaire naît d’une réponse intéressée ou d’un rendez-vous.', btn('Créer une affaire', 'plein', attrs='data-toast="Fenêtre d’ajout ouverte."')),
                              actions=btn('Vue en liste', 'contour', icone='liste', attrs='data-toast="Vue en liste (téléphone)."') + btn('Créer une affaire', 'plein', icone='plus', attrs='data-toast="Fenêtre d’ajout ouverte."'))


# ---------------- Tâches ----------------
def _taches():
    def t(txt, sous, b, cid):
        return '<li><input type="checkbox" id="%s" style="width:20px;height:20px" data-toast="Tâche faite." data-annulable><label for="%s" class="quoi"><strong>%s</strong><small>%s</small></label>%s</li>' % (cid, cid, txt, sous, b)
    normal = (filtres(['Aujourd’hui (5)', 'En retard (1)', 'Cette semaine', 'Faites'])
              + bloc('En retard', '<ul class="liste">%s</ul>' % t('Relancer la fédération', 'Fédération des Fêtes de Village · prévue hier', badge('rouge', 'En retard', '■'), 't1'), 'terracotta', 'alerte', mot='À faire')
              + bloc('Aujourd’hui', '<ul class="liste">%s%s%s%s</ul>' % (
                  t('Appeler Claire Durand', 'Garage Durand · créée par sa réponse', badge('bleu', '11:00', '◷'), 't2'),
                  t('Envoyer le devis', 'Club de voile du Lac', '', 't3'),
                  t('Préparer le rendez-vous', 'Boulangerie Martin · 15:00', badge('bleu', '15:00', '◷'), 't4'),
                  t('Répondre à la presse', 'Rédaction factice', '', 't5')), 'bleu', 'taches', mot='Prévu'))
    P['taches.html'] = page('taches', 'Tâches', '<strong>5 tâches</strong> aujourd’hui, <strong>1 en retard</strong>. Rappel du matin envoyé par e-mail à 08:00.', normal,
                            etat_vide('taches', 'Aucune tâche', 'Les réponses intéressées créent des tâches toutes seules.', btn('Ajouter une tâche', 'plein', attrs='data-toast="Tâche ajoutée."')),
                            actions=btn('Ajouter une tâche', 'plein', icone='plus', attrs='data-toast="Tâche ajoutée."'))


# ---------------- Mise en route ----------------
def _mise_en_route():
    j = [('Identité de l’expéditeur', '≈ 3 min', 'vert', 'Fait', 'identite.html'),
         ('Premier domaine et première boîte', 'attente : 12 jours (âge du domaine)', 'vert', 'Fait', 'domaines.html'),
         ('Importer ou choisir des contacts', '≈ 5 min', 'vert', 'Fait', 'contacts.html'),
         ('Premier message', '≈ 10 min', 'terracotta', 'À faire', 'message-editeur.html'),
         ('Première campagne validée', '≈ 5 min', 'gris', 'Ensuite', 'campagne-nouvelle.html')]
    li = ''.join('<li>%s<span class="quoi"><strong>%d. %s</strong><small>%s</small></span>%s</li>' % (badge(c, m, '✓' if c == 'vert' else '●'), i + 1, n, d, btn('Ouvrir', 'petit', h)) for i, (n, d, c, m, h) in enumerate(j))
    normal = bloc('5 jalons', '<ul class="liste">%s</ul>' % li, 'violet', 'etincelle', mot='Mise en route') + bloc('À faire hors de l’outil', '<ul class="liste"><li><span class="quoi">Acheter le domaine d’envoi (chez l’hébergeur)</span>%s</li><li><span class="quoi">Créer la boîte chez l’hébergeur des boîtes</span>%s</li></ul>' % (badge('vert', 'Fait', '✓'), badge('vert', 'Fait', '✓')), 'gris', 'outil')
    P['mise-en-route.html'] = page('mise-en-route', 'Mise en route', '<strong>3 jalons sur 5</strong>. Il reste environ 15 minutes de travail.', normal,
                                   actions=btn('Écrire le premier message', 'plein', 'message-editeur.html', 'fleche'), fil=[('Aujourd’hui', 'index.html', 'index')])


for f in (_index, _contacts, _contact, _entreprises, _entreprise, _reseaux, _listes, _doublons, _a_valider, _affaires, _taches, _mise_en_route):
    f()
